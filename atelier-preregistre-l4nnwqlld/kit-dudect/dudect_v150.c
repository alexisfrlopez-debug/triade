/* dudect_v150.c — LE MESUREUR TEMPS RÉEL DU KIT 1 (v0.15.0)
 *
 * La commande (ic09ydeli, point 2) : « kit dudect temps réel pour les
 * familles crypto sur la machine Windows du développeur (RDTSC/QPC,
 * affinité cœur, turbo désactivé si possible, protocole consigné) ».
 *
 * LE MÉCANISME (éprouvé au laboratoire par test_appel.c : le condensé
 * FIPS « abc » EXACT depuis la pièce scellée) :
 *   1. il charge L'IMAGE MÉMOIRE ÉTENDUE de la pièce scellée
 *      (cibles/proxy-image.bin — les blocs ne sont PAS autonomes :
 *      tls13-02 lit sa table K en .rdata par RIP-relatif ; l'image est
 *      la découpe honnête, chaque section posée à son RVA) ;
 *   2. il RECOUPE le sha256 de l'image ET de chaque plage de cible
 *      contre le manifeste (cibles/manifeste-c.txt, la source unique
 *      posée par l'extracteur) AVANT toute exécution — le mesureur ne
 *      fait confiance à personne, pas même à l'extracteur ;
 *   3. il pose l'affinité sur UN cœur, échauffe 100 appels, mesure
 *      N ≥ 60 itérations par classe (secret-fixe / secret-aléatoire)
 *      en cycles RDTSC et en secondes (QPC / CLOCK_MONOTONIC) ;
 *   4. il calcule le t de Welch et tranche au seuil |t| > 5 (les mêmes
 *      paramètres que l'édition structurelle v0.11.0 — la métrique
 *      change : le temps d'HORLOGE réel, pas le compte d'instructions) ;
 *   5. il écrit journal-dudect-<horodatage>.csv + le résumé (à recopier
 *      dans temoin-dudect.txt avec la config CPU, l'état EFFECTIF du
 *      turbo, l'OS — le run TERRAIN appartient au développeur).
 *
 * LES DEUX BACKENDS : _WIN32 (QueryPerformanceCounter,
 * SetThreadAffinityMask, rand_s — LE RUN TERRAIN) et POSIX
 * (CLOCK_MONOTONIC, sched_setaffinity, /dev/urandom — L'AUTOTEST DU
 * LABORATOIRE : le mécanisme seul, AUCUN statut terrain n'en découle).
 * Les blocs sont en convention Windows x64 : pointeurs ms_abi (GCC).
 *
 * COMPILATION (le développeur, sur sa machine Windows) :
 *   cl /O2 dudect_v150.c
 *   gcc -O2 -o dudect_v150.exe dudect_v150.c -lm
 * AU LABORATOIRE (l'autotest, Linux) :
 *   gcc -O2 -o dudect_v150 dudect_v150.c -lm
 *
 * LE CORRECTIF n° 1 DU KIT (12/11/2026, la préparation multimachines) :
 *   _CRT_RAND_S posé AVANT stdlib.h — sans lui rand_s n'est PAS déclaré
 *   (ni MSVC ni mingw-w64 ne le déclarent par défaut) : le défaut latent
 *   que l'autotest POSIX du laboratoire ne pouvait pas toucher, découvert
 *   à la cross-compilation Windows du kit. Le backend POSIX est INCHANGÉ
 *   (octet pour octet à l'exécution — l'autotest re-éprouvé après le geste).
 *
 * Usage : dudect_v150 [repertoire_cibles] [N_par_classe] [--autotest]
 *         (défauts : cibles, 200)
 */

#ifndef _WIN32
#define _GNU_SOURCE
#else
#define _CRT_RAND_S   /* rand_s : requis avant stdlib.h (MSVC et mingw-w64) */
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
static const char *NOM_OS = "Windows (le run terrain)";
#else
#include <sched.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
static void alea(unsigned char *p, size_t n) {
    static int fd = -1;
    if (fd < 0) fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0 || (size_t)read(fd, p, n) != n) {
        fprintf(stderr, "[REFUS] /dev/urandom\n"); exit(2); }
}
static double horloge_sec(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}
static int poser_affinite(int coeur) {
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(coeur, &m);
    return sched_setaffinity(0, sizeof(m), &m) == 0;
}
static const char *NOM_OS = "POSIX (autotest laboratoire)";
#endif

