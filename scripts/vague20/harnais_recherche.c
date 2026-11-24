#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <immintrin.h>
static inline uint64_t rd(void){ unsigned a,d; __asm__ volatile("rdtscp":"=a"(a),"=d"(d)::"rcx"); return ((uint64_t)d<<32)|a; }
volatile long sink = 0;
int main(void){
  size_t n = 4096; unsigned char *buf = aligned_alloc(64, n); memset(buf, 0x41, n);
  int reps = 2000; uint64_t t0,t1; long acc = 0;
  for(int i=0;i<200;i++){ unsigned char nd=(unsigned char)((i*37)&0xff); acc += (long)((char*)memchr(buf, nd, n) - (char*)buf); }
  sink = acc; acc = 0;
  t0 = rd(); for(int i=0;i<reps;i++){ unsigned char nd=(unsigned char)((i*37)&0xff); acc += (long)((char*)memchr(buf, nd, n) - (char*)buf); } t1 = rd();
  sink = acc; double c_memchr = (double)(t1-t0)/reps;
  for(int i=0;i<200;i++){ __m256i v=_mm256_set1_epi8((char)((i*37)&0xff)); for(size_t o=0;o<n;o+=32){ __m256i x=_mm256_load_si256((const __m256i*)(buf+o)); int mk=_mm256_movemask_epi8(_mm256_cmpeq_epi8(x,v)); if(mk){ acc += mk; break; } } }
  sink = acc; acc = 0;
  t0 = rd();
  for(int i=0;i<reps;i++){ __m256i v=_mm256_set1_epi8((char)((i*37)&0xff)); for(size_t o=0;o<n;o+=32){ __m256i x=_mm256_load_si256((const __m256i*)(buf+o)); int mk=_mm256_movemask_epi8(_mm256_cmpeq_epi8(x,v)); if(mk){ acc += mk; break; } } }
  t1 = rd();
  sink = acc;
  printf("%.3f %.3f %ld\n", c_memchr, (double)(t1-t0)/reps, sink);
  return 0;
}
