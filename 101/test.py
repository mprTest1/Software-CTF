from pwn import *

# 远程服务器地址
HOST = "cs412.epfl.ch"
PORT = 9020

def test1_1(param):
    if param < 2:
        return 0
    for i in range(2, int(param ** 0.5) + 1):
        if param % i == 0:
            return 0
    return 1

def find_valid_test1():
    for lower in range(2, 0xFFFF - 0x2a):
        upper = lower + 0x2a
        if test1_1(lower) and test1_1(upper):
            result = (upper << 16) | lower
            return result
    return None

def test2(param_1):
    local_38 = [
        0x90c04481,#10010000110000000100010010000001 11101111011111111011111101111111
        0x48189060,#01001000000110001001000001100000 11100111011101110011111100011111
        0x2124280a,#00100001001001000010100000001010 11000111011101110011111100011111
        0x06030314,#00000110000000110000001100010100
        0x80400401,#10000000010000000000010000000001
        0x40101000,#01000000000100000001000000000000
        0x00242008,#00000000001001000010000000001000
        0x04000004,#00000100000000000000000000000100
    ]
    bVar1 = 1
    for local_3c in range(4):
        condition = (local_38[local_3c] & param_1) == local_38[local_3c + 4]
        bVar1 &= condition
    return bVar1

def find_valid_test2():
    for candidate in range(0x00000000, 0xFFFFFFFF + 1):
        if test2(candidate):
            return candidate
    return None

local_38 = [
    0x90c04481,
    0x48189060,
    0x2124280a,
    0x06030314,
    0x80400401,
    0x40101000,
    0x00242008,
    0x04000004,
]

def find_fast_mask(local_38):
    mask = 0xFFFFFFFF
    for i in range(4):
        mask &= ~(local_38[i] ^ local_38[i + 4]) | local_38[i + 4]
    return mask

print(find_valid_test1())
#print(find_valid_test2())
print(find_fast_mask(local_38))

assert False
# 测试执行
result = find_valid_test1()
print("符合条件的值(十进制)为:", result)

# 已知的正确答案 (假设为示例: 1234-5678-9012-3456)
correct_key = "1234-5678-9012-3456"

# 建立连接
conn = remote(HOST, PORT)

# 接收提示消息
conn.recvuntil(b"activating the program:\n")

# 发送答案
conn.sendline(correct_key.encode())

# 读取服务器返回的所有信息
response = conn.recvall(timeout=2)

# 显示结果
print(response.decode())

# 关闭连接
conn.close()