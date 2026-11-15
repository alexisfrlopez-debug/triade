/*
 * loupe-13-c.c — LA PIÈCE DU BRAS C, l'unité 5 (loupe-13 recherche, la
 * campagne de comparaison des workflows D204). Le MÊME contrat
 * loupe-13:R1 que le bras T, lu comme cahier des charges : la première
 * occurrence d'un motif (1 à 32 o) dans une fenêtre, à partir d'un
 * départ donné — la position ABSOLUE (départ compté) de la PREMIÈRE,
 * jamais la seconde ; l'absence → -1 (LA FIN NOMMÉE de la table) ; le
 * motif plus long que la plage restante → -1 IMMÉDIAT (le constat
 * trivial, jamais une boucle) ; le départ = la taille (la plage vide)
 * → -1.
 *
 * LES CHOIX DU FLUX STANDARD (le C tel qu'il se pratique) :
 *   - les bornes d'abord : le motif vide, le motif > 32 (MOTIF_MAX), le
 *     départ au-delà de la fenêtre → -5 AVANT toute lecture (E1/E2/E3) ;
 *   - la recherche directe honnête (I3 : O(n·m), m ≤ 32) — chaque
 *     candidat testé par memcmp (I2 : la comparaison par la bibliothèque,
 *     jamais une boucle de comparaison réécrite — la liste d'appels est
 *     FERMÉE) ;
 *   - la dernière candidate posée une fois (taille − motif) : la boucle
 *     ne re-dérive jamais l'arithmétique ;
 *   - la fenêtre et le motif LUS SEULS (I3 — la pureté) ;
 *   - long long en retour : la position ou les verdicts -1/-5 (Q1-Q4).
 *
 * La compilation (consignée, la règle du bras C) :
 *   x86_64-w64-mingw32-gcc-posix -O2 -shared -o loupe-13-c.dll \
 *       loupe-13-c.c loupe-13-c.def
 */

#include <stdint.h>
#include <string.h>

#define MOTIF_MAX 32                   /* la borne du quotidien (P4) */

long long loupe_13_recherche(const unsigned char *fenetre,
                             unsigned long long taille,
                             const unsigned char *motif,
                             unsigned long long taille_motif,
                             unsigned long long depart)
{
    unsigned long long derniere, i;

    /* les bornes d'abord (E1/E2/E3) : jamais un octet lu au refus */
    if (taille_motif < 1 || taille_motif > MOTIF_MAX) {
        return -5;                     /* chercher rien n'est pas chercher ;
                                          la borne du quotidien */
    }
    if (depart > taille) {
        return -5;                     /* le départ est une position, pas un
                                          vœu */
    }

    /* le constat trivial (Q2) : le motif ne tient pas dans la plage
       restante — la FIN NOMMÉE sans une itération, jamais une boucle */
    if (taille_motif > taille - depart) {
        return -1;
    }

    /* la recherche directe (I2/I3) : chaque candidat au memcmp de la
       bibliothèque, le premier match gagne (Q4 — la boucle monte du
       départ, jamais un saut) */
    derniere = taille - taille_motif;  /* posée une fois, la borne */
    for (i = depart; i <= derniere; i++) {
        if (memcmp(&fenetre[i], motif, (size_t)taille_motif) == 0) {
            return (long long)i;       /* Q1 : la position ABSOLUE */
        }
    }
    return -1;                         /* Q2/Q3 : LA FIN NOMMÉE */
}
