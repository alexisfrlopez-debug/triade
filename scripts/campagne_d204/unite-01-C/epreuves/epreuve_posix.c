/* epreuve_posix.c — LE HARNAIS D'ÉPREUVE du bras C (loupe-01 × C, la
   campagne D204) — LA PHASE tests-c DU WORKFLOW.
   Les SHIMS (CreateFileW à la sémantique de partage flock, GetFileSizeEx,
   SetFilePointerEx, ReadFile, CloseHandle, GetLastError) : LIVRÉS PAR LA
   PHASE tests-c (l'appel instrumenté), conservés ici TELS QUELS.
   Le MAIN : COMPLÉTÉ PAR LE LABO (l'écart nommé au journal — l'édition
   livrée méconnaissait l'interface de la pièce : des accesseurs fantômes
   loupe_01_taille/cadre/panneau, l'encodage UTF-16 cassé, aucun vecteur
   armé — ni verrou tenu, ni géant épars, ni session double) — la pièce
   est incluse TELLE QUELLE, jamais touchée ; D122 : l'épreuve du labo
   rejoue la LOGIQUE au POSIX, le run terrain appartient au développeur. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/file.h>
#include <errno.h>
#include <wchar.h>
#include <locale.h>

#include "windows.h"
#include "loupe-01-c.c"

static DWORD last_error = 0;

HANDLE CreateFileW(LPCWSTR lpFileName, DWORD dwDesiredAccess, DWORD dwShareMode, void* lpSecurityAttributes, DWORD dwCreationDisposition, DWORD dwFlagsAndAttributes, HANDLE hTemplateFile) {
    if (dwDesiredAccess != (GENERIC_READ | GENERIC_WRITE) || dwCreationDisposition != OPEN_EXISTING) {
        last_error = ERROR_ACCESS_DENIED;
        return INVALID_HANDLE_VALUE;
    }

    /* le décodage UTF-16LE → octets (le labo : wcstombs lisait des
       wchar_t de 4 octets au POSIX — la copie manuelle des octets bas,
       arrêt au NUL, comme la spécification le demandait) */
    char path_utf8[MAX_PATH * 2 + 1];
    size_t n = 0;
    const uint16_t* p16 = (const uint16_t*)lpFileName;
    while (n < MAX_PATH && p16[n] != 0) {
        path_utf8[n] = (char)(p16[n] & 0xFF);
        ++n;
    }
    path_utf8[n] = '\0';

    int fd = open(path_utf8, O_RDWR);
    if (fd == -1) {
        if (errno == ENOENT) last_error = ERROR_FILE_NOT_FOUND;
        else if (errno == ENAMETOOLONG) last_error = ERROR_PATH_NOT_FOUND;
        else last_error = ERROR_ACCESS_DENIED;
        return INVALID_HANDLE_VALUE;
    }

    if (flock(fd, LOCK_EX | LOCK_NB) == -1) {
        close(fd);
        last_error = ERROR_SHARING_VIOLATION;
        return INVALID_HANDLE_VALUE;
    }
    return (HANDLE)(uintptr_t)fd;
}

BOOL GetFileSizeEx(HANDLE hFile, LARGE_INTEGER* lpFileSize) {
    int fd = (int)(uintptr_t)hFile;
    struct stat st;
    if (fstat(fd, &st) == -1) {
        last_error = ERROR_ACCESS_DENIED;
        return FALSE;
    }
    lpFileSize->QuadPart = st.st_size;
    return TRUE;
}

BOOL SetFilePointerEx(HANDLE hFile, LARGE_INTEGER* liDistanceToMove, LARGE_INTEGER* lpNewFilePointer, DWORD dwMoveMethod) {
    int fd = (int)(uintptr_t)hFile;
    off_t result;
    if (dwMoveMethod == FILE_BEGIN) {
        result = lseek(fd, liDistanceToMove->QuadPart, SEEK_SET);
    } else {
        result = lseek(fd, liDistanceToMove->QuadPart, SEEK_CUR);
    }
    if (result == -1) {
        last_error = ERROR_ACCESS_DENIED;
        return FALSE;
    }
    if (lpNewFilePointer) lpNewFilePointer->QuadPart = result;
    return TRUE;
}

BOOL ReadFile(HANDLE hFile, void* lpBuffer, DWORD nNumberOfBytesToRead, DWORD* lpNumberOfBytesRead, void* lpOverlapped) {
    int fd = (int)(uintptr_t)hFile;
    ssize_t total_read = 0;
    while (total_read < nNumberOfBytesToRead) {
        ssize_t bytes_read = read(fd, (char*)lpBuffer + total_read, nNumberOfBytesToRead - total_read);
        if (bytes_read == -1) {
            if (errno == EINTR) continue;
            last_error = ERROR_ACCESS_DENIED;
            return FALSE;
        }
        if (bytes_read == 0) break;
        total_read += bytes_read;
    }
    if (lpNumberOfBytesRead) *lpNumberOfBytesRead = total_read;
    return TRUE;
}

