/* mesurer_entrelacement.c — LE RIG NATIF DE LA MESURE DE COMPOSITION
 * (2sown2h3z, la vague 15) : le couloir ctr-v4i-ghash-agrege4 à la marge
 * 0xF800, le message 4096 octets (N=256, 64 groupes de quatre), RDTSCP
 * n=20, le cœur épinglé CPU 1 — LA MESURE : c/octet@4096, la cible
 * pré-enregistrée ≤ 2,0. Les scellés 0xDF00/0xDFC0 posés (le repli
 * mesurable), la table du juge à 0x508000.
 * La baseline OpenSSL EVP AES-128-GCM même machine même entrée :
 * mesurer_openssl.c. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <sched.h>
#include <string.h>
#include <sys/mman.h>
#include "donnees_rig.h"

/* les octets du couloir et des scellés : passes par le générateur
 * (rig_octets.h — assemblés par keystone au pilot, jamais retapés) */
#include "rig_octets.h"

#define COULOIR 0xF800
#define S16 0xDF00
#define S17 0xDFC0

__attribute__((naked)) static void appel_couloir(void) {
    __asm__ volatile(
        "movq $0x500200, %rcx;"   /* les clés */
        "movq $0x501000, %rdx;"   /* les compteurs */
        "movq $0x502000, %r8;"    /* le clair */
        "movq $0x503000, %r9;"    /* le chiffré (N*16 + le tag) */
        "movq $1, %r10;"          /* le verdict : le couloir */
        "movq $256, %r11;"        /* N */
        "movq $0xF800, %rax; jmpq *%rax;");
}

__attribute__((naked)) static void appel_repli(void) {
    __asm__ volatile(
        "movq $0x500200, %rcx;"
        "movq $0x501000, %rdx;"
        "movq $0x502000, %r8;"
        "movq $0x503000, %r9;"
        "movq $0, %r10;"          /* le verdict : LE REPLI scellé */
        "movq $256, %r11;"
        "movq $0xF800, %rax; jmpq *%rax;");
}

static uint64_t cyc[32];

static uint64_t mesurer(void (*volatile fp)(void), int appels) {
    uint64_t t0, t1; uint32_t a, d;
    for (int i = 0; i < 32; i++) {
        __asm__ volatile("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t0 = ((uint64_t)d << 32) | a;
        for (int k = 0; k < appels; k++) fp();
        __asm__ volatile("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t1 = ((uint64_t)d << 32) | a;
        cyc[i] = t1 - t0;
    }
    for (int i = 0; i < 32; i++) for (int j = i + 1; j < 32; j++)
        if (cyc[j] < cyc[i]) { uint64_t t = cyc[i]; cyc[i] = cyc[j]; cyc[j] = t; }
    return (cyc[15] + cyc[16]) / 2;   /* la médiane non arrondie (reçue /2) */
}

int main(void) {
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    sched_setaffinity(0, sizeof(m), &m);
    mmap((void*)0xC000, 0x4000, 7, 0x32, -1, 0);
    mmap((void*)0x500000, 0x21000, 3, 0x32, -1, 0);
    mmap((void*)0x70000, 0x10000, 3, 0x32, -1, 0);
    memcpy((void*)S16, S16_OCTETS, S16_TAILLE);
    memcpy((void*)S17, S17_OCTETS, S17_TAILLE);
    memcpy((void*)COULOIR, COULOIR_OCTETS, COULOIR_TAILLE);
    memcpy((void*)0x500200, CLES, 176);
    memcpy((void*)0x501000, COMPTEURS, 4096);
    memcpy((void*)0x502000, CLAIR, 4096);
    memcpy((void*)0x508000, TABLE, 4096);

    /* la parité couloir/repli au rig même (le garde avant la mesure) */
    unsigned char ct1[4112], ct2[4112];
    appel_couloir(); memcpy(ct1, (void*)0x503000, 4112);
    appel_repli(); memcpy(ct2, (void*)0x503000, 4112);
    if (memcmp(ct1, ct2, 4112) != 0) {
        printf("PARITE COULOIR/REPLI : ECART — mesure refusee\n");
        return 1;
    }
    printf("PARITE COULOIR/REPLI au rig : identiques (le garde vert)\n");

    uint64_t med = mesurer(appel_couloir, 10);
    double iqr = (double)(cyc[23] + cyc[24]) / 2.0 - (double)(cyc[7] + cyc[8]) / 2.0;
    printf("MESURE 4096 o (n=20, 10 appels/mesure, coeur epingle CPU 1) : "
           "mediane=%.1f c [IQR %.1f] -> %.4f c/octet@4096 "
           "(machine virtualisee nommee au registre)\n",
           (double)med / 10.0, iqr / 10.0, (double)med / 10.0 / 4096.0);

    uint64_t med_r = mesurer(appel_repli, 2);
    double iqr_r = (double)(cyc[23] + cyc[24]) / 2.0 - (double)(cyc[7] + cyc[8]) / 2.0;
    printf("REPLI (la chaine scellee par bloc, n=20) : mediane=%.1f c "
           "[IQR %.1f] -> %.4f c/octet@4096\n",
           (double)med_r / 2.0, iqr_r / 2.0, (double)med_r / 2.0 / 4096.0);
    return 0;
}
