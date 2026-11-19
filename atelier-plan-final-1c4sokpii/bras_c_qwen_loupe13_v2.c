#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long loupe_13_recherche(const unsigned char *fenetre, long taille,
                          const unsigned char *motif, long taille_motif,
                          long depart) {
    if (taille_motif == 0 || taille_motif > 32 || depart > taille) {
        return -5; // Invalid input
    }

    for (long i = depart; i <= taille - taille_motif; ++i) {
        if (memcmp(fenetre + i, motif, taille_motif) == 0) {
            return i; // Found the first occurrence
        }
    }

    return -1; // Not found
}
