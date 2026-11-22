/* moteur_oracles.c — LE MOTEUR NATIF D'EXÉCUTION DES ORACLES (8hguph5ee,
 * la vague 15) : le corps d'oracle posé à sa marge, les vecteurs exécutés
 * NATIVEMENT (mmap+appel), la console écrite en JSONL (un sha256 par
 * vecteur — le digeste de la page de sortie + les registres de retour).
 * LA CONFIG MOTEUR figée : la page 0xC000, la sortie à 0x503000, la pile
 * à 0x78000, l'ABI msx64 (rcx/rdx/r8/r9, rax le retour) — tout ce qui
 * détermine le résultat vit dans la CLÉ du mémo (le pilot).
 * Usage : moteur_oracles <corps.bin> <marge_hex> <vecteurs.bin> <n> <console.jsonl>
 *   le fichier vecteurs : N × 64 octets (rcx, rdx, r8, r9 — les quatre
 *   mots de 64 bits du vecteur) ; la page de sortie LUE (16 o) au digeste. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

typedef struct { uint64_t rcx, rdx, r8, r9; } vecteur;

/* LES PROFILS ABI (le miroir du jumeau — tout ce qui détermine le
 * résultat vit dans la clé du mémo) :
 *   a (tls13-16, l'AES) : rcx=0x500200 le calendrier, rdx=0x500400 le
 *      bloc d'entrée, r8=0x503000 la sortie ;
 *   b (tls13-17, le GHASH) : rcx=0x503000 la sortie Z, rdx=0x500400
 *      l'entrée X, r8=0x500A00 la valeur H, r10=0. */
static const char *profil_abi = "a";

int main(int argc, char **argv) {
    if (argc != 8) { fprintf(stderr, "usage attendu\n"); return 2; }
    const char *chemin_corps = argv[1];
    uint64_t marge = strtoull(argv[2], NULL, 16);
    const char *chemin_vec = argv[3];
    int n = atoi(argv[4]);
    const char *chemin_console = argv[5];
    profil_abi = argv[6];
    /* le calendrier : le FICHIER partagé du pilot (jamais deux générations) */

    int fc = open(chemin_corps, O_RDONLY);
    if (fc < 0) { perror("corps"); return 2; }
    static unsigned char corps[8192];
    ssize_t tc = read(fc, corps, sizeof(corps));
    close(fc);
    if (tc <= 0) { fprintf(stderr, "corps vide\n"); return 2; }

    int fv = open(chemin_vec, O_RDONLY);
    if (fv < 0) { perror("vecteurs"); return 2; }
    static vecteur vec[4096];
    ssize_t tv = read(fv, vec, sizeof(vecteur) * n);
    close(fv);
    if (tv < (ssize_t)(sizeof(vecteur) * n)) { fprintf(stderr, "vecteurs courts\n"); return 2; }

    mmap((void*)0xC000, 0x4000, 7, 0x32, -1, 0);
    mmap((void*)0x500000, 0x21000, 3, 0x32, -1, 0);
    mmap((void*)0x70000, 0x10000, 3, 0x32, -1, 0);
    memcpy((void*)marge, corps, (size_t)tc);

    FILE *console = fopen(chemin_console, "w");
    if (!console) { perror("console"); return 2; }
    { int fcal = open(argv[7], O_RDONLY);
      if (fcal < 0) { perror("calendrier"); return 2; }
      if (read(fcal, (void*)0x500200, 176) != 176) {
          fprintf(stderr, "calendrier court\n"); return 2;
      }
      close(fcal); }
    for (int i = 0; i < n; i++) {
        memset((void*)0x503000, 0, 16);
        /* le vecteur (4 mots) posé en DONNÉES à l'entrée 0x500400 */
        memcpy((void*)0x500400, &vec[i], 32);
        uint64_t a_rcx = 0, a_rdx = 0, a_r8 = 0, a_r9 = 0, a_r10 = 0;
        if (profil_abi[0] == 'a') {
            a_rcx = 0x500200; a_rdx = 0x500400; a_r8 = 0x503000;
        } else {
            a_rcx = 0x503000; a_rdx = 0x500400; a_r8 = 0x500A00; a_r10 = 0;
            memcpy((void*)0x500A00, &vec[i], 16);  /* H = les 2 premiers mots */
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
        fprintf(console, "{\"vecteur\": %d, \"rax\": %llu, "
                "\"digeste\": \"%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x\"}\n",
                i, (unsigned long long)rax,
                ((unsigned char*)0x503000)[0], ((unsigned char*)0x503000)[1],
                ((unsigned char*)0x503000)[2], ((unsigned char*)0x503000)[3],
                ((unsigned char*)0x503000)[4], ((unsigned char*)0x503000)[5],
                ((unsigned char*)0x503000)[6], ((unsigned char*)0x503000)[7],
                ((unsigned char*)0x503000)[8], ((unsigned char*)0x503000)[9],
                ((unsigned char*)0x503000)[10], ((unsigned char*)0x503000)[11],
                ((unsigned char*)0x503000)[12], ((unsigned char*)0x503000)[13],
                ((unsigned char*)0x503000)[14], ((unsigned char*)0x503000)[15]);
    }
    fclose(console);
    printf("OK — %d vecteurs natifs, la console a %s\n", n, chemin_console);
    return 0;
}
