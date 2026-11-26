/* couloir_sched.c — LE PILOTE DU SCHEDULE DE NOTATION (W28VAES, la pièce ii).
 * Le couloir écrit en ASSEMBLAGE SUR le calendrier de la notation gelée
 * couloir-vaes.asm (7911d03f… INTACTE) : l'ÉTAGE 3 — l'entrelacement
 * instruction-par-instruction des chaînes VAES avec les VPCLMULQDQ du pli
 * précédent, les chaînes CTR pipelinées DEUX À DEUX (l'ILP que le compilateur
 * ne préserve pas — l'objet du RÉSULTAT DISTINCT pré-enregistré).
 * L'algorithme est À L'IDENTIQUE celui du portage C v3 (le même domaine
 * réfléchi, les mêmes frontières, la même réduction) : SEUL LE CALENDRIER
 * DIFFÈRE — l'écart mesuré est l'écart de schedule, isolé.
 * Le contexte (expansion, puissances H, E_K(J0)) est posé par le pilote C
 * (le moteur d'expansion de la v3) — la frontière d'appel du message seule.
 * Compilation : gcc -O2 -mavx2 -mvaes -mvpclmulqdq -maes couloir_sched.c
 *               couloir_sched.S -lcrypto
 */
#include <immintrin.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>

/* le contexte posé par le pilote — l'ordre des champs EST le contrat de l'assemblage */
typedef struct {
    __m256i rk[15];    /* 0x000 : les clés de tour broadcastées          */
    __m128i Hr;        /* 0x1E0 : H réfléchi                            */
    __m128i Hp[8];     /* 0x1F0 : H¹..H⁸ réfléchies (H⁸ à +0x260)      */
    __m128i ej0;       /* 0x270 : E_K(J0)                               */
    __m256i vb[4];     /* 0x280 : les [H^{8-2p} | H^{7-2p}] par paire   */
    __m256i ligne0;    /* 0x300 : [2|3] l'IV aux octets 4..15           */
    uint8_t iv[12];    /* 0x320 : le préfixe des compteurs              */
} __attribute__((aligned(32))) ctx_sched;

extern void couloir_sched_msg(const ctx_sched *ctx, const uint8_t *clair,
                              uint8_t *chiffre, const uint8_t *aad,
                              uint64_t alen, uint8_t tag[16]);

