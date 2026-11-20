/* LE SHIM POSIX du labo (le rig du bras C : gcc -O2 natif, la cible seule change) */
#ifndef SHIM05
#define SHIM05
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
typedef void* HANDLE;
typedef int BOOL;
typedef struct { long long QuadPart; } LARGE_INTEGER;
typedef unsigned long DWORD;
typedef unsigned char BYTE;
#define FILE_BEGIN 0
#define INVALID_HANDLE_VALUE ((HANDLE)-1)
static BOOL SetFilePointerEx(HANDLE h, LARGE_INTEGER d, void *o, int w) {
    return fseek((FILE*)h, d.QuadPart, SEEK_SET) == 0;
}
static BOOL ReadFile(HANDLE h, void *buf, unsigned long long n,
                     DWORD *lu, void *o) {
    size_t r = fread(buf, 1, (size_t)n, (FILE*)h);
    *lu = (DWORD)r;
    return 1;
}
static DWORD GetLastError(void) { return 1117; }
#endif
