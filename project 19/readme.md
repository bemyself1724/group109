# Project19: forge a signature to pretend that you are Satoshi.

## 实验内容
比特币中使用ECDSA进行签名，本次实验研究如何在未知明文消息m的前提下，伪造能通过检验的合法签名。<br>

## 实验原理
假设已经得到了真实且合法的签名(r,s)。<br>
在验证算法中，s^{-1}(eG+rP)=R=(x',y')，只需验证r=x' mod n是否成立。<br>
针对此过程，我们随机选择u,v，计算R'=(x',y')=uG+vP。<br>
当s'^{-1}(e'G+r'P)=uG+vP，计算得到(r',s',e')，这样就伪造得到可以通过验证的签名。<br>

## 实验过程
1. 生成Satoshi的公私钥<br>
2. 伪造签名<br>
3. 验证签名<br>


## 运行方法
* 直接运行文件main.py

## 运行结果

![](https://pic.imgdb.cn/item/64cd1b8c1ddac507cc79a12c.jpg)