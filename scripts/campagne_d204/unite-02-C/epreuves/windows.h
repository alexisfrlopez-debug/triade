#include <stdint.h>
#ifndef _WINDOWS_H_
#define _WINDOWS_H_

typedef int BOOL;
#define TRUE 1
#define FALSE 0
typedef void* HANDLE;
typedef uint32_t DWORD;
typedef uint16_t WORD;
typedef const uint16_t* LPCWSTR;  /* le labo : 2 octets, comme au Windows */
typedef uint32_t* LPDWORD;
typedef int64_t LONGLONG;

typedef struct {
    uint64_t QuadPart;
} LARGE_INTEGER;

#define INVALID_HANDLE_VALUE ((HANDLE)-1)
#define GENERIC_READ         (0x80000000)
#define GENERIC_WRITE        (0x40000000)
#define FILE_SHARE_READ      (1)
#define OPEN_EXISTING        (3)
#define FILE_BEGIN           (0)
#define FILE_ATTRIBUTE_NORMAL (0)
#define ERROR_FILE_NOT_FOUND  (2)
#define ERROR_PATH_NOT_FOUND  (3)
#define ERROR_ACCESS_DENIED  (5)
#define ERROR_SHARING_VIOLATION (32)
#define MAX_PATH             (260)

HANDLE CreateFileW(LPCWSTR lpFileName, DWORD dwDesiredAccess, DWORD dwShareMode, void* lpSecurityAttributes, DWORD dwCreationDisposition, DWORD dwFlagsAndAttributes, HANDLE hTemplateFile);
BOOL GetFileSizeEx(HANDLE hFile, LARGE_INTEGER* lpFileSize);
BOOL SetFilePointerEx(HANDLE hFile, LARGE_INTEGER liDistanceToMove, LARGE_INTEGER* lpNewFilePointer, DWORD dwMoveMethod);  /* À LA VALEUR — le vrai prototype (l'écart nommé du kit 01 : jamais éprouvée là) */
BOOL ReadFile(HANDLE hFile, void* lpBuffer, DWORD nNumberOfBytesToRead, DWORD* lpNumberOfBytesRead, void* lpOverlapped);
BOOL CloseHandle(HANDLE hObject);
DWORD GetLastError(void);

#endif // _WINDOWS_H_
