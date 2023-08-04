import secrets
import random
from gmssl import sm3, func
import time

# 定义椭圆曲线参数、基点和阶
A = 0
B = 7
G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
h = 1


def NI(a, n):
    def ext_gcd(a, b, arr):
        if b == 0:
            arr[0] = 1
            arr[1] = 0
            return a
        g = ext_gcd(b, a % b, arr)
        t = arr[0]
        arr[0] = arr[1]
        arr[1] = t - int(a / b) * arr[1]
        return g

    arr = [0, 1, ]
    gcd = ext_gcd(a, n, arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1


def EC_add(p, q):
    if p == 0 and q == 0:
        return 0  # 0 + 0 = 0
    elif p == 0:
        return q  # 0 + q = q
    elif q == 0:
        return p  # p + 0 = p
    else:
        if p[0] == q[0]:
            if (p[1] + q[1]) % P == 0:
                return 0  # mutually inverse
            elif p[1] == q[1]:
                return EC_double(p)
        elif p[0] > q[0]:  # swap if px > qx
            tmp = p
            p = q
            q = tmp
        r = []
        slope = (q[1] - p[1]) * NI(q[0] - p[0], P) % P  # 斜率
        r.append((slope ** 2 - p[0] - q[0]) % P)
        r.append((slope * (p[0] - r[0]) - p[1]) % P)
        return (r[0], r[1])


def EC_NI(p):
    r = [p[0]]
    r.append(P - p[1])
    return r


def EC_sub(p, q):
    q_NI = EC_NI(q)
    return EC_add(p, q_NI)


def EC_double(p):
    r = []
    slope = (3 * p[0] ** 2 + A) * NI(2 * p[1], P) % P
    r.append((slope ** 2 - 2 * p[0]) % P)
    r.append((slope * (p[0] - r[0]) - p[1]) % P)
    return (r[0], r[1])


def EC_multi(s, p):
    n = p
    r = 0
    s_bin = bin(s)[2:]
    s_len = len(s_bin)

    for i in reversed(range(s_len)):  # 类快速幂思想
        if s_bin[i] == '1':
            r = EC_add(r, n)
        n = EC_double(n)

    return r


def get_bit_num(x):
    if isinstance(x, int):  # when int
        num = 0
        tmp = x >> 64
        while tmp:
            num += 64
            tmp >>= 64
        tmp = x >> num >> 8
        while tmp:
            num += 8
            tmp >>= 8
        x >>= num
        while x:
            num += 1
            x >>= 1
        return num
    elif isinstance(x, str):  # when string
        return len(x.encode()) << 3
    elif isinstance(x, bytes):  # when bytes
        return len(x) << 3
    return 0


def key_gen():
    sk = int(secrets.token_hex(32), 16)  # private key
    pk = EC_multi(sk, G)  # public key
    return sk, pk


def ECDSA_sign(m, sk):
    while 1:
        k = secrets.randbelow(N)  # N is prime, then k <- Zn*
        R = EC_multi(k, G)
        r = R[0] % N  # Rx mod n
        if r != 0:
            break
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    s = NI(k, N) * (e + sk * r) % N
    return (r, s)


# 生成Satoshi的公私钥
sk, pk = key_gen()
print("Satoshi的公钥是:", pk)
# 伪造签名
a = time.time()
u = random.randrange(1, N - 1)
v = random.randrange(1, N - 1)
R = EC_add(EC_multi(u, G), EC_multi(v, pk))
r = R[0] % N
s = (r * NI(v, N)) % N
sign = (r, s)
print("签名为:", sign)
# 验证签名
e = (r * u * NI(v, N)) % N
if (EC_multi(NI(s, N), EC_add(EC_multi(e, G), EC_multi(r, pk))))[0] % N == r:
    print("通过验证")
    b = time.time()
    print("伪装验证用时:", b - a, "s")
else:
    print("不通过验证")
