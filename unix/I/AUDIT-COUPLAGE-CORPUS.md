# AUDIT DE COUPLAGE DU CORPUS PARITAIRE — chantier M6-(b) (04/11/2026)

> Mandat : D149-(2) (le corpus nominal M6 RESTREINT et NOMMÉ) et D149-(3)
> (la voie du diff nul est la révision de granularité des contrats). L'audit
> classe chaque contrat candidat du patrimoine M0–M5 : **A** instanciable tel
> quel sur `x86-64-linux-elf64`, **B** révision de granularité R+1 (arguments
> nommés dans la couche I, paramétrage physique déplacé vers frag-con,
> spécification § 8.3-4), **C** couplé à l'OS (l'intention même du contrat
> appartient à l'interface Windows — instanciation hors corpus, frontière
> D149). L'audit est un LIVRABLE DU CHANTIER, écrite-avant-code.

## 1. La méthode

Chaque contrat candidat est lu ligne à ligne ; tout couplage est NOMMÉ par
espèce : (i) **registres physiques** msx64 dans les pré-conditions (rcx/rdx/r8,
l'ordre des arguments, la volatilité) ; (ii) **services OS** (WriteFile,
ExitProcess, VirtualProtect, EnterCriticalSection, GetStdHandle, Winsock) ;
(iii) **constantes de plateforme** (PAGE_EXECUTE_READWRITE, handles) ;
(iv) **plan d'adressage d'image** (RVA littéraux — propriété de l'image, pas
de l'OS, mais la granularité l'exige aussi). La classe A exige ZÉRO couplage :
un contrat qui nomme un registre n'est pas instanciable tel quel sous SysV
(l'argument 1 vit en rdi, pas en rcx).

## 2. Le constat central — la classe A est VIDE

**Aucun contrat du corpus nominal n'est de classe A.** Le paramétrage msx64
est PARTOUT, jusqu'aux feuilles les plus pures : `libc-01:R1` ouvre par
« P1 rcx contient dst » (la brique de déplacement mémoire, sans aucun service
OS, porte néanmoins la convention d'appel Windows dans sa pré-condition) ;
`libc-03:R1` (« rcx contient l'adresse d'une chaîne ») est la feuille la plus
courte du patrimoine et porte le même couplage. Même l'alignement de pile
« rsp ≡ 8 mod 16 », identique en valeur sous SysV, est ÉNONCÉ dans le vocabulaire
de la convention msx64. Ce n'est pas un défaut des contrats : c'est le constat
que l'intention du projet a vécu 26/10 → 04/11 sur un seul profil, et que la
couche I a hérité de son époque. La voie du diff nul passe donc ENTIÈREMENT
par la révision de granularité — exactement ce que D149-(3) annonçait.

## 3. La classe B — les douze révisions R+1 du corpus nominal

| Contrat | R | Couplage nommé (espèce) | La révision R+1 |
|---|---|---|---|
| hello-02 (écrire) | 1→2 | (i) rcx/rdx/r8, 4e/5e args pile ; (ii) WriteFile+IAT, HANDLE GetStdHandle ; (iii) shadow space 0x28 | arguments nommés flux/tampon/longueur ; le service d'écriture du profil et la zone d'accueil (shadow space vs néant) vivent en frag-con |
| hello-03 (sortir) | 1→2 | (i) rcx ; (ii) ExitProcess+IAT | argument nommé code ; le service de sortie du profil en frag-con ; l'inaccessible défensif (`ud2` vs arrêt nu) demeure |
| libc-01 memcpy | 1→2 | (i) rcx/rdx/r8 | dst/src/n nommés ; la carte des registres et l'ensemble non volatil du profil en frag-con |
| libc-02 memcmp | 1→2 | (i) rcx/rdx/r8 | ptr1/ptr2/n nommés ; frag-con |
| libc-03 strlen | 1→2 | (i) rcx | chaîne nommée ; frag-con |
| libc-04 itoa | 2→3 | (i) ecx/rdx | valeur/tampon nommés ; frag-con |
| libc-05 zone-alloc | 1→2 | (i) rcx/rdx ; (iv) curseur « à RVA 0x3000 » | taille/alignement nommés ; le curseur « à l'adresse déclarée au plan de l'image » (frag-loc) |
| libc-06 zone-reset | 1→2 | (iv) curseur « à RVA 0x3000 » | idem — la seule pré-condition est l'adresse, la révision la déplace au plan |
| libc-07 memset | 1→2 | (i) rcx/dl/r8 | dst/valeur/n nommés ; frag-con |
| libc-08 autotest | 2→3 | (i) frame msx64/shadow space ; (ii) GetStdHandle/WriteFile/ExitProcess ; (iv) entry PE | l'entrée de l'artefact du profil (frag-con : PE loader vs appel par le principal du jalon) ; l'émission et la terminaison passent par les services du profil (écrire/sortir sur l'instance Linux) ; le verdict N est rendu (rax) à l'appelant sur SysV, le principal porte la terminaison — l'OBSERVABLE (la ligne exacte, le code de sortie) est invariant |
| tcp-07 patch | 3→4 | (i) rcx, frame msx64 0x28 ; (ii) VirtualProtect ; (iii) PAGE_EXECUTE_READWRITE(0x40)/PAGE_EXECUTE_READ(0x20) ; (iv) entrée echo 0x4600/croissance 0x4680 | mode nommé ; le service de protection de pages du profil et ses constantes (VirtualProtect/PAGE_* ↔ mprotect/PROT_*) en frag-con ; la cible et la croissance vivent au plan de l'image (frag-loc) — l'instance Linux cible l'entrée du JOURNAL (tcp-11), la démonstration M5-(c) du chantier (d) |
| tcp-11 journal | 1→2 | (i) rcx/rdx/r8/r9 + 5e arg pile ; (ii) WriteFile, Enter/LeaveCriticalSection ; (iv) handle .data, CRITICAL_SECTION .data | préfixe/longueur/valeur/suffixe/longueur suffixe nommés (cinq arguments — EN REGISTRES sous SysV) ; le verrou d'exclusion du profil en frag-con (section critique Windows initialisée par tcp-12 ↔ qword .bss né déverrouillé, lock xchg) ; l'émission par écrire |

**Règle d'or de la révision (l'invariance)** : les OBSERVABLES — post-conditions
Q, cas d'échec E, vecteurs dorés V — sont INVARIANTS de R à R+1. La révision ne
touche QUE le paramétrage formel (pré-conditions, invariants d'ABI, services).
L'instance Windows scellée (les octets figés par les balises 0.1.0 → 0.6.0)
reste CONFORME à la révision R+1 : c'est la thèse même du diff nul — l'intention
vit dans I, pas dans les octets.

## 4. La classe C — couplés à l'OS, hors corpus (frontière D149, jamais silencieuse)

| Contrat | Le couplage à l'OS |
|---|---|
| hello-01 (main M0) | le point d'entrée PE (AddressOfEntryPoint, pile chargeur, PEB) et GetStdHandle — l'orchestration d'entrée EST la plateforme ; le corpus a son principal propre au jalon (corpus-13, modèle ah-09) |
| libc-09 (zone-alloc-ts) | l'exclusion inter-threads par section critique Windows — la contrepartie exige le verrou du profil, chantier ouvert avec le corpus réseau |
| tcp-01..06, 08..10, 12 (serveur écho M2) | l'interface socket Winsock (WSAStartup/accept/recv/send), le modèle processus/fil Windows (CreateThread, WaitForMultipleObjects) — le réseau complet est l'extension OUVERTE nommée par D149 |
| http-08/10/12 (M5) | Winsock + Schannel + ligne de commande Windows — le patrimoine du relevement HTTPS demeure primaire |

Ces contrats ne sont PAS réduits : la frontière est nommée au plan
(« le critère § 18-M6 se démontre sur le corpus nominal, l'extension au corpus
réseau est un chantier OUVERT, à la demande du développeur »).

## 5. La voie retenue — les révisions vivent dans l'arbre du jalon

Les révisions R+1 ne sont PAS écrites sur place dans m0/I, m1/I, m2/I.
Le motif est STRUCTUREL, constaté au geste même de l'état zéro du chantier :
les chaînes scellées **épinglent la révision dans leurs plans d'adressage**
(`charger_couche_I` exige `spec:R{rev} == sid` du layout) — une révision sur
place casserait le vérificateur de chaque jalon clos, et divergerait les arbres
I de leurs manifestes signés au sceau de l'Intention (D87, clé hors-ligne —
la cérémonie serait requise pour TROIS arbres avant tout autre geste).
L'invariance exigée par D149-(3) (« les scellés ne bougent pas ») s'étend donc
des octets aux chaînes et aux arbres : **m0/I, m1/I, m2/I demeurent INTACTS**
(leurs vérificateurs vivants, le sceau-I à 11 arbres verts), et les révisions
R+1 vivent dans l'arbre du jalon — `unix/I/` (convention de dossiers
D149-(5)) — qui porte le corpus nominal de M6 ET de M7 (« le MÊME corpus,
troisième instanciation de la même couche I »).

