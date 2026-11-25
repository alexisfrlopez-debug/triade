#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-dudect-s390x.py — L'ORCHESTRATEUR DU KIT-E (édition LINUXONE, v1.0.0).

La commande (le développeur, 25/11/2026) : « si tu as des idées pour des
siliciums supplémentaires du même type que google collab (environnement
gratuit en ligne, mais hardware différent) ». LE SILICIUM IBM Z (s390x)
est le plus loin de la famille — une ISA de mainframe. Le présent script
orchestre le protocole LINUXONE-S390X-1 pré-enregistré au
LISEZMOI-dudect-s390x.txt AVANT tout run :

  T0 LA MACHINE ET LES PIÈCES   l'identité nommée ; le sha256 de
       dudect_s390x.c ASSERTÉ contre le scellé ci-dessous (la pièce
       a bougé = REFUS, rien ne vit) ; le lecteur Python du FIPS « abc ».
  T1 LA COMPILATION      le compilateur trouvé (gcc) ; le binaire naît
       dans run/, son sha256 consigné. La cible matérielle n'existe PAS
       dans cette édition : KIMD/KLMD sont SUPERVISEUR — REFUSÉE PAR
       NATURE, nommée (jamais muette).
  T2 L'ÉPREUVE D'APPEL   ./run/dudect_s390x --fips — le condensé FIPS
       « abc » EXACT exigé du lecteur logiciel : un lecteur faux est un
       REFUS, rien n'est mesuré (fail-closed).
  T3 LES RUNS            TROIS exécutions dans l'ordre IMPOSÉ :
       N=60, puis N=200, puis N=400 (l'ordre du LISEZMOI-KITS-TERRAIN).
       La console de chaque run vit dans sortie-run-N<N>.txt ; le
       journal csv devient journal-dudect-s390x-N<N>.csv ; le témoin
       temoin-dudect-s390x-N<N>.txt est composé (machine, silicium,
       compilateur, empreintes, protocole, code de sortie, verdicts).
  T4 LA SYNTHÈSE         temoin-dudect-s390x-SYNTHESE.txt — les trois
       runs, leurs codes, les verdicts par cible, la lecture honnête,
       la place de la signature. TOUT vit dans preuves-dudect-s390x/.

Aucun réseau. Python SEUL (stdlib). Aucun droit particulier.
Codes de sortie : 0 = les trois runs vécus ; 2 = REFUS NOMMÉ (pièce
divergente, compilation impossible, épreuve FIPS fausse) ; 3 = un run
s'est interrompu (l'écart est nommé au témoin — la sortie console est
conservée telle quelle, D189).
"""

import datetime
import hashlib
import os
import platform
import shutil
import subprocess
import sys

DEST = "preuves-dudect-s390x"
SOURCE = "dudect_s390x.c"

# ---- LE SCELLE : le sha256 de la pièce dudect_s390x.c livrée par ce kit ----
SCELLE_DUDECT_S390X_C = ("a9f702a3c2d337bb50217f134a7535f1"
                         "6e1da0ad7afd53ba4b0cac9e56a67301")

# ---- le FIPS 180-4 « abc » (le lecteur Python du scénario) ----
ABC_SHA256 = ("ba7816bf8f01cfea414140de5dae2223"
              "b00361a396177a9cb410ff61f20015ad")

LES_N = [60, 200, 400]          # l'ordre IMPOSÉ du protocole

_journal = None


def journal(ligne):
    print(f"[journal] {ligne}")
    if _journal is not None:
        _journal.write(
            f"{datetime.datetime.now().isoformat(timespec='seconds')} "
            f"{ligne}\n")
        _journal.flush()


def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def lire_silicium():
    """Le résumé du silicium : /proc/cpuinfo LU GÉNÉRIQUEMENT (le s390x
    y nomme « vendor » et « machine » — le canal vit, il se lit)."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8",
                  errors="replace") as f:
            texte = f.read()
    except OSError as e:
        return f"</proc/cpuinfo illisible : {type(e).__name__}>"
    nb = texte.count("processor")
    indices = []
    for ligne in texte.splitlines():
        cle = ligne.split(":", 1)[0].strip().lower()
        if cle in ("model name", "vendor", "machine", "cpu"):
            indices.append(ligne.strip())
            if len(indices) >= 2:
                break
    detail = " · ".join(indices) if indices else "<modele illisible>"
    return f"{nb} cœur(s) · {detail}"


