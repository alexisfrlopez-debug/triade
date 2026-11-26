/* pilote_c.c — LE PILOTE C AU MÊME VOLUME (W28HARNAIS, prompt 3, geste 5).
 *
 * Le même code de bloc (les octets assemblés de la notation tls13-16, le
 * même fichier que le moteur exécute) appelé DIRECTEMENT, SANS échafaudage
 * d'oracle : pas de console, pas de digeste, pas de compteur — la boucle
 * nue : l'entrée posée (memcpy 32 o) + l'appel (les registres de l'ABI
 * profil a). Compilé au gcc du bac (-O2). La mesure : clock_gettime
 * monotone autour de la BOUCLE SEULE (le montage hors temps — les deux
 * moteurs le paient pareil, il n'entre pas dans le rapport de régime).
 *
 * Usage : pilote_c <corps.bin> <marge_hex> <vecteurs.bin> <n> <calendrier.bin> [passes]
 * Écrit : le temps de la boucle par passe, en microsecondes, sur stdout.
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

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage attendu\n"); return 2; }
    const char *chemin_corps = argv[1];
    uint64_t marge = strtoull(argv[2], NULL, 16);
    const char *chemin_vec = argv[3];
    int n = atoi(argv[4]);
    int passes = (argc > 6) ? atoi(argv[6]) : 5;

    int fc = open(chemin_corps, O_RDONLY);
    if (fc < 0) { perror("corps"); return 2; }
    static unsigned char corps[8192];
    ssize_t tc = read(fc, corps, sizeof(corps));
    close(fc);
    if (tc <= 0) { fprintf(stderr, "corps vide\n"); return 2; }

    int fv = open(chemin_vec, O_RDONLY);
    if (fv < 0) { perror("vecteurs"); return 2; }
    static vecteur vec[12288];
    ssize_t tv = read(fv, vec, sizeof(vecteur) * n);
    close(fv);
    if (tv < (ssize_t)(sizeof(vecteur) * n)) { fprintf(stderr, "vecteurs courts\n"); return 2; }

    mmap((void*)0xC000, 0x4000, 7, 0x32, -1, 0);
    mmap((void*)0x500000, 0x21000, 3, 0x32, -1, 0);
    mmap((void*)0x70000, 0x10000, 3, 0x32, -1, 0);
    memcpy((void*)marge, corps, (size_t)tc);
    { int fcal = open(argv[5], O_RDONLY);
      if (fcal < 0) { perror("calendrier"); return 2; }
      if (read(fcal, (void*)0x500200, 176) != 176) {
          fprintf(stderr, "calendrier court\n"); return 2;
      }
      close(fcal); }

    /* LA BOUCLE NUE : l'entrée posée + l'appel — ni console, ni digeste */
    for (int p = 0; p < passes; p++) {
        struct timespec t0, t1;
        clock_gettime(CLOCK_MONOTONIC, &t0);
        for (int i = 0; i < n; i++) {
            memcpy((void*)0x500400, &vec[i], 32);
            uint64_t a_rcx = 0x500200, a_rdx = 0x500400, a_r8 = 0x503000;
            uint64_t rax;
            __asm__ volatile(
                "movq %1, %%rcx;\n"
                "movq %2, %%rdx;\n"
                "movq %3, %%r8;\n"
                "movq %4, %%rax;\n"
                "callq *%%rax;\n"
                "movq %%rax, %0;\n"
                : "=r"(rax)
                : "r"(a_rcx), "r"(a_rdx), "r"(a_r8), "r"(marge)
                : "rax", "rcx", "rdx", "r8", "r9", "r10", "r11",
                  "rdi", "rsi", "memory", "cc");
        }
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double us = (t1.tv_sec - t0.tv_sec) * 1e6 +
                    (t1.tv_nsec - t0.tv_nsec) / 1e3;
        printf("%.3f\n", us);
        fflush(stdout);
    }
    return 0;
}