BOOL CloseHandle(HANDLE hObject) {
    int fd = (int)(uintptr_t)hObject;
    if (flock(fd, LOCK_UN) == -1) {
        last_error = ERROR_ACCESS_DENIED;
        return FALSE;
    }
    close(fd);
    return TRUE;
}

DWORD GetLastError(void) {
    DWORD err = last_error;
    last_error = 0;
    return err;
}

void hex_print(const uint8_t* data, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        printf("%02x", data[i]);
    }
}

/* --- LE MAIN (complété par le labo — l'écart nommé) -------------------- */

/* les champs du cadre aux offsets du plan (la pièce les écrit) */
static uint64_t champ_qword(size_t off) {
    uint64_t v = 0;
    for (int i = 7; i >= 0; --i) v = (v << 8) | (uint8_t)cadre[off + i];
    return v;
}
static uint32_t champ_dword(size_t off) {
    uint32_t v = 0;
    for (int i = 3; i >= 0; --i) v = (v << 8) | (uint8_t)cadre[off + i];
    return v;
}

/* l'appel du juge : le chemin en UTF-16LE + NUL, un tampon de marge nulle */
static long long appeler(const char* nom_ascii) {
    static uint8_t tampon_chemin[528];
    for (int i = 0; i < 528; ++i) tampon_chemin[i] = 0;
    for (int i = 0; nom_ascii[i]; ++i) {
        tampon_chemin[i * 2] = (uint8_t)nom_ascii[i];
        tampon_chemin[i * 2 + 1] = 0;
    }
    return loupe_01_ouvrir(tampon_chemin);
}

static void ligne_vecteur(const char* nom, long long rax) {
    printf("VECTEUR %s rax=%lld chemin=", nom, rax);
    hex_print((const uint8_t*)cadre, 520);
    printf(" taille=%llu poignee=%llu vue=%llu curseur=%llu rempl=%u tampon=",
           (unsigned long long)champ_qword(520),
           (unsigned long long)champ_qword(528),
           (unsigned long long)champ_qword(536),
           (unsigned long long)champ_qword(544), champ_dword(552));
    hex_print((const uint8_t*)cadre + 568, 384);
    printf(" panneau=");
    hex_print((const uint8_t*)panneau, 48);
    printf("\n");
}

static void ligne_etat(void) {
    printf("ETAT cadre=");
    hex_print((const uint8_t*)cadre, 960);
    printf(" panneau=");
    hex_print((const uint8_t*)panneau, 48);
    printf("\n");
}

int main(void) {
    setlocale(LC_ALL, "C");

    /* ---- V1 : les quatre témoins, loupe_03 entre chacun ---- */
    const char* temoins[] = {"temoin-1.bin", "temoin-384.bin",
                             "temoin-3f.bin", "vide.bin"};
    for (int i = 0; i < 4; ++i) {
        ligne_vecteur(temoins[i], appeler(temoins[i]));
        loupe_03_fermer();
    }

    /* ---- V2 : absent, puis verrouillé (le harnais TIENT sans partage) ---- */
    ligne_vecteur("absent-du-terrain.bin",
                  appeler("absent-du-terrain.bin"));
    {
        int fd_tenue = open("temoin-1.bin", O_RDWR);
        flock(fd_tenue, LOCK_EX | LOCK_NB);   /* la tenue sans partage */
        ligne_vecteur("temoin-1.bin", appeler("temoin-1.bin"));
        close(fd_tenue);                       /* la relâche */
    }

    /* ---- V3 : la borne 2 Gio + 1 (un fichier réel posé épars) ---- */
    {
        int fd = open("geant-plus.bin", O_CREAT | O_RDWR, 0644);
        ftruncate(fd, (off_t)0x80000001);
        close(fd);
        ligne_vecteur("geant-plus.bin", appeler("geant-plus.bin"));
        unlink("geant-plus.bin");
    }

    /* ---- V3 : la session double (l'ancien cadre INTACT) ---- */
    ligne_vecteur("temoin-384.bin", appeler("temoin-384.bin"));
    ligne_etat();
    ligne_vecteur("temoin-1.bin", appeler("temoin-1.bin"));  /* attendu -5 */
    loupe_03_fermer();

    /* ---- V3 : le chemin de 260 caractères sans NUL ---- */
    {
        static uint8_t chemin_260[528];
        for (int i = 0; i < 528; ++i) chemin_260[i] = 0;
        for (int i = 0; i < 260; ++i) {
            chemin_260[i * 2] = 'A';
            chemin_260[i * 2 + 1] = 0;
        }
        printf("VECTEUR chemin-260-sans-NUL rax=%lld chemin=",
               loupe_01_ouvrir(chemin_260));
        hex_print((const uint8_t*)cadre, 520);
        printf(" taille=%llu poignee=%llu vue=%llu curseur=%llu rempl=%u tampon=",
               (unsigned long long)champ_qword(520),
               (unsigned long long)champ_qword(528),
               (unsigned long long)champ_qword(536),
               (unsigned long long)champ_qword(544), champ_dword(552));
        hex_print((const uint8_t*)cadre + 568, 384);
        printf(" panneau=");
        hex_print((const uint8_t*)panneau, 48);
        printf("\n");
    }

    return 0;
}
