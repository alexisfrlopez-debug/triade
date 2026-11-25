/* dudect_collab.c — LE MESUREUR DE LA QUESTION (edition COLLAB x86-64, v1.0.0)
 *
 * La commande (le developpeur, 25/11/2026) : « fais le kit collab » —
 * l'avis de l'Entree 421 donne le matin meme : OUI, pas comme preuve,
 * comme DISCRIMINATEUR. LA QUESTION que ce kit pose : les trois
 * divergences |t|>5 du 24/11 au portable (tls13-02 : -10,64 ; tls13-13 :
 * +9,65 ; tls13-16 : +9,19 — l'Entree 416 les lut comme l'oscillation
 * DVFS d'un portable 2 cœurs aux classes SEQUENTIELLES) SUIVENT-ELLES
 * LA MACHINE OU LE CODE ? Sur un silicium serveur mutualise, cadence
 * stable, classes ENTRELAKEES : si elles disparaissent, la lecture DVFS
 * se renforce ; si elles persistent sur un troisieme microarchitecture,
 * la divergence suit le code — resultat nomme, jamais maquille.
 *
 * CE QUE CE KIT EST, HONNETEMENT :
 *   — le protocole COLLAB-X86-1, NOUVEAU, PRE-ENREGISTRE au
 *     LISEZMOI-dudect-collab.txt de ce kit AVANT tout run : l'equation
 *     exacte y vit, AUCUN chiffre ne sera fabrique hors d'elle ;
 *   — compile SUR LA MACHINE MEME depuis CETTE source (la source est la
 *     verite) ; la machine Colab est une machine de COMMODITE : elle SE
 *     NOMME (D206) — silicium MUTUALISE aux voisins inconnus (le t
 *     mesurera AUSSI eux), DVFS opaque sous l'hyperviseur (pas de cadre
 *     de frequence cockpit : la cadence se constate aux temps eux-memes),
 *     session EPHEMERE (rapatriez les pieces AVANT la fin — la leçon
 *     Termux de l'Entree 419) ;
 *   — la hierarchie d'evidence est INCHANGEE : le banc controle
 *     (portable, telephone) demeure la reference ; ce run est une
 *     lecture de commodite, jamais une preuve ;
 *   — les QUATRE cibles SCELLEES mesurees ici sont les familles crypto
 *     de proxy-image.bin (la piece scellee v0.15.0, l'image memoire
 *     etendue posée par l'extracteur du kit-2) : l'image est RECOUPEE
 *     (sha256 entier + sha256 de CHAQUE plage de cible contre le
 *     manifeste) AVANT toute execution, ET l'epreuve FIPS « abc » est
 *     exigée DE LA PIECE SCELLEE ELLE-MEME (le geste de test_appel.c :
 *     tls13-02 doit rendre le condense exact, puis la mutation d'un
 *     octet de sa table K doit DIVERGER le condense, puis la
 *     restauration doit le rendre exact) — l'image executee est la
 *     piece recoupee, RIEN d'autre n'est execute ;
 *   — loupe.exe et moteur-shani.bin (les autres pieces scellees) sont
 *     HORS PERIMETRE de ce kit : leurs empreintes sont CITEES, elles ne
 *     sont pas mesurees ici (chacune a son kit : la vitrine kit-3, le
 *     couloir SHA-NI kit-1 au poste reel).
 *
 * LES HUIT CIBLES (l'ordre pre-enregistre) :
 *   1. eq-constant     le CONTROLE POSITIF : comparaison 32 octets par
 *                      OU masque, AUCUN branchement sur le secret —
 *                      attendu : aucune divergence (une divergence est
 *                      un RESULTAT, D189 : consigner tel quel) ;
 *   2. eq-branchue     le CONTROLE NEGATIF : la sortie au premier octet
 *                      divergent — LE FAUX PATRON. Attendu : DIVERGENCE.
 *                      Sinon l'instrument est CONTESTE, nomme, jamais
 *                      muet ;
 *   3. sha256-logiciel la compression logicielle d'un bloc de 64 (la
 *                      meme mecanique que la cible tls13-02) ;
 *   4. sha256-x86-shani la compression par les INSTRUCTIONS MATERIELLES
 *                      SHA-NI (sha256rnds2/sha256msg1/sha256msg2 — la
 *                      famille x86, UNE AUTRE que la FEAT_SHA256 ARM du
 *                      kit-B : les deux mondes se constatent, aucun ne
 *                      se deguise). VIT seulement si le noyau expose le
 *                      drapeau « sha_ni » ET que le compilateur a
 *                      accepte -msha — la double garde ; REFUS NOMME
 *                      sinon, le reste du run vit ;
 *   5. tls13-02        SCELLEE : la compression SHA-256 de la piece —
 *                      l'etat AMONT est l'IV, le bloc 64 est LE SECRET ;
 *   6. tls13-13        SCELLEE : l'echelle X25519 — le scalaire est LE
 *                      SECRET, u est l'auxiliaire fixe ;
 *   7. tls13-16        SCELLEE : le bloc AES-128 — les 176 octets de
 *                      cles sont LE SECRET, l'entree est l'auxiliaire ;
 *   8. tls13-17        SCELLEE : le GHASH GF(2^128) — X est LE SECRET,
 *                      Y l'auxiliaire.
 *
 * LA MECANIQUE (l'equation du protocole COLLAB-X86-1) :
 *   — le compteur : RDTSC sur x86-64 (la grandeur est « ticks », jamais
 *     « cycles » — le TSC d'un serveur mutualise est invariant
 *     (constant_tsc/nonstop_tsc constates aux drapeaux) mais SA
 *     FREQUENCE N'EST PAS LUE : aucun chiffre en « secondes par appel »
 *     ne sera fabrique, seul le contrepoint CLOCK_MONOTONIC vit au csv) ;
 *   — l'ENTRELACEMENT : a CHAQUE iteration la premiere classe vit puis
 *     la seconde (le secret regenere hors mesure) — LA DIFFERENCE NOMMEE
 *     avec le kit-2 du 24/11, aux classes SEQUENTIELLES : c'est le cœur
 *     du discriminateur, un protocole NOUVEAU se definit juste ;
 *   — l'AMPLIFICATION (l'equation pre-enregistree, pas de reglage au
 *     terrain) : LOT=512 pour eq-constant/eq-branchue/tls13-16/tls13-17,
 *     LOT=64 pour sha256-logiciel/sha256-x86-shani/tls13-02, LOT=1 pour
 *     tls13-13 (l'echelle X25519 est lente a elle seule) ;
 *   — l'echauffement : 100 paires par cible, resultats jetes ;
 *   — N par classe, N=60 puis N=200 puis N=400 DANS CET ORDRE (l'ordre
 *     du LISEZMOI-KITS-TERRAIN) ;
 *   — la statistique : le t de Welch sur les ticks, le seuil |t| > 5
 *     (les memes parametres que le kit-2, le kit-B et l'edition
 *     structurelle v0.11.0) ;
 *   — L'EPREUVE PREALABLE (fail-closed, TROIS lecteurs) : le condense
 *     FIPS 180-4 « abc » EXACT exige du lecteur LOGICIEL, du lecteur
 *     SHA-NI (s'il vit) ET DE LA PIECE SCELLEE tls13-02 (avec
 *     l'adversaire de mutation K) AVANT toute mesure — un lecteur faux
 *     est un REFUS : rien n'est mesure.
 *
 * LES SORTIES :
 *   la console                       le run entier, ligne par ligne ;
 *   journal-dudect-collab-<ns>.csv   cible,classe,iteration,ticks,secondes
 *   (le temoin auto-portant est compose par scenario-collab.py qui
 *    orchestre les trois runs 60/200/400 et ecrit les temoins).
 *
 * Codes de sortie : 0 = LE RUN VECU (vert ou ecarts nommes au verdict) ;
 *                   2 = REFUS NOMME AVANT MESURE (lecteur FIPS faux,
 *                       image divergente, journal impossible).
 *
 * Compilation (le lanceur le fait pour vous) :
 *   gcc -O2 -msha -mssse3 -msse4.1 -o run/dudect_collab dudect_collab.c -lm
 *   gcc -O2                    -o run/dudect_collab dudect_collab.c -lm
 * (le drapeau -msha n'expose QUE la cible materielle SHA-NI ; les
 *  melanges de l'assemblage demandent AUSSI -mssse3 -msse4.1 — des
 *  familles ANTERIEURES que toute CPU portant sha_ni possede de facto
 *  (Goldmont 2016, Skylake) : la double garde compile + drapeau noyau
 *  demeure exacte. Sans ces drapeaux, la cible est REFUSEE PAR NATURE
 *  — nommee.)
 *
 * Eprouve au laboratoire AVANT assemblage (la mecanique, jamais le
 * statut terrain) : le bac EST un Linux x86-64 (Xeon, sha_ni present,
 * drapeau hypervisor present) — le run complet fut vecu au bac avec
 * l'etiquette AUTOTEST, consoles au dossier preuves-labo/ du paquet.
 * L'AUTOTEST PROUVE LA MECANIQUE, AUCUN statut terrain n'en decoule —
 * le run Colab appartient au developpeur.
 *
 * Usage : dudect_collab [N_par_classe] [--autotest] [--fips]
 *         (defauts : 200 ; --autotest force N=60 et l'etiquette labo ;
 *          --fips vit la seule epreuve FIPS puis sort)
 */

