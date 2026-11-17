/* dudect_v160.c — LE MESUREUR TEMPS RÉEL CONTRÔLÉ (fkkqc7v8t, la partie B2
 * du plan gelé — la cause racine du renversement N=200→N=400 fermée par le
 * PROTOCOLE, démontrée au laboratoire).
 *
 * LE CONSTAT DE SOURCE (dudect_v150.c, les lignes 396-419) — les TROIS
 * artefacts du protocole v150 que le renversement a exposés :
 *   1. L'ÉCHAUFFEMENT ASYMÉTRIQUE : 100 appels AVANT la classe fixe seule —
 *      la classe aléatoire court FROIDE (les dérivées intra-bloc constatées :
 *      Spearman ±0,67, la frontière fixe→aléatoire −728 cyc sur tls13-02) ;
 *   2. L'ORDRE BLOQUÉ : les DEUX classes en blocs — toute dérive temporelle
 *      (turbo, thermique) se COLLE à la classe (l'ANCOVA de tls13-13 :
 *      t classe seul +5,19 → contrôlé du rang −1,29 n.s. — la « dépendance »
 *      était la dérive) ;
 *   3. LE CHRONOMÈTRE NON SÉRIALISÉ : __rdtsc sans lfence — la lecture
 *      hors-ordre brouille la fenêtre ; et l'asymétrie d'état (rand_s
 *      SYSTÈME par itération aléatoire contre rien pour la fixe).
 *
 * LE PROTOCOLE v160 :
 *   · WARM-UP CONTRÔLÉ : W appels AVANT CHAQUE classe, les DEUX échauffées ;
 *   · AFFINITÉ : cœur fixé (SetThreadAffinityMask / sched_setaffinity),
 *     l'échec NOMMÉ dans le journal (jamais silencieux) ;
 *   · FRÉQUENCE : la lecture des gouverneurs (POSIX : /sys cpufreq ;
 *     Windows : les consignes powercfg au LISEZMOI — l'état EFFECTIF
 *     appartient au témoin du terrain) ;
 *   · ORDRE RANDOMISÉ : à CHAQUE itération la classe est tirée par PRNG À
 *     GRAINE CONSIGNÉE (l'entrelacement canonique dudect) ;
 *   · RUNS MULTIPLES : R runs indépendants par N, chaque run sa graine ;
 *   · LE CHRONOMÈTRE SÉRIALISÉ : lfence ; rdtsc ; lfence ;
 *   · LA SORTIE : le journal complet (run, graine, cible, classe, itération,
 *     cycles, secondes) + LE MÊME PIPELINE D'ANALYSE que la forensie
 *     (Welch + robustes + dérives — le script forensie_dudect le relit).
 *
 * LES DEUX BRAS :
 *   --controle   : le protocole v160 complet (la démonstration) ;
 *   --v150       : le bras TÉMOIN non contrôlé (l'ordre bloqué, l'échauffe
 *                  asymétrique, le chrono nu) — la CLASSE d'artefact du
 *                  renversement doit se REPRODUIRE au labo.
 *
 * LES DEUX BACKENDS du v150 CONSERVÉS : _WIN32 (le terrain du développeur)
 * et POSIX (la démonstration du laboratoire — étiquette « AUTOTEST
 * LABORATOIRE, AUCUN statut terrain », la discipline du v150 demeure).
 *
 * COMPILATION :  gcc -O2 -o dudect_v160 dudect_v160.c -lm
 * Usage : dudect_v160 [repertoire_cibles] [N] [R] [--controle|--v150]
 */

