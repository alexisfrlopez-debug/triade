#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_m10a.py — LA CONSIGNATION DU CHANTIER M10-(a) RÉALISÉ : « LES
DIX-HUIT SPÉCIFICATIONS POSÉES (la couche I complète du TGN, R2) ; LE PLAN
D'ADRESSAGE loupe/layout.py ARRÊTÉ (la table des verdicts + le cadre +
la ligne + les tables MD5 dérivées par arithmétique + les bornes + les
zones + l'IAT) ; L'HÉRITAGE DÉCLARÉ PAR LA CARTE (utilisé : libc-03
retiré) ; LA TABLE i11xxxx POSÉE AU README ; L'INSTRUMENT
verifier_specs_m10a.py VERT (150 contrôles) » : le plan reçoit la rangée
(a) RÉALISÉE + la phrase de l'État du programme, le journal reçoit
l'Entrée 195, DECISIONS reçoit la D172, le worklog reçoit la Task ID
113. Le garde sceau I (13 arbres VERTS) passe AVANT toute écriture ;
rejeu REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois =
ÉCHEC NOMMÉ, rien n'est écrit. Les ancres État sont importées de
consigner_tgn_d171 (la chaîne des gestes tient sans retranscription)."""
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_tgn_d171 as _c194  # noqa: E402  # la chaîne des gestes

# --- l'État du programme : la phrase du M10-(a) remplace celle de l'ouverture ----

ANCIEN_ETAT = _c194.NOUVEL_ETAT   # l'État 194 (le TGN ouvert, la suite M10-(a))

NOUVEL_ETAT = (
    "**LE CHANTIER M10-(a) RÉALISÉ le 07/11/2026 (Entrée 195, D172, "
    "Task 113) : LES DIX-HUIT SPÉCIFICATIONS POSÉES** — la couche I "
    "complète du TGN « Loupe » (R2 tenue : chaque bloc porté par sa "
    "spécification AVANT tout octet de notation, le gabarit § 2.2 aux "
    "SEPT blocs, chaque exigence reliée à son vecteur) ; le plan "
    "d'adressage loupe/layout.py ARRÊTÉ (la table des SEPT verdicts · "
    "le cadre de session 960 o · la ligne 77 o · les 64 constantes MD5 "
    "DÉRIVÉES PAR ARITHMÉTIQUE · les bornes du périmètre 0.1.0 [2 Gio, "
    "24 lignes, 64 Kio] · les zones .data · l'héritage PAR LA CARTE "
    "[tls13-01..04 + libc-01/02/07 + win-03, chaque entrée citée : "
    "libc-03 RETIRÉ — l'héritage déclaré est l'héritage utilisé] · "
    "l'IAT 34 feuilles) ; la table des identifiants i110001..i110018 "
    "posée au README (la lignée g9 → h10 → i11) ; l'instrument "
    "verifier_specs_m10a.py VERT — 150 contrôles, le juge est le "
    "code. SUITE : M10-(b) LE NOYAU NOTÉ (fichier + empreintes) ; la "
    "cérémonie d'ère du TGN attend son geste (le 14e arbre)**"
)

# --- la rangée (a) du plan : OUVERT → RÉALISÉ ------------------------------------

RANGEE_ANCIENNE = "(a) La couche I complète — **OUVERT (D171)**"
RANGEE_NOUVELLE = ("(a) La couche I complète — **RÉALISÉ (Entrée 195, "
                   "D172)** : les 18 spécifications posées, le plan "
                   "d'adressage et les budgets ARRÊTÉS, l'instrument "
                   "150 contrôles VERT")

# --- la D172 (append à la suite de D171) -----------------------------------------

D172 = """
## D172 — LE CHANTIER M10-(a) RÉALISÉ : LES DIX-HUIT SPÉCIFICATIONS POSÉES (la couche I complète du TGN « Loupe » — R2 tenue : chaque bloc porté par sa spécification AVANT tout octet de notation, le gabarit § 2.2 aux SEPT blocs, chaque exigence reliée à son vecteur) ; LE PLAN D'ADRESSAGE loupe/layout.py ARRÊTÉ AVANT LA NOTATION (D161 rejoué : la table des SEPT verdicts, le cadre de session, le format de ligne, les tables MD5, les bornes, les zones, l'IAT — la préfiguration n'est pas un droit) ; L'HÉRITAGE DÉCLARÉ PAR LA CARTE EST L'HÉRITAGE UTILISÉ (tls13-01..04 + libc-01/02/07 + win-03 — libc-03 RETIRÉ) ; LA TABLE DES IDENTIFIANTS i11xxxx (la lignée g9 → h10 → i11)

