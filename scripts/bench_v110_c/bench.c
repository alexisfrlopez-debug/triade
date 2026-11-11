/* bench_v110_c/bench.c — LA RÉFÉRENCE COMPILÉE à contrat équivalent
 * (la commande v0.11.0, chantier 5). C standard, freestanding, CORRECT :
 * chaque fonction est vérifiée contre hashlib/FIPS 197 côté Python AVANT
 * toute mesure (l'instrument se contrôle avant de juger).
 * Périmètre : sha256 (contrat tls13-01..04), md5 (contrat loupe-06),
 * aes128 (contrat tls13-15/16). La référence x25519 est REPORTÉE à
 * l'édition suivante (consigné au rapport).
 * Compilation : gcc -O2 / gcc -Os (clang absent du laboratoire — écart
 * NOMMÉ au rapport).
 */
#include <stdint.h>
#include <string.h>

#define ROR32(x,n) (((x)>>(n))|((x)<<(32-(n))))

/* freestanding : les propres memset/memcpy (gcc en émet malgré tout) */
void *memset(void *d, int c, size_t n) {
    uint8_t *p = (uint8_t *)d;
    for (size_t i = 0; i < n; i++) p[i] = (uint8_t)c;
    return d;
}
void *memcpy(void *d, const void *s, size_t n) {
    uint8_t *p = (uint8_t *)d; const uint8_t *q = (const uint8_t *)s;
    for (size_t i = 0; i < n; i++) p[i] = q[i];
    return d;
}

/* ================= SHA-256 (contrat tls13-01..04) ================= */
static const uint32_t K256[64] = {
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,
    0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,
    0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,
    0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
    0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,
    0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,
    0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,
    0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
    0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};

static void sha256_bloc(uint32_t h[8], const uint8_t b[64]) {
    uint32_t w[64];
    for (int i = 0; i < 16; i++)
        w[i] = ((uint32_t)b[4*i]<<24)|((uint32_t)b[4*i+1]<<16)
              |((uint32_t)b[4*i+2]<<8)|b[4*i+3];
    for (int i = 16; i < 64; i++) {
        uint32_t s0 = ROR32(w[i-15],7)^ROR32(w[i-15],18)^(w[i-15]>>3);
        uint32_t s1 = ROR32(w[i-2],17)^ROR32(w[i-2],19)^(w[i-2]>>10);
        w[i] = w[i-16]+s0+w[i-7]+s1;
    }
    uint32_t a=h[0],b2=h[1],c=h[2],d=h[3],e=h[4],f=h[5],g=h[6],h2=h[7];
    for (int i = 0; i < 64; i++) {
        uint32_t S1 = ROR32(e,6)^ROR32(e,11)^ROR32(e,25);
        uint32_t ch = (e&f)^((~e)&g);
        uint32_t t1 = h2+S1+ch+K256[i]+w[i];
        uint32_t S0 = ROR32(a,2)^ROR32(a,13)^ROR32(a,22);
        uint32_t mj = (a&b2)^(a&c)^(b2&c);
        h2=g; g=f; f=e; e=d+t1; d=c; c=b2; b2=a; a=t1+(S0+mj);
    }
    h[0]+=a;h[1]+=b2;h[2]+=c;h[3]+=d;h[4]+=e;h[5]+=f;h[6]+=g;h[7]+=h2;
}

