from sympy import *
import time

#椭圆曲线参数
a = 2
b = 2
n = 17            #阶数
k = 2
message = '202000150077'
d = 5              #私钥
G = [7, 1]         #椭圆曲线基点

# 辗转相除法求最大公因子
def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

# 扩展欧几里得
def get_xy(a, b):
    if b == 0:
        return 1, 0
    else:
        x1, y1 = get_xy(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
    return x, y

# 求逆元
def get_inverse(a, n):
    gcd_ = gcd(a, n)
    if gcd_ == 1:
        x, y = get_xy(a, n)
        return x % n
    else:
        return -100

def Add(P,Q):           #椭圆曲线点相加
    x1 = P[0]
    y1 = P[1]
    x2, y2 = Q[0],Q[1]
    if x1==x2:
        lamda = (((3 * x1 * x1 + a) % n) * get_inverse(2 * y1, n)) % n
    else:
        lamda=((y2-y1)*get_inverse(x2-x1, n))%n
    x3=(lamda*lamda-x1-x2)%n
    y3=(lamda*(x1-x3)-y1)%n
    return (x3,y3)

def binary_mul(k,m):           #二进制乘法
    k=bin(abs(k))[2:]        #将参数k转换为二进制字符串，去除前缀'0b'，得到二进制表示的字符串
    q = m
    for i in range(1,len(k)):
        q=Add(q, q)           #q << 1
        if k[i]=='1':
            q=Add(q, m)
    return q

def ECDSA_sign(m, G, d, k, n):
    e = hash(m)
    # print(e,"============")
    R = binary_mul(k, G)
    print("R",R)   #若R[0]=0，则无效，需重新选择k
    r = R[0] % n
    s = (get_inverse(k, n) * (e + d * r)) % n
    return r, s

def ECDSA_verify(m, G, r, s, P, n):
    e = hash(m)
    NI = get_inverse(s, n)
    v1 = (e * NI) % n
    v2 = (r * NI) % n
    w = Add(binary_mul(v1, G), binary_mul(v2, P))
    if w == 0:
        print('验证失败')
        return False
    else:
        if w[0] % n == r:
            print('验证通过')
            return True
        else:
            print('验证失败')
            return False

def Elliptic_Curve_Solving(x):
    r = x**3 + a*x + b        # 计算椭圆曲线方程右侧的值 r = x^3 + ax + b
    y = Symbol('y', real=True)
    # 解方程 y^2 = r，得到 y 坐标
    jie = solve(Eq(y**2, r), y)

    # 返回解的列表（可能有两个解）
    return jie

def recover_PK(s, r, m, P, G):
    r_= get_inverse(s+r,n)
    rs= r_*s
    e= hash(m)
    re = -r_*e

    tmp1=binary_mul(rs,P)
    tmp2=binary_mul(re,G)
    PK1=Add(tmp1,tmp2)

    print("由m和签名推出公钥为",PK1)



P = binary_mul(d, G)    #公钥
print("公钥为：",P)
print("测试签名、验证签名、推导公钥:")
t1 = time.time()
r,s=ECDSA_sign(message,G,d,k,n)
print("签名为:",r,s)
t2 = time.time()
print("签名用时:",(t2-t1)*1000,"ms")
t3 = time.time()
ECDSA_verify(message,G,r,s,P,n)
t4 = time.time()
print("验证用时:",(t4-t3)*1000,"ms")
t5 = time.time()
jie = (7,int(Elliptic_Curve_Solving(r)[0]))
recover_PK(s, r, message, jie, G)
t6 = time.time()
print("推导公钥用时:",t6-t5,"s")
