/* bras_c_v140/bras_c.c — LA RÉFÉRENCE COMPILÉE du bras de comparateur
 * v0.14.0 (le plan pré-enregistré : scripts/preuves_v140/PLAN_PREENREGISTRE_
 * v140.md, D193). SIX blocs de Loupe réimplémentés EN C DEPUIS LES MÊMES
 * CONTRATS de couche I (loupe/I/*.md relus avant chaque fonction) :
 *   loupe-01 ouvrir, loupe-02 lire, loupe-05 sha256,
 *   loupe-08 ligne, loupe-13 recherche, loupe-16 saisie.
 *
 * Les conventions : les points d'entrée sont ms_abi (le harnais appelle au
 * msx64 des DEUX camps — la même porte) ; les primitives OS (CreateFileW,
 * GetFileSizeEx, SetFilePointerEx, ReadFile, CloseHandle) sont prises dans
 * LA TABLE pointée par `os` — le harnais y pose les MÊMES shims du mini-OS
 * que consomme le camp notation (CA2 du plan). Le sha-256 du camp C est
 * l'implémentation FIPS 180-4 du banc v0.11.0 (bench.c, la référence
 * AUTO-VÉRIFIÉE contre hashlib — la fonction sha256_bloc), REPRISE TELLE
 * QUELLE : le bras ne réécrit pas un algorithme prouvé.
 * Adaptations NOMMÉES (CA4) : la comparaison de loupe-13 par memcmp du C
 * (l'équivalent compilé de libc-02 hérité) ; le round-trip EXCLU du camp C
 * par nature (la commande le dit).
 * Auto-vérification AVANT toute mesure : bras_c.c porte sa propre main()
 * de vérification (les vecteurs dorés des contrats) — compilée hors
 * comparaison.
 */
#include <stdint.h>
#include <stddef.h>
#include <string.h>

#define TAMPON_SESSION 384
#define CUMUL_FENETRE  65536
#define LIGNE_TAILLE   77
#define MOTIF_MAX      32
#define BORNE_TAILLE   0x80000000ULL        /* 2 Gio — loupe-01 Q2 */
#define JOURNAL_MAX    256                  /* loupe-16 P3 */

typedef uint64_t u64; typedef uint32_t u32; typedef uint16_t u16;
typedef uint8_t  u8;

/* ---- freestanding : les trois seules fonctions de la runtime demandées -- */
void *memset(void *d, int c, size_t n) {
    u8 *p = (u8 *)d;
    for (size_t i = 0; i < n; i++) p[i] = (u8)c;
    return d;
}
void *memcpy(void *d, const void *s, size_t n) {
    u8 *p = (u8 *)d; const u8 *q = (const u8 *)s;
    for (size_t i = 0; i < n; i++) p[i] = q[i];
    return d;
}
int memcmp(const void *a, const void *b, size_t n) {
    const u8 *p = (const u8 *)a, *q = (const u8 *)b;
    for (size_t i = 0; i < n; i++)
        if (p[i] != q[i]) return p[i] < q[i] ? -1 : 1;
    return 0;
}

/* ---- la table des primitives OS (posée par le harnais : MÊMES shims) --
 * les POINTEURS sont ms_abi : les shims du mini-OS lisent le msx64
 * (rcx/rdx/r8/r9 + [rsp+0x28]) — la même convention que les blocs. */
#define OSABI __attribute__((ms_abi))
struct os_api {
    OSABI long (*CreateFileW)(const u16 *nom, u32 acces, u32 partage,
                              void *sa, u32 disposition);  /* -1 = invalide */
    OSABI int  (*GetFileSizeEx)(long h, u64 *taille);      /* 1/0          */
    OSABI int  (*SetFilePointerEx)(long h, long pos, u64 *nouvelle,
                                   u32 methode);
    OSABI int  (*ReadFile)(long h, u8 *dst, u32 n, u32 *lu, void *overlapped);
    OSABI int  (*CloseHandle)(long h);                     /* 1/0          */
    OSABI u32  (*GetLastError)(void);
};
/* la table des primitives, POSE PAR LE HARNAIS (il écrit la valeur
 * du pointeur avant tout appel — les MÊMES shims que le camp notation) */
