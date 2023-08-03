T1 = [0x79cc4519]
T2 = [0x7a879d8a]
T = T1 * 16 + T2 * 48    #前十六次访问的访问T1，后48次访问T2
V = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]


# 将消息(字符串)转换成ASCII码对应的二进制
def strtobin(msg):
    msg_bin = ''
    for i in msg:
        ascii_i = ord(i)
        msg_bin = msg_bin + bin(ascii_i)[2:].rjust(8, '0')
    return msg_bin

# 对消息进行填充
def padding(m):
    length = len(m)
    m_bin = m + '1'    # 填充1个比特'1'
    k = (448 - length - 1) % 512   # 填充k个0
    if k < 0:
        k += 512
    m_bin = m_bin + '0' * k + bin(length)[2:].rjust(64, '0')   # 补充64位的原始消息长度，前补0
    return m_bin    #可按512bit分组

# 对消息进行分组
def msg_divide(m):
    length = len(m)  # 记录填充之后的长度
    temp = []
    for i in range(0, length, 8):      # 按字节划分
        tmp = m[i:i + 8]
        tmp = int(tmp, 2)            # 将tmp从二进制转换为整数
        temp.append(tmp)
    b = []
    for i in range(len(temp) // 64):
        instate = temp[i * 64:(i + 1) * 64]      #取出一个512比特分组的数据
        b.append(instate)
    return b

# ff函数
def ff(x, y, z, j):
    # x,y,z为3个32位向量，j为轮数（0<=j<64）
    if ((j >= 0) & (j <= 15)):
        ret = x ^ y ^ z
    if 16 <= j < 64:
        ret = (x & y) | (x & z) | (y & z)
    return ret


# gg函数
def gg(x, y, z, j):
    # x,y,z分别为3个32位向量（int），j为轮数（0<=j<64）
    if ((j >= 0) & (j <= 15)):
        ret = x ^ y ^ z
    if 16 <= j < 64:
        ret = (x & y) | ((~x) & z)
    return ret


def loop_left(x, n):                 # x是32位的向量
    strx = bin(x)[2:].zfill(32)      #将输入的32位向量 x 转换为二进制字符串，并用 '0' 在字符串前面填充至32位长度
    add = '0' * n
    con = strx[n:] + add             #循环左移n位
    ret = int(con, 2)
    return ret

# p0置换函数
def p0(x):
    ret = x ^ (loop_left(x, 9)) ^ (loop_left(x, 17))
    return ret

# p1置换函数
def p1(x):
    ret = x ^ (loop_left(x, 15)) ^ (loop_left(x, 23))
    return ret


# 压缩函数cf
def sm3_cf(vi, bi):
    w = []                   #用于存储消息扩展后的前68 个 32 位十进制整数 (int) 的列表
    for i in range(16):      # 将bi划分为16个字生成w_0-w_15
        weight = 0x1000000  # 16进制位置权重，初始为2^24
        rel = 0
        for j in range(i * 4, (i + 1) * 4):  # 将4字节数整合成一个字
            rel = rel + bi[j] * weight       # bi[j]数据类型是二进制对应的整数
            weight = int(weight / 0x100)     # 位置权重每次除以2^8，保证字节位置对应
        w.append(rel)

    for k in range(16, 68):    # 生成w16-w67
        tmp = p1(w[k - 16] ^ w[k - 9] ^ loop_left(w[k - 3], 15)) ^ loop_left(w[k - 13], 7) ^ w[k - 6]
        w.append(tmp)
    w1 = []

    for k in range(0, 64):     # 生成w’0-w‘64
        tmp = w[k] ^ w[k + 4]
        w1.append(tmp)
    A, B, C, D, E, F, G, H = vi        #vi的分组，消息压缩
    # 64轮加密
    for j in range(0, 64):
        #
        ss1 = loop_left((loop_left(A, 12)) ^ E ^ (loop_left(T[j], j % 32)), 7)   #前十六次访问的访问T1，后48次访问T2
        #
        ss2 = ss1 ^ loop_left(A, 12)
        tt1 = ff(A, B, C, j) ^ D ^ ss2 ^ w1[j]
        tt2 = gg(E, F, G, j) ^ H ^ ss1 ^ w[j]
        D = C
        C = loop_left(B, 9)
        B = A
        A = tt1
        H = G
        G = loop_left(F, 19)
        F = E
        E = p0(tt2)
    v_i = [A, B, C, D, E, F, G, H]
    return [v_i[i] ^ vi[i] for i in range(0, 8)]

# sm3算法
def sm3(msg):
    # 消息填充,msg是字符串类型
    msg=padding(strtobin(msg))
    b = msg_divide(msg)
    v = []
    for i in range(len(b)):
        if i == 0:
            v.append(sm3_cf(V, b[i]))
        else:
            v[0] = sm3_cf(v[i - 1], b[i])

    result = ''
    for j in range(8):
        result = result + hex(v[0][j])[2:].rjust(8,'0')
    return result

def sm3_extend(msg1,msg2):
    # 消息填充,msg是字符串类型
    msg=padding(padding(strtobin(msg1))+strtobin(msg2))
    b = msg_divide(msg)
    v = []
    for i in range(len(b)):
        if i == 0:
            v.append(sm3_cf(V, b[i]))
        else:
            v[0] = sm3_cf(v[i - 1], b[i])

    result = ''
    for j in range(8):
        result = result + hex(v[0][j])[2:].rjust(8,'0')
    return result