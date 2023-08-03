import math
v_i = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
t = [0x79cc4519, 0x7a879d8a]

def Mod32(a, b):
    c = (a + b)
    d = c % (2 ** 32)
    ans = str(d)
    return ans

def loopleft_move(text, num):                   #循环左移
    text = str(text)
    return (text[num:] + text[:num])

def Xor(a, b):             #按位异或
    result = ''
    if len(a) != len(b):
        print('len(a)!=len(b)')
        return False
    for i in range(len(a)):
        if a[i] == b[i]:
            result += '0'
        else:
            result += '1'
    return result


def Xor3(a, b, c):
    return Xor(Xor(a, b), c)


def Or(a, b):                #按位或
    result = ''
    if len(a) != len(b):
        print('len(a)!=len(b)')
        return False
    for i in range(len(a)):
        if (a[i] == '1') | (b[i] == '1'):
            result += '1'
        else:
            result += '0'
    return result


def Or3(a, b, c):
    return Or(Or(a, b), c)


def And(a, b):                     #按位与
    result = ''
    if len(a) != len(b):
        print('len(a)!=len(b)')
        return False
    for i in range(len(a)):
        if (a[i] == '1') & (b[i] == '1'):
            result += '1'
        else:
            result += '0'
    return result


def And3(a, b, c):
    return And(And(a, b), c)


def Not(a):                      #按位非
    result = ''
    for ch in a:
        if ch == '1':
            result = result + '0'
        else:
            result = result + '1'
    return result

def Fill(text):          ##按照规则填充消息
    text_bin = ''
    for i in text:
        ascii_i = ord(i)
        text_bin = text_bin + '0' + bin(ascii_i)[2:]   #转为ASCII码二进制

    length = len(text_bin)

    text_bin = text_bin + '1'

    while len(text_bin) % 512 != 448:
        text_bin += '0'
    length_bin = bin(length)[2:]

    while len(length_bin) < 64:
        length_bin = '0' + length_bin

    text_bin = text_bin + length_bin

    return text_bin


def Iteration(m, w):         #迭代

    IV = {}
    IV[0] = v_i
    length = len(m)
    n = length // 512
    b = {}
    for i in range(n):
        b[i] = m[512 * i:512 * (i + 1)]
        w = Expand(b[i])
        IV[i + 1] = Compress(w, IV[i])
    return IV[n]

def Substitute(x, mode):           #置换函数
    if mode == 0:
        ans = Xor3(x,loopleft_move(x, 9),loopleft_move(x, 17))
    else:
        ans = Xor3(x, loopleft_move(x, 15), loopleft_move(x, 23))
    return ans


def ZtoH(text):     #将32位2进制字符串转换为8位16进制字符串
    text = str(text)
    while len(text) < 32:
        text = '0' + text
    text_16 = ''
    for i in range(8):
        tmp = hex(int(text[4 * i:4 * (i + 1)], base=2))[2:]
        text_16 = text_16 + tmp
    return text_16


def BtoH(text):       #将2进制转化为16进制字符串
    text = str(text)
    while len(text) < 32:
        text = '0' + text
    text_16 = ''
    for i in range(len(text) // 4):
        tmp = hex(int(text[4 * i:4 * (i + 1)], base=2))[2:]
        text_16 = text_16 + tmp
    return text_16



def HtoB(text):             # 16进制字符串转2进制字符串
    text_2 = ''
    text = str(text)
    for ch in text:
        tmp = bin(int(ch, base=16))[2:]
        for i in range(4):
            if len(tmp) % 4 != 0:
                tmp = '0' + tmp
        text_2 = text_2 + tmp
    while len(text_2) < 32:
        text_2 = '0' + text_2
    return text_2



def OtoB(text):          # 10进制字符串转2进制字符串
    text_10 = ''
    text = str(text)
    tmp = bin(int(text, base=10))[2:]
    text_10 = text_10 + tmp
    while len(text_10) < 32:
        text_10 = '0' + text_10
    return text_10


def OtoH(text):          #10进制字符串转16进制字符串
    text_10 = ''
    text = str(text)
    tmp = hex(int(text, base=10))[2:]
    text_10 = text_10 + tmp
    while len(text_10) < 8:
        text_10 = '0' + text_10
    return text_10


def Expand(b):             #消息拓展
    w = {}
    for i in range(16):
        w[i] = b[i * 32:(i + 1) * 32]
    for j in range(16, 68):
        tmp = Xor3(w[j - 16], w[j - 9], loopleft_move(w[j - 3], 15))
        tmp = Substitute(tmp, 1)
        w[j] = Xor3(tmp, loopleft_move(w[j - 13], 7), w[j - 6])
    for j in range(64):
        w[j + 68] = Xor(w[j], w[j + 4])
    for i in w:
        w[i] = ZtoH(w[i])
    return w


def FF(x, y, z, j):               #布尔函数FF，式中X,Y,Z 为32位向量
    if ((j >= 0) & (j <= 15)):
        ans = Xor3(x, y, z)
    else:
        ans = Or3(And(x, y), And(x, z), And(y, z))
    return ans

def GG(x, y, z, j):                #布尔函数GG，式中X,Y,Z 为32位向量
    if ((j >= 0) & (j <= 15)):
        ans = Xor3(x, y, z)
    else:
        ans = Or(And(x, y), And(Not(x), z))
    return ans


def Compress(w, IV):     #消息压缩

    A = IV[0:8]
    B = IV[8:16]
    C = IV[16:24]
    D = IV[24:32]
    E = IV[32:40]
    F = IV[40:48]
    G = IV[48:56]
    H = IV[56:64]
    for j in range(64):
        if int(j) <= 15:
            T = t[0]
        else:
            T = t[1]

        tmp = int(loopleft_move(HtoB(A), 12), 2) + int(HtoB(E), 2) + int(loopleft_move(HtoB(T), j % 32), 2)
        tmp = Mod32(tmp, 0)
        SS1 = loopleft_move(OtoB(tmp), 7)
        SS2 = Xor(SS1, loopleft_move(HtoB(A), 12))
        tmp = int(FF(HtoB(A), HtoB(B), HtoB(C), j), 2) + int(HtoB(D), 2) + int(SS2, 2) + int(HtoB(w[j + 68]), 2)
        tmp = Mod32(tmp, 0)
        TT1 = int(tmp, 10)
        tmp = int(GG(HtoB(E), HtoB(F), HtoB(G), j), 2) + int(HtoB(H), 2) + int(SS1, 2) + int(HtoB(w[j]), 2)
        tmp = Mod32(tmp, 0)
        TT2 = int(tmp, 10)
        D = C
        C = ZtoH(loopleft_move(HtoB(B), 9))
        B = A
        A = OtoH(TT1)
        H = G
        G = ZtoH(loopleft_move(HtoB(F), 19))
        F = E
        E = ZtoH(Substitute(OtoB(TT2), 0))

    r = A + B + C + D + E + F + G + H
    r = HtoB(r)
    v = HtoB(IV)
    return BtoH(Xor(r, v))

def sm3(c):
    c1 = Fill(c)
    m = Expand(c1)
    b = Iteration(c1, m)
    return b
