```c
#include <stdint.h>
#include <string.h>
#include <stddef.h>

#define JOURNAL_ENTRIES 256
#define TAILLE_TAMPON 384
#define TAILLE_BARRE 80

/* Offsets littéraux du plan mémoire */
#define CADRE_TAILLE_OFFSET 520ULL
#define CADRE_POIGNEE_OFFSET 528ULL
#define CADRE_VUE_OFFSET 536ULL
#define CADRE_CURSEUR_OFFSET 544ULL
#define CADRE_REMPLISSAGE_OFFSET 552ULL
#define CADRE_SALE_OFFSET 556ULL
#define CADRE_REFUS_QUITTER_OFFSET 560ULL
#define CADRE_TAMPON_OFFSET 568ULL

#define SAISIE_ACTIF_OFFSET 4ULL
#define SAISIE_NIBBLE_OFFSET 8ULL
#define SAISIE_BARRE_OFFSET 12ULL
#define SAISIE_MODE_OFFSET 0ULL

#define JOURNAL_ENTREE_DECALAGE_OFFSET 0ULL
#define JOURNAL_ENTREE_OCTET_OFFSET 8ULL
#define JOURNAL_NOMBRE_OFFSET 4096ULL

static inline uint64_t lu_u64(const unsigned char *zone, uint64_t offset) {
    return *(const uint64_t *)(zone + offset);
}

static inline void ecrit_u64(unsigned char *zone, uint64_t offset, uint64_t valeur) {
    *(uint64_t *)(zone + offset) = valeur;
}

static inline uint32_t lu_u32(const unsigned char *zone, uint64_t offset) {
    return *(const uint32_t *)(zone + offset);
}

static inline void ecrit_u32(unsigned char *zone, uint64_t offset, uint32_t valeur) {
    *(uint32_t *)(zone + offset) = valeur;
}

static inline uint8_t lu_u8(const unsigned char *zone, uint64_t offset) {
    return *(const uint8_t *)(zone + offset);
}

static inline void ecrit_u8(unsigned char *zone, uint64_t offset, uint8_t valeur) {
    *(uint8_t *)(zone + offset) = valeur;
}

long long loupe_16_saisie(unsigned char *cadre, unsigned char *saisie, unsigned char *journal,
                          const unsigned char *disque, unsigned int lignes, unsigned int caractere) {
    uint64_t poignee = lu_u64(cadre, CADRE_POIGNEE_OFFSET);
    uint64_t curseur = lu_u64(cadre, CADRE_CURSEUR_OFFSET);
    uint64_t vue = lu_u64(cadre, CADRE_VUE_OFFSET);
    uint32_t remplissage = lu_u32(cadre, CADRE_REMPLISSAGE_OFFSET);
    uint32_t sale = lu_u32(cadre, CADRE_SALE_OFFSET);
    uint32_t refus_quitter = lu_u32(cadre, CADRE_REFUS_QUITTER_OFFSET);
    uint32_t taille = lu_u32(cadre, CADRE_TAILLE_OFFSET);

    // E1: Poignée invalide
    if (poignee == ~0ULL) {
        memset(saisie + SAISIE_BARRE_OFFSET, 0, TAILLE_BARRE);
        strcpy((char *)saisie + SAISIE_BARRE_OFFSET, "aucun fichier ouvert");
        ecrit_u32(saisie, SAISIE_MODE_OFFSET, 3);
        return -4;
    }

    // Q5: VK_SUPPR (caractère 0x08)
    if (caractere == 0x08) {
        ecrit_u32(saisie, SAISIE_NIBBLE_OFFSET, 0);
        return 0;
    }

    uint32_t actif = lu_u32(saisie, SAISIE_ACTIF_OFFSET);
    uint32_t nibble = lu_u32(saisie, SAISIE_NIBBLE_OFFSET);
    uint32_t mode = lu_u32(saisie, SAISIE_MODE_OFFSET);

    // E4: Traitement de la saisie d'un caractère hexadécimal
    if ((caractere >= '0' && caractere <= '9') ||
        (caractere >= 'a' && caractere <= 'f') ||
        (caractere >= 'A' && caractere <= 'F')) {

        uint8_t valeur;
        if (caractere >= '0' && caractere <= '9') {
            valeur = caractere - '0';
        } else if (caractere >= 'a' && caractere <= 'f') {
            valeur = caractere - 'a' + 10;
        } else { // 'A'-'F'
            valeur = caractere - 'A' + 10;
        }

        // Q1: Premier chiffre de la paire
        if (!actif) {
            ecrit_u32(saisie, SAISIE_ACTIF_OFFSET, 1);
            ecrit_u32(saisie, SAISIE_NIBBLE_OFFSET, valeur);
            return 0;
        }
        // Q2: Deuxième chiffre de la paire
        else {
            uint8_t octet = (nibble << 4) | valeur;
            ecrit_u32(saisie, SAISIE_ACTIF_OFFSET, 0);
            ecrit_u32(saisie, SAISIE_NIBBLE_OFFSET, 0);

            // E2: Curseur hors des bornes modifiables
            if (curseur >= vue + remplissage) {
                memset(saisie + SAISIE_BARRE_OFFSET, 0, TAILLE_BARRE);
                strcpy((char *)saisie + SAISIE_BARRE_OFFSET, "hors bornes");
                return -3;
            }

            // Journalisation
            uint32_t nombre_journal = lu_u32(journal, JOURNAL_NOMBRE_OFFSET);
            uint64_t decalage_log = curseur - vue;

            // Recherche de l'entrée existante dans le journal
            int trouvee = 0;
            for (uint32_t i = 0; i < nombre_journal; ++i) {
                uint64_t decalage_actuel = lu_u64(journal, i * 16ULL + JOURNAL_ENTREE_DECALAGE_OFFSET);
                if (decalage_actuel == decalage_log) {
                    ecrit_u64(journal, i * 16ULL + JOURNAL_ENTREE_DECALAGE_OFFSET, decalage_log);
                    ecrit_u8(journal, i * 16ULL + JOURNAL_ENTREE_OCTET_OFFSET, octet);
                    trouvee = 1;
                    break;
                }
            }

            // Ajout au journal si non trouvée et si possible
            if (!trouvee) {
                if (nombre_journal < JOURNAL_ENTRIES) {
                    ecrit_u64(journal, nombre_journal * 16ULL + JOURNAL_ENTREE_DECALAGE_OFFSET, decalage_log);
                    ecrit_u8(journal, nombre_journal * 16ULL + JOURNAL_ENTREE_OCTET_OFFSET, octet);
                    ecrit_u32(journal, JOURNAL_NOMBRE_OFFSET, nombre_journal + 1);
                } else {
                    memset(saisie + SAISIE_BARRE_OFFSET, 0, TAILLE_BARRE);
                    strcpy((char *)saisie + SAISIE_BARRE_OFFSET, "journal plein - Ctrl+S");
                    return -3;
                }
            }

            // Q3: Écriture dans le tampon
            ecrit_u8(cadre, CADRE_TAMPON_OFFSET + decalage_log, octet);

            // Q4: Mise à jour des indicateurs et curseur
            ecrit_u32(cadre, CADRE_SALE_OFFSET, 1);
            ecrit_u32(cadre, CADRE_REFUS_QUITTER_OFFSET, 0);
            curseur++;
            if (curseur >= taille) curseur = taille - 1;
            ecrit_u64(cadre, CADRE_CURSEUR_OFFSET, curseur);

            // LA VUE SUIT
            uint32_t v = (lignes >= 3) ? (lignes - 3) : 0;
            if (v > 24) v = 24;

            // Calcul de la nouvelle vue
            uint64_t nv;
            if (taille <= TAILLE_TAMPON) {
                nv = 0;
            } else {
                nv = (curseur - 176) & ~15ULL;
                if (nv > (taille - TAILLE_TAMPON + 15) & ~15ULL) {
                    nv = (taille - TAILLE_TAMPON + 15) & ~15ULL;
                }
                if (nv < 0) nv = 0;
            }

            // Mise à jour de la vue si nécessaire
            if (nv != vue) {
                // Relecture du disque
                memcpy(cadre + CADRE_TAMPON_OFFSET, disque + nv, TAILLE_TAMPON);
                // Recouvrement du journal
                uint32_t nombre_actuel = lu_u32(journal, JOURNAL_NOMBRE_OFFSET);
                for (uint32_t i = 0; i < nombre_actuel; ++i) {
                    uint64_t dec_j = lu_u64(journal, i * 16ULL + JOURNAL_ENTREE_DECALAGE_OFFSET);
                    uint8_t oct_j = lu_u8(journal, i * 16ULL + JOURNAL_ENTREE_OCTET_OFFSET);
                    if (nv + dec_j < taille) {
                         ecrit_u8(cadre, CADRE_TAMPON_OFFSET + dec_j, oct_j);
                    }
                }
                ecrit_u64(cadre, CADRE_VUE_OFFSET, nv);
                ecrit_u32(cadre, CADRE_REMPLISSAGE_OFFSET, (taille < TAILLE_TAMPON) ? taille : TAILLE_TAMPON);
            }
            return 0;
        }
    }
    // Caractère ignoré
    return 0;
}
```