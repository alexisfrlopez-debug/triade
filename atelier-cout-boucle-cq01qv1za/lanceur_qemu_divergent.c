/* lanceur_qemu.c — LE MOTEUR DE VOLUME (le plan § 3.1 de cq01qv1za, gelé).
 *
 * Un ELF64 STATIQUE, lié haut (0x10000000) pour ne rien toucher aux zones
 * du plan : il exécute les blocs scellés du domaine loupe à leur plan
 * d'adressage — le MÊME bytecode, le MÊME ABI msx64, une autre mécanique.
 *
 * Le lanceur ne connaît AUCUN bloc, AUCUNE adresse du domaine : tout vit
 * au fichier d'environnement (les zones, les images, l'IAT, les sentinelles,
 * les témoins, le programme d'opérations). Il exécute, il ne juge JAMAIS —
 * le juge demeure Python (hashlib), le moteur rend ses relevés.
 *
 * LES SHIMS : les SIX feuilles kernel32 du noyau loupe en fonctions
 * __attribute__((ms_abi))) — la sémantique OCTET POUR OCTET du
 * harnais_noyau.OSVirtuel (les poignées depuis 0x1000 au pas 8, les gle
 * nommés, le Nième ReadFile en échec armable, le compte des feuilles).
 *
 * L'APPELANT FACTICE : les sentinelles non volatiles posées, la pile à
 * ENTREE_RSP, le retour magique à [rsp], l'ombre de l'appelant en canari —
 * le bloc atterrit au LANDING (posé à ret_magique) qui capture les
 * registres et rend la main au pilote.
 *
 * Compilation : gcc -O2 -static -Wl,-Ttext-segment=0x10000000 \
 *               -o lanceur_qemu lanceur_qemu.c
 * Exécution   : qemu-x86_64 lanceur_qemu environnement.txt   (le volume)
 *               ./lanceur_qemu environnement.txt             (le natif)
 */
#define _GNU_SOURCE
#include <fcntl.h>
#include <setjmp.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

/* ---- les shims ms_abi : la sémantique du harnais_noyau, à l'octet ---------- */

#define MAX_FICHIERS 16
#define MAX_POIGNEES 16
#define MAX_NOM 64
#define MAX_GLE 64

struct fichier {
    char nom[MAX_NOM];
    uint8_t *contenu;      /* NULL : la taille déclarée sans contenu */
    uint64_t taille;
    int verrouille, refus_acces;
};

struct poignee {
    uint64_t h;
    int fichier;           /* -1 : libre */
    uint64_t pos;
};

static struct fichier fichiers[MAX_FICHIERS];
static int n_fichiers = 0;
static struct poignee poignees[MAX_POIGNEES];
static int n_poignees = 0;
static uint64_t prochaine_poignee = 0x1000;
static uint64_t gle = 0;
static int echec_armedans = -1;      /* -1 : désarmé */
static int echec_compteur = 0;
static int echec_close = 0;
static uint64_t compteurs[6];        /* CreateFileW..GetLastError */
static struct { const char *feuille; uint64_t gle; } journal_gle[MAX_GLE];
static int n_journal_gle = 0;

static const char *NOMS_FEUILLES[6] = {
    "CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
    "ReadFile", "CloseHandle", "GetLastError"};

static void erreur(uint64_t code) { gle = code; }

static int chercher_fichier(const char *nom) {
    for (int i = 0; i < n_fichiers; i++)
        if (strcmp(fichiers[i].nom, nom) == 0) return i;
    return -1;
}

static struct poignee *chercher_poignee(uint64_t h) {
    for (int i = 0; i < n_poignees; i++)
        if (poignees[i].h == h && poignees[i].fichier >= 0) return &poignees[i];
    return NULL;
}

/* CreateFileW(rcx=LPCWSTR, rdx=access, r8=share, r9=security,
 *             [rsp+0x28]=disposition, [rsp+0x30]=flags, [rsp+0x38]=template)
 * — la convention msx64 : le 5e argument vit à [rsp+0x28] AU SHIM (le call
 * a poussé le retour) ; la fonction ms_abi de gcc lit ses paramètres pile
 * exactement là. */
