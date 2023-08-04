# 创新创业实践课程汇总报告
## 一、成员分工
### group：109
### 姓名：刘畅 
### 学号：202000150077
未组队，所有project均一人完成。
---
## 二、实现方式

### 硬件环境：
* 处理器：Intel(R) Core(TM) i7-10875H CPU @ 2.30GHz   2.30 GHz
* 内存：16.0 GB (15.9 GB 可用)
### 软件环境：
全部完成的项目由C++与python两种语言编写
* C++编程实现环境
操作系统：win10
编译器：vs2019

* python编程实现环境
编译器：PyCharm Community Edition 2022.1.4
---

## 三、项目完成情况
### （一）已完成project
Project1: implement the naïve birthday attack of reduced SM3<br>
Project2: implement the Rho method of reduced SM3<br>
Project3: implement length extension attack for SM3, SHA256, etc.<br>
Project4: do your best to optimize SM3 implementation (software)<br>
Project5: Impl Merkle Tree following RFC6962<br>
Project9: AES / SM4 software implementation<br>
Project10: report on the application of this deduce technique in Ethereum with ECDSA<br>
Project11: impl sm2 with RFC6979<br>
Project12: verify the above pitfalls with proof-of-concept code<br>
Project13: Implement the above ECMH scheme<br>
Project14: Implement a PGP scheme with SM2<br>
Project17：比较Firefox和谷歌的记住密码插件的实现区别<br>
Project20: ECMH PoC<br>

### （二）未完成project
Project6: impl this protocol with actual network communication<br>
Project7: Try to Implement this scheme<br>
Project8: AES impl with ARM instruction<br>
Project15: implement sm2 2P sign with real network communication<br>
Project16: implement sm2 2P decrypt with real network communication<br>
Project18: send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself<br>
Project19: forge a signature to pretend that you are Satoshi<br>
Project21: Schnorr Bacth<br>
Project22: research report on MPT<br>

## 四、project具体实现（详细的原理解释与代码实现参见具体项目readme文件）

### Project1: implement the naïve birthday attack of reduced SM3

https://github.com/bemyself1724/group109/tree/main/project1

#### 实验思路
生日攻击基于生日悖论，即如果一个房间里有23个或23个以上的人，那么至少有两人生日相同的概率大于50%。随着消息空间的增大，能以较大概率在消息空间中找到碰撞。对SM3前n比特进行生日攻击，消息空间（即输入）为2的二分之n次方，我们可以检测碰撞，并通过多次实验计算成功率与所需时间。<br>

我们分别取前8比特、前16比特、前32比特进行生日攻击，各自循环1000次来计算成功率与所需时间。

#### 运行方式
直接运行birthday_attack.py即可，输入自选参数x进行前4x位生日碰撞攻击，输入-1时程序结束。

#### 实验结果

由于2^130 +1的计算复杂度过高，因此本实验采用简化的SM3进行生日碰撞，即获得哈希值后只取前4x位进行碰撞，x为自选参数。输入-1时程序结束。运行结果如图所示：

