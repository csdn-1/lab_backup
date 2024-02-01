import struct

# 32位的十六进制数
hex_num = 0xDEADBEEF

# 将十六进制数转换为无符号32位整数
unsigned_int = int(hex_num)

# 使用 'I' 格式字符打包数据
packed_data = struct.pack("!I", unsigned_int)

# 解包数据，得到原来的无符号32位整数
unpacked_data = struct.unpack("!I", packed_data)[0]

print("Hexadecimal number:", hex_num,"type:",type(hex_num))
print("Packed data:", packed_data)
print("Unpacked data:", unpacked_data)
print(int(0xdeadbeef))
print(int(3735928559))