__attribute__((ms_abi))
static uint64_t shim_CreateFileW(const uint16_t *chemin_w, uint32_t a1,
                                 uint32_t a2, uint32_t a3,
                                 uint32_t disposition, uint32_t flags,
                                 uint64_t modele) {
    (void)a1; (void)a2; (void)a3; (void)flags; (void)modele;
    if (disposition != 3) {              /* OUVRIR_EXISTANT seul */
        erreur(87);
        return 0xFFFFFFFFFFFFFFFFull;
    }
    /* le chemin UTF-16 → UTF-8 (les noms du bac : ASCII) */
    char chemin[MAX_NOM];
    int n = 0;
    while (chemin_w[n] != 0 && n < MAX_NOM - 1) { chemin[n] = (char)chemin_w[n]; n++; }
    chemin[n] = 0;
    compteurs[0]++;
    int f = chercher_fichier(chemin);
    if (f < 0) { erreur(2); return 0xFFFFFFFFFFFFFFFFull; }   /* FILE_NOT_FOUND */
    if (fichiers[f].verrouille) { erreur(32); return 0xFFFFFFFFFFFFFFFFull; }
    if (fichiers[f].refus_acces) { erreur(5); return 0xFFFFFFFFFFFFFFFFull; }
    uint64_t h = prochaine_poignee;
    prochaine_poignee += 8;
    if (n_poignees < MAX_POIGNEES) {
        poignees[n_poignees].h = h;
        poignees[n_poignees].fichier = f;
        poignees[n_poignees].pos = 0;
        n_poignees++;
    }
    gle = 0;
    return h;
}

__attribute__((ms_abi))
static uint32_t shim_GetFileSizeEx(uint64_t h, uint64_t *sortie) {
    compteurs[1]++;
    struct poignee *p = chercher_poignee(h);
    if (p == NULL) { erreur(6); return 0; }
    *sortie = fichiers[p->fichier].taille;
    return 1;
}

__attribute__((ms_abi))
static uint32_t shim_SetFilePointerEx(uint64_t h, uint64_t distance,
                                      uint64_t *nouvelle, uint32_t methode) {
    compteurs[2]++;
    struct poignee *p = chercher_poignee(h);
    if (p == NULL || methode != 0) { erreur(6); return 0; }  /* FILE_BEGIN seul */
    p->pos = distance;
    if (nouvelle) *nouvelle = distance;
    return 1;
}

__attribute__((ms_abi))
static uint32_t shim_ReadFile(uint64_t h, uint8_t *tampon, uint32_t n,
                              uint64_t *lus, uint64_t *superpose) {
    if (superpose != NULL) { erreur(87); return 0; }   /* le handle synchrone
                                                          EXIGE le NUL au slot */
    compteurs[3]++;
    if (echec_armedans > 0) {
        echec_compteur++;
        if (echec_compteur == echec_armedans) {
            erreur(1117);                                /* ERROR_IO_DEVICE */
            return 0;
        }
    }
    struct poignee *p = chercher_poignee(h);
    if (p == NULL) { erreur(6); return 0; }
    struct fichier *f = &fichiers[p->fichier];
    uint64_t pos = p->pos;
    uint64_t rendus;
    if (f->contenu == NULL || pos >= f->taille) {
        memset(tampon, 0, n);                       /* la taille sans contenu */
        rendus = n;
    } else {
        uint64_t fin = pos + n < f->taille ? pos + n : f->taille;
        rendus = fin - pos;                         /* la découpe PLEINE —
                                                       jamais zéro-rembourrée
                                                       au-delà de la taille */
        if (rendus > 0) { memcpy(tampon, f->contenu + pos, rendus); tampon[0] = (uint8_t)(tampon[0] ^ 0x01); }   /* LE MOTEUR FAUX : un octet du tampon inversé — la porte doit l attraper */
    }
    p->pos = pos + n;
    gle = 0;
    if (rendus > 0 && lus) *lus = rendus; else if (lus) *lus = 0;
    return 1;
}

__attribute__((ms_abi))
static uint32_t shim_CloseHandle(uint64_t h) {
    compteurs[4]++;
    if (echec_close) { erreur(6); return 0; }
    struct poignee *p = chercher_poignee(h);
    if (p) p->fichier = -1;
    gle = 0;
    return 1;
}

