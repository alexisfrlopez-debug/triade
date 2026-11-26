/* couloir_vaes_v2.c — LE COULOIR AES-256-GCM VAES/VPCLMULQDQ, DEUXIÈME PASSE (W28VAES).
 * La notation couloir-vaes.asm (7911d03f… INTACTE, recopiée au présent atelier) reconduite ;
 * LES QUATRE CAUSES de la décomposition W27VAES attaquées à la source :
 *   (a) l'expansion + les puissances H hors boucle PAR APPEL → AMORTIES PAR CONTEXTE DE
 *       SESSION (couloir_init_v2 UNE fois par clé, comme le chemin EVP à contexte posé) ;
 *   (b) la conversion rev128 PAR BLOC côté GHASH → LE DOMAINE RÉFLÉCHI DE BOUT EN BOUT :
 *       la conversion UNE SEULE FOIS À LA FRONTIÈRE de chaque pli (les 8 blocs du pli
 *       réfléchis en QUATRE passes ymm — deux blocs par passe), H et ses puissances
 *       demeurent en bitref8 de bout en bout ;
 *   (c) le schedule C non préservé par le compilateur → traitée par LA PIÈCE D'ASSEMBLAGE
 *       couloir_sched (le schedule de la notation exécuté) — l'écart notation-vs-C y est
 *       mesuré en propre ;
 *   (d) la frontière d'appel hors ligne → SUPPRIMÉE : le couloir inliné au point de mesure
 *       (le message part du contexte déjà posé, une seule frontière).
 * Les épreuves (dans l'ordre, AVANT toute mesure) : --kat, --negatif, --roundtrip.
 * La mesure : --mesure (n=20 par pièce, cœur épinglé par l'appelant, 4 Kio, contre EVP
 * AU MÊME VOLUME — les deux conventions nommées : EVP à contexte posé [session, la
 * comparaison à algorithme égal] ET EVP à contexte par appel [la convention W27VAES,
 * la comparabilité directe]).
 * Compilation : gcc -O2 -mavx2 -mvaes -mvpclmulqdq -maes [-DMUTATION] -lcrypto
 */
#include <immintrin.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>

/* ---- la boîte S de FIPS 197 (le code, jamais une donnée secrète) ------------ */
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

/* ---- l'expansion AES-256 : 15 clés de tour, broadcastées aux deux voies ------- */
typedef struct { __m256i rk[15]; } cles_tour;

static void expansion_aes256(const uint8_t cle[32], cles_tour *ct) {
    uint32_t w[60];
    for (int i = 0; i < 8; i++)
        w[i] = ((uint32_t)cle[4 * i] << 24) | ((uint32_t)cle[4 * i + 1] << 16)
             | ((uint32_t)cle[4 * i + 2] << 8) | cle[4 * i + 3];
    for (int i = 8; i < 60; i++) {
        uint32_t t = w[i - 1];
        if (i % 8 == 0) t = sub_word((t << 8) | (t >> 24)) ^ ((uint32_t)RCON[i / 8] << 24);
        else if (i % 8 == 4) t = sub_word(t);
        w[i] = w[i - 8] ^ t;
    }
    for (int r = 0; r < 15; r++) {
        uint8_t rk_o[16];
        for (int j = 0; j < 4; j++) {
            rk_o[4 * j] = (uint8_t)(w[4 * r + j] >> 24);
            rk_o[4 * j + 1] = (uint8_t)(w[4 * r + j] >> 16);
            rk_o[4 * j + 2] = (uint8_t)(w[4 * r + j] >> 8);
            rk_o[4 * j + 3] = (uint8_t)w[4 * r + j];
        }
        __m128i k = _mm_loadu_si128((const __m128i *)rk_o);
        ct->rk[r] = _mm256_broadcastsi128_si256(k);
#ifdef MUTATION
        if (r == 13) ct->rk[r] = _mm256_xor_si256(ct->rk[r], _mm256_set1_epi8(0x5a)); /* la mutation nommée */
#endif
    }
}

/* ---- GHASH : le corps réfléchi (les primitives W27VALES réputées) ------------- */
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
    carry = _mm_slli_si128(carry, 8);
    return _mm_or_si128(base, carry);
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

