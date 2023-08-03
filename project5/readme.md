# <center> 遵循 RFC6962 实现 Merkle Tree </center>

## 运行方式
### 验证inclusion proof
* 运行merkle_tree.py即可
  
### 验证exclusion proof
* 运行exclusion_proof.py即可

## 实验要求
* 1.构建拥有十万叶子结点的merkle_tree
* 2.构建指定元素的存在性证明
* 3.构建指定元素的排除性证明

## 1.merkle_tree的构建
在 RFC 6962 文中，Merkle 树用于创建证书数据的仅附加日志。 树结构通过创建从叶节点（单个证书）到树根的加密哈希链，可以有效验证证书数据。 对证书数据的任何篡改或修改都将导致计算出的根哈希值与可信根哈希值之间不匹配。通常需要经过以下步骤：
* 1.收集需要记录的证书数据。
* 2.将证书数据组织成 Merkle 树结构，叶节点代表各个证书。
* 3.计算每个证书的加密哈希值并将其沿树传播以计算每个内部节点的哈希值。
* 4.计算 Merkle Tree 的根哈希值，将其作为验证的可信锚点。
* 5.以安全且防篡改的方式存储根哈希和 Merkle 树，例如在仅附加日志中。
* 6.要验证证书的真实性，请遵循从叶节点到根节点的 Merkle Tree 路径并计算哈希链。 将计算出的根哈希与可信根哈希进行比较，以确保数据完整性。
  
遵循RFC6962的merkle tree结构如下图所示：
![](https://pic.imgdb.cn/item/64cb4a471ddac507cc6eead8.jpg)

根据RFC6962文档，首先对每一个叶子结点的值进行编码，然后在前面补充0x00，得到和叶子结点数量一样的Hash值，从左到右进行遍历，两两组合拼接后在前面补充0x01，如果有落单的Hash值就往上挪一层，如果该层节点非偶，则将最后一个节点上升一层。

在此实验中，我们令Merkle-Tree的叶子节点的值由字符串"leafvalue"加10位随机字符构成
```python
map = string.punctuation + string.ascii_letters + string.digits
for i in range(num):                    # 生成叶子结点数据
    for j in range(10):
        data_message += random.choice(map)
```

按照上述Merkle-Tree结构迭代生成root结点，哈希函数使用hashlib库提供的SHA256函数：

```python
def create_merkle_tree(node_list):         # 创建Merkle Tree
    l = len(node_list)
    if l == 1:                      # 已经构建到了树的根节点，直接返回该节点作为 Merkle Root
        return node_list[0]        
    new_node_list = []
    for i in range(0, l-1, 2):
        node1 = node_list[i]
        node2 = node_list[i + 1]          # 合并节点数据并计算哈希值
        combined_data = '01' + node1 + node2
        hash_value = hash_sha256(combined_data)
        new_node_list.append(hash_value)
    if l % 2 == 1:
        new_node_list.append(node_list[l-1])          # 最后一个节点将无法与其它节点成对，直接将其添加到 new_node_list 的末尾
    return create_merkle_tree(new_node_list)          # 递归调用生成root节点
```

## 2.指定元素的存在性证明
存在性证明用于检验给定数据是否在merkle tree上（不需要知道完整数据信息）。已知索引后用于审计路径和存在性证明。根据索引从根节点出发通过二分法查找叶子节点索引对应路径并记录审核路径，找到叶子结点后根据审核路径上的需要用到的哈希信息逆推root结点的数值。若一致则证明存在。可以打印路径信息用作证据。


## 3.指定元素的排除性证明
排除性证明用于检验给定数据是否在merkle tree上（不需要知道完整数据信息）。目前的排除性证明方法依赖于排序merkle tree，因此我们生成升序的叶子结点进而生成排序merkle tree，通过对集合中的元素进行排序，可以使用默克尔树来证明某些元素的非隶属关系。为了证明某个元素 不在集合中，需显示两侧的元素（进行存在性证明）。若两侧的元素相邻，则通过夹逼原理可进行排除性证明，否则有一定概率该节点存在。
过程如下：
* 查找小于交易额的前一个交易pre与大于交易额的下一笔交易next（数据块数值）
* 通过inclusion proof证明数据块pre与next存在
* 通过验证相邻通过夹逼确定排除性

## 4.运行结果
1.验证inclusion proof（以1000个叶子结点为例，生成10w叶子结点可更改实参）
![](https://pic.imgdb.cn/item/64cb48e51ddac507cc6b5ca3.jpg)

2.验证exclusion proof（以100个叶子结点为例，生成10w叶子结点可更改实参num）
![](https://pic.imgdb.cn/item/64cb42ac1ddac507cc5a1b4b.jpg)

## 引文参考
[1]https://www.jianshu.com/p/bfe990be3a21

[2]https://gist.github.com/chris-belcher/eb9abe417d74a7b5f20aabe6bff10de0

[3]https://dl.acm.org/doi/abs/10.17487/RFC6962
