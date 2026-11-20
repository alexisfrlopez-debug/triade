#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long decalage;
    unsigned char octet;
    long n;
} JournalEntry;

#define MAX_JOURNAL_SIZE 256

JournalEntry journal[MAX_JOURNAL_SIZE];
long journal_index = 0;

void loupe_16_saisie(long curseur, unsigned char octet, long *journal_dec, unsigned char *journal_oct, long *journal_n, unsigned char *tampon, long remplissage, long vue, long *sale) {
    if (!*sale) {
        fprintf(stderr, "Session non ouverte\n");
        return -4;
    }

    if (curseur - vue >= remplissage) {
        fprintf(stderr, "Cellule hors bornes\n");
        return -3;
    }

    if (journal_index == MAX_JOURNAL_SIZE) {
        fprintf(stderr, "Journal plein\n");
        return -3;
    }

    if (journal_index > 0 && journal[journal_index - 1].decalage == curseur) {
        journal[journal_index - 1].octet = octet;
    } else {
        journal[journal_index].decalage = curseur;
        journal[journal_index].octet = octet;
        journal[journal_index].n = journal_index;
        journal_index++;
    }

    tampon[curseur - vue] = octet;
    *sale = 1;

    if (curseur < remplissage) {
        *sale = 0;
    }
}