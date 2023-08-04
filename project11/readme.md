# 基于 RFC6979标准 实现 sm2

## 运行方式
* 直接运行SM2.py文件即可

## RFC6979描述
RFC 6979是一份由 IETF（Internet Engineering Task Force）发布的标准，它的全名是 “确定性使用数字签名算法（DSA）和椭圆曲线数字签名算法（ECDSA）”，该标准描述了在使用 DSA 和 ECDSA 数字签名算法时，如何使用确定性（deterministic）的方式生成签名。在传统的签名生成过程中，会使用一个随机数来计算签名，然后将随机数与签名一起发布。然而，如果在生成签名时使用了预测性不足的伪随机数或者随机数的生成过程存在漏洞，可能会导致私钥的泄露，从而危及签名的安全性。

为了避免这些潜在的问题，RFC 6979提出了一种基于哈希函数和消息的确定性签名生成算法。该算法使用了特定的伪随机数生成方式，能够确保生成的随机数在每次签名时都是唯一的，而且不能被预测。这样一来，即使攻击者获得了签名中的随机数，也无法推导出私钥信息。


## 随机数k的生成

由RFC6979文档[1]，可以写出RFC 6979 中描述的基于哈希函数的确定性k生成算法，用于确保生成的k是唯一的、不可预测的，从而提高签名的安全性。

```python
def gen_k(m, pk ,q):
    hlen = hashlib.sha256().digest_size      #计算哈希函数 SHA-256 的输出字节长度 hlen
    qlen=len(str(q))*8                       #计算椭圆曲线的阶 q 的比特长度 qlen
    h1 = hashlib.sha256(m.encode()).digest()  #通过哈希函数 SHA-256 对消息的哈希值 h1 进行处理，得到 V 和 K 的初始值
    V=b"\x01"* hlen
    K=b"\x00"* hlen

    pk=encode(pk)
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

    k = bits2int(T, qlen)
    if k>=1 and k < q:              #如果 k 在 1 和 q 之间，则返回 k 作为签名中的随机数
        return k
    else:                           #否则，继续处理 V 和 K，然后再次生成 k 的候选值，直到找到合适的 k
        K=hmac.new(K,V+b"\x00",digestmod='sha256').digest()
        V=hmac.new(K,V,digestmod='sha256').digest()

    return k

```



## SM2实现

​		SM2是一种非对称加密算法，基于椭圆曲线密码学。在官方文档中我们可以查询到加解密的实现方法[2]。

SM2的加密与解密流程如下图：

![](https://pic.imgdb.cn/item/64cca49c1ddac507cc541df3.jpg)

设需要发送的消息为比特串M，klen为M的比特长度。 

为了对明文M进行加密，步骤如下： 

（本部分参考引文文献[https://blog.csdn.net/chexlong/article/details/103293311]）

* 1：用随机数发生器产生随机数k∈[1,n-1]；
* 2：计算椭圆曲线点C1=[k]G=(x1,y1)
* 3：计算椭圆曲线点S=[h]PB，若S是无穷远点，则报错并退出
* 4：计算椭圆曲线点[k]PB=(x2,y2)
* 5：计算t=KDF(x2∥y2, klen)，若t为全0比特串，则返回A1
* 6：计算C2 = M⊕t
* 7：计算C3 = Hash(x2∥M∥y2)
* 8：输出密文C = C1∥C2∥C3

$k$由消息与私钥决定，所以在消息与私钥相同的情况下可能会出现相同的$k$，所以将RFC6979的$k$与random生成的数值相加，从而得到一个相对随机的数值。

为了对密文C=C1∥C2∥C3进行解密，步骤如下（设klen为密文中C2的比特长度）：

* 1：从C中取出比特串C1，将C1的数据类型转换为椭圆曲线上的点，验证C1是否满足椭圆曲线方程，若不满足则报错并退出
* 2：计算椭圆曲线点S=[h]C1，若S是无穷远点，则报错并退出
* 3：计算[$d_b$]C1=(x2,y2)，将坐标x2、y2的数据类型转换为比特串
* 4：计算t=KDF(x2∥y2, klen)，若t为全0比特串，则报错并退出
* 5：从C中取出比特串C2，计算M′ = C2⊕t
* 6：计算u = Hash(x2∥M′∥y2)，从C中取出比特串C3，若u$\neq$C3，则报错并退出
* 7：输出明文M′

## 实验结果
![](https://pic.imgdb.cn/item/64ccabf01ddac507cc669b6e.jpg)


## 引文参考

[1] https://www.rfc-editor.org/rfc/rfc6979.txt

[2] https://blog.csdn.net/chexlong/article/details/103293311

[3]https://www.cnblogs.com/aimmiao/p/14174215.html

