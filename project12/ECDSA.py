import random

# 辗转相除法求gcd
def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

# 求出gcd所对应的xy
def get_xy(a, b):
    if b == 0:
        return 1, 0
    else:
        x1, y1 = get_xy(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
    return x, y

# 求逆
def get_inverse(a, n):
    gcd_ = gcd(a, n)
    if gcd_ == 1:  # a&n应该互质
        x, y = get_xy(a, n)
        return x % n
    else:
        return -999

def EC_add(P, Q):
    if P[0] == Q[0]:
        aaa = (3 * pow(P[0], 2) + a)
        bbb = (2 * P[1])
        if aaa % bbb != 0:
            val = get_inverse(bbb, n)
            y = (aaa * val) % n
        else:
            y = (aaa / bbb) % n
    else:
        aaa = (Q[1] - P[1])
        bbb = (Q[0] - P[0])
        if aaa % bbb != 0:
            val = get_inverse(bbb, n)
            y = (aaa * val) % n
        else:
            y = (aaa / bbb) % n

    Rx = (pow(y, 2) - P[0] - Q[0]) % n
    Ry = (y * (P[0] - Rx) - P[1]) % n
    return (Rx, Ry)

def EC_mul(n, m):
    if n == 0:
        return 0
    if n == 1:
        return m
    t = m
    while n >= 2:
        t = EC_add(t, m)
        n = n - 1
    return t

def EC_Sign(m, G, d, k, n):
    e = hash(m)
    R = EC_mul(k, G)
    r = R[0] % n
    s = (get_inverse(k, n) * (e + d * r)) % n
    return r, s

def EC_Verify(m, G, r, s, P, n):
    e = hash(m)
    w = get_inverse(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = EC_add(EC_mul(v1, G), EC_mul(v2, P))
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

# pitfalls

# 1泄露K会导致泄露d
def leak_k(k, r, n, m, s):
    r_1 = get_inverse(r, n)
    e = hash(m)
    d = r_1 * (k * s - e) % n
    return d

# 2重用k会导致d的泄露
def reuse_k(r1, s1, m1, r2, s2, m2, n):
    e1 = hash(m1)
    e2 = hash(m2)
    d = ((s1 * e2 - s2 * e1) * get_inverse(s2 * r1 - s1 * r2, n)) % n
    return d

# 3相同k，推断对方的d
def get_others_d(r, s1, m1, d1, s2, m2, d2, n):
    e1 = hash(m1)
    e2 = hash(m2)
    d1_ = ((s1 * e2 - s2 * e1 + s1 * r * d2) * get_inverse(s2 * r, n)) % n
    d2_ = ((s2 * e1 - s1 * e2 + s2 * r * d1) * get_inverse(s1 * r, n)) % n
    if d1 == d1_ and d2 == d2_:
        print("检验成功")
    else:
        print("检验失败")

# 5如果不验证m可以伪造签名
def EC_Verify_without_m(e, n, G, r, s, P):
    w = get_inverse(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = EC_add(EC_mul(v1, G), EC_mul(v2, P))
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

# 伪造签名
def cheat(G, P, n):
    u = random.randint(1, n - 1)
    v = random.randint(1, n - 1)
    r1 = EC_add(EC_mul(u, G), EC_mul(v, P))[0]
    e1 = (r1 * u * get_inverse(v, n)) % n
    s1 = (r1 * get_inverse(v, n)) % n
    if EC_Verify_without_m(e1, n, G, r1, s1, P):
        print("伪装成功")

a = 2
b = 2
n = 17
k = 2
m1 = 'A'
m2 = 'B'
d = 5
G = [7, 1]
print("ECDSA相关pitfalls")
P = EC_mul(d, G)
r,s=EC_Sign(m1,G,d,k,n)
EC_Verify(m1,G,r,s,P,n)
print("\n")
print("k的泄露导致d的泄露:")
if d == leak_k(k,r,n,m1,s):
    print("验证成功")
print("\n")
print("重用k会导致d的泄露:")
r1,s1=EC_Sign(m2,G,d,k,n)
if d == reuse_k(r1,s1,m2,r,s,m1,n):
    print("验证成功")
print("\n")
print("相同k得到对方的d:")
r2,s2=EC_Sign(m1,G,7,k,n)
get_others_d(r,s1,m2,5,s2,m1,7,n)
print("\n")
print("检验r和-s是否为有效签名:")
EC_Verify(m1,G,r,-s,P,n)
print("\n")
print("伪造签名:")
cheat(G,P,n)

