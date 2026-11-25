#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-dudect-apple.py — L'ORCHESTRATEUR DU KIT-G (édition APPLE-SILICON, v1.0.0).

La commande (le développeur, 25/11/2026) : « si tu as des idées pour des
siliciums supplémentaires du même type que google collab (environnement
gratuit en ligne, mais hardware différent) ». LE SILICIUM APPLE (M1) vit
gratuitement en ligne sur les runners macOS des GitHub Actions (dépôt
public) : UNE AUTRE famille que le Cortex du téléphone, UNE AUTRE que le
Neoverse, UNE AUTRE que les Xeon/EPYC. Le présent script orchestre le
protocole APPLE-ARM-1 pré-enregistré au LISEZMOI-dudect-apple.txt AVANT
tout run (l'égalation de l'équation TELEPHONE-ARM-1, re-enregistrée pour
CE silicium) :

  T0 LA MACHINE ET LES PIÈCES   l'identité nommée (sysctl sur macOS,
       /proc/cpuinfo sur Linux — le canal absent est NOMMÉ) ; le sha256
       de dudect_apple.c ASSERTÉ contre le scellé ci-dessous (la pièce
       a bougé = REFUS, rien ne vit) ; le lecteur Python du FIPS « abc ».
  T1 LA COMPILATION      le compilateur trouvé (clang/gcc) — sur arm64,
       le drapeau -march=armv8-a+sha2 est essayé D'ABORD (s'il échoue,
       la compilation sobre vit — sur Apple Silicon le défaut du
       compilateur porte FEAT_SHA256 de facto, l'ÉPREUVE FIPS décide
       seule, nommée, jamais muette) ; le binaire naît dans run/, son
       sha256 consigné.
  T2 L'ÉPREUVE D'APPEL   ./run/dudect_apple --fips — le condensé FIPS
       « abc » EXACT exigé des lecteurs logiciel ET matériel (si
       compilé) : un lecteur faux est un REFUS, rien n'est mesuré
       (fail-closed — le même geste que le kit-B ; sur macOS où le canal
       noyau manque, C'EST cette épreuve qui garde la porte).
  T3 LES RUNS            TROIS exécutions dans l'ordre IMPOSÉ :
       N=60, puis N=200, puis N=400 (l'ordre du LISEZMOI-KITS-TERRAIN).
       La console de chaque run vit dans sortie-run-N<N>.txt ; le
       journal csv devient journal-dudect-apple-N<N>.csv ; le témoin
       temoin-dudect-apple-N<N>.txt est composé (machine, silicium,
       compilateur, empreintes, protocole, code de sortie, verdicts).
  T4 LA SYNTHÈSE         temoin-dudect-apple-SYNTHESE.txt — les trois
       runs, leurs codes, les verdicts par cible, la lecture honnête,
       la place de la signature. TOUT vit dans preuves-dudect-apple/.

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

DEST = "preuves-dudect-apple"
SOURCE = "dudect_apple.c"

# ---- LE SCELLE : le sha256 de la pièce dudect_apple.c livrée par ce kit ----
SCELLE_DUDECT_APPLE_C = ("6af573f6f30632e5a7538a2ad8f002b7"
                         "0e1bf3b0a4926b01652a4a962999a08b")

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
    """Le résumé du silicium : /proc/cpuinfo si le canal vit (Linux), le
    sysctl sinon (macOS — le canal /proc est ABSENT, nommé, jamais muet)."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8",
                  errors="replace") as f:
            texte = f.read()
        nb = texte.count("processor")
        sha2 = False
        for ligne in texte.splitlines():
            if ligne.startswith("Features"):
                sha2 = "sha2" in ligne.split() or any(
                    t == "sha2" for t in ligne.split(":", 1)[-1].split())
                break
        return f"{nb} cœur(s) · drapeau sha2 : " + ("PRÉSENT" if sha2
                                                    else "ABSENT")
    except OSError:
        pass
    # le canal /proc est absent (macOS) : le sysctl nommé
    morceaux = []
    for cle, etiquette in (("machdep.cpu.brand_string", "le CPU"),
                           ("hw.model", "le modèle"),
                           ("hw.ncpu", "les cœurs")):
        try:
            r = subprocess.run(["sysctl", "-n", cle],
                               capture_output=True, text=True, timeout=15)
            v = (r.stdout or "").strip()
            if v:
                morceaux.append(f"{etiquette} : {v}")
        except Exception:                    # noqa: BLE001 — refus nommé
            pass
    if morceaux:
        return " · ".join(morceaux) + " (le canal sysctl — /proc absent " \
               "sur macOS, nommé)"
    return "aucun canal d'identité lisible (le témoin le constate tel quel)"


def trouver_cc():
    for c in ("clang", "gcc", "cc"):
        p = shutil.which(c)
        if p:
            return c
    return None


def compiler(cc, machine):
    """Compile la pièce ; sur arm64 le +sha2 d'abord, la version sobre en
    repli (sur Apple Silicon le défaut porte FEAT_SHA256 de facto :
    l'ÉPREUVE FIPS décide seule — nommée, jamais muette)."""
    essais = []
    if machine in ("aarch64", "armv8l", "arm64"):
        essais.append([cc, "-O2", "-march=armv8-a+sha2",
                       "-o", "run/dudect_apple", SOURCE, "-lm"])
    essais.append([cc, "-O2", "-o", "run/dudect_apple", SOURCE, "-lm"])
    for i, cmd in enumerate(essais):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and os.path.exists("run/dudect_apple"):
            materiel = "+sha2" in " ".join(cmd)
            return (True, " ".join(cmd),
                    "AVEC le drapeau +sha2 (la cible matérielle vivra si "
                    "l'ÉPREUVE FIPS l'accepte — sur macOS le canal noyau "
                    "manque, l'épreuve décide seule)" if materiel else
                    "SANS le drapeau +sha2 (sur Apple Silicon le défaut "
                    "du compilateur porte FEAT_SHA256 de facto — "
                    "l'ÉPREUVE FIPS décide seule, nommée, jamais muette)",
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
        f"APPLE-ARM-1 — échantillons entrelacés)",
        f"Code du run   : {code}",
        f"Le binaire    : run/dudect_apple (sha256 {sha_binaire[:16]}…)",
        f"L'origine     : {origine}",
        f"La machine    : {machine}",
        f"Le silicium   : {silicium}",
        "",
        "LA MACHINE DE COMMODITÉ SE NOMME (D206) : le run Apple Silicon "
        "vit sur un runner MUTUALISÉ aux voisins inconnus ; l'affinité "
        "n'est PAS posable sur macOS (nommée au binaire — le t sera "
        "bruité, constaté tel quel) ; la hiérarchie d'évidence est "
        "INCHANGÉE — le banc contrôlé (portable, téléphone) demeure la "
        "référence.",
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
        "  - vos observations, mêmes défavorables (D189 : rapporter tel "
        "quel).",
        "",
        "PUIS : datez et signez de votre main sous ces lignes, et "
        "renvoyez le dossier preuves-dudect-apple/ ENTIER au coffre "
        "/test (dossier Drive « Triade » → « test »). Le labo recoupe "
        "sur pièces : jamais avant le run, jamais sans pièces.",
    ]
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")


def main():
    global _journal
    os.makedirs(DEST, exist_ok=True)
    os.makedirs("run", exist_ok=True)
    _journal = open(os.path.join(DEST, "scenario-dudect-apple-journal.log"),
                    "w", encoding="utf-8")

    journal("=== scenario-dudect-apple.py — L'ORCHESTRATEUR DU KIT-G "
            "(édition APPLE-SILICON, 25/11/2026) ===")

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
                f"dossier kit-G-apple-dudect/ ENTIER — D99)")
        return 2
    empreinte = sha256_fichier(SOURCE)
    journal(f"T0.piece — sha256({SOURCE}) = {empreinte}")
    if empreinte != SCELLE_DUDECT_APPLE_C:
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
                "(clang/gcc/cc). Sur macOS (Xcode Command Line Tools) : "
                "xcode-select --install  puis relancez.")
        return 2
    version = subprocess.run([cc, "--version"], capture_output=True,
                             text=True, timeout=60)
    premiere = (version.stdout or "?").strip().splitlines()[0]
    journal(f"T1.compilateur — {cc} : {premiere}")
    ok, cmd, materiel_phrase, _ = compiler(cc, platform.machine())
    if not ok:
        journal("T1.compilation — REFUS NOMMÉ : la compilation a échoué "
                "(les écarts sont consignés ci-dessus). Le labo "
                "recoupera la cause avec vous — renvoyez ce journal.")
        return 2
    journal(f"T1.compilation — VÉCUE : {cmd}")
    journal(f"T1.compilation — {materiel_phrase}")
    sha_binaire = sha256_fichier("run/dudect_apple")
    journal(f"T1.binaire — run/dudect_apple sha256 {sha_binaire}")
    origine = (f"RECOMPILÉ SUR CETTE MACHINE ({cmd} — la source est la "
               f"vérité)")

    # ---- T2 L'ÉPREUVE D'APPEL ----
    journal("T2.epreuve — ./run/dudect_apple --fips (le condensé FIPS "
            "« abc » EXACT exigé avant toute mesure ; sur macOS où le "
            "canal noyau manque, C'EST cette épreuve qui garde la porte)")
    r = subprocess.run(["./run/dudect_apple", "--fips"],
                       capture_output=True, text=True, timeout=120)
    with open(os.path.join(DEST, "sortie-epreuve-fips.txt"), "w",
              encoding="utf-8") as f:
        f.write(r.stdout + r.stderr)
    for l in (r.stdout + r.stderr).strip().splitlines():
        journal(f"T2.epreuve — {l}")
    if r.returncode != 0:
        journal(f"T2.epreuve — REFUS : code {r.returncode} — un lecteur "
                "est faux, RIEN ne sera mesuré (fail-closed)")
        return 2
    journal("T2.epreuve — VÉCUE : les lecteurs sont exacts")

    # ---- T3 LES RUNS ----
    entetes = [
        "LE TÉMOIN DUDECT-APPLE — N{N} (édition APPLE-SILICON, kit-G, v1.0.0)",
        "=" * 64,
        f"L'horodatage  : {datetime.datetime.now().isoformat(timespec='seconds')}",
        f"La pièce      : dudect_apple.c sha256 {empreinte}",
        "Le protocole  : APPLE-ARM-1 (l'égalation du TELEPHONE-ARM-1, "
        "pré-enregistrée au LISEZMOI-dudect-apple.txt AVANT tout run)",
        "Les cibles    : eq-constant (contrôle positif), eq-branchue "
        "(contrôle négatif), sha256-logiciel, sha256-arm-sha2 (si le "
        "compilateur l'expose ET que l'épreuve FIPS l'accepte — sur "
        "macOS le canal noyau manque, l'épreuve décide seule)",
    ]
    codes = {}
    for n in LES_N:
        journal(f"T3.run — N={n} par classe : LE RUN (quelques minutes)")
        r = subprocess.run(["./run/dudect_apple", str(n)],
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
                      if f.startswith("journal-dudect-apple-")
                      and f.endswith(".csv"))
        if csvs:
            shutil.move(csvs[-1],
                        os.path.join(DEST, f"journal-dudect-apple-N{n}.csv"))
            journal(f"T3.run N={n} — journal csv consigné")

        dernieres = console.strip().splitlines()[-8:]
        composer_temoin(
            os.path.join(DEST, f"temoin-dudect-apple-N{n}.txt"),
            [l.replace("{N}", str(n)) for l in entetes],
            n, r.returncode, dernieres, sha_binaire, origine,
            machine, silicium)
        journal(f"T3.run N={n} — témoin composé : temoin-dudect-apple-N{n}.txt")

    # ---- T4 LA SYNTHÈSE ----
    synthese = [
        "LA SYNTHÈSE DUDECT-APPLE — édition APPLE-SILICON, kit-G, v1.0.0",
        "=" * 64,
        f"La machine    : {machine}",
        f"Le silicium   : {silicium}",
        f"La pièce      : dudect_apple.c sha256 {empreinte}",
        f"Le binaire    : run/dudect_apple sha256 {sha_binaire}",
        f"L'origine     : {origine}",
        f"Le compilateur: {premiere}",
        "",
        "LES TROIS RUNS (l'ordre imposé du protocole) :",
    ] + [f"  N={n} — code {codes[n]} (sortie-run-N{n}.txt, "
         f"journal-dudect-apple-N{n}.csv, temoin-dudect-apple-N{n}.txt)"
         for n in LES_N] + [
        "",
        "LA LECTURE HONNÊTE (le protocole entier vit au "
        "LISEZMOI-dudect-apple.txt) :",
        "  — |t| > 5 = dépendance AU SEUIL sur CET échantillon, "
        "consignée telle quelle ;",
        "  — |t| <= 5 = aucune divergence au seuil sur cet échantillon, "
        "CETTE machine — jamais « temps constant prouvé » ;",
        "  — le contrôle négatif eq-branchue DOIT diverger (sinon "
        "l'instrument est CONTESTÉ — nommé) ;",
        "  — le rapport médian logiciel/materiel est LE CONSTAT DE CE "
        "SILICIUM (jamais une cible : aucune cible pré-enregistrée "
        "n'existe pour Apple Silicon) ;",
        "  — l'affinité n'est PAS posable sur macOS (nommée) : le t sera "
        "bruité, constaté tel quel.",
        "",
        "LES RÉFÉRENCES : le kit-B du téléphone (le même instrument sur "
        "le Cortex-A78, FEAT_SHA256, rapport 4,36 — Entrée 424) ; le "
        "kit-C COLLAB (Entrée 426) ; le coffre /test pour le retour des "
        "preuves.",
        "",
        "signature du geste : à dater et à signer de la main du "
        "développeur.",
    ]
    with open(os.path.join(DEST, "temoin-dudect-apple-SYNTHESE.txt"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(synthese) + "\n")

    vert = all(c == 0 for c in codes.values())
    journal(f"T4.synthese — les codes : "
            + ", ".join(f"N{n}={codes[n]}" for n in LES_N))
    journal("T4.synthese — le réceptacle preuves-dudect-apple/ : journal, "
            "épreuve FIPS, trois sorties, trois csv, trois témoins, "
            "synthèse")
    journal("T4.synthese — À VOTRE MAIN : datez et signez la synthèse, "
            "renvoyez le dossier ENTIER au coffre /test")

    print()
    print("=" * 64)
    print(" LE KIT-G EST VÉCU. Les preuves vivent dans preuves-dudect-apple/")
    print(" (journal, épreuve FIPS, 3 sorties, 3 csv, 3 témoins, synthèse).")
    print(" À VOTRE MAIN : datez, signez, renvoyez le dossier ENTIER au")
    print(" coffre /test (dossier Drive « Triade »).")
    print("=" * 64)
    _journal.close()
    return 0 if vert else 3


if __name__ == "__main__":
    sys.exit(main())
