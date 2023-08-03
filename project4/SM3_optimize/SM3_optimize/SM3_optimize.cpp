#pragma warning(disable:4996)
#include<iostream>
#include<bitset>
#include<sstream>
#include<fstream>
#include<intrin.h>
using namespace std;


int IV[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d ,0xb0fb0e4e };
int IV2[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d ,0xb0fb0e4e };
int T[2] = { 0x79cc4519 ,0x7a879d8a };
char* plaintext_after_padding;     //定义全局变量用于存储填充后的块值
int length;

string strtobin(const string& msg) {          //字符串转化为二进制串
    string msg_bin;
    for (char c : msg) {
        uint8_t ascii_i = static_cast<uint8_t>(c);
        for (int i = 7; i >= 0; i--) {
            msg_bin += ((ascii_i >> i) & 1) ? '1' : '0';
        }
    }
    return msg_bin;
}

string padding(const string& m) {
    int length = m.length();
    string m_bin = m + "1";
    int k = (448 - length - 1) % 512;
    if (k < 0) {
        k += 512;
    }
    m_bin += string(k, '0');
    stringstream ss;
    ss << bitset<64>(length);
    m_bin += ss.str();
    return m_bin;
}

int padding_divide(char plaintext[]) {
    int lenth = strlen(plaintext);
    long long bit_len = lenth * 8;     //计算明文消息的长度（以比特为单位）
    int final_logstr = (bit_len / 512) * 4 * 16;     //计算最终填充后的消息长度（以字符为单位）
    int final_block_long = bit_len % 512;       //需填充模块
    if (final_block_long < 448) {                //在明文消息的末尾填充至少一个1，然后补足使得填充后的消息长度满足 (lenth / 64 + 1) * 64。
        int lenth_after_padding = (lenth / 64 + 1) * 64;
        plaintext_after_padding = new char[lenth_after_padding];  //动态分配内存以存储填充后的消息
        strcpy(plaintext_after_padding, plaintext);
        plaintext_after_padding[lenth] = 0x80;   //在原始明文消息的末尾填充一个1，即0x80
        for (int i = lenth + 1; i < lenth_after_padding - 8; i++)    //从原始明文消息的下一个位置开始，填充0
        {
            plaintext_after_padding[i] = 0;
        }
        for (int i = lenth_after_padding - 8, j = 0; i < lenth_after_padding; i++, j++) //留出8个字节的位置来存储消息长度信息
        {
            plaintext_after_padding[i] = ((char*)&bit_len)[7 - j];
        }
        return lenth_after_padding;
    }
    else if (final_block_long >= 448)          //当前的消息块中不足以填充 1 和 0，则需要增加一个新的消息块
    {
        int lenth_after_padding = (lenth / 64 + 2) * 64;    //计算填充后的消息长度，使其是64的整数倍，增加两个块长度,确保在最后一个块中填充消息长度信息
        plaintext_after_padding = new char[lenth_after_padding];   //其他同上
        strcpy(plaintext_after_padding, plaintext);
        plaintext_after_padding[lenth] = 0x80;
        for (int i = lenth + 1; i < lenth_after_padding - 8; i++) {
            plaintext_after_padding[i] = 0;
        }

        for (int i = lenth_after_padding - 8, j = 0; i < lenth_after_padding; i++, j++) {
            plaintext_after_padding[i] = ((char*)&bit_len)[7 - j];
        }
        return lenth_after_padding;
    }
}

int T_j(int j) {
    if (j >= 0 && j <= 15) {
        return T[0];
    }
    else {
        return T[1];
    }
}
int loop_left(int x, int n) {
    return (x << n) | ((unsigned int)x >> (32 - n));
}

int p0(int x) {
    return x ^ loop_left(x, 9) ^ loop_left(x, 17);
}

int p1(int x) {
    return x ^ loop_left(x, 15) ^ loop_left(x, 23);
}

int ff(int x, int y, int z, int j) {
    if (j >= 0 && j <= 15) {
        return (x ^ y ^ z);
    }
    else {
        return (x & y) | (x & z) | (y & z);
    }
}

int gg(int x, int y, int z, int j) {
    if (j >= 0 && j <= 15) {
        return x ^ y ^ z;
    }
    else {
        return (x & y) | ((~x) & z);
    }
}