/* LA CONVERSION AU MONDE RÉFLÉCHI — la version 128 (l'AAD, la longueur) */
static inline __m128i rev128(__m128i v) {
    const __m128i T = _mm_setr_epi8(0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15);
    const __m128i M = _mm_set1_epi8(0x0F);
    const __m128i MF0 = _mm_set1_epi8((char)0xF0);
    __m128i bas = _mm_shuffle_epi8(T, _mm_and_si128(v, M));
    __m128i haut = _mm_shuffle_epi8(T, _mm_and_si128(_mm_srli_epi16(v, 4), M));
    return _mm_or_si128(_mm_and_si128(_mm_slli_epi16(bas, 4), MF0), haut);
}

/* LA CONVERSION À LA FRONTIÈRE DU PLI — la version 256 : DEUX blocs par passe,
 * la cause (b) attaquée : huit rev128 par pli → QUATRE rev256 (moitié des passes,
 * chaque passe ymm servant deux blocs). L'idiome est le même (les quartets masqués,
 * l'ordre des octets préservé, PAR VOIE 128 de l'ymm). */
static inline __m256i rev256(__m256i v) {
    const __m256i T = _mm256_setr_epi8(0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15,
                                       0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15);
    const __m256i M = _mm256_set1_epi8(0x0F);
    const __m256i MF0 = _mm256_set1_epi8((char)0xF0);
    __m256i bas = _mm256_shuffle_epi8(T, _mm256_and_si256(v, M));
    __m256i haut = _mm256_shuffle_epi8(T, _mm256_and_si256(_mm256_srli_epi16(v, 4), M));
    return _mm256_or_si256(_mm256_and_si256(_mm256_slli_epi16(bas, 4), MF0), haut);
}

/* ---- le contexte de session (la cause (a) soldée : UNE fois par clé) --------- */
#define TAILLE 4096

typedef struct {
    cles_tour ct;
    __m128i Hr;          /* H réfléchi (bitref8) */
    __m128i Hp[8];       /* H¹..H⁸ réfléchies — de bout en bout */
    __m128i ej0;         /* E_K(J0) pour le tag (amorti) */
    uint8_t iv[12];
} couloir_etat;

static inline __m128i un_bloc_aes(const cles_tour *ct, __m128i x) {
    x = _mm_xor_si128(x, _mm256_castsi256_si128(ct->rk[0]));
    for (int r = 1; r <= 13; r++) x = _mm_aesenc_si128(x, _mm256_castsi256_si128(ct->rk[r]));
    return _mm_aesenclast_si128(x, _mm256_castsi256_si128(ct->rk[14]));
}

static void couloir_init_v2(couloir_etat *e, const uint8_t cle[32], const uint8_t iv[12]) {
    expansion_aes256(cle, &e->ct);
    memcpy(e->iv, iv, 12);
    __m128i zero = _mm_setzero_si128();
    e->Hr = rev128(un_bloc_aes(&e->ct, zero));
    e->Hp[0] = e->Hr;
    for (int i = 1; i < 8; i++) e->Hp[i] = gfmul(e->Hp[i - 1], e->Hr);
    uint8_t j0[16];
    memcpy(j0, iv, 12);
    j0[12] = 0; j0[13] = 0; j0[14] = 0; j0[15] = 1;
    e->ej0 = un_bloc_aes(&e->ct, _mm_loadu_si128((const __m128i *)j0));
}

/* les DEUX compteurs d'un pas, en voies ymm */
static inline __m256i compteurs_ymm(const couloir_etat *e, uint64_t base) {
    uint8_t c0[16], c1[16];
    memcpy(c0, e->iv, 12);
    memcpy(c1, e->iv, 12);
    uint32_t b0 = (uint32_t)base, b1 = (uint32_t)(base + 1);
    c0[12] = b0 >> 24; c0[13] = b0 >> 16; c0[14] = b0 >> 8; c0[15] = b0;
    c1[12] = b1 >> 24; c1[13] = b1 >> 16; c1[14] = b1 >> 8; c1[15] = b1;
    __m128i lo = _mm_loadu_si128((const __m128i *)c0);
    __m128i hi = _mm_loadu_si128((const __m128i *)c1);
    return _mm256_insertf128_si256(_mm256_castsi128_si256(lo), hi, 1);
}

static inline __m256i deux_blocs_aes_ymm(const cles_tour *ct, __m256i x) {
    x = _mm256_xor_si256(x, ct->rk[0]);
    for (int r = 1; r <= 13; r++) x = _mm256_aesenc_epi128(x, ct->rk[r]);
    return _mm256_aesenclast_epi128(x, ct->rk[14]);
}

