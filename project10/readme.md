# project10 :report on the application of this deduce technique in Ethereum with ECDSA
---

## ECDSA介绍
ECDSA（Elliptic Curve Digital Signature Algorithm）是一种数字签名算法，用于生成和验证数字签名。ECDSA是ECC与DSA的结合，在比特币、以太坊等区块链网络中大量使用。每一笔区块链交易执行之前都必须进行权限校验，以确保该交易是由账户对应的私钥签发。256 位私钥的 ECDSA 签名可以达到 3072 位 RSA 签名的安全强度。整个签名过程与DSA类似，所不一样的是签名中采取的算法为ECC，最后签名出来的值也是分为r,s。


## ECDSA的实现
- 选取一条椭圆曲线，选择参数a，b，基点G，阶数为n
- 选取$d\in n$为私钥，计算公钥为$P = d\cdot G$
- 签名算法：
  1. 计算$m$的哈希值$e=H(m)$
  2. 生成随机数$k\in n$
  3. 计算$R = (x,y)=k\cdot G$
  4. 计算$r=x\mod n$，若$r=0$，则重新选择$k$
  5. 计算$s=k^{-1}(e+dr)\mod n$，若$s=0$，则重新选择$k$
  6. 返回签名$(r,s)$
```python
def ECDSA_sign(m, G, d, k, n):
    e = hash(m)
    # print(e,"============")
    R = binary_mul(k, G)
    print("R",R)   #若R[0]=0，则无效，需重新选择k
    r = R[0] % n
    s = (get_inverse(k, n) * (e + d * r)) % n
    return r, s

```
- 验证算法：
  1. 计算$m$的哈希值$e=H(m)$
  2. 计算$u_1 = es^{-1},u_2 = rs^{-1}$
  3. 计算$(x,y)=u_1G+u_2P \ mod \ n$
  4. 如果$r = x$则验证成功

```python
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

```


## 通过$m$和$(r,s)$恢复公钥$P$
* 由于$R = (x,y)$，并且r对应于其中的x$，在已知椭圆曲线系数$a$和$b$的前提下，可以通过$x$求得对应的两个$y$的值。经检验，对应的两组$(x,y)$都可以作为$R$的值推出正确的公钥$P$的值。
* ​由于𝑛略低于𝑝，因此可以有两个值𝑋与𝑟匹配。一般来说只有一个，但是如果 𝑟 < 𝑝-𝑛 ，那么就会有两个。此时会有四组$(x,y)$可以作为$R$的值推出公钥$P$的值。

```python
def recover_PK(s, r, m, P, G):
    r_= get_inverse(s+r,n)
    rs= r_*s
    e= hash(m)
    re = -r_*e

    tmp1=binary_mul(rs,P)
    tmp2=binary_mul(re,G)
    PK1=Add(tmp1,tmp2)

    print("由m和签名推出公钥为",PK1)

```





 ## 引文参考
 [1]https://www.bookstack.cn/read/ethereum_book-zh/spilt.9.ee4988229e1934ea.md
 [2]https://aaron67.cc/2020/09/30/ecdsa/
 [3]https://medium.com/@sophonlabs/sui%E5%AF%86%E7%A0%81%E5%AD%A6-%E8%B7%A8%E9%93%BE%E7%AD%BE%E5%90%8D%E9%AA%8C%E7%AD%BE-bf800e655db1

