#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_174.py — LA CONSIGNATION DU GESTE « LE CHANTIER M9-(b)
CONTINUE : LA FAMILLE enregistrement NOTÉE-MESURÉE-PROUVÉE » : JOURNAL_TRAVAIL
+Entrée 174 (ordre 173<174<marqueur, rejeu REFUSÉ), worklog +Task ID 92.
Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 174 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE enregistrement NOTÉE-MESURÉE-PROUVÉE — tls13-20/21 (l'enregistrement protéger, l'enregistrement déprotéger — RFC 8446 § 5.2/§ 5.3 : le texte interne charge || type, le nonce = IV ⊕ séquence, l'AAD = l'en-tête, LE TRANSFERT RFC 8448 EN CHAÎNES et L'ANTI-REJOUE) : la notation à la main (349/403 o, round-trip 100 %, les slots ARRÊTÉS 0x180/0x1C0 tassés depuis 0xE9C0 — fin de famille 0xED00, D161 rejoué), LE HARNAIS 48 contrôles · 48 VERTS × 3 graines (LES QUATRE CHAÎNES du transcript protégées ET déprotégées octet pour octet, LA REJOUE refusée ×4, le verdict -3 PROPAGÉ à la borne du protocole, LA VERSION héritage ignorée par la logique mais couverte par l'AAD, le verdict temps constant mesuré) ; UN DÉFAUT DE NOTATION nommé par la sonde du geste (le verdict 32 bits) (07/11)

**La reprise SUR LES TROIS MIROIRS (D164 rejouée — la demande du développeur : « on enchaine »).** La vérification LECTURE SEULE par script (scripts/verify_sync_m9e.py du labo, 16 VERTS / 0 ROUGES) : HEAD == 6dbd7db (la passation Task 91), l'arbre PROPRE, le worklog porte la passation D141 consignée, le miroir TRIADE-sauvegarde-git/ porte les fichiers du geste aead + la passation md5 MATCH (le harnais_aead, les notations aead, passe_bundle_m9d.py, worklog), le bundle courant triade-history-090-0774e55.bundle UNIQUE, archives-bundles/ relues : 35 archives (rien supprimé), /test sans copie, GitHub == 0774e55 (LA POINTE du geste aead — le commit de passation 6dbd7db EMBARQUÉ au geste présent, le flux établi), le jeton OAuth vivant. La réserve instrumentale D149 re-vérifiée AVANT usage : LE DISQUE LABO RECYCLÉ ENCORE (capstone/keystone/unicorn/pynacl/pefile emportés) — RÉINSTALLÉS PAR PROCÉDURE (le constat rejoué).