__attribute__((ms_abi))
static uint64_t shim_GetLastError(void) {
    compteurs[5]++;
    if (n_journal_gle < MAX_GLE) {
        journal_gle[n_journal_gle].feuille = "GetLastError";
        journal_gle[n_journal_gle].gle = gle;
        n_journal_gle++;
    }
    return gle;
}

/* le mort : les 28 feuilles hors noyau — l'appel DÉNONCÉ, le retour factice */
static uint64_t appels_interdits = 0;
__attribute__((ms_abi))
static uint64_t shim_mort(uint64_t a, uint64_t b, uint64_t c, uint64_t d) {
    (void)a; (void)b; (void)c; (void)d;
    appels_interdits++;
    return 0;
}

static void *ADRESSES_SHIMS[7];   /* 0..5 les feuilles, 6 le mort */

/* ---- l'appelant factice (le miroir exact de Emulation.appeler) ------------- */

static uint64_t SENT_RBX, SENT_RBP, SENT_RDI, SENT_RSI;
static uint64_t SENT_R12, SENT_R13, SENT_R14, SENT_R15;
static uint64_t ENTREE_RSP, RET_MAGIQUE;
static uint8_t CANARI = 0xA5;

sigjmp_buf jb_retour;                      /* lien externe : l'asm basique
                                              de l'atterrissage naked la
                                              référence par son nom */
volatile sig_atomic_t en_execution = 0;
uint64_t g_rax, g_rsp, g_rbx, g_rbp, g_rdi, g_rsi;
uint64_t g_r12, g_r13, g_r14, g_r15;
volatile sig_atomic_t g_crash = 0;
uint64_t g_rip_crash = 0, g_addr_crash = 0;

/* le landing : le bloc y revient par son ret — registres capturés AU POINT
 * EXACT DU RET (fonction NAKED : aucun prologue ne touche rsp avant la
 * capture — la faute de la mouture comptable : le prologue O0 poussait rbp
 * avant la lecture, le rsp lu ne fut jamais celui du ret), puis la main
 * rendue au pilote par siglongjmp (la pile factice n'est PAS la pile C) */
__attribute__((naked))
static void atterrissage(void) {
    __asm__ volatile(
        "movq %rsp, g_rsp(%rip)\n\t"
        "movq %rbx, g_rbx(%rip)\n\t"
        "movq %rbp, g_rbp(%rip)\n\t"
        "movq %rdi, g_rdi(%rip)\n\t"
        "movq %rsi, g_rsi(%rip)\n\t"
        "movq %r12, g_r12(%rip)\n\t"
        "movq %r13, g_r13(%rip)\n\t"
        "movq %r14, g_r14(%rip)\n\t"
        "movq %r15, g_r15(%rip)\n\t"
        "movq %rax, g_rax(%rip)\n\t"
        "leaq jb_retour(%rip), %rdi\n\t"
        "movl $1, %esi\n\t"
        "call siglongjmp\n\t"
        "ud2\n\t");
}

static void gestionnaire_signal(int sig, siginfo_t *si, void *ucon) {
    if (en_execution) {
        g_crash = sig;
        g_rip_crash = ((ucontext_t *)ucon)->uc_mcontext.gregs[REG_RIP];
        g_addr_crash = (uint64_t)si->si_addr;
        fprintf(stderr, "[crash] sig=%d rip=%#llx addr=%#llx rsp=%#llx\n",
                sig, (unsigned long long)g_rip_crash,
                (unsigned long long)g_addr_crash,
                (unsigned long long)((ucontext_t *)ucon)->uc_mcontext.gregs[REG_RSP]);
        siglongjmp(jb_retour, 2);
    }
    _exit(3);
}

