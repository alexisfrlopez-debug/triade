/* dudect_apple.c — LE TESTEUR DU SILICIUM APPLE (edition APPLE-SILICON, v1.0.0)
 *
 * La commande (le developpeur, 25/11/2026) : « si tu as des idees pour des
 * siliciums supplementaires du meme type que google collab (environnement
 * gratuit en ligne, mais hardware different) fais moi les packs de test
 * correspondants ». LE SILICIUM APPLE (la famille M,
 * ARM64, FEAT_SHA256) vit GRATUITEMENT en ligne sur les runners macOS des
 * GitHub Actions (depot public) : UNE AUTRE famille que le Cortex du
 * telephone, UNE AUTRE que le Neoverse des serveurs ARM, UNE AUTRE que les
 * Xeon/EPYC — le run y vivra comme LECTURE DE COMMODITE, jamais comme
 * preuve (la hierarchie demeure : le banc controle est la reference).
 *
 * CE QUE CE KIT EST, HONNETEMENT :
 *   — derive NOMME de dudect_arm.c (edition TELEPHONE, v1.0.0, le kit-B) :
 *     la mecanique (alea, controles, compression, FIPS, Welch, csv) est la
 *     MEME, la piece est recompilee SUR PLACE depuis CETTE source ; les
 *     ecarts nommes du portage : (1) l'AFFINITE — sched_setaffinity est un
 *     geste Linux, sur macOS il est REFUSE par nature et NOMME (le t sera
 *     bruite, constate tel quel) ; (2) le CANAL /proc/cpuinfo N'EXISTE PAS
 *     sur macOS — la garde noyau du kit-B ne peut pas s'y exprimer :
 *     L'EPREUVE FIPS DECIDE SEULE (fail-closed), jamais muet ; (3)
 *     l'identite du silicium vit au sysctl nomme par le scenario, pas au
 *     /proc ;
 *   — le protocole APPLE-ARM-1, NOUVEAU, PRE-ENREGISTRE dans le
 *     LISEZMOI-dudect-apple.txt de ce kit AVANT tout run : l'equation
 *     (echauffement, LOT, N, classes, statistique, seuil) est L'EGALATION
 *     du TELEPHONE-ARM-1, re-enregistree pour CE silicium ;
 *   — HORS PERIMETRE SCELLE v0.15.0 : les pieces scellees (loupe.exe,
 *     proxy-image.bin, moteur-shani.bin) sont x86-64 Windows ; CE silicium
 *     ARM64 ne les execute PAS. REFUSEES PAR NATURE — leurs empreintes
 *     sont CITEES, jamais mesurees ici ;
 *   — compile SUR LA MACHINE MEME depuis CETTE source (la source est la
 *     verite) ; AUCUN exe precompile ne vit dans ce kit ;
 *   — AUCUNE piece externe : aucun chargement d'image, aucun reseau, aucun
 *     droit particulier.
 *
 * LES QUATRE CIBLES (les deux premieres sont les CONTROLES de l'instrument —
 * un instrument non eprouve ne mesure rien) :
 *   eq-constant     le controle POSITIF : la comparaison 32 octets par OU
 *                   masque, AUCUN branchement sur le secret — attendu :
 *                   aucune divergence au seuil (une divergence est un
 *                   RESULTAT precieux : D189 : consigner tel quel) ;
 *   eq-branchue     le controle NEGATIF : la comparaison a sortie au premier
 *                   octet divergent — LE FAUX PATRON ; attendu : DIVERGENCE
 *                   (la preuve que l'instrument detecte les fuites). Si
 *                   elle ne diverge PAS : l'instrument est CONTESTE sur cet
 *                   echantillon — nomme, jamais muet ;
 *   sha256-logiciel la compression SHA-256 logicielle d'un bloc de 64 octets
 *                   (la MEME mecanique que dudect_v150.c : l'etat AMONT est
 *                   l'IV, le bloc 64 est LE SECRET) — attendu : aucune
 *                   divergence au seuil ;
 *   sha256-arm-sha2 la compression par les INSTRUCTIONS MATERIELLES
 *                   FEAT_SHA256 (SHA256H/SHA256H2 — la MEME famille que le
 *                   telephone : les deux mondes se constatent, aucun ne se
 *                   deguise). Compilee si le compilateur expose +sha2 (ou
 *                   son defaut Apple Silicon qui le porte de facto) ; sur
 *                   macOS le canal noyau manque — L'EPREUVE FIPS DECIDE
 *                   SEULE : un condense divergent est un REFUS, rien n'est
 *                   mesure (fail-closed).
 *
 * LA MECANIQUE (l'equation du protocole APPLE-ARM-1, l'egalite du
 * TELEPHONE-ARM-1) :
 *   — le compteur : CNTVCT_EL0 sur aarch64 (le compteur generique du SoC —
 *     PAS le cycle CPU ; la grandeur est nommee « ticks », jamais
 *     « cycles ») ; si la lecture est refusee (SIGILL), le repli horloge est
 *     NOMME, jamais muet. Sur hote x86-64 : TSC (l'AUTOTEST DU
 *     LABORATOIRE — aucun statut terrain n'en decoule) ;
 *   — le contrepoint : CLOCK_MONOTONIC en secondes (la colonne « secondes »
 *     du journal) ;
 *   — l'AMPLIFICATION : LOT=512 pour les comparaisons, LOT=4 pour les
 *     compressions (l'equation pre-enregistree — pas de reglage au
 *     terrain) ;
 *   — l'ENTRELACEMENT : a CHAQUE iteration, la premiere classe vit puis la
 *     seconde (le secret regenere hors mesure) ;
 *   — LES CLASSES par cible : comparaisons = EGAL (copie de l'etalon)
 *     contre DIVERGENT (secret frais — le cas d'usage canonique de la
 *     divulgation) ; compressions = SECRET-FIXE contre SECRET-ALEATOIRE
 *     (l'invariance de donnees) ;
 *   — l'echauffement : 100 paires par cible, resultats jetes ;
 *   — N par classe (60 au minimum, 200 par defaut — le terrain vit 60 puis
 *     200 puis 400 dans cet ordre, l'ordre du LISEZMOI) ;
 *   — la statistique : le t de Welch sur les ticks, le seuil |t| > 5 (les
 *     memes parametres que le kit-2, le kit-B et le kit-C) ;
 *   — l'epreuve FIPS 180-4 « abc » AVANT toute mesure : le condense EXACT
 *     est EXIGE du lecteur logiciel ET du lecteur materiel (s'il vit) — un
 *     lecteur faux est un REFUS : rien n'est mesure.
 *
 * LES SORTIES :
 *   la console           le run entier, ligne par ligne ;
 *   journal-dudect-apple-<epoch>.csv   cible,classe,iteration,ticks,secondes ;
 *   (le temoin auto-portant est compose par scenario-dudect-apple.py qui
 *    orchestre les trois runs 60/200/400 et ecrit les temoins).
 *
 * Codes de sortie : 0 = LE RUN VECU (vert ou ecarts nommes au verdict) ;
 *                   2 = REFUS NOMME AVANT MESURE (lecteur FIPS faux,
 *                       journal impossible).
 *
 * Compilation (le lanceur le fait pour vous) :
 *   clang -O2 -march=armv8-a+sha2 -o dudect_apple dudect_apple.c -lm
 *   clang -O2                      -o dudect_apple dudect_apple.c -lm
 * (sur Apple Silicon le defaut du compilateur porte FEAT_SHA256 de facto ;
 *  sur hote non-aarch64, la cible materielle est REFUSEE PAR NATURE.)
 *
 * Eprouve au laboratoire (la mecanique, jamais le silicium) sur hote Linux
 * x86-64 (autotest natif, la voie TSC) : AUCUN statut terrain n'en decoule
 * — le run Apple Silicon appartient au developpeur (ou au labo, AUSSI
 * DISTANT que le geste Actions, toujours nomme).
 *
 * Usage : dudect_apple [N_par_classe] [--autotest] [--fips]
 *         (defauts : 200 ; --autotest force N=60 et l'etiquette labo ;
 *          --fips vit la seule epreuve FIPS puis sort)
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <signal.h>
#include <setjmp.h>
#include <unistd.h>
#include <fcntl.h>
#if defined(__linux__)
#include <sched.h>      /* l'affinite est un geste Linux — nomine, jamais muet */
#endif

