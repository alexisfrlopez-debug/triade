
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
long loupe_02_lire(const unsigned char *, long, const long *,
                   const unsigned char *, long, unsigned char *,
                   long *, long);
static int verts = 0, total = 0;
static void cas(const unsigned char *f, long tf, const long *jd,
                const unsigned char *jo, long jn, long dec, long attendu,
                long att_rempl, const char *nom) {
    unsigned char tampon[384]; long rempl = -1;
    for (long i = 0; i < 384; i++) tampon[i] = 0xEE;
    long r = loupe_02_lire(f, tf, jd, jo, jn, tampon, &rempl, dec);
    total++;
    if (r != attendu || (attendu == 0 && rempl != att_rempl)) {
        printf("ROUGE %s : rendu %ld rempl %ld attendus %ld %ld\n",
               nom, r, rempl, attendu, att_rempl);
    } else verts++;
}
int main(int argc, char **argv) {
    unsigned char fichier[800]; memset(fichier, 'A', 800);
    const long jd1[] = {16}; const unsigned char jo1[] = {'Z'};
    cas(fichier, 800, jd1, jo1, 1, 0, 0, 384, "ecole-premiere-fenetre");
    cas(fichier, 800, jd1, jo1, 1, 384, 0, 384, "ecole-deuxieme-fenetre");
    cas(fichier, 800, jd1, jo1, 1, 768, 0, 32, "ecole-derniere-fenetre");
    cas(fichier, 100, jd1, jo1, 0, 96, 0, 4, "ecole-queue-4");
    cas(fichier, 800, NULL, NULL, 0, 0, -5, -1, "rejet-decalage-non-16");
    cas(fichier, 800, NULL, NULL, 0, 800, -3, -1, "rejet-hors-bornes");
    cas(fichier, 800, NULL, NULL, 0, 801, -3, -1, "rejet-au-dela");
    cas(fichier, 0, NULL, NULL, 0, 0, -3, -1, "rejet-fichier-vide");
    FILE *fv = fopen(argv[1], "rb");
    long n; fread(&n, 8, 1, fv);
    for (long k = 0; k < n; k++) {
        long tf, jn, dec, attendu, att_rempl, verif_tampon;
        fread(&tf, 8, 1, fv); fread(&jn, 8, 1, fv);
        fread(&dec, 8, 1, fv); fread(&attendu, 8, 1, fv);
        fread(&att_rempl, 8, 1, fv); fread(&verif_tampon, 8, 1, fv);
        unsigned char *f = malloc(tf ? tf : 1);
        if (tf) fread(f, 1, tf, fv);
        long *jd = malloc(jn ? jn * 8 : 8);
        unsigned char *jo = malloc(jn ? jn : 1);
        for (long j = 0; j < jn; j++) { fread(&jd[j], 8, 1, fv); fread(&jo[j], 1, 1, fv); }
        unsigned char tampon[384]; long rempl = -1;
        for (long i = 0; i < 384; i++) tampon[i] = 0xEE;
        long r = loupe_02_lire(f, tf, jd, jo, jn, tampon, &rempl, dec);
        total++;
        /* LE JUGE DU RECOUVREMENT : l'octet du journal à sa place (la
           cellule pointée par verif_tampon, -1 = la borne remplissage) */
        int ok = (r == attendu) && (rempl == att_rempl);
        if (ok && verif_tampon >= 0) {
            long dec_j = -1; unsigned char oct_j = 0;
            for (long j = 0; j < jn; j++)
                if (jd[j] >= dec && jd[j] < dec + att_rempl
                    && jd[j] - dec == verif_tampon) { dec_j = jd[j]; oct_j = jo[j]; }
            if (dec_j >= 0 && tampon[verif_tampon] != oct_j) ok = 0;
        }
        if (!ok) printf("ROUGE differentiel : rendu %ld rempl %ld attendus %ld %ld\n",
                        r, rempl, attendu, att_rempl);
        else verts++;
        free(f); free(jd); free(jo);
    }
    fclose(fv);
    printf("EPREUVE %d/%d VERT\n", verts, total);
    return verts == total ? 0 : 1;
}