void bench_sha256(const uint8_t *in, uint64_t len, uint8_t out[32]) {
    uint32_t h[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                     0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    uint8_t block[64];
    uint64_t off = 0;
    while (len - off >= 64) { sha256_bloc(h, in+off); off += 64; }
    uint64_t n = len - off;
    memset(block, 0, 64);
    memcpy(block, in+off, (size_t)n);
    block[n] = 0x80;
    if (n >= 56) { sha256_bloc(h, block); memset(block, 0, 64); }
    uint64_t bits = len * 8;
    for (int i = 0; i < 8; i++) block[63-i] = (uint8_t)(bits >> (8*i));
    sha256_bloc(h, block);
    for (int i = 0; i < 8; i++) {
        out[4*i]=(uint8_t)(h[i]>>24); out[4*i+1]=(uint8_t)(h[i]>>16);
        out[4*i+2]=(uint8_t)(h[i]>>8); out[4*i+3]=(uint8_t)h[i];
    }
}

/* ================= MD5 (contrat loupe-06) ================= */
static const uint32_t KM5[64] = {
    0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,
    0xa8304613,0xfd469501,0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,
    0x6b901122,0xfd987193,0xa679438e,0x49b40821,0xf61e2562,0xc040b340,
    0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
    0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,
    0x676f02d9,0x8d2a4c8a,0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,
    0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,0x289b7ec6,0xeaa127fa,
    0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,
    0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,
    0xffeff47d,0x85845dd1,0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,
    0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391};
static const int RM5[64] = {7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
    5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
    4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
    6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21};

static void md5_bloc(uint32_t h[4], const uint8_t b[64]) {
    uint32_t w[16];
    for (int i = 0; i < 16; i++)
        w[i] = ((uint32_t)b[4*i])|((uint32_t)b[4*i+1]<<8)
              |((uint32_t)b[4*i+2]<<16)|((uint32_t)b[4*i+3]<<24);
    uint32_t a=h[0],b2=h[1],c=h[2],d=h[3];
    for (int i = 0; i < 64; i++) {
        uint32_t f; int g;
        if (i<16)      { f=(b2&c)|((~b2)&d); g=i; }
        else if (i<32) { f=(d&b2)|((~d)&c);  g=(5*i+1)&15; }
        else if (i<48) { f=b2^c^d;           g=(3*i+5)&15; }
        else           { f=c^(b2|(~d));      g=(7*i)&15; }
        uint32_t tmp = d; d = c; c = b2;
        b2 = b2 + ROR32(a + f + KM5[i] + w[g], (uint32_t)(32 - RM5[i]));
        a = tmp;
    }
    h[0]+=a;h[1]+=b2;h[2]+=c;h[3]+=d;
}

void bench_md5(const uint8_t *in, uint64_t len, uint8_t out[16]) {
    uint32_t h[4] = {0x67452301,0xefcdab89,0x98badcfe,0x10325476};
    uint8_t block[64];
    uint64_t off = 0;
    while (len - off >= 64) { md5_bloc(h, in+off); off += 64; }
    uint64_t n = len - off;
    memset(block, 0, 64);
    memcpy(block, in+off, (size_t)n);
    block[n] = 0x80;
    if (n >= 56) { md5_bloc(h, block); memset(block, 0, 64); }
    uint64_t bits = len * 8;
    for (int i = 0; i < 8; i++) block[63-i] = (uint8_t)(bits >> (8*i));
    md5_bloc(h, block);
    for (int i = 0; i < 4; i++) {
        out[4*i]=(uint8_t)h[i]; out[4*i+1]=(uint8_t)(h[i]>>8);
        out[4*i+2]=(uint8_t)(h[i]>>16); out[4*i+3]=(uint8_t)(h[i]>>24);
    }
}

/* ================= AES-128 (contrat tls13-15/16) ================= */
static const uint8_t SBOX[256] = {
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16};
static const uint8_t RCON[11] = {0,1,2,4,8,0x10,0x20,0x40,0x80,0x1b,0x36};

static uint8_t xt(uint8_t x) { return (uint8_t)((x<<1)^((x&0x80)?0x1b:0)); }
static uint8_t gmul(uint8_t x, uint8_t y) {
    uint8_t r = 0;
    while (y) { if (y&1) r ^= x; x = xt(x); y >>= 1; }
    return r;
}

void bench_aes128(const uint8_t cle[16], const uint8_t in[16], uint8_t out[16]) {
    uint8_t rk[176];
    memcpy(rk, cle, 16);
    for (int r = 1; r <= 10; r++) {
        uint8_t t[4];
        t[0] = (uint8_t)(SBOX[rk[16*(r-1)+13]] ^ RCON[r]);
        t[1] = SBOX[rk[16*(r-1)+14]];
        t[2] = SBOX[rk[16*(r-1)+15]];
        t[3] = SBOX[rk[16*(r-1)+12]];
        /* FIPS 197 § 5.2 : SEUL le premier mot porte SubWord(RotWord)^Rcon ;
           les mots 1..3 sont w[i-4] ^ w[i-1] — jamais SubWord */
        for (int j = 0; j < 4; j++)
            rk[16*r+j] = (uint8_t)(rk[16*(r-1)+j] ^ t[j]);
        for (int j = 4; j < 16; j++)
            rk[16*r+j] = (uint8_t)(rk[16*(r-1)+j] ^ rk[16*r+j-4]);
    }
    uint8_t s[16];
    memcpy(s, in, 16);
    for (int i = 0; i < 16; i++) s[i] ^= rk[i];
    for (int r = 1; r <= 10; r++) {
        uint8_t t[16];
        for (int c = 0; c < 4; c++)
            for (int l = 0; l < 4; l++)
                t[4*c+l] = SBOX[s[4*((c+l)&3)+l]];
        memcpy(s, t, 16);
        if (r < 10) {
            for (int c = 0; c < 4; c++) {
                uint8_t a0=s[4*c],a1=s[4*c+1],a2=s[4*c+2],a3=s[4*c+3];
                s[4*c  ]=(uint8_t)(gmul(a0,2)^a1^a2^gmul(a3,3));
                s[4*c+1]=(uint8_t)(gmul(a0,3)^gmul(a1,2)^a2^a3);
                s[4*c+2]=(uint8_t)(a0^gmul(a1,3)^gmul(a2,2)^a3);
                s[4*c+3]=(uint8_t)(a0^a1^gmul(a2,3)^gmul(a3,2));
            }
        }
        for (int i = 0; i < 16; i++) s[i] ^= rk[16*r+i];
    }
    memcpy(out, s, 16);
}
