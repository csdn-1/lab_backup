import json
import pytz
from datetime import datetime, timezone, timedelta
import numpy as np
import argparse
import sys

# 解析传参
parser = argparse.ArgumentParser()
parser.add_argument("-name", type=str, help="Your json file name. only one")

args = parser.parse_args()
file_name=args.name


# 创建一个表示特定日期和时间的datetime对象
begin_time = datetime(2023, 10, 12, 10, 35, 0)
end_time = datetime(2023, 10, 12, 10, 36, 59)

# 创建一个北京时区的时差
beijing_tz = timezone(timedelta(hours=8))

# 将特定日期和时间与时区关联
time1 = begin_time.replace(tzinfo=beijing_tz)
time2 = end_time.replace(tzinfo=beijing_tz)

# 将特定日期和时间转换为Unix时间戳
unix_time_start = time1.timestamp()
unix_time_end = time2.timestamp()

print("开始时间：（北京时区）:", time1)
print("Unix时间戳:", unix_time_start)

print("结束时间：（北京时区）:", time2)
print("Unix时间戳:", unix_time_end)

# 打开JSON文件并加载数据
with open(file_name, 'r') as json_file:
    data = json.load(json_file)

meta = data[0]['meta']
data_list = data[0]['data']

print(meta['name'])

# 提取所有的val值
filtered_data = []

if file_name == "myIPServer:BunchID.json":
    for entry in data_list:
        if unix_time_start <= entry["secs"] <= unix_time_end:
            val = entry['val']
            filtered_data.extend(val)
elif file_name == "myIPServer:FrameNum.json":
    for entry in data_list:
        if unix_time_start <= entry["secs"] <= unix_time_end:
            val = entry['val']
            filtered_data.append(val)
else:
    # 其他情况下返回报错
    print(f"Error: For '{file_name}', no need to use this program")
    sys.exit(1)



# filtered_data = [entry for entry in data_list if unix_time_start <= entry["secs"] <= unix_time_end]

# 转换为NumPy数组
# val_array = np.array([entry["val"] for entry in filtered_data])
val_array = np.array(filtered_data)
# abs_val_array=np.array(filtered_data)


# 取绝对值
abs_val_array = np.abs(val_array)

# 判断数组中相邻两个元素的差的绝对值是否都为1
abs_diff = np.abs(np.diff(abs_val_array))

nonconforming_entries = [entry for entry, diff in zip(filtered_data[:-1], abs_diff) if diff != 1]
print("filtered_data: ",filtered_data)
if nonconforming_entries:
    print("以下元素及其对应的secs值不符合条件：")
    for entry in nonconforming_entries:
        print(f"元素: {entry}, secs值: {entry['secs']}")
else:
    print("所有元素都符合条件。")