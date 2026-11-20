/* cgp_oracle_u01.c — L'ORACLE ÉQUIVALENT DU BRAS C+G+ (3lmyfb2xa, la vague
   11) — l'unité 1 (loupe-01 × C) : LES MÊMES DOUZE ÉPREUVES DE CONTRAT QUE
   L'ORACLE DU BRAS T (oracle_unite01_v180 : V1 les quatre témoins, V2 les
   trois rejets d'OS, V3 la borne + la session double + le chemin long, V4
   la falsification demandée), portées À LA PIÈCE COMPILÉE loupe-01-c.c
   incluse TELLE QUELLE (jamais touchée).

   Les SHIMS : copiés du harnais de campagne epreuve_posix.c du bras C
   (unite-01-C/epreuves — la phase tests-c du workflow, conservés tels
   quels) : CreateFileW à la sémantique flock, GetFileSizeEx,
   SetFilePointerEx, ReadFile, CloseHandle, GetLastError.

   L'ÉCART NOMMÉ (E3) : le harnais de campagne nommait le refus d'ACL
   « ABSENT » (il ne l'armait pas proprement) ; ici l'épreuve T est portée
   INTÉGRALEMENT — le témoin d'accès refusé est armé par chmod 000 (le
   refus EACCES du propriétaire même), le verdict attendu -6 SYSTÈME.

   L'ÉCART NOMMÉ (P1) : le chemin de 260 caractères sans NUL — la pièce
   notée T répond -5 (l'argument invalide de l'OS émulé) ; la pièce C au
   POSIX répond -2 (ENAMETOOLONG → PATH_NOT_FOUND → ABSENT — la sémantique
   du shim, l'état de campagne constaté à observe.txt). Le juge épingle le
   verdict POSIX -2, la divergence à T NOMMÉE au rapport.

   Sortie : les lignes EPREUVE/ETAT/COMPTEUR/FALSIF, le juge
   cgp_juge_u01.py (le modèle indépendant Python) confronte. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/file.h>
#include <errno.h>
#include <locale.h>

#include "windows.h"
#include "loupe-01-c.c"          /* la pièce de l'unité 1 — TELLE QUELLE */

static DWORD last_error = 0;
static long compteur_close = 0;  /* la poignée refermée AVANT le retour */

HANDLE CreateFileW(LPCWSTR lpFileName, DWORD dwDesiredAccess, DWORD dwShareMode, void* lpSecurityAttributes, DWORD dwCreationDisposition, DWORD dwFlagsAndAttributes, HANDLE hTemplateFile) {
    if (dwDesiredAccess != (GENERIC_READ | GENERIC_WRITE) || dwCreationDisposition != OPEN_EXISTING) {
        last_error = ERROR_ACCESS_DENIED;
        return INVALID_HANDLE_VALUE;
    }
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
    compteur_close++;
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

static void hex_print(const uint8_t* data, size_t len) {
    for (size_t i = 0; i < len; ++i) printf("%02x", data[i]);
}

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

static long long appeler(const char* nom_ascii) {
    static uint8_t tampon_chemin[528];
    for (int i = 0; i < 528; ++i) tampon_chemin[i] = 0;
    for (int i = 0; nom_ascii[i]; ++i) {
        tampon_chemin[i * 2] = (uint8_t)nom_ascii[i];
        tampon_chemin[i * 2 + 1] = 0;
    }
    return loupe_01_ouvrir(tampon_chemin);
}

/* UNE ligne EPREUVE : l'état ENTIER jugé par le modèle indépendant */
static void ligne_epreuve(const char* nom, long long rax) {
    printf("EPREUVE %s rax=%lld chemin=", nom, rax);
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

    /* ---- V1 : les quatre témoins (une session par épreuve, fermée) ---- */
    const char* temoins[] = {"temoin-1.bin", "temoin-384.bin",
                             "temoin-3f.bin", "vide.bin"};
    for (int i = 0; i < 4; ++i) {
        ligne_epreuve(temoins[i], appeler(temoins[i]));
        loupe_03_fermer();
    }

    /* ---- V2 : les trois rejets d'OS ------------------------------------ */
    ligne_epreuve("absent-du-terrain.bin",
                  appeler("absent-du-terrain.bin"));
    {
        int fd_tenue = open("temoin-1.bin", O_RDWR);
        flock(fd_tenue, LOCK_EX | LOCK_NB);   /* la tenue sans partage */
        ligne_epreuve("temoin-1.bin", appeler("temoin-1.bin"));
        close(fd_tenue);                       /* la relâche */
    }
    {
        /* E3 ARMÉ (l'écart de campagne nommé comblé) : chmod 000 — le
           refus EACCES du propriétaire même → -6 SYSTÈME */
        int fd = open("temoin-acces-refuse.bin", O_CREAT | O_RDWR, 0644);
        write(fd, "\x00\x00\x00\x00", 4);
        close(fd);
        chmod("temoin-acces-refuse.bin", 0000);
        ligne_epreuve("temoin-acces-refuse.bin",
                      appeler("temoin-acces-refuse.bin"));
        chmod("temoin-acces-refuse.bin", 0644);
        unlink("temoin-acces-refuse.bin");
    }

    /* ---- V3 : la borne 2 Gio + 1 (le fichier réel posé épars) --------- */
    long avant_close = compteur_close;
    {
        int fd = open("geant-plus.bin", O_CREAT | O_RDWR, 0644);
        ftruncate(fd, (off_t)0x80000001);
        close(fd);
        ligne_epreuve("geant-plus.bin", appeler("geant-plus.bin"));
        unlink("geant-plus.bin");
    }
    printf("COMPTEUR CloseHandle avant=%ld apres=%ld\n",
           avant_close, compteur_close);

    /* ---- V3 : la session double (l'ancien cadre INTACT) --------------- */
    ligne_epreuve("temoin-384.bin", appeler("temoin-384.bin"));
    ligne_etat();
    ligne_epreuve("temoin-1.bin", appeler("temoin-1.bin"));  /* attendu -5 */
    loupe_03_fermer();

    /* ---- V3 : le chemin de 260 caractères sans NUL --------------------- */
    {
        static uint8_t chemin_260[528];
        for (int i = 0; i < 528; ++i) chemin_260[i] = 0;
        for (int i = 0; i < 260; ++i) {
            chemin_260[i * 2] = 'A';
            chemin_260[i * 2 + 1] = 0;
        }
        printf("EPREUVE chemin-260-sans-NUL rax=%lld chemin=",
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

    /* ---- V4 : LA FALSIFICATION DEMANDÉE (le juge lit l'état) ----------- */
    {
        long long r = appeler("temoin-384.bin");
        /* la taille mutée 384 → 385 AU CADRE (l'écran attendu diverge) */
        uint8_t mute[8];
        for (int i = 0; i < 8; ++i) mute[i] = (uint8_t)((385ULL) >> (8 * i));
        for (int i = 0; i < 8; ++i) cadre[520 + i] = mute[i];
        printf("FALSIF rax=%lld taille_modele=384 taille_lue=%llu\n",
               r, (unsigned long long)champ_qword(520));
        loupe_03_fermer();
    }

    return 0;
}
