
#include <stdio.h>
#include <stdint.h>
#include <string.h>
typedef unsigned long long QWORD_;
typedef unsigned long DWORD_;
#define LARGE_INTEGER union { QWORD_ q; }

#define MAX_PATH_LEN 260
#define BORNE_TAILLE ((uint64_t)2147483648)
#define TAILLE_OFFSET 520
#define POIGNEE_OFFSET 528
#define VUE_OFFSET 536
#define CURSEUR_OFFSET 544
#define REMPL_OFFSET 552
#define TAMPON_OFFSET 568
#define PANNEAU_MD5_OFFSET 0
#define PANNEAU_SHA256_OFFSET 16
#define VERDICT_OK 0
#define VERDICT_ABSENT -2
#define VERDICT_HORS_PERIMETRE -3
#define VERDICT_SESSION_OUVERTE -5
#define VERDICT_SYSTEME -6
#define VERDICT_VERROUILLE -7



#define ROTL32(x, n) (((x) << (n)) | ((x) >> (32 - (n))))
#define ROTR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define F(x, y, z) (((x) & (y)) | (~(x) & (z)))
#define G(x, y, z) (((x) & (y)) | ((x) & (z)) | ((y) & (z)))
#define H(x, y, z) ((x) ^ (y) ^ (z))
#define Ch(x, y, z) (((x) & (y)) ^ (~(x) & (z)))

static const uint32_t T[64] = {
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
};

static const uint8_t S[64] = {
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
};