#ifndef _WIN32
#define _GNU_SOURCE
#else
#define _CRT_RAND_S
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#include <intrin.h>
static void alea(unsigned char *p, size_t n) {
    for (size_t i = 0; i < n; i++) { unsigned int v; rand_s(&v);
        p[i] = (unsigned char)v; }
}
static double horloge_sec(void) {
    LARGE_INTEGER f, c; QueryPerformanceFrequency(&f);
    QueryPerformanceCounter(&c);
    return (double)c.QuadPart / (double)f.QuadPart;
}
static int poser_affinite(int coeur) {
    return SetThreadAffinityMask(GetCurrentThread(),
                                 (DWORD_PTR)1 << coeur) != 0;
}
static uint64_t rdtscc(void) { return __rdtsc(); }
static const char *NOM_OS = "Windows (le run terrain)";
#else
#include <sched.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
static uint64_t graine_prng = 20261117;
static void alea(unsigned char *p, size_t n) {
    /* xorshift64* : le PRNG À GRAINE (l'ordre randomisé consigné) */
    for (size_t i = 0; i < n; i++) {
        graine_prng ^= graine_prng >> 12;
        graine_prng ^= graine_prng << 25;
        graine_prng ^= graine_prng >> 27;
        p[i] = (unsigned char)((graine_prng * 0x2545F4914F6CDD1DULL) >>
                               56);
    }
}
static double horloge_sec(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}
static int poser_affinite(int coeur) {
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(coeur, &m);
    return sched_setaffinity(0, sizeof(m), &m) == 0;
}
static inline void lfence(void) { __asm__ volatile("lfence"); }
static uint64_t rdtscc(void) {
    unsigned int a, d;
    lfence();
    __asm__ volatile ("rdtsc" : "=a"(a), "=d"(d));
    lfence();
    return ((uint64_t)d << 32) | a;
}
static const char *NOM_OS = "POSIX (la démonstration du laboratoire)";
#endif

#if defined(__GNUC__) && !defined(_WIN32)
#define MSABI __attribute__((ms_abi))
#else
#define MSABI
#endif

