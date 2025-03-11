from pwn import *
import re

# 远程服务器地址
HOST = "cs412.epfl.ch"
PORT = 9014

def fun_00101272(arr):
    # 计算2x2矩阵的行列式
    return arr[0] * arr[3] - arr[2] * arr[1]


def process_array(arr):
    if len(arr) != 9:
        raise ValueError("输入数组必须包含9个元素")

    # 转置3x3矩阵
    for i in range(3):
        for j in range(i + 1, 3):
            arr[i * 3 + j], arr[j * 3 + i] = arr[j * 3 + i], arr[i * 3 + j]

    total = 0
    for i in range(3):
        element = arr[i]
        submatrix = []
        for y in range(2):
            for x in range(2):
                row_idx = (y + 1) % 3
                col_idx = (x + i + 1) % 3
                submatrix.append(arr[row_idx * 3 + col_idx])

        det = fun_00101272(submatrix)
        total += det * element

    diagonal_sum = sum(arr[i * 4] for i in range(3))  # 主对角线元素之和

    return total - diagonal_sum

# 连接远程服务器
p = remote(HOST, PORT)

data = p.recv(1024).decode()
print("[*] Received:", data)

match = re.search(r"Values: ([\-\d ]+)", data)
if not match:
    print("Failed to parse values.")
    exit()

values = list(map(int, match.group(1).split()))
print("[*] Received values:", values)

# 计算答案
result = process_array(values)
print(f"[*] Sending answer: {result}")

# 发送答案
p.sendline(str(result).encode('utf-8'))

response = p.recv(1024).decode()
print("[*] Server response:", response)
response = p.recv(1024).decode()
print("[*] Server response:", response)

p.close()