# AES / SM4 软件实现

本实验中使用C++实现了SM4算法与AES算法。

## 运行方式
### 1.SM4算法
* 直接运行SM4_implementation.sln工程文件
  
### 2.AES算法
* 直接运行AES_imple.sln工程文件

## SM4实现

#### **1.** 算法介绍

SM4 算法是一种分组密码算法。其分组长度为 128bit，密钥长度也为 128bit。加密算法与密钥扩展算法均采用 32 轮非线性迭代结构，以字（32 位）为单位进行加密运算，每一次迭代运算均为一轮变换函数 F。SM4 算法加/解密算法的结构相同，只是使用轮密钥相反，其中解密轮密钥是加密轮密钥的逆序。

#### **2.** 密钥扩展算法


加密密钥 $MK− (MK_0, MK_1, MK_2, MK_3)\in (Z^{32}_2)^4$，轮密钥生成方法为：

$(K_0, K_1, K_2, K_3) − (MK_0 ⊕FK_0, MK_1 ⊕FK_1, MK_2 ⊕FK_2, MK_3 ⊕FK_3), rk_i−K_{i+4 }−K_i⊕T′ (K_{i+1} ⊕K_{i+2}⊕K_{i+3} ⊕CK_i)$, $i=0,1,\cdots 31$。

其中：

(1)T'是将合成置换 T 的线性变换L替换为 L':

$L' (B) − B⊕ (B <<< 13) ⊕ (B <<<23)$


(2) 系统参数FK的取值为：
$FK_0 − (A3B1BAC6), FK_1 − (56AA3350), FK_2 − (677D9197), FK_3−(B27022DC)$


(3) 固定参数 CK 取值方法为：

设 ck_{i,j}  为 CK_i 的第j字节 $(i=0 ,1, \cdots  31; j=0, 1, 2, 3)$, 即 $$ CK_i−(ck_{i,0}, ck_{i,1}, ck_{i,2}, ck_{i,3}) \in (Z^{8}_2)^4 $$ , $$ ck_{i,j}− (4i + j) \times  7(\ mod \ 256) 
 $$ 。其中固定参数 $ CK_i(i= 0, 1,\cdots 31) $.
​		
#### **3.** 加密过程

本加密算法由 32 次迭代运算和 1 次反序变换构成（Feistel密码结构）。

轮函数：设输入为$(X_0,X_1,X_2,X_3)\in (Z^{32}_2)^4$ , 轮密钥为  $ rk\in (Z^{32}_2)$,则轮函数 $F$为：$F(X_0,X_1,X_2,X_3,rk)-X_0⊕ (X_1,X_2,X_3,rk)$

​		合成置换$T:Z^{32}_2\rightarrow Z^{32}_2$是一个可逆变换，由非线性变换 *τ* 和线性变换*L* 复合而成.


设明文输入为$(X_0,X_1,X_2,X_3)\in (Z^{32}_2)^4$ ，密文输出为$(Y_0,Y_1,Y_2,Y_3)\in (Z^{32}_2)^4$  , 轮密钥为$rk_i\in (Z^{32}_2)$, $i=0,1,\cdots 31$。加密算法的运算过程如下：

* (1)32 次迭代运算：$X_{i+4}-F(X_i,X_{i+1},X_{i+2},X_{i+3},rk_i)$$i=0,1,\cdots 31$；

* (2) 反序变换：

$ (Y_0, Y_1, Y_2, Y_3)−R(X_{32}, X_{33}, X_{34}, X_{35})−(X_{35}, X_{34}, X_{33}, X_{32})$。

#### **4.** 解密过程

本算法的解密变换与加密变换结构相同，不同的仅是轮密钥的使用顺

序。解密时，使用轮密钥序列 (rk_{31}, rk_{30}, . . . , rk_0)。




## AES实现

### **AES的加密过程**

AES使用SPN结构。 加密轮数依赖于密钥长度：
| Key Size (bits) | round               
| ----------------| ---------------- 
| 128              | 10           
| 192              | 12     
| 256              | 14


对于AES-128加密算法而言，在第一轮开始前，将明文与密钥进行异或，然后进行9轮迭代的操作，每一轮中包括4个不同的变换：字节代替（SubBytes）、行移位（ShiftRows）、列混淆（MixColumns）和轮密钥加（AddRoundKey）。最后一轮仅包含三个变换：字节代替（SubBytes）、行移位（ShiftRows）和轮密钥加（AddRoundKey）。

加密过程如图所示：