**Le contexte qui fonde la décision (07/11).** La suite annoncée à l'Entrée 194 était M10-(a) ; le message du développeur la commande (« continue sur M10-(a) »). Le TGN exige la CRÉATION (D171) : la couche I complète est la première épreuve — 18 spécifications au gabarit intégral, AUCUN octet de notation, la cérémonie d'ère précède tout build. Le modèle M9-(a) (les 28 posées, les constantes re-dérivées, l'instrument 117 VERTS) est rejoué au domaine neuf.

**Les règles.** (1) **LE GABARIT INTÉGRAL, pas la forme compacte** : les SEPT blocs du § 2.2 (Intention, Contrat pre/post/inv, Échecs, Vecteurs, Fixtures, Provenance, Décisions) — les Échecs et Vecteurs EXPLICITES rendent la couverture CONTRÔLABLE MÉCANIQUEMENT : l'instrument vérifie que CHAQUE exigence Qn et CHAQUE échec En relie au moins un vecteur (une exigence invérifiable est une exigence mal formulée — la règle du protocole, tenue par le code). (2) **LE PLAN D'ADRESSAGE ARRÊTÉ AVANT LA NOTATION** (D161, la leçon de M8-(b)) : les constantes immuables seules — la table des SEPT verdicts (0 et −1..−7, dont **−1 LA FIN NOMMÉE** de la recherche : l'échec qui n'en est pas un, la fin d'une question) ; le CADRE de session (960 o, la disposition source unique que les dix-sept autres blocs citent) ; la LIGNE (77 o exacts, le format recomposé par le vérificateur) ; les 64 constantes MD5_T DÉRIVÉES PAR ARITHMÉTIQUE au geste même (floor(2^32·|sin(i+1)|), T[0] et T[63] recoupés à RFC 1321 — le juge est le code) ; les bornes du périmètre 0.1.0 (2 Gio, 24 lignes, 64 Kio, 32 o de motif, 256 écritures) ; les zones .data (cadre, écran, saisie, motif, journal, empreintes, métriques, la fenêtre de lecture partagée) ; l'IAT (34 feuilles NOMMÉES). (3) **LES RÈGLES EXÉCUTABLES** : vue_max (la dernière fenêtre VOIT le dernier octet) et recadre (la ligne active à la 12e) vivent en FONCTIONS au plan — le vérificateur les re-joue contre la référence : la règle de spécification n'est plus une phrase, c'est un code. (4) **L'HÉRITAGE DÉCLARÉ EST L'HÉRITAGE UTILISÉ** : tls13-01..04 (la famille sha scellée 1.0.0 — R7, embarqués byte-identiques au build), libc-01/02/07 (la minilibc) et win-03 (la boucle de la démo) — CHAQUE entrée est citée par ses specs ; **libc-03 RETIRÉ au geste** : aucune spécification ne le cite, le déclarer serait une contrebande de périmètre (un défaut nommé, pas une ombrageuse richesse). (5) **LES ARBITRAGES ARCHITECTURAUX nommés à leur spec** : la table unifiée des verdicts (tout refus monte à la barre — l'écran NOMME) ; LA BARRE-SAISIE (aucun contrôle enfant : l'écran appartient à Loupe) ; LE JOURNAL DES ÉCRITURES par décalage (le disque intact jusqu'à la sauvegarde, la réversibilité d'avant) ; LE DOUBLE-GESTE de sortie (la garde refus_quitter tenue par le RÉSEAU loupe-16/17/18 — ré-armée à chaque écriture, levée à chaque sauvegarde : la perte d'octets est une VOLONTÉ deux fois nommée) ; loupe-09 LA VITRINE ENTIÈRE (WinMain + la fenêtre + LA PROCÉDURE + les trois zones déclarées — la disposition tenue deux fois : des zones et des messages) ; le PANNEAU D'EMPREINTES TOUJOURS celui du DISQUE (l'astérisque nomme la divergence, jamais un condensé d'avant). (6) **LES FRONTIÈRES DU GESTE** : AUCUN octet de notation, AUCUN arbre signé touché (le garde 13 arbres VERTS vérifié AVANT consignation), le proxy 1.0.0 et la carte tls13 INTACTS.

**Alternatives rejetées.** La forme compacte tls13 pour les specs (rejetée : le TGN est l'épreuve de la MÉTHODE ENTIÈRE — le gabarit intégral rend la couverture contrôlable par le code, la forme compacte serait un repli de rigueur au moment précis où la méthode se prouve) ; déclarer libc-03 strlen dans l'héritage (rejeté : l'héritage déclaré serait un mensonge de périmètre — chaque entrée déclarée doit être citée) ; un contrôle enfant EDIT pour la saisie d'aller et de recherche (rejeté : l'écran appartient à Loupe — la barre devient le champ, aucune dépendance au contrôle système, le modèle démo reste un MODÈLE pas un héritage) ; la sauvegarde automatique à la fermeture (rejeté : la sauvegarde comme la perte sont des volontés — le double-geste les nomme, jamais une décision prise à la place de l'utilisateur) ; le panneau calculé sur la session (le journal appliqué) plutôt que le disque (rejeté : le panneau doit être RECOUPABLE — par l'outil du labo, par Get-FileHash chez le développeur — la vérité du disque, la divergence nommée par l'astérisque) ; le recalage silencieux de l'aller-à hors bornes (rejeté : LE REFUS NOMMÉ du README fondateur — jamais un saut deviné) ; la recherche par tables (Boyer-Moore) (rejeté : l'algorithme pur à la borne du quotidien — memcmp hérité, la complexité honnête tenue dans la tête, l'optimisation prématurée interdite par R11).
"""

# --- l'Entrée 195 (avant le marqueur m5a) ----------------------------------------

ENTREE_195 = """## Entrée 195 — « continue sur M10-(a) » : LE CHANTIER M10-(a) RÉALISÉ — LES DIX-HUIT SPÉCIFICATIONS POSÉES (LA COUCHE I COMPLÈTE DU TGN, R2 TENUE) ; LE PLAN D'ADRESSAGE ARRÊTÉ AVANT LA NOTATION (LES TABLES MD5 DÉRIVÉES PAR ARITHMÉTIQUE, LE CADRE, LA LIGNE, LES BORNES, LES ZONES, L'IAT) ; L'HÉRITAGE DÉCLARÉ PAR LA CARTE (libc-03 RETIRÉ : L'HÉRITAGE DÉCLARÉ EST L'HÉRITAGE UTILISÉ) ; LA TABLE i11xxxx ; L'INSTRUMENT 150 CONTRÔLES VERTS (07/11)

**La reprise (l'état au geste).** Le TGN ouvert à l'Entrée 194 (l'application « Loupe » arbitrée, le domaine fondé, la suite annoncée : M10-(a)), le développeur commande la suite : « continue sur M10-(a) ». La couche I seule vit, rien n'est scellé — le geste pose les CONTRATS de l'application entière, AUCUN octet de notation ne naît (R2 : la cérémonie d'ère précède tout build, la dette D166/D171 demeure).

**Le geste : LES DIX-HUIT SPÉCIFICATIONS POSÉES.** loupe/I/loupe-01..18 — les cinq familles du tableau fondateur : FICHIER (01 ouvrir : la session née entière, les refus nommés absent/verrouillé/hors périmètre · 02 lire : la fenêtre bornée, LE RECOUVREMENT du journal — l'édition survit au défilement · 03 fermer : idempotent, les zones d'hygiène vidées, jamais une poignée pendante · 04 le cadre : la structure unique de 960 o, la disposition source unique), EMPREINTES (05 sha256 d'une gamme : TLS13-01..04 PAR LA CARTE, jamais une copie d'octets · 06 md5 : la notation NEUVE — RFC 1321, les SEPT vecteurs officiels, « l'empreinte du quotidien, jamais une preuve de sécurité » nommé dans la spec · 07 le cumul : MD5 + SHA-256 du fichier entier, la composition seule, le panneau TOUJOURS celui du disque), RENDU (08 la ligne : 77 o exacts, feuille pure, l'alignement des colonnes invariant même à la ligne finale · 09 l'écran : LA VITRINE ENTIÈRE — WinMain, la fenêtre, LA PROCÉDURE au routage fermé, les TROIS zones déclarées avant la première goutte de peinture · 10 peinture : l'unique peintre, la police à chasse fixe, la cellule active en inverse · 11 défilement : la molette et l'ascenseur, la DERNIÈRE fenêtre VOIT le dernier octet), NAVIGATION (12 aller : la barre-saisie hexa, LE REFUS NOMMÉ hors bornes, LA RÈGLE DE RECADRAGE déclarée ici · 13 recherche : l'algorithme PUR par memcmp hérité, ou LA FIN NOMMÉE (−1) · 14 suivant : le recouvrement de frontière — l'occurrence à cheval jamais manquée, prouvé par construction), ÉDITION (15 curseur : les bords nommés, la vue suit — jamais perdu hors écran · 16 saisie : l'octet au journal par décalage, la marque sale, LE DISQUE INTACT · 17 sauver : chaque octet à SON décalage (l'écriture À L'OCTET), le panneau re-naît, LE TÉMOIN rendu (le compte et la gamme) · 18 quitter : LE DOUBLE-GESTE garanti — la garde refus_quitter tenue par le réseau 16/17/18, la sortie sans fuite).

**Le plan d'adressage ARRÊTÉ (D161 rejoué — loupe/layout.py).** La table des SEPT verdicts (0 et −1..−7 : −1 LA FIN NOMMÉE, −2 ABSENT, −3 HORS-BORNES [hors fichier OU périmètre], −4 SESSION, −5 ENTRÉE [l'ordre refusé en l'état], −6 SYSTÈME [gle consigné], −7 VERROUILLÉ) ; le CADRE (chemin 520 + taille + poignée + vue + curseur + remplissage + sale + refus_quitter + réserve + tampon 384 = 952 o, la zone 960 alignée 16) ; la LIGNE (77 o : 8 + 2 + 48 + 2 + 16 + 1, le format recomposé par le vérificateur) ; LES 64 CONSTANTES MD5_T DÉRIVÉES PAR ARITHMÉTIQUE au geste même (floor(2^32·|sin(i+1)|) — T[0] D76AA478, T[63] EB86D391 recoupés à RFC 1321 ; le juge est le code) ; les BORNES du périmètre 0.1.0 (2 Gio — le dernier décalage 0x7FFFFFFF tient en 8 chiffres, 24 lignes, la fenêtre de 64 Kio multiple du bloc 64 de SHA et MD5, le motif ≤ 32 o, le journal ≤ 256) ; les ZONES .data (cadre 960 · écran 2320 · saisie 96 · motif 48 · journal 4112 · empreintes 48 · hwnd 8 · métriques 16 · la fenêtre de lecture 65 536 — l'exclusion de famille : jamais deux flux, l'application monofile) ; L'HÉRITAGE PAR LA CARTE (tls13-01..04 la famille sha scellée 1.0.0 · libc-01 memcpy, libc-02 memcmp, libc-07 memset · win-03 la boucle de la démo — **libc-03 RETIRÉ au geste : aucune spec ne le cite, l'héritage déclaré est l'héritage utilisé**) ; L'IAT (34 feuilles nommées : kernel32 10 · user32 18 · gdi32 6 — WriteFile vit chez loupe-17 SEUL, les TROIS feuilles de win-03 héritée incluses) ; LES RÈGLES EXÉCUTABLES (vue_max et recadre en FONCTIONS : la dernière fenêtre voit le dernier octet, la ligne active à la 12e — le vérificateur les re-joue contre la référence).

**L'instrument (verifier_specs_m10a.py — 150 CONTRÔLES VERTS).** Les 18 têtes (révision 1, provenance écrite-avant-code) + les SEPT blocs du gabarit § 2.2 par spec ; la pureté déclarée (les blocs sans IAT : 04, 07, 08, 13) ; LA COUVERTURE : chaque Qn et chaque En relie au moins un vecteur (les « couvre Q…, E… » des Vecteurs, analysés par le code — les E « AUCUN » des blocs sans échec exigent leur justification nommée) ; les verdicts cités vivent dans la table ; LES RENVOIS valides (chaque loupe-NN/tls13-NN/libc-NN/win-NN cité existe — 18 + 4 + 3 + 2 citations ; chaque entrée d'héritage est citée, la liste est fermée ; le RÉSEAU structurant : la règle de recadrage citée par 14/15, la garde refus_quitter portée par 16/17/18, le panneau composé par 05/06 et né/re-né par 01/17) ; la table i110001..i110018 au README (la lignée g9 [M8] → h10 [M9] → i11 [M10]) ; les constantes RE-DÉRIVÉES (les 64 MD5_T par sinus, le format de ligne recomposé, le cadre et les zones recomptés champ à champ, vue_max re-jouée sur 18 tailles, recadre sur 9 curseurs, l'anti-doublon IAT) ; les décisions citées vivent au registre (les trois étages de format). VERDICT : VERT — le chantier (a) est COMPLET sur pièces.

**Détail.** FRONTIÈRES : AUCUN octet de notation (R2) ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment, AUCUN arbre signé touchés ; le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle (D87) ; le proxy 1.0.0 et la carte tls13 1.0.0 INTACTS (l'anti-rollback armé) ; la dette de cérémonie D166/D171 DEMEURE (le 14e arbre et l'extension du registre figé attendent la cérémonie d'ère — AVANT tout build). Livrables : loupe/I/loupe-01..18 (les 18 spécifications), loupe/I/README.md (la charte étendue § 9 ABI/verdicts + § 10 barre-saisie/journal + la table i11xxxx + le chantier (a) COMPLET), loupe/layout.py (le plan d'adressage), scripts/verifier_specs_m10a.py (l'instrument), le présent script. Consignations : la présente Entrée PAR SCRIPT, la D172 PAR SCRIPT (docs/DECISIONS.md), le PLAN (la rangée (a) RÉALISÉE + la phrase de l'État), worklog +Task ID 113. SUITE : M10-(b) LE NOYAU NOTÉ-MESURÉ-PROUVÉ (ouvrir/lire/fermer + les empreintes : le harnais différentiel sur vecteurs officiels + fichiers réels, l'héritage sha constaté byte-identique — R7) ; la cérémonie d'ère du TGN attend son geste (le 14e arbre) ; le projet fils attend son premier geste à son message propre.

"""

# --- la Task ID 113 (append au worklog) ------------------------------------------

TASK_113 = """
## Task ID 113 — LE CHANTIER M10-(a) RÉALISÉ : LES DIX-HUIT SPÉCIFICATIONS LOUPE-01..18 POSÉES (LA COUCHE I COMPLÈTE DU TGN, R2 TENUE — LE GABARIT § 2.2 AUX SEPT BLOCS, CHAQUE EXIGENCE RELIÉE À SON VECTEUR) ; LE PLAN D'ADRESSAGE loupe/layout.py ARRÊTÉ AVANT LA NOTATION ; L'HÉRITAGE DÉCLARÉ PAR LA CARTE (libc-03 RETIRÉ) ; LA TABLE i11xxxx ; L'INSTRUMENT 150 CONTRÔLES VERTS (07/11)

- Le message du développeur : « continue sur M10-(a) » — la suite
  annoncée à l'Entrée 194. Le geste pose LES CONTRATS de l'application
  entière : AUCUN octet de notation ne naît (R2 : la cérémonie d'ère
  précède tout build).
- LES 18 SPÉCIFICATIONS aux CINQ familles du tableau fondateur :
  fichier (01 ouvrir · 02 lire + le recouvrement du journal · 03
  fermer idempotent · 04 le cadre 960 o, la disposition source unique)
  · empreintes (05 sha256 PAR LA CARTE tls13-01..04 · 06 md5 LA
  NOTATION NEUVE [RFC 1321, les sept vecteurs officiels, « jamais une
  preuve de sécurité » nommé] · 07 le cumul, le panneau TOUJOURS
  celui du disque) · rendu (08 la ligne 77 o, feuille pure · 09
  l'écran : LA VITRINE ENTIÈRE [WinMain + fenêtre + LA PROCÉDURE +
  les trois zones déclarées] · 10 peinture, l'unique peintre · 11
  défilement : la dernière fenêtre VOIT le dernier octet) ·
  navigation (12 aller : la barre-saisie, LE REFUS NOMMÉ hors bornes,
  LA RÈGLE DE RECADRAGE · 13 recherche : l'algorithme PUR par memcmp
  hérité, ou LA FIN NOMMÉE [-1] · 14 suivant : le recouvrement de
  frontière prouvé par construction) · édition (15 curseur : jamais
  perdu hors écran · 16 saisie : le journal par décalage, LE DISQUE
  INTACT · 17 sauver : l'écriture À L'OCTET, le panneau re-naît, LE
  TÉMOIN rendu · 18 quitter : LE DOUBLE-GESTE garanti, la garde
  refus_quitter tenue par le réseau 16/17/18).
- LE PLAN D'ADRESSAGE (loupe/layout.py, D161 rejoué) : la table des
  SEPT verdicts (−1 LA FIN NOMMÉE) · le cadre (952 o, la zone 960) ·
  la ligne (77 o recomposée) · LES 64 CONSTANTES MD5_T DÉRIVÉES PAR
  ARITHMÉTIQUE (T[0] D76AA478, T[63] EB86D391 — RFC 1321 recoupé, le
  juge est le code) · les bornes 0.1.0 (2 Gio, 24 lignes, 64 Kio,
  motif ≤ 32, journal ≤ 256) · les zones .data (960 · 2320 · 96 · 48
  · 4112 · 48 · 8 · 16 · 65 536) · l'IAT 34 feuilles (kernel32 10 ·
  user32 18 · gdi32 6, WriteFile chez loupe-17 SEUL) · LES RÈGLES
  EXÉCUTABLES (vue_max, recadre — des fonctions re-jouées par le
  vérificateur).
- L'HÉRITAGE DÉCLARÉ EST L'HÉRITAGE UTILISÉ : tls13-01..04 + libc-01/
  02/07 + win-03, CHAQUE entrée citée par ses specs ; libc-03 RETIRÉ
  (aucune spec ne le cite — la contrebande de périmètre est un défaut
  nommé).
- L'INSTRUMENT verifier_specs_m10a.py : 150 CONTRÔLES VERTS — les
  têtes et les sept blocs, la pureté déclarée (04/07/08/13), LA
  COUVERTURE de chaque Qn/En par un vecteur, les verdicts dans la
  table, les renvois et le réseau structurant, la table i11xxxx, les
  constantes RE-DÉRIVÉES (64 MD5_T par sinus, le format, le cadre, les
  zones, vue_max sur 18 tailles, recadre sur 9 curseurs), les
  décisions au registre.
- FRONTIÈRES : AUCUN octet de notation ; AUCUNE clé, AUCUN coffre
  réel, AUCUN fragment, AUCUN arbre signé touchés ; le garde sceau I :
  13 arbres VERTS (cle deposee reelle) vérifié AVANT consignation ; le
  proxy 1.0.0 et la carte tls13 INTACTS ; la dette de cérémonie
  D166/D171 DEMEURE (le 14e arbre attend la cérémonie d'ère, avant
  tout build). Livrables : loupe/I/loupe-01..18, loupe/I/README.md
  (§ 9 + § 10 + la table i11), loupe/layout.py,
  scripts/verifier_specs_m10a.py, scripts/consigner_m10a.py.
  Consignations : l'Entrée 195 PAR SCRIPT, la D172 PAR SCRIPT, le PLAN
  (la rangée (a) RÉALISÉE + l'État), la présente Task ID 113.
- SUITE : M10-(b) LE NOYAU NOTÉ-MESURÉ-PROUVÉ (fichier + empreintes,
  le harnais différentiel, l'héritage sha byte-identique — R7) ; la
  cérémonie d'ère du TGN attend son geste ; le projet fils attend son
  premier geste à son message propre.
"""


def main():
    # 0. le garde AVANT consignation (la discipline du projet)
    r = subprocess.run(["python3", str(REPO / "v06" / "sceau_I.py"),
                        "verifier"], capture_output=True, text=True)
    if "13 arbres VERTS" not in r.stdout:
        sys.exit("ÉCHEC : le garde sceau I ne constate pas 13 arbres VERTS "
                 f"— consignation REFUSÉE\n{r.stdout[-400:]}")
    print("GARDE : 13 arbres VERTS (cle deposee reelle) — la consignation peut suivre")

    # 0bis. l'instrument du chantier AVANT consignation (le geste se prouve)
    r = subprocess.run(["python3", str(REPO / "scripts" /
                                       "verifier_specs_m10a.py")],
                       capture_output=True, text=True)
    if "VERDICT : VERT" not in r.stdout or r.returncode != 0:
        sys.exit("ÉCHEC : l'instrument verifier_specs_m10a.py n'est pas VERT "
                 f"— consignation REFUSÉE\n{r.stdout[-600:]}")
    print("INSTRUMENT : verifier_specs_m10a.py VERT (150 contrôles) — "
          "le geste se prouve avant de se consigner")

    # 1. le plan : la rangée (a) RÉALISÉE + l'État (idempotent)
    plan = PLAN.read_text(encoding="utf-8")
    if "RÉALISÉ (Entrée 195, D172)" in plan:
        print("PLAN : la rangée (a) RÉALISÉE déjà consignée — constaté")
    else:
        if plan.count(RANGEE_ANCIENNE) != 1:
            sys.exit(f"ÉCHEC : la rangée (a) OUVERTE trouvée "
                     f"{plan.count(RANGEE_ANCIENNE)} fois (attendu : 1)")
        if plan.count(ANCIEN_ETAT) != 1:
            sys.exit(f"ÉCHEC : ancrage État trouvé "
                     f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
        plan = plan.replace(RANGEE_ANCIENNE, RANGEE_NOUVELLE, 1)
        plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
        if "RÉALISÉ (Entrée 195, D172)" not in plan:
            sys.exit("ÉCHEC : la rangée (a) absente après remplacement")
        if "LE CHANTIER M10-(a) RÉALISÉ le 07/11/2026" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du M10-(a)")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (a) RÉALISÉE + l'État du programme — consignés")

    # 2. le journal : l'Entrée 195 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 195 —" in journal:
        print("JOURNAL : l'Entrée 195 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_195 + marqueur, 1)
        if "## Entrée 195 — « continue sur M10-(a) »" not in journal:
            sys.exit("ÉCHEC : l'Entrée 195 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 195 consignée AVANT le marqueur m5a")

    # 3. le registre des décisions : la D172 à la suite de D171
    decisions = DECISIONS.read_text(encoding="utf-8")
    if "## D172 —" in decisions:
        print("DECISIONS : la D172 déjà consignée — constaté")
    else:
        if decisions.count("## D171 —") != 1:
            sys.exit("ÉCHEC : la D171 absente ou multiple (le geste "
                     "précédent n'est pas consigné)")
        decisions = decisions.rstrip("\n") + "\n" + D172.strip("\n") + "\n"
        if "## D172 — LE CHANTIER M10-(a) RÉALISÉ" not in decisions:
            sys.exit("ÉCHEC : la D172 absente après append")
        DECISIONS.write_text(decisions, encoding="utf-8")
        print("DECISIONS : la D172 consignée À LA SUITE de la D171")

    # 4. le worklog racine : la Task ID 113 à la suite de la 112
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 113 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 113 existe déjà (rejeu REFUSÉ)")
    if worklog.count("## Task ID 112 —") != 1:
        sys.exit("ÉCHEC : l'entrée Task ID 112 absente ou multiple (le geste "
                 "précédent n'est pas consigné)")
    if not worklog.rstrip().endswith(
            "projet fils attend son premier geste à son message propre."):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 112 "
                 "attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_113
    if "## Task ID 113 — LE CHANTIER M10-(a) RÉALISÉ" not in worklog:
        sys.exit("ÉCHEC : la Task ID 113 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 113 consignée À LA SUITE de la Task 112")


if __name__ == "__main__":
    main()
