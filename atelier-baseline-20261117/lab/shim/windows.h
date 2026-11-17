/* le shim windows.h du labo baseline — la tradition des shims de la
   campagne (V4 : « le shim ReadFile ») : les types et prototypes STRICTS
   de la liste fermée IAT D161, rien d'autre — le contrôle de compilation
   gcc -O2 -c (la syntaxe et la sémantique, jamais l'édition de liens). */
#ifndef SHIM_WINDOWS_H_LABO_BASELINE
#define SHIM_WINDOWS_H_LABO_BASELINE
#include <stdint.h>
#include <stddef.h>
typedef void* HANDLE;
typedef char* LPSTR;
typedef const char* LPCSTR;
typedef wchar_t* LPWSTR;
typedef const wchar_t* LPCWSTR;
typedef unsigned long DWORD;
typedef long LONG;
typedef long long LONGLONG;
typedef union { struct { DWORD LowPart; LONG HighPart; }; LONGLONG QuadPart; } LARGE_INTEGER;
typedef int BOOL;
#define INVALID_HANDLE_VALUE ((HANDLE)(intptr_t)-1)
#define FILE_BEGIN 0
#define GENERIC_READ 0x80000000L
#define GENERIC_WRITE 0x40000000L
#define FILE_SHARE_READ 0x00000001
#define OPEN_EXISTING 3
#define TRUE 1
#define FALSE 0
DWORD GetLastError(void);
BOOL SetFilePointerEx(HANDLE, LARGE_INTEGER, LARGE_INTEGER*, DWORD);
BOOL ReadFile(HANDLE, void*, DWORD, DWORD*, void*);
HANDLE CreateFileW(LPCWSTR, DWORD, DWORD, void*, DWORD, DWORD, void*);
#endif
/* __declspec — la surface mingw (la campagne compilait gcc mingw -O2) :
   le shim le porte en no-op d'alignement (une amorce de performance,
   jamais une sémantique) */
#define __declspec(x)