![](https://pic.imgdb.cn/item/64cbc6f51ddac507ccb4d558.png)

***

#### 字节替代（SubBytes）

AES定义了一个S盒，并使用S盒对每个字节进行替换，替换规则为：高4位作为行值，低4位作为列值，从S盒的对应位置取出元素作为替换。

16个字节均采用相同的S盒，S盒是AES算法中唯一的非线性部件。

```C++
void subBytes(uint8_t a[4][4]) {

    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            int temp = a[i][j];
            int row = temp / 16;
            int column = temp % 16;
            a[i][j] = S_BOX[row][column];

        }
    }
}

```

#### 行移位（ShiftRow）

每一行按字节循环移位，第一行循环左移0个字节，第二行<<<1，第三行<<<2,第四行<<<3，使得某一列的四个字节扩散到4列。

```C++
void shiftRows(uint8_t a[4][4]) {
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < i; ++j) {

            int temp = a[i][0];
            a[i][0] = a[i][1];
            a[i][1] = a[i][2];
            a[i][2] = a[i][3];
            a[i][3] = temp;
        }
    }
}


```


#### 列混合（MixColumn）

以列为单位，使得输出的每一个字节和输入的四个字节有关。

代码实现：
```C++
void mix_columns(uint8_t state[4][4]) {
    uint8_t tmp[4];
    for (int i = 0; i < 4; ++i) {
        tmp[0] = galois_mul(0x02, state[0][i]) ^ galois_mul(0x03, state[1][i]) ^ state[2][i] ^ state[3][i];
        tmp[1] = state[0][i] ^ galois_mul(0x02, state[1][i]) ^ galois_mul(0x03, state[2][i]) ^ state[3][i];
        tmp[2] = state[0][i] ^ state[1][i] ^ galois_mul(0x02, state[2][i]) ^ galois_mul(0x03, state[3][i]);
        tmp[3] = galois_mul(0x03, state[0][i]) ^ state[1][i] ^ state[2][i] ^ galois_mul(0x02, state[3][i]);

        state[0][i] = tmp[0];
        state[1][i] = tmp[1];
        state[2][i] = tmp[2];
        state[3][i] = tmp[3];
    }
}


```

做GF($2^{8}$)上的乘法，模不可约多项式$m(x)$的乘法运算，$m(x)$=$x^{8}$ +$x^{4}$ +$x^{3}$ +$x$ +1

其中：$S'_{0,c}=(\lbrace 02\rbrace \cdot S_{0,c})⊕ (\lbrace 03\rbrace \cdot S_{1,c})⊕ S_{2,c} ⊕ S_{3,c}$

此外，列混合变换的矩阵中的数字选取了{01}{02}{03}，加密速度较快。一般情况下，加密比解密更重要，设计算法时，优先保证加密的效率。例如：

　　1、CFB和OFB工作模式，只采用加密算法

　　2、部分消息认证码MAC的构造只用到加密过程


#### 密钥扩展方案

需要将128比特的主密钥扩展为44个32比特字。首先将主密钥转化为4个32 bits的字，分别记为$W_{0}$，$W_{1}$，$W_{2}$，$W_{3}$，接下来通过下述步骤求出各轮的轮密钥。

1.将上一轮轮密钥的最后一列$W_{i-1}$循环左移一个字节。
2.将结果中的每个字节依次经过S盒的查表
3.查表后得到的结果与$W_{i-4}$、以及一个32 bits的常量（常量矩阵见下图）以及进行异或，就能得到该轮轮密钥的第一列。
4.每一轮轮密钥的第一列使用上述方法求出，其余二、三、四列都直接通过异或运算得到。$W_{i}$=$W_{i-4}$⊕$W_{i-1}$，后续每一轮均按照此步骤进行处理。

```C++
void keyExpansion(uint8_t key[][4], uint8_t w[][4][4]) {
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            w[0][i][j] = key[i][j];
        }
    }
    for (int i = 1; i < 11; ++i) {
        for (int j = 0; j < 4; ++j) {
            int temp[4];
            if (j == 0) {
                temp[0] = w[i - 1][3][1];
                temp[1] = w[i - 1][3][2];
                temp[2] = w[i - 1][3][3];
                temp[3] = w[i - 1][3][0];
                for (int k = 0; k < 4; ++k) {
                    int m = temp[k];
                    int row = m / 16;
                    int column = m % 16;
                    temp[k] = S_BOX[row][column];
                    if (k == 0) {
                        temp[k] = temp[k] ^ RC[i - 1];
                    }
                }
            }
            else {
                temp[0] = w[i][j - 1][0];
                temp[1] = w[i][j - 1][1];
                temp[2] = w[i][j - 1][2];
                temp[3] = w[i][j - 1][3];
            }
            for (int l = 0; l < 4; ++l) {

                w[i][j][l] = w[i - 1][j][l] ^ temp[l];
            }

        }
    }
}


```

### **AES的解密过程**

AES使用SPN结构，加解密函数不同。除了异或密钥，S盒、行移位、列混合都为原先的逆运算，密钥逆序使用。


## 运行结果

### SM4
测试数据为：
```C++
 unsigned int key[4] = { 0x20200015,0x00772020,0x00150077,0x12345678 };
 unsigned int plaintext[4] = { 0x12345678,0x12345678,0x12345678,0x12345678 };
 unsigned int ciphertext[4] = { 0x0EE39625,0x2C0C2F8C,0x7DA76895,0xCD0D349A };
```
其中密文由明文加密获得，如下图所示：

![](https://pic.imgdb.cn/item/64cbbef61ddac507cc9b6598.jpg)

### AES
输入小于16位长度的字符串，输出AES的加密结果如下图所示：

![](https://pic.imgdb.cn/item/64cba7d91ddac507cc563976.jpg)
 


##  引文参考
[1]https://blog.csdn.net/weixin_45859485/article/details/118515873
