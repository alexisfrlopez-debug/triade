/* loupe-16-saisie · le miroir C du bloc de campagne (l'unité 04 D210, bras C)
 * La saisie : l'octet au journal, la marque sale, la garde ré-armée — le
 * disque demeure intact (I1 : la sauvegarde vit chez loupe-17 seul).
 *
 * Le flux standard : gcc -O2 -std=c11 -Wall -Wextra PROPRE ; la DLL au
 * terrain : x86_64-w64-mingw32-gcc -O2 -shared -o loupe-16-d210-c.dll
 * source-loupe-16-C.c loupe-16-c.def (le .def : EXPORTS loupe_16_saisie).
 *
 * Les zones du MIROIR (les offsets du plan loupe, la source unique — les
 * mêmes que le bras T lit par lea rip) : le cadre, la saisie, le journal ;
 * le disque passe par pointeur : LA RELECTURE au miroir C est memcpy (le
 * tampon re-né de disque[vue..] + le recouvrement du journal) — l'échec
 * de relecture vit au bras T seul (le scellé loupe-02 le rend), nommé.
 */
#include <stdint.h>
#include <string.h>

/* LE CADRE (0xE000 au plan) : les offsets littéraux du plan */
#define CADRE_TAILLE        520u   /* u64 */
#define CADRE_POIGNEE       528u   /* u64 — INVALIDE (~0) hors session */
#define CADRE_VUE           536u   /* u64 */
#define CADRE_CURSEUR       544u   /* u64 */
#define CADRE_REMPLISSAGE   552u   /* u32 — LUI SEUL, jamais le qword */
#define CADRE_SALE          556u   /* u32 */
#define CADRE_REFUS_QUITTER 560u   /* u32 — la garde de loupe-18 */
#define CADRE_TAMPON        568u   /* 384 octets */

/* LA SAISIE (0xE400) : le mode, l'attente, la barre */
#define SAISIE_MODE         0u     /* u32 — 3 = MESSAGE */
#define SAISIE_ACTIF        4u     /* u32 — l'attente du premier chiffre */
#define SAISIE_NIBBLE       8u     /* u32 — sa valeur 0..15 */
#define SAISIE_BARRE        12u    /* 80 octets */

/* LE JOURNAL (0xE4A0) : 256 entrées de 16 o + le nombre */
#define JOURNAL_NOMBRE      4096u  /* u32 */
#define EDITS_MAX           256u
#define TAMPON_SESSION      384u

static uint64_t lire_u64(const unsigned char *zone, uint32_t off) {
    uint64_t v = 0;
    for (unsigned int i = 0; i < 8; ++i) {
        v |= (uint64_t)zone[off + i] << (8u * i);
    }
    return v;
}

static uint32_t lire_u32(const unsigned char *zone, uint32_t off) {
    uint32_t v = 0;
    for (unsigned int i = 0; i < 4; ++i) {
        v |= (uint32_t)zone[off + i] << (8u * i);
    }
    return v;
}

static void ecrire_u64(unsigned char *zone, uint32_t off, uint64_t v) {
    for (unsigned int i = 0; i < 8; ++i) {
        zone[off + i] = (unsigned char)(v >> (8u * i));
    }
}

static void ecrire_u32(unsigned char *zone, uint32_t off, uint32_t v) {
    for (unsigned int i = 0; i < 4; ++i) {
        zone[off + i] = (unsigned char)(v >> (8u * i));
    }
}

/* LE MESSAGE À LA BARRE : la phrase copiée (NUL final), le mode MESSAGE */
static void poser_message(unsigned char *saisie, const char *phrase) {
    size_t n = strlen(phrase);
    if (n > 79) {
        n = 79;
    }
    memcpy(saisie + SAISIE_BARRE, phrase, n);
    saisie[SAISIE_BARRE + n] = '\0';
    ecrire_u32(saisie, SAISIE_MODE, 3u);
}

/* LE RECOUVREMENT : le tampon re-né du disque + les octets du journal */
static void relire_vue(unsigned char *cadre, unsigned char *journal,
                       const unsigned char *disque, uint64_t nv) {
    uint64_t taille = lire_u64(cadre, CADRE_TAILLE);
    uint32_t nombre = lire_u32(journal, JOURNAL_NOMBRE);
    uint32_t rempl = (taille - nv < TAMPON_SESSION)
                     ? (uint32_t)(taille - nv) : TAMPON_SESSION;
    memcpy(cadre + CADRE_TAMPON, disque + nv, rempl);
    for (uint32_t i = 0; i < nombre; ++i) {
        uint64_t dec = lire_u64(journal + 16u * i, 0u);
        if (nv <= dec && dec - nv < (uint64_t)rempl) {
            cadre[CADRE_TAMPON + (uint32_t)(dec - nv)] =
                journal[16u * i + 8u];
        }
    }
    ecrire_u64(cadre, CADRE_VUE, nv);
    ecrire_u32(cadre, CADRE_REMPLISSAGE, rempl);
}

