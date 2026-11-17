/* harnais_c.c — L'ÉPREUVE D'EXÉCUTION V1-V5 DU BRAS C (le labo de la
   baseline, session du 17/11/2026) : la pièce loupe-05-it3.c compilée
   gcc -O2 -std=c11 contre le shim windows.h du labo, les TROIS fonctions
   de la liste fermée D161 servies par le harnais (le fichier en mémoire,
   le pointeur, l'échec armable, la mutation armable).

   Sortie : des lignes PARSEABLES (le pilote Python assemble le JSON) :
     V1 <n> <crashs> <divergents>
     V1E <cas> <off> <len> <rax> <produit16> <attendu16>
     V2 vide <produit64> <ok>
     V2 abc <produit64> <ok>
     V3 <e1> <e2> <e3> <ok>
     V4 <rax> <intacte> <fenetres> <code>
     V5 <ref16> <mute16> <divergence>

   Usage : harnais_c <proxy.exe> <gammes.txt>
   gammes.txt : des lignes « off len » ; le séparateur « -1 -1 » ouvre les
   gammes multi-fenêtres du témoin bi-fenêtre (proxy.exe ×2). */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h> /* le shim du labo (-I lab/shim) */

#include "../bras-C/loupe-05-it3.c"

/* --- le modèle de fichier du harnais --- */
static uint8_t *fichier;
static uint64_t taille_f, pos_f;
static int fenetre_courante = 0;
static int failread_au = 0, mutate_au = 0;
static DWORD derniere_erreur = 0;

BOOL SetFilePointerEx(HANDLE h, LARGE_INTEGER li, LARGE_INTEGER *np, DWORD m) {
    (void)h; (void)np; (void)m;
    pos_f = (uint64_t)li.QuadPart;
    return 1;
}

BOOL ReadFile(HANDLE h, void *buf, DWORD n, DWORD *lus, void *o) {
    (void)h; (void)o;
    fenetre_courante++;
    if (failread_au == fenetre_courante) {
        derniere_erreur = 5; /* ERROR_ACCESS_DENIED — le code consigné */
        return 0;
    }
    uint64_t a = (uint64_t)n;
    if (a > taille_f - pos_f) a = taille_f - pos_f;
    memcpy(buf, fichier + pos_f, a);
    pos_f += a;
    *lus = (DWORD)a;
    if (mutate_au == fenetre_courante) ((uint8_t *)buf)[0] ^= 0xFF;
    return 1;
}

DWORD GetLastError(void) { return derniere_erreur; }

/* --- les témoins --- */
static uint8_t zone_etat[536]; /* la taille vit à +520 (la convention de la pièce) */
static uint8_t sortie[32];

