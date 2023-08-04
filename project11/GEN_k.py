import hashlib
import binascii
import hmac


def bianma(val):
    code_string = ''.join([chr(x) for x in range(256)])
    result_bytes = bytes()
    while val>0:
        curcode = code_string[val % 256]
        result_bytes = bytes([ord(curcode)]) + result_bytes
        val //= 256

    pad_size = 32 - len(result_bytes)

    if (pad_size > 0):
        result_bytes = b'\x00' * pad_size + result_bytes

    return result_bytes

def b_to_int(data, qlen):
    x = int(binascii.hexlify(data), 16)
    l = len(data) * 8

    if l > qlen:
        return x >> (l - qlen)
    return x

def gen_k(m, pk ,q):
    hlen = hashlib.sha256().digest_size      #计算哈希函数 SHA-256 的输出字节长度 hlen
    qlen=len(str(q))*8                       #计算椭圆曲线的阶 q 的比特长度 qlen
    h1 = hashlib.sha256(m.encode()).digest()  #通过哈希函数 SHA-256 对消息的哈希值 h1 进行处理，得到 V 和 K 的初始值
    V=b"\x01"* hlen
    K=b"\x00"* hlen

    pk=bianma(pk)
    K = hmac.new(K, V + b'\x00' + pk + h1, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()
    K = hmac.new(K, V + b'\x01' + pk + h1, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()

    T = b''
    tlen = 0
    while tlen < qlen:       #利用HMAC-SHA256对V,K进行多轮处理，生成 k 的候选值 T，直到满足T的长度大于等于qlen为止
        V = hmac.new(K, V, hashlib.sha256).digest()
        T += V
        tlen = len(T)*8

    k = b_to_int(T, qlen)
    if k>=1 and k < q:              #如果 k 在 1 和 q 之间，则返回 k 作为签名中的随机数
        return k
    else:                           #否则，继续处理 V 和 K，然后再次生成 k 的候选值，直到找到合适的 k
        K=hmac.new(K,V+b"\x00",digestmod='sha256').digest()
        V=hmac.new(K,V,digestmod='sha256').digest()

    return k