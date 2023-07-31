# exclusion proof
# 1.要求基于交易排序的Merkel tree
# 2.查找小于交易额的前一个交易pre与大于交易额的下一笔交易next（数据块数值）
# 3.通过inclusion proof证明数据块pre与next存在
# 4.通过验证相邻通过夹逼确定排除性
# 5.由于要求基于排序的Merkel tree，故在本实验中采取随机数代替交易值
# 6.由于调用 Python 对象时有最大递归深度限制，故使用99个叶子节点模拟过程
import math
import hashlib
import random

def generate_sorted_list(length):
    sorted_list = [random.randint(1, 100)]
    for _ in range(length - 1):
        next_element = sorted_list[-1] + random.randint(1, 10)
        sorted_list.append(next_element)

    return sorted_list

def hash_sha256(data):
    data_bytes = data.encode('utf-8')         # 将输入数据编码为 utf-8 格式的字节序列
    sha256_hash = hashlib.sha256(data_bytes)  # 计算 SHA-256 哈希值
    hash_value = sha256_hash.hexdigest()
    return hash_value

def merkle_tree_init_order(num):               # 将各项数据进行初始化
    if num & (num - 1) == 0:                   # 把num最右边的1变为0，其它位不变。如果是2的幂次，那么只有1个1，减1后变为0，与原数做与操作结果为0。
        deep = int(math.log(num, 2)) + 1
    else:                                      # n不为2的幂次
        deep = int(math.log(num, 2)) + 2
    k = deep
    tree = [None] * k                      # 层数
    leaf_node = [None] * num
    data_block = [None] * num
    tree[k - 1] = data_block                # 将最底层的数据块数组赋值给tree数组的最后一个元素
    k = k - 2                               # 当前层数
    for i in range(num):                    # 生成叶子结点
        leaf_node[i] = data_message_order[i]
        data_block[i] = hash_sha256('00' + str(data_message_order[i]))
    return k,deep,tree,leaf_node,data_block

def create_merkle_tree_order(node_list):         # 创建Merkle Tree
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
    return create_merkle_tree_order(new_node_list)          # 递归调用生成root节点

def path(m,num,data_block3):
    global path_hash
    if num == 1:
        path_hash.append(data_block3[0])      #已经到达 Merkle Tree 的叶子节点，此时将节点的哈希值添加到列表
        return 0
    if num & (num - 1) == 0:         #判断是否为2的幂次
        p = 2 ** (int(math.log(num, 2))-1)
    else:
        p = 2 ** int(math.log(num, 2))
    if m < p:                                 #二分法查找要找的节点在左子树
        path_hash.append(create_merkle_tree_order(data_block3[p:num]))      #将右子树的哈希值添加到 path_hash 列表中
        print(data_block3[p:num])
        data_block3 = data_block3[0:p]     #更新 data_block，只保留左子树的数据块
        new_m = m           #递归使用
        new_num = p
        direction.append(0)       #0表示向左走
    else:
        path_hash.append(create_merkle_tree_order(data_block3[0:p]))    #将左子树的哈希值添加到 path_hash 列表中
        data_block3 = data_block3[p:num]      #更新 data_block，只保留右子树的数据块
        new_m = m - p
        new_num = num - p
        direction.append(1)         #1表示向右走
    return path(new_m,new_num,data_block3)

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

def inclusion_proof(m,node_num,data_block):          # 构建指定元素的包含证明与排除证明
    path(m, node_num,data_block)
    # print('要求数据的hash值为：',data_block[m])
    proof = cal_root()
    if root == proof:
        print('包含性证明成立')
        return True
    else:
        print('结点不存在')
        return False

def find_leaf_pre(value,num):
    low = 0
    high = num-1
    if value < data_message_order[low] or value > data_message_order[high]:
        print("节点不在Merkle tree中")
        return None
    while data_message_order[low] <= data_message_order[high]:
        mid = int((low + high) / 2)
        if data_message_order[mid]==value:
            return mid-1
        if (data_message_order[mid] < value) and (value < data_message_order[mid+1]):
            return mid 
        elif data_message_order[mid] < value:
            low = mid
        else:
            high = mid

def find_leaf_next(value,num):
    low = 0
    high = num-1
    if (value < data_message_order[low]) or (value > data_message_order[high]):
        print("节点不在Merkle tree中")
        return None
    while data_message_order[low] <= data_message_order[high]:
        mid = int((low + high) / 2)
        if data_message_order[mid]==value:
            return mid+1
        if (data_message_order[mid] < value) and (value < data_message_order[mid+1]):
            return mid + 1
        elif data_message_order[mid] < value:
            low = mid
        else:
            high = mid
            
def exclusion_proof(num,value,data_block1,data_block2):
    pre=find_leaf_pre(value, num)
    next=find_leaf_next(value,num)
    print("pre=",pre)
    print("next=",next)
    if inclusion_proof(pre,num,data_block1) :
        global path_hash
        global direction
        path_hash = []
        direction = []
        if inclusion_proof(next,num,data_block2):
            if pre+1 == next:
                print("排除性证明成功，节点不存在")
            else:
                print("排除性证明失败，节点可能存在")
    return 

num=100
value=159
data_message_order = generate_sorted_list(num)
k,deep,tree,leaf_node,data_block = merkle_tree_init_order(num)
data_block1=data_block2=data_block
print(leaf_node)
root = create_merkle_tree_order(data_block)
path_hash = []
direction = []
exclusion_proof(num,value,data_block1,data_block2)