#if defined(__GNUC__) && !defined(_WIN32)
#define MSABI __attribute__((ms_abi))
#else
#define MSABI
#endif

/* ---- SHA-256 (le recoup du mesureur) ---- */
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
        t[nb*64 - 1 - i] = (unsigned char)((bits >> (8*i)) & 0xff);
    for (size_t b = 0; b < nb; b++) {
        uint32_t w[64];
        for (int i = 0; i < 16; i++) {
            const unsigned char *p = t + b*64 + 4*i;
            w[i] = ((uint32_t)p[0]<<24)|((uint32_t)p[1]<<16)
                 |((uint32_t)p[2]<<8)|(uint32_t)p[3];
        }
        for (int i = 16; i < 64; i++) {
            uint32_t s0 = ror32(w[i-15],7)^ror32(w[i-15],18)^(w[i-15]>>3);
            uint32_t s1 = ror32(w[i-2],17)^ror32(w[i-2],19)^(w[i-2]>>10);
            w[i] = w[i-16]+s0+w[i-7]+s1;
        }
        uint32_t a=h[0],bb=h[1],c=h[2],dd=h[3],e=h[4],f=h[5],g=h[6],hh=h[7];
        for (int i = 0; i < 64; i++) {
            uint32_t S1 = ror32(e,6)^ror32(e,11)^ror32(e,25);
            uint32_t ch = (e&f)^((~e)&g);
            uint32_t t1 = hh+S1+ch+K256[i]+w[i];
            uint32_t S0 = ror32(a,2)^ror32(a,13)^ror32(a,22);
            uint32_t mj = (a&bb)^(a&c)^(bb&c);
            uint32_t t2 = S0+mj;
            hh=g; g=f; f=e; e=dd+t1; dd=c; c=bb; bb=a; a=t1+t2;
        }
        h[0]+=a; h[1]+=bb; h[2]+=c; h[3]+=dd;
        h[4]+=e; h[5]+=f; h[6]+=g; h[7]+=hh;
    }
    free(t);
    for (int i = 0; i < 8; i++) {
        o[4*i]=(unsigned char)(h[i]>>24); o[4*i+1]=(unsigned char)(h[i]>>16);
        o[4*i+2]=(unsigned char)(h[i]>>8); o[4*i+3]=(unsigned char)h[i];
    }
}

/* ---- les contrats de couche I (la convention Windows x64) ---- */
typedef void (MSABI *f_sha256_t)(uint32_t *etat8, const unsigned char *b64);
typedef void (MSABI *f_x25519_t)(unsigned char *s32,
                                 const unsigned char *scalaire32,
                                 const unsigned char *u32_);
typedef void (MSABI *f_aes128_t)(const unsigned char *cles176,
                                 const unsigned char *entree16,
                                 unsigned char *sortie16);
typedef void (MSABI *f_ghash_t)(unsigned char *z16,
                                const unsigned char *x16,
                                const unsigned char *y16);
enum { F_SHA, F_X25519, F_AES, F_GHASH };

typedef struct {
    char nom[16]; unsigned char sha_plage[32];
    size_t rva, taille; int famille;
} cible_t;

static void hex_vers(const char *hx, unsigned char *o, int n) {
    char t[3] = {0,0,0};
    for (int i = 0; i < n; i++) {
        t[0] = hx[2*i]; t[1] = hx[2*i+1];
        o[i] = (unsigned char)strtoul(t, NULL, 16);
    }
}

/* le manifeste simple : "image <sha>", "taille <n>",
 * "cible <nom> <rva> <taille> <sha_plage>" */
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

/* ---- la mesure ---- */
static uint64_t rdtscc(void) {
#ifdef _WIN32
    return __rdtsc();
#else
    unsigned int a, d;
    __asm__ volatile ("rdtsc" : "=a"(a), "=d"(d));
    return ((uint64_t)d << 32) | a;
#endif
}

#define NMAX 4096
typedef struct { uint64_t cyc[NMAX]; double sec[NMAX]; size_t n; } serie_t;