#if !defined(__x86_64__)
#error "dudect_collab.c vit sur x86-64 (l'edition COLLAB) — les pieces scellees sont x86-64 : compilez sur la machine Colab (ou le bac x86-64 du laboratoire)"
#endif

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <sched.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>

/* ---- les pieces scellees v0.15.0 : empreintes CITEES ----
 * proxy-image.bin est MESUREE ici (recoupee avant execution) ;
 * loupe.exe et moteur-shani.bin sont HORS PERIMETRE de ce kit. */
static const char *PIECES_CITEES[] = {
    "proxy-image.bin  MESUREE ICI (recoup: 0782d7e20d0bd4a268e6ec7ed0"
    "dc1453a0f42d7e72b784c2acc9ed423a885dff)",
    "loupe.exe 0.1.1  HORS PERIMETRE (sa vitrine est le kit-3) sha256 "
    "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1",
    "moteur-shani.bin HORS PERIMETRE (son couloir est le kit-1 au poste "
    "reel) sha256 761ab194d88d527c653111a41324b0bb3e9247b1c56ba8dc9fede"
    "eccbe04bcec",
};

/* ---- l'alea (/dev/urandom — reprise veritable de dudect_v150.c) ---- */
static void alea(unsigned char *p, size_t n) {
    static int fd = -1;
    if (fd < 0) fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0 || (size_t)read(fd, p, n) != n) {
        fprintf(stderr, "[REFUS] /dev/urandom\n"); exit(2); }
}

static double horloge_sec(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return (double)t.tv_sec + 1e-9 * (double)t.tv_nsec;
}

static int poser_affinite(int coeur) {
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(coeur, &m);
    return sched_setaffinity(0, sizeof(m), &m) == 0;
}

/* ---- le compteur : TSC (le serveur mutualise se nomme, D206) ---- */
static uint64_t lecteur_tsc(void) {
    unsigned int a, d;
    __asm__ volatile ("rdtsc" : "=a"(a), "=d"(d));
    return ((uint64_t)d << 32) | a;
}

/* ---- SHA-256 : la table K et la mecanique de dudect_v150.c (la meme source) ---- */
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
static uint32_t ror32(uint32_t x, int n) { return (x>>n)|(x<<(32-n)); }

/* la compression LOGICIELLE d'un bloc de 64 octets — noinline et le
 * bloc VOLATIL : le compilateur ne peut NI plier l'appel dans la boucle
 * de lot, NI hisser les lectures hors des iterations mesurees */
__attribute__((noinline))
static void sha256_compress(uint32_t h[8], const volatile unsigned char bloc[64]) {
    uint32_t w[64];
    for (int i = 0; i < 16; i++) {
        unsigned char p0 = bloc[4*i], p1 = bloc[4*i+1];
        unsigned char p2 = bloc[4*i+2], p3 = bloc[4*i+3];
        w[i] = ((uint32_t)p0<<24)|((uint32_t)p1<<16)
             |((uint32_t)p2<<8)|(uint32_t)p3;
    }
    for (int i = 16; i < 64; i++) {
        uint32_t s0 = ror32(w[i-15],7)^ror32(w[i-15],18)^(w[i-15]>>3);
        uint32_t s1 = ror32(w[i-2],17)^ror32(w[i-2],19)^(w[i-2]>>10);
        w[i] = w[i-16]+s0+w[i-7]+s1;
    }
    uint32_t a=h[0],bb=h[1],c=h[2],dd=h[3],e=h[4],f=h[5],g=h[6],hh=h[7];
    for (int i = 0; i < 64; i++) {
        uint32_t S1 = ror32(e,6)^ror32(e,11)^ror32(e,25);
        uint32_t ch = (e&f)^((~e)&g);
        uint32_t t1 = hh+S1+ch+K256[i]+w[i];
        uint32_t S0 = ror32(a,2)^ror32(a,13)^ror32(a,22);
        uint32_t mj = (a&bb)^(a&c)^(bb&c);
        uint32_t t2 = S0+mj;
        hh=g; g=f; f=e; e=dd+t1; dd=c; c=bb; bb=a; a=t1+t2;
    }
    h[0]+=a; h[1]+=bb; h[2]+=c; h[3]+=dd;
    h[4]+=e; h[5]+=f; h[6]+=g; h[7]+=hh;
}

