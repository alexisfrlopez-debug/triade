#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>
extern const unsigned char hyb[];
extern const unsigned char avx[];
extern const unsigned char shani[];
extern const unsigned char sc13[]; extern const unsigned char sc02[]; extern const unsigned char ktable[];
static void pose_page(unsigned long base, size_t taille) {
    void *p = mmap((void*)base, taille, PROT_READ|PROT_WRITE|PROT_EXEC,
                   MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(3); }
}
static long appeler_msx64(unsigned long fn, unsigned long rcx_v,
                          unsigned long rdx_v, unsigned long r8_v,
                          unsigned long r9_v, unsigned long pile_v) {
    long ret;
    __asm__ volatile(
        "subq $0x30, %%rsp\n\t"
        "movq %6, 0x20(%%rsp)\n\t"
        "movq %2, %%rcx\n\t"
        "movq %3, %%rdx\n\t"
        "movq %4, %%r8\n\t"
        "movq %5, %%r9\n\t"
        "callq *%1\n\t"
        "movq %%rax, %0\n\t"
        "addq $0x30, %%rsp\n\t"
        : "=r"(ret)
        : "r"(fn), "r"(rcx_v), "r"(rdx_v), "r"(r8_v), "r"(r9_v),
          "r"(pile_v)
        : "rax", "rbx", "rcx", "rdx", "r8", "r9", "r10", "r11", "cc", "memory");
    return ret;
}
static unsigned char tamp[4096], motif[32];
int main(void) {
    pose_page(0xC000, 0x4000); pose_page(0x2000, 0x1000);
    pose_page(0x5000, 0x2000); pose_page(0x1000, 0x1000);
    unsigned char *t = (unsigned char *)0x1180;
    int i = 0;
    t[i++]=0x48; t[i++]=0x89; t[i++]=0xCF; t[i++]=0x48; t[i++]=0x89; t[i++]=0xD6;
    t[i++]=0x4C; t[i++]=0x89; t[i++]=0xC2; t[i++]=0x48; t[i++]=0xB8;
    uint64_t ad = (uint64_t)(void *)&memcmp;
    for (int k = 0; k < 8; k++) t[i++] = (unsigned char)(ad >> (8*k));
    t[i++]=0xFF; t[i++]=0xE0;
    __builtin___clear_cache((char*)t, (char*)t+i);
    memcpy((void*)0xCD00, hyb, 314);
    memcpy((void*)0xD100, avx, 494);
    memcpy((void*)0xD300, shani, 880);
    memcpy((void*)0x5740, sc13, 126);
    memcpy((void*)0xC080, sc02, 387);
    memcpy((void*)0x2F00, ktable, 256);
    __builtin___clear_cache((char*)0xC000, (char*)0x10000);
    for (int k = 0; k < 4096; k++) tamp[k] = (unsigned char)(k * 31 + 7);
    for (int k = 0; k < 16; k++) motif[k] = 0xEE;
    fprintf(stderr, "l'hybride absent... "); fflush(stderr);
    long r = appeler_msx64(0xCD00, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0);
    fprintf(stderr, "= %ld\n", r); fflush(stderr);
    fprintf(stderr, "l'avx2 absent... "); fflush(stderr);
    r = appeler_msx64(0xD100, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0);
    fprintf(stderr, "= %ld\n", r); fflush(stderr);
    return 0;
}