def trouver_cc():
    for c in ("gcc", "clang", "cc"):
        p = shutil.which(c)
        if p:
            return c
    return None


def compiler(cc):
    """Compile la pièce (la compilation sobre suffit : aucune cible
    matérielle ne vit dans cette édition — KIMD/KLMD SUPERVISEUR)."""
    essais = [
        [cc, "-O2", "-o", "run/dudect_s390x", SOURCE, "-lm"],
    ]
    for i, cmd in enumerate(essais):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and os.path.exists("run/dudect_s390x"):
            return (True, " ".join(cmd),
                    "la compilation sobre (aucune cible matérielle dans "
                    "cette édition : KIMD/KLMD sont SUPERVISEUR — "
                    "REFUSÉES PAR NATURE, nommées, jamais muettes)",
                    r)
        journal(f"T1.compilation — l'essai n° {i+1} a échoué : "
                f"code {r.returncode}")
        for l in (r.stderr or "").strip().splitlines()[:5]:
            journal(f"T1.compilation écart — {l}")
    return (False, "", "", r)


def composer_temoin(chemin, entetes, run_n, code, console_dernieres,
                    sha_binaire, origine, machine, silicium):
    lignes = entetes + [
        f"Le run        : N={run_n} par classe (le protocole "
        f"LINUXONE-S390X-1 — échantillons entrelacés)",
        f"Code du run   : {code}",
        f"Le binaire    : run/dudect_s390x (sha256 {sha_binaire[:16]}…)",
        f"L'origine     : {origine}",
        f"La machine    : {machine}",
        f"Le silicium   : {silicium}",
        "",
        "LA MACHINE DE COMMODITÉ SE NOMME (D206) : le run s390x vit sur "
        "une machine d'accès gratuit (la porte ouverte par le maître — "
        "Z Xplore ou toute autre) ; le compteur est l'HORLOGE DU NOYAU "
        "en nanosecondes, NOMMÉE, jamais déguisée en cycles ; la "
        "hiérarchie d'évidence est INCHANGÉE — le banc contrôlé "
        "(portable, téléphone) demeure la référence.",
        "",
        "LES DERNIÈRES LIGNES DE LA CONSOLE (la sortie complète vit "
        "dans sortie-run-N%d.txt) :" % run_n,
        ""] + ["  " + l for l in console_dernieres] + [
        "",
        "LA LECTURE HONNÊTE : |t| > 5 = dépendance AU SEUIL sur CET "
        "échantillon, consignée telle quelle ; |t| <= 5 = aucune "
        "divergence au seuil sur cet échantillon, CETTE machine — "
        "jamais « temps constant prouvé ».",
        "",
        "À COMPLÉTER DE VOTRE MAIN (le mesureur ne peut pas le lire à "
        "votre place) :",
        "  - l'état EFFECTIF du gouverneur de fréquence pendant le run, "
        "si vous le connaissez (le Z gouverne sa cadence — constatez-le "
        "tel quel) ;",
        "  - vos observations, mêmes défavorables (D189 : rapporter tel "
        "quel).",
        "",
        "PUIS : datez et signez de votre main sous ces lignes, et "
        "renvoyez le dossier preuves-dudect-s390x/ ENTIER au coffre "
        "/test (dossier Drive « Triade » → « test »). Le labo recoupe "
        "sur pièces : jamais avant le run, jamais sans pièces.",
    ]
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")