/* le condense complet (le bourrement FIPS 180-4 — pour l'epreuve « abc ») */
static void sha256(const unsigned char *d, size_t n, unsigned char o[32]) {
    uint32_t h[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                     0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    size_t reste = n % 64;
    size_t nb = n/64 + 1;
    if (reste >= 56) nb++;
    unsigned char *t = (unsigned char*)calloc(nb, 64);
    if (!t) { fprintf(stderr, "[REFUS] memoire\n"); exit(2); }
    memcpy(t, d, n);
    t[n] = 0x80;
    uint64_t bits = (uint64_t)n * 8;
    for (int i = 0; i < 8; i++)
        t[nb*64 - 1 - i] = (unsigned char)((bits >> (8*i)) & 0xff);
    for (size_t b = 0; b < nb; b++)
        sha256_compress(h, t + b*64);
    free(t);
    for (int i = 0; i < 8; i++) {
        o[4*i]=(unsigned char)(h[i]>>24); o[4*i+1]=(unsigned char)(h[i]>>16);
        o[4*i+2]=(unsigned char)(h[i]>>8); o[4*i+3]=(unsigned char)h[i];
    }
}

/* ---- la compression MATERIELLE : SHA-NI x86 (sha256rnds2/msg1/msg2) ----
 * Compilee seulement si le compilateur a accepte -msha -mssse3 -msse4.1
 * (les melanges alignr/blend vivent aux familles anterieures, que toute
 * CPU sha_ni porte de facto) ; executee seulement si le NOYAU expose le
 * drapeau « sha_ni » — la double garde. Les groupes de K sont charges
 * depuis la table K256 VERIFIEE ci-dessus (pas de constante repaquee :
 * la meme source de verite). */
#if defined(__SHA__) && defined(__SSSE3__) && defined(__SSE4_1__)
#include <immintrin.h>
#define SHANI_COMPILABLE 1
__attribute__((noinline))
static void sha256_x86_shani(uint32_t etat[8],
                             const volatile unsigned char bloc[64]) {
    unsigned char b[64];
    for (int i = 0; i < 64; i++) b[i] = bloc[i];   /* la relecture honnete */
    __m128i STATE0, STATE1, MSG, TMP, MASK;
    __m128i TMSG0, TMSG1, TMSG2, TMSG3;
    __m128i ABEF_SAVE, CDGH_SAVE;
    MASK = _mm_set_epi64x(0x0c0d0e0f08090a0bULL, 0x0405060700010203ULL);
    TMP    = _mm_loadu_si128((const __m128i *)&etat[0]);
    STATE1 = _mm_loadu_si128((const __m128i *)&etat[4]);
    TMP    = _mm_shuffle_epi32(TMP, 0xB1);          /* CDAB */
    STATE1 = _mm_shuffle_epi32(STATE1, 0x1B);       /* EFGH */
    STATE0 = _mm_alignr_epi8(TMP, STATE1, 8);       /* ABEF */
    STATE1 = _mm_blend_epi16(STATE1, TMP, 0xF0);    /* CDGH */
    ABEF_SAVE = STATE0;
    CDGH_SAVE = STATE1;
    /* Rounds 0-3 */
    TMSG0 = _mm_shuffle_epi8(_mm_loadu_si128((const __m128i *)(b + 0)), MASK);
    MSG = _mm_add_epi32(TMSG0, _mm_loadu_si128((const __m128i *)&K256[0]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    /* Rounds 4-7 */
    TMSG1 = _mm_shuffle_epi8(_mm_loadu_si128((const __m128i *)(b + 16)), MASK);
    MSG = _mm_add_epi32(TMSG1, _mm_loadu_si128((const __m128i *)&K256[4]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG0 = _mm_sha256msg1_epu32(TMSG0, TMSG1);
    /* Rounds 8-11 */
    TMSG2 = _mm_shuffle_epi8(_mm_loadu_si128((const __m128i *)(b + 32)), MASK);
    MSG = _mm_add_epi32(TMSG2, _mm_loadu_si128((const __m128i *)&K256[8]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG1 = _mm_sha256msg1_epu32(TMSG1, TMSG2);
    /* Rounds 12-15 */
    TMSG3 = _mm_shuffle_epi8(_mm_loadu_si128((const __m128i *)(b + 48)), MASK);
    MSG = _mm_add_epi32(TMSG3, _mm_loadu_si128((const __m128i *)&K256[12]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG3, TMSG2, 4);
    TMSG0 = _mm_add_epi32(TMSG0, TMP);
    TMSG0 = _mm_sha256msg2_epu32(TMSG0, TMSG3);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG2 = _mm_sha256msg1_epu32(TMSG2, TMSG3);
    /* Rounds 16-19 */
    MSG = _mm_add_epi32(TMSG0, _mm_loadu_si128((const __m128i *)&K256[16]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG0, TMSG3, 4);
    TMSG1 = _mm_add_epi32(TMSG1, TMP);
    TMSG1 = _mm_sha256msg2_epu32(TMSG1, TMSG0);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG3 = _mm_sha256msg1_epu32(TMSG3, TMSG0);
    /* Rounds 20-23 */
    MSG = _mm_add_epi32(TMSG1, _mm_loadu_si128((const __m128i *)&K256[20]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG1, TMSG0, 4);
    TMSG2 = _mm_add_epi32(TMSG2, TMP);
    TMSG2 = _mm_sha256msg2_epu32(TMSG2, TMSG1);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG0 = _mm_sha256msg1_epu32(TMSG0, TMSG1);
    /* Rounds 24-27 */
    MSG = _mm_add_epi32(TMSG2, _mm_loadu_si128((const __m128i *)&K256[24]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG2, TMSG1, 4);
    TMSG3 = _mm_add_epi32(TMSG3, TMP);
    TMSG3 = _mm_sha256msg2_epu32(TMSG3, TMSG2);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG1 = _mm_sha256msg1_epu32(TMSG1, TMSG2);
    /* Rounds 28-31 */
    MSG = _mm_add_epi32(TMSG3, _mm_loadu_si128((const __m128i *)&K256[28]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG3, TMSG2, 4);
    TMSG0 = _mm_add_epi32(TMSG0, TMP);
    TMSG0 = _mm_sha256msg2_epu32(TMSG0, TMSG3);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG2 = _mm_sha256msg1_epu32(TMSG2, TMSG3);
    /* Rounds 32-35 */
    MSG = _mm_add_epi32(TMSG0, _mm_loadu_si128((const __m128i *)&K256[32]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG0, TMSG3, 4);
    TMSG1 = _mm_add_epi32(TMSG1, TMP);
    TMSG1 = _mm_sha256msg2_epu32(TMSG1, TMSG0);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG3 = _mm_sha256msg1_epu32(TMSG3, TMSG0);
    /* Rounds 36-39 */
    MSG = _mm_add_epi32(TMSG1, _mm_loadu_si128((const __m128i *)&K256[36]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG1, TMSG0, 4);
    TMSG2 = _mm_add_epi32(TMSG2, TMP);
    TMSG2 = _mm_sha256msg2_epu32(TMSG2, TMSG1);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG0 = _mm_sha256msg1_epu32(TMSG0, TMSG1);
    /* Rounds 40-43 */
    MSG = _mm_add_epi32(TMSG2, _mm_loadu_si128((const __m128i *)&K256[40]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG2, TMSG1, 4);
    TMSG3 = _mm_add_epi32(TMSG3, TMP);
    TMSG3 = _mm_sha256msg2_epu32(TMSG3, TMSG2);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG1 = _mm_sha256msg1_epu32(TMSG1, TMSG2);
    /* Rounds 44-47 */
    MSG = _mm_add_epi32(TMSG3, _mm_loadu_si128((const __m128i *)&K256[44]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG3, TMSG2, 4);
    TMSG0 = _mm_add_epi32(TMSG0, TMP);
    TMSG0 = _mm_sha256msg2_epu32(TMSG0, TMSG3);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG2 = _mm_sha256msg1_epu32(TMSG2, TMSG3);
    /* Rounds 48-51 */
    MSG = _mm_add_epi32(TMSG0, _mm_loadu_si128((const __m128i *)&K256[48]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG0, TMSG3, 4);
    TMSG1 = _mm_add_epi32(TMSG1, TMP);
    TMSG1 = _mm_sha256msg2_epu32(TMSG1, TMSG0);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    TMSG3 = _mm_sha256msg1_epu32(TMSG3, TMSG0);
    /* Rounds 52-55 */
    MSG = _mm_add_epi32(TMSG1, _mm_loadu_si128((const __m128i *)&K256[52]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG1, TMSG0, 4);
    TMSG2 = _mm_add_epi32(TMSG2, TMP);
    TMSG2 = _mm_sha256msg2_epu32(TMSG2, TMSG1);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    /* Rounds 56-59 */
    MSG = _mm_add_epi32(TMSG2, _mm_loadu_si128((const __m128i *)&K256[56]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    TMP = _mm_alignr_epi8(TMSG2, TMSG1, 4);
    TMSG3 = _mm_add_epi32(TMSG3, TMP);
    TMSG3 = _mm_sha256msg2_epu32(TMSG3, TMSG2);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    /* Rounds 60-63 */
    MSG = _mm_add_epi32(TMSG3, _mm_loadu_si128((const __m128i *)&K256[60]));
    STATE1 = _mm_sha256rnds2_epu32(STATE1, STATE0, MSG);
    MSG = _mm_shuffle_epi32(MSG, 0x0E);
    STATE0 = _mm_sha256rnds2_epu32(STATE0, STATE1, MSG);
    /* l'addition de flux et la remise en ordre */
    STATE0 = _mm_add_epi32(STATE0, ABEF_SAVE);
    STATE1 = _mm_add_epi32(STATE1, CDGH_SAVE);
    TMP    = _mm_shuffle_epi32(STATE0, 0x1B);       /* FEBA */
    STATE1 = _mm_shuffle_epi32(STATE1, 0xB1);       /* DCHG */
    STATE0 = _mm_blend_epi16(TMP, STATE1, 0xF0);    /* DCBA */
    STATE1 = _mm_alignr_epi8(STATE1, TMP, 8);       /* ABEF */
    _mm_storeu_si128((__m128i *)&etat[0], STATE0);
    _mm_storeu_si128((__m128i *)&etat[4], STATE1);
}
/* le condense complet par la voie MATERIELLE (l'epreuve FIPS) */
static void sha256_shani(const unsigned char *d, size_t n, unsigned char o[32]) {
    uint32_t h[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                     0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    size_t reste = n % 64;
    size_t nb = n/64 + 1;
    if (reste >= 56) nb++;
    unsigned char *t = (unsigned char*)calloc(nb, 64);
    if (!t) { fprintf(stderr, "[REFUS] memoire\n"); exit(2); }
    memcpy(t, d, n);
    t[n] = 0x80;
    uint64_t bits = (uint64_t)n * 8;
    for (int i = 0; i < 8; i++)
        t[nb*64 - 1 - i] = (unsigned char)((bits >> (8*i)) & 0xff);
    for (size_t b = 0; b < nb; b++)
        sha256_x86_shani(h, t + b*64);
    free(t);
    for (int i = 0; i < 8; i++) {
        o[4*i]=(unsigned char)(h[i]>>24); o[4*i+1]=(unsigned char)(h[i]>>16);
        o[4*i+2]=(unsigned char)(h[i]>>8); o[4*i+3]=(unsigned char)h[i];
    }
}
#else
#define SHANI_COMPILABLE 0
#endif

/* ---- les deux controles de l'instrument ---- */
/* le POSITIF : le OU masque — AUCUN branchement sur le secret */
__attribute__((noinline))
static int eq_constant(const volatile unsigned char *a,
                       const volatile unsigned char *b, size_t n) {
    unsigned char diff = 0;
    for (size_t i = 0; i < n; i++) diff |= a[i] ^ b[i];
    return (int)((diff - 1) >> 8) & 1;    /* 1 si egaux — sans branche */
}
/* le NEGATIF : la sortie au premier octet divergent — LE FAUX PATRON */
__attribute__((noinline))
static int eq_branchue(const volatile unsigned char *a,
                       const volatile unsigned char *b, size_t n) {
    for (size_t i = 0; i < n; i++)
        if (a[i] != b[i]) return 0;
    return 1;
}

/* ---- le puits (le resultat consomme — rien n'est elimine) ---- */
static volatile unsigned long g_puits = 0;

/* ---- les contrats de couche I (la convention Windows x64, ms_abi) ----
 * (reprise veritable de dudect_v150.c — le mesureur du kit-2) */
#if defined(__GNUC__)
#define MSABI __attribute__((ms_abi))
#else
#define MSABI
#endif
typedef void (MSABI *f_sha256_t)(uint32_t *etat8, const unsigned char *b64);
typedef void (MSABI *f_x25519_t)(unsigned char *s32,
                                 const unsigned char *scalaire32,
                                 const unsigned char *u32_);
typedef void (MSABI *f_aes128_t)(const unsigned char *cles176,
                                 const unsigned char *entree16,
                                 unsigned char *sortie16);
typedef void (MSABI *f_ghash_t)(unsigned char *z16,
                                const unsigned char *x16,
                                const unsigned char *y16);

/* ---- le manifeste simple (reprise veritable de dudect_v150.c) ---- */
typedef struct {
    char nom[16]; unsigned char sha_plage[32];
    size_t rva, taille; int famille;
} cible_t;

static void hex_vers(const char *hx, unsigned char *o, int n) {
    char t[3] = {0,0,0};
    for (int i = 0; i < n; i++) {
        t[0] = hx[2*i]; t[1] = hx[2*i+1];
        o[i] = (unsigned char)strtoul(t, NULL, 16);
    }
}

enum { F_SHA, F_X25519, F_AES, F_GHASH };

static int lire_manifeste(const char *rep, char sha_image[65],
                          size_t *taille_image, cible_t *tab, int max) {
    char chemin[512];
    snprintf(chemin, sizeof chemin, "%s/manifeste-c.txt", rep);
    FILE *f = fopen(chemin, "r");
    if (!f) { fprintf(stderr, "[REFUS] manifeste introuvable : %s\n",
                      chemin); return -1; }
    char ligne[512]; int n = 0; char sha[65];
    while (fgets(ligne, sizeof ligne, f)) {
        if (sscanf(ligne, "image %64s", sha) == 1)
            memcpy(sha_image, sha, 65);
        else if (sscanf(ligne, "taille %zu", taille_image) == 1) { }
        else if (sscanf(ligne, "cible %15s %zu %zu %64s",
                        tab[n].nom, &tab[n].rva, &tab[n].taille, sha) == 4) {
            hex_vers(sha, tab[n].sha_plage, 32);
            if (strncmp(tab[n].nom, "tls13-02", 8) == 0)
                tab[n].famille = F_SHA;
            else if (strncmp(tab[n].nom, "tls13-13", 8) == 0)
                tab[n].famille = F_X25519;
            else if (strncmp(tab[n].nom, "tls13-16", 8) == 0)
                tab[n].famille = F_AES;
            else if (strncmp(tab[n].nom, "tls13-17", 8) == 0)
                tab[n].famille = F_GHASH;
            else tab[n].famille = -1;
            if (++n >= max) break;
        }
    }
    fclose(f);
    return n;
}

/* ---- l'epreuve FIPS DEPUIS LA PIECE SCELLEE (le geste de test_appel.c) ---- */
static const uint32_t IV256[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,
                                  0xa54ff53a,0x510e527f,0x9b05688c,
                                  0x1f83d9ab,0x5be0cd19};
static void condense_abc_scellee(void *fn, unsigned char out[32]) {
    unsigned char bloc[64];
    memset(bloc, 0, sizeof bloc);
    bloc[0] = 'a'; bloc[1] = 'b'; bloc[2] = 'c'; bloc[3] = 0x80;
    bloc[63] = 24;   /* la longueur 24 bits, grand-boutiste au dernier mot */
    uint32_t etat[8];
    memcpy(etat, IV256, sizeof etat);
    ((f_sha256_t)fn)(etat, bloc);
    for (int i = 0; i < 8; i++) {
        out[4*i]=(unsigned char)(etat[i]>>24); out[4*i+1]=(unsigned char)(etat[i]>>16);
        out[4*i+2]=(unsigned char)(etat[i]>>8); out[4*i+3]=(unsigned char)etat[i];
    }
}

/* ---- la statistique (reprise veritable de dudect_v150.c) ---- */
#define NMAX 4096
typedef struct { uint64_t cyc[NMAX]; double sec[NMAX]; size_t n; } serie_t;
static double moy(const uint64_t *x, size_t n) {
    double s = 0; for (size_t i = 0; i < n; i++) s += (double)x[i];
    return s / (double)n;
}
static double var(const uint64_t *x, size_t n, double m) {
    double s = 0; for (size_t i = 0; i < n; i++) {
        double d = (double)x[i] - m; s += d * d; }
    return n > 1 ? s / (double)(n - 1) : 0.0;
}
static double t_welch(const serie_t *a, const serie_t *b) {
    double ma = moy(a->cyc, a->n), mb = moy(b->cyc, b->n);
    double va = var(a->cyc, a->n, ma) / (double)a->n;
    double vb = var(b->cyc, b->n, mb) / (double)b->n;
    double den = sqrt(va + vb);
    return den > 0 ? (ma - mb) / den : 0.0;
}
static uint64_t mediane(uint64_t *x, size_t n) {
    for (size_t i = 1; i < n; i++) { uint64_t k = x[i]; size_t j = i;
        while (j > 0 && x[j-1] > k) { x[j] = x[j-1]; j--; }
        x[j] = k; }
    return x[n/2];
}

static void hexa(const unsigned char *p, int n, char *o) {
    for (int i = 0; i < n; i++) sprintf(o + 2*i, "%02x", p[i]);
    o[2*n] = 0;
}

/* ---- le drapeau du noyau (le jeton EXACT, jamais un sous-mot) ---- */
static int drapeau_cpuinfo(const char *jeton) {
    FILE *f = fopen("/proc/cpuinfo", "r");
    if (!f) return -1;                       /* illisible : constate tel quel */
    char ligne[8192];
    int vu = 0;
    size_t l = strlen(jeton);
    while (fgets(ligne, sizeof ligne, f)) {
        if (strncmp(ligne, "flags", 5) != 0) continue;
        char *c = ligne;
        while (*c) {
            char *d = c;
            while (*d && *d != ' ' && *d != '\t' && *d != '\n') d++;
            if ((size_t)(d - c) == l && memcmp(c, jeton, l) == 0) { vu = 1; break; }
            c = (*d) ? d + 1 : d;
        }
        break;
    }
    fclose(f);
    return vu;
}

/* ---- l'appel par cible ---- */
enum { T_EQ_CT, T_EQ_BR, T_SHA_SW, T_SHA_HW, T_TLS02, T_TLS13, T_TLS16, T_TLS17 };
static void appeler(int t, void *fn, unsigned char *secret,
                    unsigned char *aux, unsigned char *sortie) {
    uint32_t etat[8];
    switch (t) {
    case T_EQ_CT:  g_puits += (unsigned long)eq_constant(secret, aux, 32); break;
    case T_EQ_BR:  g_puits += (unsigned long)eq_branchue(secret, aux, 32); break;
    case T_SHA_SW: memcpy(etat, IV256, sizeof etat);
                   sha256_compress(etat, secret); g_puits += etat[0]; break;
#if SHANI_COMPILABLE
    case T_SHA_HW: memcpy(etat, IV256, sizeof etat);
                   sha256_x86_shani(etat, secret); g_puits += etat[0]; break;
#endif
    case T_TLS02:  memcpy(etat, IV256, sizeof etat);
                   ((f_sha256_t)fn)(etat, secret); g_puits += etat[0]; break;
    case T_TLS13:  ((f_x25519_t)fn)(sortie, secret, aux);
                   g_puits += sortie[0]; break;
    case T_TLS16:  ((f_aes128_t)fn)(secret, aux, sortie);
                   g_puits += sortie[0]; break;
    case T_TLS17:  ((f_ghash_t)fn)(sortie, secret, aux);
                   g_puits += sortie[0]; break;
    }
}

int main(int argc, char **argv) {
    volatile size_t n = 200;
    volatile int autotest = 0, fips_seul = 0;
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--autotest") == 0) autotest = 1;
        else if (strcmp(argv[i], "--fips") == 0) fips_seul = 1;
        else if (i == 1) { n = (size_t)strtoul(argv[i], NULL, 10); }
        else { fprintf(stderr, "[REFUS] argument inconnu : %s\n", argv[i]);
               return 2; }
    }
    if (n < 60) n = 60;             /* la commande : N >= 60 par classe */
    if (n > NMAX) n = NMAX;
    if (autotest) n = 60;

    printf("=== dudect_collab - LE MESUREUR DE LA QUESTION "
           "(edition COLLAB x86-64, v1.0.0) ===\n");
    printf("[config] arch=x86-64  compteur=TSC (la grandeur est « ticks »)"
           "  N=%zu/classe  seuil |t|>5\n", n);
    printf("[config] echantillons ENTRELACES (le protocole COLLAB-X86-1, "
           "pre-enregistre AVANT tout run)\n");
    if (autotest)
        printf("[ETIQUETTE] AUTOTEST LABORATOIRE - la mecanique seule : "
               "AUCUN statut terrain n'en decoule (le run Colab "
               "appartient au developpeur)\n");

    /* ---- la machine se nomme (D206 : la mutualisation, pas un defaut) ---- */
    int f_hyp = drapeau_cpuinfo("hypervisor");
    int f_ctsc = drapeau_cpuinfo("constant_tsc");
    int f_nstsc = drapeau_cpuinfo("nonstop_tsc");
    int f_shani = drapeau_cpuinfo("sha_ni");
    printf("[machine] drapeau hypervisor : %s — le silicium est %s : "
           "les voisins sont INCONNUS, le t mesurera AUSSI eux\n",
           f_hyp < 0 ? "ILLISIBLE (constate tel quel)" :
                       (f_hyp ? "present" : "ABSENT"),
           f_hyp == 1 ? "MUTUALISE" : "non virtualise (constate tel quel)");
    printf("[machine] drapeaux constant_tsc=%s nonstop_tsc=%s — le TSC est "
           "%s ; sa FREQUENCE n'est pas lue : aucun « cycle » ne sera "
           "fabrique, seul le contrepoint CLOCK_MONOTONIC vit au csv\n",
           f_ctsc == 1 ? "present" : "ABSENT/illisible",
           f_nstsc == 1 ? "present" : "ABSENT/illisible",
           (f_ctsc == 1 && f_nstsc == 1) ?
               "invariant (constate aux drapeaux)" :
               "d'invariance NON CONSTATEE (nomme, jamais muet)");
    printf("[machine] drapeau sha_ni : %s\n",
           f_shani < 0 ? "ILLISIBLE (constate tel quel)" :
                         (f_shani ? "PRESENT" : "ABSENT"));

    /* ---- les pieces citees (le coeur de l'honnetete) ---- */
    printf("[perimetre] les pieces scellees v0.15.0 face a ce kit :\n");
    for (size_t i = 0; i < sizeof PIECES_CITEES / sizeof *PIECES_CITEES; i++)
        printf("[perimetre]   %s\n", PIECES_CITEES[i]);

    /* ---- l'epreuve FIPS 180-4 « abc » — les TROIS lecteurs ---- */
    static const char ABC_ATTENDU[] =
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";
    unsigned char condense[32]; char hex[65];
    sha256((const unsigned char *)"abc", 3, condense);
    hexa(condense, 32, hex);
    printf("[fips] sha256-logiciel(abc) = %s — %s\n", hex,
           strcmp(hex, ABC_ATTENDU) == 0 ? "EXACT" : "DIVERGENT");
    if (strcmp(hex, ABC_ATTENDU) != 0) {
        fprintf(stderr, "[REFUS] le lecteur LOGICIEL est faux - RIEN ne "
                "sera mesure (fail-closed)\n");
        return 2;
    }
#if SHANI_COMPILABLE
    if (f_shani == 1) {
        sha256_shani((const unsigned char *)"abc", 3, condense);
        hexa(condense, 32, hex);
        printf("[fips] sha256-x86-shani(abc) = %s — %s\n", hex,
               strcmp(hex, ABC_ATTENDU) == 0 ? "EXACT" : "DIVERGENT");
        if (strcmp(hex, ABC_ATTENDU) != 0) {
            fprintf(stderr, "[REFUS] le lecteur MATERIEL SHA-NI est faux - "
                    "RIEN ne sera mesure (fail-closed)\n");
            return 2;
        }
    } else {
        printf("[fips] sha256-x86-shani : PASSE (le noyau n'expose pas "
               "« sha_ni » — REFUS NOMME, la cible sera passee)\n");
    }
#else
    printf("[fips] sha256-x86-shani : PASSE (compilation SANS -msha — la "
           "cible est REFUSEE PAR NATURE, nommee)\n");
#endif

    /* ---- l'image scellee : chargee, recoupee, mappee ---- */
    char sha_image[65] = "";
    size_t taille_image = 0;
    cible_t scellees[8];
    int nb = lire_manifeste("cibles", sha_image, &taille_image, scellees, 8);
    if (nb <= 0 || !sha_image[0] || !taille_image) {
        fprintf(stderr, "[REFUS] manifeste incomprehensible - copiez le "
                "dossier kit-C-collab-dudect/ ENTIER (D99)\n");
        return 2;
    }
    printf("[manifeste] image %ld octets, %d cible(s) scellee(s)\n",
           (long)taille_image, nb);
    FILE *f = fopen("cibles/proxy-image.bin", "rb");
    if (!f) { perror("cibles/proxy-image.bin"); return 2; }
    unsigned char *brut = (unsigned char *)malloc(taille_image);
    if (fread(brut, 1, taille_image, f) != taille_image) {
        fprintf(stderr, "[REFUS] image tronquee\n"); return 2;
    }
    fclose(f);
    unsigned char calcule[32];
    sha256(brut, taille_image, calcule);
    unsigned char attendu[32]; hex_vers(sha_image, attendu, 32);
    if (memcmp(calcule, attendu, 32) != 0) {
        fprintf(stderr, "[REFUS] sha256 de l'IMAGE divergent - ce n'est "
                "PAS la piece scellee, RIEN n'est execute\n");
        return 2;
    }
    printf("[image] sha256 recoupe - la piece scellee\n");

    /* la carte : l'indice a la base reelle 0x140000000 (la meme que le
     * binaire d'origine — un INDICE pour le noyau, jamais une exigence :
     * l'adresse effective est NOMMEE, et l'epreuve FIPS + la mutation K
     * prouvent que la piece executee est la piece recoupee OU QU'ELLE
     * VIVE) */
    size_t garde = (taille_image + 4095) & ~4095UL;
    void *image = mmap((void *)0x140000000UL, garde,
                       PROT_READ|PROT_WRITE|PROT_EXEC,
                       MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    int indice_tenu = (image == (void *)0x140000000UL);
    if (image == MAP_FAILED) {
        image = mmap(NULL, garde, PROT_READ|PROT_WRITE|PROT_EXEC,
                     MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    }
    if (image == MAP_FAILED) {
        fprintf(stderr, "[REFUS] mmap de l'image\n"); return 2;
    }
    memcpy(image, brut, taille_image);
    free(brut);
    printf("[image] mapee a %p (%s)\n", image,
           indice_tenu ? "l'indice 0x140000000 tenu" :
                         "l'indice 0x140000000 REFUSE — adresse libre du "
                         "noyau, nommee");

    /* le recoup PAR CIBLE : la plage de l'image mapee */
    int vecues_scellees = 0;
    for (int k = 0; k < nb; k++) {
        if (scellees[k].famille < 0) continue;
        sha256((unsigned char *)image + scellees[k].rva,
               scellees[k].taille, calcule);
        if (memcmp(calcule, scellees[k].sha_plage, 32) != 0) {
            fprintf(stderr, "[REFUS] %s : sha256 de la PLAGE divergent - "
                    "RIEN n'est execute\n", scellees[k].nom);
            return 2;
        }
        printf("[%s] plage recoupee (RVA %zu, %zu o) - la piece scellee\n",
               scellees[k].nom, scellees[k].rva, scellees[k].taille);
        vecues_scellees++;
    }
    if (vecues_scellees != 4) {
        fprintf(stderr, "[REFUS] le manifeste ne porte pas les QUATRE "
                "familles attendues (%d) - copiez le dossier ENTIER\n",
                vecues_scellees);
        return 2;
    }

    /* ---- l'epreuve FIPS DEPUIS LA PIECE SCELLEE (le geste test_appel) ---- */
    void *fn_tls02 = (char *)image + scellees[0].rva;
    condense_abc_scellee(fn_tls02, condense);
    hexa(condense, 32, hex);
    printf("[fips] tls13-02 SCELLEE (abc) = %s — %s\n", hex,
           strcmp(hex, ABC_ATTENDU) == 0 ?
           "EXACT (la piece scellee est le lecteur)" : "DIVERGENT");
    if (strcmp(hex, ABC_ATTENDU) != 0) {
        fprintf(stderr, "[REFUS] le lecteur SCELLE est faux - RIEN ne "
                "sera mesure (fail-closed)\n");
        return 2;
    }
    /* l'adversaire : un octet de la table K mute (EN MEMOIRE SEULEMENT —
     * la carte est MAP_PRIVATE, le FICHIER sur disque n'est JAMAIS
     * touche) -> le condense DOIT diverger -> la restauration rend
     * l'exact : la preuve que l'image executee EST celle recoupee */
    {
        unsigned char *k = (unsigned char *)image + 0x2F00;  /* .rdata K[64] */
        unsigned char sauve = k[0];
        k[0] ^= 0x01;
        condense_abc_scellee(fn_tls02, condense);
        hexa(condense, 32, hex);
        int diverge = strcmp(hex, ABC_ATTENDU) != 0;
        printf("[mutation K] condense %s — la table est BIEN lue par la "
               "piece (en memoire seule : le fichier sur disque est "
               "intouchable)\n", diverge ? "DIVERGE" : "INCANGE (refus)");
        k[0] = sauve;
        condense_abc_scellee(fn_tls02, condense);
        hexa(condense, 32, hex);
        int restaure = strcmp(hex, ABC_ATTENDU) == 0;
        printf("[restauration] %s\n", restaure ? "EXACT" : "refus");
        if (!diverge || !restaure) {
            fprintf(stderr, "[REFUS] l'adversaire de mutation K echoue - "
                    "l'image executee n'est pas la piece recoupee\n");
            return 2;
        }
    }
    if (fips_seul) {
        printf("[fips] l'epreuve est vecue seule (l'option --fips) - "
               "code 0\n");
        return 0;
    }

    /* ---- l'affinite (au mieux - un refus est consigne, jamais muet) ---- */
    printf("[affinite] coeur 0 : %s\n", poser_affinite(0) ? "posee" :
           "REFUSEE (le t sera bruite - consignez-le)");

    /* ---- le journal csv (l'horodatage a la nanoseconde) ---- */
    struct timespec maintenant;
    clock_gettime(CLOCK_REALTIME, &maintenant);
    char nom_csv[256];
    snprintf(nom_csv, sizeof nom_csv, "journal-dudect-collab-%ld%09ld.csv",
             (long)maintenant.tv_sec, (long)maintenant.tv_nsec);
    FILE *csv = fopen(nom_csv, "w");
    if (!csv) { perror("fopen"); return 2; }
    fprintf(csv, "cible,classe,iteration,ticks,secondes\n");

    /* ---- les huit cibles (l'ordre pre-enregistre) ---- */
    struct { const char *nom; int t; int lot; int egalite;
             const char *ca; const char *cb; void *fn; } cibles[] = {
        {"eq-constant",      T_EQ_CT,  512, 1, "egal",      "divergent", NULL},
        {"eq-branchue",      T_EQ_BR,  512, 1, "egal",      "divergent", NULL},
        {"sha256-logiciel",  T_SHA_SW,  64, 0, "fixe",      "aleatoire", NULL},
#if SHANI_COMPILABLE
        {"sha256-x86-shani", T_SHA_HW,  64, 0, "fixe",      "aleatoire", NULL},
#endif
        {"tls13-02",         T_TLS02,   64, 0, "fixe",      "aleatoire", NULL},
        {"tls13-13",         T_TLS13,    1, 0, "fixe",      "aleatoire", NULL},
        {"tls13-16",         T_TLS16,  512, 0, "fixe",      "aleatoire", NULL},
        {"tls13-17",         T_TLS17,  512, 0, "fixe",      "aleatoire", NULL},
    };
    int nb_cibles = (int)(sizeof cibles / sizeof *cibles);
    /* les fonctions scellees, resolues au manifeste */
    for (int k = 0; k < nb_cibles; k++) {
        if (cibles[k].t == T_TLS02) cibles[k].fn = (char *)image + scellees[0].rva;
        if (cibles[k].t == T_TLS13) cibles[k].fn = (char *)image + scellees[1].rva;
        if (cibles[k].t == T_TLS16) cibles[k].fn = (char *)image + scellees[2].rva;
        if (cibles[k].t == T_TLS17) cibles[k].fn = (char *)image + scellees[3].rva;
    }

    unsigned char secret_fixe[256], secret[256], aux[256], sortie[64];
    alea(secret_fixe, sizeof secret_fixe);
    memcpy(secret, secret_fixe, sizeof secret);

    int vecues = 0, refus = 0, instrument_conteste = 0, positif_diverge = 0;
    double med_log = -1.0, med_mat = -1.0, med_tls02 = -1.0;

    for (int k = 0; k < nb_cibles; k++) {
        if (cibles[k].t == T_SHA_HW && f_shani != 1) {
            printf("[%s] REFUS NOMME : le noyau n'expose pas « sha_ni » - "
                   "la cible est PASSEE, le reste du run vit\n",
                   cibles[k].nom);
            refus++;
            continue;
        }
        printf("[%s] echauffement 100 paires, puis %zu iterations entrelacees "
               "(LOT=%d appels par echantillon)\n", cibles[k].nom, n,
               cibles[k].lot);
        alea(aux, sizeof aux);   /* l'auxiliaire fixe de la cible (le geste
                                  * du kit-2 : seul LE secret varie) */

        int lot = cibles[k].lot;
        /* l'echauffement : 100 paires, resultats jetes */
        for (int j = 0; j < 100; j++) {
            if (cibles[k].egalite) memcpy(secret, aux, 256);
            else memcpy(secret, secret_fixe, 256);
            for (int l = 0; l < lot; l++)
                appeler(cibles[k].t, cibles[k].fn, secret, aux, sortie);
            alea(secret, sizeof secret);
            for (int l = 0; l < lot; l++)
                appeler(cibles[k].t, cibles[k].fn, secret, aux, sortie);
        }

        serie_t un, deux;
        un.n = deux.n = 0;
        for (size_t i = 0; i < n; i++) {
            /* la premiere classe (egal / secret-fixe) — le secret RESTAURE
             * a CHAQUE iteration (l'egal se recopie, sinon la classe un
             * mesurerait le reste aleatoire de l'iteration amont) */
            if (cibles[k].egalite) memcpy(secret, aux, 256);
            else memcpy(secret, secret_fixe, 256);
            double t0s = horloge_sec(); uint64_t t0 = lecteur_tsc();
            for (int l = 0; l < lot; l++)
                appeler(cibles[k].t, cibles[k].fn, secret, aux, sortie);
            uint64_t t1 = lecteur_tsc(); double t1s = horloge_sec();
            un.cyc[un.n] = t1 - t0; un.sec[un.n] = t1s - t0s; un.n++;
            fprintf(csv, "%s,%s,%zu,%llu,%.9f\n", cibles[k].nom, cibles[k].ca,
                    i, (unsigned long long)(t1 - t0), t1s - t0s);
            /* la seconde classe (divergent / secret-aleatoire — le secret
             * regenere HORS mesure) */
            alea(secret, sizeof secret);
            t0s = horloge_sec(); t0 = lecteur_tsc();
            for (int l = 0; l < lot; l++)
                appeler(cibles[k].t, cibles[k].fn, secret, aux, sortie);
            t1 = lecteur_tsc(); t1s = horloge_sec();
            deux.cyc[deux.n] = t1 - t0; deux.sec[deux.n] = t1s - t0s;
            deux.n++;
            fprintf(csv, "%s,%s,%zu,%llu,%.9f\n", cibles[k].nom, cibles[k].cb,
                    i, (unsigned long long)(t1 - t0), t1s - t0s);
        }
        double tw = t_welch(&un, &deux);
        uint64_t *fc = malloc(un.n * sizeof(uint64_t));
        uint64_t *ac = malloc(deux.n * sizeof(uint64_t));
        if (!fc || !ac) { fprintf(stderr, "[REFUS] memoire\n"); return 2; }
        memcpy(fc, un.cyc, un.n * sizeof(uint64_t));
        memcpy(ac, deux.cyc, deux.n * sizeof(uint64_t));
        uint64_t mun = mediane(fc, un.n);
        uint64_t mdeux = mediane(ac, deux.n);
        free(fc); free(ac);
        int diverge = fabs(tw) > 5.0;
        printf("  %-10s : moy %.1f ticks, med %llu (par appel : %.2f)\n",
               cibles[k].ca, moy(un.cyc, un.n),
               (unsigned long long)mun, (double)mun / lot);
        printf("  %-10s : moy %.1f ticks, med %llu (par appel : %.2f)\n",
               cibles[k].cb, moy(deux.cyc, deux.n),
               (unsigned long long)mdeux, (double)mdeux / lot);
        printf("  t de Welch = %.2f -> %s (seuil |t| > 5)\n", tw,
               diverge ? "DIVERGENCE TEMPORELLE (a consigner telle quelle)"
                       : "AUCUNE divergence au seuil");
        if (cibles[k].t == T_EQ_CT && diverge) {
            printf("  ATTENDU : aucune divergence — la divergence d'un "
                   "patron constant est un RESULTAT (D189 : consigner "
                   "tel quel)\n");
            positif_diverge = 1;
        }
        if (cibles[k].t == T_EQ_BR && !diverge) {
            printf("  ATTENDU : divergence — L'INSTRUMENT EST CONTESTE sur "
                   "cet echantillon (nomme, jamais muet : le temoin le "
                   "dit, le labo recoupera avec vous)\n");
            instrument_conteste = 1;
        }
        if (cibles[k].t == T_SHA_SW) med_log = (double)mun / lot;
        if (cibles[k].t == T_SHA_HW) med_mat = (double)mun / lot;
        if (cibles[k].t == T_TLS02) med_tls02 = (double)mun / lot;
        vecues++;
    }
    fclose(csv);
    printf("[sortie] %s — joignez-le au temoin (la synthese le fait)\n",
           nom_csv);
    if (med_log > 0 && med_mat > 0)
        printf("[constat] le rapport median logiciel/SHA-NI = %.2f — LE "
               "CONSTAT DE CE SILICIUM (jamais une cible : aucune cible "
               "pre-enregistree n'existe pour ce silicium)\n",
               med_log / med_mat);
    if (med_tls02 > 0)
        printf("[constat] tls13-02 SCELLEE : %.2f ticks par appel — la "
               "piece du coffre, mesuree sur CE silicium (le labo la "
               "relira contre le kit-2 du 24/11)\n", med_tls02);

    /* ---- le verdict ---- */
    printf("[verdict] LE RUN VECU : %d/%d cible(s) consignee(s), %d refus "
           "nomme(s)", vecues, nb_cibles, refus);
    if (instrument_conteste) printf(" — INSTRUMENT CONTESTE (nomme)");
    if (positif_diverge)     printf(" — controle positif DIVERGENT (resultat)");
    printf("\n");
    printf("[la question] les trois divergences |t|>5 du 24/11 au portable "
           "(tls13-02 : -10,64 ; tls13-13 : +9,65 ; tls13-16 : +9,19 — "
           "l'Entree 416 les lut comme DVFS aux classes SEQUENTIELLES) : "
           "CE run, sur CE silicium, classes ENTRELACEES, dit ce qu'il "
           "dit. La lecture appartient au labo, sur pieces — jamais "
           "avant le run, jamais sans pieces\n");
    printf("[verdict] la lecture honnete : |t| > 5 = dependance AU SEUIL "
           "sur CET echantillon, CETTE machine mutualisee, consignee "
           "telle quelle ; |t| <= 5 = aucune divergence au seuil sur cet "
           "echantillon — jamais « temps constant prouve »\n");
    printf("[verdict] code de sortie : 0 (le run vecu, vert ou ecarts "
           "nommes)\n");
    return 0;
}
