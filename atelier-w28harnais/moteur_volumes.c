/* moteur_volumes.c — LE MOTEUR NATIF GÉNÉRALISÉ AUX VOLUMES COMPLETS
 * (W28HARNAIS, prompt 3, geste 5 — la cible de régime ≤ 5 × C
 * pré-enregistrée au plan gelé).
 *
 * Le moteur committé (atelier-oracles-8hguph5ee/moteur_oracles.c, la vague 15)
 * exécute ≤ 4 096 vecteurs par appel et écrit sa console par fprintf À CHAQUE
 * vecteur — l'I/O formatée par vecteur est le régime dominant (mesuré : ~875 ×
 * l'appel nu). LE MOTEUR GÉNÉRALISÉ : même sémantique d'exécution à
 * l'identique (la page 0xC000, la sortie à 0x503000, la pile 0x78000, l'ABI
 * msx64 profil a — le corps copié à sa marge, le calendrier lu au pilot,
 * memset sortie + memcpy entrée + l'appel + LE DIGESTE LU par vecteur) ;
 * TROIS changements de RÉGIME seulement, AUCUN contrôle retiré :
 *   (1) le VOLUME : 12 288 vecteurs en un appel (le lot unique) ;
 *   (2) LE COMPTE EN REGISTRES BRUTS : le rax et les 16 octets du digeste
 *       enregistrés par vecteur dans un tampon (le compte exact du moteur
 *       committé, la lecture de sortie jamais retirée) ;
 *   (3) LA CONSOLE DIFFÉRÉE : le texte (le même format, LIGNE-IDENTIQUE au
 *       moteur committé — la preuve d'équivalence vit au rapport) assemblé
 *       en UNE passe après la boucle, l'hex en table de 512 octets.
 * Le RÉGIME CHAUD (la boucle d'exécution : entrée posée + appel + digeste
 * lue + compte rendu) est horlogé à l'IDENTIQUE du pilote C (clock_gettime
 * monotone autour de la boucle seule, le montage hors temps) et rendu sur
 * stdout — la convention symétrique du pilote ; le régime de BOUT EN BOUT
 * (montage + boucle + console) vit au pilot qui l'horloge au mur.
 *
 * Usage : moteur_volumes <corps.bin> <marge_hex> <vecteurs.bin> <n> <console.jsonl> <profil> <calendrier.bin>
 * stdout : "HOT <µs>" (la boucle d'exécution) — la console et le compte au fichier.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

typedef struct { uint64_t rcx, rdx, r8, r9; } vecteur;
typedef struct { uint64_t rax; unsigned char digeste[16]; } compte;

static const char HEX[] = "0123456789abcdef";

/* le formateur maison d'entier non signé — décimal, jamais un snprintf */
static size_t fmt_u64(char *dst, uint64_t v) {
    char tmp[20];
    size_t k = 0;
    do { tmp[k++] = (char)('0' + (v % 10)); v /= 10; } while (v);
    for (size_t j = 0; j < k; j++)
        dst[j] = tmp[k - 1 - j];
    return k;
}

