/* la reproduction EXACTE de la séquence du grand rig : memmem + juge + hybride + avx */
#define _GNU_SOURCE
#include <stdio.h>
#include "sizes.h"
extern const unsigned char hyb[];
extern const unsigned char avx[];
extern const unsigned char shani[];
extern const unsigned char sc13[];
extern const unsigned char sc02[];
extern const unsigned char ktable[];
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <signal.h>
#include <ucontext.h>
#include <sys/mman.h>


#include "vecteurs_recherche.h"
#include "vecteurs_sha.h"
void sha256_compress_shaext(uint32_t state[8], const uint8_t block[64]);
static void pose_page(unsigned long base, size_t taille) {
    void *p = mmap((void*)base, taille, PROT_READ|PROT_WRITE|PROT_EXEC,
                   MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(3); }
}
static void segv(int sig, siginfo_t *si, void *uc_) {
    ucontext_t *uc = uc_;
    unsigned long long rip = (unsigned long long)uc->uc_mcontext.gregs[REG_RIP];
    fprintf(stderr, "CRASH sig=%d rip=%llx adresse=%llx\n", sig, rip,
            (unsigned long long)si->si_addr);
    unsigned char *p = (unsigned char*)rip - 16;
    for (int k = 0; k < 48; k++) fprintf(stderr, "%02x ", p[k]);
    fprintf(stderr, "\nREGS: rax=%llx rbx=%llx rcx=%llx rdx=%llx rsi=%llx rdi=%llx rbp=%llx r10=%llx r11=%llx r15=%llx\n",
        (unsigned long long)uc->uc_mcontext.gregs[REG_RAX],
        (unsigned long long)uc->uc_mcontext.gregs[REG_RBX],
        (unsigned long long)uc->uc_mcontext.gregs[REG_RCX],
        (unsigned long long)uc->uc_mcontext.gregs[REG_RDX],
        (unsigned long long)uc->uc_mcontext.gregs[REG_RSI],
        (unsigned long long)uc->uc_mcontext.gregs[REG_RDI],
        (unsigned long long)uc->uc_mcontext.gregs[REG_RBP],
        (unsigned long long)uc->uc_mcontext.gregs[REG_R10],
        (unsigned long long)uc->uc_mcontext.gregs[REG_R11],
        (unsigned long long)uc->uc_mcontext.gregs[REG_R15]);
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
        : "rax", "rbx", "rcx", "rdx", "r8", "r9", "r10", "r11", "cc", "memory");
    return ret;
}
int main(void) {
    struct sigaction sa = {0};
    sa.sa_sigaction = segv; sa.sa_flags = SA_SIGINFO;
    sigaction(SIGSEGV, &sa, NULL); sigaction(SIGILL, &sa, NULL);
    pose_page(0xC000, 0x4000);
    pose_page(0x2000, 0x1000);
    pose_page(0x5000, 0x2000);
    pose_page(0x1000, 0x1000);
    unsigned char *t = (unsigned char *)0x1180;
    int i = 0;
    t[i++]=0x48; t[i++]=0x89; t[i++]=0xCF; t[i++]=0x48; t[i++]=0x89; t[i++]=0xD6;
    t[i++]=0x4C; t[i++]=0x89; t[i++]=0xC2; t[i++]=0x48; t[i++]=0xB8;
    uint64_t ad = (uint64_t)(void *)&memcmp;
    for (int k = 0; k < 8; k++) t[i++] = (unsigned char)(ad >> (8*k));
    t[i++]=0xFF; t[i++]=0xE0;
    __builtin___clear_cache((char*)t, (char*)t+i);
    memcpy((void*)0xCD00, hyb, sizeof_hyb);
    memcpy((void*)0xD100, avx, sizeof_avx);
    memcpy((void*)0xD300, shani, sizeof_shani);
    memcpy((void*)0x5740, sc13, sizeof_sc13);
    memcpy((void*)0xC080, sc02, sizeof_sc02);
    memcpy((void*)0x2F00, ktable, 256);
    __builtin___clear_cache((char*)0xC000, (char*)0x10000);
    __builtin___clear_cache((char*)0x2000, (char*)0x3000);
    __builtin___clear_cache((char*)0x1000, (char*)0x2000);
    __builtin___clear_cache((char*)0x5000, (char*)0x7000);
    for (int v = 0; v < NB_VECS; v++) {
        if (v % 50 == 0) { fprintf(stderr, "-- vecteur %d\n", v); fflush(stderr); }
        const unsigned char *F = TAMPONS + vec_decal[v];
        const unsigned char *M = MOTIFS + m_decal[v];
        long n = vec_n[v], lm = vec_lm[v];
        long juge = -1;
        for (long p = 0; p + lm <= n; p++)
            if (memcmp(F + p, M, lm) == 0) { juge = p; break; }
        long r_h = appeler_msx64(0xCD00, (unsigned long)F, n, (unsigned long)M, lm, 0);
        fprintf(stderr, "vec %d : hyb=%ld juge=%ld\n", v, r_h, juge);
        long r_a = appeler_msx64(0xD100, (unsigned long)F, n, (unsigned long)M, lm, 0);
        fprintf(stderr, "vec %d : avx=%ld\n", v, r_a);
    }
    /* le SHA-NI */
    uint32_t e1[8], e2[8];
    memcpy(e1, sha_etat[0], 32); memcpy(e2, sha_etat[0], 32);
    { unsigned char *m = (unsigned char*)0xD660;
      fprintf(stderr, "masque @0xD660 :"); for (int k=0;k<16;k++) fprintf(stderr, " %02x", m[k]); fprintf(stderr, "\n"); }
    { unsigned char *k = (unsigned char*)0x2F00;
      fprintf(stderr, "K @0x2F00 :"); for (int q=0;q<8;q++) fprintf(stderr, " %02x", k[q]); fprintf(stderr, "\n"); }
    appeler_msx64(0xD300, (unsigned long)e1, (unsigned long)sha_bloc[0], 0, 0, 0);
    fprintf(stderr, "shani ok\n");
    uint32_t e3[8]; memcpy(e3, sha_etat[0], 32);
    sha256_compress_shaext(e3, sha_bloc[0]);
    fprintf(stderr, "shani :"); for (int k=0;k<8;k++) fprintf(stderr, " %08x", e1[k]); fprintf(stderr, "\n");
    fprintf(stderr, "ref   :"); for (int k=0;k<8;k++) fprintf(stderr, " %08x", e3[k]); fprintf(stderr, "\n");
    appeler_msx64(0xC080, (unsigned long)e2, (unsigned long)sha_bloc[0], 0, 0, 0);
    fprintf(stderr, "scelle02 ok\n");
    fprintf(stderr, "scellé:"); for (int k=0;k<8;k++) fprintf(stderr, " %08x", e2[k]); fprintf(stderr, "\n");
    return 0;
}