long long loupe_16_saisie(
    unsigned char *cadre,
    unsigned char *saisie,
    unsigned char *journal,
    const unsigned char *disque,
    unsigned int lignes,
    unsigned int caractere
) {
    /* E1 : sans session ouverte → -4, la phrase nommée à la barre */
    if (lire_u64(cadre, CADRE_POIGNEE) == ~(uint64_t)0) {
        poser_message(saisie, "aucun fichier ouvert");
        return -4;
    }

    /* Q5 : VK_SUPPR pendant l'attente → le nibble effacé */
    if (caractere == 0x08u) {
        if (lire_u32(saisie, SAISIE_ACTIF) != 0u) {
            ecrire_u32(saisie, SAISIE_ACTIF, 0u);
            ecrire_u32(saisie, SAISIE_NIBBLE, 0u);
        }
        return 0;
    }

    /* E4 : la classe — les SEIZE chiffres hexa écoutent, le reste ignoré */
    unsigned int c = caractere;
    if (c >= 0x61u && c <= 0x66u) {
        c -= 0x20u;                       /* les minuscules portées aux MAJUSCULES */
    }
    unsigned int valeur;
    if (c >= 0x30u && c <= 0x39u) {
        valeur = c - 0x30u;
    } else if (c >= 0x41u && c <= 0x46u) {
        valeur = c - 0x37u;
    } else {
        return 0;                          /* ignoré proprement (E4) */
    }

    /* Q1 : le premier chiffre → l'attente posée (rien n'est écrit) */
    if (lire_u32(saisie, SAISIE_ACTIF) == 0u) {
        ecrire_u32(saisie, SAISIE_ACTIF, 1u);
        ecrire_u32(saisie, SAISIE_NIBBLE, valeur);
        return 0;
    }

    /* Q2 : le second chiffre — l'attente CONSOMMÉE avant tout contrôle */
    unsigned int premier = lire_u32(saisie, SAISIE_NIBBLE);
    ecrire_u32(saisie, SAISIE_ACTIF, 0u);
    ecrire_u32(saisie, SAISIE_NIBBLE, 0u);
    unsigned int octet = (premier << 4) | valeur;

    /* E2 : la cellule fantôme (le refus PRÉCÈDE le journal) */
    uint64_t curseur = lire_u64(cadre, CADRE_CURSEUR);
    uint64_t vue = lire_u64(cadre, CADRE_VUE);
    uint32_t remplissage = lire_u32(cadre, CADRE_REMPLISSAGE);
    if (curseur >= vue + (uint64_t)remplissage) {
        poser_message(saisie, "hors bornes");
        return -3;
    }

    /* Q2 : le journal PAR DÉCALAGE — présent REMPLACÉ, absent AJOUTÉ */
    uint32_t nombre = lire_u32(journal, JOURNAL_NOMBRE);
    uint32_t i = 0;
    while (i < nombre) {
        if (lire_u64(journal + 16u * i, 0u) == curseur) {
            break;
        }
        ++i;
    }
    if (i < nombre) {
        journal[16u * i + 8u] = (unsigned char)octet;   /* REMPLACÉ */
    } else if (nombre < EDITS_MAX) {
        ecrire_u64(journal + 16u * nombre, 0u, curseur);
        journal[16u * nombre + 8u] = (unsigned char)octet;
        ecrire_u32(journal, JOURNAL_NOMBRE, nombre + 1u);
    } else {
        poser_message(saisie, "journal plein - Ctrl+S");  /* E3, rien perdu */
        return -3;
    }

    /* Q3 : l'octet visible immédiatement au tampon de vue */
    cadre[CADRE_TAMPON + (uint32_t)(curseur - vue)] = (unsigned char)octet;

    /* Q4 : la marque, LA GARDE RÉ-ARMÉE, le pas clampé */
    uint64_t taille = lire_u64(cadre, CADRE_TAILLE);
    ecrire_u32(cadre, CADRE_SALE, 1u);
    ecrire_u32(cadre, CADRE_REFUS_QUITTER, 0u);
    curseur = curseur + 1u;
    if (curseur >= taille) {              /* clampé à taille − 1 ; le vide : 0 */
        curseur = (taille > 0u) ? taille - 1u : 0u;
    }
    ecrire_u64(cadre, CADRE_CURSEUR, curseur);

    /* LA VUE SUIT (le renvoi de loupe-15 Q3) : la vitrine [vue, vue+16·V) */
    uint32_t v = (lignes > 3u) ? lignes - 3u : 0u;
    if (v > 24u) {
        v = 24u;
    }
    if (curseur < vue || curseur >= vue + (uint64_t)(16u * v)) {
        uint64_t nv = (curseur > 176u) ? curseur - 176u : 0u;
        nv &= ~(uint64_t)15u;                    /* aligne16_inf */
        uint64_t vmax = 0u;
        if (taille > TAMPON_SESSION) {
            vmax = (taille - TAMPON_SESSION + 15u) & ~(uint64_t)15u;
        }
        if (nv > vmax) {
            nv = vmax;
        }
        if (nv != vue) {
            relire_vue(cadre, journal, disque, nv);  /* la relecture au miroir */
        }
    }
    return 0;
}
