#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA CONSIGNATION de l'Entrée 284 + Task 191 (le run VERT de
l'unité 1 × bras T recoupé — LA PREMIÈRE MESURE de la campagne, l'unité
close à it1 ; la deuxième unité loupe-01 × bras C construite, éprouvée
et livrée au coffre).

  1. le dépôt local rattrapé (fast-forward si besoin) ;
  2. les textes appended : worklog.md (Task 191),
     docs/JOURNAL_TRAVAIL.md (Entrée 284), OU-TROUVER portée à 284 ;
  3. D141 : le courant 283-7678421 archivé versionné (bundle) ;
  4. le commit (l'atelier unite-01-C/ entier + les journaux M2/M4) + le
     push GitHub (le jeton ghp_ du coffre)."""
import json
import pathlib
import re
import subprocess

REPO = pathlib.Path("/home/z/my-project/work/triade")
WORK = pathlib.Path("/home/z/my-project/work")
GIT = "https://github.com/alexisfrlopez-debug/triade.git"


def run(*args, **kw):
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout, r.stderr


def git(*args):
    code, out, err = run("git", *args)
    if code != 0:
        raise RuntimeError(f"git {' '.join(args[:3])}… : {err[:400]}")
    return out


# ------------------------------------------------------------------
# 1. LE DÉPÔT RATTRAPÉ
# ------------------------------------------------------------------
git("config", "core.filemode", "false")
st = git("status", "--short")
print(f"[git] l'état local : {len(st.splitlines())} chemin(s) en jeu")
token = (WORK / "token_git_coffre.txt").read_text().strip()
git("fetch", f"https://x-access-token:{token}@{GIT[8:]}", "main")
git("merge", "--ff-only", "FETCH_HEAD")
head = git("rev-parse", "--short", "HEAD").strip()
sujet = git("log", "-1", "--format=%s").strip()[:80]
print(f"[git] fast-forward OK — HEAD {head} : {sujet}…")

# ------------------------------------------------------------------
# 2. LES TEXTES
# ------------------------------------------------------------------
JOURNAL = """

## Entrée 284 — LE RUN DE L'UNITÉ 1 × BRAS T REVENU VERT, RECOUPÉ : LA PREMIÈRE MESURE DE LA CAMPAGNE EST NÉE (CA1), L'UNITÉ CLOSE À IT1 — ET LA DEUXIÈME UNITÉ LOUPE-01 × BRAS C CONSTRUITE, ÉPROUVÉE ET LIVRÉE AU COFFRE (l'annonce : « nouveau run dans /test du drive » — le dossier « Nouveau run », créé le 14/11 08:58:52Z)

- LA REPRISE TENUE : le kit v2 couru au terrain — le témoin preuves-unite01/temoin-unite01.txt (1 299 o, sha256 896f42a2…) DATÉ DE LA MAIN (14/11/2026) et SIGNÉ (Alexis Lopez), le geste D99 tenu ; T0 RECOUPÉ : loupe.exe 127 488 o sha256 4d119b22… == la gravure du kit v2 == l'empreinte que porte le témoin ; LE VERDICT : 15 VERT, 0 ROUGE (T0, V1×8, V2×3, V3×3) — le REFUS de l'Entrée 283 réparé, la faute était bien au labo ; preuves-unite01/ rendu ENTIER (vérifié au source du scénario : il n'écrit QUE le témoin).

- LA PREMIÈRE MESURE (CA1) : l'atelier né du verrou (les HUIT pièces recoupées, le plan a78caf8c… == D204), livraisons.csv porte SA PREMIÈRE LIGNE — T-loupe-01-it1, VERT, le recoup « en attente » → RECOUPÉ VERT PAR LE LABO ; le carnet : cristallisation 85 minutes (M3, 08:35-10:00) ; la session GUI complète consignée : SIX runs 1-clic (voie1, voie2, diagnostic, geste-b, vitrine, séquestre), la calibration VERT (écart 0,000 s), le GUI intègre (les pièces recoupées à la gravure EMPREINTES) ; DEUX ABSENCES NOMMÉES : temoin-shani.txt absent du rejeu geste-b (D189 — le VERDICT présent, un rejeu : la chaîne voie 2 demeure fermée, D165) et la réplication non consignée (EN ATTENTE des deux jeux d'annotations — jamais maquillée).

- L'ARRÊT AU PREMIER VERT RECOUPÉ (§ 7 du plan) : T-loupe-01 FERMÉE À IT1 — une livraison sur trois de cap, la PREMIÈRE unité close de la partie contrôlée (une sur douze).

- LA DEUXIÈME UNITÉ (la commande « go consignation et loupe-01 × bras C ») : le MÊME contrat de couche I lu comme cahier des charges, le source C écrit par le MÊME agent au chemin instrumenté (compter_tokens.py, CA3) — ONZE appels, 67 475 tokens LUS DU LOG, zéro estimation (spec 5 605 ; oracle 4 423, écrit-avant-code ; source-c 14 660 ; SEPT correctifs 39 224 ; tests-c 3 563) ; la première édition TRONQUÉE par la limite de complétion (trois fois — l'événement nommé, le format PATCH naquit : les remplacements exacts et la suite assemblés par l'outil auteur, comme les étiquettes de la notation du bras T).

- LES DÉFAUTS NOMMÉS AVANT TOUTE CORRECTION (la règle, aux deux bras) : l'argument confondu avec le cadre ; la copie du chemin cassée aux octets hauts UTF-16 ; la double ouverture du fichier ; GENERIC_READ sans GENERIC_WRITE ; ERROR_PATH_NOT_FOUND absent de la table E1 ; les rondes MD5 2 et 4 fausses (la majorité et le Ch au lieu de la sélection et c^(b|~d)) ; la table S TRANSPOSÉE (les quatre groupes par rangée au lieu d'un groupe répété) ; le compteur de tampon lu au champ REMPL du cadre SANS initialisation entre les vecteurs ; le NUL du chemin posé à la capacité (259) au lieu de la fin réelle ; ET LES DEUX APPELS memset ÉMIS PAR gcc -O2 (l'idiome reconnu des boucles de bourrage de md5_final/sha256_final — le CRT jamais résolu sous DONT_RESOLVE : la parade des écritures VOLATILE, l'idiome ne fusionne jamais un magasin volatile).

