from hashlib import sha256
import base64
def right_rotate(x, n):
    return (x >> n) | (x << (32 - n))

def ch(x, y, z):
    return (x & y) ^ (~x & z)

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def f0(x):
    return right_rotate(x, 2) ^ right_rotate(x, 13) ^ right_rotate(x, 22)

def f1(x):
    return right_rotate(x, 6) ^ right_rotate(x, 11) ^ right_rotate(x, 25)

def sigma_0(x):
    return right_rotate(x, 7) ^ right_rotate(x, 18) ^ (x >> 3)

def sigma_1(x):
    return right_rotate(x, 17) ^ right_rotate(x, 19) ^ (x >> 10)

def padding(msg, key_length):
    if isinstance(msg, str):              #进行输入的判断并转化
        msg = bytearray(msg, 'ascii')
    elif isinstance(msg, bytes):
        msg = bytearray(msg)
    elif not isinstance(msg, bytearray):
        raise TypeError
    length = (len(msg) + key_length) * 8
    msg.append(0x80)
    while ((len(msg) + key_length) * 8 + 64) % 512 != 0:
        msg.append(0x00)
    msg += length.to_bytes(8, 'big')
    return msg

def Sha256(msg: bytearray, state=None, init_length=0) -> bytearray:
    msg=padding(msg,init_length)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    blocks = []
    for i in range(0, len(msg), 64):
        blocks.append(msg[i:i + 64])

    if (state == None):
        h0 = 0x6a09e667
        h1 = 0xbb67ae85
        h2 = 0x3c6ef372
        h3 = 0xa54ff53a
        h5 = 0x9b05688c
        h4 = 0x510e527f
        h6 = 0x1f83d9ab
        h7 = 0x5be0cd19
    else:
        h0 = state[0]
        h1 = state[1]
        h2 = state[2]
        h3 = state[3]
        h4 = state[4]
        h5 = state[5]
        h6 = state[6]
        h7 = state[7]

    for message_divide in blocks:
        s = []
        for t in range(0, 64):
            if t <= 15:
                s.append(bytes(message_divide[t * 4:(t * 4) + 4]))
            else:
                m1 = sigma_1(int.from_bytes(s[t - 2], 'big'))
                m2 = int.from_bytes(s[t - 7], 'big')
                m3 = sigma_0(int.from_bytes(s[t - 15], 'big'))
                m4 = int.from_bytes(s[t - 16], 'big')
                temp =((m1 + m2 + m3 + m4) % 2 ** 32).to_bytes(4, 'big')
                s.append(temp)

        assert len(s) == 64

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        for t in range(64):
            t1 = ((h + f1(e) + ch(e, f, g) + K[t] +
                   int.from_bytes(s[t], 'big')) % 2 ** 32)

            t2 = (f0(a) + maj(a, b, c)) % 2 ** 32

            h = g
            g = f
            f = e
            e = (d + t1) % 2 ** 32
            d = c
            c = b
            b = a
            a = (t1 + t2) % 2 ** 32

        h0 = (h0 + a) % 2 ** 32
        h1 = (h1 + b) % 2 ** 32
        h2 = (h2 + c) % 2 ** 32
        h3 = (h3 + d) % 2 ** 32
        h4 = (h4 + e) % 2 ** 32
        h5 = (h5 + f) % 2 ** 32
        h6 = (h6 + g) % 2 ** 32
        h7 = (h7 + h) % 2 ** 32

    return ((h0).to_bytes(4, 'big') + (h1).to_bytes(4, 'big') + (h2).to_bytes(4, 'big') + (h3).to_bytes(4, 'big') +
            (h4).to_bytes(4, 'big') + (h5).to_bytes(4, 'big') + (h6).to_bytes(4, 'big') + (h7).to_bytes(4, 'big'))

def reverse_h(h):
    res = [0] * 8
    res[0] = int(h[0:8], 16)
    res[1] = int(h[8:16], 16)
    res[2] = int(h[16:24], 16)
    res[3] = int(h[24:32], 16)
    res[4] = int(h[32:40], 16)
    res[5] = int(h[40:48], 16)
    res[6] = int(h[48:56], 16)
    res[7] = int(h[56:64], 16)
    return res

def length_extansion_attack(message_og, hash_og, keylen, attack_message):
    state = reverse_h(hash_og)     #由于大小端问题需调整顺序
    message_og_padded = padding(message_og, keylen)
    hash_attack = Sha256(attack_message, state, init_length=len(message_og_padded) + keylen).hex()
    secret_extend = message_og_padded + bytearray(attack_message, 'ascii')

    return secret_extend, hash_attack


key = '202000150077'
key_hash = base64.b16decode(key.encode().hex(), casefold=True)
h = sha256()
h.update(key_hash)
secret = 'I know that is my test1'
h.update(secret.encode())
h = h.hexdigest()
print('消息为'+secret)
append_m = 'me on the next page'
secret_extend, hash_attack = length_extansion_attack(secret, h, len(key), append_m)
hash_extend = sha256(key_hash + padding(secret, len(key)) + bytearray(append_m, 'ascii')).hexdigest()
print("伪造的hash值:", hash_attack)
print("长度扩展的hash值:", hash_extend)
if hash_attack == hash_extend:
        print("SHA256长度扩展攻击成功！")
else:
        print("SHA256长度扩展攻击失败")

