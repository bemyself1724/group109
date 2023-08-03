from SM3 import *
import random
from gmssl import sm3,func
import time
def Rho(n):
    x = random.random()
    # h1 = sm3(str(x))
    # h2 = sm3(str(h1))
    h1 = sm3.sm3_hash(func.bytes_to_list(bytes(str(x), encoding='utf-8')))
    h2 = sm3.sm3_hash(func.bytes_to_list(bytes(str(h1), encoding='utf-8')))
    while 1:
        # h1 = sm3(str(h1))
        # h2 = sm3(str(sm3(h2)))
        h1=sm3.sm3_hash(func.bytes_to_list(bytes(str(h1), encoding='utf-8')))
        h2=sm3.sm3_hash(func.bytes_to_list(bytes(str(h2), encoding='utf-8')))
        h2 = sm3.sm3_hash(func.bytes_to_list(bytes(str(h2), encoding='utf-8')))   #步幅为2
        if h1[:n] == h2[:n]:
            if h1!=h2:
                b = time.time()
                print("Found a pair of the first" ,4*n, "bit collisions",h1[:n],"and",h2[:n],"(in hex)")
                print("碰撞用时:", b - a, "s")
                break
            # else:
            #     print("初始选择失败,重新选择")
    return (h1[:n], h2[:n])


while 1:
    n = int(input("寻找前4x位rho碰撞，请输入x："))
    a = time.time()
    if n == 0:
        print("请重新输入")
        continue
    if n == -1:
        break
    Rho(n)