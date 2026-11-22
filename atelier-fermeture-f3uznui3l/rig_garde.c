#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <sched.h>
static unsigned char G[] = { 0x48, 0x89, 0xd8, 0x48, 0x01, 0xd0, 0x48, 0x05, 0x38, 0x02, 0x00, 0x00, 0x48, 0x3d, 0x00, 0xe0, 0x00, 0x00, 0x72, 0x0b, 0x48, 0x3d, 0xc0, 0xe3, 0x00, 0x00, 0x73, 0x03, 0x31, 0xc0, 0xc3, 0xb8, 0xfb, 0xff, 0xff, 0xff, 0xc3 };
int main(void) {
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    sched_setaffinity(0, sizeof(m), &m);
    uint64_t t0, t1; uint32_t a, d;
    uint64_t cyc[200];
    for (int i = 0; i < 20; i++) ((void(*)(void))(void*)G);
    for (int i = 0; i < 200; i++) {
        __asm__ volatile ("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t0 = ((uint64_t)d << 32) | a;
        ((void(*)(void))(void*)G);
        __asm__ volatile ("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t1 = ((uint64_t)d << 32) | a;
        cyc[i] = t1 - t0;
    }
    for (int i = 0; i < 200; i++) for (int j = i + 1; j < 200; j++)
        if (cyc[j] < cyc[i]) { uint64_t t = cyc[i]; cyc[i] = cyc[j]; cyc[j] = t; }
    printf("garde n=200 mediane=%.1f iqr=%.1f (machine virtualisee, coeur epingle)",
           (double)(cyc[99] + cyc[100]) / 2.0,
           (double)(cyc[149] + cyc[150]) / 2.0 - (double)(cyc[49] + cyc[50]) / 2.0);
    return 0;
}
