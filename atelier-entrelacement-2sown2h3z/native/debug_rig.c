#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
#include "donnees_rig.h"
#include "rig_octets.h"
#define COULOIR 0xF800
int main(void) {
    mmap((void*)0xC000, 0x4000, 7, 0x32, -1, 0);
    mmap((void*)0x500000, 0x21000, 3, 0x32, -1, 0);
    mmap((void*)0x70000, 0x10000, 3, 0x32, -1, 0);
    memcpy((void*)0xDF00, S16_OCTETS, S16_TAILLE);
    memcpy((void*)0xDFC0, S17_OCTETS, S17_TAILLE);
    memcpy((void*)COULOIR, COULOIR_OCTETS, COULOIR_TAILLE);
    memcpy((void*)0x500200, CLES, 176);
    memcpy((void*)0x501000, COMPTEURS, 4096);
    memcpy((void*)0x502000, CLAIR, 4096);
    memcpy((void*)0x508000, TABLE, 4096);
    long rax;
    __asm__ volatile(
        "movq $0x500200, %%rcx;"
        "movq $0x501000, %%rdx;"
        "movq $0x502000, %%r8;"
        "movq $0x503000, %%r9;"
        "movq $1, %%r10;"
        "movq $256, %%r11;"
        "movq $0xF800, %%rax; callq *%%rax;"
        : "=a"(rax) :: "rcx", "rdx", "r8", "r9", "r10", "r11", "rdi", "rsi",
           "rbx", "r12", "r13", "r14", "r15", "memory", "cc");
    printf("rax=%ld (0x%lx)\n", rax, (unsigned long)rax);
    unsigned char *ct = (unsigned char*)0x503000;
    printf("ct[0..15] = ");
    for (int i = 0; i < 16; i++) printf("%02x", ct[i]);
    printf("\nct[4080..4095] = ");
    for (int i = 4080; i < 4096; i++) printf("%02x", ct[i]);
    printf("\ntag = ");
    for (int i = 4096; i < 4112; i++) printf("%02x", ct[i]);
    printf("\n");
    return 0;
}