/* ---- SHA-256 (le recoup du mesureur, inchangé du v150) ---- */
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
static uint32_t ror32(uint32_t x, int n) { return (x>>n)|(x<<(32-n)); }
static void sha256(const unsigned char *d, size_t n, unsigned char o[32]) {
    uint32_t h[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                     0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    size_t reste = n % 64;
    size_t nb = n/64 + 1;
    if (reste >= 56) nb++;
    unsigned char *t = (unsigned char*)calloc(nb, 64);
    if (!t) { fprintf(stderr, "[REFUS] memoire\n"); exit(2); }
    memcpy(t, d, n);
    t[n] = 0x80;
    uint64_t bits = (uint64_t)n * 8;
    for (int i = 0; i < 8; i++)
        t[nb*64-1-i] = (unsigned char)(bits >> (8*i));
    for (size_t b = 0; b < nb; b++) {
        uint32_t w[64];
        for (int i = 0; i < 16; i++)
            w[i] = ((uint32_t)t[b*64+4*i] << 24) |
                   ((uint32_t)t[b*64+4*i+1] << 16) |
                   ((uint32_t)t[b*64+4*i+2] << 8) |
                   (uint32_t)t[b*64+4*i+3];
        for (int i = 16; i < 64; i++) {
            uint32_t s0 = ror32(w[i-15],7) ^ ror32(w[i-15],18) ^
                          (w[i-15] >> 3);
            uint32_t s1 = ror32(w[i-2],17) ^ ror32(w[i-2],19) ^
                          (w[i-2] >> 10);
            w[i] = w[i-16] + s0 + w[i-7] + s1;
        }
        uint32_t a=h[0],bb=h[1],c=h[2],dd=h[3],e=h[4],f=h[5],g=h[6],hh=h[7];
        for (int i = 0; i < 64; i++) {
            uint32_t S1 = ror32(e,6) ^ ror32(e,11) ^ ror32(e,25);
            uint32_t ch = (e & f) ^ ((~e) & g);
            uint32_t t1 = hh + S1 + ch + K256[i] + w[i];
            uint32_t S0 = ror32(a,2) ^ ror32(a,13) ^ ror32(a,22);
            uint32_t mj = (a & bb) ^ (a & c) ^ (bb & c);
            uint32_t t2 = S0 + mj;
            hh=g; g=f; f=e; e=dd+t1; dd=c; c=bb; bb=a; a=t1+t2;
        }
        h[0]+=a; h[1]+=bb; h[2]+=c; h[3]+=dd;
        h[4]+=e; h[5]+=f; h[6]+=g; h[7]+=hh;
    }
    for (int i = 0; i < 8; i++) {
        o[4*i] = (unsigned char)(h[i] >> 24);
        o[4*i+1] = (unsigned char)(h[i] >> 16);
        o[4*i+2] = (unsigned char)(h[i] >> 8);
        o[4*i+3] = (unsigned char)h[i];
    }
    free(t);
}

/* ---- les cibles (le manifeste du kit-2, inchangé) ---- */
typedef struct { char nom[16]; size_t rva, taille;
                 unsigned char sha_plage[32]; int famille; } cible_t;
enum { F_SHA, F_X25519, F_AES, F_GHASH };
typedef void (MSABI *f_sha256_t)(void *, void *);
typedef void (MSABI *f_x25519_t)(void *, void *, void *);
typedef void (MSABI *f_aes128_t)(void *, void *, void *);
typedef void (MSABI *f_ghash_t)(void *, void *, void *);

static void hex_vers(const char *hx, unsigned char *o, int n) {
    char t[3] = {0,0,0};
    for (int i = 0; i < n; i++) {
        t[0] = hx[2*i]; t[1] = hx[2*i+1];
        o[i] = (unsigned char)strtoul(t, NULL, 16);
    }
}

static int lire_manifeste(const char *rep, char sha_image[65],
                          size_t *taille_image, cible_t *tab, int max) {
    char chemin[512];
    snprintf(chemin, sizeof chemin, "%s/manifeste-c.txt", rep);
    FILE *f = fopen(chemin, "r");
    if (!f) { fprintf(stderr, "[REFUS] manifeste introuvable : %s\n",
                      chemin); return -1; }
    char ligne[512]; int n = 0; char sha[65];
    while (fgets(ligne, sizeof ligne, f)) {
        if (sscanf(ligne, "image %64s", sha) == 1)
            memcpy(sha_image, sha, 65);
        else if (sscanf(ligne, "taille %zu", taille_image) == 1) { }
        else if (sscanf(ligne, "cible %15s %zu %zu %64s",
                        tab[n].nom, &tab[n].rva, &tab[n].taille, sha) == 4) {
            hex_vers(sha, tab[n].sha_plage, 32);
            if (strncmp(tab[n].nom, "tls13-02", 8) == 0)
                tab[n].famille = F_SHA;
            else if (strncmp(tab[n].nom, "tls13-13", 8) == 0)
                tab[n].famille = F_X25519;
            else if (strncmp(tab[n].nom, "tls13-16", 8) == 0)
                tab[n].famille = F_AES;
            else if (strncmp(tab[n].nom, "tls13-17", 8) == 0)
                tab[n].famille = F_GHASH;
            else tab[n].famille = -1;
            if (++n >= max) break;
        }
    }
    fclose(f);
    return n;
}

static void appeler(int famille, void *fn, unsigned char *secret,
                    unsigned char *aux, unsigned char *sortie) {
    switch (famille) {
    case F_SHA: {
        uint32_t etat[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,
                            0xa54ff53a,0x510e527f,0x9b05688c,
                            0x1f83d9ab,0x5be0cd19};
        ((f_sha256_t)fn)(etat, secret); break; }
    case F_X25519:
        ((f_x25519_t)fn)(sortie, secret, aux); break;
    case F_AES:
        ((f_aes128_t)fn)(secret, aux, sortie); break;
    case F_GHASH:
        ((f_ghash_t)fn)(sortie, secret, aux); break;
    }
}

/* le PRNG d'ordre (le tirage de classe consigné) */
static uint64_t prng_ordre;
static uint64_t prng_suivant(void) {
    prng_ordre ^= prng_ordre >> 12;
    prng_ordre ^= prng_ordre << 25;
    prng_ordre ^= prng_ordre >> 27;
    return prng_ordre * 0x2545F4914F6CDD1DULL;
}

static double moy(const uint64_t *x, size_t n) {
    double s = 0; for (size_t i = 0; i < n; i++) s += (double)x[i];
    return s / (double)n;
}
static double var(const uint64_t *x, size_t n, double m) {
    double s = 0; for (size_t i = 0; i < n; i++) {
        double d = (double)x[i] - m; s += d * d; }
    return n > 1 ? s / (double)(n - 1) : 0.0;
}
static double t_welch(const uint64_t *a, size_t na,
                      const uint64_t *b, size_t nb) {
    double ma = moy(a, na), mb = moy(b, nb);
    double va = var(a, na, ma) / (double)na;
    double vb = var(b, nb, mb) / (double)nb;
    double den = sqrt(va + vb);
    return den > 0 ? (ma - mb) / den : 0.0;
}

#define NMAX 4096
#define W_ECHAUFFE 200

int main(int argc, char **argv) {
    const char *rep = "cibles";
    size_t n = 200;
    int runs = 5;
    int controle = 1;               /* défaut : le protocole contrôlé */
    int args_pos = 0;
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--controle") == 0) controle = 1;
        else if (strcmp(argv[i], "--v150") == 0) controle = 0;
        else if (args_pos == 0) { rep = argv[i]; args_pos++; }
        else if (args_pos == 1) {
            n = (size_t)strtoul(argv[i], NULL, 10); args_pos++; }
        else if (args_pos == 2) {
            runs = (int)strtol(argv[i], NULL, 10); args_pos++; }
    }
    if (n < 60) n = 60;
    if (n > NMAX) n = NMAX;
    if (runs < 1) runs = 1;
    if (runs > 10) runs = 10;

    printf("=== dudect_v160 — le mesureur TEMPS RÉEL CONTRÔLÉ "
           "(fkkqc7v8t, B2) ===\n");
    printf("[config] OS=%s  N=%zu/classe  R=%d run(s)  seuil |t|>5  "
           "bras=%s\n", NOM_OS, n, runs,
           controle ? "CONTRÔLE (warm-up des deux classes, ordre "
                      "randomisé à graine, lfence-rdtsc-lfence)"
                    : "TÉMOIN v150 (l'ordre bloqué, l'échauffe "
                      "asymétrique, le chrono nu)");
    printf("[étiquette] %s\n", controle ?
           "la démonstration du protocole — le statut TERRAIN "
           "appartient au run signé du développeur" :
           "le bras TÉMOIN — la reproduction VOLONTAIRE de la classe "
           "d'artefact du renversement");
    if (poser_affinite(0))
        printf("[affinité] cœur 0 : posée\n");
    else
        printf("[affinité] REFUSÉE — le run demeure, l'écart est NOMMÉ "
               "(consignez-le)\n");
#ifndef _WIN32
    /* la lecture des gouverneurs (le bac peut ne rien exposer — gap nommé) */
    FILE *g = fopen("/sys/devices/system/cpu/cpu0/cpufreq/"
                    "scaling_governor", "r");
    if (g) { char gov[64]; if (fscanf(g, "%63s", gov) == 1)
        printf("[fréquence] le gouverneur cpu0 : %s\n", gov);
        fclose(g); }
    else
        printf("[fréquence] /sys cpufreq NON EXPOSÉ par le bac — le contrôle"
               " EFFECTIF appartient au terrain (powercfg, le LISEZMOI)\n");
#endif

    char sha_image[65] = "";
    size_t taille_image = 0;
    cible_t cibles[8];
    int nb = lire_manifeste(rep, sha_image, &taille_image, cibles, 8);
    if (nb <= 0 || !sha_image[0] || !taille_image) return 2;

    char chemin[512];
    snprintf(chemin, sizeof chemin, "%s/proxy-image.bin", rep);
    FILE *f = fopen(chemin, "rb");
    if (!f) { perror(chemin); return 2; }
    unsigned char *brut = (unsigned char *)malloc(taille_image);
    if (fread(brut, 1, taille_image, f) != taille_image) {
        fprintf(stderr, "[REFUS] image tronquée\n"); return 2; }
    fclose(f);
    unsigned char calcule[32], attendu[32];
    sha256(brut, taille_image, calcule);
    hex_vers(sha_image, attendu, 32);
    if (memcmp(calcule, attendu, 32) != 0) {
        fprintf(stderr, "[REFUS] sha256 de l'IMAGE divergent — RIEN "
                "n'est exécuté\n"); return 2; }
    printf("[image] sha256 recoupé — la pièce scellée\n");

    void *image = NULL;
#ifdef _WIN32
    image = VirtualAlloc(NULL, (SIZE_T)taille_image, MEM_COMMIT,
                         PAGE_READWRITE);
    if (image) { memcpy(image, brut, taille_image);
        DWORD old;
        if (!VirtualProtect(image, (SIZE_T)taille_image,
                            PAGE_EXECUTE_READ, &old)) image = NULL; }
#else
    size_t garde = (taille_image + 4095) & ~4095UL;
    image = mmap(NULL, garde, PROT_READ|PROT_WRITE|PROT_EXEC,
                 MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    if (image == MAP_FAILED) image = NULL;
    else memcpy(image, brut, taille_image);
#endif
    free(brut);
    if (!image) { fprintf(stderr, "[REFUS] mmap/VirtualAlloc\n"); return 2; }

    char nom_csv[256];
    snprintf(nom_csv, sizeof nom_csv, "journal-dudect-v160-%s-%ld.csv",
             controle ? "controle" : "v150", (long)time(NULL));
    FILE *csv = fopen(nom_csv, "w");
    if (!csv) { perror("fopen"); return 2; }
    fprintf(csv, "run,graine,cible,classe,iteration,cycles,secondes\n");

    for (int r = 0; r < runs; r++) {
        uint64_t graine_run = 20261117 + 1000 * (uint64_t)r;
        prng_ordre = graine_run;
        graine_prng = graine_run ^ 0x9e3779b97f4a7c15ULL;
        printf("--- run %d/%d (graine %llu) ---\n", r + 1, runs,
               (unsigned long long)graine_run);
        for (int k = 0; k < nb; k++) {
            if (cibles[k].famille < 0) continue;
            sha256((unsigned char *)image + cibles[k].rva, cibles[k].taille,
                   calcule);
            if (memcmp(calcule, cibles[k].sha_plage, 32) != 0) {
                fprintf(stderr, "[REFUS] %s : sha256 de la PLAGE divergent"
                        " — RIEN n'est exécuté\n", cibles[k].nom);
                return 2;
            }
            void *fn = (char *)image + cibles[k].rva;

            unsigned char secret_fixe[256], secret[256], aux[64], sortie[64];
            alea(secret_fixe, sizeof secret_fixe);
            memcpy(secret, secret_fixe, sizeof secret);
            alea(aux, sizeof aux);

            uint64_t cyc_f[NMAX], cyc_a[NMAX];
            double sec_f[NMAX], sec_a[NMAX];
            size_t nf = 0, na_ = 0;

            if (controle) {
                /* LE PROTOCOLE CONTRÔLÉ : warm-up des DEUX classes (les
                 * DEUX secrets échauffés), puis l'ordre RANDOMISÉ par
                 * itération (la classe tirée au PRNG à graine) */
                for (int i = 0; i < W_ECHAUFFE; i++) {
                    appeler(cibles[k].famille, fn, secret_fixe, aux, sortie);
                    alea(secret, sizeof secret);
                    appeler(cibles[k].famille, fn, secret, aux, sortie);
                }
                memcpy(secret, secret_fixe, sizeof secret);
                for (size_t i = 0; i < 2 * n; i++) {
                    int classe_aleatoire =
                        (int)(prng_suivant() & 1ULL);
                    if (classe_aleatoire) alea(secret, sizeof secret);
                    double t0s = horloge_sec();
                    uint64_t t0 = rdtscc();
                    appeler(cibles[k].famille, fn, secret, aux, sortie);
                    uint64_t t1 = rdtscc();
                    double t1s = horloge_sec();
                    if (classe_aleatoire) {
                        cyc_a[na_] = t1 - t0; sec_a[na_] = t1s - t0s;
                        fprintf(csv, "%d,%llu,%s,aleatoire,%zu,%llu,%.9f\n",
                                r, (unsigned long long)graine_run,
                                cibles[k].nom, na_,
                                (unsigned long long)(t1 - t0), t1s - t0s);
                        na_++;
                    } else {
                        cyc_f[nf] = t1 - t0; sec_f[nf] = t1s - t0s;
                        fprintf(csv, "%d,%llu,%s,fixe,%zu,%llu,%.9f\n",
                                r, (unsigned long long)graine_run,
                                cibles[k].nom, nf,
                                (unsigned long long)(t1 - t0), t1s - t0s);
                        nf++;
                    }
                    memcpy(secret, secret_fixe, sizeof secret);
                }
            } else {
                /* LE BRAS TÉMOIN v150 : l'échauffement AVANT la fixe
                 * seule, l'ordre BLOQUÉ, le chrono NU (sans lfence) */
                for (int i = 0; i < 100; i++)
                    appeler(cibles[k].famille, fn, secret, aux, sortie);
                for (size_t i = 0; i < n; i++) {
                    double t0s = horloge_sec();
                    uint64_t t0 = rdtscc();
                    appeler(cibles[k].famille, fn, secret_fixe, aux, sortie);
                    uint64_t t1 = rdtscc();
                    double t1s = horloge_sec();
                    cyc_f[nf] = t1 - t0; sec_f[nf] = t1s - t0s;
                    fprintf(csv, "%d,%llu,%s,fixe,%zu,%llu,%.9f\n",
                            r, (unsigned long long)graine_run,
                            cibles[k].nom, i,
                            (unsigned long long)(t1 - t0), t1s - t0s);
                    nf++;
                }
                for (size_t i = 0; i < n; i++) {
                    alea(secret, sizeof secret);
                    double t0s = horloge_sec();
                    uint64_t t0 = rdtscc();
                    appeler(cibles[k].famille, fn, secret, aux, sortie);
                    uint64_t t1 = rdtscc();
                    double t1s = horloge_sec();
                    cyc_a[na_] = t1 - t0; sec_a[na_] = t1s - t0s;
                    fprintf(csv, "%d,%llu,%s,aleatoire,%zu,%llu,%.9f\n",
                            r, (unsigned long long)graine_run,
                            cibles[k].nom, i,
                            (unsigned long long)(t1 - t0), t1s - t0s);
                    na_++;
                }
            }
            double tw = t_welch(cyc_f, nf, cyc_a, na_);
            printf("  [%s] fixe moy %.1f cyc (n=%zu) | aleatoire moy %.1f "
                   "(n=%zu) | t de Welch = %+.2f -> %s\n", cibles[k].nom,
                   moy(cyc_f, nf), nf, moy(cyc_a, na_), na_, tw,
                   fabs(tw) > 5.0 ?
                   "DIVERGENCE (à consigner telle quelle)" :
                   "aucune divergence au seuil");
        }
    }
    fclose(csv);
    printf("[sortie] %s — l'analyse par forensie_dudect (le pipeline "
           "unique : Welch + robustes + dérives)\n", nom_csv);
    return 0;
}