- LES FAUTES DU LABO NOMMÉES TELLES (jamais maquillées) : la prescription S[i % 16] du correctif-4 — FAUSSE sur la table de 64 entrées livrée (S[i] direct était le juste du correctif-3, l'épreuve Python du transform le prouva) ; l'étiquette AVANT inexacte d'un remplacement du correctif-6 (l'auteur supposa le i_chemin déjà posé — l'APRÈS exact appliqué au bloc UNIQUE de copie du chemin, fail-closed) ; les offsets de la IMAGE_EXPORT_DIRECTORY appris au fil de l'épreuve (Name +12, Base +16 — les versions sont des WORD ; NumberOfNames +24, les tables +28/+32/+36).

- LA COMPILATION (M4, la commande consignée) : x86_64-w64-mingw32-gcc-posix -O2 -shared -o loupe-01-c.dll loupe-01-c.c loupe-01-c.def — le compilateur croisé gcc-mingw-w64 14.2 extrait des paquets Debian SANS ROOT au bac du labo (les .deb décompressés, l'outillage au travail/mingw-debs — aucun privilège demandé) ; les commandes de vérification journalisées au journal_verifications.jsonl (build 0,678 s ; la suite de tests ; les contrôles binaires — deux échecs de CHEMIN nommés puis corrigés, les lignes demeurées).

- LES ÉPREUVES (D122 — le labo n'a AUCUN Windows, la LOGIQUE rejouée au POSIX) : la couche MD5+SHA-256 32 VERT 0 ROUGE (toutes les frontières du rembourrage — 0, 1, 55, 56, 57, 63, 64, 65… 196 609 — et l'absorption IRRÉGULIÈRE par morceaux de 7, 1, 4090, 13…, le juge hashlib) ; LE CONTRAT ENTIER 17 VERT 0 ROUGE (les quatre témoins champ à champ contre l'oracle hashlib — le chemin, la taille, la vue, le curseur, le remplissage, le tampon, LE PANNEAU ; absent → -2 ; verrouillé → -7 — la tenue flock sans partage au shim ; la borne 2 Gio + 1 posée ÉPARS au disque → -3 ; la session double → -5, l'ancien cadre ET panneau relus IDENTIQUES octet par octet ; le chemin de 260 caractères sans NUL → refus nommé, RIEN au cadre) — le harnais de la phase tests-c livré par l'appel instrumenté (les shims POSIX aux six feuilles), son main complété par le labo (l'écart nommé : des accesseurs fantômes, l'encodage UTF-16, aucun vecteur armé), le décodage LPCWSTR corrigé (le wchar_t POSIX en fait 4 — la pièce est juste, le shim devait refléter le Windows) ; LES CONTRÔLES BINAIRES 16 VERT 0 ROUGE (PE32+ DLL x86-64 ; les QUATRE exports dont les DONNÉES cadre 960 o et panneau 48 o vers .data ; les CINQ feuilles kernel32 aux slots RÉELS de la table d'imports ; AUCUN appel CRT dans la clôture des fonctions — l'audit par adresses IAT suit les fonctions, leurs appelés et les thunks ; les relocations présentes) ; la découverte PE du scénario éprouvée au POSIX (les quatre exports, les cinq slots — test_decouverte.py).

- LE KIT LIVRÉ : /test/kit-unite-loupe-01-C-20261114/ — 12/12 pièces recoupées par re-téléchargement ET 12/12 au bac du miroir download/kit_unite_loupe_01_C/ (24/24 VERT) ; la pièce loupe-01-c.dll 93 625 o sha256 85b34ed4…, le source loupe-01-c.c 860ff1cf… (la livraison du bras C : le binaire ET le source), les QUATRE témoins OCTET POUR OCTET ceux du kit T (df7e70e5…/3396717b…/c5fc1f28…/e3b0c442… — la génération fixe, recoupés à la gravure du kit T avant la copie) ; le scénario scenario-unite01C.py ADAPTÉ AU PE COMPILÉ (la découverte par la table d'exports, la résolution des feuilles aux slots réels de la table d'imports, LES MÊMES vecteurs, le MÊME juge hashlib, le témoin à preuves-unite01C/) ; LES ÉCARTS NOMMÉS du bras C : SetFilePointerEx absente des imports (la lecture séquentielle depuis l'ouverture — le scénario résout les feuilles que la pièce déclare, les cinq suffisent) ; les imports du CRT de lancement mingw (InitializeCriticalSection…) présents à la table SANS jamais être appelés (aucun point d'entrée ne court sous DONT_RESOLVE — l'audit de la clôture le prouve).

- LA REPRISE (au développeur, tout au clic) : le GUI onglet 1·KIT de l'unité loupe-01 × C → CHOISIR kit-unite-loupe-01-C-20261114 (le GUI recoupe la gravure) ; onglet 2·RUN → LANCER LANCEUR-UNITE-01-C.bat ; onglet 3·TÉMOIN → DATER, SIGNER DE VOTRE MAIN, renvoyer preuves-unite01C/ ENTIER au coffre /test — la DEUXIÈME livraison de la campagne naîtra au geste (M1).

- LA CONSIGNATION : la présente Entrée 284 + Task 191 ; la carte OU-TROUVER portée à 284 ; D141 tenu avant le commit (le courant 283-7678421 archivé versionné au miroir) ; le commit porte l'atelier de construction ENTIER (scripts/campagne_d204/unite-01-C/ : les prompts, les sources, les épreuves, le kit, les scripts de montage et de livraison) et les journaux M2/M4 de la campagne ; le push GitHub ; le miroir Drive synchronisé. (14/11, la session du run vert de l'unité 1 et de la construction du bras C)
"""

WORKLOG = """

Task ID: 191
Agent: Z.ai (agent principal — la session du run vert de l'unité 1 × bras T et de la construction de l'unité loupe-01 × bras C)
Task: LE RUN DE L'UNITÉ 1 × BRAS T EST REVENU VERT (le kit v2 couru au terrain : 15 VERT 0 ROUGE, le témoin daté de la main 14/11/2026 et signé Alexis Lopez, T0 recoupé 4d119b22… == la gravure) — LA PREMIÈRE MESURE DE LA CAMPAGNE EST NÉE (CA1 : l'atelier, la ligne livraisons.csv T-loupe-01-it1 VERT recoupée par le labo, le carnet cristallisation 85 min) ; l'unité T-loupe-01 CLOSE à it1 (l'arrêt au premier vert recoupé, § 7) ; la session GUI consignée (six runs 1-clic, calibration VERT 0,000 s, deux absences nommées : le temoin-shani du rejeu geste-b D189, la réplication en attente des deux jeux).

