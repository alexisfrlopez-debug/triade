/* moteur_session.c — L'OUVERTURE DE SESSION NATIVE : LE MD5+SHA256 DU TÉMOIN
 * 196 609 o PAR LES BLOCS SCELLÉS (W29MOTEUR, prompt 2 de la vague 29 — le
 * plan gelé PLAN-W29MOTEUR.md).
 *
 * L'image loupe (extraite du harnais_noyau aux octets mêmes : les notations
 * du noyau, les héritages des scellés, les tables MD5, l'IAT) est MONTÉE au
 * moteur natif (mmap aux RVA du plan) ; les SIX feuilles kernel32 du noyau
 * portées en AMORCES NATIVES lisant le témoin (le code des blocs INCHANGÉ —
 * les octets assemblés, la carte est le montage).
 *
 * L'appel : loupe-01(rcx=ADRESSE_CHEMIN) — la session née ENTIÈRE (le
 * md5+sha256 du fichier entier vivent au panneau R_EMPREINTES 0xE3C0/0xE3D0).
 * La confrontation : les condensés recoupés À hashlib (le juge croisé, la
 * référence passée en argument). La mesure : clock_gettime monotone autour
 * de L'OUVERTURE seule (le montage et la remise au vierge hors temps — la
 * convention W28HARNAIS), n passes, la médiane publiée.
 *
 * Usage : moteur_session <image-bas.bin> <image-data.bin> <temoin-3f.bin> \
 *                         <md5 attendu hex> <sha256 attendu hex> <passes>
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

/* LE PLAN (loupe/layout.py, la source unique — jamais gravé de tête) */
#define ADRESSE_CHEMIN   0x700400
#define R_EMPREINTES     0xE3C0       /* le panneau : md5[16] + sha256[32] */
#define IAT_CreateFileW      0x3118
#define IAT_GetFileSizeEx    0x3120
#define IAT_SetFilePointerEx 0x3128
#define IAT_ReadFile         0x3130
#define IAT_CloseHandle      0x3140
#define IAT_GetLastError     0x3148
#define LOUPE01_VA       0x4080
#define ENTREE_RSP       (0x7F007EF8ULL)   /* ≡ 8 (mod 16), le point de vue de l'APPELÉ */
#define MORT             0x901000          /* les 28 feuilles hors noyau : l'appel DÉNONCÉ */

extern void stub_CreateFileW(void);
extern void stub_GetFileSizeEx(void);
extern void stub_SetFilePointerEx(void);
extern void stub_ReadFile(void);
extern void stub_CloseHandle(void);
extern void stub_GetLastError(void);

/* ---- LES HELPEurs NATIFS (SysV) — le témoin EST le fichier de la session -- */

long c_createfilew(const unsigned short *chemin) {
    (void)chemin;                        /* la session née sur LE TÉMOIN (l'unique
                                            fichier déclaré — le miroir OSVirtuel) */
    return open("temoin-3f.bin", O_RDONLY);
}
long c_getfilesizeex(long h, long long *taille) {
    struct stat st;
    if (fstat((int)h, &st) != 0) return 0;
    *taille = (long long)st.st_size;
    return 1;
}
long c_setfilepointerex(long h, long long dist, long long *nouvelle, long methode) {
    /* dwMoveMethod : 0 = FILE_BEGIN, 1 = FILE_CURRENT, 2 = FILE_END */
    int whence = (methode == 0) ? SEEK_SET : (methode == 1) ? SEEK_CUR : SEEK_END;
    off_t r = lseek((int)h, (off_t)dist, whence);
    if (r < 0) return 0;
    if (nouvelle) *nouvelle = (long long)r;
    return 1;
}
long c_readfile(long h, void *buf, unsigned long n, unsigned long *lu) {
    ssize_t r = read((int)h, buf, (size_t)n);
    if (r < 0) return 0;
    if (lu) *lu = (unsigned long)r;
    return 1;
}
long c_closehandle(long h) {
    close((int)h);
    return 1;
}
long c_getlasterror(void) { return 0; }

/* ---- LE MONTAGE -------------------------------------------------------------- */

static unsigned char *monter(unsigned long adr, unsigned long taille, int prot) {
    unsigned char *p = mmap((void *)adr, taille, prot,
                             MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(2); }
    return p;
}

static void lire_fichier(const char *chemin, unsigned char *dest, unsigned long taille) {
    int f = open(chemin, O_RDONLY);
    if (f < 0) { perror(chemin); exit(2); }
    if (read(f, dest, taille) != (ssize_t)taille) {
        fprintf(stderr, "court : %s\n", chemin); exit(2);
    }
    close(f);
}

static void hexlify(const unsigned char *src, int n, char *dst) {
    static const char H[] = "0123456789abcdef";
    for (int i = 0; i < n; i++) {
        dst[2 * i] = H[src[i] >> 4];
        dst[2 * i + 1] = H[src[i] & 15];
    }
    dst[2 * n] = 0;
}

