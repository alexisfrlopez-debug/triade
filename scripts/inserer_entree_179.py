#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_179.py — LA CONSIGNATION DU GESTE « L'ERRATUM n° 5 (la
sonde terrain : l'octet du record CH + le CCS hérité + les verdicts 64
bits) NOMMÉ AVANT LE TERRAIN, RÉPARÉ À LA SOURCE ; LE BUILD 1.0.0-dev.2
NÉ, la carte GÉNÉRATION 10 ; LE KIT TERRAIN M9-(f) ASSEMBLÉ, ÉPROUVÉ ET
DÉPOSÉ AU COFFRE /test » : JOURNAL_TRAVAIL +Entrée 179 (ordre
178<179<marqueur, rejeu REFUSÉ), worklog +Task ID 97. Tout ancrage
absent = ÉCHEC NOMMÉ, rien n'est écrit.

La datation : la présente porte le 06/11 (le geste du développeur
« Prépare le kit terrain » reçu le 06/11 ; les horodatages du build et
du dépôt : 06/11 — l'heure locale du labo)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 179 — L'ERRATUM n° 5 (la sonde terrain du labo : l'octet de longueur du record CH, le CCS hérité, les verdicts 64 bits) NOMMÉ AVANT LE KIT et RÉPARÉ À LA SOURCE ; LE BUILD 1.0.0-dev.2 NÉ, la carte GÉNÉRATION 10, le verrou croisé 86/86 ; LE KIT TERRAIN M9-(f) ASSEMBLÉ, ÉPROUVÉ ET DÉPOSÉ AU COFFRE /test — LA GRANDE ŒUVRE ATTEND LE GESTE DU DÉVELOPPEUR (06/11)

**La préparation du kit EST une sonde — la doctrine a tenu encore (le modèle n° 4 : le défaut nommé AVANT le terrain, le geste du développeur épargné).** La sonde du labo (scripts/sonde_erratum_ch_record.py, la pièce rejouable : le CH de 114 o composé par la construction re-jouée du plan, les DEUX vols exacts) : le vol DE L'ARTEFACT dev.1 (`16 03 03 00 76` + 114 o : la longueur DÉCLARÉE 118 pour un vol de 119 = 5 + 114 — le brouillon tls13-27 se contredisant LUI-MÊME, la spec scellée disait juste : « 5 o : type 22, 0x0303, 114 ») reçoit **LE SILENCE de google, github, cloudflare et debian TOUS** (le serveur attend 4 octets jamais émis — l'interblocage PROUVÉ sur pièces) ; le vol corrigé (`00 72`) reçoit **LE SERVERHELLO des QUATRE** — dev.1 ne pouvait franchir AUCUN serveur réel, jamais. LE SECOND CONSTAT (la même sonde, la carte du run) : les serveurs réels émettent TOUS l'enregistrement CCS de compatibilité (`14 03 03 00 01 01`) ENTRE leur ServerHello et leur vol protégé — RFC 8446 § 4.1.3 (« un client DOIT ignorer les change_cipher_spec reçus pendant la poignée »), la machine dev.1 exigeait le type 23 STRICT : elle en mourrait -3 contre le monde réel. LE TROISIÈME (la conception du kit) : les verdicts internes de 27 s'écrivaient `mov eax, -N` — zéro-étendus, un kit 64 bits aurait lu +4294967293 au lieu de -3 (la convention de la lignée est `mov rax, -N` : sys-02/03/04 TOUS la tiennent).

**Le client de référence du labo (scripts/sonde_cible_terrain.py — le juge de la cible).** UN client TLS 1.3 EN PYTHON PUR rejouant NOTRE offre scellée exacte (le calendrier AUTO-TESTÉ sur les pièces consignées RFC 8448 : c_hs/s_hs/c_ap/s_ap + le Finished serveur, les hash du RFC en ARGUMENTS — la méthode du harnais) : **LES QUATRE SESSIONS RÉELLES TIENNENT DE BOUT EN BOUT** (la poignée entière, le certificat extrait, la ligne applicative reçue) contre google/github/cloudflare/debian — google servant sans SNI le certificat intentionnel `CN=invalid2.invalid` (« No SNI provided - please fix your client »), github son `*.github.com` (Sectigo, RSA-4096), debian un 421 (sans SNI), cloudflare **LE VRAI certificat `CN=www.cloudflare.com` (Let's Encrypt YR2, RSA-2048, émis 2026-11-01, VALIDE → 2027-01-30)** avec le témoin « HTTP/1.1 200 OK » STABLE. **LA CIBLE FIGÉE au labo** : www.cloudflare.com:443 — l'empreinte épinglée (sha256 du DER de la PREMIÈRE entrée, le DÉTROIT de tls13-26) `045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f`, **TROIS sessions consécutives, empreinte IDENTIQUE de bout en bout** — un vrai certificat d'une vraie autorité, la cible la plus orthodoxe du lot (l'erratum d'extraction consigné au passage : le message Certificate porte `ctx u8` AVANT la liste — le DER à l'offset message 11, la machine avait raison, `DER_8448 = CERT_8448[11:11+432]`).

**La réparation À LA SOURCE (le miroir exact de l'erratum n° 4 — les arbres I HORS du sceau, INTACTS : la spec disait 114, la notation seule était fautive).** (1) `mov byte ptr [r10 + 4], 0x76` → `0x72` (brouillon + notation) ; (2) LE BLOC CCS à la queue des rejets : `.pr_ccs_ou_mort` — le type 20 lu, la longueur déclarée EXIGÉE == 1 (un faux « CCS » est le refus -2 NOMMÉ, jamais un aval aveugle), la charge héritage D'UN octet lue au socle SANS déverrouillage (AUCUNE séquence consommée, AUCUNE clé touchée, le transcript INTACT), la boucle protégée REPREND ; (3) LES TROIS VERDICTS EN 64 BITS (`mov rax, -3` l'alerte inconnue d'É3, `-3` l'état hors ligne, `-2` la taille hors borne — la frontière du kit, Q3 de tls13-28) ; LE SUIVANT DU PLAN : tls13/layout.py — le slot de 27 ré-arrêté 0xB80 → **0xBC0** (2975 o de code, padding 33 — D8 : ≥ 16, aligné 16, multiple de 64), **TLS28_VA 0x10AC0 → 0x10D00** (LA RÉSERVE INT3 après les fixtures [0x10D00, 0x10FFF) : la zone fixtures 0x10B80..0x10CF0 INTACTE, les 26 autres blocs BYTE-IDENTIQUES — seuls 27 [code + le onzième appel TLS28] et l'adresse de 28 bougent), VERSION_DEV 0x01000001 → **0x01000002** (dev.2 — le premier build dev.1 demeure, vendu par sa propre Entrée). LE HARNAIS CORRIGÉ ENSEMBLE (machine et référence ne divergent JAMAIS) : `ch_rec = 16 03 03 00 72` (la référence avait codifié le même 0x76 — le simulateur ne parse pas la longueur, la faute dormait verte), **V7.h LE CCS HÉRITÉ AVALÉ** (le record servi ENTRE le SH et le vol : la session s'établit, le journal INTACT, la réception POIGNÉE aux séquences 0/1 — AUCUN octet de séquence consommé) et **V7.i LE FAUX CCS REFUSÉ** (longueur 2 → -2 NOMMÉ, l'état 5, le journal == l'offre seule) ; LA SENTINELLE DU HARNAIS DÉPLACÉE (RET_MAGIQUE 0x10D00 → **0x10E00** : l'émulateur rentrait EN COLLISION avec le socle déplacé — nommé, la sentinelle suit) ; les pins du plan (2975 o, TLS28 ×11) et verifier_specs_m9a (dev.2) suivis.

**Le build re-exécuté — 1.0.0-dev.2 NÉ (tls13/build_m9.py + tls13/carte_m9.py).** LA CHAÎNE ENTIÈRE REJOUÉE VERTE : le garde sceau-I 13/13 AVANT construire() (les TREIZE arbres I INTACTS — l'erratum n° 5 touche layout + notations, HORS du sceau), l'ancre 0.9.0 confrontée OCTET PAR OCTET, les 28 blocs round-trip 100 %, l'oracle structurel 589 verrous (AUCUN IAT, AUCUN site syscall, les appels fermés — le onzième appel de 27 au plan 0x10D00, LES SLOTS DISJOINTS, la composition intégrale : chaque octet de .text6 compté), les oracles M4 560 + M5 365 + sys 131 verts ; L'ARTEFACT : **tls13/proxy.exe 1.0.0-dev.2, 65 024 o, sha256 d892893469608fd69e381b92b8e18623107bd2bc694f43a512bc5900773dc314** — DÉTERMINISTE (deux exécutions du build, octets IDENTIUX) ; les octets réparés RELUS DANS L'IMAGE : `41 C7 02 16 03 03 00 41 C6 42 04 72` @RVA 0x10082, le bloc CCS `41 80 3A 14 …` présent, l'ancien 0x76 ABSENT ; LA CARTE GÉNÉRATION 10 (GENERATION 10, version=1.0.0-dev.2, les étiquettes de fragments « generation=10 », les zones « socle-28=0x10d00-0x10daf » — l'incohérence de génération des fragments du premier jet nommée et réparée au geste), la lignée D80 + la graine durable D144 tenues (LA RELÈVE : coffre_fort.bin + obtenir lignee-D80/graine-ed25519-cartes → .keys/, LE TÉMOIN pub e9cd8c549485… TENU), le verrou croisé **86/86** + le tableau de bord. **Le harnais poignée 54/54 VERTS × 3 graines** (20261107/41/20261108 — les 52 + les DEUX nouveaux contrôles CCS).

**LE KIT TERRAIN M9-(f) ASSEMBLÉ, ÉPROUVÉ, DÉPOSÉ (LA GRANDE ŒUVRE ATTEND).** LE SCÉNARIO (tls13/terrain/scenario-m9f.py — python SEUL : ctypes/hashlib/os/platform/socket/struct/sys/threading/time) : T0 LE TÉMOIN (l'empreinte assertée, le VRAI ntdll localisé + haché, la cartographie DONT_RESOLVE, les octets constatés UN PAR UN — **dont l'OCTET 0x72 DE L'ERRATUM n° 5 relu dans l'image** @0x10082, le trombone, le device AFD, les spans NT — la cible résolue par DNS, l'empreinte épinglée consignée) ; T1 LA RÉSOLUTION (les DEUX lecteurs : la marche EAT en Python + sys-02 à son adresse scellée, LE MÊME SSN pour NtCreateFile/NtDeviceIoControlFile/NtClose, le motif du stub confronté) ; T2 L'ÉTABLISSEMENT (sys-04 : create+bind+connect, TROIS appels NT, chaque SSN résolu AU GESTE MÊME — le VRAI afd.sys, zéro ws2_32) ; T3 LA SESSION (tls13-27 OUVRIR, le socle 28 câblé aux rappels DU KIT → sys-05/sys-06, le kit 96 o : aléa + couple + EMPREINTE ÉPINGLÉE ; LE RECOUP : le CH émis == la construction re-jouée en Python pur — l'aléa @+6, la clé publique @+82 == l'échelle RFC 7748 refaite en Python : les DEUX lecteurs encore) ; T4 LA LIGNE (É2 le GET scellé PAR LA MACHINE, É3 la réponse DÉCHIFFRÉE PAR LA MACHINE, le témoin « HTTP/1.1 200 OK » dans le flux restitué) ; T5 LA FALSIFICATION CONTRE LE VRAI SERVEUR (l'empreinte mutée d'un bit → -6 NOMMÉ, l'état 5, le journal == l'offre seule — la confiance est une COMPARAISON) ; T6 LA CLÔTURE (É4 le close_notify 24 o de la machine ; NtClose ÉMIS PAR SYS-01 par un trampoline à deux instructions — mov rax, ssn ; jmp sys-01 : ctypes ne charge pas rax, le trampoline le fait, LE GESTE DU KIT I8) ; la garde-chien 300 s (un transport muet est une information). LE LISEZMOI (LISEZMOI-KIT-M9F.md : POURQUOI dev.2 — l'erratum n° 5 raconté —, le geste en trois temps, les frontières nommées : le certificat servi SANS SNI + la rotation Let's Encrypt [un -6 honnête vaut un re-gel], le socle socket courant POUR LA PREMIÈRE FOIS sur le VRAI afd.sys, la limite rdx/ctypes nommée). L'ASSEMBLAGE (scripts/assembler_kit_m9f.py) : **26 constantes recoupées PAR AST contre l'artefact/le plan/la sonde** (dont l'octet 0x72 relu DANS L'IMAGE, le device AFD dérivé du nom, l'empreinte épinglée == la pièce de la sonde, SESSION_TAILLE 17520 == le plan), py_compile VERT, l'extraction vierge VÉRIFIÉE — **kit-m9f.zip (34 759 o, md5 a73fb526…, sha256 5f30b34e…)**. LE DÉPÔT (scripts/deposer_kit_m9f.py) : la vague m8d CONSOMMÉE archivée → /test/archives-livraisons/vagues-m8/ (kit-m8d.zip + LISEZMOI-m8d.txt, déplacement PATCH, md5 recoupés après), **preuves-m9f/ NÉ** avec son LISEZMOI-preuves.txt, **kit-m9f.zip + LISEZMOI-m9f.txt DÉPOSÉS à la racine du /test** (md5 MATCH par relecture), l'index mis à jour, la racine vérifiée (13 entrées : la vague courante + les résidents + les réceptacles + les salles d'archive).

**Détail.** FRONTIÈRES : le scellé 0.9.0 INTACT (relu par la confrontation du build), la carte génération 8 scellée INTACTE, **les arbres I INCHANGÉS** (l'erratum n° 5 touche layout + notations + instruments : HORS du sceau — le garde 13/13 VERT re-passé par le build même), AUCUNE balise posée (dev.2 = un geste de BUILD ; **la finale 1.0.0 attend le terrain vert du (f) — le scellage sera un fait de carte, D104**), la clé privée JAMAIS traversée (D87 : la relève de la phrase se fait au coffre LOCAL, jamais un secret ne quitte le poste), dev.1 conservé par l'histoire git (vendu par l'Entrée 178, remplacé par dev.2 au même chemin — l'append-only tient). Livrables : scripts/sonde_erratum_ch_record.py + scripts/sonde_cible_terrain.py (les pièces rejouables), tls13/layout.py (dev.2 + le slot 0xBC0 + TLS28_VA 0x10D00), tls13/notation/brouillons+tls13-27 (l'octet, le bloc CCS, les trois verdicts 64 bits, l'en-tête d'erratum), tls13/harnais_poignee.py (la référence 0x72 + V7.h/V7.i + la sentinelle 0x10E00 + les pins 2975/×11), verifier_specs_m9a.py (dev.2), tls13/build_m9.py + tls13/carte_m9.py (les littéraux dev.2, GENERATION 10, les zones), tls13/proxy.exe (1.0.0-dev.2, 65 024 o, sha256 d8928934…), tls13/carte/ (la génération 10), tls13/terrain/scenario-m9f.py + LISEZMOI-KIT-M9F.md, scripts/assembler_kit_m9f.py, scripts/deposer_kit_m9f.py, download/kit-m9f.zip. Consignations : la présente Entrée 179 PAR SCRIPT, PLAN (la rangée (f) + l'État du programme PAR maj_plan_m9j.py), worklog +Task ID 97. SUITE : **LE GESTE DU DÉVELOPPEUR** (dézipper kit-m9f.zip au /test du Drive, `python scenario-m9f.py` sur la machine Windows 11, réseau vivant, ~10 s) → renvoyer preuves-m9f/ au coffre → le labo recoupe sur pièces (D138/D145/D148) → si vert : **LA FINALE 1.0.0** (fait de carte) — le jalon M9 franchi, LA GRANDE ŒUVRE : le client TLS 1.3 ENTIER en blocs scellés, zéro délégation cryptographique."""

TASK = """## Task ID 97 — L'ERRATUM n° 5 (la sonde terrain : l'octet du record CH 0x76→0x72, LE CCS HÉRITÉ, les verdicts 64 bits) NOMMÉ AVANT LE KIT ET RÉPARÉ À LA SOURCE ; LE BUILD 1.0.0-dev.2 NÉ (carte GÉNÉRATION 10, verrou croisé 86/86) ; LE KIT TERRAIN M9-(f) DÉPOSÉ AU COFFRE /test — LA GRANDE ŒUVRE ATTEND LE GESTE DU DÉVELOPPEUR (06/11)

- LA SONDE AVANT LE KIT (la doctrine n° 4 rejouée — le geste du
  développeur épargné) : sonde_erratum_ch_record.py — le vol de
  l'artefact dev.1 (16 03 03 00 76 + 114 : la longueur déclarée 118
  pour 119 = 5 + 114 émis) reçoit LE SILENCE de google/github/
  cloudflare/debian TOUS ; le vol corrigé 0x72 reçoit le ServerHello
  des QUATRE — dev.1 ne pouvait franchir AUCUN serveur réel. SECOND
  CONSTAT : les serveurs réels émettent TOUS le CCS hérité (14 03 03
  00 01 01) entre le SH et le vol — RFC 8446 § 4.1.3 impose de
  l'ignorer ; la machine exigeait le type 23 strict : morte -3 contre
  le monde réel. TROISIÈME (la frontière du kit) : les verdicts
  internes mov eax, -N zéro-étendus — un kit 64 bits lirait
  +4294967293 ; la lignée écrit mov rax (sys-02/03/04 tous).
- LE CLIENT DE RÉFÉRENCE (sonde_cible_terrain.py, python pur, le
  calendrier AUTO-TESTÉ sur les pièces RFC 8448) : les QUATRE sessions
  réelles TIENNENT de bout en bout ; LA CIBLE FIGÉE : www.cloudflare.com
  — LE VRAI certificat CN=www.cloudflare.com (Let's Encrypt YR2,
  RSA-2048, valide → 2027-01-30) servi SANS SNI, l'empreinte épinglée
  045d0758… IDENTIQUE sur 3 sessions consécutives, le témoin
  « HTTP/1.1 200 OK » stable.
- LA RÉPARATION À LA SOURCE (les arbres I HORS du sceau — INTACTS :
  la spec disait 114, la notation seule était fautive ; le garde 13/13
  re-passé VERT) : l'octet 0x72 (brouillon + notation) ; LE BLOC CCS
  (.pr_ccs_ou_mort : type 20, longueur EXIGÉE == 1 — un faux CCS est
  le refus -2 NOMMÉ —, la charge d'UN octet avalée au socle SANS
  déverrouillage, AUCUNE séquence consommée, la boucle reprend) ; LES
  TROIS VERDICTS EN 64 BITS ; LE PLAN : slot de 27 ré-arrêté 0xB80 →
  0xBC0 (2975 o, padding 33), TLS28_VA 0x10AC0 → 0x10D00 (la réserve
  int3 APRÈS les fixtures — la zone fixtures INTACTE, les 26 autres
  blocs byte-identiques), VERSION_DEV 0x01000002. LE HARNAIS corrigé
  ENSEMBLE (machine ET référence) : ch_rec 0x72, V7.h LE CCS AVALÉ
  (session établie, journal intact, séquences 0/1), V7.i LE FAUX CCS
  REFUSÉ (-2), la SENTINELLE RET_MAGIQUE déplacée 0x10D00 → 0x10E00
  (la collision avec le socle déplacé nommée) — 54/54 × 3 graines
  VERTS (20261107/41/20261108).
- LE BUILD 1.0.0-dev.2 NÉ : la chaîne entière verte (l'ancre 0.9.0
  confrontée octet par octet, 589 verrous structurels, M4 560 + M5 365
  + sys 131) ; tls13/proxy.exe 65 024 o, sha256
  d892893469608fd69e381b92b8e18623107bd2bc694f43a512bc5900773dc314,
  DÉTERMINISTE (deux builds, octets identiques) ; les octets réparés
  RELUS DANS L'IMAGE (0x72 @0x10082, le bloc CCS présent, le 0x76
  absent) ; LA CARTE GÉNÉRATION 10 (fragments « generation=10 », zones
  socle-28=0x10d00-0x10daf, la lignée D80 + la graine durable tenues,
  le témoin pub e9cd8c549485…), le verrou croisé 86/86.
- LE KIT TERRAIN DÉPOSÉ (scripts/assembler_kit_m9f.py +
  deposer_kit_m9f.py) : scenario-m9f.py (T0..T6 : le VRAI ntdll par
  les DEUX lecteurs, sys-04/05/06 sur le VRAI afd.sys, tls13-27 OUVRIR
  avec LE RECOUP du CH contre la construction re-jouée en Python pur,
  la ligne chiffrée échangée, la falsification -6 contre le serveur
  réel, le close_notify + NtClose par sys-01 en trampoline) — 26
  constantes recoupées PAR AST (dont l'octet 0x72 relu DANS l'image),
  l'extraction vierge VERT — kit-m9f.zip (34 759 o, md5 a73fb526…,
  sha256 5f30b34e…) DÉPOSÉ à la racine du /test (md5 MATCH relu) avec
  LISEZMOI-m9f.txt ; preuves-m9f/ NÉ avec son LISEZMOI-preuves ; la
  vague m8d CONSOMMÉE archivée → vagues-m8/ ; l'index mis à jour ; la
  racine vérifiée (13 entrées).
- FRONTIÈRES : le scellé 0.9.0 INTACT, la carte gén 8 INTACTE, les
  arbres I INCHANGÉS (l'erratum touche layout + notation + instruments,
  hors sceau), AUCUNE balise (la finale 1.0.0 attend le terrain vert,
  D104), dev.1 conservé par l'histoire git, la clé privée jamais
  traversée (D87).
- SUITE : LE GESTE DU DÉVELOPPEUR — dézipper kit-m9f.zip (au coffre
  /test du Drive), python scenario-m9f.py (Windows 11, réseau vivant,
  ~10 s) → renvoyer preuves-m9f/ au coffre /test/preuves-m9f/ → le
  labo recoupe (D138/D145/D148) → si vert : LA FINALE 1.0.0 (fait de
  carte) — le jalon M9 franchi, LA GRANDE ŒUVRE.

Stage Summary:
- L'ERRATUM n° 5 EST LA PREUVE DE LA MÉTHODE ENCORE : la sonde a
  nommé l'octet 0x76 (le SILENCE des serveurs prouvé sur pièces), le
  CCS hérité (les 4 serveurs constatés) et les verdicts 64 bits AVANT
  le terrain — le kit déposé embarque le build RÉPARÉ et le constat
  de l'octet relu dans l'image.
- LE BUILD 1.0.0-dev.2 EST NÉ : 65 024 o, sha256 d8928934…,
  déterministe, la carte génération 10, le verrou croisé 86/86, le
  harnais 54/54 × 3 graines — la spécification scellée n'a JAMAIS
  bougé (la notation seule était fautive, les arbres I intacts).
- LE KIT TERRAIN M9-(f) EST AU COFFRE /test : la grande œuvre attend
  le geste du développeur — la session réelle, l'épinglage, la ligne
  chiffrée ; si vert : la finale 1.0.0, le jalon M9 franchi."""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 179" in journal:
        sys.exit("ÉCHEC : Entrée 179 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 178" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 178 introuvable")
    if MARQUEUR not in journal:
        sys.exit("ÉCHEC : marqueur introuvable")
    i178 = journal.index("## Entrée 178")
    im = journal.index(MARQUEUR)
    if not (i178 < im):
        sys.exit("ÉCHEC : l'ordre 178<marqueur est rompu")
    if "## Entrée 179" in journal[i178:im]:
        sys.exit("ÉCHEC : état inattendu entre 178 et le marqueur")
    # l'insertion APRÈS la SECTION 178, avant le marqueur (la leçon 175)
    journal = journal[:im] + ENTREE + "\n\n" + journal[im:]
    JOURNAL.write_text(journal, encoding="utf-8")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 97" in worklog:
        sys.exit("ÉCHEC : Task ID 97 déjà consigné (rejeu REFUSÉ)")
    if "## Task ID 96" not in worklog:
        sys.exit("ÉCHEC : ancrage Task ID 96 introuvable")
    worklog = worklog.rstrip("\n") + "\n\n" + TASK + "\n"
    WORKLOG.write_text(worklog, encoding="utf-8")

    print("[consignation] Entrée 179 déposée au journal "
          "(ordre 178<179<marqueur)")
    print("[consignation] Task ID 97 déposé au worklog")
    print("[consignation] la relecture fait foi :")
    j = JOURNAL.read_text(encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    assert j.index("## Entrée 178") < j.index("## Entrée 179") < j.index(MARQUEUR)
    assert "## Entrée 179" in j and "erratum n° 5" in j
    assert "d892893469608fd69e381b92b8e18623107bd2bc694f43a512bc5900773dc314" in j
    assert "045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f" in j
    assert "kit-m9f.zip" in j
    assert "## Task ID 97" in w and w.index("## Task ID 96") < w.index("## Task ID 97")
    print("[consignation] ORDRE et ANCRAGES constatés — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