/* ---- l'expansion (le moteur de la v3 reconduit, la frontière amortie) -------- */
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
static const uint8_t RCON[11] = {0, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36};
static inline uint32_t sub_word(uint32_t w) {
    return ((uint32_t)SBOX[(w >> 24) & 0xff] << 24) | ((uint32_t)SBOX[(w >> 16) & 0xff] << 16)
         | ((uint32_t)SBOX[(w >> 8) & 0xff] << 8) | (uint32_t)SBOX[w & 0xff];
}
typedef struct { __m256i rk[15]; } cles_tour;
static void expansion_aes256(const uint8_t cle[32], cles_tour *ct) {
    uint32_t w[60];
    for (int i = 0; i < 8; i++)
        w[i] = ((uint32_t)cle[4*i] << 24) | ((uint32_t)cle[4*i+1] << 16) | ((uint32_t)cle[4*i+2] << 8) | cle[4*i+3];
    for (int i = 8; i < 60; i++) {
        uint32_t t = w[i-1];
        if (i % 8 == 0) t = sub_word((t << 8) | (t >> 24)) ^ ((uint32_t)RCON[i/8] << 24);
        else if (i % 8 == 4) t = sub_word(t);
        w[i] = w[i-8] ^ t;
    }
    for (int r = 0; r < 15; r++) {
        uint8_t rk_o[16];
        for (int j = 0; j < 4; j++) {
            rk_o[4*j] = (uint8_t)(w[4*r+j] >> 24); rk_o[4*j+1] = (uint8_t)(w[4*r+j] >> 16);
            rk_o[4*j+2] = (uint8_t)(w[4*r+j] >> 8); rk_o[4*j+3] = (uint8_t)w[4*r+j];
        }
        ct->rk[r] = _mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i *)rk_o));
    }
}
static inline void clmul_karatsuba(__m128i a, __m128i b, __m128i *lo, __m128i *hi) {
    __m128i a01 = _mm_xor_si128(_mm_unpacklo_epi64(a, a), _mm_unpackhi_epi64(a, a));
    __m128i b01 = _mm_xor_si128(_mm_unpacklo_epi64(b, b), _mm_unpackhi_epi64(b, b));
    __m128i l = _mm_clmulepi64_si128(a, b, 0x00);
    __m128i h = _mm_clmulepi64_si128(a, b, 0x11);
    __m128i m = _mm_clmulepi64_si128(a01, b01, 0x00);
    m = _mm_xor_si128(m, _mm_xor_si128(l, h));
    *lo = _mm_xor_si128(l, _mm_slli_si128(m, 8));
    *hi = _mm_xor_si128(h, _mm_srli_si128(m, 8));
}
static inline __m128i shl128(__m128i v, int n) {
    __m128i base = _mm_slli_epi64(v, n);
    __m128i carry = _mm_srli_epi64(v, 64 - n);
    return _mm_or_si128(base, _mm_slli_si128(carry, 8));
}
static inline __m128i reduit_gcm(__m128i lo, __m128i hi) {
    uint64_t x3 = (uint64_t)_mm_extract_epi64(hi, 1);
    uint64_t x2 = (uint64_t)_mm_extract_epi64(hi, 0);
    uint64_t d = x2 ^ (x3 >> 63) ^ (x3 >> 62) ^ (x3 >> 57);
    __m128i xd = _mm_set_epi64x((long long)x3, (long long)d);
    __m128i h = _mm_xor_si128(_mm_xor_si128(xd, shl128(xd, 1)),
                              _mm_xor_si128(shl128(xd, 2), shl128(xd, 7)));
    return _mm_xor_si128(lo, h);
}
static __m128i gfmul(__m128i a, __m128i b) {
    __m128i lo, hi;
    clmul_karatsuba(a, b, &lo, &hi);
    return reduit_gcm(lo, hi);
}
static inline __m128i rev128(__m128i v) {
    const __m128i T = _mm_setr_epi8(0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15);
    const __m128i M = _mm_set1_epi8(0x0F);
    const __m128i MF0 = _mm_set1_epi8((char)0xF0);
    __m128i bas = _mm_shuffle_epi8(T, _mm_and_si128(v, M));
    __m128i haut = _mm_shuffle_epi8(T, _mm_and_si128(_mm_srli_epi16(v, 4), M));
    return _mm_or_si128(_mm_and_si128(_mm_slli_epi16(bas, 4), MF0), haut);
}
static inline __m128i un_bloc_aes(const cles_tour *ct, __m128i x) {
    x = _mm_xor_si128(x, _mm256_castsi256_si128(ct->rk[0]));
    for (int r = 1; r <= 13; r++) x = _mm_aesenc_si128(x, _mm256_castsi256_si128(ct->rk[r]));
    return _mm_aesenclast_si128(x, _mm256_castsi256_si128(ct->rk[14]));
}
#define TAILLE 4096

