# <center> 实现SM3、SHA256的长度扩展攻击 </center>

## 运行方式
### 1. 进行SM3的长度扩展攻击
* 直接运行SM3_lenattack.py
### 2. 进行SHA256的长度扩展攻击
* 直接运行SHA256_lenattack.py


## 1.SM3算法
SM3算法的实现结构与之前相同，不再赘述。

## 2.SHA256算法
SHA256算法是SHA-2（Secure Hash Algorithm 2）家族中的一员，接受任意长度的输入消息，并生成固定长度的256位（32字节）哈希值作为输出。主要结构由三个部分构成：消息填充，消息扩展，迭代压缩。

### 消息填充
* 对消息进行补码处理: 将消息转化为二进制补码形式，假设消息M的二进制编码长度为l位. 首先在消息末尾补上一位"1", 然后再补上个"0", 其中为下列方程的最小非负整数：
  
![](https://pic.imgdb.cn/item/64cb1deb1ddac507ccf9fe83.jpg)

* 填充一个64位大小的数据块，大端模式存放原始数据长度。


### 消息扩展
将填充后的消息划分成512位（64字节）的消息分组。
* 对于每一块，将块分解为16个32-bit的字，记为w[0], …, w[15]
也就是说，前16个字直接由消息的第i个块分解得到。
* 其余的字由如下迭代公式得到：
  
![](https://pic.imgdb.cn/item/64cb20401ddac507cc00e7c0.jpg)



### 迭代压缩
由定义的初始值H0通过压缩函数生成迭代的中间值值H1，经过64次压缩后后生成本消息分组的最终哈希值。压缩函数的结构如图：

![](https://pic.imgdb.cn/item/64cb223f1ddac507cc06552d.jpg)

  
## 3.长度扩展攻击
长度扩展攻击是一种特殊类型的攻击，它利用哈希函数的特性（比如MD街都）来构造具有相同前缀但不同后缀的两个输入消息，并获得它们的哈希值。通常具有以下步骤：
* 对于指定消息secret，对其进行填充并进行hash得到init_hash
* 选取附加消息append_m，计算secret||append_m的hash得到new_hash。
* 以第一次hash的结果init_hash作为IV值对附加消息填充后的消息块进行迭代压缩得到lenattack_hash。
* 如果new_hash与lenattack_hash相同那么视为攻击成功。

### SM3长度扩展攻击函数
```python
def sm3_lenattack(init_m, add_m, new_v):
    msg = init_m + add_m         #将原始消息与附加消息连接起来
    msg = padding(msg)
    msg = msg[len(init_m):]      #取附加消息部分与填充部分
    b = msg_divide(msg)          #调用sm3算法后半部分进行哈希
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
```
### SHA256长度扩展攻击函数

```python
def length_extansion_attack(message_og, hash_og, keylen, attack_message):
    state = reverse_h(hash_og)     #由于大小端问题需调整顺序
    message_og_padded = padding(message_og, keylen)
    hash_attack = Sha256(attack_message, state, init_length=len(message_og_padded) + keylen).hex()
    secret_extend = message_og_padded + bytearray(attack_message, 'ascii')

    return secret_extend, hash_attack
```


## 4.运行结果
* SM3长度扩展攻击
  
![](https://pic.imgdb.cn/item/64cb273e1ddac507cc13a225.jpg)

* SHA256长度扩展攻击
  
![](https://pic.imgdb.cn/item/64cb27cd1ddac507cc1514b4.jpg)
  

##  引文参考
[1]https://zhuanlan.zhihu.com/p/44668032
[2]https://en.wikipedia.org/wiki/Length_extension_attack
