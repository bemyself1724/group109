# ECMH scheme


## 运行方式
* 直接运行ECMH.py文件即可

## 1.1 实验要求
如下图所示:

![](https://pic.imgdb.cn/item/64ccd5431ddac507ccc8d6fb.jpg)

## 1.2 ECMH方案介绍
ECMH通过把哈希映射成椭圆曲线上的点（选择secp256k1曲线），然后利用ECC进行运算，利用椭圆曲线上的加法添加信息并将信息存储在集合中，后将集合中每一个元素的hash映射成椭圆曲线上的点。

选择secp256k1曲线相关参数如下：
```python
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
G = [Gx, Gy]
```

ECMH方案如下：
```python
def ECMH(M):
    global a, b, p
    while (1):
        M = hash(M)
        temp = M ** 3 + a * M + b
        temp = temp % p
        y = second_remain(temp, p)
        if (y == -1):
            continue
        return temp, y
```
其中，二次剩余函数我们使用的Tonelli-Shanks算法是用于在模素数情况下求平方根的算法：

![](https://pic.imgdb.cn/item/64ccde931ddac507ccdcb391.jpg)

ECMH_Group则是将映射到椭圆曲线上的值进行点加。


## 1.3运行结果

![](https://pic.imgdb.cn/item/64ccdd6c1ddac507ccda6610.jpg)


## 引文参考

[1]https://blog.csdn.net/weixin_44617902/article/details/112785051

[2]https://github.com/tomasvdw/secp256k1/tree/multiset/src/modules/multiset