static void contexte_poser(ctx_sched *c, const uint8_t cle[32], const uint8_t iv[12]) {
    expansion_aes256(cle, (cles_tour *)c->rk);
    memcpy(c->iv, iv, 12);
    __m128i zero = _mm_setzero_si128();
    c->Hr = rev128(un_bloc_aes((const cles_tour *)c->rk, zero));
    c->Hp[0] = c->Hr;
    for (int i = 1; i < 8; i++) c->Hp[i] = gfmul(c->Hp[i-1], c->Hr);
    uint8_t j0[16];
    memcpy(j0, iv, 12);
    j0[12] = 0; j0[13] = 0; j0[14] = 0; j0[15] = 1;
    c->ej0 = un_bloc_aes((const cles_tour *)c->rk, _mm_loadu_si128((const __m128i *)j0));
    c->vb[0] = _mm256_insertf128_si256(_mm256_castsi128_si256(c->Hp[7]), c->Hp[6], 1);
    c->vb[1] = _mm256_insertf128_si256(_mm256_castsi128_si256(c->Hp[5]), c->Hp[4], 1);
    c->vb[2] = _mm256_insertf128_si256(_mm256_castsi128_si256(c->Hp[3]), c->Hp[2], 1);
    c->vb[3] = _mm256_insertf128_si256(_mm256_castsi128_si256(c->Hp[1]), c->Hp[0], 1);
    /* la ligne des compteurs : lane = [ctr_le32 || iv12], posée ici (le pilote) */
    {
        __m256i lane = _mm256_setr_epi32((int)2, 0, 0, 0, (int)3, 0, 0, 0);
        __m256i ivv = _mm256_setr_epi8(0,0,0,0, iv[0],iv[1],iv[2],iv[3],iv[4],iv[5],iv[6],iv[7],
                                        iv[8],iv[9],iv[10],iv[11], 0,0,0,0, iv[0],iv[1],iv[2],iv[3],
                                        iv[4],iv[5],iv[6],iv[7], iv[8],iv[9],iv[10],iv[11]);
        const __m256i MASQUE = _mm256_setr_epi16(0xFFFF, 0xFFFF, 0, 0, 0, 0, 0, 0,
                                                 0xFFFF, 0xFFFF, 0, 0, 0, 0, 0, 0);
        c->ligne0 = _mm256_or_si256(_mm256_and_si256(MASQUE, lane),
                                    _mm256_andnot_si256(MASQUE, ivv));
    }
}

