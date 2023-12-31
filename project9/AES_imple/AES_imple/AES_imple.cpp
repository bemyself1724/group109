﻿#include <iostream>
#include <stdint.h>
#include <iomanip>
#include <string>
#include <sstream>
#include <time.h>


using namespace std;

//定义S盒
uint8_t S_BOX[16][16] = { 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
                               0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
                               0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
                               0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
                               0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
                               0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
                               0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
                               0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
                               0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
                               0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
                               0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
                               0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
                               0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
                               0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
                               0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
                               0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 };


//常量轮值表
uint8_t RC[10] = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36 };


//密钥拓展算法
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

//轮密钥加
void addRoundKey(uint8_t a[4][4], uint8_t k[4][4]) {
    // 由于用w[11][4][4]表示W[44]导致行列转置，所以在进行异或操作的时候应该是a[i，j] 异或 k[j,i]
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            a[i][j] = a[i][j] ^ k[i][j];
        }
    }
}





//字节代换
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

//行移位
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

// Multiply two elements in GF(2^8)
uint8_t galois_mul(uint8_t a, uint8_t b) {                     //a是乘法矩阵，b是行变换后明文
    uint8_t p = 0;
    uint8_t hi_bit_set;
    for (int i = 0; i < 8; ++i) {
        if ((b & 1) == 1) {
            p ^= a;
        }
        hi_bit_set = (a & 0x80);
        a <<= 1;
        if (hi_bit_set == 0x80) {
            a ^= 0x1B; // 00011011
        }
        b >>= 1;
    }
    return p;
}

// AES MixColumns step
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


void AES_ENCRYPT(char* input)
{
    int i, j;
    uint8_t a[] = { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };
    for (int i = 0; i < 16; i++)
    {
        a[i] = int(input[i]);
        /*cout << a[i] << endl;*/
    }
    a[12] = 0x00;
    a[13] = 0x00;
    a[14] = 0x00;
    a[15] = 0x00;

    uint8_t  plaintext[4][4];

    for (j = 0; j < 4; j++)
    {
        for (i = 0; i < 4; i++)
        {
            plaintext[i][j] = a[4 * j + i];
        }
    }

    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 4; j++)
        {
            cout << "0x" << hex << (unsigned int)plaintext[i][j] << " "; // 将unsigned char类型转换成16进制输出
        }
        cout << endl;
    }



    //下面是密钥扩展及输出验证
    uint8_t exkey[11][4][4];
    keyExpansion(plaintext, exkey); //因为密钥和明文一样，直接传入plaintext



    //下面是初始轮密钥加
    addRoundKey(plaintext, exkey[0]);

    //下面十轮迭代
    int round = 0;
    for (round = 0; round < 10; round++)
    {
        subBytes(plaintext);
        shiftRows(plaintext);
        if (round < 9)
        {
            mix_columns(plaintext);
        }
        addRoundKey(plaintext, exkey[round + 1]);
    }

    cout << "加密结果为：" << endl;
    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 4; j++)
        {
            cout << "0x" << hex << (unsigned int)plaintext[i][j] << " "; // 将unsigned char类型转换成16进制输出
        }
        cout << endl;
    }


}
int main() {

    char input[16];
    cout << "请输入要加密的信息，小于16位: ";
    cin >> input;
    clock_t start = clock();
    AES_ENCRYPT(input);
    clock_t end = clock();
    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    printf("Time measured: %.3f seconds.\n", elapsed);
    return 0;

}