int main(int argc, char **argv) {
    if (argc != 7) { fprintf(stderr, "usage attendu\n"); return 2; }
    unsigned long passes = strtoul(argv[6], NULL, 10);

    /* LE MONTAGE : l'image aux RVA du plan */
    unsigned char *bas = monter(0x1000, 0xD000 - 0x1000, 7);       /* RWX : libc+rdata+text2 */
    unsigned char *don = monter(0xE000, 0x20000 - 0xE000, 3);      /* RW  : .data */
    monter(0x700000, 0x1000, 3);                                    /* le chemin d'appel */
    monter(0x7F000000, 0x10000, 3);                                 /* la pile */
    monter(0x900000, 0x1000, 3);                                    /* la zone amorces */
    mmap((void *)MORT, 0x1000, PROT_NONE,
         MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);           /* le MORT : l'appel dénoncé */

    lire_fichier(argv[1], bas, 0xD000 - 0x1000);
    static unsigned char data_vierge[0x20000 - 0xE000];
    lire_fichier(argv[2], data_vierge, sizeof(data_vierge));
    memcpy(don, data_vierge, sizeof(data_vierge));

    /* L'IAT : les SIX feuilles du noyau vers LEURS AMORCES, les 28 autres au MORT */
    *(uint64_t *)(bas + IAT_CreateFileW      - 0x1000) = (uint64_t)&stub_CreateFileW;
    *(uint64_t *)(bas + IAT_GetFileSizeEx    - 0x1000) = (uint64_t)&stub_GetFileSizeEx;
    *(uint64_t *)(bas + IAT_SetFilePointerEx - 0x1000) = (uint64_t)&stub_SetFilePointerEx;
    *(uint64_t *)(bas + IAT_ReadFile         - 0x1000) = (uint64_t)&stub_ReadFile;
    *(uint64_t *)(bas + IAT_CloseHandle      - 0x1000) = (uint64_t)&stub_CloseHandle;
    *(uint64_t *)(bas + IAT_GetLastError     - 0x1000) = (uint64_t)&stub_GetLastError;

    /* LE CHEMIN : « temoin-3f.bin » en UTF-16 à l'adresse du plan */
    {
        static const unsigned short chemin[] = u"temoin-3f.bin";
        memcpy((void *)ADRESSE_CHEMIN, chemin, sizeof(chemin));
    }

    /* LES PASSES : l'ouverture seule horlogée, la remise au vierge hors temps */
    double us[64];
    if (passes > 64) passes = 64;
    uint64_t rax_final = 0;
    for (unsigned long p = 0; p < passes; p++) {
        memcpy(don, data_vierge, sizeof(data_vierge));     /* le CADRE au vierge + la poignée INVALIDE */
        struct timespec t0, t1;
        clock_gettime(CLOCK_MONOTONIC, &t0);
        uint64_t rax, fake = ENTREE_RSP - 8;   /* ≡ 0 (mod 16) avant le call */
        __asm__ volatile(
            "pushq %%rbx; pushq %%rbp; pushq %%r12; pushq %%r13;\n"
            "pushq %%r14; pushq %%r15;\n"       /* les non-volatils gardés */
            "movq %2, %%rcx;\n"
            "xchgq %%rsp, %1;\n"               /* la pile du FAUX APPELANT msx64 */
            "callq *%3;\n"                     /* loupe-01(rcx = le chemin) */
            "xchgq %%rsp, %1;\n"               /* la pile du C rendue */
            "movq %%rax, %0;\n"
            "popq %%r15; popq %%r14; popq %%r13; popq %%r12;\n"
            "popq %%rbp; popq %%rbx;\n"
            : "=r"(rax), "+r"(fake)
            : "r"((uint64_t)ADRESSE_CHEMIN), "r"((uint64_t)LOUPE01_VA)
            : "rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11",
              "memory", "cc");
        clock_gettime(CLOCK_MONOTONIC, &t1);
        us[p] = (t1.tv_sec - t0.tv_sec) * 1e6 + (t1.tv_nsec - t0.tv_nsec) / 1e3;
        rax_final = rax;
    }

    /* LA CONFRONTATION : les condensés du panneau contre hashlib (la référence) */
    char md5[33], sha[65];
    hexlify((unsigned char *)R_EMPREINTES, 16, md5);
    hexlify((unsigned char *)(R_EMPREINTES + 16), 32, sha);
    int md5_ok = strcmp(md5, argv[4]) == 0;
    int sha_ok = strcmp(sha, argv[5]) == 0;

    /* LA MÉDIANE (n passes) */
    for (unsigned long i = 0; i < passes; i++)
        for (unsigned long j = i + 1; j < passes; j++)
            if (us[j] < us[i]) { double t = us[i]; us[i] = us[j]; us[j] = t; }
    double mediane = us[passes / 2];

    printf("OUVERTURE rax=%llu md5=%s(%d) sha256=%s(%d)\n",
           (unsigned long long)rax_final, md5, md5_ok, sha, sha_ok);
    printf("SESSION %.3f\n", mediane);           /* la médiane des ouvertures, µs */
    for (unsigned long p = 0; p < passes; p++)
        printf("PASSE %.3f\n", us[p]);
    /* rax est NON SPÉCIFIÉ sur le chemin de succès (l'épilogue ne le pose pas —
       les refus seules posent leurs codes négatifs) : LES CONDENSÉS SONT LE
       VERDICT, la confrontation à hashlib. */
    return (md5_ok && sha_ok) ? 0 : 1;
}
