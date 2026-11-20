#include <string.h>
long l13_o3(const unsigned char *fenetre, long taille,
        const unsigned char *motif, long taille_motif, long depart) {
    if (taille_motif > 32 || taille < 0 || depart > taille) return -5;
    for (long i = depart; i <= taille - taille_motif; ++i)
        if (memcmp(fenetre + i, motif, taille_motif) == 0) return i;
    return -1;
}
