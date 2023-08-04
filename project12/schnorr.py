import hashlib
from random import randint


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

def sch_add(x1,y1,x2,y2,a,p):
    if x1==x2 and y1==p-y2:
        return False
    if x1!=x2:
        lamda=((y2-y1)*get_inverse(x2-x1, p))%p
    else:
        lamda=(((3*x1*x1+a)%p)*get_inverse(2*y1, p))%p
    x3=(lamda*lamda-x1-x2)%p
    y3=(lamda*(x1-x3)-y1)%p
    return x3,y3

def sch_mul(x,y,k,a,p):
    k=bin(abs(k))[2:]
    qx,qy=x,y
    for i in range(1,len(k)):
        qx,qy=sch_add(qx, qy, qx, qy, a, p)
        if k[i]=='1':
            qx,qy=sch_add(qx, qy, x, y, a, p)
    return qx,qy

def hash_(m,r):
    hash=hashlib.sha256()
    hash.update(m.encode())
    hash.update(str(r).encode())
    return int(hash.hexdigest(),16)

def sch_sign(m,pk,k):
    R = sch_mul(Gx, Gy, k, a, p)
    e = hash_(m,R)
    s = (k + e*pk) % n
    return R, s

def sch_verify(m,R,s,P):
    e = hash_(m,R)
    sG = sch_mul(Gx,Gy,s,a,p)
    ReP = sch_mul(P[0],P[1],e,a,p)
    ReP = sch_add(ReP[0],ReP[1],R[0],R[1],a,p)
    if sG[0]==ReP[0] and sG[1]==ReP[1]:
        print("验证成功")
    else: print("验证失败")

def sch_verify_without_m(e,R,s,P):
    sG = sch_mul(Gx,Gy,s,a,p)
    ReP = sch_mul(P[0],P[1],e,a,p)
    ReP = sch_add(ReP[0],ReP[1],R[0],R[1],a,p)
    if sG[0]==ReP[0] and sG[1]==ReP[1]:
        print("验证成功")
    else: print("验证失败")

def leak_k(k, R, n, m, s):
    sk = s - k
    e = hash_(m,R)
    e_ = get_inverse(e,n)
    d = e_*sk % n
    return d

def reuse_k(R1, s1, plaintext1, R2, s2, m2, n):
    e1 = hash_(plaintext1,R1)
    e2 = hash_(m2,R2)
    d = ((s1-s2) * get_inverse(e1-e2, n)) % n
    return d

def get_others_d(R1, s1, plaintext1, d1, R2, s2, m2, d2,n):
    e1 = hash_(plaintext1, R1)
    e2 = hash_(m2, R2)
    d1_ = ((s1-s2+e2*d2) * get_inverse(e1, n)) % n
    d2_ = ((s2-s1+e1*d1) * get_inverse(e2, n)) % n
    if d1 == d1_ and d2 == d2_:
        print("检验成功")
    else:
        print("检验失败")

a = 0
b = 7
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
d = 5
P = sch_mul(Gx,Gy,d,a,p)
k = randint(1, n)
print("schnorr相关pitfalls")
plaintext = '123456789'
plaintext1 = '987654321'
R,s = sch_sign(plaintext,d,k)
R1,s1 = sch_sign(plaintext1,d,k)
print("\n")
sch_verify(plaintext,R,s,P)
print("\n")
print("k的泄露导致d的泄露:")
if d == leak_k(k,R,n,plaintext,s):
    print("验证成功")
print("\n")
print("重用k会导致d的泄露:")
if d == reuse_k(R1,s1,plaintext1,R,s,plaintext,n):
    print("验证成功")
print("\n")
print("相同k得到对方的d:")
R2,s2 = sch_sign(plaintext1,7,k)
get_others_d(R,s,plaintext,d,R2,s2,plaintext1,7,n)
print("\n")
print("检验r和-s是否为有效签名:")
sch_verify(plaintext,R,-s,P)
print("\n")
print("不使用m，伪装签名:")
e3 = hash_(plaintext, R)
sch_verify_without_m(e3,R,s,P)