const struct os_api *os;

/* ---- le cadre du camp C (le miroir des champs du plan) ---------------- */
struct cadre_c {
    u16  chemin[260];        /* +0     : le chemin copié (loupe-01 Q3)  */
    u64  reserve0;
    u64  taille;             /* +520/8 : la taille du fichier            */
    u64  poignee;            /*        : INVALIDE = 0 (session fermée)   */
    u64  remplissage;        /* +552/8 : la fenêtre effective (loupe-02) */
    u8   tampon[TAMPON_SESSION];
    u64  vue;                /* le défilement (loupe-11)                 */
    u64  curseur;            /* la cellule active                        */
    u32  sale;               /* la marque (loupe-16 Q4)                  */
    u32  refus_quitter;      /* la garde (loupe-18)                      */
    u8   nibble;             /* le premier chiffre hexa en attente       */
    u32  journal_n;          /* le nombre d'entrées distinctes           */
    struct { u64 decalage; u8 octet; u8 reserve[7]; } journal[JOURNAL_MAX];
    u8   cumul[CUMUL_FENETRE];   /* TAMPON_CUMUL (loupe-05 I3)           */
    u8   sortie32[32];           /* le condensé de gamme                  */
};
/* le cadre du camp C, POSE PAR LE HARNAIS (sa structure .data à lui) */
struct cadre_c *cadre_ptr;
#define C (*cadre_ptr)

