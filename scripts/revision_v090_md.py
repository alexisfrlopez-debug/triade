#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v090_md.py — LA RÉVISION DE CONSOLIDATION DU PROGRAMME D'APRÈS
M10 sur docs/PROTOCOLE_TRIADE.md (le modèle D169/D176 : v0.7.0 après M8,
v0.8.0 après M9, v0.9.0 après M10). Chaque remplacement ASSERTÉ.

La v0.9.0 consigne : LE JALON M10 FRANCHI (D178 — la balise `loupe 0.1.0`
SCELLÉE sur le onzième run vert recoupé 39/39, la méthode TRIADE entière
prouvée par la CRÉATION : onze runs, onze leçons) ET LE PROGRAMME D'APRÈS
M10 (D179 — la version 0.1.1-dev.1 COMMANDÉE : la dette [R10-PÉRIMÉE]
soldée à la naissance, le douzième run attendu, la balise `loupe 0.1.1`
se scellera sur le vert recoupé)."""

CHEMIN = "/home/z/my-project/triade/docs/PROTOCOLE_TRIADE.md"
texte = open(CHEMIN, encoding="utf-8").read()
n_marqueurs_avant = sum(texte.count(m) for m in ("v0.8.0", "v0.8.1", "v0.8.2",
                                                 "v0.8.3", "v0.8.4"))


def remplace(ancien, nouveau, combien=1):
    global texte
    n = texte.count(ancien)
    assert n == combien, f"ancre {n}x (attendu {combien}) : {ancien[:80]!r}"
    texte = texte.replace(ancien, nouveau)


# ── 1. le titre et la source de travail ────────────────────────────────────
remplace("# PROTOCOLE TRIADE v0.8.0 — Spécification technique",
         "# PROTOCOLE TRIADE v0.9.0 — Spécification technique")
remplace("> Source de travail faisant autorité pour la v0.8.0. Les archives formelles des versions",
         "> Source de travail faisant autorité pour la v0.9.0. Les archives formelles des versions")
remplace("demeurent : `docs/Protocole_TRIADE_v0.7.0_Specification.pdf` (v0.7.0),",
         "demeurent : `docs/Protocole_TRIADE_v0.8.4_Specification.pdf` (v0.8.4 — "
         "dernière révision de terrain du TGN),\n"
         "> `docs/Protocole_TRIADE_v0.8.0_Specification.pdf` (v0.8.0),\n"
         "> `docs/Protocole_TRIADE_v0.7.0_Specification.pdf` (v0.7.0),")

# ── 2. le paragraphe d'en-tête (la consolidation en tête) ─────────────────
remplace("""> La v0.8.0 consolide le programme d'après M9 (D170/D171) : le jalon M9 — TLS 1.3 pur
> en blocs scellés, le domaine `tls13` — est FRANCHI (finale `1.0.0` scellée sur le
> run terrain vert recoupé et LA SESSION RÉELLE — la ligne applicative chiffrée
> échangée avec un serveur réel, D170), et LE TEST GRANDEUR NATURE est ouvert (D171) :
> le jalon M10 — coder une application réelle NEUVE entièrement avec TRIADE — porte
> l'application « Loupe » (l'éditeur hexadécimal au panneau d'empreintes, le domaine
> `loupe`), sa couche I de 18 spécifications et ses QUATRE chantiers de notation
> accomplis (le noyau, le rendu + la navigation, l'édition + la table de routage
> étendue — les 18 blocs NOTÉS-MESURÉS-PROUVÉS) ; le kit terrain attend LA CÉRÉMONIE
> D'ÈRE du TGN (le quatorzième arbre, la dette D166/D171) ; la
> v0.6.1 consigne l'arbitrage du niveau de naissance d'un coffre neuf (D137) ; la""",
         """> La v0.9.0 consolide le programme d'après M10 (D178/D179) : LE JALON M10 — le test