/* ---- EVP (les deux conventions) + la porte + la mesure (la v3 reconduite) --- */
static void evp_chiffre(const uint8_t cle[32], const uint8_t iv[12], const uint8_t *clair,
                        size_t n, const uint8_t *aad, size_t alen, uint8_t *chiffre, uint8_t tag[16]) {
    EVP_CIPHER_CTX *c = EVP_CIPHER_CTX_new();
    int len = 0;
    EVP_EncryptInit_ex(c, EVP_aes_256_gcm(), NULL, NULL, NULL);
    EVP_CIPHER_CTX_ctrl(c, EVP_CTRL_GCM_SET_IVLEN, 12, NULL);
    EVP_EncryptInit_ex(c, NULL, NULL, cle, iv);
    if (alen) EVP_EncryptUpdate(c, NULL, &len, aad, (int)alen);
    EVP_EncryptUpdate(c, chiffre, &len, clair, (int)n);
    EVP_EncryptFinal_ex(c, chiffre + len, &len);
    EVP_CIPHER_CTX_ctrl(c, EVP_CTRL_GCM_GET_TAG, 16, tag);
    EVP_CIPHER_CTX_free(c);
}
typedef struct { EVP_CIPHER_CTX *c; } evp_session;
static int evp_session_init(evp_session *s, const uint8_t cle[32], const uint8_t iv[12]) {
    s->c = EVP_CIPHER_CTX_new();
    if (EVP_EncryptInit_ex(s->c, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1) return 0;
    if (EVP_CIPHER_CTX_ctrl(s->c, EVP_CTRL_GCM_SET_IVLEN, 12, NULL) != 1) return 0;
    return EVP_EncryptInit_ex(s->c, NULL, NULL, cle, iv) == 1;
}
static int evp_session_msg(evp_session *s, const uint8_t iv[12], const uint8_t *clair,
                           size_t n, const uint8_t *aad, size_t alen, uint8_t *chiffre, uint8_t tag[16]) {
    int len = 0, len2 = 0;
    if (EVP_EncryptInit_ex(s->c, NULL, NULL, NULL, iv) != 1) return 0;
    if (alen) EVP_EncryptUpdate(s->c, NULL, &len, aad, (int)alen);
    EVP_EncryptUpdate(s->c, chiffre, &len2, clair, (int)n);
    EVP_EncryptFinal_ex(s->c, chiffre + len2, &len2);
    return EVP_CIPHER_CTX_ctrl(s->c, EVP_CTRL_GCM_GET_TAG, 16, tag) == 1;
}
static void evp_session_close(evp_session *s) { EVP_CIPHER_CTX_free(s->c); }
static int hex_vers(const char *h, uint8_t *o, size_t max) {
    size_t n = strlen(h) / 2;
    if (n > max) return -1;
    for (size_t i = 0; i < n; i++) sscanf(h + 2*i, "%2hhx", o + i);
    return (int)n;
}

static int pilote_main(int argc, char **argv) {
    __builtin_cpu_init();
    if (!(__builtin_cpu_supports("vaes") && __builtin_cpu_supports("vpclmulqdq")
          && __builtin_cpu_supports("avx2"))) {
        printf("SILICIUM-ABSENT : le couloir refuse\n"); return 4;
    }
    if (argc < 2) { fprintf(stderr, "usage : couloir_sched --kat|--negatif|--roundtrip|--mesure\n"); return 2; }

    if (!strcmp(argv[1], "--negatif-mutant")) {
        /* la mutation nommée : rk13 ⊕ 0x5a — posée APRÈS le contexte, la même
         * que la variante C (la première clé de tour décalée) */
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 7 + 1;
        for (int i = 0; i < 12; i++) IV[i] = i * 3 + 5;
        ctx_sched c; contexte_poser(&c, K, IV);
        __m256i r13 = c.rk[13];
        r13 = _mm256_xor_si256(r13, _mm256_set1_epi8(0x5a));
        c.rk[13] = r13;
        uint8_t clair[TAILLE], ch[TAILLE], tag[16], tag_evp[16], ch_evp[TAILLE];
        memset(clair, 0, sizeof clair);
        couloir_sched_msg(&c, clair, ch, NULL, 0, tag);
        evp_chiffre(K, IV, clair, TAILLE, NULL, 0, ch_evp, tag_evp);
        int ok = !memcmp(tag, tag_evp, 16) && !memcmp(ch, ch_evp, TAILLE);
        printf("variante mutée (rk13 ⊕ 0x5a) contre EVP : %s — %s\n",
               ok ? "passe (ROUGE)" : "diverge",
               ok ? "REFUS ATTENDU NON VÉCU" : "LE REFUS NOMMÉ (la mutation refuse au premier vecteur)");
        return ok ? 3 : 0;
    }

    if (!strcmp(argv[1], "--kat") || !strcmp(argv[1], "--negatif")) {
        FILE *f = fopen("vecteurs-dores-nist.depouille", "r");
        if (!f) { fprintf(stderr, "vecteurs dorés introuvables\n"); return 2; }
        char ligne[512];
        char key[65] = "", iv[25] = "", pt[8192] = "", aad[8192] = "", ct_att[8192] = "", tag_att[33] = "";
        int nvec = 0, verts = 0, premier = 1;
        while (fgets(ligne, sizeof ligne, f)) {
            if (!strncmp(ligne, "Key = ", 6)) { strcpy(key, ligne + 6); key[strcspn(key, "\n")] = 0; }
            else if (!strncmp(ligne, "IV = ", 5)) { strcpy(iv, ligne + 5); iv[strcspn(iv, "\n")] = 0; }
            else if (!strncmp(ligne, "PT = ", 5)) { strcpy(pt, ligne + 5); pt[strcspn(pt, "\n")] = 0; }
            else if (!strncmp(ligne, "AAD = ", 6)) { strcpy(aad, ligne + 6); aad[strcspn(aad, "\n")] = 0; }
            else if (!strncmp(ligne, "CT = ", 5)) { strcpy(ct_att, ligne + 5); ct_att[strcspn(ct_att, "\n")] = 0; }
            else if (!strncmp(ligne, "Tag = ", 6)) {
                strcpy(tag_att, ligne + 6); tag_att[strcspn(tag_att, "\n")] = 0;
                nvec++;
                uint8_t K[32], IV[12];
                hex_vers(key, K, 32); hex_vers(iv, IV, 12);
                uint8_t *clair = calloc(TAILLE, 1), *chiffre = calloc(TAILLE, 1);
                hex_vers(pt, clair, TAILLE);
                uint8_t aad_b[1024]; size_t aadlen = hex_vers(aad, aad_b, 1024);
                if (strlen(aad) == 0) aadlen = 0;
                ctx_sched c; contexte_poser(&c, K, IV);
                uint8_t tag[16];
                couloir_sched_msg(&c, clair, chiffre, aad_b, aadlen, tag);
                uint8_t *ct_evp = calloc(TAILLE, 1), tag_evp[16];
                evp_chiffre(K, IV, clair, TAILLE, aad_b, aadlen, ct_evp, tag_evp);
                int ok = !memcmp(tag, tag_evp, 16) && !memcmp(chiffre, ct_evp, TAILLE);
                verts += ok ? 1 : 0;
                if (premier) {
                    printf("premier vecteur : couloir-sched==EVP %s\n", ok ? "VERT" : "ROUGE");
                    premier = 0;
                    if (!ok) {
                        printf("KAT ROUGE AU PREMIER VECTEUR — %s\n",
                               strcmp(argv[1], "--negatif") == 0
                               ? "COMPORTEMENT ATTENDU DE LA VARIANTE MUTÉE (le refus nommé)"
                               : "REFUS : PARITÉ-VECTEURS-DORÉS");
                        free(clair); free(chiffre); free(ct_evp); fclose(f);
                        return strcmp(argv[1], "--negatif") == 0 ? 0 : 3;
                    }
                }
                free(clair); free(chiffre); free(ct_evp);
                key[0] = iv[0] = pt[0] = aad[0] = ct_att[0] = tag_att[0] = 0;
            }
        }
        fclose(f);
        printf("%s : %d/%d vecteurs couloir-sched==EVP octet pour octet (4 Kio paddés, tag compris)\n",
               argv[1], verts, nvec);
        return (verts == nvec) ? 0 : 3;
    }

    if (!strcmp(argv[1], "--dbg1")) {
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 7 + 1;
        for (int i = 0; i < 12; i++) IV[i] = i * 3 + 5;
        uint8_t clair[TAILLE], ch[TAILLE], tag[16];
        memset(clair, 0, TAILLE);
        ctx_sched c; contexte_poser(&c, K, IV);
        couloir_sched_msg(&c, clair, ch, NULL, 0, tag);
        printf("tag: "); for (int i = 0; i < 16; i++) printf("%02x", tag[i]); printf("\n");
        printf("ct16: "); for (int i = 0; i < 16; i++) printf("%02x", ch[i]); printf("\n");
        printf("ct2048: "); for (int i = 2048; i < 2064; i++) printf("%02x", ch[i]); printf("\n");
        { FILE *fo = fopen("/tmp/ct_sched.bin", "wb"); if (fo) { fwrite(ch, 1, TAILLE, fo); fclose(fo); } }
        return 0;
    }

    if (!strcmp(argv[1], "--roundtrip")) {
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 7 + 1;
        for (int i = 0; i < 12; i++) IV[i] = i * 3 + 5;
        uint8_t *clair = malloc(TAILLE), *chiffre = malloc(TAILLE), tag[16], rt[TAILLE];
        for (size_t i = 0; i < TAILLE; i++) clair[i] = (uint8_t)(i * 31 + 17);
        ctx_sched c; contexte_poser(&c, K, IV);
        couloir_sched_msg(&c, clair, chiffre, NULL, 0, tag);
        EVP_CIPHER_CTX *e = EVP_CIPHER_CTX_new();
        int len = 0;
        EVP_DecryptInit_ex(e, EVP_aes_256_gcm(), NULL, NULL, NULL);
        EVP_CIPHER_CTX_ctrl(e, EVP_CTRL_GCM_SET_IVLEN, 12, NULL);
        EVP_DecryptInit_ex(e, NULL, NULL, K, IV);
        EVP_DecryptUpdate(e, rt, &len, chiffre, TAILLE);
        EVP_CIPHER_CTX_ctrl(e, EVP_CTRL_GCM_SET_TAG, 16, tag);
        int ok = EVP_DecryptFinal_ex(e, rt + len, &len) == 1 && !memcmp(rt, clair, TAILLE);
        EVP_CIPHER_CTX_free(e);
        printf("round-trip couloir-sched→EVP : %s\n", ok ? "VERT" : "ROUGE");
        return ok ? 0 : 3;
    }

    if (!strcmp(argv[1], "--session-vert")) {
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 11 + 3;
        for (int i = 0; i < 12; i++) IV[i] = i * 5 + 9;
        uint8_t *clair = malloc(TAILLE), *ch1 = malloc(TAILLE), *ch2 = malloc(TAILLE), t1[16], t2[16];
        for (size_t i = 0; i < TAILLE; i++) clair[i] = (uint8_t)(i * 13 + 7);
        evp_chiffre(K, IV, clair, TAILLE, NULL, 0, ch1, t1);
        evp_session s; evp_session_init(&s, K, IV);
        evp_session_msg(&s, IV, clair, TAILLE, NULL, 0, ch2, t2);
        evp_session_close(&s);
        int ok = !memcmp(ch1, ch2, TAILLE) && !memcmp(t1, t2, 16);
        printf("la convention session EVP recoupée : %s\n",
               ok ? "VERT (octet pour octet)" : "ROUGE");
        return ok ? 0 : 3;
    }

    if (!strcmp(argv[1], "--mesure")) {
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 11 + 3;
        for (int i = 0; i < 12; i++) IV[i] = i * 5 + 9;
        uint8_t *clair = malloc(TAILLE), *chiffre = malloc(TAILLE), tag[16];
        for (size_t i = 0; i < TAILLE; i++) clair[i] = (uint8_t)(i * 13 + 7);
        const int N = 20;
        double t_cs[4][N], t_es[4][N], t_ea[4][N];
        ctx_sched c;
        contexte_poser(&c, K, IV);
        evp_session s;
        int session_ok = evp_session_init(&s, K, IV);
        for (int passe = 0; passe < 4; passe++) {
            for (int i = 0; i < N; i++) {
                struct timespec a, b;
                clock_gettime(CLOCK_MONOTONIC, &a);
                couloir_sched_msg(&c, clair, chiffre, NULL, 0, tag);
                clock_gettime(CLOCK_MONOTONIC, &b);
                t_cs[passe][i] = (b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec);
            }
            for (int i = 0; i < N; i++) {
                struct timespec a, b;
                clock_gettime(CLOCK_MONOTONIC, &a);
                if (session_ok) evp_session_msg(&s, IV, clair, TAILLE, NULL, 0, chiffre, tag);
                else evp_chiffre(K, IV, clair, TAILLE, NULL, 0, chiffre, tag);
                clock_gettime(CLOCK_MONOTONIC, &b);
                t_es[passe][i] = (b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec);
            }
            for (int i = 0; i < N; i++) {
                struct timespec a, b;
                clock_gettime(CLOCK_MONOTONIC, &a);
                evp_chiffre(K, IV, clair, TAILLE, NULL, 0, chiffre, tag);
                clock_gettime(CLOCK_MONOTONIC, &b);
                t_ea[passe][i] = (b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec);
            }
        }
        if (session_ok) evp_session_close(&s);
        int cmp(const void *x, const void *y) { double d = *(double *)x - *(double *)y; return d < 0 ? -1 : d > 0; }
        double med_passe(double t[4][N]) {
            double meds[4];
            for (int p = 0; p < 4; p++) { qsort(t[p], N, sizeof(double), cmp); meds[p] = t[p][N/2]; }
            qsort(meds, 4, sizeof(double), cmp);
            return meds[2];
        }
        double mc = med_passe(t_cs), mes = med_passe(t_es), mea = med_passe(t_ea);
        printf("{\"mediane_couloir_sched_ns\": %.1f, \"mediane_evp_session_ns\": %.1f, "
               "\"mediane_evp_par_appel_ns\": %.1f, \"ratio_vs_session\": %.4f, "
               "\"ratio_vs_par_appel\": %.4f, \"cible\": 1.05, \"verdict_session\": \"%s\", "
               "\"verdict_par_appel\": \"%s\"}\n",
               mc, mes, mea, mc / mes, mc / mea,
               mc / mes <= 1.05 ? "TENUE" : "MANQUÉE",
               mc / mea <= 1.05 ? "TENUE" : "MANQUÉE");
        return 0;
    }
    fprintf(stderr, "mode inconnu\n");
    return 2;
}
int main(int argc, char **argv) { return pilote_main(argc, argv); }