Work Log:
- LE RECOUP DU RUN REVENU : le dossier « Nouveau run » du /test exploré (59 pièces rapatriées) — le témoin signé, la pièce recoupée à la gravure, le plan a78caf8c… == D204, le GUI intègre, l'atelier né, la ligne de livraison recoupée VERT ; preuves-unite01/ rendu ENTIER (le scénario n'écrit que le témoin — vérifié au source).
- LA CONSTRUCTION DU BRAS C (loupe-01 × C, le même contrat) : ONZE appels instrumentés 67 475 tokens LUS DU LOG (spec/oracle écrit-avant-code/source-c/7 correctifs/tests-c) ; la première édition tronquée trois fois par la limite de complétion — le format PATCH (les remplacements exacts + la suite) assemblé par l'outil auteur build_unite01C.py ; les défauts nommés avant correction (l'argument-cadre, la copie UTF-16, la double ouverture, les rondes MD5, la table S transposée, le compteur de tampon, le NUL à la capacité, les DEUX memset de gcc -O2 — la parade volatile) ; LES FAUTES DU LABO NOMMÉES (la prescription S[i % 16], l'étiquette AVANT inexacte, les offsets de la table d'export).
- LA COMPILATION : gcc-mingw-w64 14.2 croisé extrait des .deb SANS ROOT (aucun privilège) ; M4 journalisé (build 0,678 s, les suites, les contrôles — deux échecs de chemin nommés).
- LES ÉPREUVES D122 AU POSIX : la couche MD5+SHA-256 32 VERT 0 ROUGE ; le contrat entier 17 VERT 0 ROUGE (le harnais de la phase tests-c, son main complété par le labo — l'écart nommé) ; les contrôles binaires 16 VERT 0 ROUGE (aucun appel CRT dans la clôture — l'audit par adresses IAT) ; la découverte PE du scénario éprouvée.
- LA LIVRAISON : /test/kit-unite-loupe-01-C-20261114/ 12/12 + le bac du miroir 12/12, TOUT recoupé par re-téléchargement (24/24 VERT) ; les témoins octet pour octet ceux du kit T.
- LE GIT : D141 (le courant 283-7678421 en bundle versionné), le commit de l'Entrée 284 (l'atelier unite-01-C/ entier + les journaux M2/M4), le push GitHub au jeton ghp_ du /tokens.
- SUITE : au développeur — LA REPRISE de l'unité loupe-01 × C au GUI (onglet 1·KIT choisir le dossier, 2·RUN lancer, 3·TÉMOIN dater signer de la main, renvoyer preuves-unite01C/ ENTIER au /test) ; puis le labo recoupe et la campagne continue (loupe-02 × T ou l'appariement que le développeur arbitre).
"""

OU = """

