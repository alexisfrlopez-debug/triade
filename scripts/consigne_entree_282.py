#!/usr/bin/env python3
"""TRIADE — LA CONSIGNATION de l'Entrée 282 + Task 189 : LA PREMIÈRE UNITÉ
DE LA CAMPAGNE D204 CONSTRUITE ET LIVRÉE (loupe-01 OUVRIR × bras T, la
commande du développeur : « go pour l'unité 1 »). Append au worklog.md et
au docs/JOURNAL_TRAVAIL.md — la carte OU-TROUVER portée à 282."""
import pathlib

REPO = pathlib.Path("/home/z/my-project/work/triade")

WORKLOG = """

Task ID: 189
Agent: Z.ai (agent principal — la session de la première unité de la campagne)
Task: LA PREMIÈRE UNITÉ DE LA CAMPAGNE D204 CONSTRUITE, CRISTALLISÉE ET
LIVRÉE — loupe-01 OUVRIR × bras T (la commande « go pour l'unité 1 ») : le
workflow mesuré de bout en bout, les journaux M2/M4 NÉS DE LA PREMIÈRE
MESURE (CA1), la pièce recomposée du plan où SEUL le slot loupe-01 porte
la notation de campagne, le kit aux EMPREINTES gravées déposé au coffre
/test en son dossier daté kit-unite-loupe-01-T-20261114/.

Work Log:
- LA PRÉPARATION (avant toute mesure, D122) : l'infrastructure de campagne
  écrite et éprouvée AU LABO — le builder (scripts/campagne_d204/
  unite-01-T/build_unite01.py : les 17 notations scellées LUES à leurs
  arbres + la notation de campagne par la chaîne brouillon → auteur →
  notation, l'oracle structurel et l'audit msx64 du plan, la recomposition
  PE, le différentiel contre le scellé CONFINÉ au slot loupe-01 et à la
  porte R10), le round-trip (R5), l'oracle du bloc (les vecteurs du
  contrat, le juge = le modèle indépendant hashlib, le harnais du domaine
  portant la pièce de campagne au slot). L'ÉPREUVE DE PLOBERIE : le
  builder avec le BROUILLON SCELLÉ reproduit loupe.exe 0.1.1-dev.1 OCTET
  POUR OCTET (sha256 c1115105…) — la mécanique est fidèle AVANT toute
  mesure, puis l'épreuve RETIRÉE (le brouillon scellé ne demeure JAMAIS
  au dossier de campagne : la notation mesurée naît de l'appel seul).
- LE WORKFLOW MESURÉ (chaque appel au modèle par compter_tokens.py, chaque
  commande par chronometre_verification.py — les journaux à preuves_v150/
  comparaison_resultats/, NÉS de la première mesure : la ligne de garde
  d'abord, 02:08:50Z) : le GARDE sceau-I 14 arbres VERT (0,070 s) ;
  la PHASE SPEC (5 313 tokens — le contrat lu, les notes d'auteur) ; la
  PHASE ORACLE (3 752 tokens — les attentes du juge dérivées du contrat
  AVANT le code, écrit-avant-code) ; la PHASE NOTATION (11 480 tokens —
  le brouillon écrit À LA MAIN, jamais la notation scellée au prompt) ;
  SIX CORRECTIFS comptés (32 613 tokens) tenus par les DÉFAUTS NOMMÉS AU
  LABO avant toute correction (D1-D25 : la syntaxe RIP+offset, CreateFileW
  testé à zéro, les arguments 5-7 au home space, l'alignement, rcx écrasé
  par loupe-04, l'ordre de la session, le verdict de l'appelé effacé par
  loupe-03, la poignée pendante de GetFileSizeEx, le hTemplateFile écrit
  sur 4 octets — le défaut que seul le VRAI Windows aurait vécu, la
  borne par registre, la poignée jamais chargée pour GetFileSizeEx) ;
  les builds (3 refus nommés ~0,22 s, puis VERT ~0,48 s), les round-trips
  (0,223 / 0,212 s), l'oracle (le premier ROUGE : D25 nommé sur
  l'émulation, 0,310 s ; le second VERT 10,202 s — le panneau du témoin
  3f, deux passages d'empreintes sous émulation).
- LA PIÈCE : loupe.exe de campagne 127 488 o, sha256 4d119b22…, la
  notation 356 o de code au slot 0x4080 (448 o, padding 92) ; le
  différentiel contre le scellé : 12 plages, 356 o, TOUTES au slot
  loupe-01 et à la porte R10 — les arbres signés INTACTS, le garde
  14/14 AVANT tout geste ; LA CRISTALLISATION R6 : DIX rebuilds
  consécutifs identiques (10/10, sha constant).
- LE KIT : kit-unite-loupe-01-T-20261114/ — la pièce + la notation livrée
  + le brouillon + le scénario terrain (LE CHARGEUR : LoadLibraryEx
  DONT_RESOLVE, les six feuilles du noyau résolues aux slots, loupe-01
  appelé aux témoins, le juge hashlib, le témoin né du run) + le lanceur
  officiel + les QUATRE témoins (la génération FIXE, graine 20261107) +
  la gravure EMPREINTES (10 pièces sha256, le format du GUI) + le
  LISEZMOI ; py_compile VERT, l'épreuve d'extraction vierge 11/11, le
  zip 219 581 o (sha256 a1153d67…).
- LE DÉPÔT au coffre /test : le dossier daté + le zip, 12/12 pièces
  recoupées PAR RE-TÉLÉCHARGEMENT octet pour octet (id Drive du dossier
  19ct_zU8LUs5zaluYyssg4EBH6EGYOUHJ) — le GUI attend le kit à l'onglet
  1·KIT de l'unité loupe-01 × T.
- LA MESURE (M2 : 9 appels, 53 158 tokens, 100 % lus du log d'usage,
  zéro estimation — CA3 ; M4 : 20 lignes — la garde, les builds, les
  round-trips, les oracles ; M1 : les 25 défauts nommés au labo AVANT
  tout run = exclusions § 2.3, JAMAIS ÉCHAPPÉS — la première LIVRAISON
  naîtra du run du développeur ; M3 : le carnet au geste du développeur).
- LA FRONTIÈRE TENUE : le labo n'a couru AUCUN run terrain (CA6), n'a
  daté ni signé AUCUN témoin (D99), les pièces scellées du projet
  INTACTES (le différentiel le prouve octet pour octet), le plan
  VERROUILLÉ a78caf8c… INTACT, AUCUN agrégat calculé en cours de route
  (CA7 — les comptes seuls vivent au journal).
- SUITE : au développeur — le GUI (onglet 1·KIT : choisir le dossier
  kit-unite-loupe-01-T-20261114 du /test), le RUN (le lanceur officiel),
  le TÉMOIN daté signé de la main, le dossier ENTIER renvoyé au /test ;
  puis l'unité 2 (loupe-01 × bras C) quand le vert recoupé ferme l'unité 1.
"""

