import base64
from gmssl import sm2, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT


print("发送方加密")
# 由SM2算法生成SM2的密钥
sk_send = "00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5"
pk_send = "B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207"
sk_rec = "228a9707053e1b333fb8cb839567a9db4ca1cf5381e9a6a539774e6c3563cdfa"
pk_rec = "893cb9392dabd2fac095f657a7e0bc308e32f4b79380d478547f57123dccb3bc4a3a2d009f5826b6624c99dd41baf470a8baf46722f2d36b1d26f19af112c5cd"
print("生成 sm2密钥：")
print("公钥是:",pk_send,"\n私钥是:",pk_rec)


print("\n生成SM4对称密钥：")
sm4Key_str = func.random_hex(16)
sm4Key = bytes(sm4Key_str, encoding='utf-8')
sm4_crypt = CryptSM4()  # 初始化CryptSM4
sm4_crypt.set_key(sm4Key, mode=SM4_ENCRYPT)  # 初始化key到CryptSM4 这里传的是SM_DECRYPT
print("SM4对称密钥：", sm4Key)

# 用公钥对sm4Key进行加密
print("\n加密密钥")
sm2_crypt = sm2.CryptSM2(private_key=None, public_key=pk_rec)  # 附公钥
encryptKey = sm2_crypt.encrypt(sm4Key)  # 对sm4Key(bytes) 进行加密,返回bytes
encryptKey = base64.b64encode(encryptKey)  # bytes 转base64
print("加密后密钥：",encryptKey)

# sm4对数据进行加密
print("\n加密数据:")
data = input("输入数据为:")
data = data.encode("utf-8")
encryptData = sm4_crypt.crypt_ecb(data)  # 对数据(bytes)加密
encryptData = base64.b64encode(encryptData)  # bytes 转base64
encryptData = encryptData.decode("utf-8")  # 由于转为base64,还是bytes,json不支持,故转为str
print("加密后的数据:",encryptData)


print("\n发送密文与加密后的密钥：")
result = {"密文":encryptData,"密钥":encryptKey}
print(result)


print("接收方解密")
encryptKey =base64.b64decode(result["密钥"])
encryptData = base64.b64decode(result["密文"])

# sm2解密sm4Key
print("\n解密会话密钥")
sm2_crypt_r =sm2.CryptSM2(private_key=sk_rec,public_key=None)
sm4Key_r = sm2_crypt_r.decrypt(encryptKey)  # 解密, 返回bytes
print("会话密钥是:",sm4Key_r)

# sm4解密得到data
print("\n会话密钥解密得到数据")
sm4_crypt_r=CryptSM4()
sm4_crypt_r.set_key(sm4Key_r,mode=SM4_DECRYPT)
data_rec=sm4_crypt_r.crypt_ecb(encryptData)
data_rec1 = data_rec.decode('utf-8')
print("数据为:",data_rec1)