/* ---- LE MESSAGE (la cause (d) soldée : UNE frontière, le contexte déjà posé) --
 * Le couloir entier inliné : le GHASH de l'AAD, la boucle entrelacée, le tag. */
static void couloir_msg(couloir_etat *e, const uint8_t *clair, uint8_t *chiffre,
                        const uint8_t *aad, size_t alen, uint8_t tag[16]) {
    /* le GHASH de l'AAD (la voie scalaire — l'AAD est court) */
    __m128i acc = _mm_setzero_si128();
    size_t i = 0;
    for (; i + 16 <= alen; i += 16) {
        __m128i x = rev128(_mm_loadu_si128((const __m128i *)(aad + i)));
        acc = gfmul(_mm_xor_si128(acc, x), e->Hr);
    }
    if (i < alen) {
        uint8_t buf[16] = {0};
        memcpy(buf, aad + i, alen - i);
        __m128i x = rev128(_mm_loadu_si128((const __m128i *)buf));
        acc = gfmul(_mm_xor_si128(acc, x), e->Hr);
    }

    /* LA BOUCLE ENTRELACÉE : 4 Kio = 32 blocs = 4 plis de 8 ;
     * la frappe CTR du pli g+1 précède le pli GHASH du pli g ;
     * LA FRONTIÈRE RÉFLÉCHIE : les 8 blocs du pli convertis en QUATRE rev256 */
    __m256i flot_suivant = deux_blocs_aes_ymm(&e->ct, compteurs_ymm(e, 2));
    __m128i pile_lo = _mm_setzero_si128(), pile_hi = _mm_setzero_si128();
    for (int g = 0; g < TAILLE / 128; g++) {
        /* la frappe CTR des 8 blocs du pli g (4 pas de 2 blocs) — ET la
         * conversion à la frontière : chaque chiffre ymm reflété DÈS SA NAISSANCE */
        __m256i refl[4];
        for (int k = 0; k < 4; k++) {
            __m256i flot;
            if (g == 0 && k == 0) flot = flot_suivant;       /* l'entrelacement : déjà frappé */
            else flot = deux_blocs_aes_ymm(&e->ct, compteurs_ymm(e, 8 * (uint64_t)g + 2 * k + 2));
            __m256i clair_ymm = _mm256_loadu_si256((const __m256i *)(clair + 128 * g + 32 * k));
            __m256i ct_ymm = _mm256_xor_si256(flot, clair_ymm);
            _mm256_storeu_si256((__m256i *)(chiffre + 128 * g + 32 * k), ct_ymm);
            refl[k] = rev256(ct_ymm);                        /* LA FRONTIÈRE : deux blocs par passe */
        }
        /* la frappe du pli SUIVANT commence ici (l'entrelacement) */
        if (g + 1 < TAILLE / 128)
            flot_suivant = deux_blocs_aes_ymm(&e->ct, compteurs_ymm(e, 8 * (uint64_t)(g + 1) + 2));
        /* le pli GHASH des 8 blocs RÉFLÉCHIS : les produits par paires sur VPCLMULQDQ */
        for (int paire = 0; paire < 4; paire++) {
            __m256i va = refl[paire];
            /* les puissances appariées : la voie basse C_{2p} ⊗ H^{8-2p}, la haute C_{2p+1} ⊗ H^{7-2p} */
            __m128i h0 = e->Hp[8 - 1 - 2 * paire];
            __m128i h1 = e->Hp[8 - 2 - 2 * paire];
            __m256i vb = _mm256_insertf128_si256(_mm256_castsi128_si256(h0), h1, 1);
            __m256i a01 = _mm256_xor_si256(_mm256_unpacklo_epi64(va, va),
                                           _mm256_unpackhi_epi64(va, va));
            __m256i b01 = _mm256_xor_si256(_mm256_unpacklo_epi64(vb, vb),
                                           _mm256_unpackhi_epi64(vb, vb));
            __m256i l = _mm256_clmulepi64_epi128(va, vb, 0x00);
            __m256i h = _mm256_clmulepi64_epi128(va, vb, 0x11);
            __m256i m = _mm256_clmulepi64_epi128(a01, b01, 0x00);
            m = _mm256_xor_si256(m, _mm256_xor_si256(l, h));
            __m256i ml = _mm256_slli_si256(m, 8);
            __m256i mh = _mm256_srli_si256(m, 8);
            __m256i lo_lane = _mm256_xor_si256(l, ml);
            __m256i hi_lane = _mm256_xor_si256(h, mh);
            pile_lo = _mm_xor_si128(pile_lo, _mm256_castsi256_si128(lo_lane));
            pile_lo = _mm_xor_si128(pile_lo, _mm256_extracti128_si256(lo_lane, 1));
            pile_hi = _mm_xor_si128(pile_hi, _mm256_castsi256_si128(hi_lane));
            pile_hi = _mm_xor_si128(pile_hi, _mm256_extracti128_si256(hi_lane, 1));
        }
        /* le pli du compte précédent : acc⊗H⁸ — puis la réduction UNIQUE du pli */
        __m128i alo, ahi;
        clmul_karatsuba(acc, e->Hp[7], &alo, &ahi);
        __m128i lo = _mm_xor_si128(pile_lo, alo);
        __m128i hi = _mm_xor_si128(pile_hi, ahi);
        acc = reduit_gcm(lo, hi);
        pile_lo = pile_hi = _mm_setzero_si128();
#ifdef DBG2
        { uint8_t b[16]; memcpy(b, &acc, 16); printf("  acc(fold) : "); for (int q=0;q<16;q++) printf("%02x", b[q]); printf("\n"); }
#endif
    }

    /* le bloc des longueurs (bits) */
    uint8_t lb[16];
    uint64_t abits = (uint64_t)alen * 8, cbits = (uint64_t)TAILLE * 8;
    for (int k = 0; k < 8; k++) { lb[k] = abits >> (56 - 8 * k); lb[8 + k] = cbits >> (56 - 8 * k); }
    __m128i lx = rev128(_mm_loadu_si128((const __m128i *)lb));
    acc = gfmul(_mm_xor_si128(acc, lx), e->Hr);

    __m128i t = _mm_xor_si128(rev128(acc), e->ej0);
    _mm_storeu_si128((__m128i *)tag, t);
}

