/* cgp_oracle_u02.c — L'ORACLE ÉQUIVALENT DU BRAS C+G+ (3lmyfb2xa, la vague
   11) — l'unité 2 (loupe-02 × C) : LE DIFFÉRENTIEL DE L'ORACLE DU BRAS T
   porté À LA PIÈCE COMPILÉE loupe-02-c.c incluse TELLE QUELLE — les MÊMES
   QUATRE FICHIERS (les trois témoins + le scellé proxy.exe lu en copie),
   les MÊMES DÉCALAGES (les listes pré-générées par le juge à la MÊME
   GRAINE 20261114, la même consommation du rng), CHAQUE décalage une
   épreuve jugée par le modèle indépendant — le volume ÉGAL au bras T :
   2032 décalages (2 + 24 + 1003 + 1003).

   Les SHIMS : copiés du harnais de campagne epreuve_posix.c du bras C
   (unite-02-C/epreuves — le vrai prototype SetFilePointerEx À LA VALEUR,
   le tiroir d'échec ReadFile) ; le tiroir reste DÉSARMÉ : le
   différentiel n'arme aucun échec (les scénarios d'échec vivent à
   l'épreuve de contrat de la liste C, reconduite).

   Entrée : cgp-decales-u02.txt — une ligne par fichier
   « <nom> <dec1>,<dec2>,… » (le juge les pré-génère).
   Sortie : les lignes OUVRIR/EPREUVE, le juge cgp_juge_u02.py confronte. */
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
#include "loupe-02-c.c"          /* la pièce de l'unité 2 — TELLE QUELLE */

static DWORD last_error = 0;
int lire_echec_dans = -1;        /* le tiroir E4 : -1 désarmé */

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

/* le VRAI prototype : l'union À LA VALEUR (l'écart nommé du kit 01) */
BOOL SetFilePointerEx(HANDLE hFile, LARGE_INTEGER liDistanceToMove, LARGE_INTEGER* lpNewFilePointer, DWORD dwMoveMethod) {
    int fd = (int)(uintptr_t)hFile;
    off_t result;
    if (dwMoveMethod == FILE_BEGIN) {
        result = lseek(fd, liDistanceToMove.QuadPart, SEEK_SET);
    } else {
        result = lseek(fd, liDistanceToMove.QuadPart, SEEK_CUR);
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
    if (lire_echec_dans == 0) {          /* le tiroir E4 : CE refus-ci */
        last_error = ERROR_ACCESS_DENIED;
        lire_echec_dans = -1;
        return FALSE;
    }
    if (lire_echec_dans > 0) {
        --lire_echec_dans;               /* pas encore ce refus-ci */
    }
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

static long long appeler_ouvrir(const char* nom_ascii) {
    static uint8_t tampon_chemin[528];
    for (int i = 0; i < 528; ++i) tampon_chemin[i] = 0;
    for (int i = 0; nom_ascii[i]; ++i) {
        tampon_chemin[i * 2] = (uint8_t)nom_ascii[i];
        tampon_chemin[i * 2 + 1] = 0;
    }
    return loupe_01_ouvrir(tampon_chemin);
}

int main(void) {
    setlocale(LC_ALL, "C");
    FILE* f = fopen("cgp-decales-u02.txt", "r");
    if (!f) {
        fprintf(stderr, "[oracle-u02] REFUS DÉCALAGES-ABSENTS : "
                        "cgp-decales-u02.txt (le juge --prepare d'abord)\n");
        return 2;
    }
    char nom[256];
    char decs[65536];
    /* le journal d'édition VIERGE (BSS) : le différentiel du bras T porte
       journal vide — le modèle modele_fenetre(contenu, dec, []) */
    while (fscanf(f, "%255s %65535s", nom, decs) == 2) {
        long long r = appeler_ouvrir(nom);
        printf("OUVRIR %s rax=%lld rempl=%u\n", nom, r, champ_dword(552));
        fflush(stdout);
        char* ctx = NULL;
        for (char* t = strtok_r(decs, ",", &ctx); t;
             t = strtok_r(NULL, ",", &ctx)) {
            uint64_t dec = strtoull(t, NULL, 10);
            long long rl = loupe_02_lire(dec);
            printf("EPREUVE %s dec=%llu rax=%lld rempl=%u vue=%llu "
                   "curseur=%llu tampon=",
                   nom, (unsigned long long)dec, rl, champ_dword(552),
                   (unsigned long long)champ_qword(536),
                   (unsigned long long)champ_qword(544));
            hex_print((const uint8_t*)cadre + 568, 384);
            printf("\n");
        }
        loupe_03_fermer();
    }
    fclose(f);
    return 0;
}