static int pile_equilibree(void) { return g_rsp == ENTREE_RSP + 8; }
static int non_volatiles_rendus(void) {
    return g_rbx == SENT_RBX && g_rbp == SENT_RBP && g_rdi == SENT_RDI
        && g_rsi == SENT_RSI && g_r12 == SENT_R12 && g_r13 == SENT_R13
        && g_r14 == SENT_R14 && g_r15 == SENT_R15;
}
static int canaris_haut(void) {
    const uint8_t *p = (const uint8_t *)(ENTREE_RSP + 8);
    for (size_t i = 0; i < 0x170; i++) if (p[i] != CANARI) return 0;
    return 1;
}
static int etat_propre(void) {
    return g_crash == 0 && pile_equilibree() && canaris_haut()
        && non_volatiles_rendus();
}
/* LE VERDICT VIT DANS EAX (la table des SEPT verdicts — le 32 bits SIGNÉ) */
static int64_t verdict_eax(uint64_t rax64) {
    uint32_t eax = (uint32_t)(rax64 & 0xFFFFFFFFu);
    return eax >= 0x80000000u ? (int64_t)eax - (1LL << 32) : (int64_t)eax;
}

/* UN appel : les sentinelles posées, la pile factice armée, le bloc sauté ;
 * le retour (ou le crash) rend la main au pilote.
 * LA TRANSITION EST BULLETPROOF : le contexte vit en MÉMOIRE, lu par
 * l'asm au fil des mov — aucun opérande d'entrée ne peut être alloué à un
 * registre que la séquence écrase (la fausse de la première mouture : le
 * compilateur plaçait ENTREE_RSP ou va dans rbx/rbp, écrasés AVANT leur
 * lecture — le saut partait dans le vide, rax restait à zéro, la pile
 * jamais équilibrée). Le pointeur du contexte est ÉPINGLÉ à r11 — jamais
 * écrit par la séquence. */
struct ctx_appel {
    uint64_t rbx, rbp, rdi, rsi, r12, r13, r14, r15;
    uint64_t rsp, rcx, va;
};

static void appeler_bloc(uint64_t va, uint64_t rcx_val) {
    uint64_t *pile = (uint64_t *)ENTREE_RSP;
    pile[0] = RET_MAGIQUE;
    memset((void *)(ENTREE_RSP + 8), CANARI, 0x170);
    g_crash = 0;
    struct ctx_appel ctx = {
        SENT_RBX, SENT_RBP, SENT_RDI, SENT_RSI,
        SENT_R12, SENT_R13, SENT_R14, SENT_R15,
        ENTREE_RSP, rcx_val, va};
    register const struct ctx_appel *pr __asm__("r11");
    if (sigsetjmp(jb_retour, 1) == 0) {
        pr = &ctx;      /* IMMÉDIATEMENT avant l'asm : r11 est VOLATILE au
                           fil des appels — le sigsetjmp l'eût détruit (la
                           faute vue en pièces : r11 = 0x246 au premier mov) */
        en_execution = 1;
        __asm__ volatile (
            "movq 0(%[p]), %%rbx\n\t"
            "movq 8(%[p]), %%rbp\n\t"
            "movq 16(%[p]), %%rdi\n\t"
            "movq 24(%[p]), %%rsi\n\t"
            "movq 32(%[p]), %%r12\n\t"
            "movq 40(%[p]), %%r13\n\t"
            "movq 48(%[p]), %%r14\n\t"
            "movq 56(%[p]), %%r15\n\t"
            "movq 64(%[p]), %%rsp\n\t"
            "movq 72(%[p]), %%rcx\n\t"
            "xorl %%eax, %%eax\n\t"
            "jmpq *80(%[p])\n\t"
            :
            : [p] "r"(pr)
            : "memory");
        __builtin_unreachable();   /* le bloc retourne au landing qui
                                      siglongjmp — la suite n'existe pas */
    }
    en_execution = 0;
}

/* ---- le domaine par l'environnement (le lanceur ne sait rien) -------------- */

static uint64_t ADRESSE_CHEMIN = 0;
static uint64_t R_CADRE = 0, R_EMPREINTES = 0;

static uint64_t hexa(const char *s) { return strtoull(s, NULL, 16); }

static void poser_zone(uint64_t addr, uint64_t taille) {
    /* RWX — le miroir du mem_map d'Unicorn (UC_PROT_ALL par défaut : les
     * zones du plan y sont lisibles/écrivables/exécutables ; le lanceur
     * mappe l'identique — la page du bloc DOIT être exécutable) */
    void *p = mmap((void *)addr, taille,
                   PROT_READ | PROT_WRITE | PROT_EXEC,
                   MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) {
        fprintf(stderr, "lanceur: mmap %#llx (%llu) ÉCHEC\n",
                (unsigned long long)addr, (unsigned long long)taille);
        _exit(4);
    }
}