11. **LE RUN VERT DE L'UNITÉ 1 × BRAS T + LA DEUXIÈME UNITÉ LOUPE-01 × BRAS C LIVRÉE (Entrée 284)** : le run revenu du terrain (le dossier « Nouveau run » au /test) — 15 VERT 0 ROUGE, le témoin daté et signé de la main (Alexis Lopez, 14/11/2026), T0 recoupé (loupe.exe 4d119b22… == la gravure) ; LA PREMIÈRE MESURE EST NÉE (CA1 : l'atelier, la ligne livraisons.csv T-loupe-01-it1 VERT recoupée par le labo, le carnet cristallisation 85 min) ; l'unité T-loupe-01 CLOSE à it1 (§ 7 : l'arrêt au premier vert recoupé) ; LE KIT DU BRAS C au /test/kit-unite-loupe-01-C-20261114/ (12/12 recoupés + 12/12 au bac du miroir) : la pièce loupe-01-c.dll (gcc -O2 -shared, 93 625 o, 85b34ed4…), le source loupe-01-c.c, le scénario adapté au PE compilé, les MÊMES témoins ; la construction mesurée (11 appels, 67 475 tokens LUS DU LOG) et éprouvée au labo (MD5+SHA-256 32 VERT ; le contrat entier 17 VERT au POSIX D122 ; les contrôles binaires 16 VERT — aucun appel CRT) ; LA REPRISE au GUI : onglet 1·KIT de l'unité loupe-01 × C choisir le dossier → 2·RUN → 3·TÉMOIN signé de la main → preuves-unite01C/ ENTIER au /test.
"""

with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(WORKLOG)
with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8",
          newline="\n") as f:
    f.write(JOURNAL)

# la carte OU-TROUVER : la section 11 + la portée rafraîchie
ou_path = REPO / "OU-TROUVER-LES-LIVRABLES.md"
ou = ou_path.read_text(encoding="utf-8")
ou += OU
ou, n1 = re.subn(r"Entrées 251-283", "Entrées 251-284", ou)
ou, n2 = re.subn(r"Tasks 158-190", "Tasks 158-191", ou)
assert n1 == 1 and n2 == 1, f"portées : {n1}, {n2}"
ou_path.write_text(ou, encoding="utf-8", newline="\n")
print("[consigné] worklog.md (Task 191) + JOURNAL_TRAVAIL.md (Entrée 284) "
      "+ OU-TROUVER portée à 284")

# ------------------------------------------------------------------
# 3. D141 — LE COURANT 283 ARCHIVÉ VERSIONNÉ
# ------------------------------------------------------------------
bundle = WORK / "triade-history-283-7678421.bundle"
if bundle.exists():
    bundle.unlink()
code, out, err = run("git", "bundle", "create", str(bundle), "--all")
assert code == 0, err
print(f"[D141] {bundle.name} : {bundle.stat().st_size:,} o")

# ------------------------------------------------------------------
# 4. LE COMMIT + LE PUSH
# ------------------------------------------------------------------
git("add", "worklog.md", "docs/JOURNAL_TRAVAIL.md",
    "OU-TROUVER-LES-LIVRABLES.md", "scripts/campagne_d204/unite-01-C/",
    "scripts/preuves_v150/comparaison_resultats/")
st = git("status", "--short")
print(f"[git] staged : {len(st.strip().splitlines())} chemin(s)")
sujet = ("Entrée 284 + Task 191 : LE RUN DE L'UNITÉ 1 × BRAS T REVENU "
         "VERT, RECOUPÉ — LA PREMIÈRE MESURE DE LA CAMPAGNE (CA1), "
         "L'UNITÉ CLOSE À IT1 (§ 7) ; LA DEUXIÈME UNITÉ LOUPE-01 × BRAS C "
         "CONSTRUITE, ÉPROUVÉE ET LIVRÉE : le témoin daté de la main et "
         "signé (14/11/2026, Alexis Lopez), T0 recoupé (4d119b22… == la "
         "gravure), 15 VERT 0 ROUGE, preuves-unite01/ rendu ENTIER ; "
         "l'atelier né du verrou, livraisons.csv T-loupe-01-it1 VERT "
         "(recoup « en attente » → RECOUPÉ VERT par le labo), le carnet "
         "cristallisation 85 min (M3), la session GUI (six runs 1-clic, "
         "calibration 0,000 s, le temoin-shani du geste-b NOMMÉ ABSENT "
         "D189, la réplication en attente des deux jeux) ; LE BRAS C : "
         "onze appels instrumentés 67 475 tokens LUS DU LOG (spec 5 605, "
         "oracle 4 423 écrit-avant-code, source-c 14 660, SEPT correctifs "
         "39 224, tests-c 3 563), la première édition tronquée trois fois "
         "— le format PATCH assemblé par l'outil auteur ; les défauts "
         "nommés avant correction (l'argument-cadre, la copie UTF-16, la "
         "double ouverture, les rondes MD5 2/4, la table S transposée, le "
         "compteur de tampon, le NUL à la capacité, les DEUX memset de "
         "gcc -O2 — la parade volatile) ET LES FAUTES DU LABO NOMMÉES "
         "(S[i % 16], l'étiquette AVANT inexacte, les offsets de la table "
         "d'export) ; la compilation gcc-mingw-w64 14.2 croisée extraite "
         "des .deb SANS ROOT ; les épreuves D122 : MD5+SHA-256 32 VERT, "
         "le contrat entier 17 VERT (le harnais tests-c, son main complété "
         "par le labo — l'écart nommé), les contrôles binaires 16 VERT "
         "(AUCUN appel CRT dans la clôture — l'audit par adresses IAT), "
         "la découverte PE éprouvée ; LE KIT au /test/kit-unite-loupe-01-"
         "C-20261114/ 12/12 + le bac du miroir 12/12 (24/24 recoupés par "
         "re-téléchargement), les témoins octet pour octet ceux du kit T ; "
         "LES ÉCARTS NOMMÉS : SetFilePointerEx absente (la lecture "
         "séquentielle), les imports du CRT de lancement jamais appelés ; "
         "LA REPRISE au GUI : 1·KIT choisir → 2·RUN lancer → 3·TÉMOIN "
         "signé de la main → preuves-unite01C/ ENTIER au /test ; la carte "
         "OU-TROUVER portée à 284 ; D141 tenu (le courant 283-7678421 "
         "archivé versionné)")
git("commit", "-m", sujet)
nouveau = git("rev-parse", "--short", "HEAD").strip()
print(f"[git] commit {nouveau}")

# le push — le jeton jamais imprimé
code, out, err = run("git", "push",
                     f"https://x-access-token:{token}@{GIT[8:]}",
                     "HEAD:main")
print((out + err).replace(token, "[JETON]"))
assert code == 0, "le push a refusé"
code, out, err = run("git", "ls-remote",
                     f"https://x-access-token:{token}@{GIT[8:]}",
                     "refs/heads/main")
print("ls-remote :", out.strip().split()[0][:12])
(WORK / "etat_git_284.json").write_text(json.dumps({
    "head": nouveau, "push": out.strip()}, indent=1))
print(f"[git] PUSH OK — main @ {nouveau}")
