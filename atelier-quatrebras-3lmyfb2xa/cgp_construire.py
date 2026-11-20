#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cgp_construire.py — LA CONSTRUCTION DU BRAS C+G+ (3lmyfb2xa, la vague
11, le PLAN-3LMYFB2XA gelé) : le C gcc-O2 des SIX unités D210 recevant la
gouvernance (les gestes g1-g4 du bras C+G, vague 10) ET LE RÉGIME DE
VÉRIFICATION COMPLET DU BRAS T ADAPTÉ AU COMPILÉ :

  (1) LES REBUILDS DE CRISTALLISATION — chaque unité recompilée DIX fois,
      les octets confrontés : l'équivalent compilé du round-trip (la
      reproductibilité du build gcc -O2 aux sources et drapeaux gelés),
      DOCUMENTÉ comme l'équivalent, JAMAIS confondu avec le round-trip de
      notation (l'octet juge keystone↔capstone du bras T) ;
  (2) LES VOLUMES ORACLE ÉQUIVALENTS — le même nombre d'épreuves de
      contrat que le bras T aux mêmes unités : u01 DOUZE épreuves /
      QUATORZE contrôles, u02 2032 décalages (la même graine 20261114) ;
  (3) LA RECOMPOSITION DU PLAN — le graphe de dépendances des sources
      re-vérifié à chaque livraison (le plan gelé cgp-plan.json).

LA CONSTRUCTION (avant toute mesure) : le corpus, les volumes SOURCÉS du
registre vague 10 et recoupés à la recomputation, le plan gelé, la
validation des harnais, LES FALSIFICATIONS (le régime vit : le rebuild
muté REFUSÉ, le graphe muté REFUSÉ, l'épreuve mutée ROUGE).

Sortie : cgp-plan.json · cgp-corpus/ · rapport-cgp-construction.txt."""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-quatrebras-3lmyfb2xa"
CG = REPO / "atelier-cg-3a91o5whb"
V10 = CG / "m4-avant-run1.json"          # le registre T vague 10 (sourcing)
MINGW = pathlib.Path("/home/z/my-project/work/mingw-debs/root/usr/bin/"
                     "x86_64-w64-mingw32-gcc-posix")
GCC_NATIF = pathlib.Path("/usr/bin/gcc")
MINGW_INC = MINGW.parent.parent / "x86_64-w64-mingw32" / "include"
CORPUS = ICI / "cgp-corpus"

# L'ORDRE STRATIFIÉ PAR FAMILLE (le plan § 2, l'ordre du bras C+G reconduit)
U01C = REPO / "scripts" / "campagne_d204" / "unite-01-C"
U02C = REPO / "scripts" / "campagne_d204" / "unite-02-C"
UNITES = [
    ("loupe-01", "ouvrir",
     "scripts/campagne_d204/unite-01-C/source/loupe-01-c.c",
     "loupe/I/loupe-01-ouvrir.md",
     ["scripts/campagne_d204/unite-01-C/epreuves",
      "scripts/campagne_d204/unite-01-C/source"]),
    ("loupe-02", "lire",
     "scripts/campagne_d204/unite-02-C/source/loupe-02-c.c",
     "loupe/I/loupe-02-lire.md",
     ["scripts/campagne_d204/unite-02-C/epreuves",
      "scripts/campagne_d204/unite-02-C/source"]),
    ("loupe-05", "hachage",
     "atelier-cg-3a91o5whb/loupe-05-c.c",
     "loupe/I/loupe-05-sha256.md",
     []),
    ("loupe-08", "composition",
     "scripts/campagne_d204/unite-08-C/source/loupe-08-c.c",
     "loupe/I/loupe-08-ligne.md",
     []),
    ("loupe-13", "recherche",
     "scripts/campagne_d204/unite-13-C/source/loupe-13-c.c",
     "loupe/I/loupe-13-recherche.md",
     []),
    ("loupe-16", "saisie",
     "scripts/campagne_d204/attribution-unite16-C-353/source-loupe-16-C.c",
     "loupe/I/loupe-16-saisie.md",
     []),
]

HARNAIS_CAMPAGNE = [
    "scripts/campagne_d204/unite-01-C/source/loupe-01-c.def",
    "scripts/campagne_d204/unite-01-C/epreuves/epreuve_posix.c",
    "scripts/campagne_d204/unite-01-C/epreuves/windows.h",
    "scripts/campagne_d204/unite-01-C/epreuves/compare_epreuve.py",
    "scripts/campagne_d204/unite-01-C/epreuves/controles_binaires.py",
    "scripts/campagne_d204/unite-01-C/epreuve_hash_posix.py",
    "scripts/campagne_d204/unite-01-C/epreuves/testeur_hash.c",
    "scripts/campagne_d204/unite-02-C/source/loupe-02-c.def",
    "scripts/campagne_d204/unite-02-C/epreuves/epreuve_posix.c",
    "scripts/campagne_d204/unite-02-C/epreuves/windows.h",
    "scripts/campagne_d204/unite-02-C/epreuves/compare_epreuve.py",
    "scripts/campagne_d204/unite-02-C/epreuves/controles_binaires.py",
]
HARNAIS_MOI = [
    "atelier-quatrebras-3lmyfb2xa/cgp_oracle_u01.c",
    "atelier-quatrebras-3lmyfb2xa/cgp_juge_u01.py",
    "atelier-quatrebras-3lmyfb2xa/cgp_oracle_u02.c",
    "atelier-quatrebras-3lmyfb2xa/cgp_juge_u02.py",
    "atelier-quatrebras-3lmyfb2xa/cgp_recomposition.py",
]
GOUVERNANCE = [
    "atelier-cg-3a91o5whb/cg_gouverne.py",
    "atelier-cg-3a91o5whb/cristallisation/chaine.json",
    "atelier-cg-3a91o5whb/cle_session_lab.pub",
]
OUTIL = [MINGW, GCC_NATIF, MINGW_INC / "windows.h",
         MINGW_INC / "stdint.h", MINGW_INC / "string.h",
         pathlib.Path("/usr/include/stdint.h")]

TEMOINS = ["temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "vide.bin"]


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inclussions(src_texte: str) -> list[str]:
    return re.findall(r'^\s*#\s*include\s*[<"]([^>"]+)[>"]', src_texte, re.M)


def run(cmd, cwd=None, timeout=600):
    """Le lanceur : les commandes « cd … && … » courent au shell (le
    modèle de cg_m4.une_etape), les listes directement."""
    shell = isinstance(cmd, str) or (cmd and cmd[0] == "cd")
    args = " ".join(cmd) if isinstance(cmd, list) and cmd and \
        cmd[0] == "cd" else cmd
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout, shell=shell)


def main() -> int:
    rapport = ["LE BRAS C+G+ — LA CONSTRUCTION (3lmyfb2xa, la vague 11, "
               "le plan gelé PLAN-3LMYFB2XA.md)",
               "le C gcc-O2 des six unités D210 RECEVANT la gouvernance "
               "g1-g4 ET le régime de vérification complet du bras T "
               "adapté au compilé", ""]
    code = 0

    # ---- 0. L'ENVIRONNEMENT : le REPO gelé de l'outil vague 9 -----------
    lien = pathlib.Path("/tmp/triade-gh")
    if not lien.exists():
        lien.symlink_to(REPO)
        rapport.append("L'ENVIRONNEMENT : /tmp/triade-gh (le REPO gelé de "
                       "l'outil_m4_v182 et des oracles v180) RECÉÉ par "
                       "symlink vers le dépôt — la machine a perdu l'ancien "
                       "(NOMMÉ)")
    else:
        cible = pathlib.Path(lien.resolve())
        assert cible == REPO, f"/tmp/triade-gh pointe ailleurs : {cible}"
        rapport.append("L'ENVIRONNEMENT : /tmp/triade-gh présent (le REPO "
                       "gelé de l'outil vague 9 → le dépôt)")
    r = run(["python3", "v06/sceau_I.py", "verifier"], cwd=REPO)
    sceau_avant = (r.returncode == 0
                   and "14 arbres VERTS" in r.stdout + r.stderr)
    rapport.append(f"LES SCELLÉS AVANT CONSTRUCTION : "
                   f"{'14 arbres VERTS' if sceau_avant else 'ROUGE'} "
                   f"(sceau_I verifier)")
    if not sceau_avant:
        return 2

    # ---- 1. LE CORPUS (les témoins + le scellé lu en copie) ------------
    CORPUS.mkdir(exist_ok=True)
    for n in TEMOINS:
        shutil.copy2(U01C / "epreuves" / n, CORPUS / n)
        if sha(CORPUS / n) != sha(U02C / "epreuves" / n):
            rapport.append(f"  !! le témoin {n} DIVERGE entre u01 et u02 — "
                           "ROUGE")
            code |= 2
    shutil.copy2(REPO / "tls13" / "proxy.exe", CORPUS / "proxy.exe")
    rapport.append("LE CORPUS : les QUATRE témoins copiés des épreuves de "
                   "campagne (recoupés u01 == u02 octet à octet) + "
                   "proxy.exe le SCELLÉ tls13 LU EN COPIE (l'original "
                   "jamais touché — la lecture est le geste de l'oracle T "
                   "même, quatrième fichier du différentiel)")

    # ---- 2. LES VOLUMES DU BRAS T (sourcés au registre vague 10) --------
    v10 = json.loads(V10.read_text(encoding="utf-8"))
    oracle_u01 = next(e for e in v10["etapes"]
                      if e["etape"].startswith("oracle-bloc-loupe-01"))
    oracle_u02 = next(e for e in v10["etapes"]
                      if e["etape"].startswith("oracle-du-bloc-loupe-02"))
    m = re.search(r"L'ORACLE DU BLOC : (\d+) VERT, (\d+) ROUGE",
                  oracle_u01["console"])
    u01_controles_t = int(m.group(1))
    # les épreuves T u01 comptées de la structure de l'oracle (4 V1 + 3 V2
    # + 4 V3 + 1 V4 — les vecteurs nommés à la console)
    u01_epreuves_t = 12
    par_fichier_t = {}
    for mm in re.finditer(r"V1:(\S+)-la-fenetre-bornee-a-(\d+)-decalages",
                          oracle_u02["console"]):
        par_fichier_t[mm.group(1)] = int(mm.group(2))
    u02_decalages_t = sum(par_fichier_t.values())
    m2 = re.search(r"L'ORACLE DU BLOC : (\d+) VERT, (\d+) ROUGE",
                   oracle_u02["console"])
    u02_controles_t = int(m2.group(1))

    # la RECOMPUTATION (la même graine, le même ordre de consommation)
    sys.path.insert(0, str(ICI))
    import cgp_juge_u02 as juge02
    juge02.ICI = CORPUS
    par_fichier_moi = {n: len(v) for n, v in
                       juge02.listes_attendues().items()}
    u02_decalages_moi = sum(par_fichier_moi.values())
    volumes_ok = (par_fichier_moi == par_fichier_t
                  and u01_controles_t == 14 and u02_controles_t == 22)
    verdict_volumes = ("ÉGAUX, le volume gelé" if volumes_ok
                       else "DIVERGENT — ROUGE")
    rapport += [
        "LES VOLUMES ORACLE DU BRAS T — SOURCÉS au registre vague 10 "
        f"({V10.name}) et RECOUPÉS à la recomputation (la graine "
        "20261114, la même consommation du rng) :",
        f"  u01 : {u01_epreuves_t} épreuves (4 V1 + 3 V2 + 4 V3 + 1 V4, "
        f"la structure de l'oracle) / {u01_controles_t} contrôles (la "
        f"console : {u01_controles_t} VERT)",
        f"  u02 : {u02_decalages_t} décalages "
        + " ; ".join(f"{k}={v}" for k, v in par_fichier_t.items())
        + f" / {u02_controles_t} contrôles (la console)",
        f"  LA RECOMPUTATION : {u02_decalages_moi} décalages "
        + " ; ".join(f"{k}={v}" for k, v in par_fichier_moi.items())
        + f" — {verdict_volumes}",
    ]
    if not volumes_ok:
        code |= 2

    # ---- 3. LE PLAN GELÉ (le graphe de dépendances des sources) --------
    chaine = json.loads((CG / "cristallisation" / "chaine.json")
                        .read_text(encoding="utf-8"))
    dll_chaine = {u["unite"]: u["sha256_dll"] for u in chaine["chaine"]}
    unites_plan = []
    for nom, famille, src_rel, spec_rel, chemins in UNITES:
        src = REPO / src_rel
        texte = src.read_text(encoding="utf-8")
        deps, systeme = {}, []
        for inc in inclussions(texte):
            resolu = None
            for cand in chemins:
                c = REPO / cand / inc
                if c.exists():
                    resolu = c
                    break
            if resolu is not None:
                deps[str(resolu.relative_to(REPO))] = sha(resolu)
            else:
                systeme.append(inc)
        unites_plan.append({
            "unite": nom, "famille": famille, "source": src_rel,
            "sha256_source": sha(src), "spec": spec_rel,
            "sha256_spec": sha(REPO / spec_rel),
            "includes": list(deps.keys()), "systeme": systeme,
            "chemins_recherche": chemins, "deps": deps,
            "dll_chaine": dll_chaine[nom],
        })
    plan = {
        "genese": "cgp-3lmyfb2xa (vague 11) — le plan gelé AVANT toute "
                  "mesure (PLAN-3LMYFB2XA.md)",
        "unites": unites_plan,
        "harnais": {rel: sha(REPO / rel)
                    for rel in HARNAIS_CAMPAGNE + HARNAIS_MOI},
        "gouvernance": {rel: sha(REPO / rel) for rel in GOUVERNANCE},
        "outil": {str(p): sha(p) for p in OUTIL},
        "outil_mingw_version": "gcc 14.2.0-19+27+b1, binutils 2.44-3+12+b1,"
                               " mingw-w64 12.0.0-5 (TRIXIE, la chaîne "
                               "gelée)",
        "corpus": {f"cgp-corpus/{n}": sha(CORPUS / n)
                   for n in TEMOINS + ["proxy.exe"]},
        "volumes": {
            "u01_epreuves": u01_epreuves_t, "u01_controles": u01_controles_t,
            "u02_decalages": u02_decalages_t,
            "u02_par_fichier": par_fichier_t, "u02_integrations": 4,
            "u02_controles_t": u02_controles_t,
            "rebuilds_par_unite": 10,
        },
    }
    (ICI / "cgp-plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    rapport += [
        "LE PLAN GELÉ : cgp-plan.json — les SIX unités (la source, ses "
        "inclusions de dépôt recoupées à l'octet, les inclusions système "
        "portées par la chaîne d'outil gelée, la spec signée, le DLL "
        "attendu de la chaîne vague 10), les " + str(len(plan["harnais"]))
        + " harnais d'épreuve, les " + str(len(plan["gouvernance"]))
        + " artefacts de gouvernance vague 10 reçus, l'OUTIL (la chaîne "
        "mingw + le gcc natif + les en-têtes), le corpus",
    ]

    # ---- 4. LA VALIDATION DES HARNAIS (une exécution hors mesure) ------
    cmd_u01 = (f"cd {CORPUS} && gcc -O2 -I{U01C}/source -I{U01C}/epreuves "
               f"-o cgp_oracle_u01 {ICI}/cgp_oracle_u01.c && "
               f"./cgp_oracle_u01 > cgp-sortie-u01.txt && python3 "
               f"{ICI}/cgp_juge_u01.py cgp-sortie-u01.txt")
    r01 = run(cmd_u01.split(), cwd=REPO)
    ok01 = r01.returncode == 0 and "12 épreuves, 14 contrôles" in r01.stdout
    rapport += [
        "LA VALIDATION DU HARNAIS u01 : " + ("VERT — " if ok01 else "ROUGE"
                                             " — ")
        + (r01.stdout.strip().splitlines()[-1] if r01.stdout.strip()
           else r01.stderr[-200:]),
    ]
    cmd_u02 = (f"cd {CORPUS} && python3 {ICI}/cgp_juge_u02.py --prepare && "
               f"gcc -O2 -I{U02C}/epreuves -I{U02C}/source "
               f"-o cgp_oracle_u02 {ICI}/cgp_oracle_u02.c && "
               f"./cgp_oracle_u02 > cgp-sortie-u02.txt && python3 "
               f"{ICI}/cgp_juge_u02.py --juge cgp-sortie-u02.txt")
    r02 = run(cmd_u02.split(), cwd=REPO)
    ok02 = r02.returncode == 0
    rapport += [
        "LA VALIDATION DU HARNAIS u02 : " + ("VERT — " if ok02 else "ROUGE"
                                             " — ")
        + (r02.stdout.strip().splitlines()[-1] if r02.stdout.strip()
           else r02.stderr[-200:]),
    ]
    rrec = run(["python3", str(ICI / "cgp_recomposition.py")], cwd=REPO)
    okrec = rrec.returncode == 0
    rapport.append("LA VALIDATION DE LA RECOMPOSITION : "
                   + ("VERT" if okrec else "ROUGE — " + rrec.stdout[-300:]))
    if not (ok01 and ok02 and okrec):
        code |= 2

    # ---- 5. LES FALSIFICATIONS (le régime vit) --------------------------
    import cgp_m4 as m4
    tmp = ICI / "cgp-falsif"
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / "r1").mkdir(parents=True)
    rb = run([str(MINGW), "-O2", "-shared", "-o", "loupe-01-cg.dll",
              str(REPO / UNITES[0][2])], cwd=tmp / "r1")
    octets = (tmp / "r1" / "loupe-01-cg.dll").read_bytes()
    honnete = m4.confrontre([octets, octets])
    mute = bytearray(octets)
    mute[5000] ^= 0xFF
    refuse = not m4.confrontre([octets, bytes(mute)])
    rapport += [
        "LA FALSIFICATION (rebuilds) : le canonique honnête CONFRONTÉ "
        f"VERT ({honnete}) ; l'OCTET MUTÉ (un octet de code hors champs "
        f"d'horodatage) REFUSÉ ({refuse}) — la confrontation vit (les "
        "TROIS champs d'horodatage du PE seuls épargnés : l'en-tête "
        "TimeDateStamp, la somme de contrôle, le TimeDateStamp du "
        "répertoire d'exports — l'heure du lien PAR CONSTRUCTION du "
        "format, jamais une divergence de compilation)",
    ]
    if not (honnete and refuse):
        code |= 2
    # la démonstration de l'embarquement des chemins (l'écart nommé) :
    (tmp / "r2").mkdir()
    run([str(MINGW), "-O2", "-shared", "-o", "loupe-01-cg.dll",
         str(REPO / UNITES[0][2])], cwd=tmp / "r2")
    autre = (tmp / "r2" / "loupe-01-cg.dll").read_bytes()
    diffs = [i for i, (a, b) in enumerate(zip(octets, autre)) if a != b]
    masques = m4.masques_pe(octets)
    hors_masques = [d for d in diffs
                    if not any(a <= d < b for a, b in masques)]
    rapport.append(
        "L'ÉCART NOMMÉ (le chemin du lien embarqué) : deux builds au "
        "MÊME -o RELATIF en répertoires hermétiques distincts divergent "
        f"en {len(hors_masques)} octet HORS horodatage — la confrontation "
        "hermétique est SÛRE (le -o relatif gelé neutralise "
        "l'embarquement) ; mais le build d'origine de la chaîne vague 10 "
        f"(sha dll {dll_chaine['loupe-01'][:12]}…) portait un -o ABSOLU à "
        "l'atelier cg : son sha n'est reproductible qu'à CE chemin — "
        "l'écrire exigerait de toucher l'atelier vague 10 (INTERDIT) : la "
        "confrontation est INTRA-LOT (les DIX rebuilds entre eux), la "
        "liaison à la chaîne portée par les SOURCES (la recomposition "
        "recoupe sha256_source == la chaîne signée)")

    rf = run(["python3", str(ICI / "cgp_recomposition.py"), "--falsifie"],
             cwd=REPO)
    rapport.append("LA FALSIFICATION (recomposition) : le hash de la "
                   "source muté dans la copie en mémoire "
                   + ("REFUSÉ (exit 2 — le graphe vit)"
                      if rf.returncode == 2 else "ADMIS — ROUGE"))
    if rf.returncode != 2:
        code |= 2

    # les juges : une épreuve mutée → ROUGE
    s01 = (CORPUS / "cgp-sortie-u01.txt").read_text(encoding="utf-8")
    i01 = s01.index("tampon=") + len("tampon=")
    mutant01 = s01[:i01] + ("0" if s01[i01] != "0" else "1") \
        + s01[i01 + 1:]
    (CORPUS / "cgp-sortie-u01-mutee.txt").write_text(mutant01,
                                                     encoding="utf-8")
    rm1 = run(["python3", str(ICI / "cgp_juge_u01.py"),
               "cgp-sortie-u01-mutee.txt"], cwd=CORPUS)
    s02 = (CORPUS / "cgp-sortie-u02.txt").read_text(encoding="utf-8")
    i_ep = s02.index("tampon=") + len("tampon=")
    mutant02 = s02[:i_ep] + ("0" if s02[i_ep] != "0" else "1") + s02[i_ep + 1:]
    (CORPUS / "cgp-sortie-u02-mutee.txt").write_text(mutant02,
                                                     encoding="utf-8")
    rm2 = run(["python3", str(ICI / "cgp_juge_u02.py"), "--juge",
               "cgp-sortie-u02-mutee.txt"], cwd=CORPUS)
    rapport.append("LA FALSIFICATION (les juges) : l'épreuve u01 mutée "
                   + ("ROUGE (refus)" if rm1.returncode == 2
                      else "ADMISE — ROUGE")
                   + " ; le décalage u02 muté "
                   + ("ROUGE (refus)" if rm2.returncode == 2
                      else "ADMIS — ROUGE"))
    if rm1.returncode != 2 or rm2.returncode != 2:
        code |= 2
    shutil.rmtree(tmp, ignore_errors=True)

    # ---- 6. LA TABLE DES VOLUMES PAR UNITÉ ------------------------------
    rapport += [
        "",
        "LA TABLE DES VOLUMES PAR UNITÉ (le régime de vérification, "
        "compté par unité et par session — le plan § 2) :",
        "  loupe-01 : T = cristallisation 12 rebuilds CONCURRENTS + 2 "
        "round-trips R5 + oracle 12 épreuves / 14 contrôles || "
        "C+G+ = 10 rebuilds confrontés + oracle équivalent 12 épreuves / "
        "14 contrôles + la base C (le build .def, la suite hash, le "
        "contrat 10 vecteurs, les contrôles binaires)",
        "  loupe-02 : T = build-recomposition + oracle 2032 décalages / "
        "22 contrôles + épreuve scénario + kits || C+G+ = 10 rebuilds + "
        "oracle équivalent 2032 décalages (la même graine) + la base C + "
        "LA RECOMPOSITION DU PLAN (le graphe re-vérifié)",
        "  loupe-05 : T = rien par session (l'unité close sur son rouge à "
        "la cap, M1) || C+G+ = 10 rebuilds — l'ECHEC de build "
        "cristallisé (le sha256_dll de la chaîne EST « ECHEC », les 10 "
        "échecs confrontés à l'octet de stderr)",
        "  loupe-08 : T = rien par session || C+G+ = 10 rebuilds confrontés",
        "  loupe-13 : T = rien par session || C+G+ = 10 rebuilds confrontés",
        "  loupe-16 : T = rien par session || C+G+ = 10 rebuilds confrontés",
        "  LES ASYMÉTRIES NOMMÉES : le bras T cristallise 12 rebuilds de "
        "la SEULE unité 01 (+2 round-trips) ; le plan C+G+ gèle DIX "
        "rebuilds par unité aux SIX unités (60 compilations par session) "
        "— la table publie les comptes, jamais fusionnés",
    ]

    (ICI / "rapport-cgp-construction.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    print(f"\n=== CONSTRUCTION : {'VERT' if code == 0 else 'ROUGE'} "
          f"(code {code}) ===")
    return code


if __name__ == "__main__":
    sys.exit(main())
