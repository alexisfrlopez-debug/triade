#include <string.h>
long l13v_o2(const unsigned char *fenetre, long taille,
        const unsigned char *motif, long taille_motif, long depart) {
    if (taille_motif > 32 || taille < 0 || depart > taille) return -5;
    if (taille_motif == 0) return depart;
    long fin = taille - taille_motif;
    long i = depart;
    while (i <= fin) {
        const unsigned char *hit = memchr(fenetre + i, motif[0],
                                          (size_t)(fin - i + 1));
        if (!hit) return -1;
        if (memcmp(hit, motif, (size_t)taille_motif) == 0)
            return (long)(hit - fenetre);
        i = (long)(hit - fenetre) + 1;
    }
    return -1;
}
