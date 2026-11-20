// sha256ni_ref.c — LA RÉFÉRENCE SHA-NI DE LABORATOIRE (l'intrication des
// extensions SHA) — la disposition des lanes RÉSOLUE PAR SONDES EMPIRIQUES
// (rnds2 : src = (A,B,E,F) aux lanes 3,2,1,0 ; dst = (C,D,G,H) ; la
// sortie = le nouveau (a2,b2,e2,f2) dans dst — la sonde rnds2_probe.c ;
// msg1 : out[j] = dst[j] + σ0(dst[j+1]), out[3] = dst[3] + σ0(src[0]) ;
// msg2 : out[0] = dst[0] + σ1(src[2]), out[1] = dst[1] + σ1(src[3]),
// out[2] = dst[2] + σ1(out[0]), out[3] = dst[3] + σ1(out[1]) — les
// sondes msg_probe/msg2_probe2) ; LA SÉQUENCE D'EXTENSION DÉRIVÉE : la
// génération g (fenêtre W[16+4g..19+4g]) = msg1(S[g], S[g+1]) puis
// alignr(S[g+3], S[g+2], 4) ajouté puis msg2(S[g], S[g+3]) — le cycle
// des quatre fenêtres, l'ordre des générations respecté.
// gcc -O2 -msha -mssse3 -msse4.1 -o sha256ni_ref sha256ni_ref.c
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <immintrin.h>

void sha256_compress_shaext(uint32_t state[8], const uint8_t block[64])
{
    __m128i ABEF, CDGH, SAV0, SAV1, MSG, TMP;
    __m128i S[4];
    int g;
    const __m128i BSWAP = _mm_set_epi8(12,13,14,15, 8,9,10,11,
                                       4,5,6,7, 0,1,2,3);
    static const uint32_t K[64] = {
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,
        0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,
        0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,
        0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,
        0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,
        0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,
        0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,
        0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
        0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
    };
    const __m128i *K256 = (const __m128i *)K;

    /* l'état : les mots BE → les valeurs ; ABEF/CDGH aux lanes 3,2,1,0 */
    {
        __m128i t0, t1;
        /* l'état est un tableau de u32 (les VALEURS natives — pas d'octets
           BE : AUCUN bswap ici ; le bswap n'appartient qu'au BLOC) */
        t0 = _mm_loadu_si128((const __m128i *)&state[0]);   /* [A,B,C,D] */
        t1 = _mm_loadu_si128((const __m128i *)&state[4]);   /* [E,F,G,H] */
        SAV0 = t0; SAV1 = t1;
        t0 = _mm_shuffle_epi32(t0, 0xB1);   /* [B,A,D,C] */
        t1 = _mm_shuffle_epi32(t1, 0xB1);   /* [F,E,H,G] */
        ABEF = _mm_unpacklo_epi64(t1, t0);  /* [F,E,B,A] */
        CDGH = _mm_unpackhi_epi64(t1, t0);  /* [H,G,D,C] */
    }
    /* les fenêtres du message (bswap par dword, plain lanes) */
    S[0] = _mm_shuffle_epi8(_mm_loadu_si128((const __m128i *)&block[0]),  BSWAP);
    S[1] = _mm_shuffle_epi8(_mm_loadu_si128((const __m128i *)&block[16]), BSWAP);
    S[2] = _mm_shuffle_epi8(_mm_loadu_si128((const __m128i *)&block[32]), BSWAP);
    S[3] = _mm_shuffle_epi8(_mm_loadu_si128((const __m128i *)&block[48]), BSWAP);

    /* les rondes 0-15 : les fenêtres d'entrée telles quelles */
    for (g = 0; g < 4; g++) {
        MSG = _mm_add_epi32(S[g], K256[g]);
        CDGH = _mm_sha256rnds2_epu32(CDGH, ABEF, MSG);
        MSG = _mm_shuffle_epi32(MSG, 0x0E);
        ABEF = _mm_sha256rnds2_epu32(ABEF, CDGH, MSG);
    }
    /* les générations 0..11 : chaque fenêtre W[16+4g..19+4g] étendue
       puis consommée par sa paire de rnds2 */
    for (g = 0; g < 12; g++) {
        int k = g & 3;                 /* le slot de la fenêtre générée */
        int k1 = (g + 1) & 3;          /* la fenêtre plus récente (msg1) */
        int k2 = (g + 2) & 3, k3 = (g + 3) & 3;
        S[k] = _mm_sha256msg1_epu32(S[k], S[k1]);
        TMP = _mm_alignr_epi8(S[k3], S[k2], 4);   /* W[4g+9..4g+12] */
        S[k] = _mm_add_epi32(S[k], TMP);
        S[k] = _mm_sha256msg2_epu32(S[k], S[k3]);
        MSG = _mm_add_epi32(S[k], K256[4 + g]);
        CDGH = _mm_sha256rnds2_epu32(CDGH, ABEF, MSG);
        MSG = _mm_shuffle_epi32(MSG, 0x0E);
        ABEF = _mm_sha256rnds2_epu32(ABEF, CDGH, MSG);
    }

    /* la sommation : état += les variables ; la recomposition */
    {
        __m128i t0, t1;
        t0 = _mm_unpackhi_epi64(ABEF, CDGH);   /* [B,A,D,C] */
        t1 = _mm_unpacklo_epi64(ABEF, CDGH);   /* [F,E,H,G] */
        t0 = _mm_shuffle_epi32(t0, 0xB1);      /* [A,B,C,D] */
        t1 = _mm_shuffle_epi32(t1, 0xB1);      /* [E,F,G,H] */
        t0 = _mm_add_epi32(t0, SAV0);
        t1 = _mm_add_epi32(t1, SAV1);
        _mm_storeu_si128((__m128i *)&state[0], t0);
        _mm_storeu_si128((__m128i *)&state[4], t1);
    }
}

int main(void)
{
    uint32_t state[8];
    uint32_t init[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                        0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    uint8_t bloc[64];
    memcpy(state, init, 32);
    for (int i = 0; i < 64; i++) bloc[i] = (uint8_t)(i * 7 + 3);
    sha256_compress_shaext(state, bloc);
    printf("etat_shaext:");
    for (int i = 0; i < 8; i++) printf("%08x", state[i]);
    printf("\n");
    return 0;
}
