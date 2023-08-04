# Verify the above pitfalls with proof-of-concept code


## 运行方式
分别运行ECDSA.py文件，SM2.py文件,schnorr.py文件可以获得相应签名验证算法的pitfalls结果。

## 实现说明

​通过实现ECDSA、Schnorr和SM2的数字签名与验证代码，验证了下图中的部分经典pitfalls:

![](https://pic.imgdb.cn/item/64ccb3521ddac507cc79d118.jpg)

即：
1、泄露随机数k，推导出私钥d。<br>
2、重用随机数k，推导出私钥d。<br>
3、两个用户使用了同样的k，推导出对方的私钥。<br>
4、在不验证m的前提下伪造签名<br>
5、(r,s)和(r,-s)都是合法的签名。调用验证算法验证(r,-s)是否能通过检测。<br>


## 签名，验证代码实现
ECDSA,SM2相关算法的实现可参考project10,project11
注：SM2中随机数k随机生成，不再使用RFC6979标准随机数生成算法

### Schnorr签名算法
Schnorr签名的基本原理如下：

#### 密钥生成：

选择一个大素数p，并找到一个生成元g，使得g的阶是p-1（即g^k mod p ≠ 1，其中k是p-1的因子）。
随机选择一个私钥x（0 < x < p-1），然后计算公钥y = g^x mod p。

#### 签名过程：
假设要对消息M进行签名。

选择一个随机数k（1 < k < p-1）。
计算临时值R = g^k mod p。
计算消息的哈希值e = H(M)，其中H是哈希函数。
计算签名的值s = (k + x * e) mod (p-1)。
#### 验证过程：
对于收到的签名 (R, s) 和消息 M：

计算消息的哈希值 e = H(M)。
计算公钥点 Q = R + g^s * y^(-e) mod p。
如果 Q 等于临时值 R，则签名有效；否则签名无效。

三种算法的伪代码如下图所示：
![](https://pic.imgdb.cn/item/64ccbaa81ddac507cc8b5ad5.jpg)

## pitfalls验证

### 1.验证k的泄露导致d的泄露
以SM2为例，原理如下图所示：
![](https://pic.imgdb.cn/item/64ccbc3b1ddac507cc8efc04.jpg)


算法的实现过程体现了$k$和$d$有关的公式，对公式进行等式变换即可得到由k推出d的公式。

代码如下：

```python
def leak_k(k,r, n, s,d):
    sr = (s+r)%n
    sr = get_inverse(sr,n)
    ks = (k-s)%n
    dA = (ks*sr)%n
    print("k的泄露导致d的泄露:")
    if dA == d:
        print("success")
    else:
        print("fault")
```


### 2.重用$k$会导致$d$的泄露

以SM2为例，原理如下图所示：
![](https://pic.imgdb.cn/item/64ccc5b01ddac507cca5e7c7.jpg)

```python
def reuse_k(r1,r2,s1,plaintext1,s2,plaintext2,n,d):
    dA = s2 - s1
    r = get_inverse((s1 - s2 + r1 - r2),n)
    dA = (dA*r)%n
    print("重用k会导致d的泄露:")
    if dA == d:
        print("成功泄露")
    else:
        print("失败")
```


### 3.相同$k$可以得到他人的$d$
以SM2为例，原理如下图所示：
![](https://pic.imgdb.cn/item/64ccc61c1ddac507cca6e356.jpg)

代码如下：

```python
def same_k_get_d(r1, r2, s1, s2, d1, d2, n):
    sr=get_inverse(s1+r1,n)
    sk1 = (sr*(s2+s2*d2+r2*d2-s1))%n

    sr_ = get_inverse(s2 + r2, n)
    sk2 = (sr_ * (s1+s1*d1+r1*d1-s2)) % n
    print("相同k得到对方的d:")
    if d1 == sk1 and d2 == sk2:
        print("成功")
    else:
        print("失败")
```


### 4.检验$r$和$-s$是否为有效签名

以SM2为例,将r与-s放入验证函数中。
```python
sm2_verify(plaintext1,id,r,get_inverse(s,n),xB,yB)

```

### 5.在不验证$m$的条件下伪造签名
代码如下：
```python
t = (r + s) % n
x,y=SM2_mul(gx, gy, s, a, p)
x,y=SM2_mul(xB, yB, t, a, p)
x,y = EC_add(x,y,x,y,a,p)
h = r - x
if sm2_verify2(r,s,n,h,xB,yB):
    print("伪造成功")
```


## 运行结果

**SM2相关pitfalls**

![](https://pic.imgdb.cn/item/64cccbfa1ddac507ccb3e947.jpg)

**Schnorr相关pitfalls**

![](https://pic.imgdb.cn/item/64cccb1e1ddac507ccb1e959.jpg)

**ECDSA相关pitfalls**

![](https://pic.imgdb.cn/item/64cccafc1ddac507ccb19c6a.jpg)




