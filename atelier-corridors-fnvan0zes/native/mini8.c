#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/mman.h>
extern const unsigned char shani[];

extern const unsigned shani_diag_taille;
static void pose_page(unsigned long b, size_t t) {
    void *p = mmap((void*)b, t, PROT_READ|PROT_WRITE|PROT_EXEC,
                   MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); _exit(3); }
}
static long appeler_msx64(unsigned long fn, unsigned long rcx_v,
                          unsigned long rdx_v, unsigned long r8_v,
                          unsigned long r9_v, unsigned long pile_v) {
    long ret;
    __asm__ volatile(
        "subq $0x30, %%rsp\n\tmovq %6, 0x20(%%rsp)\n\tmovq %2, %%rcx\n\t"
        "movq %3, %%rdx\n\tmovq %4, %%r8\n\tmovq %5, %%r9\n\tcallq *%1\n\t"
        "movq %%rax, %0\n\taddq $0x30, %%rsp\n\t"
        : "=r"(ret) : "r"(fn), "r"(rcx_v), "r"(rdx_v), "r"(r8_v), "r"(r9_v), "r"(pile_v)
        : "rax", "rbx", "rcx", "rdx", "r8", "r9", "r10", "r11", "cc", "memory");
    return ret;
}
int main(void) {
    pose_page(0x2000, 0x1000); pose_page(0x1000, 0x1000); pose_page(0xD000, 0x1000);
    memcpy((void*)0xD300, shani, shani_diag_taille);
    __builtin___clear_cache((char*)0xD000, (char*)0xE000);
    static const uint32_t K[64] = {
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
    memcpy((void*)0x2F00, K, 256);
    __builtin___clear_cache((char*)0x2000, (char*)0x3000);
    uint32_t etat[44] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                         0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    uint8_t bloc[64]; for (int i = 0; i < 64; i++) bloc[i] = (uint8_t)(i*7+3);
    appeler_msx64(0xD300, (unsigned long)etat, (unsigned long)bloc, 0, 0, 0);
    printf("N ABEF: %08x %08x %08x %08x\n", etat[0],etat[1],etat[2],etat[3]);
    printf("N CDGH: %08x %08x %08x %08x\n", etat[4],etat[5],etat[6],etat[7]);
    printf("N S[0]: %08x %08x %08x %08x\n", etat[8],etat[9],etat[10],etat[11]);
    printf("N S[1]: %08x %08x %08x %08x\n", etat[12],etat[13],etat[14],etat[15]);
    printf("N S[2]: %08x %08x %08x %08x\n", etat[16],etat[17],etat[18],etat[19]);
    printf("N S[3]: %08x %08x %08x %08x\n", etat[20],etat[21],etat[22],etat[23]);
    printf("N S0@gen0: %08x %08x %08x %08x\n", etat[36],etat[37],etat[38],etat[39]);

    return 0;
}