JOURNAL = """

## Entrée 282 — LA PREMIÈRE UNITÉ DE LA CAMPAGNE D204 CONSTRUITE, CRISTALLISÉE ET LIVRÉE : loupe-01 OUVRIR × bras T, le workflow mesuré de bout en bout (la commande du développeur : « go pour l'unité 1 » — la suite nommée à l'Entrée 281) : LA CAMPAGNE EST NÉE à 02:08:50Z — le dossier des résultats (preuves_v150/comparaison_resultats/) NAÎT de la première mesure (CA1 tenu : la ligne de garde d'abord, les journaux M2/M4 créés par les instruments mêmes, jamais avant).

- LE GARDE D'ABORD (les arbres signés avant tout geste, § 2 du plan) : sceau-I 14 arbres VERT, chronométré 0,070 s — la première ligne du journal M4 ; l'infrastructure de campagne fut éprouvée AVANT (D122) : le builder au brouillon SCELLÉ reproduit loupe.exe 0.1.1-dev.1 OCTET POUR OCTET (c1115105…) — l'épreuve retirée ensuite, la notation mesurée naît de l'appel seul.

- LE WORKFLOW MESURÉ (M2 : 9 appels, 53 158 tokens, 100 % lus du log d'usage, zéro estimation — CA3) : SPEC 5 313 tokens (le contrat loupe-01:R3 lu, les notes d'auteur) ; ORACLE 3 752 tokens (les attentes du juge dérivées du contrat AVANT le code — écrit-avant-code, charte § 3) ; NOTATION 11 480 tokens (le brouillon écrit À LA MAIN depuis le contrat + les faits du plan — JAMAIS la notation scellée au prompt) ; SIX CORRECTIFS 32 613 tokens, chacun tenu par les DÉFAUTS NOMMÉS AU LABO AVANT toute correction (la règle D202) : D1-D25 — la syntaxe [rip+SYMBOLE+offset] hors outil, CreateFileW testé à zéro (la poignée INVALIDE est -1), les arguments 5-7 de CreateFileW au home space (LA CLASSE de l'Entrée 207, revécue), l'alignement rsp ≡ 0 (mod 16), rcx écrasé par loupe-04 à travers l'appel, l'ordre de la session inversé (loupe-02 PUIS loupe-07, le contrat Q4), le verdict de l'appelé effacé par loupe-03, la poignée pendante au refus de GetFileSizeEx, le hTemplateFile écrit sur 4 octets (LES 4 OCTETS HAUTS AU HASARD — le défaut que l'émulation passe et que le VRAI Windows aurait vécu : nommé au labo, JAMAIS ÉCHAPPÉ), la borne 0x80000000 par registre (keystone refuse l'immédiat), la poignée jamais chargée dans rcx pour GetFileSizeEx (le diagnostic de l'oracle sur l'émulation : -6 sur tout fichier sain) — VINGT-CINQ défauts nommés au LABO avant tout run : exclusions § 2.3, JAMAIS ÉCHAPPÉS (M1), la première LIVRAISON naîtra du run du développeur seul.

- LES VÉRIFICATIONS (M4 : 20 lignes au journal) : les builds — trois refus nommés (~0,22 s : la résolution auteur, les mêmes refus qui nommèrent les défauts), puis VERT ~0,48 s ; les round-trips R5 — 0,223 s puis 0,212 s (keystone == capstone == keystone, l'octet juge) ; l'oracle du bloc — le premier ROUGE 0,310 s (D25 nommé : dix vecteurs rouges, le diagnostic précis), le second VERT 10,202 s : LES QUATORZE VECTEURS DU CONTRAT VERTS (les trois formes du remplissage + le vide, la session née entière champ à champ, le panneau == (md5, sha256) hashlib du fichier entier, les trois refus d'OS traduits par la table, la borne 2 Gio la poignée fermée comptée, la session double l'ancien cadre intact, le chemin de 260 sans NUL, LA FALSIFICATION DEMANDÉE — la taille mutée, l'écran attendu diverge, le juge lit l'état jamais le modèle).

- LA PIÈCE : loupe.exe de campagne — 127 488 o, sha256 4d119b22273c8fe140a2b74d5f8fe3f8eef5457540cbc9e178529e13fee244a5 — la notation 356 o de code au slot 0x4080 (448 o, 92 o de padding NOP), les 17 autres blocs et les 8 héritages LES SCELLÉS INTACTS (D161 tenu pour les dix-sept : chaque longueur == la mesure d'arrêt) ; LE DIFFÉRENTIEL contre le scellé : 12 plages, 356 octets, TOUTES au slot loupe-01 et à la porte R10 — l'écart CONFINÉ, nommé, les arbres signés INTACTS (§ 3 du plan : la campagne vit sur des artefacts dev) ; LA CRISTALLISATION R6 : DIX rebuilds consécutifs IDENTIQUES (10/10, le sha constant à chaque rebuild).

- LE KIT TERRAIN (le modèle de la campagne Loupe, CA2 : la pièce + le scénario + les témoins) : kit-unite-loupe-01-T-20261114/ — la pièce ; la notation livrée (l'explicite résolue par l'outil auteur, le round-trip au labo) ; le brouillon de la main (la septième édition) ; scenario-unite01.py (python SEUL : LE CHARGEUR — LoadLibraryEx DONT_RESOLVE, les six feuilles kernel32 du noyau résolues aux slots du plan par VirtualProtect, loupe-01 appelé à son adresse au plan, les vecteurs du contrat jugés par le modèle indépendant hashlib, LE TÉMOIN né du run — l'accès refusé NOMMÉ ABSENT du terrain, le chemin de 260 CONSIGNÉ TEL QUEL : le système le refuse avant la mesure du bloc) ; LANCEUR-UNITE-01-T.bat (le lanceur officiel — sa propre console, INTACT) ; les QUATRE témoins du kit (temoin-1.bin, temoin-384.bin, temoin-3f.bin, vide.bin — la génération FIXE du harnais, graine 20261107, les mêmes qu'au labo) ; la GRAVURE EMPREINTES-KIT-UNITE-01-T.txt (10 pièces sha256 au format du GUI — l'onglet 1·KIT recoupe, une divergence rien ne court) ; le LISEZMOI ; py_compile VERT, l'épreuve d'extraction vierge 11/11, le zip 219 581 o (sha256 a1153d672a826a5d…).

- LE DÉPÔT AU COFFRE /test : le dossier daté kit-unite-loupe-01-T-20261114/ (id Drive 19ct_zU8LUs5zaluYyssg4EBH6EGYOUHJ) — les ONZE pièces + le zip, 12/12 recoupées PAR RE-TÉLÉCHARGEMENT octet pour octet, 0 écart ; le GUI de campagne attend le kit à l'onglet 1·KIT de l'unité loupe-01 × T ; LA CAP § 7 armée par le GUI : au plus TROIS livraisons pour ce bloc, l'arrêt au premier vert recoupé.

- LA FRONTIÈRE TENUE PAR CONSTRUCTION : le labo n'a couru AUCUN run terrain (CA6 — le run appartient au développeur), n'a daté ni signé AUCUN témoin (D99 — la main du développeur), n'a fabriqué AUCUN chiffre (CA5 — les comptes seuls vivent aux journaux, AUCUN agrégat calculé en cours de route, CA7), les pièces scellées du projet INTACTES (le différentiel le prouve), le plan VERROUILLÉ a78caf8c… INTACT (les HUIT pièces du kit campagne inchangées, le verrou du GUI le constatera).

- LA CONSIGNATION : la présente Entrée 282 + Task 189 ; la carte OU-TROUVER portée à 282 ; D141 tenu avant le commit (le courant 281-ba7ccd9 archivé versionné au miroir) ; le commit ; le push GitHub ; le miroir synchronisé. (14/11, la session de la première unité de la campagne)
"""