/* ---- les pieces scellees v0.15.0 (les empreintes CITEES, jamais mesurees) ---- */
static const char *PIECES_X86_REFUSEES[] = {
    "loupe.exe 0.1.1        sha256 c111510535767a40b0122d4e42261c9d"
    "8e1ec10d94d95ef666fd76ceb93e61d1",
    "proxy-image.bin        sha256 0782d7e20d0bd4a268e6ec7ed0dc1453"
    "a0f42d7e72b784c2acc9ed423a885dff",
    "moteur-shani.bin       sha256 761ab194d88d527c653111a41324b0bb"
    "3e9247b1c56ba8dc9fedeeccbe04bcec",
};

/* ---- l'alea (/dev/urandom — reprise veritable de dudect_v150.c) ---- */
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

/* l'affinite : un geste LINUX — sur macOS il est REFUSE PAR NATURE et
 * NOMME (le t sera bruite, constate tel quel, jamais maquille) */
static int poser_affinite(int coeur) {
#if defined(__linux__)
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(coeur, &m);
    return sched_setaffinity(0, sizeof(m), &m) == 0;
#else
    (void)coeur;
    return 0;    /* macOS : pas de goupille — l'ecart est nomme a la console */
#endif
}

/* ---- le compteur : CNTVCT_EL0 (aarch64), TSC (autotest labo x86-64),
 *     avec le repli horloge NOMME si la lecture est refusee (SIGILL) ---- */