> grandeur nature, l'application « Loupe » (l'éditeur hexadécimal au panneau
> d'empreintes, le domaine `loupe`) — est FRANCHI : l'application est NÉE ENTIÈREMENT
> DE LA MÉTHODE (la cérémonie d'ère passée sur pièces — le garde à QUATORZE arbres,
> les 18 blocs NOTÉS-MESURÉS-PROUVÉS, le kit déployé au coffre /test), ONZE RUNS
> TERRAIN l'ont VÉCUE — onze défauts nommés, onze retouches documentées (chaque
> défaut du kit ou de la pièce NOMMÉ sur pièces, jamais un vert muet) — ET LA
> VITRINE A VÉCU CHEZ SON UTILISATEUR (les deux codes à 0, deux runs de suite) :
> LE ONZIÈME RUN recoupé 39/39, LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE
> CARTE (D178 — l'artefact INTACT, la dette de la carte soldée par la
> régénération des notations, la cristallisation 26 × 10/10, l'anti-rollback
> ARMÉ) : LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION. LE PROGRAMME
> D'APRÈS M10 est ouvert à la commande du développeur (D179) : la version
> `0.1.1-dev.1` est NÉE DE LA RECOMPOSITION — la dette [R10-PÉRIMÉE] (les 17
> sommes de l'ère dev.5) SOLDÉE À LA NAISSANCE, le code BYTE-IDENTIQUE au vécu
> des onze runs (R4/R7), le DOUZIÈME RUN attendu : la balise `loupe 0.1.1` se
> scellera sur le vert recoupé (le miroir D165/D170) ; la
> v0.6.1 consigne l'arbitrage du niveau de naissance d'un coffre neuf (D137) ; la""")

# ── 3. la ligne « Version : » (l'état de la spécification) ─────────────────
_ligne_v084 = texte[texte.index("- Version : v0.8.4"):]
_ligne_v084 = _ligne_v084[:_ligne_v084.index("\n")]
remplace(_ligne_v084,
         "- Version : v0.9.0 — la révision de consolidation du programme d'après M10 "
         "(D178/D179) : **LE JALON M10 FRANCHI le 11/11/2026** — l'application "
         "« Loupe » NÉE ENTIÈREMENT DE LA MÉTHODE (la couche I de 18 spécifications "
         "écrites-avant-code, les QUATRE chantiers de notation — 159 contrôles verts "
         "aux trois graines —, la cérémonie d'ère PASSÉE : le garde 14/14, le kit "
         "déployé au coffre /test), ONZE RUNS TERRAIN (Entrées 202–219 : ONZE DÉFAUTS "
         "NOMMÉS, ONZE RETOUCHES DOCUMENTÉES — les refus du chargeur 0xc000007b "
         "[l'enveloppe de la lignée NORME DE FAIT], [CADRE-NÉ] [l'initialiseur .data "
         "MIROIR EXACT du CADRE_VIERGE — LE GARDE GUÉRI : le contrôle dérive du plan, "
         "jamais de la pièce qu'il contrôle], la classe des arguments pile [l'audit "
         "d'ABI msx64 NÉ AU BUILD], [SESSION] -7 [L'OMBRE au kit, l'artefact "
         "acquitté], [HINSTANCE-PEB] [r12 = GetModuleHandleW(NULL) LE VRAI MODULE], "
         "[D54-QUATRIÈME] + [EAX-SANS-SIGNE] [l'IAT relogée 0x3100 en QUATRE plages "
         "séparées par NULL, les 20 rendus étendus au 64 bits], [OFT-QWORD] [les "
         "QUATRE OFT au pas DWORD — la sixième mort NOMMÉE par le journal "
         "d'événements [4/4]], [FREE-SANS-TYPE] [le HMODULE en POINTEUR, l'essai "
         "isolé pour TOUTE classe], [RET-NU] [mov eax, 1 ; ret — le verdict ATTACH "
         "VRAI PAR CONSTRUCTION], [SONDE-EXE] [le faux négatif structurel : le "
         "chargeur de bibliothèque ne résout JAMAIS les imports d'un EXE — LA "
         "LIAISON PROUVÉE PAR LE VIVANT]) — ET LA VITRINE A VÉCU (0 et 0 aux "
         "dixième et onzième runs : L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON "
         "UTILISATEUR) ; LE ONZIÈME RUN recoupé 39/39 : **LA BALISE `loupe 0.1.0` "
         "SCELLÉE PAR FAIT DE CARTE** (D178 — la dette de la carte soldée par la "
         "RÉGÉNÉRATION DES NOTATIONS [18/18 == la pièce OCTET POUR OCTET, l'écart "
         "587 → 0], la cristallisation 26 × 10/10, la re-signature à la graine "
         "durable [LE TÉMOIN NE BOUGE PAS], l'anti-rollback ARMÉ, loupe.exe INTACT "
         "054de960…) — LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION ; LE "
         "PROGRAMME D'APRÈS M10 (D179, la commande du développeur) : la version "
         "`0.1.1-dev.1` NÉE DE LA RECOMPOSITION — LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA "
         "NAISSANCE (les 17 sommes rafraîchies à la VÉRITÉ des blocs, le qword porté "
         "0x00010008 → 0x00010101, 0 OCTET AILLEURS — le code byte-identique au vécu "
         "des onze runs, R4/R7), la carte GÉNÉRATION 17, le kit 0.1.1-dev.1 DÉPOSÉ "
         "au coffre /test (loupe-kit-13, le réceptacle ARMÉ) — LE DOUZIÈME RUN "
         "ATTENDU : si le vert tient, LA BALISE `loupe 0.1.1` SCELLÉE sur run "
         "recoupé (le miroir D165/D170). Sous les révisions de terrain v0.8.1 à "
         "v0.8.4, les enseignements des runs un à un ; sous la v0.8.0, la "
         "consolidation du programme d'après M9 (D170/D171)")
remplace("- Date : 9 novembre 2026", "- Date : 11 novembre 2026")

# ── 4. § 1.10 — ce que change la version ───────────────────────────────────
remplace("### 1.10 Ce que change la v0.8.0", "### 1.10 Ce que change la v0.9.0")
remplace("""La révision de consolidation du programme d'après M9 (D170/D171). Le **jalon M9**
(TLS 1.3 pur en blocs scellés — le domaine `tls13`, l'ère 1.0.0) est **franchi** :
les 28 blocs notés-mesurés-prouvés — les primitives aux vecteurs officiels octet
pour octet (FIPS 180-4, RFC 2104/4231, 5869, 7748, SP 800-38D), la poignée
rejouée sur le transcript RFC 8448, les héritages PAR LA CARTE (R7) —, le socle
socket par syscalls directs, le septième run terrain vert sur pièces et recoupé,
LA SESSION RÉELLE (la ligne applicative chiffrée ÉCHANGÉE avec un serveur réel,
le témoin « HTTP/1.1 200 OK » DÉCHIFFRÉ PAR LA MACHINE, l'épinglage -6 NOMMÉ
contre le vrai serveur, la fermeture propre), la finale `1.0.0` scellée sur le
recoup exigé comme pièce (D170 : le scellage est un fait de carte, l'artefact ne
bouge jamais) — et l'ère M8 refermée propre par l'export de continuité. **LE TEST
GRANDEUR NATURE est ouvert (D171)** : le protocole avait prouvé chaque capacité,
M0 à M9 — il reste à prouver qu'il DÉVELOPPE une application réelle NEUVE, de
l'intention à l'octet livré (le modèle RoomEq s'arrêtait au recodage ; le TGN
exige la CRÉATION). L'application — arbitrée à D171, contredisible — est
« Loupe », l'éditeur hexadécimal au panneau d'empreintes sur le profil primaire
(l'outil du quotidien du projet : voir les octets, leurs lignes, leurs empreintes
md5/sha-256, leur place) : le domaine `loupe` fondé (la charte + le tableau des
18 blocs en cinq familles), la couche I posée écrite-avant-code (D172 : les 18
spécifications, le plan d'adressage arrêté avant toute notation, la table des
sept verdicts), et les QUATRE chantiers de notation accomplis — le noyau
fichier + empreintes (D173 : les héritages vivent à leurs adresses scellées, le
mini-OS virtuel du harnais), le rendu + la navigation (D174 : l'oracle à
scénarios — l'écran attendu octet par octet —, le mini-GUI virtuel, le plancher
qui ne recule jamais), l'édition + la table de routage étendue de loupe-09 r2
(D175 : le disque saisissable et la mort du harnais, le réseau de la garde
16↔17↔18, l'écriture à l'octet prouvée différentielle) — les 18 blocs
NOTÉS-MESURÉS-PROUVÉS, 45 + 53 + 59 contrôles verts aux trois graines sur les
trois harnais. Le **kit terrain attend LA CÉRÉMONIE D'ÈRE du TGN** : la dette
D166/D171 est nommée à la naissance — le quatorzième arbre (`loupe`) et
l'extension du registre figé exigent la clé hors-ligne du développeur AVANT
tout build (§ 13.5) ; le garde demeure à treize arbres. Le projet fils
COFFRE-FORT est dégelé en parallèle (D135 amendée par D171) : le père continue
sans ralentir, la frontière fondatrice demeure INTACTE. Aucune règle du cœur
n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la
fonction objectif est inchangée.""",
         """La révision de consolidation du programme d'après M10 (D178/D179). Le **jalon M10**
(le test grandeur nature — le domaine `loupe`) est **franchi** : l'application
« Loupe », l'éditeur hexadécimal au panneau d'empreintes, est NÉE ENTIÈREMENT DE
LA MÉTHODE — la cérémonie d'ère passée sur pièces (le garde à QUATORZE arbres,
la dette D166/D171 soldée), la couche I de 18 spécifications écrites-avant-code
(D172), les QUATRE chantiers de notation (D173–D175 : les 18 blocs
NOTÉS-MESURÉS-PROUVÉS, 159 contrôles verts aux trois graines), le kit déployé au
coffre `/test` (M10-(d)) — ET ONZE RUNS TERRAIN (M10-(e), Entrées 202–219) :
ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES — les refus du chargeur
(l'enveloppe prouvée de la lignée NORME DE FAIT), [CADRE-NÉ] (l'initialiseur
`.data` MIROIR EXACT du `CADRE_VIERGE` du harnais — LE GARDE GUÉRI : le contrôle
dérive du plan, jamais de la pièce qu'il contrôle), la classe des arguments pile
(l'audit d'ABI msx64 NÉ AU BUILD), [SESSION] -7 VERROUILLÉ (L'OMBRE au kit,
l'artefact acquitté), [HINSTANCE-PEB] (l'entrée réécrite : r12 =
GetModuleHandleW(NULL) LE VRAI MODULE), [D54-QUATRIÈME] + [EAX-SANS-SIGNE]
(l'IAT relogée à 0x3100 en QUATRE plages séparées par NULL, les 20 rendus
négatifs étendus au 64 bits), [OFT-QWORD] (les QUATRE OFT au pas DWORD du
chargeur — la sixième mort NOMMÉE par le journal d'événements [4/4]),
[FREE-SANS-TYPE] (le HMODULE en POINTEUR, l'essai isolé pour TOUTE classe
d'exception), [RET-NU] (`mov eax, 1 ; ret` — le verdict ATTACH VRAI PAR
CONSTRUCTION), [SONDE-EXE] (le faux négatif STRUCTUREL de la sonde de liaison :
le chargeur de bibliothèque ne résout JAMAIS les imports d'un module exécutable —
LA LIAISON PROUVÉE PAR LE VIVANT) — ET LA VITRINE A VÉCU (0 et 0 aux dixième et
onzième runs : L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR). LE
ONZIÈME RUN recoupé 39/39 : **LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE
CARTE** (D178 : la dette de la carte soldée par la RÉGÉNÉRATION DES NOTATIONS —
18/18 notations == la pièce OCTET POUR OCTET, l'écart de l'audit 587 → 0 ; la
cristallisation 26 × 10/10 ; la re-signature à la graine durable D144 — LE
TÉMOIN NE BOUGE PAS ; l'anti-rollback ARMÉ ; loupe.exe INTACT 054de960… — LE
MÊME binaire que le run a couru) : **LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA
CRÉATION — de l'intention (la couche I) à l'octet vécu chez son utilisateur**.
LE PROGRAMME D'APRÈS M10 APPARTIENT AU DÉVELOPPEUR : la version `0.1.1-dev.1`
est COMMANDÉE (D179) — la dette [R10-PÉRIMÉE] (les 17 sommes de l'ère dev.5 que
les retouches des Entrées 210/214 changèrent sans rafraîchir la table) SOLDÉE À
LA NAISSANCE : la pièce naît de LA RECOMPOSITION même (chaque somme == son bloc
relu, par construction), le qword version porté 0x00010101, 0 OCTET AILLEURS —
le code BYTE-IDENTIQUE au vécu des onze runs (R4 : le contrat stable ; R7 : les
adresses intactes), la carte GÉNÉRATION 17 ; le kit 0.1.1-dev.1 DÉPOSÉ au
coffre `/test` (loupe-kit-13, le réceptacle ARMÉ) — LE DOUZIÈME RUN ATTENDU :
si le vert tient (le scénario ENTIER T0 → S0 → LA LIAISON ET la vitrine
vivante), LA BALISE `loupe 0.1.1` SCELLÉE sur run terrain recoupé (le miroir
D165/D170 : la porte est de processus). Le projet fils COFFRE-FORT demeure
dégelable au rythme du développeur (D135 amendée par D171) : la frontière
fondatrice demeure INTACTE. Aucune règle du cœur n'est modifiée ; aucune couche
n'est ajoutée à l'exécution ; la hiérarchie de la fonction objectif est
inchangée.""")

# ── 5. § 18 — la rangée M10 franchie ───────────────────────────────────────
_ligne_m10 = texte[texte.index("| M10 | Le test grandeur nature"):]
_ligne_m10 = _ligne_m10[:_ligne_m10.index("\n")]
remplace(_ligne_m10,
         "| M10 | Le test grandeur nature — « Loupe » (domaine `loupe`) | coder une "
         "application réelle NEUVE entièrement avec TRIADE, de l'intention (la couche "
         "I) à l'octet livré (le kit terrain) ; les 18 spécifications écrites-avant-"
         "code avant tout octet de notation (R2) ; les héritages PAR LA CARTE "
         "byte-identiques aux adresses scellées (R7) ; l'oracle à scénarios vert — "
         "l'écran attendu octet par octet ; le kit déployé au coffre `/test` "
         "(modèle m9f) ; la balise `loupe 0.1.0` scellée sur run terrain recoupé | "
         "**franchi** 11/11/2026 (Entrées 218/219, D178) — l'application est NÉE "
         "ENTIÈREMENT DE LA MÉTHODE : la cérémonie d'ère PASSÉE SUR PIÈCES (le 14e "
         "arbre, la dette D166/D171 SOLDÉE — le garde 14/14), les 18 blocs NOTÉS-"
         "MESURÉS-PROUVÉS (59 + 53 + 45 contrôles verts aux trois graines), le kit "
         "déployé (M10-(d)) — ET ONZE RUNS TERRAIN, ONZE DÉFAUTS NOMMÉS, ONZE "
         "RETOUCHES DOCUMENTÉES : les refus du chargeur 0xc000007b (dev.1/dev.2 — "
         "l'enveloppe de la lignée NORME DE FAIT), [CADRE-NÉ] (dev.4 — "
         "l'initialiseur .data MIROIR EXACT du CADRE_VIERGE, LE GARDE GUÉRI : le "
         "contrôle dérive du plan, jamais de la pièce qu'il contrôle), la classe des "
         "arguments pile (dev.5 — l'audit d'ABI msx64 NÉ AU BUILD), [SESSION] -7 "
         "VERROUILLÉ (dev.6 kit — L'OMBRE temoin-session.bin, la pièce ACQUITTÉE), "
         "[HINSTANCE-PEB] (dev.6 — l'entrée réécrite r12 = GetModuleHandleW(NULL)), "
         "[D54-QUATRIÈME] + [EAX-SANS-SIGNE] (dev.7 — l'IAT relogée 0x3100 en "
         "QUATRE plages séparées par NULL, les 20 rendus au 64 bits), [OFT-QWORD] "
         "(dev.8 — les QUATRE OFT au pas DWORD : la sixième mort nommée par le "
         "journal d'événements [4/4]), [FREE-SANS-TYPE] (dev.12 kit — le HMODULE en "
         "POINTEUR, l'essai pour TOUTE classe), [RET-NU] (dev.11 kit — mov eax, 1 ; "
         "ret), [SONDE-EXE] (le faux négatif STRUCTUREL : le chargeur de "
         "bibliothèque ne résout JAMAIS les imports d'un EXE — LA LIAISON PROUVÉE "
         "PAR LE VIVANT) ; LA VITRINE VIVANTE (0 et 0 aux 10e/11e runs — après six "
         "morts, L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR) ; LE "
         "ONZIÈME RUN recoupé 39/39 (T0→T7 TOUT VERT la quatrième fois, LA CASCADE "
         "205 VÉCUE ENTIÈRE la première, la vitrine la seconde) : LE VERT TIENT "
         "ENTIER — LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE (D178 : la "
         "dette de la carte soldée par la RÉGÉNÉRATION DES NOTATIONS [18/18 == la "
         "pièce OCTET POUR OCTET, 587 → 0], la cristallisation 26 × 10/10, "
         "l'anti-rollback ARMÉ, loupe.exe INTACT 054de960…) — LA MÉTHODE TRIADE "
         "ENTIÈRE PROUVÉE PAR LA CRÉATION ; LA SUITE COMMANDÉE (D179) : la version "
         "0.1.1-dev.1 née de la recomposition — la dette [R10-PÉRIMÉE] SOLDÉE À LA "
         "NAISSANCE (17 sommes rafraîchies à la vérité des blocs, le qword porté "
         "0x00010101, 0 octet de code changé), le douzième run attendu : la balise "
         "`loupe 0.1.1` sur le vert recoupé |")

# ── 6. § 18 — le préambule (la phrase périmée sur la cérémonie) ────────────
remplace("""M10 est l'épreuve de
la MÉTHODE ENTIÈRE (D171) : non plus une capacité, mais une application réelle
neuve — l'outil du quotidien du projet — développée de l'intention à l'octet
livré, chaque geste prouvé ; la notation entière (18 blocs) est déjà
notée-mesurée-prouvée, le build attend la cérémonie d'ère du TGN.""",
         """M10 est l'épreuve de
la MÉTHODE ENTIÈRE (D171) : non plus une capacité, mais une application réelle
neuve — l'outil du quotidien du projet — développée de l'intention à l'octet
livré, chaque geste prouvé — ET ELLE EST FRANCHIE (D178) : onze runs terrain,
onze leçons, la balise `loupe 0.1.0` scellée sur le onzième run recoupé — la
création a vécu chez son utilisateur ; la version 0.1.1 (D179) poursuit : la
dette [R10-PÉRIMÉE] soldée à la naissance, le douzième run attendu.""")

# ── 7. § 21 — le journal des versions (l'entrée v0.9.0 en tête) ────────────
remplace("""| Version | Date | Contenu |
|---|---|---|
| v0.8.2 | 9 nov. 2026 |""",
         """| Version | Date | Contenu |
|---|---|---|
| v0.9.0 | 11 nov. 2026 | Révision de consolidation du programme d'après M10 (D178/D179) : LE JALON M10 — le test grandeur nature « Loupe » — est FRANCHI (l'application NÉE ENTIÈREMENT DE LA MÉTHODE : onze runs terrain, onze défauts nommés, onze retouches documentées, LA VITRINE VIVANTE chez son utilisateur, le onzième run recoupé 39/39 — la balise `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE, la dette de la carte soldée par la régénération des notations, la cristallisation 26 × 10/10, l'anti-rollback ARMÉ) : LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION ; LE PROGRAMME D'APRÈS M10 (D179) : la version `0.1.1-dev.1` COMMANDÉE — la dette [R10-PÉRIMÉE] (17 sommes de l'ère dev.5) SOLDÉE À LA NAISSANCE (la pièce née de la recomposition, le qword porté 0x00010101, 0 octet de code changé — R4/R7), le kit 0.1.1-dev.1 déposé au coffre /test, LE DOUZIÈME RUN ATTENDU (la balise `loupe 0.1.1` sur le vert recoupé, le miroir D165/D170). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.8.2 | 9 nov. 2026 |""")

# ── 8. la clôture (le paragraphe final) ────────────────────────────────────
_cloture = texte[texte.index("La présente version consigne"):]
_cloture = _cloture[:_cloture.index("\n")]
remplace(_cloture,
         "La présente version consigne LA RÉVISION DE CONSOLIDATION DU PROGRAMME "
         "D'APRÈS M10 (v0.9.0, D178/D179) : les jalons M0 à M10 sont TOUS franchis "
         "sur validations terrain (balises finales 0.2.0, 0.9.0, `1.0.0` et "
         "`loupe 0.1.0` — la session réelle la ligne applicative chiffrée, la "
         "création l'application née de TRIADE vécue chez son utilisateur), le "
         "programme de souveraineté cryptographique accompli (axes 2-3-4, D133) ; "
         "LE JALON M10 est l'épreuve de la MÉTHODE ENTIÈRE — onze runs terrain, "
         "onze défauts nommés, onze retouches documentées : chaque défaut du kit ou "
         "de la pièce nommé sur pièces (le chargeur, le CADRE-NÉ, la classe des "
         "arguments pile, L'OMBRE, le HINSTANCE, l'IAT relogée, les OFT au pas "
         "DWORD, le POINTEUR du FreeLibrary, le RET-NU, le SONDE-EXE), chaque "
         "enseignement consigné (le contrôle dérive du plan, jamais de la pièce "
         "qu'il contrôle ; l'échec nommé vaut plus que le vert muet ; la vitrine "
         "vivante prouve la liaison mieux que toute sonde) — et la balise "
         "`loupe 0.1.0` scellée sur le onzième run recoupé 39/39 : LA MÉTHODE "
         "TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION. Le programme d'après M10 est "
         "ouvert à la commande du développeur : la version 0.1.1-dev.1 (D179) "
         "porte la dette [R10-PÉRIMÉE] soldée à la naissance — le douzième run "
         "attendu scellera la balise `loupe 0.1.1` sur le vert recoupé. Les "
         "profils additionnels après M7 restent volontairement hors du périmètre "
         "courant afin que chaque addition s'appuie sur des résultats mesurés. La "
         "règle de gouvernance demeure : toute évolution invalide explicitement ce "
         "qu'elle remplace, et rien ne se change en silence — le terrain compris : "
         "chaque lecture d'exécution est une révision potentielle du modèle, et "
         "son enseignement se consigne (§ 8.4, § 8.5).")

open(CHEMIN, "w", encoding="utf-8").write(texte)
print(f"[md v0.9.0] la consolidation appliquée — {len(remplace.__doc__ or '')}"
      f" ; marqueurs v0.8.x : {n_marqueurs_avant} → "
      f"{sum(texte.count(m) for m in ('v0.8.0', 'v0.8.1', 'v0.8.2', 'v0.8.3', 'v0.8.4'))}"
      f" (les archives historiques demeurent), v0.9.0 : {texte.count('v0.9.0')}")
