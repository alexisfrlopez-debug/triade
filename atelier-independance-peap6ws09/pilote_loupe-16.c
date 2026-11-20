
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
long loupe_16_saisie(long, unsigned char, long *, unsigned char *,
                     long *, unsigned char *, long, long, long *);
static int verts = 0, total = 0;
static void cas(long curseur, unsigned char octet, long jn_avant,
                long deja_au_journal, long attendu, long jn_attendu,
                long sale_attendu, const char *nom) {
    long jd[300]; unsigned char jo[300]; long jn = jn_avant;
    for (long i = 0; i < 300; i++) { jd[i] = -1; jo[i] = 0; }
    if (deja_au_journal >= 0) { jd[deja_au_journal] = curseur; jo[deja_au_journal] = 'x'; }

    for (long i = 0; i < 384; i++) tampon[i] = 'A';
    long sale = 0;
    long r = loupe_16_saisie(curseur, octet, jd, jo, &jn, tampon, 384, 0, &sale);
    total++;
    if (r != attendu || jn != jn_attendu || sale != sale_attendu) {
        printf("ROUGE %s : rendu %ld jn %ld sale %ld attendus %ld %ld %ld\n",
               nom, r, jn, sale, attendu, jn_attendu, sale_attendu);
    } else verts++;
}
int main(void) {
    cas(16, 'Z', 0, -1, 0, 1, 1, "ecole-premier-ajout");
    cas(32, 'Y', 1, -1, 0, 2, 1, "ecole-deuxieme-ajout");
    cas(16, 'W', 1, 0, 0, 1, 1, "ecole-remplacement");
    /* le journal plein : 256 distincts, le 257e refuse */
    long jd[300]; unsigned char jo[300]; long jn = 256;
    for (long i = 0; i < 256; i++) { jd[i] = i * 4; jo[i] = 'q'; }
    unsigned char tampon[384]; for (long i = 0; i < 384; i++) tampon[i] = 'A';
    long sale = 0;
    long r = loupe_16_saisie(5000, 'K', jd, jo, &jn, tampon, 384, 0, &sale);
    total++;
    if (r == -3 && jn == 256) verts++;
    else printf("ROUGE journal-plein : rendu %ld jn %ld\n", r, jn);
    printf("EPREUVE %d/%d VERT\n", verts, total);
    return verts == total ? 0 : 1;
}