/* ======================= loupe-05 : sha-256 (FIPS 180-4) =============== */
/* repris TEL QUEL du banc v0.11.0 (bench.c, auto-vérifié contre hashlib) */
#define ROR32(x,n) (((x)>>(n))|((x)<<(32-(n))))
static const uint32_t K256[64] = {
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,
    0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,
    0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,
    0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
    0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,
    0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,
    0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,
    0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
    0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
static void sha256_bloc(uint32_t h[8], const uint8_t b[64]) {
    uint32_t w[64];
    for (int i = 0; i < 16; i++)
        w[i] = ((uint32_t)b[4*i]<<24)|((uint32_t)b[4*i+1]<<16)
              |((uint32_t)b[4*i+2]<<8)|b[4*i+3];
    for (int i = 16; i < 64; i++) {
        uint32_t s0 = ROR32(w[i-15],7)^ROR32(w[i-15],18)^(w[i-15]>>3);
        uint32_t s1 = ROR32(w[i-2],17)^ROR32(w[i-2],19)^(w[i-2]>>10);
        w[i] = w[i-16]+s0+w[i-7]+s1;
    }
    uint32_t a=h[0],b2=h[1],c=h[2],d=h[3],e=h[4],f=h[5],g=h[6],h2=h[7];
    for (int i = 0; i < 64; i++) {
        uint32_t S1 = ROR32(e,6)^ROR32(e,11)^ROR32(e,25);
        uint32_t ch = (e&f)^((~e)&g);
        uint32_t t1 = h2+S1+ch+K256[i]+w[i];
        uint32_t S0 = ROR32(a,2)^ROR32(a,13)^ROR32(a,22);
        uint32_t mj = (a&b2)^(a&c)^(b2&c);
        h2=g; g=f; f=e; e=d+t1; d=c; c=b2; b2=a; a=t1+(S0+mj);
    }
    h[0]+=a;h[1]+=b2;h[2]+=c;h[3]+=d;h[4]+=e;h[5]+=f;h[6]+=g;h[7]+=h2;
}

/* les déclarations anticipées (loupe-01 compose 02 et 05 — Q4) */
__attribute__((ms_abi)) long loupe02_lire(u64 decalage);
__attribute__((ms_abi)) long loupe05_sha256(u64 decalage, u64 longueur,
                                             u8 *sortie);

/* ======================= loupe-01 · ouvrir (r3) ======================== */
/* Contrat loupe-01-ouvrir.md : P1 chemin, P2 session fermée, Q1..Q5,
 * E1..E4 (verdicts -2 ABSENT, -7 VERROUILLÉ, -6 SYSTÈME, -5 session,
 * -3 hors périmètre 2 Gio). */
__attribute__((ms_abi)) long loupe01_ouvrir(const u16 *chemin)
{
    if (C.poignee != 0) return -5;                 /* P2 : un à la fois   */
    if (chemin == NULL) return -5;                 /* E-l'entrée          */
    long h = os->CreateFileW(chemin, 0xC0000000u, 1u, NULL, 3u);  /* Q1  */
    if (h == -1) {                                 /* l'invalide : table */
        u32 e = os->GetLastError();                /* I4 : jamais un brut*/
        if (e == 2) return -2;                     /* E1 ABSENT          */
        if (e == 32) return -7;                    /* E2 VERROUILLÉ      */
        return -6;                                 /* E3 SYSTÈME         */
    }
    u64 t;
    if (!os->GetFileSizeEx(h, &t)) { os->CloseHandle(h); return -6; }
    if (t > BORNE_TAILLE) {                        /* Q2 la borne nommée  */
        os->CloseHandle(h);                        /* ferme AVANT retour  */
        return -3;
    }
    for (int i = 0; i < 260 && chemin[i]; i++)     /* Q3 le chemin copié  */
        C.chemin[i] = chemin[i];
    C.poignee = (u64)h;
    C.taille = (u64)t;
    C.remplissage = 0;
    C.vue = 0; C.curseur = 0;                      /* le vierge posé      */
    /* Q4 : la session née entière — la fenêtre SI taille > 0 (r3 : le
       vide n'a PAS de fenêtre), le panneau du vide DÉFINI (e3b0c442…)   */
    if (t > 0) {
        if (loupe02_lire(0) != 0) {                /* la première fenêtre */
            os->CloseHandle((long)C.poignee);
            C.poignee = 0;
            return -6;
        }
    } else {
        C.remplissage = 0;
    }
    if (loupe05_sha256(0, (u32)t, C.sortie32) != 0) {  /* le panneau      */
        os->CloseHandle((long)C.poignee);
        C.poignee = 0;
        return -6;
    }
    return 0;                                      /* Q5                 */
}

/* ======================= loupe-02 · lire =============================== */
/* Contrat loupe-02-lire.md : P1 session, P2 décalage multiple de 16,
 * P3 décalage < taille ; Q1 remplissage = min(384, taille − décalage) ;
 * Q2 le recouvrement du journal ; E1..E4 (-4, -5, -3, -6). */
__attribute__((ms_abi)) long loupe02_lire(u64 decalage)
{
    if (C.poignee == 0) return -4;                 /* E1 SESSION          */
    if (decalage & 15) return -5;                  /* E2 la grille droite */
    if (decalage >= C.taille) return -3;           /* E3 HORS-BORNES      */
    u64 n = C.taille - decalage;
    if (n > TAMPON_SESSION) n = TAMPON_SESSION;    /* Q1 la double borne  */
    if (!os->SetFilePointerEx((long)C.poignee, (long)decalage, NULL, 0u))
        { C.remplissage = 0; return -6; }          /* E4 fail-closed      */
    u32 lu;
    if (!os->ReadFile((long)C.poignee, C.tampon, (u32)n, &lu, NULL))
        { C.remplissage = 0; return -6; }
    C.remplissage = n;
    /* Q2 : le recouvrement — l'édition survit au défilement             */
    for (u32 i = 0; i < C.journal_n; i++) {
        u64 d = C.journal[i].decalage;
        if (d >= decalage && d < decalage + n)
            C.tampon[d - decalage] = C.journal[i].octet;
    }
    return 0;                                      /* Q3 : rien déplacé   */
}

/* ======================= loupe-05 · sha256 d'une gamme ================== */
/* Contrat loupe-05-sha256.md : P1 session, P2/P3 la gamme dans le fichier,
 * P4 la sortie ; Q1..Q4 par fenêtres de CUMUL_FENETRE ; E1..E4. */
__attribute__((ms_abi)) long loupe05_sha256(u64 decalage, u64 longueur,
                                             u8 *sortie)
{
    if (C.poignee == 0) return -4;                 /* E1                  */
    if (decalage + longueur > C.taille) return -3; /* E2 la gamme         */
    if (sortie == NULL) return -5;                 /* E3                  */
    uint32_t h[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                     0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    /* le contexte à cheval : les octets en attente PORTÉS d'une fenêtre à
       l'autre (le miroir de tls13-03 — jamais un bloc incomplet haché)   */
    u8 attente[64];
    u32 n_attente = 0;
    u64 fait = 0;
    while (fait < longueur) {                      /* Q2 les fenêtres     */
        u32 n = (longueur - fait > CUMUL_FENETRE)
                ? CUMUL_FENETRE : (u32)(longueur - fait);
        u32 lu;
        if (!os->SetFilePointerEx((long)C.poignee, (long)(decalage + fait),
                                  NULL, 0u)
            || !os->ReadFile((long)C.poignee, C.cumul, n, &lu, NULL)) {
            return -6;                             /* E4 : sortie INTACTE */
        }
        u32 o = 0;
        while (o < n) {                            /* tls13-03 l'absorb   */
            while (n_attente < 64 && o < n)
                attente[n_attente++] = C.cumul[o++];
            if (n_attente == 64) {
                sha256_bloc(h, attente);
                n_attente = 0;
            }
        }
        fait += n;
    }
    /* la finalisation (tls13-04) : le bourrage sur l'attente portée     */
    u8 fin[128];
    memset(fin, 0, sizeof fin);
    memcpy(fin, attente, n_attente);
    fin[n_attente] = 0x80;
    u32 fb = (n_attente < 56) ? 64 : 128;
    u64 bits = longueur * 8;
    for (int i = 0; i < 8; i++) fin[fb - 1 - i] = (u8)(bits >> (8*i));
    for (u32 o = 0; o < fb; o += 64) sha256_bloc(h, fin + o);
    for (int i = 0; i < 8; i++) {
        sortie[4*i]   = (u8)(h[i] >> 24);
        sortie[4*i+1] = (u8)(h[i] >> 16);
        sortie[4*i+2] = (u8)(h[i] >> 8);
        sortie[4*i+3] = (u8)(h[i]);
    }
    return 0;                                      /* Q4                 */
}

/* ======================= loupe-08 · ligne ============================== */
/* Contrat loupe-08-ligne.md : 77 o exactement — 8 hex du décalage, les
 * 16 groupes (l'espace médian doublé), le miroir ASCII, le NUL ; la
 * ligne incomplète garde le format ; E1..E3 (-5). */
static const char HEX[] = "0123456789ABCDEF";
__attribute__((ms_abi)) long loupe08_ligne(const u8 *source, u64 longueur,
                                            u8 *sortie, u64 decalage)
{
    if (source == NULL || sortie == NULL) return -5;   /* E3              */
    if (longueur == 0 || longueur > 16) return -5;     /* E1, E2          */
    u8 *p = sortie;
    for (int i = 28; i >= 0; i -= 4)                /* 8 hex, grand-bout  */
        *p++ = (u8)HEX[(decalage >> i) & 0xF];
    *p++ = ' '; *p++ = ' ';
    for (u64 i = 0; i < 16; i++) {
        if (i == 8) *p++ = ' ';                     /* l'espace médian    */
        if (i < longueur) {
            *p++ = (u8)HEX[source[i] >> 4];
            *p++ = (u8)HEX[source[i] & 0xF];
        } else {
            *p++ = ' '; *p++ = ' ';                 /* Q3 les absents     */
        }
        if (i < 15) *p++ = ' ';
    }
    *p++ = ' '; *p++ = ' ';
    for (u64 i = 0; i < 16; i++)                    /* Q2 le miroir       */
        *p++ = (i < longueur && source[i] >= 0x20 && source[i] <= 0x7E)
               ? source[i] : (i < longueur ? '.' : ' ');
    *p = 0;                                         /* le NUL             */
    return 0;                                       /* Q4                 */
}

/* ======================= loupe-13 · recherche =========================== */
/* Contrat loupe-13-recherche.md : l'algorithme pur — la PREMIÈRE
 * occurrence, -1 l'absence nommée, la plage vide -1 ; E1..E3 (-5).
 * ADAPTATION NOMMÉE (CA4) : la comparaison par memcmp du C — l'équivalent
 * compilé du libc-02 hérité du camp notation. */
__attribute__((ms_abi)) long loupe13_recherche(const u8 *fenetre,
                                                u64 taille, const u8 *motif,
                                                u64 taille_motif, u64 depart)
{
    if (taille_motif == 0 || taille_motif > MOTIF_MAX) return -5;  /* E1, E2 */
    if (depart > taille) return -5;                             /* E3      */
    if (taille_motif > taille - depart) return -1;              /* Q2 trivial */
    for (u64 i = depart; i + taille_motif <= taille; i++)
        if (memcmp(fenetre + i, motif, taille_motif) == 0)
            return (long)i;                                     /* Q1 la 1re */
    return -1;                                                  /* Q2 la fin */
}

/* ======================= loupe-16 · saisie ============================== */
/* Contrat loupe-16-saisie.md : les deux chiffres hexa, le journal PAR
 * DÉCALAGE (le remplacement, jamais le cumul), la vue si visible, la
 * marque, la garde ré-armée, le curseur qui avance ; E1..E4. */
__attribute__((ms_abi)) long loupe16_saisie(u64 caractere)
{
    if (C.poignee == 0) return -4;                 /* E1 SESSION          */
    int nib = -1;
    if (caractere >= '0' && caractere <= '9') nib = (int)(caractere - '0');
    else if (caractere >= 'A' && caractere <= 'F') nib = (int)(caractere - 'A' + 10);
    else if (caractere >= 'a' && caractere <= 'f') nib = (int)(caractere - 'a' + 10);
    else if (caractere == 0x08) {                  /* VK_SUPPR/RETOUR : Q5 */
        C.nibble = 0;                              /* annulée proprement  */
        return 0;
    } else return 0;                               /* E4 : ignoré propre  */
    if (C.nibble == 0) {                           /* Q1 le premier       */
        C.nibble = (u8)(nib + 1);                  /* 1..16 (0 = attente)*/
        return 0;
    }
    u8 octet = (u8)(((C.nibble - 1) << 4) | nib);  /* Q2 l'octet composé  */
    u64 cellule = C.curseur;
    if (cellule - C.vue >= C.remplissage)          /* E2 la cellule       */
        return -3;                                 /* fantôme : RIEN      */
    u32 j = 0;
    while (j < C.journal_n && C.journal[j].decalage != cellule) j++;
    if (j == C.journal_n) {                        /* l'entrée NEUVE      */
        if (C.journal_n >= JOURNAL_MAX) return -3; /* E3 le journal plein */
        C.journal[j].decalage = cellule;
        C.journal_n++;
    }
    C.journal[j].octet = octet;                    /* le REMPLACEMENT     */
    if (cellule - C.vue < C.remplissage)           /* Q3 la vue si visib. */
        C.tampon[cellule - C.vue] = octet;
    C.sale = 1;                                    /* Q4 la marque        */
    C.refus_quitter = 0;                           /* la garde ré-armée   */
    if (cellule + 1 < C.taille) cellule += 1;      /* le curseur avance   */
    C.curseur = cellule;
    C.nibble = 0;
    return 0;                                      /* Q5                  */
}

/* ================== l'auto-vérification (CA1, hors mesure) ============= */
/* compilée seulement à -DBRAS_C_AUTOTEST : les vecteurs dorés des
 * contrats — le vide, « abc » (sha256), les formats de ligne, les
 * recherches de l'école. Le harnais de comparaison appelle ces points
 * par leur symbole ; la vérification est exécutée AVANT toute mesure. */
#ifdef BRAS_C_AUTOTEST
#include <stdio.h>
static void sha256_simple(const u8 *m, u64 n, u8 out[32]) {
    uint32_t h[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                     0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    u64 bits = n * 8; u8 fin[128]; u32 queue = (u32)(n & 63);
    memset(fin, 0, sizeof fin);
    memcpy(fin, m, n); fin[queue] = 0x80;
    u32 fb = (queue < 56) ? 64 : 128;
    for (int i = 0; i < 8; i++) fin[fb - 1 - i] = (u8)(bits >> (8*i));
    u32 avant = (u32)(n - queue);
    for (u32 o = 0; o < avant; o += 64) sha256_bloc(h, m + o);
    for (u32 o = 0; o < fb; o += 64) sha256_bloc(h, fin + o);
    for (int i = 0; i < 8; i++) {
        out[4*i]=(u8)(h[i]>>24); out[4*i+1]=(u8)(h[i]>>16);
        out[4*i+2]=(u8)(h[i]>>8); out[4*i+3]=(u8)(h[i]);
    }
}
int main(void) {
    int ok = 1; u8 d[32];
    sha256_simple((const u8*)"", 0, d);            /* e3b0c442… le vide   */
    ok &= !memcmp(d, "\xe3\xb0\xc4\x42\x98\xfc\x1c\x14\x9a\xfb\xf4\xc8"
      "\x99\x6f\xb9\x24\x27\xae\x41\xe4\x64\x9b\x93\x4c\xa4\x95\x99\x1b"
      "\x78\x52\xb8\x55", 32);
    sha256_simple((const u8*)"abc", 3, d);         /* ba7816bf… l'école   */
    ok &= !memcmp(d, "\xba\x78\x16\xbf\x8f\x01\xcf\xea\x41\x41\x40\xde"
      "\x5d\xae\x22\x23\xb0\x03\x61\xa3\x96\x17\x7a\x9c\xb4\x10\xff\x61"
      "\xf2\x00\x15\xad", 32);
    u8 ligne[77];
    ok &= loupe08_ligne((const u8*)"MZ\x90\x00\x03\x00\x00\x00"
        "\x04\x00\x00\x00\xff\xff\x00\x00", 16, ligne, 0) == 0;
    ok &= !memcmp(ligne, "00000000  4D 5A 90 00 03 00 00 00  04 00 00 "
        "00 FF FF 00 00  MZ..............", 76);
    ok &= loupe13_recherche((const u8*)"AAAAB", 5, (const u8*)"AAAA", 4, 0) == 0;
    ok &= loupe13_recherche((const u8*)"AAAAB", 5, (const u8*)"AAAB", 4, 0) == 1;
    ok &= loupe13_recherche((const u8*)"AAAAB", 5, (const u8*)"AAB", 3, 2) == 2;
    ok &= loupe13_recherche((const u8*)"AAAAB", 5, (const u8*)"Z", 1, 0) == -1;
    printf(ok ? "BRAS_C_AUTOTEST : VERT\n" : "BRAS_C_AUTOTEST : FAUX\n");
    return ok ? 0 : 1;
}
#endif