* 通过编写的SM3.py文件进行12bit生日碰撞
![](https://pic.imgdb.cn/item/64ca450f1ddac507cc8a7aae.jpg)

* 通过gmssl库提供的SM3哈希算法进行12bit生日碰撞
![](https://pic.imgdb.cn/item/64ca45ee1ddac507cc8ce172.jpg)

* 通过gmssl库提供的SM3哈希算法进行20bit生日碰撞
  ![](https://pic.imgdb.cn/item/64ca52651ddac507cca69cf3.jpg)


通过比较可知，随位数增加，所需时间增长，攻击速度变慢。

### Project2: implement the Rho method of reduced SM3

https://github.com/bemyself1724/group109/tree/main/project2

#### 实验思路
Rho算法的核心思想即不必逐个寻找碰撞，而是“跳着”求，在每一步迭代中分别移动1步和2步，也就是h1 = SM3(h1)和h2 = SM3(SM3(h2))。然后，检测h1和h2是否相等，如果相等则认为找到了一个循环节。此时按照相同的步幅进行迭代，直到找到下一循环节则认为找到了一组碰撞。<br>
选择两个随机的起始点h1和h2(本代码中选择由同一起始点x迭代生成)，并选择一个随机的迭代函数，此处为SM3哈希函数。h1 = SM3(x) 和 h2 = SM3(SM3(x))。<br>
由于SM3哈希函数不是基于离散对数问题，而是基于一系列位运算和非线性函数设计的，具有强抗碰撞性，因此我们选择简化的SM3算法进行Rho碰撞,即获得哈希值后只取前4x位进行碰撞.<br>
Rho方法的成功性会受到哈希函数的碰撞性与初始值选择的影响，而SM3的抗碰撞性很高，因此当找到一组完整SM3的哈希值相等时则认为寻找碰撞失败，需重新选择初始值。<br>

#### 运行方式
直接运行SM3_Rho.py即可，输入自选参数x进行前4x位Rho方法碰撞攻击，输入-1时程序结束。

#### 实验结果
本实验采用简化的SM3进行Rho碰撞，即获得哈希值后只取前4x位进行碰撞，x为自选参数。输入-1时程序结束。运行结果如图所示：

* 通过编写的SM3.py文件进行12bit Rho碰撞
  
![](https://pic.imgdb.cn/item/64ca819b1ddac507cc0aef26.jpg)

* 通过gmssl库提供的SM3哈希算法进行20bit Rho碰撞
  
![](https://pic.imgdb.cn/item/64ca7d961ddac507cc025081.jpg)

### Project3: implement length extension attack for SM3, SHA256, etc.

https://github.com/bemyself1724/group109/tree/main/project3

#### 实验思路
对于基于Merkle–Damgård结构的算法，如MD5、SHA256、SM3等，均存在长度扩展攻击。长度扩展攻击是一种特殊类型的攻击，它利用哈希函数的特性（比如MD结构）来构造具有相同前缀但不同后缀的两个输入消息，并获得它们的哈希值。通常具有以下步骤：
* 对于指定消息secret，对其进行填充并进行hash得到init_hash
* 选取附加消息append_m，计算secret||append_m的hash得到new_hash。
* 以第一次hash的结果init_hash作为IV值对附加消息填充后的消息块进行迭代压缩得到lenattack_hash。
* 如果new_hash与lenattack_hash相同那么视为攻击成功。
本实验实现了SM3与SHA256的长度扩展攻击。
注：SHA256存在大小端问题需调整。

#### 运行方式
1. 进行SM3的长度扩展攻击
* 直接运行SM3_lenattack.py
2. 进行SHA256的长度扩展攻击
* 直接运行SHA256_lenattack.py

#### 实验结果
* SM3长度扩展攻击
  
![](https://pic.imgdb.cn/item/64cb273e1ddac507cc13a225.jpg)

* SHA256长度扩展攻击
  
![](https://pic.imgdb.cn/item/64cb27cd1ddac507cc1514b4.jpg)

### Project4: do your best to optimize SM3 implementation (software)

https://github.com/bemyself1724/group109/tree/main/project4

#### 实验思路
根据SM3说明文档，编写SM3的各个基本组件。包括布尔函数、置换函数、消息扩展函数、压缩迭代函数。<br>
从理论上讲，SM3算法中使用最多且最耗时的是消息扩展和64轮压缩函数,因此，快速实现的关键在加速这两部分。采取的优化方式有采用SIMD指令并行计算；循环展开；逻辑函数优化等。

#### SIMD指令并行计算
传统的指令集架构（如标量指令集）一次只能处理一个数据元素，而SIMD指令集可以在同一时钟周期内同时处理多个数据元素，从而实现并行计算。在本实验中，采用_mm_and_si128， _mm_srli_epi32等指令，提高了并行性和处理速度，节省了指令缓存和指令解码的开销，简化了编程。


#### 循环展开
在消息扩展过程中，循环内存在大量的循环移位与逻辑运算操作。因此，可以借助SIMD指令进行循环展开，步幅为4，内部使用SIMD指令进行并行计算，一次进行4个扩展块的生成，减少了消息扩展快加载和存储次数，提高了消息扩展的速度。
注：
* 1.理论上可以进一步通过增加数组存储进行步幅为8的循环展开，出现了编译器溢出的问题未能解决。
* 2.采用类似思路：迭代压缩过程中每一个消息块需要进行 64 轮迭代，每轮迭代处理一组输入。由于相邻轮迭代的输入之间没有依赖关系，所以可以通过复制一组处理逻辑，在每轮迭代中处理两组输入，在一个周期内串行地完成两轮压缩函数，将一个消息块的迭代周期降到 32 个，从而提升吞吐量。

#### 逻辑函数优化
由于SM3算法存在很多逻辑操作，例如P1函数，循环左移函数等。可以借助SIMD指令使得逻辑函数内部可并行计算中间数值

此外，本实验还采用了预计算必要常数值，优化数组结构提高命中率等角度提高了加密速度。


#### 运行方式
将SM3_optimize文件目录下的工程文件SM3_optimize.sln复制到自己的项目中即可运行。

#### 实验结果
![](https://pic.imgdb.cn/item/64cb38431ddac507cc4095c9.jpg)


### Project5: Impl Merkle Tree following RFC6962

https://github.com/bemyself1724/group109/tree/main/project5

#### 实验思路
##### 1.merkle_tree的构建
在 RFC 6962 文中，Merkle 树用于创建证书数据的仅附加日志。 树结构通过创建从叶节点（单个证书）到树根的加密哈希链，可以有效验证证书数据。 对证书数据的任何篡改或修改都将导致计算出的根哈希值与可信根哈希值之间不匹配。通常需要经过以下步骤：
* 1.收集需要记录的证书数据。
* 2.将证书数据组织成 Merkle 树结构，叶节点代表各个证书。
* 3.计算每个证书的加密哈希值并将其沿树传播以计算每个内部节点的哈希值。
* 4.计算 Merkle Tree 的根哈希值，将其作为验证的可信锚点。
* 5.以安全且防篡改的方式存储根哈希和 Merkle 树，例如在仅附加日志中。
* 6.要验证证书的真实性，请遵循从叶节点到根节点的 Merkle Tree 路径并计算哈希链。 将计算出的根哈希与可信根哈希进行比较，以确保数据完整性。

##### 2.指定元素的存在性证明
存在性证明用于检验给定数据是否在merkle tree上（不需要知道完整数据信息）。已知索引后用于审计路径和存在性证明。根据索引从根节点出发通过二分法查找叶子节点索引对应路径并记录审核路径，找到叶子结点后根据审核路径上的需要用到的哈希信息逆推root结点的数值。若一致则证明存在。可以打印路径信息用作证据。


##### 3.指定元素的排除性证明
排除性证明用于检验给定数据是否在merkle tree上（不需要知道完整数据信息）。目前的排除性证明方法依赖于排序merkle tree，因此我们生成升序的叶子结点进而生成排序merkle tree，通过对集合中的元素进行排序，可以使用默克尔树来证明某些元素的非隶属关系。为了证明某个元素 不在集合中，需显示两侧的元素（进行存在性证明）。若两侧的元素相邻，则通过夹逼原理可进行排除性证明，否则有一定概率该节点存在。
过程如下：
* 查找小于交易额的前一个交易pre与大于交易额的下一笔交易next（数据块数值）
* 通过inclusion proof证明数据块pre与next存在
* 通过验证相邻通过夹逼确定排除性

实验代码包括两部分：

其一是merkle_tree.py，用于实现merkle tree的创建以及进行指定节点的存在性证明；<br>
其二是exclusion_proof.py，该文件实现排序MerkleTree的创建，同时可以用于进行指定节点的排除性证明。<br>

#### 运行方式
##### 验证inclusion proof
* 运行merkle_tree.py即可
  
##### 验证exclusion proof
* 运行exclusion_proof.py即可

#### 实验结果

1.验证inclusion proof（以1000个叶子结点为例，生成10w叶子结点可更改实参）
![](https://pic.imgdb.cn/item/64cb48e51ddac507cc6b5ca3.jpg)

2.验证exclusion proof（以100个叶子结点为例，生成10w叶子结点可更改实参num）
![](https://pic.imgdb.cn/item/64cb42ac1ddac507cc5a1b4b.jpg)

### Project9: AES / SM4 software implementation

https://github.com/bemyself1724/group109/tree/main/project9

#### 实验原理
SM4 算法是一种分组密码算法。其分组长度为 128bit，密钥长度也为 128bit。加密算法与密钥扩展算法均采用 32 轮非线性迭代结构，以字（32 位）为单位进行加密运算，每一次迭代运算均为一轮变换函数 F。SM4 算法加/解密算法的结构相同，只是使用轮密钥相反，其中解密轮密钥是加密轮密钥的逆序。算法结构分为：
* 密钥扩展过程
* 加密过程
* 解密过程

AES使用SPN结构。 加密轮数依赖于密钥长度：
| Key Size (bits) | Round               
| ----------------| ---------------- 
| 128              | 10           
| 192              | 12     
| 256              | 14


对于AES-128加密算法而言，在第一轮开始前，将明文与密钥进行异或，然后进行9轮迭代的操作，每一轮中包括4个不同的变换：字节代替（SubBytes）、行移位（ShiftRows）、列混淆（MixColumns）和轮密钥加（AddRoundKey）。最后一轮仅包含三个变换：字节代替（SubBytes）、行移位（ShiftRows）和轮密钥加（AddRoundKey）。

解密方案<br>

AES使用SPN结构，加解密函数不同。除了异或密钥，S盒、行移位、列混合都为原先的逆运算。每轮的密钥分别由种子密钥经过密钥扩展算法得到。<br>
首先对密文进行一次轮密钥加操作。<br>
然后进行10轮迭代加密，每一轮顺序执行以下四个操作：逆行移位，逆字节代换，逆轮密钥加，逆列混合。注意最后一轮迭代不执行逆列混合操作。<br>

密钥扩展方案<br>

需要将128比特的主密钥扩展为44个32比特字。首先将主密钥转化为4个32 bits的字，分别记为$W_{0}$，$W_{1}$，$W_{2}$，$W_{3}$，接下来通过下述步骤求出各轮的轮密钥。

1.将上一轮轮密钥的最后一列$W_{i-1}$循环左移一个字节。<br>
2.将结果中的每个字节依次经过S盒的查表<br>
3.查表后得到的结果与$W_{i-4}$、以及一个32 bits的常量（常量矩阵见下图）以及进行异或，就能得到该轮轮密钥的第一列。<br>
4.每一轮轮密钥的第一列使用上述方法求出，其余二、三、四列都直接通过异或运算得到。$W_{i}$=$W_{i-4}$⊕$W_{i-1}$，后续每一轮均按照此步骤进行处理。

#### 运行方式
##### 1.SM4算法
* 直接运行SM4_implementation.sln工程文件
  
##### 2.AES算法
* 直接运行AES_imple.sln工程文件

#### 实验结果
##### SM4
测试数据为：
```C++
 unsigned int key[4] = { 0x20200015,0x00772020,0x00150077,0x12345678 };
 unsigned int plaintext[4] = { 0x12345678,0x12345678,0x12345678,0x12345678 };
 unsigned int ciphertext[4] = { 0x0EE39625,0x2C0C2F8C,0x7DA76895,0xCD0D349A };
```
其中密文由明文加密获得，如下图所示：

![](https://pic.imgdb.cn/item/64cbbef61ddac507cc9b6598.jpg)

##### AES
输出AES的加密结果如下图所示：

![](https://pic.imgdb.cn/item/64cba7d91ddac507cc563976.jpg)


### Project10: report on the application of this deduce technique in Ethereum with ECDSA

https://github.com/bemyself1724/group109/tree/main/project10

#### 实验思路
E整个签名过程与DSA类似，所不一样的是签名中采取的算法为ECC，最后签名出来的值也是分为r,s。<br>

ECDSA的实现过程如下：<br>
##### 密钥生成：
选取一条椭圆曲线，选择参数a，b，基点G，阶数为n
选取$d\in n$为私钥，计算公钥为$P = d\cdot G$
##### 签名算法：
  *  计算$m$的哈希值$e=H(m)$
  *  生成随机数$k\in n$
  *  计算$R = (x,y)=k\cdot G$
  *  计算$r=x\mod n$，若$r=0$，则重新选择$k$
  *  计算$s=k^{-1}(e+dr)\mod n$，若$s=0$，则重新选择$k$
  *  返回签名$(r,s)$

##### 验证算法：
*  计算$m$的哈希值$e=H(m)$
*  计算$u_1 = es^{-1},u_2 = rs^{-1}$
*  计算$(x,y)=u_1G+u_2P \ mod \ n$
*  如果$r = x$则验证成功

##### 通过m和(r,s)恢复公钥P
* 由于R = (x,y)，并且r对应于其中的x，在已知椭圆曲线系数a和b的前提下，可以通过x求得对应的两个y的值。经检验，对应的两组(x,y)都可以作为R的值推出正确的公钥P的值。
* ​由于𝑛略低于𝑝，因此可以有两个值𝑋与𝑟匹配。一般来说只有一个，但是如果 𝑟 < 𝑝-𝑛 ，那么就会有两个。此时会有四组$(x,y)$可以作为R的值推出公钥P的值。

#### 运行方式
直接运行ECDSA.py文件即可

#### 实验结果
签名与验证耗时较少

![](https://pic.imgdb.cn/item/64cc73591ddac507ccdd0d4d.jpg)

### Project11: impl sm2 with RFC6979

https://github.com/bemyself1724/group109/tree/main/project11

#### 实验思路

##### 随机数k的生成

由RFC6979文档，可以写出RFC 6979 中描述的基于哈希函数的确定性k生成算法，用于确保生成的k是唯一的、不可预测的，从而提高签名的安全性。

设需要发送的消息为比特串M，klen为M的比特长度。 

为了对明文M进行加密，步骤如下： <br>
* 1：用随机数发生器产生随机数k∈[1,n-1]；
* 2：计算椭圆曲线点C1=[k]G=(x1,y1)
* 3：计算椭圆曲线点S=[h]PB，若S是无穷远点，则报错并退出
* 4：计算椭圆曲线点[k]PB=(x2,y2)
* 5：计算t=KDF(x2∥y2, klen)，若t为全0比特串，则返回A1
* 6：计算C2 = M⊕t
* 7：计算C3 = Hash(x2∥M∥y2)
* 8：输出密文C = C1∥C2∥C3

k由消息与私钥决定，所以在消息与私钥相同的情况下可能会出现相同的k，所以将RFC6979的k与random生成的数值相加，从而得到一个相对随机的数值。

为了对密文C=C1∥C2∥C3进行解密，步骤如下（设klen为密文中C2的比特长度）：

* 1：从C中取出比特串C1，将C1的数据类型转换为椭圆曲线上的点，验证C1是否满足椭圆曲线方程，若不满足则报错并退出
* 2：计算椭圆曲线点S=[h]C1，若S是无穷远点，则报错并退出
* 3：计算[$d_b$]C1=(x2,y2)，将坐标x2、y2的数据类型转换为比特串
* 4：计算t=KDF(x2∥y2, klen)，若t为全0比特串，则报错并退出
* 5：从C中取出比特串C2，计算M′ = C2⊕t
* 6：计算u = Hash(x2∥M′∥y2)，从C中取出比特串C3，若u$\neq$C3，则报错并退出
* 7：输出明文M′

#### 运行方式
直接运行SM2.py文件即可

#### 实验结果

![](https://pic.imgdb.cn/item/64ccabf01ddac507cc669b6e.jpg)

### Project12: verify the above pitfalls with proof-of-concept code

https://github.com/bemyself1724/group109/tree/main/project12

#### 实验思路
本实验首先实现了三种数字签名算法：ECDSA，SM2，Schnorr。
通过编写代码，证明三种数字签名算法中存在部分缺陷。<br>
对三种签名算法可能存在的安全隐患进行测试，测试内容如下：<br>

1、泄露随机数k，推导出私钥d。<br>
2、重用随机数k，推导出私钥d。<br>
3、两个用户使用了同样的k，推导出对方的私钥。<br>
4、在不验证m的前提下伪造签名<br>
5、验证(r,s)和(r,-s)都是合法的签名。调用验证算法验证(r,-s)是否能通过检测。<br>

#### 运行方式
分别运行ECDSA.py文件，SM2.py文件,schnorr.py文件可以获得相应签名验证算法的pitfalls结果。

#### 实验结果
运行结果如下：<br>（受限于篇幅，仅展示ECDSA签名算法的安全隐患运行结果，具体请参见本项目的readme文件）

**ECDSA相关pitfalls**

![](https://pic.imgdb.cn/item/64cccafc1ddac507ccb19c6a.jpg)


### Project13: Implement the above ECMH scheme

https://github.com/bemyself1724/group109/tree/main/project13

#### 实验思路
ECMH通过把哈希映射成椭圆曲线上的点（选择secp256k1曲线），然后利用ECC进行运算，利用椭圆曲线上的加法添加信息并将信息存储在集合中，后将集合中每一个元素的hash映射成椭圆曲线上的点。

#### 运行方式
* 直接运行ECMH.py文件即可

#### 实验结果
![](https://pic.imgdb.cn/item/64ccdd6c1ddac507ccda6610.jpg)

### Project14: Implement a PGP scheme with SM2

https://github.com/bemyself1724/group109/tree/main/project14

#### 实验思路
PGP（Pretty Good Privacy）是个混合加密算法，它由一个对称加密算法（本实验使用SM4）、一个公钥加密算法（本实验使用SM2）以及一个随机数生成算法（本实验参考RFC6962）组成.<br>
当用户想要向另一个用户发送加密消息时，他们使用对称会话密钥对消息进行加密，再使用消息接收者的公钥对对称会话密钥加密。加密后，只有拥有相应私钥的接收者可以解密会话密钥并进一步阅读消息。这种方式既可以保护数据的安全性，也可以提高加解密的速度.<br>

* 发送方加密：
1.发送端 和 接收端 分别生成sm2的公钥和私钥$(pk_send,sk_send),(pk_rec,sk_rec)$<br>
2.生成临时会话密钥 SK,这里的对称加密使用sm4<br>
3.加密sk：$encryptKey=Ecn_{pk_r}(Sk)$<br>
4.加密data：$encrypt=Ecn_{Sk}(data)$<br>

* 接收方解密：<br>
1.用sk_r解密encryptKey得到SK<br>
2.用sk解密得到data<ne>

#### 运行方式
* 直接运行文件PGP.py

#### 实验结果
![](https://pic.imgdb.cn/item/64cd02081ddac507cc31efa6.jpg)

### Project17: 比较Firefox和谷歌的记住密码插件的实现区别

https://github.com/bemyself1724/group109/tree/main/project17

#### 实验思路
Firefox和谷歌这两大主流浏览器中都提供了记住密码的功能，而功能相关的插件存在实现方式的区别，从以下几个方面进行讨论：
* 密码保存方式
* 跨设备同步
* 加密方法
* 第三方插件集成
* 密码自动填充

受限于篇幅，具体分析请参考项目readme文件


