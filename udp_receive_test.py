import socket
import datetime

# 创建UDP套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# 绑定本机地址和端口
server_address = ("192.169.100.227", 2000)
udp_socket.bind(server_address)

print("UDP Server启动，等待数据...")

while True:
    # 接收数据
    data, client_address = udp_socket.recvfrom(102800)

    # 获取当前时间，包括微秒
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # 打印时间和收到的数据
    # print(f"收到来自 {client_address} 的数据：时间：{current_time}")
    # print(repr(data))
    print(f"Time: {current_time} Data: {data.hex()}")

# 关闭套接字
udp_socket.close()

##########################################################################################################
# import socket

# # 创建UDP套接字
# udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # 允许套接字接收广播消息
# udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# # 绑定到特定的IP和端口
# udp_socket.bind(('192.169.100.227', 2000))  # 这里9999是要绑定的端口号

# # 接收数据
# while True:
#     data, addr = udp_socket.recvfrom(102800)  # 1024是接收缓冲区的大小
#     print("Received message: ", data.decode('utf-8'), " from ", addr)

# # 关闭套接字
# udp_socket.close()

