from SM3 import *
import random
from gmssl import sm3,func
import time
def birthday_attack(n):
    while 1:
        x = random.random()
        y = random.random()
        # h1 = sm3(str(x))
        # h2 = sm3(str(y))
        h1 = sm3.sm3_hash(func.bytes_to_list(bytes(str(x), encoding='utf-8')))
        h2 = sm3.sm3_hash(func.bytes_to_list(bytes(str(y), encoding='utf-8')))
        if h1[:n] == h2[:n]:
            if h1!=h2:
                b = time.time()
                print("Found a pair of the first" ,4*n, "bit collisions",h1[:n],"and",h2[:n],"(in hex)")
                print("碰撞用时:", b - a, "s")
                break
    return (h1[:n], h2[:n])


while 1:
    n = int(input("寻找前4x位碰撞，请输入x："))
    a = time.time()
    if n == 0:
        print("请重新输入")
        continue
    if n == -1:
        break
    birthday_attack(n)