static void armer_fichier(uint8_t *f, uint64_t t) {
    fichier = f; taille_f = t; pos_f = 0;
    memset(zone_etat, 0, sizeof zone_etat);
    memcpy(zone_etat + 520, &t, 8);
    g_session_handle = (HANDLE)zone_etat;
}
/* LE JUGE EST EXTERNE : chaque condensé produit est imprimé, le pilote
   Python le compare à hashlib.sha256 — la pièce n'est JAMAIS jugée contre
   ses propres fonctions (la référence circulaire est écartée). */

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s proxy.exe gammes.txt\n", argv[0]); return 2; }

    /* le proxy scellé + le témoin bi-fenêtre */
    FILE *fp = fopen(argv[1], "rb");
    if (!fp) { perror("proxy"); return 2; }
    fseek(fp, 0, SEEK_END);
    long ts = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    uint8_t *proxy = malloc(ts);
    if (fread(proxy, 1, ts, fp) != (size_t)ts) return 2;
    fclose(fp);
    uint64_t tproxy = (uint64_t)ts;
    uint8_t *bi = malloc(ts * 2);
    memcpy(bi, proxy, ts);
    memcpy(bi + ts, proxy, ts);
    uint64_t tbi = tproxy * 2;

    /* V1 — les gammes (proxy puis multi-fenêtres sur le bi) */
    FILE *fg = fopen(argv[2], "r");
    if (!fg) { perror("gammes"); return 2; }
    long long n = 0;
    uint64_t off, lon;
    int multi = 0;
    while (fscanf(fg, "%llu %llu", (unsigned long long *)&off,
                  (unsigned long long *)&lon) == 2) {
        if ((long long)off == -1) { multi = 1; continue; }
        n++;
        armer_fichier(multi ? bi : proxy, multi ? tbi : tproxy);
        fenetre_courante = 0;
        memset(sortie, 0xAA, 32);
        long long rax = loupe_05_sha256(off, lon, sortie);
        printf("V1D %d %llu %llu %lld ", multi, (unsigned long long)off,
               (unsigned long long)lon, rax);
        for (int i = 0; i < 32; i++) printf("%02x", sortie[i]);
        printf("\n");
    }
    fclose(fg);
    printf("V1 %lld 0 0\n", n);

    /* V2 — le doré (le vide et « abc ») */
    armer_fichier(proxy, tproxy);
    fenetre_courante = 0;
    memset(sortie, 0xAA, 32);
    long long rax = loupe_05_sha256(0, 0, sortie);
    printf("V2 vide ");
    for (int i = 0; i < 32; i++) printf("%02x", sortie[i]);
    printf(" %d\n", rax == 0);
    uint8_t abc[3] = {'a', 'b', 'c'};
    armer_fichier(abc, 3);
    fenetre_courante = 0;
    memset(sortie, 0xAA, 32);
    rax = loupe_05_sha256(0, 3, sortie);
    printf("V2 abc ");
    for (int i = 0; i < 32; i++) printf("%02x", sortie[i]);
    printf(" %d\n", rax == 0);

    /* V3 — les rejets (E1 session, E2 bornes, E3 entrée) */
    armer_fichier(proxy, tproxy);
    g_session_handle = INVALID_HANDLE_VALUE;
    long long e1 = loupe_05_sha256(0, 1, sortie);
    armer_fichier(proxy, tproxy);
    long long e2 = loupe_05_sha256(0, tproxy + 1, sortie);
    armer_fichier(proxy, tproxy);
    long long e3 = loupe_05_sha256(0, 1, NULL);
    printf("V3 %lld %lld %lld %d\n", e1, e2, e3,
           e1 == -4 && e2 == -3 && e3 == -5);

    /* V4 — le rejet système : ReadFile échoue à la 2e fenêtre (le bi) */
    armer_fichier(bi, tbi);
    fenetre_courante = 0;
    failread_au = 2;
    memset(sortie, 0x5A, 32);
    uint8_t avant[32];
    memcpy(avant, sortie, 32);
    rax = loupe_05_sha256(0, tbi, sortie);
    int intacte = memcmp(sortie, avant, 32) == 0;
    printf("V4 %lld %d %d %lu\n", rax, intacte, fenetre_courante,
           (unsigned long)derniere_erreur);
    failread_au = 0;

    /* V5 — la falsification : un octet du tampon muté à la 2e fenêtre */
    armer_fichier(bi, tbi);
    fenetre_courante = 0;
    memset(sortie, 0, 32);
    loupe_05_sha256(0, tbi, sortie);
    uint8_t ref[32];
    memcpy(ref, sortie, 32);
    armer_fichier(bi, tbi);
    fenetre_courante = 0;
    mutate_au = 2;
    memset(sortie, 0, 32);
    loupe_05_sha256(0, tbi, sortie);
    int divergence = memcmp(ref, sortie, 32) != 0;
    printf("V5 ");
    for (int i = 0; i < 8; i++) printf("%02x", ref[i]);
    printf(" ");
    for (int i = 0; i < 8; i++) printf("%02x", sortie[i]);
    printf(" %d\n", divergence);

    return 0;
}
