/*
 * loupe-08-c.c — LA PIÈCE DU BRAS C, l'unité 4 (loupe-08 ligne, la campagne
 * de comparaison des workflows D204). Le MÊME contrat loupe-08:R1 que le
 * bras T, lu comme cahier des charges : composer UNE ligne hexadécimale de
 * 77 o au tampon fixe — les 8 chiffres MAJUSCULES du décalage (grand-
 * boutiste), 2 espaces, les seize groupes « HH » séparés d'un espace (le
 * médian DOUBLÉ après le huitième), 2 espaces, le miroir ASCII de 16 (le
 * point hors 0x20..0x7E), le NUL — EXACTEMENT 77 o écrits, jamais un de
 * plus ; la ligne incomplète garde ses colonnes (les groupes absents deux
 * espaces, le miroir absent un espace).
 *
 * LES CHOIX DU FLUX STANDARD (le C tel qu'il se pratique) :
 *   - la table « 0123456789ABCDEF » au fichier, MAJUSCULES (I4) ;
 *   - les bornes d'abord : la longueur hors 1..16, un pointeur nul → -5
 *     AVANT toute écriture (I2 / E1-E3) ;
 *   - le squelette d'espaces posé d'une boucle, puis les groupes et le
 *     miroir par-dessus : la ligne incomplète née du remplissage même
 *     (Q3) ;
 *   - le miroir : la double comparaison 0x20..0x7E, lisible ;
 *   - long long en retour : le verdict -5 ou 0 (Q4).
 *
 * La compilation (consignée, la règle du bras C) :
 *   x86_64-w64-mingw32-gcc-posix -O2 -shared -o loupe-08-c.dll \
 *       loupe-08-c.c loupe-08-c.def
 */

#include <stdint.h>

/* la table du plan (I4 — la convention MAJUSCULES du journal des builds) */
static const char HEX[] = "0123456789ABCDEF";

long long loupe_08_ligne(const unsigned char *source,
                         unsigned long long longueur,
                         char *sortie,
                         unsigned long long decalage)
{
    int i, k;

    /* les bornes d'abord (I2) : jamais un octet écrit au refus */
    if (source == 0 || sortie == 0) {
        return -5;
    }
    if (longueur < 1 || longueur > 16) {
        return -5;
    }

    /* les huit chiffres du décalage, grand-boutistes (Q1) */
    for (k = 0; k < 8; k++) {
        sortie[k] = HEX[(decalage >> (28 - 4 * k)) & 0xFULL];
    }

    /* le squelette [8..75] : séparateurs, groupes absents, miroir absent
       (Q3 — la colonne ASCII ne bouge jamais) */
    for (i = 8; i < 76; i++) {
        sortie[i] = ' ';
    }

    /* les seize groupes « HH » (l'espace médian DOUBLÉ : pos 33-34) */
    for (i = 0; i < 16; i++) {
        int pos = 10 + 3 * i + (i >= 8 ? 1 : 0);
        if (i < (int)longueur) {
            sortie[pos] = HEX[source[i] >> 4];
            sortie[pos + 1] = HEX[source[i] & 0xF];
        }
    }

    /* le miroir ASCII (Q2 : 0x20..0x7E le caractère, sinon le point) */
    for (i = 0; i < 16; i++) {
        if (i < (int)longueur) {
            unsigned char c = source[i];
            sortie[60 + i] = (c >= 0x20 && c <= 0x7E) ? (char)c : '.';
        }
    }

    sortie[76] = '\0';
    return 0;
}