def main():
    global _journal
    os.makedirs(DEST, exist_ok=True)
    os.makedirs("run", exist_ok=True)
    _journal = open(os.path.join(DEST, "scenario-dudect-s390x-journal.log"),
                    "w", encoding="utf-8")

    journal("=== scenario-dudect-s390x.py — L'ORCHESTRATEUR DU KIT-E "
            "(édition LINUXONE, 25/11/2026) ===")

    # ---- T0 LA MACHINE ET LES PIÈCES ----
    try:
        uname = " ".join(os.uname())
    except AttributeError:
        uname = platform.platform()
    machine_nom = platform.node() or "<sans-nom>"
    machine = (f"{machine_nom} · {platform.machine()} · "
               f"Python {sys.version.split()[0]} · {uname}")
    journal(f"T0.machine — {machine}")
    silicium = lire_silicium()
    journal(f"T0.silicium — {silicium}")
    rendu = hashlib.sha256(b"abc").hexdigest()
    journal(f"T0.lecteur python sha256(abc) = {rendu[:16]}… — "
            f"{'EXACT' if rendu == ABC_SHA256 else 'DIVERGENT'}")
    if rendu != ABC_SHA256:
        journal("T0.lecteur — REFUS : le lecteur Python est faux")
        return 2

    if not os.path.exists(SOURCE):
        journal(f"T0.piece — REFUS : {SOURCE} est ABSENT (copiez le "
                f"dossier kit-E-dudect-s390x/ ENTIER — D99)")
        return 2
    empreinte = sha256_fichier(SOURCE)
    journal(f"T0.piece — sha256({SOURCE}) = {empreinte}")
    if empreinte != SCELLE_DUDECT_S390X_C:
        journal("T0.piece — REFUS : l'empreinte DIVERGE du scellé — la "
                "pièce a bougé, RIEN ne sera compilé ni exécuté. "
                "Re-extrayez le zip COMPLET dans un dossier NEUF (D99).")
        return 2
    journal("T0.piece — l'empreinte recoupe le scellé : la pièce est la "
            "pièce du labo")

    # ---- T1 LA COMPILATION ----
    cc = trouver_cc()
    if cc is None:
        journal("T1.compilateur — REFUS NOMMÉ : aucun compilateur "
                "(gcc/clang/cc). Sur Ubuntu/RHEL s390x : "
                "sudo apt-get install -y gcc  (ou dnf install gcc) "
                "puis relancez. Le lanceur du kit tente l'installation "
                "lui-même s'il peut.")
        return 2
    version = subprocess.run([cc, "--version"], capture_output=True,
                             text=True, timeout=60)
    premiere = (version.stdout or "?").strip().splitlines()[0]
    journal(f"T1.compilateur — {cc} : {premiere}")
    ok, cmd, materiel_phrase, _ = compiler(cc)
    if not ok:
        journal("T1.compilation — REFUS NOMMÉ : la compilation a échoué "
                "(les écarts sont consignés ci-dessus). Le labo "
                "recoupera la cause avec vous — renvoyez ce journal.")
        return 2
    journal(f"T1.compilation — VÉCUE : {cmd}")
    journal(f"T1.compilation — {materiel_phrase}")
    sha_binaire = sha256_fichier("run/dudect_s390x")
    journal(f"T1.binaire — run/dudect_s390x sha256 {sha_binaire}")
    origine = (f"RECOMPILÉ SUR CETTE MACHINE ({cmd} — la source est la "
               f"vérité)")

    # ---- T2 L'ÉPREUVE D'APPEL ----
    journal("T2.epreuve — ./run/dudect_s390x --fips (le condensé FIPS "
            "« abc » EXACT exigé avant toute mesure)")
    r = subprocess.run(["./run/dudect_s390x", "--fips"],
                       capture_output=True, text=True, timeout=120)
    with open(os.path.join(DEST, "sortie-epreuve-fips.txt"), "w",
              encoding="utf-8") as f:
        f.write(r.stdout + r.stderr)
    for l in (r.stdout + r.stderr).strip().splitlines():
        journal(f"T2.epreuve — {l}")
    if r.returncode != 0:
        journal(f"T2.epreuve — REFUS : code {r.returncode} — le lecteur "
                "est faux, RIEN ne sera mesuré (fail-closed)")
        return 2
    journal("T2.epreuve — VÉCUE : le lecteur est exact")

    # ---- T3 LES RUNS ----
    entetes = [
        "LE TÉMOIN DUDECT-S390X — N{N} (édition LINUXONE, kit-E, v1.0.0)",
        "=" * 64,
        f"L'horodatage  : {datetime.datetime.now().isoformat(timespec='seconds')}",
        f"La pièce      : dudect_s390x.c sha256 {empreinte}",
        "Le protocole  : LINUXONE-S390X-1 (pré-enregistré au "
        "LISEZMOI-dudect-s390x.txt AVANT tout run)",
        "Les cibles    : eq-constant (contrôle positif), eq-branchue "
        "(contrôle négatif), sha256-logiciel — la cible matérielle est "
        "REFUSÉE PAR NATURE (KIMD/KLMD SUPERVISEUR, nommée)",
    ]
    codes = {}
    for n in LES_N:
        journal(f"T3.run — N={n} par classe : LE RUN (quelques minutes)")
        r = subprocess.run(["./run/dudect_s390x", str(n)],
                           capture_output=True, text=True, timeout=1800)
        codes[n] = r.returncode
        console = r.stdout + r.stderr
        chemin_console = os.path.join(DEST, f"sortie-run-N{n}.txt")
        with open(chemin_console, "w", encoding="utf-8") as f:
            f.write(console)
        for l in console.strip().splitlines():
            print(f"  {l}")
        journal(f"T3.run N={n} — code de sortie {r.returncode}")

        # le journal csv du run : renommé au nom de son N
        csvs = sorted(f for f in os.listdir(".")
                      if f.startswith("journal-dudect-s390x-")
                      and f.endswith(".csv"))
        if csvs:
            shutil.move(csvs[-1],
                        os.path.join(DEST, f"journal-dudect-s390x-N{n}.csv"))
            journal(f"T3.run N={n} — journal csv consigné")

        dernieres = console.strip().splitlines()[-8:]
        composer_temoin(
            os.path.join(DEST, f"temoin-dudect-s390x-N{n}.txt"),
            [l.replace("{N}", str(n)) for l in entetes],
            n, r.returncode, dernieres, sha_binaire, origine,
            machine, silicium)
        journal(f"T3.run N={n} — témoin composé : temoin-dudect-s390x-N{n}.txt")

    # ---- T4 LA SYNTHÈSE ----
    synthese = [
        "LA SYNTHÈSE DUDECT-S390X — édition LINUXONE, kit-E, v1.0.0",
        "=" * 64,
        f"La machine    : {machine}",
        f"Le silicium   : {silicium}",
        f"La pièce      : dudect_s390x.c sha256 {empreinte}",
        f"Le binaire    : run/dudect_s390x sha256 {sha_binaire}",
        f"L'origine     : {origine}",
        f"Le compilateur: {premiere}",
        "",
        "LES TROIS RUNS (l'ordre imposé du protocole) :",
    ] + [f"  N={n} — code {codes[n]} (sortie-run-N{n}.txt, "
         f"journal-dudect-s390x-N{n}.csv, temoin-dudect-s390x-N{n}.txt)"
         for n in LES_N] + [
        "",
        "LA LECTURE HONNÊTE (le protocole entier vit au "
        "LISEZMOI-dudect-s390x.txt) :",
        "  — |t| > 5 = dépendance AU SEUIL sur CET échantillon, "
        "consignée telle quelle ;",
        "  — |t| <= 5 = aucune divergence au seuil sur cet échantillon, "
        "CETTE machine — jamais « temps constant prouvé » ;",
        "  — le contrôle négatif eq-branchue DOIT diverger (sinon "
        "l'instrument est CONTESTÉ — nommé) ;",
        "  — le compteur est l'HORLOGE DU NOYAU en nanosecondes "
        "(NOMMÉE, jamais déguisée en cycles).",
        "",
        "LES RÉFÉRENCES : le kit-2 du 24/11 (la machine n° 1) ; le kit-B "
        "du téléphone ; le kit-C COLLAB (Entrée 426) ; le coffre /test "
        "pour le retour des preuves.",
        "",
        "signature du geste : à dater et à signer de la main du "
        "développeur.",
    ]
    with open(os.path.join(DEST, "temoin-dudect-s390x-SYNTHESE.txt"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(synthese) + "\n")

    vert = all(c == 0 for c in codes.values())
    journal(f"T4.synthese — les codes : "
            + ", ".join(f"N{n}={codes[n]}" for n in LES_N))
    journal("T4.synthese — le réceptacle preuves-dudect-s390x/ : journal, "
            "épreuve FIPS, trois sorties, trois csv, trois témoins, "
            "synthèse")
    journal("T4.synthese — À VOTRE MAIN : datez et signez la synthèse, "
            "renvoyez le dossier ENTIER au coffre /test")

    print()
    print("=" * 64)
    print(" LE KIT-E EST VÉCU. Les preuves vivent dans preuves-dudect-s390x/")
    print(" (journal, épreuve FIPS, 3 sorties, 3 csv, 3 témoins, synthèse).")
    print(" À VOTRE MAIN : datez, signez, renvoyez le dossier ENTIER au")
    print(" coffre /test (dossier Drive « Triade »).")
    print("=" * 64)
    _journal.close()
    return 0 if vert else 3


if __name__ == "__main__":
    sys.exit(main())