int reversebytes_uint32t(int value)         //SM3为大端格式存储，所以在标准运算中，针对每个待哈希的值应该进行翻转字节顺序
{
    return (value & 0x000000FFU) << 24 | (value & 0x0000FF00U) << 8 |
        (value & 0x00FF0000U) >> 8 | (value & 0xFF000000U) >> 24;
}


void CF(int* V, int* BB) {
    int W[68];
    int w_1[64];
    for (int i = 0; i < 16; i++)
    {
        W[i] = reversebytes_uint32t(BB[i]);
    }
    for (int i = 16; i < 68; i++)
    {
        W[i] = p1(W[i - 16] ^ W[i - 9] ^ (loop_left(W[i - 3], 15))) ^ loop_left(W[i - 13], 7) ^ W[i - 6];

    }
    for (int i = 0; i < 64; i++) {
        w_1[i] = W[i] ^ W[i + 4];

    }
    int A = V[0], B = V[1], C = V[2], D = V[3], E = V[4], F = V[5], G = V[6], H = V[7];

    for (int i = 0; i < 64; i++) {
        int SS1 = loop_left(loop_left(A, 12) ^ E ^ loop_left(T_j(i), i % 32), 7);
        int SS2 = SS1 ^ loop_left(A, 12);
        int TT1 = ff(A, B, C, i) ^ D ^ SS2 ^ w_1[i];
        int TT2 = gg(E, F, G, i) ^ H ^ SS1 ^ W[i];
        D = C;
        C = loop_left(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = loop_left(F, 19);
        F = E;
        E = p0(TT2);


    }
    V[0] = A ^ V[0];
    V[1] = B ^ V[1];
    V[2] = C ^ V[2];
    V[3] = D ^ V[3];
    V[4] = E ^ V[4];
    V[5] = F ^ V[5];
    V[6] = G ^ V[6];
    V[7] = H ^ V[7];

}

void sm3(char plaintext[], int* hash_val) {
    int n = padding_divide(plaintext) / 64;
    for (int i = 0; i < n; i++) {
        CF(IV, (int*)&plaintext_after_padding[i * 64]);
    }
    for (int i = 0; i < 8; i++) {
        hash_val[i] = reversebytes_uint32t(IV[i]);
    }
    memcpy(IV, IV2, 64);
}

__m128i left_simd(__m128i a, int k)
{
    k = k % 32;
    __m128i tmp1, tmp2, tmp3, tmp4;
    __m128i zhengshu = _mm_set_epi32(0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF);  //定义一个128位整数，其所有位均为1
    tmp2 = _mm_and_si128(zhengshu, _mm_slli_epi32(a, k));   //将a向左移动 k 位，并将结果与整数进行按位与操作，将多余的位清零
    tmp3 = _mm_srli_epi32(_mm_and_si128(zhengshu, a), 32 - k);  //将 a 向右移动 32 - k 位，并将结果与整数进行按位与操作，将多余的位清零
    tmp4 = _mm_or_si128(tmp2, tmp3);
    return tmp4;
}

__m128i P1_simd(__m128i X) {
    __m128i tmp1, tmp2, tmp3, tmp4, tmp5;
    tmp1 = X;
    tmp2 = left_simd(X, 15);
    tmp3 = left_simd(X, 23);
    tmp4 = _mm_xor_si128(tmp1, tmp2);
    tmp5 = _mm_xor_si128(tmp4, tmp3);
    return tmp5;
}

//__m128i P0_simd(__m128i X) {
//    __m128i tmp1, tmp2, tmp3, tmp4, tmp5;
//    tmp1 = X;
//    tmp2 = left_simd(X, 9);
//    tmp3 = left_simd(X, 17);
//    tmp4 = _mm_xor_si128(tmp1, tmp2);
//    tmp5 = _mm_xor_si128(tmp4, tmp3);
//    return tmp5;
//}

void CF_simd(int* V, int* BB) {
    int W[68];
    int w_1[64];
    __m128i w16, w9, w13, w3, w6, w16_or_w9, LL15_w3, LL7_w13, w16_or_w9_or_LL15_w3, LL7_w13_or_w6, P, re;

    for (int i = 0; i < 16; i++)
    {
        W[i] = reversebytes_uint32t(BB[i]);
    }

    for (int j = 4; j < 17; j++)
    {
        W[j * 4] = p1(W[j * 4 - 16] ^ W[j * 4 - 9] ^ (loop_left(W[j * 4 - 3], 15))) ^ loop_left(W[j * 4 - 13], 7) ^ W[j * 4 - 6];
        w16 = _mm_setr_epi32(W[j * 4 - 16], W[j * 4 - 15], W[j * 4 - 14], W[j * 4 - 13]);  //w0||w1||w2||w3
        w13 = _mm_setr_epi32(W[j * 4 - 13], W[j * 4 - 12], W[j * 4 - 11], W[j * 4 - 10]);
        w9 = _mm_setr_epi32(W[j * 4 - 9], W[j * 4 - 8], W[j * 4 - 7], W[j * 4 - 6]);    //w8||...||w11
        w6 = _mm_setr_epi32(W[j * 4 - 6], W[j * 4 - 5], W[j * 4 - 4], W[j * 4 - 3]);
        w3 = _mm_setr_epi32(W[j * 4 - 3], W[j * 4 - 2], W[j * 4 - 1], W[j * 4]);
        w16_or_w9 = _mm_xor_si128(w16, w9);       //W[i - 16] ^ W[i - 9]
        LL15_w3 = left_simd(w3, 15);              //loop_left(W[i - 3], 15)
        LL7_w13 = left_simd(w13, 7);              //loop_left(W[i - 13], 7)
        w16_or_w9_or_LL15_w3 = _mm_xor_si128(w16_or_w9, LL15_w3);    //(W[i - 16] ^ W[i - 9] ^ (loop_left(W[i - 3], 15))
        LL7_w13_or_w6 = _mm_xor_si128(LL7_w13, w6);       //loop_left(W[i - 13], 7) ^ W[i - 6]
        P = P1_simd(w16_or_w9_or_LL15_w3);
        re = _mm_xor_si128(P, LL7_w13_or_w6);
        memcpy(&W[j * 4], (int*)&re, 16);         //进行4个W[]的填充
    }

    //for (int j = 4; j < 17; j += 2)      // 步长2（对i来说是8）,存在缓冲区溢出的问题未解决
    //{
    //    W[j * 4] = p1(W[j * 4 - 16] ^ W[j * 4 - 9] ^ (loop_left(W[j * 4 - 3], 15))) ^ loop_left(W[j * 4 - 13], 7) ^ W[j * 4 - 6];
    //    w16 = _mm_setr_epi32(W[j * 4 - 16], W[j * 4 - 15], W[j * 4 - 14], W[j * 4 - 13]);
    //    w9 = _mm_setr_epi32(W[j * 4 - 9], W[j * 4 - 8], W[j * 4 - 7], W[j * 4 - 6]);
    //    w13 = _mm_setr_epi32(W[j * 4 - 13], W[j * 4 - 12], W[j * 4 - 11], W[j * 4 - 10]);
    //    w3 = _mm_setr_epi32(W[j * 4 - 3], W[j * 4 - 2], W[j * 4 - 1], W[j * 4]);
    //    w6 = _mm_setr_epi32(W[j * 4 - 6], W[j * 4 - 5], W[j * 4 - 4], W[j * 4 - 3]);
    //    w16_or_w9 = _mm_xor_si128(w16, w9);       //W[i - 16] ^ W[i - 9]
    //    LL15_w3 = left_simd(w3, 15);              //loop_left(W[i - 3], 15)
    //    LL7_w13 = left_simd(w13, 7);              //loop_left(W[i - 13], 7)
    //    w16_or_w9_or_LL15_w3 = _mm_xor_si128(w16_or_w9, LL15_w3);    //(W[i - 16] ^ W[i - 9] ^ (loop_left(W[i - 3], 15))
    //    LL7_w13_or_w6 = _mm_xor_si128(LL7_w13, w6);       //loop_left(W[i - 13], 7) ^ W[i - 6]
    //    P = P1_simd(w16_or_w9_or_LL15_w3);
    //    re = _mm_xor_si128(P, LL7_w13_or_w6);
    //    memcpy(&W[j * 4], (int*)&re, 16);
    //    W[(j + 1) * 4] = p1(W[(j + 1) * 4 - 16] ^ W[(j + 1) * 4 - 9] ^ (loop_left(W[(j + 1) * 4 - 3], 15))) ^ loop_left(W[(j + 1) * 4 - 13], 7) ^ W[(j + 1) * 4 - 6];
    //    w16 = _mm_setr_epi32(W[(j+1) * 4 - 16], W[(j+1) * 4 - 15], W[(j+1) * 4 - 14], W[(j+1) * 4 - 13]);
    //    w9 = _mm_setr_epi32(W[(j+1) * 4 - 9], W[(j+1) * 4 - 8], W[(j+1) * 4 - 7], W[(j+1) * 4 - 6]);
    //    w13 = _mm_setr_epi32(W[(j+1) * 4 - 13], W[(j+1) * 4 - 12], W[(j+1) * 4 - 11], W[(j+1) * 4 - 10]);
    //    w3 = _mm_setr_epi32(W[(j+1) * 4 - 3], W[(j+1) * 4 - 2], W[(j+1) * 4 - 1], W[(j+1) * 4]);
    //    w6 = _mm_setr_epi32(W[(j+1) * 4 - 6], W[(j+1) * 4 - 5], W[(j+1) * 4 - 4], W[(j+1) * 4 - 3]);
    //    w16_or_w9 = _mm_xor_si128(w16, w9);       //W[i - 16] ^ W[i - 9]
    //    LL15_w3 = left_simd(w3, 15);              //loop_left(W[i - 3], 15)
    //    LL7_w13 = left_simd(w13, 7);              //loop_left(W[i - 13], 7)
    //    w16_or_w9_or_LL15_w3 = _mm_xor_si128(w16_or_w9, LL15_w3);    //(W[i - 16] ^ W[i - 9] ^ (loop_left(W[i - 3], 15))
    //    LL7_w13_or_w6 = _mm_xor_si128(LL7_w13, w6);       //loop_left(W[i - 13], 7) ^ W[i - 6]
    //    P = P1_simd(w16_or_w9_or_LL15_w3);
    //    re = _mm_xor_si128(P, LL7_w13_or_w6);
    //    memcpy(&W[(j + 1) * 4], (int*)&re, 16);
    //}

    for (int i = 0; i < 64; i++) {
        w_1[i] = W[i] ^ W[i + 4];
    }
    int A = V[0], B = V[1], C = V[2], D = V[3], E = V[4], F = V[5], G = V[6], H = V[7];
    for (int i = 0; i < 64; i++) {
        int SS1 = loop_left(loop_left(A, 12) ^ E ^ loop_left(T_j(i), i % 32), 7);
        int SS2 = SS1 ^ loop_left(A, 12);
        int TT1 = ff(A, B, C, i) ^ D ^ SS2 ^ w_1[i];
        int TT2 = gg(E, F, G, i) ^ H ^ SS1 ^ W[i];
        D = C;
        C = loop_left(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = loop_left(F, 19);
        F = E;
        E = p0(TT2);

    }
    V[0] = A ^ V[0];
    V[1] = B ^ V[1];
    V[2] = C ^ V[2];
    V[3] = D ^ V[3];
    V[4] = E ^ V[4];
    V[5] = F ^ V[5];
    V[6] = G ^ V[6];
    V[7] = H ^ V[7];

}

void sm3_simd(char plaintext[], int* hash_val) {
    int n = padding_divide(plaintext) / 64;
    for (int i = 0; i < n; i++) {
        CF_simd(IV, (int*)&plaintext_after_padding[i * 64]);
    }
    for (int i = 0; i < 8; i++) {
        hash_val[i] = reversebytes_uint32t(IV[i]);
    }
    memcpy(IV, IV2, 64);
}



static void dump_buf(char* ciphertext_32, int lenth)     //输出结果
{
    for (int i = 0; i < lenth; i++) {
        printf("%02X ", (unsigned char)ciphertext_32[i]);
    }
    printf("\n");
}


int main() {
    char plaintext[] = "202000150077";
    int hash1[8];
    int hash2[8];
    sm3(plaintext, hash1);
    sm3_simd(plaintext, hash2);
    cout << "加密结果：" << endl;
    dump_buf((char*)hash1, 32);
    cout << "优化后加密结果：" << endl;
    dump_buf((char*)hash2, 32);
    clock_t startTime = clock();
    for (int i = 0; i < 10000; i++) {
        sm3(plaintext, hash1);
    }
    clock_t endTime = clock();
    cout << "一般SM3哈希10000次用时：" << double(endTime - startTime) / CLOCKS_PER_SEC << "s" << endl;
    startTime = clock();
    for (int i = 0; i < 10000; i++) {
        sm3_simd(plaintext, hash2);
    }
    endTime = clock();
    cout << "SIMD与循环展开SM3哈希10000次用时：" << double(endTime - startTime) / CLOCKS_PER_SEC << "s" << endl;

    return 0;
}