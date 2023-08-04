import math
from gmssl import sm3,func
from random import randint
import hashlib
import time


k = 0
e = 0
p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

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

def SM2_mul(x,y,k,a,p):
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



dB=randint(1,n-1)
xB,yB=SM2_mul(gx,gy,dB,a,p)
k = randint(1, n)       #随机生成，不再由RFC69
while k == dB:
    k = randint(1, n)

def sm2_sign(m,ida,d,xB,yB):
    global k
    m = str(m)
    m='0'*((4-(len(bin(int(m.encode().hex(),16))[2:])%4))%4)+bin(int(m.encode().hex(),16))[2:]
    ENTLA = str(len(ida))
    za = ENTLA+str(ida)+str(a)+str(b)+str(gx)+str(gy)+str(xB)+str(yB)

    Z_A = hashlib.sha256(za.encode()).digest().hex()
    M = m
    M_ = Z_A + M
    M_ = M_.encode()
    hash_object = hashlib.sha256()
    hash_object.update(M_)
    e = hash_object.hexdigest()


    while True:
        x1,y1=SM2_mul(gx, gy, k, a, p)
        r = (x1+int(e,16))%n
        if r!=0 and r+k !=n:
            break
    s = (get_inverse(d+1,n)*(k-r*d))%n
    return r,s


def sm2_verify(m,ida,r,s,xB,yB):
    if r > n-1 or r<1 or s > n-1 or s<1:
        return -1

    m = str(m)
    m='0'*((4-(len(bin(int(m.encode().hex(),16))[2:])%4))%4)+bin(int(m.encode().hex(),16))[2:]
    ENTLA = str(len(ida))
    za = ENTLA+str(ida)+str(a)+str(b)+str(gx)+str(gy)+str(xB)+str(yB)

    Z_A = hashlib.sha256(za.encode()).digest().hex()
    M = m
    M_ = Z_A + M
    M_ = M_.encode()
    hash_object = hashlib.sha256()
    hash_object.update(M_)
    e = hash_object.hexdigest()

    t = (r+s)%n
    if t == 0:
        return -1
    xx,yy=SM2_mul(gx, gy, s, a, p)
    xxx,yyy=SM2_mul(xB, yB, t, a, p)
    x1_,y1_ = EC_add(xx,yy,xxx,yyy,a,p)
    v = (x1_+int(e,16))%n
    if v == r:
        print("验证成功")
    else: print("验证失败")

def sm2_verify2(r,s,n,h,xB,yB):
    t = (r + s) % n
    if t == 0:
        return -1
    xx, yy = SM2_mul(gx, gy, s, a, p)
    xxx, yyy = SM2_mul(xB, yB, t, a, p)
    x1_, y1_ = EC_add(xx, yy, xxx, yyy, a, p)

    return (r == ((h + x1_) % n))

def leak_k(k,r, n, s,d):
    sr = (s+r)%n
    srni = get_inverse(sr,n)
    ks = (k-s)%n
    dA = (ks*srni)%n
    print("k的泄露导致d的泄露:")
    if dA == d:
        print("成功")
    else:
        print("失败")

def reuse_k(r1,r2,s1,plaintext1,s2,plaintext2,n,d):
    dA = s2 - s1
    r = get_inverse((s1 - s2 + r1 - r2),n)
    dA = (dA*r)%n
    print("重用k会导致d的泄露:")
    if dA == d:
        print("成功泄露")
    else:
        print("失败")

def same_k_get_d(r1, r2, s1, s2, d1, d2, n):
    sr=get_inverse(s1+r1,n)
    sk1 = (sr*(s2+s2*d2+r2*d2-s1))%n

    sr_ = get_inverse(s2 + r2, n)
    sk2 = (sr_ * (s1+s1*d1+r1*d1-s2)) % n
    print("相同k得到对方的d:")
    if d1 == sk1 and d2 == sk2:
        print("成功")
    else:
        print("失败")


id = '01'
plaintext1 = [123456789]
plaintext2 = [987654321]
print("SM2相关pitfalls")
r,s =sm2_sign(plaintext1,id,dB,xB,yB)
r_,s_ =sm2_sign(plaintext2,id,dB,xB,yB)
print("\n")
sm2_verify(plaintext1,id,r,s,xB,yB)
print("\n")
leak_k(k, r, n, s,dB)
print("\n")
reuse_k(r,r_,s,plaintext1,s_,plaintext2,n,dB)
print("\n")
dB_=randint(1,n-1)
while dB_ == dB:
    dB_ = randint(1, n)
xB_,yB_=SM2_mul(gx,gy,dB_,a,p)
r_1, s_1 = sm2_sign(plaintext2, id,dB_,xB_,yB_)
same_k_get_d(r_, r_1, s_, s_1, dB, dB_, n)
print("\n")
print("检验r和-s是否为有效签名:")
sm2_verify(plaintext1,id,r,get_inverse(s,n),xB,yB)
print("\n")
print("不使用m，伪装签名:")
t = (r + s) % n
x,y=SM2_mul(gx, gy, s, a, p)
x,y=SM2_mul(xB, yB, t, a, p)
x,y = EC_add(x,y,x,y,a,p)
h = r - x
if sm2_verify2(r,s,n,h,xB,yB):
    print("伪造成功")
else:
    print("伪造失败")