#if defined(__aarch64__)
static uint64_t lecteur_cntvct(void) {
    uint64_t v;
    __asm__ volatile ("mrs %0, cntvct_el0" : "=r"(v));
    return v;
}
#define ARCH_NOM "aarch64 (Apple Silicon — l'identite vit au sysctl du scenario)"
#else
static uint64_t lecteur_cntvct(void) {
    unsigned int a, d;
    __asm__ volatile ("rdtsc" : "=a"(a), "=d"(d));
    return ((uint64_t)d << 32) | a;
}
#define ARCH_NOM "non-aarch64 (l'hote x86-64 du laboratoire)"
#endif
__attribute__((unused)) static uint64_t lecteur_horloge(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return (uint64_t)t.tv_sec * 1000000000ull + (uint64_t)t.tv_nsec;
}
static volatile sig_atomic_t g_sigil = 0;
static sigjmp_buf g_jb;
__attribute__((unused)) static void gestion_sigill(int s) { (void)s; g_sigil = 1; siglongjmp(g_jb, 1); }

/* ---- SHA-256 : la table K et la mecanique de dudect_v150.c (la meme source) ---- */
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

/* la compression LOGICIELLE d'un bloc de 64 octets — noinline et le
 * bloc VOLATIL : le compilateur ne peut NI plier l'appel dans la boucle
 * de lot, NI hisser les lectures hors des iterations mesurees */