int main(int argc, char **argv) {
    if (argc != 8) { fprintf(stderr, "usage attendu\n"); return 2; }
    const char *chemin_corps = argv[1];
    uint64_t marge = strtoull(argv[2], NULL, 16);
    const char *chemin_vec = argv[3];
    int n = atoi(argv[4]);
    const char *chemin_console = argv[5];
    const char *profil_abi = argv[6];

    int fc = open(chemin_corps, O_RDONLY);
    if (fc < 0) { perror("corps"); return 2; }
    static unsigned char corps[8192];
    ssize_t tc = read(fc, corps, sizeof(corps));
    close(fc);
    if (tc <= 0) { fprintf(stderr, "corps vide\n"); return 2; }

    int fv = open(chemin_vec, O_RDONLY);
    if (fv < 0) { perror("vecteurs"); return 2; }
    static vecteur vec[12288];                    /* le volume complet : 12 288 */
    ssize_t tv = read(fv, vec, sizeof(vecteur) * n);
    close(fv);
    if (tv < (ssize_t)(sizeof(vecteur) * n)) { fprintf(stderr, "vecteurs courts\n"); return 2; }

    mmap((void*)0xC000, 0x4000, 7, 0x32, -1, 0);
    mmap((void*)0x500000, 0x21000, 3, 0x32, -1, 0);
    mmap((void*)0x70000, 0x10000, 3, 0x32, -1, 0);
    memcpy((void*)marge, corps, (size_t)tc);

    { int fcal = open(argv[7], O_RDONLY);
      if (fcal < 0) { perror("calendrier"); return 2; }
      if (read(fcal, (void*)0x500200, 176) != 176) {
          fprintf(stderr, "calendrier court\n"); return 2;
      }
      close(fcal); }

    /* LE COMPTE EN REGISTRES BRUTS — le digeste lu par vecteur, JAMAIS retiré */
    compte *rec = malloc(sizeof(compte) * (size_t)n);
    if (!rec) { fprintf(stderr, "compte\n"); return 2; }

    /* LA BOUCLE D'EXÉCUTION (le régime chaud) — horlogée comme le pilote */
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (int i = 0; i < n; i++) {
        memset((void*)0x503000, 0, 16);
        memcpy((void*)0x500400, &vec[i], 32);
        uint64_t a_rcx = 0, a_rdx = 0, a_r8 = 0, a_r9 = 0, a_r10 = 0;
        if (profil_abi[0] == 'a') {
            a_rcx = 0x500200; a_rdx = 0x500400; a_r8 = 0x503000;
        } else {
            a_rcx = 0x503000; a_rdx = 0x500400; a_r8 = 0x500A00; a_r10 = 0;
            memcpy((void*)0x500A00, &vec[i], 16);
        }
        uint64_t rax;
        __asm__ volatile(
            "movq %1, %%rcx;\n"
            "movq %2, %%rdx;\n"
            "movq %3, %%r8;\n"
            "movq %4, %%r9;\n"
            "movq %6, %%r10;\n"
            "movq %5, %%rax;\n"
            "callq *%%rax;\n"
            "movq %%rax, %0;\n"
            : "=r"(rax)
            : "r"(a_rcx), "r"(a_rdx), "r"(a_r8), "r"(a_r9), "r"(marge),
              "r"(a_r10)
            : "rax", "rcx", "rdx", "r8", "r9", "r10", "r11",
              "rdi", "rsi", "memory", "cc");
        rec[i].rax = rax;
        memcpy(rec[i].digeste, (void*)0x503000, 16);   /* le digeste LU */
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double us = (t1.tv_sec - t0.tv_sec) * 1e6 + (t1.tv_nsec - t0.tv_nsec) / 1e3;

    /* LA CONSOLE DIFFÉRÉE — le format du moteur committé, LIGNE-IDENTIQUE,
       en UNE passe : l'hex en table, les entiers au formateur maison (le
       snprintf par vecteur était le dernier régime dominant de la passe) */
    size_t cap = (size_t)n * 80 + 64;
    char *buf = malloc(cap);
    if (!buf) { fprintf(stderr, "tampon\n"); return 2; }
    size_t pos = 0;
    for (int i = 0; i < n; i++) {
        memcpy(buf + pos, "{\"vecteur\": ", 12); pos += 12;
        pos += fmt_u64(buf + pos, (uint64_t)i);
        memcpy(buf + pos, ", \"rax\": ", 9); pos += 9;
        pos += fmt_u64(buf + pos, rec[i].rax);
        memcpy(buf + pos, ", \"digeste\": \"", 14); pos += 14;
        for (int k = 0; k < 16; k++) {
            buf[pos++] = HEX[rec[i].digeste[k] >> 4];
            buf[pos++] = HEX[rec[i].digeste[k] & 15];
        }
        buf[pos++] = '"';
        buf[pos++] = '}';
        buf[pos++] = '\n';
    }
    FILE *console = fopen(chemin_console, "w");
    if (!console) { perror("console"); return 2; }
    fwrite(buf, 1, pos, console);
    fclose(console);
    free(buf);
    free(rec);
    printf("OK — %d vecteurs natifs (le moteur généralisé), la console a %s\n", n, chemin_console);
    printf("HOT %.3f\n", us);                       /* le régime chaud, la convention du pilote */
    return 0;
}
