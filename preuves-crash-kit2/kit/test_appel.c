/* test_appel.c — L'ÉPREUVE D'APPEL (l'autotest du kit dudect).
 * Charge L'IMAGE MÉMOIRE ÉTENDUE de la pièce scellée (proxy-image.bin,
 * produite par extraire_cibles_v150.py — les blocs ne sont PAS autonomes :
 * tls13-02 lit sa table K en .rdata par RIP-relatif), l'appelle à
 * base + RVA, et confronte le condensé au vecteur FIPS 180-4 « abc » :
 *   ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
 * L'adversaire de l'épreuve : un octet de l'image muté → le condensé
 * DOIT diverger (la preuve que l'image exécutée EST celle recoupée). */
#ifndef _WIN32
#define _GNU_SOURCE
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#ifndef _WIN32
#include <sys/mman.h>
#else
#include <windows.h>
#endif

/* LE CORRECTIF n° 1 DU KIT (12/11/2026, la préparation multimachines) :
 *   le backend _WIN32 AJOUTÉ (VirtualAlloc/VirtualProtect — le fichier
 *   n'avait QUE mmap POSIX et ne compilait AUCUNEMENT sous Windows,
 *   le défaut latent découvert à la cross-compilation du kit) ; le
 *   backend POSIX INCHANGÉ (l'autotest re-éprouvé après le geste). */
/* LE CORRECTIF n° 2 DU KIT (12/11/2026, le premier run terrain) :
 *   le kit-2 a CRASHÉ au lancement chez le développeur — le backend
 *   _WIN32 du correctif n° 1 passait l'image en PAGE_EXECUTE_READ
 *   (lecture seule exécutable) puis l'épreuve de l'adversaire ÉCRIT
 *   dans la table K (k[0] ^= 0x01) : violation d'accès (0xC0000005),
 *   l'exe meurt à l'instruction « mov [rbp+0x2f00],al » (0x140008229).
 *   Le labo ne pouvait pas le voir : le backend POSIX mappe l'image
 *   RWX, la mutation s'y écrit toujours — la divergence des deux
 *   backends est née du correctif n° 1 lui-même. LA RÉPARATION :
 *   PAGE_EXECUTE_READWRITE (0x40) — les deux backends portent la MÊME
 *   sémantique RWX, celle que l'autotest POSIX a toujours validée.
 *   L'exe précompilé livré est l'exe du labo PATCHÉ D'UN OCTET
 *   (0x20→0x40, l'immédiat de « mov r8d » qui alimente VirtualProtect) ;
 *   la coquille du printf (« utation K] ») est corrigée à la source. */


#if defined(__GNUC__) && !defined(_WIN32)
#define MSABI __attribute__((ms_abi))
#else
#define MSABI
#endif

typedef void (MSABI *f_comp)(uint32_t *etat, const unsigned char *bloc);

static void hex32(const uint32_t *e, unsigned char o[32]) {
    for (int i = 0; i < 8; i++) {
        o[4*i] = (unsigned char)(e[i]>>24); o[4*i+1] = (unsigned char)(e[i]>>16);
        o[4*i+2] = (unsigned char)(e[i]>>8); o[4*i+3] = (unsigned char)e[i];
    }
}

static int condense_abc(void *image, unsigned char out[32]) {
    unsigned char bloc[64];
    memset(bloc, 0, sizeof bloc);
    bloc[0] = 'a'; bloc[1] = 'b'; bloc[2] = 'c'; bloc[3] = 0x80;
    bloc[63] = 24;   /* la longueur 24 bits, grand-boutiste au dernier mot */
    uint32_t etat[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                        0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    ((f_comp)((char *)image + 0xC080))(etat, bloc);   /* tls13-02 */
    hex32(etat, out);
    return 0;
}

int main(int argc, char **argv) {
    const char *chemin = argc > 1 ? argv[1] : "cibles/proxy-image.bin";
    FILE *f = fopen(chemin, "rb");
    if (!f) { perror("fopen"); return 2; }
    fseek(f, 0, SEEK_END); long t = ftell(f); fseek(f, 0, SEEK_SET);
#ifdef _WIN32
    void *image = VirtualAlloc(NULL, (SIZE_T)t, MEM_COMMIT,
                               PAGE_READWRITE);
    if (!image) { fprintf(stderr, "[REFUS] VirtualAlloc\n"); return 2; }
#else
    size_t garde = ((size_t)t + 4095) & ~4095UL;
    void *image = mmap(NULL, garde, PROT_READ|PROT_WRITE|PROT_EXEC,
                       MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    if (image == MAP_FAILED) { perror("mmap"); return 2; }
#endif
    if (fread(image, 1, (size_t)t, f) != (size_t)t) return 2;
    fclose(f);
#ifdef _WIN32
    {   DWORD old;
        if (!VirtualProtect(image, (SIZE_T)t, PAGE_EXECUTE_READWRITE, &old)) {
            fprintf(stderr, "[REFUS] VirtualProtect\n"); return 2; } }
#endif
    printf("[image] %s : %ld octets mappes a %p\n", chemin, t, image);

    static const unsigned char attendu[32] = {
        0xba,0x78,0x16,0xbf,0x8f,0x01,0xcf,0xea,0x41,0x41,0x40,0xde,
        0x5d,0xae,0x22,0x23,0xb0,0x03,0x61,0xa3,0x96,0x17,0x7a,0x9c,
        0xb4,0x10,0xff,0x61,0xf2,0x00,0x15,0xad};
    unsigned char c[32];
    condense_abc(image, c);
    printf("[FIPS abc] ");
    for (int i = 0; i < 32; i++) printf("%02x", c[i]);
    int ok = memcmp(c, attendu, 32) == 0;
    printf(" -> %s\n", ok ? "EXACT (la piece scellee est bien l'image "
           "executee)" : "DIVERGENT (refuse)");
    if (!ok) return 1;

    /* l'adversaire : un octet de la table K mute -> le condense diverge */
    unsigned char *k = (unsigned char *)image + 0x2F00;   /* .rdata K[64] */
    unsigned char sauve = k[0];
    k[0] ^= 0x01;
    condense_abc(image, c);
    int diverge = memcmp(c, attendu, 32) != 0;
    printf("[mutation K] condense %s — la table est BIEN lue par la "
           "piece\n", diverge ? "DIVERGE" : "INCHANGE (refuse)");
    k[0] = sauve;
    condense_abc(image, c);
    int restaure = memcmp(c, attendu, 32) == 0;
    printf("[restauration] %s\n", restaure ? "EXACT" : "refuse");
    return (ok && diverge && restaure) ? 0 : 1;
}