with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(WORKLOG)
with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8",
          newline="\n") as f:
    f.write(JOURNAL)

# la carte OU-TROUVER portée à 282 (la ligne de portée + la section)
carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
texte = carte.read_text(encoding="utf-8")
texte = texte.replace("Entrées 251-281) et au worklog (`worklog.md`, Tasks 158-188)",
                      "Entrées 251-282) et au worklog (`worklog.md`, Tasks 158-189)")
if "LA CAMPAGNE D204 EST NÉE" not in texte:
    texte += """

9. **LA CAMPAGNE D204 EST NÉE — LA PREMIÈRE UNITÉ LIVRÉE (Entrée 282)** :
   le dossier des résultats (scripts/preuves_v150/comparaison_resultats/)
   NAÎT de la première mesure (CA1 : la ligne de garde, 14/11 02:08:50Z) ;
   l'unité 1 — loupe-01 OUVRIR × bras T — construite, vérifiée (l'oracle
   du bloc 14 VERT, le round-trip R5, la cristallisation 10/10),
   livrée au coffre /test/kit-unite-loupe-01-T-20261114/ (12/12 pièces
   recoupées par re-téléchargement) : la pièce (le scellé ne diffère qu'au
   slot loupe-01 et à la porte R10), la notation de campagne (7 éditions,
   6 correctifs, 25 défauts nommés au labo AVANT tout run — exclusions,
   jamais échappés), le scénario chargeur + les témoins + la gravure
   EMPREINTES ; la mesure vit aux journaux (M2 : 53 158 tokens en 9
   appels lus du log ; M4 : 20 lignes) ; LE RUN APPARTIENT AU
   DÉVELOPPEUR (le GUI onglet 1·KIT → 2·RUN → 3·TÉMOIN daté signé, le
   dossier ENTIER renvoyé au /test).
"""
carte.write_text(texte, encoding="utf-8", newline="\n")
print("[consigné] worklog.md + docs/JOURNAL_TRAVAIL.md — l'Entrée 282 + "
      "Task 189 ; la carte OU-TROUVER portée à 282")
