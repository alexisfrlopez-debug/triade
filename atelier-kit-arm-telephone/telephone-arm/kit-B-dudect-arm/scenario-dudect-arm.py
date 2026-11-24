#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-dudect-arm.py — L'ORCHESTRATEUR DU KIT-B (édition TÉLÉPHONE, v1.0.0).

La commande (le développeur, 25/11/2026) : « tu peux me faire un kit de
test arm/pour téléphone si nécessaire ». Le kit-B ÉPROUVE le troisième
silicium là où le kit-A (constat-arm.py, le correctif n° 3 du 12/11)
le CONSTATE. Le présent script orchestre le protocole TELEPHONE-ARM-1
pré-enregistré au LISEZMOI-dudect-arm.txt AVANT tout run :

  T0 LA MACHINE ET LES PIÈCES   l'identité nommée ; le sha256 de
       dudect_arm.c ASSERTÉ contre le scellé ci-dessous (la pièce a
       bougé = REFUS, rien ne vit) ; le lecteur Python du FIPS « abc ».
  T1 LA COMPILATION      le compilateur trouvé (clang/gcc) — sur
       aarch64, le drapeau -march=armv8-a+sha2 est essayé D'ABORD (il
       n'expose QUE la cible matérielle ; s'il échoue, la compilation
       sobre vit et la cible matérielle est REFUSÉE PAR NATURE — nommée,
       jamais muette) ; le binaire naît dans run/, son sha256 consigné.
  T2 L'ÉPREUVE D'APPEL   ./run/dudect_arm --fips — le condensé FIPS
       « abc » EXACT exigé des lecteurs logiciel ET matériel (si
       présent) : un lecteur faux est un REFUS, rien n'est mesuré
       (fail-closed — le même geste que test_appel au kit-2).
  T3 LES RUNS            TROIS exécutions dans l'ordre IMPOSÉ :
       N=60, puis N=200, puis N=400 (l'ordre du LISEZMOI-KITS-TERRAIN).
       La console de chaque run vit dans sortie-run-N<N>.txt ; le
       journal csv devient journal-dudect-arm-N<N>.csv ; le témoin
       temoin-dudect-arm-N<N>.txt est composé (machine, silicium,
       compilateur, empreintes, protocole, code de sortie, verdicts).
  T4 LA SYNTHÈSE         temoin-dudect-arm-SYNTHESE.txt — les trois
       runs, leurs codes, les verdicts par cible, la lecture honnête,
       la place de la signature. TOUT vit dans preuves-dudect-arm/.

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

DEST = "preuves-dudect-arm"
SOURCE = "dudect_arm.c"

# ---- LE SCELLE : le sha256 de la pièce dudect_arm.c livrée par ce kit ----
SCELLE_DUDECT_ARM_C = "08681278e0efe013ff9e6379eff8ea02219f04a6bdbcb59b4a5d2a1016474a32"

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


def lire_cpuinfo_resume():
    """Le résumé du silicium : les Features (le jeton sha2 EXACT)."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8",
                  errors="replace") as f:
            texte = f.read()
    except OSError as e:
        return f"</proc/cpuinfo illisible : {type(e).__name__}>"
    nb = texte.count("processor")
    sha2 = False
    for ligne in texte.splitlines():
        if ligne.startswith("Features"):
            sha2 = "sha2" in ligne.split() or any(
                t == "sha2" for t in ligne.split(":", 1)[-1].split())
            break
    return f"{nb} cœur(s) · drapeau sha2 : " + ("PRÉSENT" if sha2
                                                else "ABSENT")


def getprop(nom):
    exe = shutil.which("getprop") or "/system/bin/getprop"
    if not os.path.exists(exe):
        return None
    try:
        r = subprocess.run([exe, nom], capture_output=True, timeout=10)
        v = r.stdout.decode("utf-8", "replace").strip()
        return v or None
    except Exception:                        # noqa: BLE001 — refus nommé
        return None


def trouver_cc():
    for c in ("clang", "gcc", "cc"):
        p = shutil.which(c)
        if p:
            return c
    return None


def compiler(cc, machine):
    """Compile la pièce ; sur aarch64 le +sha2 d'abord, la version sobre en
    repli (la cible matérielle est alors REFUSÉE PAR NATURE — nommée)."""
    essais = []
    if machine in ("aarch64", "armv8l", "arm64"):
        essais.append([cc, "-O2", "-march=armv8-a+sha2",
                       "-o", "run/dudect_arm", SOURCE, "-lm"])
    essais.append([cc, "-O2", "-o", "run/dudect_arm", SOURCE, "-lm"])
    for i, cmd in enumerate(essais):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and os.path.exists("run/dudect_arm"):
            materiel = "+sha2" in " ".join(cmd)
            return (True, " ".join(cmd),
                    "AVEC le drapeau +sha2 (la cible matérielle vivra "
                    "si le noyau expose « sha2 »)" if materiel else
                    "SANS le drapeau +sha2 (la cible matérielle est "
                    "REFUSÉE PAR NATURE — nommée, jamais muette)",
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
        f"TELEPHONE-ARM-1 — échantillons entrelacés)",
        f"Code du run   : {code}",
        f"Le binaire    : run/dudect_arm (sha256 {sha_binaire[:16]}…)",
        f"L'origine     : {origine}",
        f"La machine    : {machine}",
        f"Le silicium   : {silicium}",
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
        "  - l'état EFFECTIF du gouverneur de fréquence (DVFS) pendant "
        "le run, si vous le connaissez ;",
        "  - vos observations, mêmes défavorables (D189 : rapporter tel "
        "quel).",
        "",
        "PUIS : datez et signez de votre main sous ces lignes, et "
        "renvoyez le dossier preuves-dudect-arm/ ENTIER au coffre /test "
        "(dossier Drive « Triade » → « test »). Le labo recoupe sur "
        "pièces : jamais avant le run, jamais sans pièces.",
    ]
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")


def main():
    global _journal
    os.makedirs(DEST, exist_ok=True)
    os.makedirs("run", exist_ok=True)
    _journal = open(os.path.join(DEST, "scenario-dudect-arm-journal.log"),
                    "w", encoding="utf-8")

    journal("=== scenario-dudect-arm.py — L'ORCHESTRATEUR DU KIT-B "
            "(édition TÉLÉPHONE, 25/11/2026) ===")

    # ---- T0 LA MACHINE ET LES PIÈCES ----
    try:
        uname = " ".join(os.uname())
    except AttributeError:
        uname = platform.platform()
    machine_nom = platform.node() or "<sans-nom>"
    machine = (f"{machine_nom} · {platform.machine()} · "
               f"Python {sys.version.split()[0]} · {uname}")
    journal(f"T0.machine — {machine}")
    silicium = lire_cpuinfo_resume()
    journal(f"T0.silicium — {silicium}")
    modele = getprop("ro.product.model") or getprop("ro.product.device")
    if modele:
        journal(f"T0.android — modèle {modele}")
    rendu = hashlib.sha256(b"abc").hexdigest()
    journal(f"T0.lecteur python sha256(abc) = {rendu[:16]}… — "
            f"{'EXACT' if rendu == ABC_SHA256 else 'DIVERGENT'}")
    if rendu != ABC_SHA256:
        journal("T0.lecteur — REFUS : le lecteur Python est faux")
        return 2

    if not os.path.exists(SOURCE):
        journal(f"T0.piece — REFUS : {SOURCE} est ABSENT (copiez le "
                f"dossier kit-B-dudect-arm/ ENTIER — D99)")
        return 2
    empreinte = sha256_fichier(SOURCE)
    journal(f"T0.piece — sha256({SOURCE}) = {empreinte}")
    if empreinte != SCELLE_DUDECT_ARM_C:
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
                "(clang/gcc/cc). Le lanceur du kit l'installe par "
                "« pkg install clang » ; à la main : "
                "« pkg install clang » puis relancez.")
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
    sha_binaire = sha256_fichier("run/dudect_arm")
    journal(f"T1.binaire — run/dudect_arm sha256 {sha_binaire}")
    origine = (f"RECOMPILÉ SUR CETTE MACHINE ({cmd} — la source est la "
               f"vérité)")

    # ---- T2 L'ÉPREUVE D'APPEL ----
    journal("T2.epreuve — ./run/dudect_arm --fips (le condensé FIPS "
            "« abc » EXACT exigé avant toute mesure)")
    r = subprocess.run(["./run/dudect_arm", "--fips"],
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
        "LE TÉMOIN DUDECT-ARM — N{N} (édition TÉLÉPHONE, kit-B, v1.0.0)",
        "=" * 64,
        f"L'horodatage  : {datetime.datetime.now().isoformat(timespec='seconds')}",
        f"La pièce      : dudect_arm.c sha256 {empreinte}",
        "Le protocole  : TELEPHONE-ARM-1 (pré-enregistré au "
        "LISEZMOI-dudect-arm.txt AVANT tout run)",
        "Les cibles    : eq-constant (contrôle positif), eq-branchue "
        "(contrôle négatif), sha256-logiciel, sha256-arm-sha2 (si le "
        "noyau expose « sha2 » et le compilateur +sha2)",
    ]
    codes = {}
    for n in LES_N:
        journal(f"T3.run — N={n} par classe : LE RUN (quelques secondes)")
        r = subprocess.run(["./run/dudect_arm", str(n)],
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
                      if f.startswith("journal-dudect-arm-")
                      and f.endswith(".csv"))
        if csvs:
            shutil.move(csvs[-1],
                        os.path.join(DEST, f"journal-dudect-arm-N{n}.csv"))
            journal(f"T3.run N={n} — journal csv consigné")

        dernieres = console.strip().splitlines()[-8:]
        composer_temoin(
            os.path.join(DEST, f"temoin-dudect-arm-N{n}.txt"),
            [l.replace("{N}", str(n)) for l in entetes],
            n, r.returncode, dernieres, sha_binaire, origine,
            machine, silicium)
        journal(f"T3.run N={n} — témoin composé : temoin-dudect-arm-N{n}.txt")

    # ---- T4 LA SYNTHÈSE ----
    synthese = [
        "LA SYNTHÈSE DUDECT-ARM — édition TÉLÉPHONE, kit-B, v1.0.0",
        "=" * 64,
        f"La machine    : {machine}",
        f"Le silicium   : {silicium}",
        f"La pièce      : dudect_arm.c sha256 {empreinte}",
        f"Le binaire    : run/dudect_arm sha256 {sha_binaire}",
        f"L'origine     : {origine}",
        f"Le compilateur: {premiere}",
        "",
        "LES TROIS RUNS (l'ordre imposé du protocole) :",
    ] + [f"  N={n} — code {codes[n]} (sortie-run-N{n}.txt, "
         f"journal-dudect-arm-N{n}.csv, temoin-dudect-arm-N{n}.txt)"
         for n in LES_N] + [
        "",
        "LA LECTURE HONNÊTE (le protocole entier vit au "
        "LISEZMOI-dudect-arm.txt) :",
        "  — |t| > 5 = dépendance AU SEUIL sur CET échantillon, "
        "consignée telle quelle ;",
        "  — |t| <= 5 = aucune divergence au seuil sur cet échantillon, "
        "CETTE machine — jamais « temps constant prouvé » ;",
        "  — le contrôle négatif eq-branchue DOIT diverger (sinon "
        "l'instrument est CONTESTÉ — nommé) ;",
        "  — le rapport médian logiciel/materiel est LE CONSTAT DE CE "
        "SILICIUM (jamais une cible : aucune cible pré-enregistrée "
        "n'existe pour ARM).",
        "",
        "LES RÉFÉRENCES : kit-A (constat-arm.py) pour l'identité "
        "complète ; le coffre /test pour le retour des preuves.",
        "",
        "signature du geste : à dater et à signer de la main du "
        "développeur.",
    ]
    with open(os.path.join(DEST, "temoin-dudect-arm-SYNTHESE.txt"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(synthese) + "\n")

    vert = all(c == 0 for c in codes.values())
    journal(f"T4.synthese — les codes : "
            + ", ".join(f"N{n}={codes[n]}" for n in LES_N))
    journal("T4.synthese — le réceptacle preuves-dudect-arm/ : journal, "
            "épreuve, trois sorties, trois csv, trois témoins, synthèse")
    journal("T4.synthese — À VOTRE MAIN : datez et signez la synthèse, "
            "renvoyez le dossier ENTIER au coffre /test")

    print()
    print("=" * 64)
    print(" LE KIT-B EST VÉCU. Les preuves vivent dans preuves-dudect-arm/")
    print(" (journal, épreuve FIPS, 3 sorties, 3 csv, 3 témoins, synthèse).")
    print(" À VOTRE MAIN : datez, signez, renvoyez le dossier ENTIER au")
    print(" coffre /test (dossier Drive « Triade »).")
    print("=" * 64)
    _journal.close()
    return 0 if vert else 3


if __name__ == "__main__":
    sys.exit(main())