static const uint32_t K[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

typedef struct { uint32_t etat[4]; uint8_t tampon[64]; uint32_t rempli; uint64_t total; } ctx_md5;
typedef struct { uint32_t etat[8]; uint8_t tampon[64]; uint32_t rempli; uint64_t total; } ctx_sha256;

void md5_transform(uint32_t state[4], const uint8_t data[64]) {
    uint32_t a = state[0], b = state[1], c = state[2], d = state[3];
    uint32_t w[16];

    for (int i = 0; i < 16; ++i) {
        w[i] = (uint32_t)data[i * 4] | (uint32_t)data[i * 4 + 1] << 8 |
               (uint32_t)data[i * 4 + 2] << 16 | (uint32_t)data[i * 4 + 3] << 24;
    }

    for (int i = 0; i < 64; ++i) {
        uint32_t f, g;
        if (i < 16) { f = F(b, c, d); g = i; }
        else if (i < 32) { f = (d & b) | (~d & c); g = (5 * i + 1) % 16; }
        else if (i < 48) { f = H(b, c, d); g = (3 * i + 5) % 16; }
        else { f = c ^ (b | ~d); g = (7 * i) % 16; }

        uint32_t temp = d;
        d = c;
        c = b;
        b = b + ROTL32(a + f + T[i] + w[g], S[i]);
        a = temp;
    }

    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
}

void sha256_transform(uint32_t state[8], const uint8_t data[64]) {
    uint32_t a = state[0], b = state[1], c = state[2], d = state[3];
    uint32_t e = state[4], f = state[5], g = state[6], h = state[7];
    uint32_t w[64];

    for (int i = 0; i < 16; ++i) {
        w[i] = (uint32_t)data[i * 4] << 24 | (uint32_t)data[i * 4 + 1] << 16 |
               (uint32_t)data[i * 4 + 2] << 8 | (uint32_t)data[i * 4 + 3];
    }
    for (int i = 16; i < 64; ++i) {
        uint32_t s0 = ROTR32(w[i - 15], 7) ^ ROTR32(w[i - 15], 18) ^ (w[i - 15] >> 3);
        uint32_t s1 = ROTR32(w[i - 2], 17) ^ ROTR32(w[i - 2], 19) ^ (w[i - 2] >> 10);
        w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }

    for (int i = 0; i < 64; ++i) {
        uint32_t S1 = ROTR32(e, 6) ^ ROTR32(e, 11) ^ ROTR32(e, 25);
        uint32_t ch = Ch(e, f, g);
        uint32_t temp1 = h + S1 + ch + K[i] + w[i];
        uint32_t S0 = ROTR32(a, 2) ^ ROTR32(a, 13) ^ ROTR32(a, 22);
        uint32_t maj = ((a & b) | (a & c)) | (b & c);
        uint32_t temp2 = S0 + maj;

        h = g;
        g = f;
        f = e;
        e = d + temp1;
        d = c;
        c = b;
        b = a;
        a = temp1 + temp2;
    }

    state[0] += a; state[1] += b; state[2] += c; state[3] += d;
    state[4] += e; state[5] += f; state[6] += g; state[7] += h;
}

void md5_absorbe(ctx_md5 *c, const uint8_t *d, uint32_t n) {
    for (uint32_t k = 0; k < n; ++k) {
        c->tampon[c->rempli++] = d[k];
        c->total++;
        if (c->rempli == 64) {
            md5_transform(c->etat, c->tampon);
            c->rempli = 0;
        }
    }
}

void sha256_absorbe(ctx_sha256 *c, const uint8_t *d, uint32_t n) {
    for (uint32_t k = 0; k < n; ++k) {
        c->tampon[c->rempli++] = d[k];
        c->total++;
        if (c->rempli == 64) {
            sha256_transform(c->etat, c->tampon);
            c->rempli = 0;
        }
    }
}

void md5_final(ctx_md5 *c, uint8_t sortie[16]) {
    uint64_t bits = c->total * 8;
    c->tampon[c->rempli++] = 0x80;
    if (c->rempli > 56) {
        for (int i = c->rempli; i < 64; ++i)
            *(volatile uint8_t*)&c->tampon[i] = 0;   /* jamais un
            appel memset — le CRT ne vit pas sous DONT_RESOLVE */
        md5_transform(c->etat, c->tampon);
        c->rempli = 0;
    }
    for (int i = c->rempli; i < 56; ++i)
        *(volatile uint8_t*)&c->tampon[i] = 0;  /* idem — jamais
        un appel memset */
    for (int i = 0; i < 8; ++i) {
        c->tampon[56 + i] = (uint8_t)(bits >> (i * 8));
    }
    md5_transform(c->etat, c->tampon);
    for (int i = 0; i < 4; ++i) {
        uint32_t s = c->etat[i];
        sortie[i * 4 + 0] = (uint8_t)(s);
        sortie[i * 4 + 1] = (uint8_t)(s >> 8);
        sortie[i * 4 + 2] = (uint8_t)(s >> 16);
        sortie[i * 4 + 3] = (uint8_t)(s >> 24);
    }
}

void sha256_final(ctx_sha256 *c, uint8_t sortie[32]) {
    uint64_t bits = c->total * 8;
    c->tampon[c->rempli++] = 0x80;
    if (c->rempli > 56) {
        for (int i = c->rempli; i < 64; ++i)
            *(volatile uint8_t*)&c->tampon[i] = 0;   /* jamais un
            appel memset — le CRT ne vit pas sous DONT_RESOLVE */
        sha256_transform(c->etat, c->tampon);
        c->rempli = 0;
    }
    for (int i = c->rempli; i < 56; ++i)
        *(volatile uint8_t*)&c->tampon[i] = 0;  /* idem — jamais
        un appel memset */
    for (int i = 0; i < 8; ++i) {
        c->tampon[56 + i] = (uint8_t)(bits >> ((7 - i) * 8));
    }
    sha256_transform(c->etat, c->tampon);
    for (int i = 0; i < 8; ++i) {
        uint32_t s = c->etat[i];
        sortie[i * 4 + 0] = (uint8_t)(s >> 24);
        sortie[i * 4 + 1] = (uint8_t)(s >> 16);
        sortie[i * 4 + 2] = (uint8_t)(s >> 8);
        sortie[i * 4 + 3] = (uint8_t)(s);
    }
}


char panneau[48];

int main(void) {
    /* le corpus : les frontières du rembourrage + les tailles des témoins */
    static const int tailles[] = {0, 1, 2, 31, 32, 33, 54, 55, 56, 57, 63,
                                  64, 65, 111, 112, 119, 120, 127, 128,
                                  129, 255, 256, 383, 384, 385, 511, 512,
                                  4096, 4097, 65536, 131072, 196609};
    static unsigned char donnees[196609];
    for (size_t i = 0; i < sizeof donnees; i++)
        donnees[i] = (unsigned char)(i * 131 + (i >> 7) * 17 + i / 251);
    for (size_t t = 0; t < sizeof tailles / sizeof tailles[0]; t++) {
        int n = tailles[t];
        ctx_md5 m5 = {{0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476}, {0}, 0, 0};
        ctx_sha256 s2 = {{0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                          0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19}, {0}, 0, 0};
        /* l'absorption en morceaux IRREGULIERS (7, 1, 4090, 13...) —
           l'incrémentalité éprouvée, pas seulement les blocs entiers */
        size_t reste = (size_t)n, pris = 0;
        static const size_t pas[] = {7, 1, 4090, 13, 64, 3, 5000, 2};
        size_t k = 0;
        while (reste > 0) {
            size_t a = pas[k++ % (sizeof pas / sizeof pas[0])];
            if (a > reste) a = reste;
            md5_absorbe(&m5, donnees + pris, (uint32_t)a);
            sha256_absorbe(&s2, donnees + pris, (uint32_t)a);
            pris += a; reste -= a;
        }
        md5_final(&m5, panneau);
        sha256_final(&s2, panneau + 16);
        printf("%d ", n);
        for (int i = 0; i < 48; i++) printf("%02x", (unsigned char)panneau[i]);
        printf("\n");
    }
    return 0;
}