static uint64_t lire_u64_mem(uint64_t addr) { return *(uint64_t *)addr; }
static uint32_t lire_u32_mem(uint64_t addr) { return *(uint32_t *)addr; }

static void ligne_hex(FILE *out, const char *champ, uint64_t addr, int n) {
    fprintf(out, "\"%s\":\"", champ);
    for (int i = 0; i < n; i++) fprintf(out, "%02x", ((uint8_t *)addr)[i]);
    fprintf(out, "\"");
}

/* l'impression du relevé d'ouverture/lecture — le format EXACT partagé avec
 * le moteur Unicorn (le traducteur Python sérialise l'identique) ; pos =
 * la position du fichier à la poignée du cadre (le relevé du mémo la porte) */
static uint64_t pos_de_poignee_cadre(void) {
    uint64_t h = lire_u64_mem(R_CADRE + 528);
    struct poignee *p = chercher_poignee(h);
    return p ? p->pos : 0xFFFFFFFFFFFFFFFFull;
}

static void imprimer_releve(FILE *out, const char *op, const char *detail,
                            int64_t rax) {
    fprintf(out, "{\"op\":\"%s\",\"detail\":\"%s\",\"rax\":%lld,\"propre\":%d,"
                 "\"poignee\":%llu,\"taille\":%llu,\"vue\":%llu,\"curseur\":%llu,"
                 "\"remplissage\":%u,\"pos\":%llu,",
            op, detail, (long long)rax, etat_propre(),
            (unsigned long long)lire_u64_mem(R_CADRE + 528),
            (unsigned long long)lire_u64_mem(R_CADRE + 520),
            (unsigned long long)lire_u64_mem(R_CADRE + 536),
            (unsigned long long)lire_u64_mem(R_CADRE + 544),
            (unsigned)lire_u32_mem(R_CADRE + 552),
            (unsigned long long)pos_de_poignee_cadre());
    ligne_hex(out, "tampon", R_CADRE + 568, 384);
    fputc(',', out);
    ligne_hex(out, "panneau", R_EMPREINTES, 48);
    fprintf(out, ",\"crash\":\"%s\"}\n",
            g_crash ? (g_crash == 11 ? "SIGSEGV" : "SIG") : "");
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: lanceur_qemu <environnement.txt>\n");
        return 64;
    }
    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_sigaction = gestionnaire_signal;
    sa.sa_flags = SA_SIGINFO;
    sigaction(SIGSEGV, &sa, NULL);
    sigaction(SIGBUS, &sa, NULL);
    sigaction(SIGFPE, &sa, NULL);

    ADRESSES_SHIMS[0] = (void *)(uintptr_t)&shim_CreateFileW;
    ADRESSES_SHIMS[1] = (void *)(uintptr_t)&shim_GetFileSizeEx;
    ADRESSES_SHIMS[2] = (void *)(uintptr_t)&shim_SetFilePointerEx;
    ADRESSES_SHIMS[3] = (void *)(uintptr_t)&shim_ReadFile;
    ADRESSES_SHIMS[4] = (void *)(uintptr_t)&shim_CloseHandle;
    ADRESSES_SHIMS[5] = (void *)(uintptr_t)&shim_GetLastError;
    ADRESSES_SHIMS[6] = (void *)(uintptr_t)&shim_mort;

    FILE *env = fopen(argv[1], "r");
    if (!env) { perror("environnement"); return 65; }
    char ligne[512];
    FILE *out = stdout;

    while (fgets(ligne, sizeof ligne, env)) {
        char c0[64], c1[160], c2[160], c3[64], c4[64], c5[260], c6[260], c7[64];
        if (ligne[0] == '#' || ligne[0] == '\n') continue;
        int n = sscanf(ligne, "%63s %159s %159s %63s %63s %259s %259s %63s",
                        c0, c1, c2, c3, c4, c5, c6, c7);
        if (n <= 0) continue;
        if (strcmp(c0, "zone") == 0 && n >= 3) {
            poser_zone(hexa(c1), hexa(c2));
        } else if (strcmp(c0, "image") == 0 && n >= 4) {
            uint64_t addr = hexa(c2), taille = hexa(c3);
            poser_zone(addr & ~0xFFFULL,
                       ((addr + taille + 0xFFF) & ~0xFFFULL) - (addr & ~0xFFFULL));
            FILE *f = fopen(c1, "rb");
            if (!f) { fprintf(stderr, "image %s illisible\n", c1); return 66; }
            if (fread((void *)addr, 1, taille, f) != taille) {
                fprintf(stderr, "image %s tronquée\n", c1); return 66;
            }
            fclose(f);
        } else if (strcmp(c0, "iat") == 0 && n >= 3) {
            int idx = atoi(c2);
            *(uint64_t *)hexa(c1) = (uint64_t)(uintptr_t)
                ADRESSES_SHIMS[idx < 7 ? idx : 6];
        } else if (strcmp(c0, "landing") == 0 && n >= 2) {
            /* movabs r10, atterrissage ; jmp r10 — 13 octets au retour
             * magique : l'atterrissage est NAKED, l'alignement est le sien */
            uint64_t adr = hexa(c1);
            uint8_t code[13];
            uint64_t cible = (uint64_t)(uintptr_t)atterrissage;
            code[0] = 0x49; code[1] = 0xBA;
            memcpy(code + 2, &cible, 8);
            code[10] = 0x41; code[11] = 0xFF; code[12] = 0xE2;
            memcpy((void *)adr, code, 13);
        } else if (strcmp(c0, "ret_magique") == 0 && n >= 2) {
            RET_MAGIQUE = hexa(c1);
        } else if (strcmp(c0, "entree_rsp") == 0 && n >= 2) {
            ENTREE_RSP = hexa(c1);
        } else if (strcmp(c0, "canari") == 0 && n >= 2) {
            CANARI = (uint8_t)hexa(c1);
        } else if (strcmp(c0, "sentinelle") == 0 && n >= 3) {
            uint64_t v = hexa(c2);
            if (!strcmp(c1, "rbx")) SENT_RBX = v;
            else if (!strcmp(c1, "rbp")) SENT_RBP = v;
            else if (!strcmp(c1, "rdi")) SENT_RDI = v;
            else if (!strcmp(c1, "rsi")) SENT_RSI = v;
            else if (!strcmp(c1, "r12")) SENT_R12 = v;
            else if (!strcmp(c1, "r13")) SENT_R13 = v;
            else if (!strcmp(c1, "r14")) SENT_R14 = v;
            else if (!strcmp(c1, "r15")) SENT_R15 = v;
        } else if (strcmp(c0, "adresse_chemin") == 0 && n >= 2) {
            ADRESSE_CHEMIN = hexa(c1);
        } else if (strcmp(c0, "cadre") == 0 && n >= 3) {
            R_CADRE = hexa(c1); R_EMPREINTES = hexa(c2);
        } else if (strcmp(c0, "temoin") == 0 && n >= 3) {
            FILE *f = fopen(c2, "rb");
            if (!f) { fprintf(stderr, "témoin %s illisible\n", c2); return 67; }
            fseek(f, 0, SEEK_END);
            long t = ftell(f);
            fseek(f, 0, SEEK_SET);
            if (n_fichiers >= MAX_FICHIERS) { fprintf(stderr, "trop de témoins\n"); return 68; }
            strncpy(fichiers[n_fichiers].nom, c1, MAX_NOM - 1);
            fichiers[n_fichiers].contenu = malloc(t ? t : 1);
            if (t && fread(fichiers[n_fichiers].contenu, 1, t, f) != (size_t)t) {
                fprintf(stderr, "témoin %s tronqué\n", c1); return 67;
            }
            fichiers[n_fichiers].taille = (uint64_t)t;
            fichiers[n_fichiers].verrouille = 0;
            fichiers[n_fichiers].refus_acces = 0;
            n_fichiers++;
            fclose(f);
        }
        /* les directives ci-dessus se consomment AVANT le premier op : le
         * fichier d'environnement porte la préparation PUIS le programme */
        else if (strcmp(c0, "op") == 0 && n >= 3) {
            if (strcmp(c1, "ouvrir") == 0 && n >= 4) {
                /* le chemin UTF-16-NUL posé à ADRESSE_CHEMIN, l'appel du bloc */
                const char *chemin = c2;
                uint16_t *w = (uint16_t *)ADRESSE_CHEMIN;
                size_t i = 0;
                for (; chemin[i] && i < 259; i++) w[i] = (uint16_t)(uint8_t)chemin[i];
                w[i] = 0;
                appeler_bloc(hexa(c3), ADRESSE_CHEMIN);
                imprimer_releve(out, "ouvrir", chemin, verdict_eax(g_rax));
            } else if (strcmp(c1, "lire") == 0 && n >= 4) {
                appeler_bloc(hexa(c3), hexa(c2));
                char detail[32];
                snprintf(detail, sizeof detail, "0x%llx",
                         (unsigned long long)hexa(c2));
                imprimer_releve(out, "lire", detail, verdict_eax(g_rax));
            } else if (strcmp(c1, "fermer") == 0 && n >= 3) {
                appeler_bloc(hexa(c2), 0);
                imprimer_releve(out, "fermer", "", verdict_eax(g_rax));
            } else if (strcmp(c1, "restaurer") == 0 && n >= 7) {
                /* 7 jetons : op restaurer <poignée> <pos> <chemin> <cadre>
                 * <panneau> — la mouture première exigeait 8 (un jeton
                 * fantôme) : l'op SAUTÉE en silence, la session jamais
                 * restaurée — la faute vue en pièces au décalage manquant */
                /* la reprise au relevé du mémo : le cadre et le panneau
                 * RELEVÉS posés à leurs adresses, la poignée rendue à l'OS
                 * virtuel — puis tout est vivant (le miroir de
                 * memo_sessions.reconstruire_session) */
                uint64_t poignee = hexa(c2), pos = hexa(c3);
                int fi = chercher_fichier(c4);
                if (fi < 0) { fprintf(stderr, "restaurer: temoin %s inconnu\n", c4); return 69; }
                FILE *fc = fopen(c5, "rb"), *fp = fopen(c6, "rb");
                if (!fc || !fp) { fprintf(stderr, "restaurer: relevés illisibles\n"); return 70; }
                if (fread((void *)R_CADRE, 1, 960, fc) != 960
                    || fread((void *)R_EMPREINTES, 1, 48, fp) != 48) {
                    fprintf(stderr, "restaurer: relevés tronqués\n"); return 70;
                }
                fclose(fc); fclose(fp);
                (void)c7;
                if (n_poignees < MAX_POIGNEES) {
                    poignees[n_poignees].h = poignee;
                    poignees[n_poignees].fichier = fi;
                    poignees[n_poignees].pos = pos;
                    n_poignees++;
                }
                fprintf(out, "{\"op\":\"restaurer\",\"poignee\":%llu,"
                             "\"pos\":%llu}\n",
                        (unsigned long long)poignee,
                        (unsigned long long)pos);
            } else if (strcmp(c1, "armer_echec") == 0 && n >= 3) {
                echec_armedans = atoi(c2);
                echec_compteur = 0;
                fprintf(out, "{\"op\":\"armer_echec\",\"dans\":%d}\n",
                        echec_armedans);
            } else if (strcmp(c1, "echec_close") == 0 && n >= 3) {
                echec_close = atoi(c2);
            }
        } else if (strcmp(c0, "etat") == 0) {
            fprintf(out, "{\"op\":\"etat\",\"compteurs\":[");
            for (int i = 0; i < 6; i++)
                fprintf(out, "%s%llu", i ? "," : "",
                        (unsigned long long)compteurs[i]);
            fprintf(out, "],\"gle\":%llu,\"journal_gle\":[",
                    (unsigned long long)gle);
            for (int i = 0; i < n_journal_gle; i++)
                fprintf(out, "%s[\"%s\",%llu]", i ? "," : "",
                        journal_gle[i].feuille,
                        (unsigned long long)journal_gle[i].gle);
            fprintf(out, "],\"interdits\":%llu}\n",
                    (unsigned long long)appels_interdits);
        } else if (strcmp(c0, "fin") == 0) {
            break;
        }
    }
    fclose(env);
    fflush(out);
    return 0;
}
