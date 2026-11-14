/* epreuve_posix.c — LE HARNAIS D'ÉPREUVE du bras C (loupe-02 × C, la
   campagne D204) — LA PHASE tests-c DU WORKFLOW de l'unité 2.
   Les shims : ceux du kit 01 CONSERVÉS, avec DEUX écarts nommés —
   ① SetFilePointerEx déclarée À LA VALEUR (le vrai prototype Windows :
      l'union passée par valeur ; la déclaration du kit 01 la disait à
      l'POINTEUR — jamais éprouvée là, la pièce du kit 01 ne l'appelait
      pas : L'ÉCART NOMMÉ de la 284) ;
   ② le tiroir d'échec de ReadFile (lire_echec_dans : le Nième appel
      refuse, E4 du contrat — le harnais arme, la pièce ne sait rien).
   Le main : les vecteurs du contrat loupe-02:R1 — l'état DUMPÉ, le juge
   est compare_epreuve.py (le modèle indépendant Python). La pièce est
   incluse TELLE QUELLE, jamais touchée ; D122 : le labo rejoue la
   LOGIQUE au POSIX, le run terrain appartient au développeur. */
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
int lire_echec_dans = -1;        /* le tiroir E4 : -1 désarmé, N = le Nième */

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

/* L'ÉTAT DE LA LECTURE — une ligne VECTEUR : rax, rempl, le tampon 384,
   la vue et le curseur (Q3 : ils ne bougent jamais) */
static void ligne_lire(const char* nom, uint64_t dec, long long rax) {
    printf("VECTEUR %s dec=%llu rax=%lld rempl=%u vue=%llu curseur=%llu tampon=",
           nom, (unsigned long long)dec, rax, champ_dword(552),
           (unsigned long long)champ_qword(536),
           (unsigned long long)champ_qword(544));
    hex_print((const uint8_t*)cadre + 568, 384);
    printf("\n");
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

/* poser le journal d'édition (le format loupe-16 : u64 décalage · u8 octet
   · 7 réserve ; le nombre u32 à +4096) — le harnais écrit, la pièce lit */
static void poser_journal(const uint64_t* decs, const uint8_t* octets, int n) {
    memset((void*)journal, 0, 4112);
    for (int i = 0; i < n; ++i) {
        uint8_t* e = (uint8_t*)journal + 16 * i;
        for (int k = 0; k < 8; ++k) e[k] = (uint8_t)(decs[i] >> (8 * k));
        e[8] = octets[i];
    }
    *(uint32_t*)((uint8_t*)journal + 4096) = (uint32_t)n;
}

int main(void) {
    setlocale(LC_ALL, "C");

    /* ---- V1 : les témoins — la fenêtre née, puis les frontières --------- */
    const char* temoins[] = {"temoin-1.bin", "temoin-384.bin", "temoin-3f.bin"};
    for (int i = 0; i < 3; ++i) {
        long long r = appeler_ouvrir(temoins[i]);
        printf("OUVRIR %s rax=%lld rempl=%u\n", temoins[i], r, champ_dword(552));
        /* la fenêtre née à l'ouverture : le tampon == la découpe (le
           bloC session du kit 01 lit sa première fenêtre INLINE — l'écart
           nommé du bras C : le loupe-01 du plan appelle loupe-02, la
           pièce C l'incline dans son ouvrir) */
        ligne_lire("nee", 0, 0);
        uint64_t taille = champ_qword(520);
        uint64_t frontieres[8];
        int nf = 0;
        frontieres[nf++] = 0;
        if (taille >= 16) frontieres[nf++] = (taille - 1) / 16 * 16;
        if (taille >= 384 + 16) frontieres[nf++] = (taille - 384) & ~(uint64_t)15;
        if (taille >= 16 && taille % 16 == 0) frontieres[nf++] = taille - 16;
        if (taille >= 65536 + 384) {
            frontieres[nf++] = 65536;
            frontieres[nf++] = 65536 + 368;
        }
        for (int k = 0; k < nf; ++k) {
            ligne_lire("frontiere", frontieres[k], loupe_02_lire(frontieres[k]));
        }
        loupe_03_fermer();
    }
    /* le vide : l'ouverture sans fenêtre, aucun décalage valide */
    {
        long long r = appeler_ouvrir("vide.bin");   /* capté AVANT le dump :
                                                       l'ordre d'évaluation des
                                                       arguments n'est pas C */
        printf("OUVRIR vide.bin rax=%lld rempl=%u\n", r, champ_dword(552));
        ligne_lire("vide", 0, loupe_02_lire(0));
        loupe_03_fermer();
    }

    /* ---- V2 : LE RECOUVREMENT du journal -------------------------------- */
    appeler_ouvrir("temoin-3f.bin");
    {
        const uint64_t decs[] = {65536, 65536 + 383, 65536 + 384, 65536 - 16};
        const uint8_t octets[] = {0xAA, 0xBB, 0xCC, 0xDD};
        poser_journal(decs, octets, 4);
        printf("JOURNAL avant=");
        hex_print((const uint8_t*)journal, 4112);
        printf("\n");
        ligne_lire("bords", 65536, loupe_02_lire(65536));
        printf("JOURNAL apres=");
        hex_print((const uint8_t*)journal, 4112);
        printf("\n");
    }
    {
        const uint64_t decs[] = {65536 + 5, 65536 + 100, 65536 + 200,
                                 65536 + 300, 65536 + 383};
        const uint8_t octets[] = {0x11, 0x22, 0x33, 0x44, 0x55};
        poser_journal(decs, octets, 5);
        ligne_lire("multi", 65536, loupe_02_lire(65536));
    }
    poser_journal(NULL, NULL, 0);
    loupe_03_fermer();

    /* ---- V3 : LES REJETS — le tampon empoisonné INTACT ------------------ */
    ligne_lire("sans-session", 0, loupe_02_lire(0));
    appeler_ouvrir("temoin-384.bin");
    memset((void*)(cadre + 568), 0xCC, 384);          /* le poison */
    *(uint32_t*)(cadre + 552) = 0xBEEF;               /* le remplissage piégé */
    ligne_lire("non-aligne", 40, loupe_02_lire(40));
    ligne_lire("a-la-taille", 384, loupe_02_lire(384));
    ligne_lire("au-dela", 400, loupe_02_lire(400));
    ligne_lire("immense", 1ULL << 40, loupe_02_lire(1ULL << 40));

    /* ---- V4 : L'ÉCHEC SYSTÈME — le tiroir, puis la session SURVIT ------- */
    lire_echec_dans = 0;                              /* le PROCHAIN refuse */
    ligne_lire("echec-read", 0, loupe_02_lire(0));
    ligne_lire("session-survit", 0, loupe_02_lire(0));
    loupe_03_fermer();

    /* ---- V5 : LA FALSIFICATION DEMANDÉE ---------------------------------- */
    appeler_ouvrir("temoin-384.bin");
    ligne_lire("falsif-avant", 0, loupe_02_lire(0));
    cadre[568 + 3] = 0xFF;                            /* l'octet muté */
    printf("ETAT cadre=");
    hex_print((const uint8_t*)cadre, 960);
    printf("\n");
    loupe_03_fermer();

    return 0;
}