static double moy(const uint64_t *x, size_t n) {
    double s = 0; for (size_t i = 0; i < n; i++) s += (double)x[i];
    return s / (double)n;
}
static double var(const uint64_t *x, size_t n, double m) {
    double s = 0; for (size_t i = 0; i < n; i++) {
        double d = (double)x[i] - m; s += d * d; }
    return n > 1 ? s / (double)(n - 1) : 0.0;
}
static double t_welch(const serie_t *a, const serie_t *b) {
    double ma = moy(a->cyc, a->n), mb = moy(b->cyc, b->n);
    double va = var(a->cyc, a->n, ma) / (double)a->n;
    double vb = var(b->cyc, b->n, mb) / (double)b->n;
    double den = sqrt(va + vb);
    return den > 0 ? (ma - mb) / den : 0.0;
}
static uint64_t mediane(uint64_t *x, size_t n) {
    for (size_t i = 1; i < n; i++) { uint64_t k = x[i]; size_t j = i;
        while (j > 0 && x[j-1] > k) { x[j] = x[j-1]; j--; }
        x[j] = k; }
    return x[n/2];
}

static void appeler(int famille, void *fn, unsigned char *secret,
                    unsigned char *aux, unsigned char *sortie) {
    switch (famille) {
    case F_SHA: {   /* tls13-02 : etat(8 u32) AMONT, bloc 64 = LE SECRET */
        uint32_t etat[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,
                            0xa54ff53a,0x510e527f,0x9b05688c,
                            0x1f83d9ab,0x5be0cd19};
        ((f_sha256_t)fn)(etat, secret);
        break; }
    case F_X25519:  /* tls13-13 : sortie, scalaire = LE SECRET, u */
        ((f_x25519_t)fn)(sortie, secret, aux); break;
    case F_AES:     /* tls13-16 : cles = LE SECRET, entree, sortie */
        ((f_aes128_t)fn)(secret, aux, sortie); break;
    case F_GHASH:   /* tls13-17 : Z, X = LE SECRET, Y */
        ((f_ghash_t)fn)(sortie, secret, aux); break;
    }
}

int main(int argc, char **argv) {
    const char *rep = "cibles";
    size_t n = 200;
    int autotest = 0;
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--autotest") == 0) autotest = 1;
        else if (i == 1) rep = argv[i];
        else if (i == 2) n = (size_t)strtoul(argv[i], NULL, 10);
    }
    if (n < 60) n = 60;             /* la commande : N >= 60 par classe */
    if (n > NMAX) n = NMAX;

    printf("=== dudect_v150 - le mesureur temps reel (kit 1, v0.15.0) ===\n");
    printf("[config] OS=%s  N=%zu/classe  seuil |t|>5\n", NOM_OS, n);
    if (autotest)
        printf("[ETIQUETTE] AUTOTEST LABORATOIRE - le mecanisme seul : "
               "AUCUN statut terrain n'en decoule (le run materiel "
               "appartient au developpeur)\n");
    printf("[affinite] coeur 0 : %s\n", poser_affinite(0) ? "posee" :
           "REFUSEE (le t sera bruite - consignez-le)");

    char sha_image[65] = "";
    size_t taille_image = 0;
    cible_t cibles[8];
    int nb = lire_manifeste(rep, sha_image, &taille_image, cibles, 8);
    if (nb <= 0 || !sha_image[0] || !taille_image) return 2;
    printf("[manifeste] image %ld octets, %d cible(s)\n",
           (long)taille_image, nb);

    /* l'image étendue : chargée, recoupée, mappée exécutable */
    char chemin[512];
    snprintf(chemin, sizeof chemin, "%s/proxy-image.bin", rep);
    FILE *f = fopen(chemin, "rb");
    if (!f) { perror(chemin); return 2; }
    unsigned char *brut = (unsigned char *)malloc(taille_image);
    if (fread(brut, 1, taille_image, f) != taille_image) {
        fprintf(stderr, "[REFUS] image tronquee\n"); return 2; }
    fclose(f);
    unsigned char calcule[32];
    sha256(brut, taille_image, calcule);
    unsigned char attendu[32]; hex_vers(sha_image, attendu, 32);
    if (memcmp(calcule, attendu, 32) != 0) {
        fprintf(stderr, "[REFUS] sha256 de l'IMAGE divergent - ce n'est "
                "PAS la piece scellee, RIEN n'est execute\n");
        return 2;
    }
    printf("[image] sha256 recoupe - la piece scellee\n");

    void *image = NULL;