__attribute__((noinline))
static void sha256_compress(uint32_t h[8], const volatile unsigned char bloc[64]) {
    uint32_t w[64];
    for (int i = 0; i < 16; i++) {
        unsigned char p0 = bloc[4*i], p1 = bloc[4*i+1];
        unsigned char p2 = bloc[4*i+2], p3 = bloc[4*i+3];
        w[i] = ((uint32_t)p0<<24)|((uint32_t)p1<<16)
             |((uint32_t)p2<<8)|(uint32_t)p3;
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

/* le condense complet (le bourrement FIPS 180-4 — pour l'epreuve « abc ») */
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
    for (size_t b = 0; b < nb; b++)
        sha256_compress(h, t + b*64);
    free(t);
    for (int i = 0; i < 8; i++) {
        o[4*i]=(unsigned char)(h[i]>>24); o[4*i+1]=(unsigned char)(h[i]>>16);
        o[4*i+2]=(unsigned char)(h[i]>>8); o[4*i+3]=(unsigned char)h[i];
    }
}

/* ---- la compression MATERIELLE : FEAT_SHA256 (SHA256H/SHA256H2/SU0/SU1) ----
 * Compilee si le compilateur expose +sha2 (ou son defaut Apple Silicon) ;
 * sur macOS le canal noyau manque — L'EPREUVE FIPS DECIDE SEULE. */
#if defined(__aarch64__) && defined(__ARM_FEATURE_SHA2)
#include <arm_neon.h>
#define HW_COMPILABLE 1
__attribute__((noinline))
static void sha256_arm_hw(uint32_t etat[8], const volatile unsigned char bloc[64]) {
    unsigned char b[64];
    for (int i = 0; i < 64; i++) b[i] = bloc[i];   /* la relecture honnete */
    uint32x4_t S0 = vld1q_u32(&etat[0]);           /* a b c d */
    uint32x4_t S1 = vld1q_u32(&etat[4]);           /* e f g h */
    uint32x4_t M0 = vreinterpretq_u32_u8(vrev32q_u8(vld1q_u8(b +  0)));
    uint32x4_t M1 = vreinterpretq_u32_u8(vrev32q_u8(vld1q_u8(b + 16)));
    uint32x4_t M2 = vreinterpretq_u32_u8(vrev32q_u8(vld1q_u8(b + 32)));
    uint32x4_t M3 = vreinterpretq_u32_u8(vrev32q_u8(vld1q_u8(b + 48)));
    uint32x4_t MSG, T;
    /* groupes 0-3 : les mots W[0..15] tels quels */
    MSG = vaddq_u32(M0, vld1q_u32(&K256[0]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    MSG = vaddq_u32(M1, vld1q_u32(&K256[4]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    MSG = vaddq_u32(M2, vld1q_u32(&K256[8]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    MSG = vaddq_u32(M3, vld1q_u32(&K256[12]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    /* groupes 4-15 : l'expansion roule Mi, su0(Mi, Mi+1) puis su1(Mi, Mi+2, Mi+3) */
    M0 = vsha256su0q_u32(M0, M1); M0 = vsha256su1q_u32(M0, M2, M3);
    MSG = vaddq_u32(M0, vld1q_u32(&K256[16]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M1 = vsha256su0q_u32(M1, M2); M1 = vsha256su1q_u32(M1, M3, M0);
    MSG = vaddq_u32(M1, vld1q_u32(&K256[20]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M2 = vsha256su0q_u32(M2, M3); M2 = vsha256su1q_u32(M2, M0, M1);
    MSG = vaddq_u32(M2, vld1q_u32(&K256[24]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M3 = vsha256su0q_u32(M3, M0); M3 = vsha256su1q_u32(M3, M1, M2);
    MSG = vaddq_u32(M3, vld1q_u32(&K256[28]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M0 = vsha256su0q_u32(M0, M1); M0 = vsha256su1q_u32(M0, M2, M3);
    MSG = vaddq_u32(M0, vld1q_u32(&K256[32]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M1 = vsha256su0q_u32(M1, M2); M1 = vsha256su1q_u32(M1, M3, M0);
    MSG = vaddq_u32(M1, vld1q_u32(&K256[36]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M2 = vsha256su0q_u32(M2, M3); M2 = vsha256su1q_u32(M2, M0, M1);
    MSG = vaddq_u32(M2, vld1q_u32(&K256[40]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M3 = vsha256su0q_u32(M3, M0); M3 = vsha256su1q_u32(M3, M1, M2);
    MSG = vaddq_u32(M3, vld1q_u32(&K256[44]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M0 = vsha256su0q_u32(M0, M1); M0 = vsha256su1q_u32(M0, M2, M3);
    MSG = vaddq_u32(M0, vld1q_u32(&K256[48]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M1 = vsha256su0q_u32(M1, M2); M1 = vsha256su1q_u32(M1, M3, M0);
    MSG = vaddq_u32(M1, vld1q_u32(&K256[52]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M2 = vsha256su0q_u32(M2, M3); M2 = vsha256su1q_u32(M2, M0, M1);
    MSG = vaddq_u32(M2, vld1q_u32(&K256[56]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    M3 = vsha256su0q_u32(M3, M0); M3 = vsha256su1q_u32(M3, M1, M2);
    MSG = vaddq_u32(M3, vld1q_u32(&K256[60]));
    T   = vsha256hq_u32(S0, S1, MSG);  S1 = vsha256h2q_u32(S1, S0, MSG);  S0 = T;
    /* l'accumulation finale : l'etat initial rendu en tableau */
    uint32x4_t F0 = vld1q_u32(&etat[0]);
    uint32x4_t F1 = vld1q_u32(&etat[4]);
    vst1q_u32(&etat[0], vaddq_u32(F0, S0));
    vst1q_u32(&etat[4], vaddq_u32(F1, S1));
}
/* le condense complet par la voie MATERIELLE (l'epreuve FIPS) */
static void sha256_hw(const unsigned char *d, size_t n, unsigned char o[32]) {
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
    for (size_t b = 0; b < nb; b++)
        sha256_arm_hw(h, t + b*64);
    free(t);
    for (int i = 0; i < 8; i++) {
        o[4*i]=(unsigned char)(h[i]>>24); o[4*i+1]=(unsigned char)(h[i]>>16);
        o[4*i+2]=(unsigned char)(h[i]>>8); o[4*i+3]=(unsigned char)h[i];
    }
}
#else
#define HW_COMPILABLE 0
#endif

/* ---- les deux controles de l'instrument ---- */
/* le POSITIF : le OU masque — AUCUN branchement sur le secret */
__attribute__((noinline))
static int eq_constant(const volatile unsigned char *a,
                       const volatile unsigned char *b, size_t n) {
    unsigned char diff = 0;
    for (size_t i = 0; i < n; i++) diff |= a[i] ^ b[i];
    return (int)((diff - 1) >> 8) & 1;    /* 1 si egaux — sans branche */
}
/* le NEGATIF : la sortie au premier octet divergent — LE FAUX PATRON */
__attribute__((noinline))
static int eq_branchue(const volatile unsigned char *a,
                       const volatile unsigned char *b, size_t n) {
    for (size_t i = 0; i < n; i++)
        if (a[i] != b[i]) return 0;
    return 1;
}

/* ---- le puits (le resultat consomme — rien n'est elimine) ---- */
static volatile unsigned long g_puits = 0;

/* ---- l'appel par cible (l'etat AMONT est l'IV, comme tls13-02) ---- */
enum { T_EQ_CT, T_EQ_BR, T_SHA_SW, T_SHA_HW };
static const uint32_t IV256[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,
                                  0xa54ff53a,0x510e527f,0x9b05688c,
                                  0x1f83d9ab,0x5be0cd19};
static void appeler(int t, unsigned char *secret, unsigned char *aux) {
    uint32_t etat[8];
    memcpy(etat, IV256, sizeof etat);
    switch (t) {
    case T_EQ_CT:  g_puits += (unsigned long)eq_constant(secret, aux, 32); break;
    case T_EQ_BR:  g_puits += (unsigned long)eq_branchue(secret, aux, 32); break;
    case T_SHA_SW: sha256_compress(etat, secret); g_puits += etat[0]; break;
#if HW_COMPILABLE
    case T_SHA_HW: sha256_arm_hw(etat, secret);   g_puits += etat[0]; break;
#endif
    }
}

/* ---- le drapeau « sha2 » du noyau (le jeton EXACT) — UN CANAL LINUX :
 *     sur macOS /proc/cpuinfo n'existe pas, la fonction rend -1 (canal
 *     absent) et L'EPREUVE FIPS DECIDE SEULE — nomme, jamais muet ---- */
static int drapeau_sha2(void) {
    FILE *f = fopen("/proc/cpuinfo", "r");
    if (!f) return -1;                       /* canal absent (macOS) : nomme */
    char ligne[4096];
    int vu = 0;
    while (fgets(ligne, sizeof ligne, f)) {
        if (strncmp(ligne, "Features", 8) != 0) continue;
        char *c = ligne;
        while (*c) {
            char *d = c;
            while (*d && *d != ' ' && *d != '\t' && *d != '\n') d++;
            if (d - c == 4 && memcmp(c, "sha2", 4) == 0) { vu = 1; break; }
            c = (*d) ? d + 1 : d;
        }
        if (vu) break;
    }
    fclose(f);
    return vu;
}

/* ---- la statistique (reprise veritable de dudect_v150.c) ---- */
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

static void hexa(const unsigned char *p, int n, char *o) {
    for (int i = 0; i < n; i++) sprintf(o + 2*i, "%02x", p[i]);
    o[2*n] = 0;
}

int main(int argc, char **argv) {
    volatile size_t n = 200;
    volatile int autotest = 0, fips_seul = 0;
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--autotest") == 0) autotest = 1;
        else if (strcmp(argv[i], "--fips") == 0) fips_seul = 1;
        else if (i == 1) { n = (size_t)strtoul(argv[i], NULL, 10); }
        else { fprintf(stderr, "[REFUS] argument inconnu : %s\n", argv[i]);
               return 2; }
    }
    if (n < 60) n = 60;             /* la commande : N >= 60 par classe */
    if (n > NMAX) n = NMAX;
    if (autotest) n = 60;

    /* ---- le compteur : la sonde CNTVCT avec le repli NOMME ---- */
    uint64_t (*compteur)(void) = lecteur_cntvct;
    const char *nom_compteur =
#if defined(__aarch64__)
        "CNTVCT_EL0 (le compteur generique du SoC — PAS le cycle CPU)";
#else
        "TSC (l'autotest du laboratoire x86-64)";
#endif
#if defined(__aarch64__)
    void (*ancien)(int) = signal(SIGILL, gestion_sigill);
    if (sigsetjmp(g_jb, 1) == 0) { (void)lecteur_cntvct(); }
    else { compteur = lecteur_horloge;
           nom_compteur = "CLOCK_MONOTONIC en nanosecondes (le REPLI : "
                          "CNTVCT_EL0 refuse — SIGIL — nomme, jamais muet)"; }
    signal(SIGILL, ancien);
#endif

    printf("=== dudect_apple - LE TESTEUR DU SILICIUM APPLE "
           "(edition APPLE-SILICON, v1.0.0) ===\n");
    printf("[config] arch=%s  compteur=%s\n", ARCH_NOM, nom_compteur);
    printf("[config] N=%zu/classe  seuil |t|>5  echantillons ENTRELACES "
           "(le protocole APPLE-ARM-1)\n", n);
    if (autotest)
        printf("[ETIQUETTE] AUTOTEST LABORATOIRE - la mecanique seule : "
               "AUCUN statut terrain n'en decoule (le run Apple Silicon "
               "appartient au developpeur)\n");

    /* ---- le refus nomme des pieces x86-64 (le coeur de l'honnetete) ---- */
    printf("[refus] les pieces scellees v0.15.0 sont x86-64 Windows - "
           "REFUSEES PAR NATURE sur ce silicium (empreintes citees) :\n");
    for (size_t i = 0; i < sizeof PIECES_X86_REFUSEES / sizeof *PIECES_X86_REFUSEES; i++)
        printf("[refus]   %s\n", PIECES_X86_REFUSEES[i]);

    /* ---- le canal noyau : PRESENT (Linux), ABSENT (macOS — nomme) ---- */
    int sha2_noyau = drapeau_sha2();
    if (sha2_noyau < 0)
        printf("[silicium] le canal /proc/cpuinfo est ABSENT (macOS) : la\n"
               "           garde noyau ne peut pas s'y exprimer —\n"
               "           L'EPREUVE FIPS DECIDE SEULE (fail-closed) : si\n"
               "           le lecteur materiel vit et rend le condense\n"
               "           exact, la cible vit ; sinon REFUS NOMME.\n");
    else if (sha2_noyau)
        printf("[silicium] le drapeau « sha2 » EST expose par le noyau : "
               "FEAT_SHA256 (SHA256H/SHA256H2) - la MEME famille que le "
               "telephone\n");
    else
        printf("[silicium] le drapeau « sha2 » est ABSENT des Features : "
               "la cible materielle sera REFUSEE, nommee\n");

    /* ---- l'epreuve FIPS 180-4 « abc » (fail-closed avant toute mesure) ---- */
    static const char ABC_ATTENDU[] =
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";
    unsigned char condense[32]; char hex[65];
    sha256((const unsigned char *)"abc", 3, condense);
    hexa(condense, 32, hex);
    printf("[fips] sha256-logiciel(abc) = %s — %s\n", hex,
           strcmp(hex, ABC_ATTENDU) == 0 ? "EXACT" : "DIVERGENT");
    if (strcmp(hex, ABC_ATTENDU) != 0) {
        fprintf(stderr, "[REFUS] le lecteur LOGICIEL est faux - RIEN ne "
                "sera mesure (fail-closed)\n");
        return 2;
    }
#if HW_COMPILABLE
    sha256_hw((const unsigned char *)"abc", 3, condense);
    hexa(condense, 32, hex);
    printf("[fips] sha256-arm-sha2(abc) = %s — %s\n", hex,
           strcmp(hex, ABC_ATTENDU) == 0 ? "EXACT" : "DIVERGENT");
    if (strcmp(hex, ABC_ATTENDU) != 0) {
        fprintf(stderr, "[REFUS] le lecteur MATERIEL est faux (l'assemblage "
                "SHA256H diverge du FIPS) - RIEN ne sera mesure (fail-closed)\n");
        return 2;
    }
#else
    printf("[silicium] la cible materielle n'est PAS compilable ici "
           "(compilateur sans +sha2, ou hote non-aarch64) — REFUS NOMME, "
           "le reste du run vit\n");
#endif
    if (fips_seul) {
        printf("[fips] l'epreuve est vecue seule (l'option --fips) - "
               "code 0\n");
        return 0;
    }

    /* ---- l'affinite (au mieux - un refus est consigne, jamais muet) ---- */
    printf("[affinite] coeur 0 : %s\n", poser_affinite(0) ? "posee" :
           "REFUSEE sur ce systeme (macOS : pas de goupille — le t sera "
           "bruite, consignez-le)");

    /* ---- le journal csv (l'horodatage a la nanoseconde : deux runs dans
     *     la meme seconde ne s'ecrasent JAMAIS l'un l'autre) ---- */
    struct timespec maintenant;
    clock_gettime(CLOCK_REALTIME, &maintenant);
    char nom_csv[256];
    snprintf(nom_csv, sizeof nom_csv, "journal-dudect-apple-%ld%09ld.csv",
             (long)maintenant.tv_sec, (long)maintenant.tv_nsec);
    FILE *csv = fopen(nom_csv, "w");
    if (!csv) { perror("fopen"); return 2; }
    fprintf(csv, "cible,classe,iteration,ticks,secondes\n");

    /* ---- les cibles ---- */
    struct { const char *nom; int t; int lot; int egalite;
             const char *ca; const char *cb; } cibles[] = {
        {"eq-constant",     T_EQ_CT,  512, 1, "egal",      "divergent"},
        {"eq-branchue",     T_EQ_BR,  512, 1, "egal",      "divergent"},
        {"sha256-logiciel", T_SHA_SW,   4, 0, "fixe",      "aleatoire"},
#if HW_COMPILABLE
        {"sha256-arm-sha2", T_SHA_HW,   4, 0, "fixe",      "aleatoire"},
#endif
    };
    int nb = (int)(sizeof cibles / sizeof *cibles);

    unsigned char secret_fixe[64], secret[64], aux[64];
    alea(secret_fixe, sizeof secret_fixe);
    alea(aux, sizeof aux);
    memcpy(secret, secret_fixe, sizeof secret);

    int vecues = 0, refus = 0, instrument_conteste = 0, positif_diverge = 0;
    double med_log = -1.0, med_mat = -1.0;

    for (int k = 0; k < nb; k++) {
        if (cibles[k].t == T_SHA_HW && sha2_noyau == 0) {
            printf("[%s] REFUS NOMME : le noyau n'expose pas « sha2 » - la "
                   "cible est PASSEE, le reste du run vit\n", cibles[k].nom);
            refus++;
            continue;
        }
        printf("[%s] echauffement 100 paires, puis %zu iterations entrelacees "
               "(LOT=%d appels par echantillon)\n", cibles[k].nom, n, cibles[k].lot);

        int lot = cibles[k].lot;
        /* la premiere classe : EGAL (la copie de l'etalon) pour les
         * comparaisons, SECRET-FIXE pour les compressions */
        if (cibles[k].egalite) memcpy(secret, aux, 64);
        else memcpy(secret, secret_fixe, 64);
        /* l'echauffement : 100 paires, resultats jetes */
        for (int j = 0; j < 100; j++) {
            if (cibles[k].egalite) memcpy(secret, aux, 64);
            else memcpy(secret, secret_fixe, 64);
            for (int l = 0; l < lot; l++) appeler(cibles[k].t, secret, aux);
            alea(secret, sizeof secret);
            for (int l = 0; l < lot; l++) appeler(cibles[k].t, secret, aux);
        }

        serie_t un, deux;
        un.n = deux.n = 0;
        for (size_t i = 0; i < n; i++) {
            /* la premiere classe (egal / secret-fixe) — le secret RESTAURE
             * a CHAQUE iteration (l'egal se recopie, sinon la classe un
             * mesurerait le reste aleatoire de l'iteration amont) */
            if (cibles[k].egalite) memcpy(secret, aux, 64);
            else memcpy(secret, secret_fixe, 64);
            double t0s = horloge_sec(); uint64_t t0 = compteur();
            for (int l = 0; l < lot; l++) appeler(cibles[k].t, secret, aux);
            uint64_t t1 = compteur(); double t1s = horloge_sec();
            un.cyc[un.n] = t1 - t0; un.sec[un.n] = t1s - t0s; un.n++;
            fprintf(csv, "%s,%s,%zu,%llu,%.9f\n", cibles[k].nom, cibles[k].ca,
                    i, (unsigned long long)(t1 - t0), t1s - t0s);
            /* la seconde classe (divergent / secret-aleatoire — le secret
             * regenere HORS mesure) */
            alea(secret, sizeof secret);
            t0s = horloge_sec(); t0 = compteur();
            for (int l = 0; l < lot; l++) appeler(cibles[k].t, secret, aux);
            t1 = compteur(); t1s = horloge_sec();
            deux.cyc[deux.n] = t1 - t0; deux.sec[deux.n] = t1s - t0s;
            deux.n++;
            fprintf(csv, "%s,%s,%zu,%llu,%.9f\n", cibles[k].nom, cibles[k].cb,
                    i, (unsigned long long)(t1 - t0), t1s - t0s);
        }
        double tw = t_welch(&un, &deux);
        uint64_t *fc = malloc(un.n * sizeof(uint64_t));
        uint64_t *ac = malloc(deux.n * sizeof(uint64_t));
        if (!fc || !ac) { fprintf(stderr, "[REFUS] memoire\n"); return 2; }
        memcpy(fc, un.cyc, un.n * sizeof(uint64_t));
        memcpy(ac, deux.cyc, deux.n * sizeof(uint64_t));
        uint64_t mun = mediane(fc, un.n);
        uint64_t mdeux = mediane(ac, deux.n);
        free(fc); free(ac);
        int diverge = fabs(tw) > 5.0;
        printf("  %-10s     : moy %.1f ticks, med %llu (par appel : "
               "%.2f)\n", cibles[k].ca, moy(un.cyc, un.n),
               (unsigned long long)mun, (double)mun / lot);
        printf("  %-10s     : moy %.1f ticks, med %llu (par appel : "
               "%.2f)\n", cibles[k].cb, moy(deux.cyc, deux.n),
               (unsigned long long)mdeux, (double)mdeux / lot);
        printf("  t de Welch = %.2f -> %s (seuil |t| > 5)\n", tw,
               diverge ? "DIVERGENCE TEMPORELLE (a consigner telle quelle)"
                       : "AUCUNE divergence au seuil");
        if (cibles[k].t == T_EQ_CT) {
            if (diverge) {
                printf("  ATTENDU : aucune divergence — la divergence d'un "
                       "patron constant est un RESULTAT (D189 : consigner "
                       "tel quel)\n");
                positif_diverge = 1;
            }
        }
        if (cibles[k].t == T_EQ_BR && !diverge) {
            printf("  ATTENDU : divergence — L'INSTRUMENT EST CONTESTE sur "
                   "cet echantillon (nomme, jamais muet : le temoin le dit, "
                   "le labo recoupera avec vous)\n");
            instrument_conteste = 1;
        }
        if (cibles[k].t == T_SHA_SW) med_log = (double)mun / lot;
        if (cibles[k].t == T_SHA_HW) med_mat = (double)mun / lot;
        vecues++;
    }
    fclose(csv);
    printf("[sortie] %s — joignez-le au temoin (la synthese le fait)\n",
           nom_csv);
    if (med_log > 0 && med_mat > 0)
        printf("[constat] le rapport median logiciel/materiel = %.2f — LE "
               "CONSTAT DE CE SILICIUM (jamais une cible : aucune cible "
               "pre-enregistree n'existe pour Apple Silicon)\n", med_log / med_mat);

    /* ---- le verdict ---- */
    printf("[verdict] LE RUN VECU : %d/%d cible(s) consignee(s), %d refus "
           "nomme(s)", vecues, nb, refus);
    if (instrument_conteste) printf(" — INSTRUMENT CONTESTE (nomme)");
    if (positif_diverge)     printf(" — controle positif DIVERGENT (resultat)");
    printf("\n");
    printf("[verdict] la lecture honnete : |t| > 5 = dependance AU SEUIL sur "
           "CET echantillon, consignee telle quelle ; |t| <= 5 = aucune "
           "divergence au seuil sur cet echantillon, CETTE machine - jamais "
           "« temps constant prouve »\n");
    printf("[verdict] code de sortie : 0 (le run vecu, vert ou ecarts "
           "nommes)\n");
    return 0;
}
