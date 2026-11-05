#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_171.py — LA CONSIGNATION DU GESTE « LE CHANTIER M9-(b)
CONTINUE : LA FAMILLE hkdf NOTÉE-MESURÉE-PROUVÉE » : JOURNAL_TRAVAIL +Entrée
171 (ordre 170<171<marqueur, rejeu REFUSÉ), worklog +Task ID 89. Tout ancrage
absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 171 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE hkdf NOTÉE-MESURÉE-PROUVÉE — tls13-05..08 (HMAC-SHA-256 RFC 2104, HKDF-Extract/Expand RFC 5869, HKDF-Expand-Label RFC 8446 § 7.1) : la notation à la main (435/151/347/310 o, round-trip 100 %, les slots ARRÊTÉS 0x200/0xC0/0x180/0x180 tassés depuis 0xC3C0 — D161 rejoué), LE HARNAIS 52 contrôles · 52 VERTS × 3 graines (les SEPT vecteurs RFC 4231, les TROIS cas RFC 5869, LE TRANSFERT RFC 8448 — trois extraits + DIX étiquettes, la structure HkdfLabel RECROISÉE avec les « info » EXACTES de la RFC, la borne L = 8160, la falsification attrapée, le temps constant MESURÉ) ; UN DÉFAUT DE NOTATION nommé par le fail-closed (le masque opad écrasait l'intérieur) ; l'erratum d'arithmétique de la spec tls13-08 consigné AVANT la notation (06/11)

**La reprise SUR LES TROIS MIROIRS (D164 rejouée — la demande du développeur : « vérifie si la synchro entre le git et le drive est ok »).** Le bundle Drive triade-history.bundle cloné : pointe 39d84ae (la passation du Task 88 — l'arbre propre), le bundle du geste triade-history-090-c82fe7b.bundle relu md5 5ca58429… == le consigné du worklog, les SEIZE fichiers des deux derniers commits RECROISÉS octet pour octet avec le miroir TRIADE-sauvegarde-git/ (16/16 MATCH — les 4 notations sha, les 4 brouillons, le harnais, layout, auteur, JOURNAL, PLAN, worklog), les fichiers d'instruction racine MATCH, les archives-bundles relues (32 archives, l'ancien 090-ffe06fc présent) ; GitHub interrogé par ls-remote : bundle051/v0.5.1-jalon-v7 == c82fe7b — LA POINTE DU GESTE consignée par la passation (le commit de passation 39d84ae suivra au geste présent, miroir du flux établi). Les jetons rapatriés du coffre Drive /tokens vers .gdrive/ (600, JAMAIS affichés — la procédure du Task 79), check_auth.py : OAuth Drive 200, GitHub 200 (compte alexisfrlopez-debug), la remote origin reconfigurée vers github.com/alexisfrlopez-debug/triade.git (la mécanique de l'Entrée 133 : credential helper store, .gdrive/git-credentials 600). La réserve instrumentale D149 re-vérifiée AVANT usage : le disque labo recyclé avait emporté keystone/capstone/unicorn/pefile/pynacl — RÉINSTALLÉS PAR PROCÉDURE.

**L'arbre scellé INTACT (la frontière première du geste).** Le sceau I vérifié AVANT le geste et intégré au harnais (V0.c) : scripts/verifier_specs_m9a.py rejoué — VERDICT VERT (les 28 spécifications posées et cohérentes) ; la famille sha relue aux longueurs ARRÊTÉES 74/387/139/165 o (V0.b — la frontière du geste précédent) ; le scellé 0.9.0 relu (V0.a : 44 544 o, sha256 1492b0bc…b0cd4, les fixtures M8 intacts). R2 tenue : les specs tls13-05..08 signées au chantier (a) PRÉCÈDENT la notation — AUCUN octet de l'arbre scellé n'a bougé.

**La notation (les quatre brouillons msx64 → les quatre notations explicites WYSIWYG).** tls13-05 (h100005, HMAC-SHA-256) 435 o · 102 instructions — LA COMPOSITION DÉCLARÉE : TLS01 ×2 (DEUX contextes sur la pile, le chemin de la clé longue en emprunte un TROISIÈME : l'expulsion exercée), TLS03 ×4, TLS04 ×2 — la clé EXPULSÉE à 64 o dans les DEUX sens (≤ 64 : copiée et zéro-paddée ; > 64 : HACHÉE d'abord — RFC 4231 les clés de 131 o), les masques ipad/opad posés sur 64 positions FIXES par HUIT quads (movabs imm64 du plan — le temps constant PAR RAPPORT AU CONTENU, la longueur K publique), K' + le masque + ctx_i + ctx_o + L'INTÉRIEUR (32 o DÉDIÉS) sur la pile — AUCUN déplacement RIP, aucun état détenu (I2). tls13-06 (h100006, HKDF-Extract) 151 o · 41 instructions — le sel DEVIENT la clé du HMAC (l'expulsion EST le geste du bloc), le sel VIDE = les 32 zéros du RFC 5869 § 2.2 PORTÉS PAR LA PILE (quatre quads — AUCUN registre non volatil touché), l'IKM vide REFUSÉ (-2), UN appel à TLS05. tls13-07 (h100007, HKDF-Expand) 347 o · 105 instructions — l'ALLOCATION DYNAMIQUE 16-ALIGNÉE sur la pile ((F + 0x78) & ~0xF, l'épilogue RECALCULE depuis F), T(i−1) LU DEPUIS OKM ELLE-MÊME (I2 : la sortie est le tampon, aucune seconde copie), la DERNIÈRE itération dépose T(N) dans le brouillon 32 o puis recopie SEULS les L − 32(N−1) octets (la sortie JAMAIS dépassée), l'octet compteur 1..N ≤ 255 (la longueur est la garde), F borné à 2^61 − 33 (l'arithmétique du tampon), N refus nommé -1/-2. tls13-08 (h100008, HKDF-Expand-Label — LE bloc du calendrier) 310 o · 82 instructions — la structure HkdfLabel sérialisée GROS-BOUTISTE PAR IMMÉDIATS FIXES (u16 par xchg al,ah ; le préfixe « tls13 » DU PLAN D'ADRESSAGE en 0x31736c74 + 0x2033 — jamais recopié, T5 ; les longueurs u8), le libellé et le contexte recopiés, UN appel à TLS07, les SEIZE refus nommés (-1 pointeurs, -2 bornes libellé 0/250, C 256, L 0/8161).

**L'ARRÊT des slots (D161 rejoué).** Le MINIMUM admissible par longueur (multiple de 64, padding >= 16, tassés depuis la fin sha 0xC3C0) : tls13-05 @0xC3C0 (slot 0x200, padding 77) · tls13-06 @0xC5C0 (0xC0, 41) · tls13-07 @0xC680 (0x180, 37) · tls13-08 @0xC800 (0x180, 74) — fin de la famille hkdf à 0xC980, la réserve .text6 suit pour x25519/aead.

**L'ERRATUM consigné AVANT la notation (sur pièces — le modèle M9 av-10, le miroir M8-(b) libc-02).** La spec tls13-08 I1 écrit « 2 + 1 + 6 + libellé + 1 + C ≤ 264 o » : l'arithmétique des bornes P3/P5 (libellé ≤ 249, C ≤ 255) donne 2 + 1 + 255 + 1 + 255 = 514 o — l'ADDITION seule de la spec est fautive, JAMAIS son contrat : le tampon est ARRÊTÉ à 514 o (frame 0x2A0), l'erratum consigné dans l'en-tête du brouillon et au présent journal.

**Le harnais (tls13/harnais_hkdf.py — le modèle harnais_sha : l'émulation nue à les RVA du plan, les HUIT blocs posés, l'appelant factice msx64, les LOGEMENTS d'arguments de pile écrits à [rsp+0x28+8i] et relus intacts).** 52 contrôles · 52 VERTS × 3 graines (20261106, 41, 20261107) : V0 les pièces (le scellé relu, la famille sha intacte aux longueurs arrêtées, l'arbre I scellé relu VERT) ; V1 le round-trip 100 % (keystone == capstone, 102/41/105/82 instructions, les tailles == l'ARRÊT 435/151/347/310) + les concordances au plan (les appels de 05 == TLS01×3/TLS03×5/TLS04×3, de 06/07 == TLS05, de 08 == TLS07 ; les masques ipad/opad ×8 == HMAC_IPAD/OPAD ; le préfixe == PREFIXE_ETIQUETTE) + la structure (AUCUN syscall, AUCUN appel indirect, AUCUN déplacement RIP — tout vit en immédiats et sur la pile) + le temps constant STRUCTUREL (28 sauts conditionnels, chacun sur cmp/test SANS opérande mémoire) ; V2 les SEPT vecteurs officiels RFC 4231 appendice A OCTET POUR OCTET (les clés de 20/4/25 o, les DEUX clés de 131 o — l'expulsion exercée, le cas 5 sur sa troncature officielle de 128 bits) — la référence hashlib CROISÉE avant de juger, puis le balayage différentiel 132 cas (clés 0/1/31/32/33/63/64/65/100/131 × messages 0..1000 — l'expulsion aux bornes) ; V3 les TROIS cas officiels RFC 5869 (Extract, Expand, la CHAÎNE complète) + LE TRANSFERT RFC 8448 § 3 : les TROIS extraits du transcript (early : sel 32 zéros + IKM 32 zéros ; handshake : sel dérivé + IKM le secret partagé ; master — le sel vide ET le sel dérivé exercés sur pièces officielles) + les DIX étiquettes (« derived » ×2, « c hs traffic », « s hs traffic », « key » ×2, « iv » ×2, « finished » ×2 — les clés consignées par le transcript, RENDUES par le bloc) + LA STRUCTURE RECROISÉE (la HkdfLabel reconstruite == les « info » EXACTES imprimées par la RFC, octet pour octet — la sérialisation consignée) + la borne L = 8160 (255 itérations, le compteur atteint 0xFF) + les bornes de découpe 1/31/32/33/64/65/8159 + l'oracle différentiel 240 cas aléatoires bornés ; V4 le contrat (les HUIT non-volatiles rendus, la pile équilibrée, l'ombre et les logements intacts, la zone profonde intacte ; L'ALIGNEMENT msx64 à l'entrée de CHAQUE callee — 77 entrées surveillées à travers les appels directs, rsp ≡ 8 mod 16 chacune ; les entrées INTACTES relues octet pour octet ; la sortie JAMAIS dépassée — les canaris après L intacts à la borne 8159 ; les SEIZE refus NOMMÉS exercés un par un) ; V5 la falsification, ZÉRO SILENCE (42/42 mutations de clé et de message attrapées ; 11/11 de l'IKM et du sel ; 6/6 du PRK et du secret ; la comparaison non muette 20/20 ; K corrompu → l'HMAC diverge : la table @0x2F00 est LUE à travers la composition) ; V6 le temps constant MESURÉ (la clé courte 18 371 instructions EXACTEMENT ×4 ; la clé longue 31 844 ×4 ; l'IKM 18 407 ×4 ; le PRK 74 387 ×2 ; le secret 18 704 ×2 — le contenu JAMAIS, la longueur seule).

**LE DÉFAUT DE NOTATION nommé par le fail-closed (le premier du domaine : les blocs sha étaient nés bons, celui-ci a été CORRIGÉ PAR LA PREUVE).** tls13-05 rangeait le condensé INTÉRIEUR dans le masque @+0x60 : le masquage opad l'ÉCRASAIT avant l'absorption extérieure — V2 a nommé la faute au premier passage (les SEPT vecteurs RFC 4231 divergeaient, déterministes et faux) : CORRIGÉ par le slot DÉDIÉ @+0x180 (32 o, frame 0x1A0 — le masque opad n'écrase JAMAIS l'intérieur), re-mesuré 433→435 o, slots ré-arrêtés, REJOUÉ : 52/52 VERTS. Second défaut plus menu : tls13-06 touchait rdi non volatil pour poser les 32 zéros — V4.a l'a nommé (sentinelle rompue) : les QUATRE QUADS DIRECTS [rsp+0x28..0x40] le rendent, re-mesuré 147→151 o. Les défauts d'INSTRUMENT nommés et corrigés au geste : le round-trip mov/movabs (l'imm64 se note movabs — la convention des aînés av-01), les verdicts SIGNÉS (mov rax, -N l'extension de signe de la lignée sys — mov eax, -N zéro-étendait), l'exemption des logements par PLAGE d'octets (le qword entier, pas sa seule base), la zone profonde DESCENDUE à [−0x1000, −0xC00) (la chaîne 08→07→05→03→02 est profonde de ≈ 0x9B0 : le cadre de tls13-02, le w[64] de la compression, descend SOUS l'ancienne zone — l'alignement de la zone sur la CHAÎNE réelle, jamais sur une estimation), une page PAR donnée d'entrée (le canari « avant la donnée » voyait la donnée voisine), deux transcriptions hex du fixture RFC corrigées SUR LES RFC elles-mêmes (l'OKM du cas 5869-2, l'étiquette finished de c hs traffic — la référence croisée les aurait nommées).

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), AUCUN build (le chantier (e) attend son geste — le garde est VERT), l'arbre scellé tls13/I INTACT (le sceau relu VERT au harnais V0 APRÈS le geste), m8/proxy.exe INTACT (1492b0bc…, relu en V0.a), AUCUNE règle modifiée, la charte § 2 tenue (les vecteurs officiels AVANT usage — la référence croisée, la falsification). Livrables : tls13/layout.py (la famille hkdf ARRÊTÉE + les adresses A_HMAC/A_EXTRACT/A_EXPAND/A_EXPAND_LABEL), tls13/outils/auteur.py (les 8 blocs), tls13/notation/ (4 brouillons + 4 notations explicites), tls13/harnais_hkdf.py (52 contrôles VERTS × 3 graines) ; consignations : la présente Entrée PAR SCRIPT, PLAN (le chantier M9-(b) : la famille hkdf ; l'État du programme), worklog +Task ID 89.

- SUITE : LE CHANTIER M9-(b) CONTINUE — la famille x25519 (tls13-09..14 : les miroirs win des contrats av-05..11, l'échelle de Montgomery SANS branche de données, RFC 7748 § 6.1), puis aead (tls13-15..19 : SP 800-38A/38D, l'arrêt AES-NI, GHASH sans table par donnée) — la même discipline, les slots à la suite de 0xC980 ; puis (c) l'enregistrement + la poignée au harnais RFC 8448, (d) le socle socket sys-04+, (e) le build 1.0.0-dev.1, (f) le terrain.

"""

TASK = """

## Task ID 89 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE hkdf NOTÉE-MESURÉE-PROUVÉE (06/11)

- LA SYNCHRO VÉRIFIÉE SUR LES TROIS MIROIRS (la demande du développeur) :
  le bundle Drive cloné (pointe 39d84ae == la passation Task 88, l'arbre
  propre), le bundle du geste md5 5ca58429… == consigné, les 16 fichiers du
  geste recroisés 16/16 MATCH avec le miroir, GitHub == c82fe7b (la pointe
  du geste, le flux établi), les jetons du coffre /tokens (check_auth 200).
- LE GESTE : tls13-05..08 — HMAC-SHA-256 (RFC 2104 : l'expulsion de la clé
  dans les DEUX sens, les masques sur 64 positions fixes), HKDF-Extract
  (le sel devient la clé, le sel vide 32 zéros SUR LA PILE), HKDF-Expand
  (l'allocation dynamique 16-alignée, T(i−1) LU DEPUIS OKM, la borne
  8160), HKDF-Expand-Label (la HkdfLabel GROS-BOUTISTE par immédiats, le
  préfixe « tls13 » du plan) — notés (435/151/347/310 o, round-trip
  100 %), mesurés (les slots ARRÊTÉS 0x200/0xC0/0x180/0x180 tassés depuis
  0xC3C0 — D161 rejoué), prouvés (LE HARNAIS 52 contrôles · 52 VERTS × 3
  graines).
- LES PREUVES : les SEPT vecteurs RFC 4231 octet pour octet (les clés de
  131 o, la troncature officielle) + le balayage différentiel 132 cas ;
  les TROIS cas RFC 5869 + la chaîne complète ; LE TRANSFERT RFC 8448 —
  les trois extraits (early/handshake/master : le sel vide ET le sel
  dérivé) + les DIX étiquettes (« derived », « c/s hs traffic », « key »,
  « iv », « finished ») avec la structure HkdfLabel RECROISÉE sur les
  « info » EXACTES de la RFC ; la borne L = 8160 (le compteur d'un octet) ;
  les SEIZE refus nommés ; la falsification 59/59 attrapée + K corrompu →
  divergence ; le temps constant MESURÉ (18 371/31 844/18 407/74 387/
  18 704 instructions exactement) ; l'alignement msx64 à 77 entrées de
  callee ; la sortie JAMAIS dépassée (canaris après L).
- LE DÉFAUT DE NOTATION nommé par le fail-closed : tls13-05 rangeait
  l'intérieur dans le masque — l'opad l'écrasait (les SEPT vecteurs
  divergeaient au premier passage) : le slot DÉDIÉ @+0x180, re-mesuré,
  ré-arrêté, rejoué VERT ; rdi rendu dans 06 (quatre quads directs) ;
  l'erratum d'arithmétique de la spec tls13-08 consigné AVANT la notation
  (« ≤ 264 o » : les bornes P3/P5 donnent 514).
- FRONTIÈRES : aucune balise, AUCUN build, l'arbre scellé tls13/I INTACT
  (verifier_specs_m9a relu VERT au harnais V0), m8/proxy.exe INTACT, la
  famille sha intacte (74/387/139/165 relus) ; consignations : Entrée 171
  PAR SCRIPT, PLAN (chantier (b) : la famille hkdf + État du programme),
  worklog +Task ID 89.
- SUITE : la famille x25519 (tls13-09..14), puis aead (tls13-15..19) —
  les slots à la suite de 0xC980 ; puis (c) RFC 8448, (d) sys-04+,
  (e) le build 1.0.0-dev.1, (f) le terrain.

Stage Summary:
- LA SECONDE FAMILLE de la grande œuvre est notée-mesurée-prouvée : le
  calendrier de clés de TLS 1.3 (HMAC, Extract, Expand, Expand-Label)
  existe en octets et rend les clés du transcript officiel RFC 8448
  octet pour octet.
- LA PREUVE A CORRIGÉ LA NOTATION : le défaut de l'intérieur écrasé par
  l'opad, nommé par les vecteurs officiels au premier passage, corrigé
  par le slot dédié — le fail-closed fait son travail.
"""


def inserer():
    j = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 171 —" in j:
        print("[inserer-171] REJEU REFUSÉ : l'Entrée 171 existe déjà.")
        return 1
    n = j.count(MARQUEUR)
    if n != 1:
        print(f"[inserer-171] ÉCHEC : marqueur {n} fois dans le journal.")
        return 1
    if "## Entrée 170 —" not in j:
        print("[inserer-171] ÉCHEC : l'Entrée 170 est absente (ordre 170<171).")
        return 1
    j = j.replace(MARQUEUR, ENTREE + MARQUEUR)
    JOURNAL.write_text(j, encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 89 —" in w:
        print("[inserer-171] REJEU REFUSÉ : le Task ID 89 existe déjà.")
        return 1
    w = w.rstrip("\n") + "\n" + TASK
    WORKLOG.write_text(w, encoding="utf-8")
    print("[inserer-171] PASSÉ : Entrée 171 insérée avant le marqueur ; worklog +Task ID 89.")
    return 0


if __name__ == "__main__":
    sys.exit(inserer())
