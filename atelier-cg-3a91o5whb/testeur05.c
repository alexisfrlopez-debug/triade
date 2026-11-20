/* LE TESTEUR POSIX : le cœur sha256 de la pièce confronté au juge hashlib
   (les vecteurs FIPS 180-4 + les tampons aléatoires déterministes) */
#define main piece_main_unused
#include "loupe-05-posix.c"
#undef main
#undef main_piece_main

int main(void) {
    struct sha256_ctx ctx;
    uint8_t hash[32];
    int verts = 0, total = 0;
    /* les vecteurs FIPS 180-4 */
    struct { const char *txt; const char *hex; } V[] = {
        {"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"},
        {"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
         "248d6a61d20638b8e5c026930c3e60abe95590b8315d769dcd8bb0f6fa5cc6fc"},
        {"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
    };
    for (unsigned i = 0; i < sizeof(V)/sizeof(V[0]); i++) {
        sha256_init(&ctx);
        sha256_update(&ctx, (const uint8_t*)V[i].txt, strlen(V[i].txt));
        sha256_final(&ctx, hash);
        char hex[65] = {0};
        for (int j = 0; j < 32; j++) sprintf(hex + j*2, "%02x", hash[j]);
        total++;
        int ok = strcmp(hex, V[i].hex) == 0;
        verts += ok;
        printf("[%s] FIPS %u : %s\n", ok ? "VERT" : "ROUGE", i, hex);
    }
    /* les tampons pseudo-aléatoires déterministes (les tailles aux bords
       du rembourrage : 55, 56, 63, 64, 65, 127, 128, 1000, 65536+3) */
    uint64_t xs = 20261120;
    size_t tailles[] = {55, 56, 63, 64, 65, 127, 128, 1000, 65539};
    for (unsigned t = 0; t < sizeof(tailles)/sizeof(tailles[0]); t++) {
        size_t n = tailles[t];
        uint8_t *buf = malloc(n ? n : 1);
        for (size_t j = 0; j < n; j++) {
            xs ^= xs << 13; xs ^= xs >> 7; xs ^= xs << 17;
            buf[j] = (uint8_t)(xs >> 32);
        }
        sha256_init(&ctx);
        /* les fenêtres de 64 : l'update en morceaux de 64 (le miroir des
           fenêtres de la pièce) */
        size_t off = 0;
        while (off < n) {
            size_t m = (n - off > 64) ? 64 : (n - off);
            sha256_update(&ctx, buf + off, m);
            off += m;
        }
        sha256_final(&ctx, hash);
        /* le fichier témoin pour le juge python */
        char nom[64];
        sprintf(nom, "temoin-%zu.bin", n);
        FILE *f = fopen(nom, "wb");
        fwrite(buf, 1, n, f);
        fclose(f);
        char nomh[64];
        sprintf(nomh, "rendu-%zu.hex", n);
        f = fopen(nomh, "w");
        for (int j = 0; j < 32; j++) fprintf(f, "%02x", hash[j]);
        fclose(f);
        free(buf);
    }
    printf("LES VECTEURS FIPS : %d/%d VERT — les 9 témoins posés "
           "(le juge python suit)\n", verts, total);
    return 0;
}