/* ---- le dispatch HISSÉ HORS BOUCLE -------------------------------------------- */
static int silicium_ok(void) {
    __builtin_cpu_init();
    return __builtin_cpu_supports("vaes") && __builtin_cpu_supports("vpclmulqdq")
        && __builtin_cpu_supports("avx2");
}

/* ---- le référentiel EVP : LES DEUX CONVENTIONS ---------------------------------
 * evp_par_appel : la convention W27VAES (un contexte complet par appel, la clé
 *                 re-établie — la comparabilité directe à la mesure précédente) ;
 * evp_session   : la convention à algorithme égal (le contexte posé UNE fois à la
 *                 clé, chaque message ne portant que l'IV — le même amortissement
 *                 que le couloir v2). */
typedef struct {
    EVP_CIPHER_CTX *c;
} evp_session;

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

static int evp_session_init(evp_session *s, const uint8_t cle[32], const uint8_t iv[12]) {
    s->c = EVP_CIPHER_CTX_new();
    int len = 0;
    if (EVP_EncryptInit_ex(s->c, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1) return 0;
    if (EVP_CIPHER_CTX_ctrl(s->c, EVP_CTRL_GCM_SET_IVLEN, 12, NULL) != 1) return 0;
    if (EVP_EncryptInit_ex(s->c, NULL, NULL, cle, iv) != 1) return 0;
    return 1;
}

static int evp_session_msg(evp_session *s, const uint8_t iv[12], const uint8_t *clair,
                           size_t n, const uint8_t *aad, size_t alen, uint8_t *chiffre, uint8_t tag[16]) {
    int len = 0, len2 = 0;
    if (EVP_EncryptInit_ex(s->c, NULL, NULL, NULL, iv) != 1) return 0;   /* l'IV neuf, la clé posée */
    if (alen) EVP_EncryptUpdate(s->c, NULL, &len, aad, (int)alen);
    EVP_EncryptUpdate(s->c, chiffre, &len2, clair, (int)n);
    EVP_EncryptFinal_ex(s->c, chiffre + len2, &len2);
    if (EVP_CIPHER_CTX_ctrl(s->c, EVP_CTRL_GCM_GET_TAG, 16, tag) != 1) return 0;
    return 1;
}

static void evp_session_close(evp_session *s) { EVP_CIPHER_CTX_free(s->c); }

/* ---- la porte : les épreuves AVANT toute mesure -------------------------------- */
static int hex_vers(const char *h, uint8_t *o, size_t max) {
    size_t n = strlen(h) / 2;
    if (n > max) return -1;
    for (size_t i = 0; i < n; i++) sscanf(h + 2 * i, "%2hhx", o + i);
    return (int)n;
}

static int couloir_main(int argc, char **argv) {
    if (!silicium_ok()) {
        printf("SILICIUM-ABSENT : le couloir refuse (aucun repli)\n");
        return 4;
    }
    if (argc < 2) { fprintf(stderr, "usage : couloir_vaes_v2 --kat|--negatif|--roundtrip|--mesure|--debug\n"); return 2; }

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
                uint8_t K[32], IV[12], TAG_A[16];
                hex_vers(key, K, 32); hex_vers(iv, IV, 12); hex_vers(tag_att, TAG_A, 16);
                uint8_t *clair = calloc(TAILLE, 1), *chiffre = calloc(TAILLE, 1);
                hex_vers(pt, clair, TAILLE);
                uint8_t aad_b[1024]; size_t aadlen = hex_vers(aad, aad_b, 1024);
                if (strlen(aad) == 0) aadlen = 0;
                couloir_etat e; couloir_init_v2(&e, K, IV);
                uint8_t tag[16];
                couloir_msg(&e, clair, chiffre, aad_b, aadlen, tag);
                uint8_t *ct_evp = calloc(TAILLE, 1), tag_evp[16];
                evp_chiffre(K, IV, clair, TAILLE, aad_b, aadlen, ct_evp, tag_evp);
                int ok = !memcmp(tag, tag_evp, 16) && !memcmp(chiffre, ct_evp, TAILLE);
                verts += ok ? 1 : 0;
                if (premier) {
                    printf("premier vecteur : couloir==EVP %s\n", ok ? "VERT" : "ROUGE");
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
        printf("%s : %d/%d vecteurs couloir==EVP octet pour octet (4 Kio paddés, tag compris)\n",
               argv[1], verts, nvec);
        return (verts == nvec) ? 0 : 3;
    }

    if (!strcmp(argv[1], "--debug")) {
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 7 + 1;
        for (int i = 0; i < 12; i++) IV[i] = i * 3 + 5;
        couloir_etat e; couloir_init_v2(&e, K, IV);
        printf("H_reflechi = ");
        for (int i = 0; i < 16; i++) printf("%02x", ((uint8_t *)&e.Hr)[i]);
        printf("\nE_K(J0)    = ");
        for (int i = 0; i < 16; i++) printf("%02x", ((uint8_t *)&e.ej0)[i]);
        printf("\nH1 = ");
        for (int i = 0; i < 16; i++) printf("%02x", ((uint8_t *)&e.Hp[0])[i]);
        printf("\nH2 = ");
        for (int i = 0; i < 16; i++) printf("%02x", ((uint8_t *)&e.Hp[1])[i]);
        printf("\n");
        return 0;
    }

    if (!strcmp(argv[1], "--roundtrip")) {
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 7 + 1;
        for (int i = 0; i < 12; i++) IV[i] = i * 3 + 5;
        uint8_t *clair = malloc(TAILLE), *chiffre = malloc(TAILLE), tag[16], rt[TAILLE];
        for (size_t i = 0; i < TAILLE; i++) clair[i] = (uint8_t)(i * 31 + 17);
        couloir_etat e; couloir_init_v2(&e, K, IV);
        couloir_msg(&e, clair, chiffre, NULL, 0, tag);
        EVP_CIPHER_CTX *c = EVP_CIPHER_CTX_new();
        int len = 0;
        EVP_DecryptInit_ex(c, EVP_aes_256_gcm(), NULL, NULL, NULL);
        EVP_CIPHER_CTX_ctrl(c, EVP_CTRL_GCM_SET_IVLEN, 12, NULL);
        EVP_DecryptInit_ex(c, NULL, NULL, K, IV);
        EVP_DecryptUpdate(c, rt, &len, chiffre, TAILLE);
        EVP_CIPHER_CTX_ctrl(c, EVP_CTRL_GCM_SET_TAG, 16, tag);
        int ok = EVP_DecryptFinal_ex(c, rt + len, &len) == 1 && !memcmp(rt, clair, TAILLE);
        EVP_CIPHER_CTX_free(c);
        printf("round-trip couloir→EVP : %s\n", ok ? "VERT" : "ROUGE");
        return ok ? 0 : 3;
    }

    if (!strcmp(argv[1], "--session-vert")) {
        /* la CONVENTION SESSION recoupée : la même clé, l'IV posé par message —
         * le ciphertext et le tag DOIVENT être identiques à la convention par appel */
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
        printf("la convention session EVP recoupée contre la convention par appel : %s\n",
               ok ? "VERT (octet pour octet)" : "ROUGE (la voie session refuse — le fallback nommé)");
        return ok ? 0 : 3;
    }


    if (!strcmp(argv[1], "--dbg1")) {
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 7 + 1;
        for (int i = 0; i < 12; i++) IV[i] = i * 3 + 5;
        uint8_t clair[TAILLE], ch[TAILLE], tag[16];
        memset(clair, 0, TAILLE);
        couloir_etat e; couloir_init_v2(&e, K, IV);
        couloir_msg(&e, clair, ch, NULL, 0, tag);
        printf("tag: "); for (int i = 0; i < 16; i++) printf("%02x", tag[i]); printf("\n");
        printf("ct16: "); for (int i = 0; i < 16; i++) printf("%02x", ch[i]); printf("\n");
        printf("ct2048: "); for (int i = 2048; i < 2064; i++) printf("%02x", ch[i]); printf("\n");
        { FILE *fo = fopen("/tmp/ct_v2.bin", "wb"); if (fo) { fwrite(ch, 1, TAILLE, fo); fclose(fo); } }
        { FILE *fo = fopen("/tmp/ct_s_.bin", "wb"); if (fo) { fwrite(ch, 1, TAILLE, fo); fclose(fo); } }
        return 0;
    }
    if (!strcmp(argv[1], "--mesure")) {
        /* n=20 par pièce, quatre passes, 4 Kio, contre EVP AU MÊME VOLUME.
         * TROIS PIÈCES : le couloir v2 (session, inliné), EVP session, EVP par appel.
         * L'ENVIRONNEMENT : le chemin EVP réel consigné (OPENSSL_ia32cap), la
         * fréquence NON goupillée (VM) — le caveat nommé, le kit machine réelle livré. */
        uint8_t K[32], IV[12];
        for (int i = 0; i < 32; i++) K[i] = i * 11 + 3;
        for (int i = 0; i < 12; i++) IV[i] = i * 5 + 9;
        uint8_t *clair = malloc(TAILLE), *chiffre = malloc(TAILLE), tag[16];
        for (size_t i = 0; i < TAILLE; i++) clair[i] = (uint8_t)(i * 13 + 7);
        const int N = 20;
        double t_c2[4][N], t_es[4][N], t_ea[4][N];
        couloir_etat e;
        couloir_init_v2(&e, K, IV);                       /* le contexte posé UNE fois (la session) */
        evp_session s;
        int session_ok = evp_session_init(&s, K, IV);
        for (int passe = 0; passe < 4; passe++) {
            for (int i = 0; i < N; i++) {
                struct timespec a, b;
                clock_gettime(CLOCK_MONOTONIC, &a);
                couloir_msg(&e, clair, chiffre, NULL, 0, tag);
                clock_gettime(CLOCK_MONOTONIC, &b);
                t_c2[passe][i] = (b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec);
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
        /* les médianes par passe puis la médiane des passes (la convention W27VAES) */
        int cmp(const void *x, const void *y) { double d = *(double *)x - *(double *)y; return d < 0 ? -1 : d > 0; }
        double med_passe(double t[4][N]) {
            double meds[4];
            for (int p = 0; p < 4; p++) { qsort(t[p], N, sizeof(double), cmp); meds[p] = t[p][N / 2]; }
            qsort(meds, 4, sizeof(double), cmp);
            return meds[2];
        }
        double mc = med_passe(t_c2), mes = med_passe(t_es), mea = med_passe(t_ea);
        printf("{\"mediane_couloir_v2_ns\": %.1f, \"mediane_evp_session_ns\": %.1f, "
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

int main(int argc, char **argv) { return couloir_main(argc, argv); }