#ifdef _WIN32
    image = VirtualAlloc(NULL, (SIZE_T)taille_image, MEM_COMMIT,
                         PAGE_READWRITE);
    if (image) { memcpy(image, brut, taille_image);
        DWORD old; VirtualProtect(image, (SIZE_T)taille_image,
                                  PAGE_EXECUTE_READ, &old); }
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
    snprintf(nom_csv, sizeof nom_csv, "journal-dudect-%ld.csv",
             (long)time(NULL));
    FILE *csv = fopen(nom_csv, "w");
    if (!csv) { perror("fopen"); return 2; }
    fprintf(csv, "cible,classe,iteration,cycles,secondes\n");

    int echecs = 0;
    for (int k = 0; k < nb; k++) {
        if (cibles[k].famille < 0) continue;
        /* le recoup PAR CIBLE : la plage de l'image mappée */
        sha256((unsigned char *)image + cibles[k].rva, cibles[k].taille,
               calcule);
        if (memcmp(calcule, cibles[k].sha_plage, 32) != 0) {
            fprintf(stderr, "[REFUS] %s : sha256 de la PLAGE divergent - "
                    "RIEN n'est execute\n", cibles[k].nom);
            echecs++; continue;
        }
        void *fn = (char *)image + cibles[k].rva;
        printf("[%s] plage recoupee (RVA %zu, %zu o) - la piece scellee\n",
               cibles[k].nom, cibles[k].rva, cibles[k].taille);

        unsigned char secret_fixe[256], secret[256], aux[64], sortie[64];
        alea(secret_fixe, sizeof secret_fixe);
        memcpy(secret, secret_fixe, sizeof secret);
        alea(aux, sizeof aux);
        for (int i = 0; i < 100; i++)      /* l'échauffement */
            appeler(cibles[k].famille, fn, secret, aux, sortie);

        serie_t fixe, alea_s;
        fixe.n = alea_s.n = 0;
        for (size_t i = 0; i < n; i++) {   /* la classe FIXE */
            double t0s = horloge_sec(); uint64_t t0 = rdtscc();
            appeler(cibles[k].famille, fn, secret_fixe, aux, sortie);
            uint64_t t1 = rdtscc(); double t1s = horloge_sec();
            fixe.cyc[fixe.n] = t1 - t0; fixe.sec[fixe.n] = t1s - t0s;
            fixe.n++;
            fprintf(csv, "%s,fixe,%zu,%llu,%.9f\n", cibles[k].nom, i,
                    (unsigned long long)(t1 - t0), t1s - t0s);
        }
        for (size_t i = 0; i < n; i++) {   /* la classe ALÉATOIRE */
            alea(secret, sizeof secret);
            double t0s = horloge_sec(); uint64_t t0 = rdtscc();
            appeler(cibles[k].famille, fn, secret, aux, sortie);
            uint64_t t1 = rdtscc(); double t1s = horloge_sec();
            alea_s.cyc[alea_s.n] = t1 - t0; alea_s.sec[alea_s.n] = t1s - t0s;
            alea_s.n++;
            fprintf(csv, "%s,aleatoire,%zu,%llu,%.9f\n", cibles[k].nom, i,
                    (unsigned long long)(t1 - t0), t1s - t0s);
        }
        double tw = t_welch(&fixe, &alea_s);
        uint64_t fc[64], ac[64];
        size_t m = n < 64 ? n : 64;
        memcpy(fc, fixe.cyc, m * sizeof(uint64_t));
        memcpy(ac, alea_s.cyc, m * sizeof(uint64_t));
        printf("  fixe      : moy %.1f cyc, med %llu\n",
               moy(fixe.cyc, fixe.n),
               (unsigned long long)mediane(fc, m));
        printf("  aleatoire : moy %.1f cyc, med %llu\n",
               moy(alea_s.cyc, alea_s.n),
               (unsigned long long)mediane(ac, m));
        printf("  t de Welch = %.2f -> %s (seuil |t| > 5)\n", tw,
               fabs(tw) > 5.0 ?
               "DIVERGENCE TEMPORELLE (a consigner telle quelle)" :
               "AUCUNE divergence au seuil");
    }
    fclose(csv);
    printf("[sortie] %s - joignez-le a temoin-dudect.txt avec la config "
           "CPU, l'etat EFFECTIF du turbo et l'OS\n", nom_csv);
    return echecs ? 2 : 0;
}
