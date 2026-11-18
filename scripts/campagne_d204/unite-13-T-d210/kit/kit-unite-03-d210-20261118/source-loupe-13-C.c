#include <stdint.h>
#include <string.h>

#define MOTIF_MAX 32

long long loupe_13_recherche(
    const unsigned char *fenetre,
    unsigned long long taille_fenetre,
    const unsigned char *motif,
    unsigned long long taille_motif,
    unsigned long long depart
) {
    if (taille_motif == 0 || taille_motif > MOTIF_MAX || depart > taille_fenetre) {
        return -5;
    }

    unsigned long long longueur_restante = taille_fenetre - depart;
    if (taille_motif > longueur_restante) {
        return -1;
    }

    for (unsigned long long i = depart; i <= taille_fenetre - taille_motif; ++i) {
        if (memcmp(fenetre + i, motif, taille_motif) == 0) {
            return i;
        }
    }

    return -1;
}
