#include <windows.h>

#define INVALIDE_HANDLE ((HANDLE)-1)
#define TAILLE_FENETRE 384
#define OFFSET_TAMPON 568
#define OFFSET_REMPLISSAGE 552

extern HANDLE poignee_cadre;
extern DWORD taille_fichier;
extern uint8_t* tampon_cadre;
extern struct {
    DWORD decalage;
    uint8_t octet;
} journal_edition[];
extern int taille_journal;

int loupe_02(DWORD decalage) {
    // P1: Vérifier si la session est ouverte (poignee_cadre != INVALIDE_HANDLE)
    if (poignee_cadre == INVALIDE_HANDLE) {
        return -4; // SESSION
    }

    // P2: Vérifier si le décalage est un multiple de 16
    if (decalage & 0xF) {
        return -5; // ENTRÉE
    }

    // P3: Vérifier si decalage < taille_fichier
    if (decalage >= taille_fichier) {
        return -3; // HORS-BORNES
    }

    // Calculer remplissage = min(TAILLE_FENETRE, taille_fichier - decalage)
    DWORD* p_remplissage = (DWORD*)(tampon_cadre + OFFSET_REMPLISSAGE);
    DWORD remplissage = taille_fichier - decalage;
    if (remplissage > TAILLE_FENETRE) {
        remplissage = TAILLE_FENETRE;
    }

    // SetFilePointerEx: repositionner au début de la fenêtre
    LARGE_INTEGER liDebut;
    liDebut.QuadPart = decalage;
    LARGE_INTEGER liFin;
    if (!SetFilePointerEx(poignee_cadre, liDebut, &liFin, FILE_BEGIN)) {
        goto echec_systeme;
    }

    // ReadFile: lire la fenêtre
    DWORD lus = 0;
    if (!ReadFile(poignee_cadre, tampon_cadre + OFFSET_TAMPON, remplissage, &lus, NULL)) {
        goto echec_systeme;
    }

    // Q2: Recouvrir les octets du journal d'édition
    for (int i = 0; i < taille_journal; ++i) {
        DWORD offset_journal = journal_edition[i].decalage;
        if (offset_journal >= decalage && offset_journal < decalage + remplissage) {
            uint8_t* p_octet = tampon_cadre + OFFSET_TAMPON + (offset_journal - decalage);
            *p_octet = journal_edition[i].octet;
        }
    }

    // Q1: Stocker le remplissage au cadre
    *p_remplissage = remplissage;

    // Succès
    return 0;

echec_systeme:
    DWORD erreur = GetLastError();
    *p_remplissage = 0;
    (void)erreur;
    return -6; // SYSTÈME
}
