/* piece-labo-loupe08-v2.c - LA PIECE DU LABO de l'epreuve v2 (gcc -O2
   -shared, le contrat des rejets : -5, RIEN d'ecrit) - l'epreuve
   epreuve_kits08_v2_20261115.py la porte aussi DANS son texte. */
#include <stdint.h>
int64_t loupe_08_ligne(const void *src, uint64_t len, void *dst,
                      uint64_t off)
{
    (void)off;
    if (len == 0 || len > 16 || src == 0 || dst == 0)
        return -5;              /* le refus : RIEN d'ecrit, jamais */
    return 0;
}
