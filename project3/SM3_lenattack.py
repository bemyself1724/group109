from SM3_value import *
# from gmssl import func,sm3


def sm3_lenattack(init_m, add_m, new_v):
    msg = init_m + add_m         #将原始消息与附加消息连接起来
    msg = padding(msg)
    msg = msg[len(init_m):]      #取附加消息部分与填充部分
    b = msg_divide(msg)          #调用sm3算法的后半部分进行哈希
    v = []
    for i in range(len(b)):
        if i == 0:
            v.append(sm3_cf(new_v, b[i]))
        else:
            v[0] = sm3_cf(v[i - 1], b[i])
    result = ''
    for j in range(8):
        result = result + hex(v[0][j])[2:].rjust(8, '0')
    return result



secret = 'I know that is my test1'
print('消息为'+secret)
init_hash = sm3(secret)
IV = []  # 将原消息的hash值作为IV
for i in range(0, len(init_hash), 8):
    IV.append(int(init_hash[i:i + 8], 16))   #以字为单位
print('消息的哈希值为'+init_hash)
append_m = 'me on the next page'
print('附加消息为'+append_m)
lenattack_hash=sm3_lenattack(padding(strtobin(secret)), strtobin(append_m), IV)
new_hash=sm3_extend(secret,append_m)
print('伪造的哈希为'+lenattack_hash)
print('伪造消息的哈希为'+new_hash)

if(new_hash == lenattack_hash):
    print('长度扩展攻击成功!')
else:
    print('长度扩展攻击失败!')


