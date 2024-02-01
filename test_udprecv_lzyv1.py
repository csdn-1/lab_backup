import time
import socket
import struct

if __name__=='__main__':

    # 创建udp套接字
    udp_ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # udp_socket.bind(('10.19.49.226',9012))
    #udp_ser_socket.bind(('10.19.51.55',4001))
    udp_ser_socket.bind(('10.19.53.119',4001))
    #255.255.240.0
    print('ready to receive!')

    psize = 2**10
    fmt = "!HH%dQI" %psize

    while True:    
        data = udp_ser_socket.recv(16+16+psize*64+32)
        
        msg = struct.unpack(fmt, data)
        #print(msg)
        print("bunchID: {} {} {} ".format(msg[2], msg[3], msg[4]) )
        # time.sleep(1)
    
    client_socket.close()