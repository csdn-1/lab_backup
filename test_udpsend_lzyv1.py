import time
import socket
import struct
import numpy as np

def get_send_msgflowbytes(frameNum, length, data):
    if length != psize:
        print('data lost!')
        pass
    else:
        a = struct.pack("!HH", frameNum, np.uint16(length))
        
        fmt = "!%dQ" %psize
        b = struct.pack(fmt, *data)

        end=0xdeadbeef
        c=struct.pack("!I",end)
        b = a + b+c
        return b

if __name__=='__main__':

    # 创建udp套接字
   
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    #dest_addr = ('10.19.51.55',4001)
    dest_addr = ('10.19.53.119',4001)

    print('Ready to Send!')
    time.sleep(1)
    
    # 记录每包开头的BunchID值
    cnt = 0
    
    # 规定单包BuncnhID个数
    psize = 2**10
    
    # 包头帧号 16 bits
    frameNum = np.uint16(0)


    # BunchID + FPPS 字节长度
    # bfLen = np.uint32(psize * 8)
    # BunchID 48 bits
    # bunchid = 0
    # FPPS 16 bits
    # FPPS = np.uint16(0)
    
    while True:

        data = []
        for x in range(psize):
            x = x * (10**5)
            data.append(np.uint64(cnt+x))
            #curID = np.uint64(cnt + x)
            # print((FPPS & np.uint16(0xFFFF)), " ")
            #curBF = np.uint64((curID << np.uint64(16)) | (FPPS & np.uint16(0xFFFF))) 
            # print(curBF, " ")
            #data.append(curBF)
            #FPPS = np.uint16(curID / (10**6))
            # time.sleep(0.1)
        
        cnt += (psize * (10**5))
        number_of_BunchID=len(data)

        #msg = get_send_msgflowbytes(len(data), data, frameNum, bfLen)  #构建符合要求的数据包格式
        msg = get_send_msgflowbytes(frameNum, number_of_BunchID, data)  #构建符合要求的数据包格式

        print("sending msg -- frameNum: {} total_number: {}  data: {}".format(frameNum, number_of_BunchID, data[0:10]))

        udp_socket.sendto(msg, dest_addr)
        
        frameNum += 1
        # print(bin(671088641), " ")

        # FPPS = np.uint16(frameNum / 10) # 每10个包+1


        time.sleep(0.1)
    
    client_socket.close()
