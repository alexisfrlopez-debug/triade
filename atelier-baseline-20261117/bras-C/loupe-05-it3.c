#include <stdint.h>
#include <windows.h>
#include <string.h>

#define TAMPON_CUMUL (64 * 1024)
#define CUMUL_FENETRE TAMPON_CUMUL

// --- Définitions pour SHA-256 (FIPS 180-4) ---
typedef struct {
    uint32_t etat[8];
    uint8_t tampon[64];
    uint32_t rempli;
    uint64_t total;
} ctx_sha256;

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

#define ROTR(x,n) (((x) >> (n)) | ((x) << (32-(n))))
#define CH(x,y,z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x,y,z) (((x) & (y)) | ((x) & (z)) | ((y) & (z)))
#define SIGMA0(x) (ROTR(x,2) ^ ROTR(x,13) ^ ROTR(x,22))
#define SIGMA1(x) (ROTR(x,6) ^ ROTR(x,11) ^ ROTR(x,25))
#define sigma0(x) (ROTR(x,7) ^ ROTR(x,18) ^ ((x) >> 3))
#define sigma1(x) (ROTR(x,17) ^ ROTR(x,19) ^ ((x) >> 10))

static void sha256_transform(uint32_t state[8], const uint8_t data[64]) {
    uint32_t a, b, c, d, e, f, g, h, t1, t2;
    uint32_t w[64];

    for (int t = 0; t < 16; t++) {
        w[t] = (uint32_t)data[t * 4] << 24 |
               (uint32_t)data[t * 4 + 1] << 16 |
               (uint32_t)data[t * 4 + 2] << 8 |
               (uint32_t)data[t * 4 + 3];
    }
    for (int t = 16; t < 64; t++) {
        w[t] = sigma1(w[t - 2]) + w[t - 7] + sigma0(w[t - 15]) + w[t - 16];
    }

    a = state[0]; b = state[1]; c = state[2]; d = state[3];
    e = state[4]; f = state[5]; g = state[6]; h = state[7];

    for (int t = 0; t < 64; t++) {
        t1 = h + SIGMA1(e) + CH(e, f, g) + K[t] + w[t];
        t2 = SIGMA0(a) + MAJ(a, b, c);
        h = g; g = f; f = e; e = d + t1;
        d = c; c = b; b = a; a = t1 + t2;
    }

    state[0] += a; state[1] += b; state[2] += c; state[3] += d;
    state[4] += e; state[5] += f; state[6] += g; state[7] += h;
}

static void sha256_absorbe(ctx_sha256* ctx, const uint8_t* data, uint32_t len) {
    uint32_t i;
    for (i = 0; i < len; i++) {
        ctx->tampon[ctx->rempli] = data[i];
        ctx->rempli++;
        if (ctx->rempli == 64) {
            sha256_transform(ctx->etat, ctx->tampon);
            ctx->rempli = 0;
        }
    }
    ctx->total += len;
}

static void sha256_final(ctx_sha256* ctx, uint8_t sortie[32]) {
    uint64_t i = ctx->rempli;
    ctx->tampon[i++] = 0x80;
    if (ctx->rempli < 56) {
        memset(&ctx->tampon[i], 0, 56 - i);
    } else {
        memset(&ctx->tampon[i], 0, 64 - i);
        sha256_transform(ctx->etat, ctx->tampon);
        memset(ctx->tampon, 0, 56);
    }
    ctx->tampon[63] = (ctx->total * 8) >> 56;
    ctx->tampon[62] = (ctx->total * 8) >> 48;
    ctx->tampon[61] = (ctx->total * 8) >> 40;
    ctx->tampon[60] = (ctx->total * 8) >> 32;
    ctx->tampon[59] = (ctx->total * 8) >> 24;
    ctx->tampon[58] = (ctx->total * 8) >> 16;
    ctx->tampon[57] = (ctx->total * 8) >> 8;
    ctx->tampon[56] = (ctx->total * 8);
    sha256_transform(ctx->etat, ctx->tampon);
    for (i = 0; i < 8; i++) {
        sortie[i * 4] = (ctx->etat[i] >> 24) & 0xff;
        sortie[i * 4 + 1] = (ctx->etat[i] >> 16) & 0xff;
        sortie[i * 4 + 2] = (ctx->etat[i] >> 8) & 0xff;
        sortie[i * 4 + 3] = ctx->etat[i] & 0xff;
    }
}

// --- Implémentation de la fonction exportée ---
HANDLE g_session_handle = INVALID_HANDLE_VALUE;

long long loupe_05_sha256(uint64_t decalage, uint64_t longueur, void* sortie_ptr) {
    // E1: Vérification de la session
    if (g_session_handle == INVALID_HANDLE_VALUE) {
        return -4;
    }

    // E3: Vérification du pointeur de sortie
    if (sortie_ptr == NULL) {
        return -5;
    }

    // E2: Vérification des bornes
    uint64_t taille = *(uint64_t*)((uint8_t*)g_session_handle + 520);
    if (longueur > taille || decalage > taille - longueur) {
        return -3;
    }

    // Initialisation du contexte SHA-256 avec les H0 FIPS
    ctx_sha256 s2 = {
        .etat = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19},
        .tampon = {0},
        .rempli = 0,
        .total = 0
    };

    uint8_t fenetre[CUMUL_FENETRE];
    uint64_t restant = longueur;
    uint64_t offset_courant = decalage;

    while (restant > 0) {
        uint64_t a_lire = (restant < CUMUL_FENETRE) ? restant : CUMUL_FENETRE;

        // Repositionner le pointeur de fichier pour chaque fenêtre
        LARGE_INTEGER li;
        li.QuadPart = offset_courant;
        if (!SetFilePointerEx(g_session_handle, li, NULL, FILE_BEGIN)) {
            return -6;
        }

        DWORD lus;
        if (!ReadFile(g_session_handle, fenetre, (DWORD)a_lire, &lus, NULL)) {
            return -6;
        }

        if (lus != a_lire) {
            return -6;
        }

        sha256_absorbe(&s2, fenetre, (uint32_t)lus);
        restant -= lus;
        offset_courant += lus;
    }

    sha256_final(&s2, (uint8_t*)sortie_ptr);
    return 0;
}