**LA DÉRIVATION PAR CODE d'abord (scripts/derive_enregistrement.py — le juge est le code).** La référence : la couche enregistrement RFC 8446 § 5.2 sur la référence GCM du labo aead (le texte interne = charge || type, BOURRE LONGUEUR ZÉRO le choix minimal ; le nonce = IV ⊕ séquence, le u64 GROS-BOUTISTE sur les octets 4..11 ; l'AAD = l'en-tête 23/0x0303/N+17 u16 gros-boutiste). LES QUATRE CHAÎNES du transcript : chaque contexte de trafic consomme ses séquences 0, 1, 2… — le serveur (S_HS : le vol de 679 o ; S_AP : le NewSessionTicket, les applicatives, la close_notify aux séquences 0/1/2) et le client (C_HS : le Finished ; C_AP : les applicatives et la close_notify aux séquences 0/1) — chaque enregistrement du § 3 PROTÉGÉ en chaîne == le transcript octet pour octet, DÉPROTÉGÉ en chaîne, ET LA REJOUE refusée. LES CONTRE-PREUVES : la borne (N = 2^14−1 scellé : le texte interne 2^14 == la borne de la brique ; N = 2^14 : le texte interne 2^14+1 HORS brique → le verdict -3 PROPAGÉ nommé, la fragmentation à l'appelant), LA VERSION héritage (IGNORÉE par la logique, COUVERTE par l'AAD : la mutation → refus), L'ORDRE (la séquence avance après le succès, JAMAIS après l'échec). LA FAUTE DE CONSTANTE nommée par la dérivation elle-même : le payload du Finished client copié AVEC son octet de type (37 o → l'en-tête dérivée 0x36 ≠ le transcript 0x35) — corrigé 36 o SANS le type : LE JUGE EST LE CODE, la faute d'instrument attrapée AVANT la notation.

**La notation (les deux brouillons msx64 → les deux notations explicites WYSIWYG).** tls13-20 (h100020, protéger) 349 o · 76 instructions — LE CONTEXTE (200 o, la disposition DÉCLARÉE par la spec : clés de tour @+0 [176], IV @+176 [12], réserve @+188 [4], séquence u64 @+192 [8] — posé par l'APPELANT, tls13-24 le posera au geste qui le dérivera), LE CADRE NOMMÉ 0x4078 (l'ombre de 18, les QUATRE args de pile, le nonce local, l'en-tête LOCALE, la sortie et le contexte SAUVÉS, LE TEXTE INTERNE jusqu'à 2^14+1 SUR LA PILE — la pile du domaine dimensionnée par l'appelant), l'en-tête LOCALE (CINQ octets FIXES : 23 opaque, 0x0303 héritage, N+17 u16 gros-boutiste — copiée à la sortie APRÈS le succès : le fail-closed de la famille, le -3 n'écrit RIEN), le nonce (le IV COPIÉ en local, la séquence XORée GROS-BOUTISTE sur les octets 4..11 — le contexte JAMAIS réécrit sur son IV), le texte interne (la charge recopiée PUIS le type au DERNIER octet — le type une VALEUR pas un pointeur : AUCUN test de nul sur rdx), UNE composition TLS18, L'ORDRE NOMMÉ (l'incrémentation SUIT le scellement — un échec n'avance JAMAIS), les refus -1 (les pointeurs : le contexte, la charge si N > 0, la sortie), -2 (N > 2^14), -3 (LE VERDICT PROPAGÉ de 18 : N = 2^14 porte le texte interne à 2^14+1, HORS la brique — le maximal du protocole REFUSÉ par la composition, la fragmentation à l'APPELANT, RFC 8446 § 5.1 le choix libre), L'INDIFFÉRENCE (N = 0 : le pointeur de charge nul n'est PAS un refus — le couple longueur/pointeur). tls13-21 (h100021, déprotéger) 403 o · 86 instructions — l'en-tête CONFRONTÉE AVANT TOUT (I2 : les verdicts -1/-2 précèdent le -4) : le type reçu == 23 (le protégé est TOUJOURS opaque → -1), la longueur DÉCLARÉE == reçue (l'épuisement exact → -2), les bornes structurelles (le total ≥ 5+18 ; L ≥ 18 le minimum P2 [au minimum le type interne et l'étiquette] ; L ≤ 2^14+16 LA BORNE DE LA BRIQUE — 19 ne peut plus refuser sur les longueurs), LA VERSION HÉRITAGE IGNORÉE (RFC 8446 § 5.1 « MUST be ignored for all purposes » — la spec ne promet pas ce que le protocole n'exige pas ; les octets version restent couverts par l'AAD), l'AAD = l'en-tête REÇUE TELLE QUELLE (l'authentification couvre les octets reçus), UNE composition TLS19, LE TYPE = LE DERNIER OCTET du texte interne déverrouillé dans le tampon LOCAL (la sortie P4 n'a que L−17 o), LA RESTITUTION DERNIÈRE (le -4 : la charge et le type INTACTS, la séquence ne bouge pas), L'ORDRE (le succès : la séquence incrémentée).

**L'ARRÊT des slots (D161 rejoué — la mesure auteur décide).** Le MINIMUM admissible par longueur (multiple de 64, padding ≥ 16, tassés depuis la fin aead 0xE9C0) : tls13-20 @0xE9C0 (slot 0x180, padding 35) · tls13-21 @0xEB40 (0x1C0, 45) — **fin de la famille enregistrement à 0xED00** (la marge : la famille poignée [tls13-23..28, six blocs] sous 0xF000 — 0x300 o restants, la mesure décidera). Le ré-arrêt en cours de geste : 20 préfiguré 343 o mesuré **349 o** (le défaut de la sonde corrigé : les verdicts 32 bits → 64 bits), 21 préfiguré 395 mesuré **403** — les slots TIENNENT, la chaîne ne bouge pas.

**LA SONDE DU GESTE (scripts/sonde_enregistrement.py — le fail-closed AVANT le harnais : la méthode du geste aead rejouée, la sonde d'abord, le harnais ensuite) : 25/25 VERTS APRÈS la correction — 7/25 avant : LA PREUVE A CORRIGÉ LA NOTATION, QUATRIÈME GESTE DE SUITE.** LE DÉFAUT : **les verdicts en eax 32 bits** — `mov eax, -1` laisse le HAUT de rax à ZÉRO : l'appelant lit 4294967295 au lieu de −1 ; la famille aead rend ses verdicts par `mov rax, -N` (le 64 bits signé) : les SEPT verdicts de 20/21 corrigés (3 + 4), re-mesuré 343→349 et 395→403, les slots TIENNENT, REJOUÉ VERT. Les fautes d'INSTRUMENT nommées par la sonde : la composition incomplètement chargée (16/17 non posés : les zéros @0xdf00 lisaient [rax=0] — le crochet de faute l'a nommée : LA COMPOSITION SE CHARGE ENTIÈRE) ; la séquence python jamais réavancée entre les appels (le bloc avance SA séquence, la sonde réécrivait seq 0 : la relecture après CHAQUE appel).

**Le harnais (tls13/harnais_enregistrement.py — le modèle harnais_aead : LA RÉFÉRENCE GCM IMPORTÉE de la lignée [harnais_aead — la source unique : la référence AES+GHASH+GCM contre-preuvée ET les constantes du transfert TRANSFERT_8448 consignées], l'émulation nue aux RVA du plan, les VINGT-ET-UN blocs posés, l'appelant factice msx64 aux sentinelles et canaris, LA ZONE MORTE PROFONDE DÉPLACÉE à −0x5000 [sous le cadre NOMMÉ 0x4078 — la leçon : −0x1000 était INSIDE, le record layer descend à 0x4160]).** 48 contrôles · 48 VERTS × 3 graines (20261107, 41, 20261108) : V0 les pièces (le scellé relu, les DIX-NEUF notations précédentes INTACTES, LE CONTEXTE 200 o posé à la disposition DÉCLARÉE, l'arbre I relu VERT) ; V1 le round-trip 100 % (349/403 o, 76/86 instructions) + les concordances (20 → TLS18 UNE composition, 21 → TLS19 ; l'en-tête CINQ octets fixes ; le nonce aux offset 176/184/192 + bswap ; les bornes 0x4000/23/18/16400 ; AUCUN déplacement RIP — la famille autoporteur) + le temps constant STRUCTUREL (20 exactement SEPT sauts, 21 exactement ONZE, TOUS sur les données publiques — l'en-tête reçue est une MÉTADONNÉE de protocole, la charge et le chiffré ne touchent JAMAIS une branche) ; V2 **LE TRANSFERT RFC 8448 EN CHAÎNES** (LES QUATRE contextes de trafic consommés en séquence : chaque enregistrement du § 3 PROTÉGÉ par 20 == le transcript OCTET POUR OCTET [le nonce = IV ⊕ séquence, les séquences 0..N successives], PUIS DÉPROTÉGÉ par 21 [les charges ET les types], ET LA REJOUE REFUSÉE ×4 [l'enregistrement consommé rejoué → −4, la sortie INTACTE : L'ANTI-REJOUE DU PROTOCOLE tient dans la cryptographie, pas dans un compteur de logique] + l'oracle 60+60 ZÉRO écart) ; V3 les punitifs (**LA BORNE** : N = 2^14−1 scellé puis ouvert — le texte interne 2^14 == EXACTEMENT la borne de la brique ; N = 2^14 → le -3 PROPAGÉ NOMMÉ, la sortie VIERGE, la séquence INCHANGÉE [le maximal du protocole refusé par la composition, la fragmentation à l'APPELANT] ; N = 2^14+1 → −2 ; le type PASSE-PLAT 21/22/23 ; L'INDIFFÉRENCE : N = 0 avec la charge NULLE — l'alerte vide scellée en 22 o, pas un refus ; les refus −1 [les pointeurs] ; les confrontations de l'en-tête : le type → −1, la longueur → −2, **LA VERSION HÉRITAGE MUTÉE → −4** ; L'ORDRE : la séquence 7 → 8 au succès, FIGÉE à 7 sur le −3 ET le −4) ; V4 le contrat (les non-volatiles, la pile, la zone morte profonde, l'alignement à 2 entrées de callee [TLS18 ×1 par 20, TLS19 ×1 par 21], la charge ET l'enregistrement reçus INTACTS, **LE CONTEXTE RÉÉCRIT SUR SA SÉQUENCE SEULE** [les 192 premiers octets OCTET-IDENTIQUES, la séquence seule avancée 41 → 42], les sorties jamais dépassées, les refus SANS corruption) ; V5 la falsification ZÉRO SILENCE (la charge/le type/LA SÉQUENCE mutés → l'enregistrement diverge 6/6 ; le chiffré et l'étiquette mutés → −4 6/6 ; l'en-tête mutée : l'octet type → −1, les octets longueur → −2, **LES OCTETS VERSION → −4 — la logique les ignore, l'AAD les couvre : la cryptographie attrape ce que la logique ignore** 5/5 ; la rejoue attrapée ; la comparaison non muette) ; V6 le temps constant MESURÉ (le scellage 2× → 12 963 instructions EXACTEMENT ; le déscellage conforme 2× → 13 029 ; **LE VERDICT : trois enregistrements divergents — le chiffré muté au premier/milieu/dernier octet — 11 800 instructions LE MÊME COMPTE : la position de la divergence INVISIBLE dans le temps**).

**Détail.** FRONTIÈRES : aucune balise ne bouge, AUCUN build (le chantier (e) attend — le garde VERT), l'arbre scellé tls13/I INTACT (verifier_specs_m9a relu VERT au harnais V0 APRÈS le geste — R2 tenue), m8/proxy.exe INTACT (relu en V0.a), les familles sha, hkdf, x25519 ET aead intactes (relues aux longueurs arrêtées en V0.b), AUCUNE règle modifiée, la charte § 2 tenue (le transcript officiel AVANT usage — la dérivation croisée, la falsification), la charte § 3 tenue (le temps constant NOMMÉ par bloc, structurel ET mesuré — le verdict compris). Livrables : tls13/layout.py (la famille enregistrement ARRÊTÉE + A_PROTEGER/A_DEPROTEGER + TLS18/TLS19 aux SYMBOLES de l'auteur), tls13/outils/auteur.py (les 21 blocs, h100020/h100021 + les NOMS_COURTS), tls13/notation/ (2 brouillons + 2 notations explicites), tls13/harnais_enregistrement.py (48 contrôles VERTS × 3 graines) ; le labo : scripts/derive_enregistrement.py (la dérivation — TOUT VERT), scripts/sonde_enregistrement.py (la sonde 25/25), scripts/mesurer_enregistrement.py (la mesure D161), scripts/verify_sync_m9e.py (la reprise D164). Consignations : la présente Entrée PAR SCRIPT, PLAN (chantier (b) : la famille enregistrement + État du programme), worklog +Task ID 92.

- SUITE : LE CHANTIER M9-(b) CONTINUE — la famille poignée (tls13-23..28 : ServerHello traiter, le calendrier des clés — LE CONTEXTE posé par tls13-24, Finished calculer/vérifier, l'épinglage, la machine d'états — LE TRANSFERT RFC 8448 EN BOUT EN BOUT, de l'enregistrement au Finished), les slots à la suite de 0xED00 (la marge : 0x300 o, la mesure décidera) ; puis (d) le socle socket sys-04+, (e) LA CÉRÉMONIE DE L'ÈRE + le build 1.0.0-dev.1, (f) le terrain — LA GRANDE ŒUVRE.

"""

TASK = """

## Task ID 92 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE enregistrement NOTÉE-MESURÉE-PROUVÉE (07/11)

- LA SYNCHRO VÉRIFIÉE SUR LES TROIS MIROIRS (« on enchaine ») :
  verify_sync_m9e.py 16 VERTS / 0 ROUGES — HEAD 6dbd7db (la passation
  Task 91), l'arbre propre, le bundle courant 090-0774e55 UNIQUE, 35
  archives, /test sans copie, GitHub == 0774e55 (la pointe aead), le
  jeton OAuth vivant ; la réserve instrumentale RÉINSTALLÉE (le disque
  labo recyclé ENCORE : capstone/keystone/unicorn/nacl/pefile).
- LE GESTE : tls13-20/21 — l'enregistrement protéger (le contexte 200 o
  à la disposition DÉCLARÉE, le cadre NOMMÉ 0x4078 : le texte interne
  jusqu'à 2^14+1 sur la pile, l'en-tête LOCALE cinq octets fixes copiée
  à la sortie APRÈS le succès — le fail-closed : le refus n'écrit
  RIEN ; le nonce = IV ⊕ séquence GROS-BOUTISTE, le contexte jamais
  réécrit sur son IV ; le type au DERNIER octet du texte interne ;
  l'incrémentation SUIT le scellement ; le verdict -3 PROPAGÉ de 18 :
  N = 2^14 porte le texte interne à 2^14+1, HORS la brique — le
  maximal du protocole refusé par la composition, la fragmentation à
  l'appelant) et l'enregistrement déprotéger (l'en-tête confrontée
  AVANT TOUT : le type → -1, la longueur déclarée == reçue et les
  bornes 18..2^14+16 → -2, LA VERSION héritage IGNORÉE par la logique
  mais COUVERTE par l'AAD ; l'AAD = l'en-tête reçue telle quelle ; le
  type = le DERNIER octet déverrouillé dans le tampon local ; la
  restitution DERNIÈRE ; la séquence n'avance JAMAIS sur l'échec) —
  notés (349/403 o, round-trip 100 %), mesurés (les slots ARRÊTÉS
  0x180/0x1C0 depuis 0xE9C0, fin 0xED00 — D161 rejoué), prouvés (LE
  HARNAIS 48 contrôles · 48 VERTS × 3 graines).
- LES PREUVES : LE TRANSFERT RFC 8448 EN CHAÎNES — les QUATRE
  contextes de trafic consommés en séquence : chaque enregistrement du
  § 3 PROTÉGÉ par 20 == le transcript OCTET POUR OCTET, PUIS
  DÉPROTÉGÉ par 21 (les charges ET les types), ET LA REJOUE REFUSÉE
  ×4 (l'anti-rejoue tient dans la cryptographie, pas dans un compteur
  de logique) ; l'oracle 60+60 ZÉRO écart ; LA BORNE (N = 2^14−1
  scellé/ouvert — le texte interne 2^14 == la borne de la brique ;
  N = 2^14 → le -3 PROPAGÉ, la sortie VIERGE ; N = 2^14+1 → -2) ; le
  type passe-plat 21/22/23 ; l'indifférence (N = 0 : la charge nulle
  n'est pas un refus) ; LA VERSION héritage mutée → -4 (l'AAD couvre
  ce que la logique ignore — RFC 8446 § 5.1 « MUST be ignored ») ;
  L'ORDRE (7 → 8 au succès, FIGÉE sur le -3 et le -4) ; le contrat
  (le contexte réécrit SUR SA SÉQUENCE SEULE — les 192 premiers
  octets OCTET-IDENTIQUES ; l'alignement aux 2 entrées de callee ;
  les refus SANS corruption) ; la falsification (17/17 attrapées) ;
  le temps constant MESURÉ (12 963/13 029/11 800 instructions — LE
  VERDICT : la position de la divergence INVISIBLE dans le temps).
- LE DÉFAUT DE NOTATION nommé par LA SONDE du geste (la méthode du
  geste aead rejouée : la sonde d'abord, le harnais ensuite) : les
  verdicts en eax 32 bits — le HAUT de rax à ZÉRO, l'appelant lit
  4294967295 au lieu de −1 ; corrigé en mov rax, -N (le 64 bits
  signé de la famille), re-mesuré 343→349 et 395→403, les slots
  TIENNENT, REJOUÉ VERT (25/25). Les fautes d'instrument : la
  composition incomplètement chargée (16/17 non posés — le crochet
  de faute l'a nommée), la séquence python jamais réavancée (la
  relecture après CHAQUE appel). La faute de CONSTANTE nommée par la
  dérivation : le payload du Finished copié AVEC son type (0x36 ≠
  0x35) — le juge est le code, corrigé AVANT la notation.
- FRONTIÈRES : aucune balise, AUCUN build, l'arbre scellé tls13/I
  INTACT (verifier_specs_m9a relu VERT au harnais V0), m8/proxy.exe
  INTACT, les familles sha/hkdf/x25519/aead intactes (relues en V0.b) ;
  consignations : Entrée 174 PAR SCRIPT, PLAN (chantier (b) : la
  famille enregistrement + État du programme), worklog +Task ID 92.
- SUITE : la famille poignée (tls13-23..28 — ServerHello, le
  calendrier des clés [LE CONTEXTE posé par tls13-24], Finished,
  l'épinglage, la machine d'états : LE TRANSFERT RFC 8448 en bout en
  bout), les slots à la suite de 0xED00 (la marge : 0x300 o, la
  mesure décidera) ; puis (d) sys-04+, (e) LA CÉRÉMONIE + le build
  1.0.0-dev.1, (f) le terrain.

Stage Summary:
- LA CINQUIÈME FAMILLE de la grande œuvre est notée-mesurée-prouvée :
  LA COUCHE ENREGISTREMENT de TLS 1.3 existe en octets — les SEPT
  enregistrements du transcript officiel RFC 8448 PROTÉGÉS et
  DÉPROTÉGÉS en chaînes par les briques mêmes, l'anti-rejoue tenu par
  la cryptographie, la borne du protocole nommée (le -3 propagé), la
  version héritage couverte par l'AAD quand la logique l'ignore.
- LA MÉTHODE TIENT : la dérivation (qui a nommé SA PROPRE faute de
  constante), la sonde (qui a nommé le verdict 32 bits), le harnais
  (qui a nommé ses fautes d'instrument) — le fail-closed QUATRIÈME
  geste de suite, la preuve corrige la notation, l'instrument se
  prouve non-vide.
"""

def inserer():
    j = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 174 —" in j:
        print("[inserer-174] REJEU REFUSÉ : l'Entrée 174 existe déjà.")
        return 1
    n = j.count(MARQUEUR)
    if n != 1:
        print(f"[inserer-174] ÉCHEC : marqueur {n} fois dans le journal.")
        return 1
    if "## Entrée 173 —" not in j:
        print("[inserer-174] ÉCHEC : l'Entrée 173 est absente (ordre 173<174).")
        return 1
    j = j.replace(MARQUEUR, ENTREE + MARQUEUR)
    JOURNAL.write_text(j, encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 92 —" in w:
        print("[inserer-174] REJEU REFUSÉ : le Task ID 92 existe déjà.")
        return 1
    w = w.rstrip("\n") + "\n" + TASK
    WORKLOG.write_text(w, encoding="utf-8")
    print("[inserer-174] PASSÉ : Entrée 174 insérée avant le marqueur ; worklog +Task ID 92.")
    return 0


if __name__ == "__main__":
    sys.exit(inserer())