Le diff nul se mesure alors PAR SCRIPT en trois recoupements (`diff_nul.py`,
rejouable) :
1. **Les fichiers canoniques** : l'instance Linux charge EXACTEMENT les
   fichiers de `unix/I/` (empreintes identiques, aucune copie nulle part) ;
   M7 en fera autant — la même couche I, la même empreinte ;
2. **L'équivalence des observables R1 ↔ R+1** : pour chaque contrat révisé,
   les sections observables (post, échecs, vecteurs) de l'ancêtre scellé et
   de la révision sont extraites et comparées — le diff est NUL sur les
   observables, les pré-conditions seules bougent (la granularité) ;
3. **L'invariance des scellés** : les empreintes sha256 des artefacts Windows
   (hello.exe, selftest.exe, echo.exe, proxy.exe 0.4.0, proxy.exe 0.6.0) sont
   identiques à l'état zéro mesuré avant le geste.

## 6. L'incident de l'état zéro (consigné, il fonde une règle)

En mesurant l'état zéro, le geste a lancé `m1/build_m1.py` SANS argument pour
« constater le refus anti-rollback » : le mode par défaut est la CONSTRUCTION,
et la garde de l'ère m1 a **échoué ouverte** — la carte scellée ne s'ouvre
pas sous la phrase du jour (lignée de clés réinitialisée depuis le scellage)
et `except ErreurCarte: pass` traite « illisible » comme « absente :
première construction ». Le build a tourné : selftest.exe est resté
OCTET-IDENTIQUE (chaîne déterministe), la carte m1 régénérée en dev.2 a été
RESTAURÉE octet-pour-octet depuis git, et le constat structurel est né :
**toutes les gardes m1→m5 (l'ère D147 comprise) échouent ouvertes sur carte
illisible**. La règle qui en sort (consignée à la décision du chantier) :
ABSENT ≠ ILLISIBLE — une carte PRÉSENTE et indéchiffrable est un REFUS,
jamais une permission ; la garde du jalon (`build_corpus.py`) distingue les
deux dès sa naissance. Le correctif des chaînes historiques est un geste
nommé pour le développeur (cinq chaînes scellées, aucune urgence : les cartes
m1→m4 sont des scellés d'archives, seule m5 vit sous la phrase du jour).

## 7. Décisions et frontières

Décisions : D14 (universalité), D22 (suite de conformité), D34 (échelle
auto-hébergée — le hachoir a frayé la voie ELF64), D87 (sceau de l'Intention),
D149 (programme M6/M7, corpus restreint, révision de granularité), D150
(tables motivées par bloc, l'état traverse en mémoire).

Frontières : l'audit ne TOUCHE rien (aucun fichier modifié — les révisions
suivent, écrites-avant-code) ; la classe C n'est jamais une réduction (la
frontière D149 la nomme au plan) ; l'incident de l'état zéro est restauré et
consigné (§ 6) ; les révisions R+1 de l'arbre du jalon seront mesurées
équivalentes aux ancêtres par le script du diff nul AVANT tout vert de
l'oracle.
