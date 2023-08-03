# 构建Merkle Tree
# 1.首先对每一个要创建的数据块进行编码，然后在前面补充0x00，得到数量一样的Hash值作为叶子节点数据
# 2.从左到右一次遍历，两个一组拼接后两两组合，拼接后在前面补充0x01，如果有奇数Hash值就上移一层
# 3.递归得到一个root节点hash值
#  inclusion proof
# 1.根据索引从根节点出发查找叶子节点路径并记录审核路径
# 2.由数据块值和路径计算根节点并比对初始化的merkel_root
# 3.一致则验证了包含性
# exclusion proof
# 1.要求基于交易排序的Merkel tree
# 2.查找小于交易额的前一个交易pre与大于交易额的下一笔交易next（数据块数值）
# 3.通过inclusion proof证明数据块pre与next存在
# 4.通过验证相邻通过夹逼确定排除性
# 5.由于要求基于排序的Merkel tree，故在本实验中采取随机数代替交易值


import math
import hashlib
import random
import codecs
import string


map = string.punctuation + string.ascii_letters + string.digits

def hash_sha256(data):
    data_bytes = data.encode('utf-8')         # 将输入数据编码为 utf-8 格式的字节序列
    sha256_hash = hashlib.sha256(data_bytes)  # 计算 SHA-256 哈希值
    hash_value = sha256_hash.hexdigest()
    return hash_value

def merkle_tree_init(num):                     # 将各项数据进行初始化
    if num & (num - 1) == 0:                   # 把num最右边的1变为0，其它位不变。如果是2的幂次，那么只有1个1，减1后变为0，与原数做与操作结果为0。
        deep = int(math.log(num, 2)) + 1
    else:                                      # n不为2的幂次
        deep = int(math.log(num, 2)) + 2
    k = deep
    tree = [None] * k                      # 层数
    leaf_node = [None] * num
    data_block = [None] * num
    data_message = 'leafvalue'              # 用来生成叶子结点数据
    tree[k - 1] = data_block                # 将最底层的数据块数组赋值给tree数组的最后一个元素
    k = k - 2                               # 当前层数
    for i in range(num):                    # 生成叶子结点
        for j in range(10):
            data_message += random.choice(map)
        leaf_node[i] = data_message
        data_block[i] = hash_sha256('00' + data_message)
    return k,deep,tree,leaf_node,data_block


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


k,deep,tree,leaf_node,data_block = merkle_tree_init(1000)
root = create_merkle_tree(data_block)
path_hash = []        #用于存储路径中需要借助的哈希值，用于路径审核
direction  = []        #存在性证明
# path_hashvalue=[]
# path_directionvalue=[]

def path(m,num):
    global path_hash          
    global data_block          #存储了Merkle Tree中所有叶子节点的数据块
    if num == 1:
        path_hash.append(data_block[0])      #已经到达 Merkle Tree 的叶子节点，此时将节点的哈希值添加到列表
        return 0
    if num & (num - 1) == 0:         #判断是否为2的幂次
        p = 2 ** (int(math.log(num, 2))-1)
    else:
        p = 2 ** int(math.log(num, 2))
    if m < p:                                 #二分法查找要找的节点在左子树
        path_hash.append(create_merkle_tree(data_block[p:num]))      #将右子树的哈希值添加到 path_hash 列表中
        data_block = data_block[0:p]     #更新 data_block，只保留左子树的数据块
        new_m = m           #递归使用
        new_num = p
        direction.append(0)       #0表示向左走
    else:
        path_hash.append(create_merkle_tree(data_block[0:p]))    #将左子树的哈希值添加到 path_hash 列表中
        data_block = data_block[p:num]      #更新 data_block，只保留右子树的数据块
        new_m = m - p
        new_num = num - p
        direction.append(1)         #1表示向右走
    return path(new_m,new_num)

def cal_root():
    l = len(path_hash)
    if l == 1:
        return path_hash[0]
    if direction[l-2] == 0:     #左右判断组合顺序
        path_hash[l-2] = hash_sha256('01' + path_hash[l-1] + path_hash[l-2])
    else:
        path_hash[l-2] = hash_sha256('01' + path_hash[l - 2] + path_hash[l - 1])
    # path_hashvalue.append(path_hash.pop())
    # path_directionvalue.append(direction.pop())
    path_hash.pop()
    direction.pop()
    return cal_root()

def inclusion_proof(m,node_num):          # 构建指定元素的包含证明与排除证明
    if m>node_num:
        print('结点不存在')
        return
    print('要求数据的hash值为：', data_block[m])
    path(m, node_num)
    proof = cal_root()
    if root == proof:
        print('包含性证明成立')
        return
    else:
        print('结点不存在')
        return

index = int(input("共1000个节点，请输入整数节点索引: "))
inclusion_proof(index,1000)
