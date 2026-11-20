#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <signal.h>
#include <ucontext.h>
#include <sys/mman.h>
extern const unsigned char avx[];
extern const unsigned char sc13[];
#include "vecteurs_recherche.h"
static void pose_page(unsigned long base, size_t taille) {
    void *p = mmap((void*)base, taille, PROT_READ|PROT_WRITE|PROT_EXEC,
                   MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(3); }
}
static void segv(int sig, siginfo_t *si, void *uc_) {
    ucontext_t *uc = uc_;
    fprintf(stderr, "CRASH à rip=%llx adresse=%llx\n",
            (unsigned long long)uc->uc_mcontext.gregs[REG_RIP],
            (unsigned long long)si->si_addr);
    _exit(9);
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
        : "rax", "rcx", "rdx", "r8", "r9", "r10", "r11", "memory");
    return ret;
}
int main(void) {
    struct sigaction sa = {0};
    sa.sa_sigaction = segv; sa.sa_flags = SA_SIGINFO;
    sigaction(SIGSEGV, &sa, NULL); sigaction(SIGILL, &sa, NULL);
    pose_page(0x2000, 0x1000);
    pose_page(0x5000, 0x2000);
    pose_page(0xC000, 0x4000);
    /* le trampoline memcmp */
    pose_page(0x1000, 0x1000);
    unsigned char *t = (unsigned char *)0x1180;
    int i = 0;
    t[i++]=0x48; t[i++]=0x89; t[i++]=0xCF;
    t[i++]=0x48; t[i++]=0x89; t[i++]=0xD6;
    t[i++]=0x4C; t[i++]=0x89; t[i++]=0xC2;
    t[i++]=0x48; t[i++]=0xB8;
    uint64_t ad = (uint64_t)(void *)&memcmp;
    for (int k = 0; k < 8; k++) t[i++] = (unsigned char)(ad >> (8*k));
    t[i++]=0xFF; t[i++]=0xE0;
    __builtin___clear_cache((char*)t, (char*)t+i);
    memcpy((void*)0xD100, avx, 4096);
    __builtin___clear_cache((char*)0xC000, (char*)0x10000);
    long r = appeler_msx64(0xD100, (unsigned long)(TAMPONS + vec_decal[0]),
                           vec_n[0], (unsigned long)(MOTIFS + m_decal[0]),
                           vec_lm[0], 0);
    printf("avxride(vec 0) = %ld (juge %ld)\n", r, (long)-1);
    return 0;
}
