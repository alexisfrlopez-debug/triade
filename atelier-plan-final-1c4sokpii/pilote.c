
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
long loupe_13_recherche(const unsigned char *, long, const unsigned char *,
                        long, long);
static int verts = 0, total = 0;
static void cas(const unsigned char *f, long tf, const unsigned char *m,
                long tm, long d, long attendu, const char *nom) {
    long r = loupe_13_recherche(f, tf, m, tm, d);
    total++;
    if (r == attendu) { verts++; }
    else printf("ROUGE %s : rendu %ld attendu %ld\n", nom, r, attendu);
}
/* la différentielle : 2000 cas recalculés côté Python (le juge
   bytes.find) — les cas passent par un fichier de vecteurs */
int main(int argc, char **argv) {
    /* V2 l'école : les 10 cas tenus pour toujours */
    unsigned char ecole[] = "AAAAAB";
    unsigned char m1[] = "A", m2[] = "AAAA", m3[] = "AB", m4[] = "Z";
    cas(ecole, 6, m1, 1, 0, 0, "ecole-premier-octet");
    cas(ecole, 6, m2, 4, 0, 0, "ecole-motif-repetitif");
    cas(ecole, 6, m3, 2, 5, -1, "ecole-depart-apres-occurrence");
    cas(ecole, 6, m4, 1, 0, -1, "ecole-absent");
    cas(ecole, 6, m1, 1, 3, 3, "ecole-depart-au-milieu");
    cas(ecole, 6, m2, 4, 2, -1, "ecole-plage-trop-courte");
    cas(ecole, 0, m1, 1, 0, -1, "ecole-fenetre-vide");
    cas(ecole, 6, m1, 1, 6, -1, "ecole-plage-vide");
    /* V3 les TROIS rejets -5 */
    cas(ecole, 6, m1, 0, 0, -5, "rejet-motif-vide");
    unsigned char m33[33]; memset(m33, 'A', 33);
    cas(ecole, 6, m33, 33, 0, -5, "rejet-motif-33");
    cas(ecole, 6, m1, 1, 7, -5, "rejet-depart-au-dela");
    /* V1 la différentielle : les vecteurs au fichier (2000 cas) */
    FILE *fv = fopen(argv[1], "rb");
    if (!fv) { printf("ROUGE vecteurs introuvables\n"); return 1; }
    long n; fread(&n, 8, 1, fv);
    for (long k = 0; k < n; k++) {
        long tf, tm, d, attendu;
        fread(&tf, 8, 1, fv); fread(&tm, 8, 1, fv);
        fread(&d, 8, 1, fv); fread(&attendu, 8, 1, fv);
        unsigned char *f = malloc(tf ? tf : 1), *m = malloc(tm ? tm : 1);
        if (tf) fread(f, 1, tf, fv); if (tm) fread(m, 1, tm, fv);
        cas(f, tf, m, tm, d, attendu, "differentiel");
        free(f); free(m);
    }
    fclose(fv);
    printf("EPREUVE %d/%d VERT\n", verts, total);
    return verts == total ? 0 : 1;
}
