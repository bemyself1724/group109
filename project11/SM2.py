import math
from gmssl import sm3
from random import randint
import random
from GEN_k import gen_k
import time

def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def get_xy(a, b):
    if b == 0:
        return 1, 0
    else:
        x1, y1 = get_xy(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
    return x, y

def get_inverse(a, n):
    gcd_ = gcd(a, n)
    if gcd_ == 1:
        x, y = get_xy(a, n)
        return x % n

def EC_add(x1,y1,x2,y2,a,p):           #椭圆曲线上的加法
    if x1==x2 and y1==p-y2:
        return False
    if x1!=x2:
        w=((y2-y1)*get_inverse(x2-x1, p))%p
    else:
        w=(((3*x1*x1+a)%p)*get_inverse(2*y1, p))%p
    x3=(w*w-x1-x2)%p
    y3=(w*(x1-x3)-y1)%p
    return x3,y3

def muti_point(x,y,k,a,p):
    k=bin(k)[2:]
    qx,qy=x,y
    for i in range(1,len(k)):
        qx,qy=EC_add(qx, qy, qx, qy, a, p)
        if k[i]=='1':
            qx,qy=EC_add(qx, qy, x, y, a, p)
    return qx,qy

def kdf(z,klen):
    ct=1
    k=''
    for _ in range(math.ceil(klen/256)):
        k=k+sm3.sm3_hash([i for i in bytes.fromhex(hex(int(z+'{:032b}'.format(ct),2))[2:])])
        ct=ct+1
    k='0'*((256-(len(bin(int(k,16))[2:])%256))%256)+bin(int(k,16))[2:]
    return k[:klen]

#相关参数
p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

dB=randint(1,n-1)
xB,yB=muti_point(gx,gy,dB,a,p)

def encrypt(m):
    m = str(m)
    plen=len(hex(p)[2:])
    m='0'*((4-(len(bin(int(m.encode().hex(),16))[2:])%4))%4)+bin(int(m.encode().hex(),16))[2:]
    klen=len(m)
    while True:
        k=gen_k(m,dB,n)+(random.getrandbits(256)%n)
        x2,y2=muti_point(xB, yB, k, a, p)
        x2,y2='{:0256b}'.format(x2),'{:0256b}'.format(y2)
        t=kdf(x2+y2, klen)
        if int(t,2)!=0:
            break
    x1,y1=muti_point(gx, gy, k, a, p)
    x1,y1=(plen-len(hex(x1)[2:]))*'0'+hex(x1)[2:],(plen-len(hex(y1)[2:]))*'0'+hex(y1)[2:]
    c1='04'+x1+y1
    c2=((klen//4)-len(hex(int(m,2)^int(t,2))[2:]))*'0'+hex(int(m,2)^int(t,2))[2:]
    c3=sm3.sm3_hash([i for i in bytes.fromhex(hex(int(x2+m+y2,2))[2:])])
    return c1,c2,c3

def decrypt(c1,c2,c3,a,b,p):
    c1=c1[2:]
    x1,y1=int(c1[:len(c1)//2],16),int(c1[len(c1)//2:],16)
    if pow(y1,2,p)!=(pow(x1,3,p)+a*x1+b)%p:
        return False
    x2,y2=muti_point(x1, y1, dB, a, p)
    x2,y2='{:0256b}'.format(x2),'{:0256b}'.format(y2)
    klen=len(c2)*4
    t=kdf(x2+y2, klen)
    if int(t,2)==0:
        return False
    m='0'*(klen-len(bin(int(c2,16)^int(t,2))[2:]))+bin(int(c2,16)^int(t,2))[2:]
    u=sm3.sm3_hash([i for i in bytes.fromhex(hex(int(x2+m+y2,2))[2:])])
    if u!=c3:
        return False
    return hex(int(m,2))[2:]


plaintext = [20,20,10,15,10,77]
print('输入明文是:',plaintext)
time1 = time.time()
c1,c2,c3=encrypt(plaintext)
ciphertext=(c1+c2+c3).upper()
time2 = time.time()
print('密文是:')
for i in range(len(ciphertext)):
    print(ciphertext[i*8:(i+1)*8],end=' ')
print("\n")
print("加密用时:", time2 - time1, "s")

time3 = time.time()
m1=decrypt(c1, c2, c3, a, b, p)
m1=str(bytes.fromhex(m1))
m1='\n'.join(m1[2:-1].split('\\n'))
print('解密后明文是:')
print(m1)
time4 = time.time()
print("解密用时:", time4 - time3, "s")
