#include "shim05.h"

static const uint32_t K[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

static const uint32_t H0[8] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

long long loupe_05(void *cadre, long long decalage, long long longueur, void *sortie) {
    if (!sortie) return -5;

    HANDLE *p_handle = (HANDLE *)((char *)cadre + 528);
    HANDLE h = *p_handle;
    if (h == INVALID_HANDLE_VALUE) return -4;

    uint64_t *p_taille = (uint64_t *)((char *)cadre + 520);
    uint64_t taille_fichier = *p_taille;

    if (decalage < 0 || longueur < 0 || decalage + longueur > taille_fichier) {
        return -3;
    }

    typedef struct {
        uint64_t total;
        uint32_t etat[8];
        uint8_t buf[64];
    } sha256_ctx;

    sha256_ctx ctx;
    ctx.total = 0;

    for (int i = 0; i < 8; ++i) {
        ctx.etat[i] = H0[i];
    }

    for (int i = 0; i < 64; ++i) {
        ctx.buf[i] = 0;
    }

    LARGE_INTEGER li_decalage;
    li_decalage.QuadPart = decalage;

    BYTE tampon[65536];
    long long restant = longueur;
    while (restant > 0) {
        long long a_lire = restant;
        if (a_lire > sizeof(tampon)) {
            a_lire = sizeof(tampon);
        }

        SetFilePointerEx(h, li_decalage, NULL, FILE_BEGIN);

        DWORD lus = 0;
        if (!ReadFile(h, tampon, (DWORD)a_lire, &lus, NULL)) {
            return -1;
        }

        if (lus == 0) {
            break;
        }

        for (DWORD i = 0; i < lus; ++i) {
            ctx.buf[ctx.total & 0x3F] = tampon[i];
            ctx.total++;
            if ((ctx.total & 0x3F) == 0) {
                uint32_t W[64];
                for (int t = 0; t < 16; ++t) {
                    W[t] = (ctx.buf[t * 4 + 0] << 24) | (ctx.buf[t * 4 + 1] << 16) | (ctx.buf[t * 4 + 2] << 8) | (ctx.buf[t * 4 + 3]);
                }
                for (int t = 16; t < 64; ++t) {
                    uint32_t s0 = (W[t-15] >> 7) | (W[t-15] << 25);
                    s0 ^= (W[t-15] >> 18) | (W[t-15] << 14);
                    s0 ^= (W[t-15] >> 3);
                    uint32_t s1 = (W[t-2] >> 17) | (W[t-2] << 15);
                    s1 ^= (W[t-2] >> 19) | (W[t-2] << 13);
                    s1 ^= (W[t-2] >> 10);
                    W[t] = W[t-16] + s0 + W[t-7] + s1;
                }

                uint32_t a = ctx.etat[0];
                uint32_t b = ctx.etat[1];
                uint32_t c = ctx.etat[2];
                uint32_t d = ctx.etat[3];
                uint32_t e = ctx.etat[4];
                uint32_t f = ctx.etat[5];
                uint32_t g = ctx.etat[6];
                uint32_t h = ctx.etat[7];

                for (int t = 0; t < 64; ++t) {
                    uint32_t S1 = (e >> 6) | (e << 26);
                    S1 ^= (e >> 11) | (e << 21);
                    S1 ^= (e >> 25) | (e << 7);
                    uint32_t ch = (e & f) ^ ((~e) & g);
                    uint32_t temp1 = h + S1 + ch + K[t] + W[t];
                    uint32_t S0 = (a >> 2) | (a << 30);
                    S0 ^= (a >> 13) | (a << 19);
                    S0 ^= (a >> 22) | (a << 10);
                    uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
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

                ctx.etat[0] += a;
                ctx.etat[1] += b;
                ctx.etat[2] += c;
                ctx.etat[3] += d;
                ctx.etat[4] += e;
                ctx.etat[5] += f;
                ctx.etat[6] += g;
                ctx.etat[7] += h;
            }
        }

        li_decalage.QuadPart += lus;
        restant -= lus;
    }

    uint64_t l_bit = ctx.total * 8;

    ctx.buf[ctx.total & 0x3F] = 0x80;
    ctx.total++;

    if ((ctx.total & 0x3F) > 56) {
        for (int i = (ctx.total & 0x3F); i < 64; ++i) {
            ctx.buf[i] = 0;
        }
        uint32_t W[64];
        for (int t = 0; t < 16; ++t) {
            W[t] = (ctx.buf[t * 4 + 0] << 24) | (ctx.buf[t * 4 + 1] << 16) | (ctx.buf[t * 4 + 2] << 8) | (ctx.buf[t * 4 + 3]);
        }
        for (int t = 16; t < 64; ++t) {
            uint32_t s0 = (W[t-15] >> 7) | (W[t-15] << 25);
            s0 ^= (W[t-15] >> 18) | (W[t-15] << 14);
            s0 ^= (W[t-15] >> 3);
            uint32_t s1 = (W[t-2] >> 17) | (W[t-2] << 15);
            s1 ^= (W[t-2] >> 19) | (W[t-2] << 13);
            s1 ^= (W[t-2] >> 10);
            W[t] = W[t-16] + s0 + W[t-7] + s1;
        }

        uint32_t a = ctx.etat[0];
        uint32_t b = ctx.etat[1];
        uint32_t c = ctx.etat[2];
        uint32_t d = ctx.etat[3];
        uint32_t e = ctx.etat[4];
        uint32_t f = ctx.etat[5];
        uint32_t g = ctx.etat[6];
        uint32_t h = ctx.etat[7];

        for (int t = 0; t < 64; ++t) {
            uint32_t S1 = (e >> 6) | (e << 26);
            S1 ^= (e >> 11) | (e << 21);
            S1 ^= (e >> 25) | (e << 7);
            uint32_t ch = (e & f) ^ ((~e) & g);
            uint32_t temp1 = h + S1 + ch + K[t] + W[t];
            uint32_t S0 = (a >> 2) | (a << 30);
            S0 ^= (a >> 13) | (a << 19);
            S0 ^= (a >> 22) | (a << 10);
            uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
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

        ctx.etat[0] += a;
        ctx.etat[1] += b;
        ctx.etat[2] += c;
        ctx.etat[3] += d;
        ctx.etat[4] += e;
        ctx.etat[5] += f;
        ctx.etat[6] += g;
        ctx.etat[7] += h;

        for (int i = 0; i < 64; ++i) {
            ctx.buf[i] = 0;
        }
        ctx.total = 0;
        ctx.total += 64;
    } else {
        for (int i = (ctx.total & 0x3F); i < 56; ++i) {
            ctx.buf[i] = 0;
        }
        ctx.total += (56 - (ctx.total & 0x3F));
    }

    ctx.buf[56] = (l_bit >> 56) & 0xFF;
    ctx.buf[57] = (l_bit >> 48) & 0xFF;
    ctx.buf[58] = (l_bit >> 40) & 0xFF;
    ctx.buf[59] = (l_bit >> 32) & 0xFF;
    ctx.buf[60] = (l_bit >> 24) & 0xFF;
    ctx.buf[61] = (l_bit >> 16) & 0xFF;
    ctx.buf[62] = (l_bit >> 8) & 0xFF;
    ctx.buf[63] = l_bit & 0xFF;

    uint32_t W[64];
    for (int t = 0; t < 16; ++t) {
        W[t] = (ctx.buf[t * 4 + 0] << 24) | (ctx.buf[t * 4 + 1] << 16) | (ctx.buf[t * 4 + 2] << 8) | (ctx.buf[t * 4 + 3]);
    }
    for (int t = 16; t < 64; ++t) {
        uint32_t s0 = (W[t-15] >> 7) | (W[t-15] << 25);
        s0 ^= (W[t-15] >> 18) | (W[t-15] << 14);
        s0 ^= (W[t-15] >> 3);
        uint32_t s1 = (W[t-2] >> 17) | (W[t-2] << 15);
        s1 ^= (W[t-2] >> 19) | (W[t-2] << 13);
        s1 ^= (W[t-2] >> 10);
        W[t] = W[t-16] + s0 + W[t-7] + s1;
    }

    uint32_t a = ctx.etat[0];
    uint32_t b = ctx.etat[1];
    uint32_t c = ctx.etat[2];
    uint32_t d = ctx.etat[3];
    uint32_t e = ctx.etat[4];
    uint32_t f = ctx.etat[5];
    uint32_t g = ctx.etat[6];
    uint32_t h = ctx.etat[7];

    for (int t = 0; t < 64; ++t) {
        uint32_t S1 = (e >> 6) | (e << 26);
        S1 ^= (e >> 11) | (e << 21);
        S1 ^= (e >> 25) | (e << 7);
        uint32_t ch = (e & f) ^ ((~e) & g);
        uint32_t temp1 = h + S1 + ch + K[t] + W[t];
        uint32_t S0 = (a >> 2) | (a << 30);
        S0 ^= (a >> 13) | (a << 19);
        S0 ^= (a >> 22) | (a << 10);
        uint32_t maj = (a & b) | (a & c) | (b & c);
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

    ctx.etat[0] += a;
    ctx.etat[1] += b;
    ctx.etat[2] += c;
    ctx.etat[3] += d;
    ctx.etat[4] += e;
    ctx.etat[5] += f;
    ctx.etat[6] += g;
    ctx.etat[7] += h;

    uint8_t *p_sortie = (uint8_t *)sortie;
    p_sortie[0] = (ctx.etat[0] >> 24) & 0xFF;
    p_sortie[1] = (ctx.etat[0] >> 16) & 0xFF;
    p_sortie[2] = (ctx.etat[0] >> 8) & 0xFF;
    p_sortie[3] = ctx.etat[0] & 0xFF;
    p_sortie[4] = (ctx.etat[1] >> 24) & 0xFF;
    p_sortie[5] = (ctx.etat[1] >> 16) & 0xFF;
    p_sortie[6] = (ctx.etat[1] >> 8) & 0xFF;
    p_sortie[7] = ctx.etat[1] & 0xFF;
    p_sortie[8] = (ctx.etat[2] >> 24) & 0xFF;
    p_sortie[9] = (ctx.etat[2] >> 16) & 0xFF;
    p_sortie[10] = (ctx.etat[2] >> 8) & 0xFF;
    p_sortie[11] = ctx.etat[2] & 0xFF;
    p_sortie[12] = (ctx.etat[3] >> 24) & 0xFF;
    p_sortie[13] = (ctx.etat[3] >> 16) & 0xFF;
    p_sortie[14] = (ctx.etat[3] >> 8) & 0xFF;
    p_sortie[15] = ctx.etat[3] & 0xFF;
    p_sortie[16] = (ctx.etat[4] >> 24) & 0xFF;
    p_sortie[17] = (ctx.etat[4] >> 16) & 0xFF;
    p_sortie[18] = (ctx.etat[4] >> 8) & 0xFF;
    p_sortie[19] = ctx.etat[4] & 0xFF;
    p_sortie[20