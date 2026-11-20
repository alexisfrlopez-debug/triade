#include <stdio.h>
#include <stdlib.h>

#define INVALIDE 0xFFFFFFFF

long loupe_02_lire(const unsigned char *fichier, long taille, const long *journal_dec, const unsigned char *journal_oct, long journal_n, unsigned char *tampon, long *remplissage, long decalage) {
    if (decalage % 16 != 0) {
        return -5;
    }
    if (decalage >= taille) {
        return -3;
    }

    *remplissage = min(384, taille - decalage);
    for (long i = 0; i < *remplissage; ++i) {
        tampon[i] = fichier[decalage + i];
    }

    for (long j = 0; j < journal_n; ++j) {
        if (journal_dec[j] >= decalage && journal_dec[j] < decalage + *remplissage) {
            tampon[journal_dec[j] - decalage] = journal_oct[j];
        }
    }

    return 0;
}

long min(long a, long b) {
    return (a < b) ? a : b;
}