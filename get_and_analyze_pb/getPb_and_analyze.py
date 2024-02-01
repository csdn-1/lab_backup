import numpy as np
import urllib.request
import json
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
import argparse
import sys

# 解析传参
parser = argparse.ArgumentParser()
parser.add_argument("-n", type=str, help="'-n f' for FrameNum, '-n b' for BunchID, '-n e' for End, '-n bn' for BunchIDNum")

args = parser.parse_args()
if args.n=='f':
    target_record="myIPServer:FrameNum"
elif args.n=='b':
    target_record="myIPServer:BunchID"
elif args.n=='e':
    target_record="myIPServer:End"
elif args.n=='bn':
    target_record="myIPServer:BunchIDNum"
else:
    print("Wrong arguement")
    sys.exit(1)


# 自定义时间区间（北京时间）
begin_beijing_time = datetime(2023, 10, 16, 17, 39, 50, tzinfo=timezone(timedelta(hours=8)))
end_beijing_time = datetime(2023, 10, 16, 17, 40, 10, tzinfo=timezone(timedelta(hours=8)))


def beijing_time_to_utc(beijing_time):
    # 定义北京时区
    beijing_tz = timezone(timedelta(hours=8))

    # 将北京时间转换为UTC时间
    utc_time = beijing_time.astimezone(timezone.utc)

    # 格式化为ISO 8601字符串
    iso8601_utc_time = utc_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return iso8601_utc_time


def get_data(begin_beijing_time,end_beijing_time,target_record):

    # 将北京时间转换为UTC时间
    begin_utc_time = beijing_time_to_utc(begin_beijing_time)
    end_utc_time = beijing_time_to_utc(end_beijing_time)

    base_url = "http://10.19.54.232:17668/retrieval/data/getData.json?"
    url = f"{base_url}pv={quote(target_record)}&donotchunk&from={quote(begin_utc_time)}&to={quote(end_utc_time)}"
    req=urllib.request.urlopen(url)
    data = json.load(req)
    a = json.dumps(data, indent=4)
    file_name = f"{target_record}.json"
    with open(file_name, "w") as f:
        f.seek(0)
        f.write(a)
    # print(f"已拉取json文件: {file_name}")
    print(f"已拉取json文件")


def deal_json(begin_beijing_time,end_beijing_time,target_record):

    # 将北京时间转为UNIX标准时间
    begin_unix_time = begin_beijing_time.timestamp()
    end_unix_time = end_beijing_time.timestamp()
    # print(f"Begin unix time: {begin_unix_time}\nEnd unix time: {end_unix_time}")
    file_name = f"{target_record}.json"

    # 打开JSON文件并加载数据
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)

    meta = data[0]['meta']
    data_list = data[0]['data']

    print("json文件中的PV为：", meta['name'])

    nonconforming_entries = []
    checked = []

    if file_name == "myIPServer:BunchID.json":
        for entry in data_list:
            if begin_unix_time <= entry["secs"] <= end_unix_time:
                val = entry['val']

                if len(checked)==0:
                    if not is_conforming(val):
                        nonconforming_entries.append(entry)
                    checked.extend(val)
                else:
                    if not is_conforming(val,checked[-1]):
                        nonconforming_entries.append(entry)
                    checked.extend(val)

    elif file_name == "myIPServer:FrameNum.json":
        for entry in data_list:
            if begin_unix_time <= entry["secs"] <= end_unix_time:
                val = entry['val']
                
                if len(checked)==0:
                    checked.append(val)
                else:
                    if not is_conforming(val,checked[-1]):
                        nonconforming_entries.append(entry)
                    checked.append(val)
    else:
        # 其他情况下返回报错
        print(f"不支持 '{file_name}'，退出程序")
        sys.exit(1)

    # 迭代 nonconforming_entries 并执行相应操作
    if len(nonconforming_entries)==0:
        print("所有数据均无问题")
    else:
        for entry in nonconforming_entries:
            secs_str = f'secs = {entry["secs"]}, nanos = {entry["nanos"]}'
            
            if isinstance(entry["val"], list):
                val_str = ', val = ' + ', '.join(map(str, entry["val"][:3]))
            else:
                val_str = ', val = ' + str(entry["val"])
            
            print(f'{secs_str}{val_str} 的数据存在问题\nval只显示前三位')



def is_conforming(val, prev_val_last=None):
    if isinstance(val,list):
        # 取绝对值(AA接收无符号的FrameNum会把最高位当成符号位，所以要取绝对值)
        val=np.abs(val)

        # 使用NumPy来检查val中的值是否相差为1
        diff = np.abs(np.diff(val))
        
        if prev_val_last is not None and val[0] - prev_val_last != 1:
            return False

        # 使用NumPy来检查val中的值是否都相差为1
        if not np.all(diff == 1):
            return False

        return True
    else:
        if np.abs(np.abs(prev_val_last)-np.abs(val))==1:
            return True
        else:
            return False


print("自定义时间起点:", begin_beijing_time)
print("自定义时间终点:", end_beijing_time)

get_data(begin_beijing_time,end_beijing_time,target_record)
deal_json(begin_beijing_time,end_beijing_time,target_record)


    

# req = urllib.request.urlopen(
#     # FrameNum
#     "http://10.19.54.232:17668/retrieval/data/getData.json?pv=myIPServer%3AFrameNum&donotchunk&from=2023-10-12T10%3A39%3A30.000Z&to=2023-10-12T20%3A22%3A59.000Z"
#     # "http://10.19.54.232:17668/retrieval/data/getData.json?pv=myIPServer%3AFrameNum&donotchunk&from=2023-10-12T2%3A39%3A30.000Z&to=2023-10-12T12%3A22%3A59.000Z"
#     # BunchID
#     # "http://10.19.54.232:17668/retrieval/data/getData.json?pv=myIPServer%3AEnd&donotchunk"
# )
# data = json.load(req)
# a = json.dumps(data, indent=4)
# with open("Pb.json", "w") as f:
# # with open("BunchID_Pb.json", "w") as f:
#     f.seek(0)
#     f.write(a)
