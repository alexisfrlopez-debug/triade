#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-kaggle.py — L'ORCHESTRATEUR DU KIT-C (édition KAGGLE x86-64, v1.0.0).

La commande (le développeur, 25/11/2026) : « si tu as des idées pour des
siliciums supplémentaires du même type que google collab (environnement
gratuit en ligne, mais hardware différent) fais moi les packs de test
correspondants ». Kaggle Notebooks EST ce type d'environnement : gratuit,
en ligne, notebook — le silicium y est UN AUTRE serveur x86-64 de commodité
(les hôtes GPU/TPU changent la race des sessions : T4, P100, TPU —
CONSTATÉS au témoin, jamais mesurés par ce kit). Le kit-C pose LA MÊME
QUESTION que l'édition COLLAB (l'avis de l'Entrée 421) : les trois
divergences |t|>5 du 24/11 au portable SUIVENT-ELLES LA MACHINE OU LE
CODE ? Un point de plus sur un AUTRE silicium serveur — la lecture
appartient au labo, sur pièces. Le présent script orchestre le protocole
KAGGLE-X86-1 — l'ÉGALATION du protocole COLLAB-X86-1, pré-enregistrée au
LISEZMOI-dudect-kaggle.txt AVANT tout run :

  T0 LA MACHINE ET LES PIÈCES   l'identité nommée (la machine de
       commodité SE NOMME, D206) ; l'accélérateur CONSTATÉ (nvidia-smi
       s'il vit : le GPU est NOMMÉ, jamais mesuré — l'instrument mesure
       le CPU) ; le sha256 de dudect_collab.c ASSERTÉ contre le scellé
       ci-dessous (la pièce a bougé = REFUS, rien ne vit) ; le sha256 de
       l'image scellée cibles/proxy-image.bin ASSERTÉ ; le lecteur Python
       du FIPS « abc ».
  T1 LA COMPILATION      le compilateur trouvé (gcc) — les drapeaux
       -msha -mssse3 -msse4.1 sont essayés D'ABORD ; s'ils échouent, la
       compilation sobre vit et la cible est REFUSÉE PAR NATURE — nommée,
       jamais muette ; le binaire naît dans run/, son sha256 consigné.
  T2 L'ÉPREUVE D'APPEL   ./run/dudect_collab --fips — le condensé FIPS
       « abc » EXACT exigé des TROIS lecteurs : logiciel, SHA-NI (s'il
       vit) ET LA PIÈCE SCELLÉE tls13-02 (avec l'adversaire de mutation
       K). Un lecteur faux est un REFUS, rien n'est mesuré (fail-closed).
  T3 LES RUNS            TROIS exécutions dans l'ordre IMPOSÉ :
       N=60, puis N=200, puis N=400. La console de chaque run vit dans
       sortie-run-N<N>.txt ; le journal csv devient
       journal-dudect-kaggle-N<N>.csv ; le témoin
       temoin-dudect-kaggle-N<N>.txt est composé (machine, silicium,
       accélérateur, mutualisation, compilateur, empreintes, protocole,
       code de sortie, verdicts).
  T4 LA SYNTHÈSE ET LE RETOUR      temoin-dudect-kaggle-SYNTHESE.txt —
       les trois runs, leurs codes, les verdicts par cible, la lecture
       honnête, la place de la signature — PUIS LE ZIP DE RETOUR
       preuves-kaggle-<horodatage>.zip (la session Kaggle est ÉPHÉMÈRE :
       téléchargez le zip AVANT la fin, et sauvegardez le notebook pour
       que /kaggle/working vive dans la version enregistrée). TOUT vit
       dans preuves-kaggle/.

Aucun réseau hors l'éventuelle installation de paquets (le lanceur s'en
charge). Python SEUL (stdlib). Aucun droit particulier.
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
import zipfile

DEST = "preuves-kaggle"
SOURCE = "dudect_collab.c"

# ---- LES SCELLÉS : les sha256 des pièces livrées par ce kit ----
# dudect_collab.c, cibles/proxy-image.bin et cibles/manifeste-c.txt sont
# les pièces BYTE-POUR-BYTE de l'édition COLLAB (Entrée 425) — la question
# est la même, le terrain change ; les scellés ne bougent pas.
SCELLE_DUDECT_COLLAB_C = ("ae698c2916c67fe25f7a5662fb932675"
                          "a2e8c5023f838cafe5ad3a8d00daca0d")
SCELLE_PROXY_IMAGE = ("0782d7e20d0bd4a268e6ec7ed0dc1453"
                      "a0f42d7e72b784c2acc9ed423a885dff")
SCELLE_MANIFESTE_C = ("7293cd86359cebba81d590173a49c462"
                      "f876cf5ce8b639d5c26c2577713ea5d8")

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
    """Le résumé du silicium : le modèle, les cœurs, les drapeaux nommés
    (sha_ni, hypervisor, constant_tsc, nonstop_tsc — le jeton EXACT)."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8",
                  errors="replace") as f:
            texte = f.read()
    except OSError as e:
        return f"</proc/cpuinfo illisible : {type(e).__name__}>"
    nb = texte.count("processor")
    modele = "<modele illisible>"
    for ligne in texte.splitlines():
        if ligne.startswith("model name"):
            modele = ligne.split(":", 1)[-1].strip()
            break
    drapeaux = []
    for ligne in texte.splitlines():
        if ligne.startswith("flags"):
            jetons = ligne.split(":", 1)[-1].split()
            for nom in ("sha_ni", "hypervisor", "constant_tsc",
                        "nonstop_tsc"):
                if nom in jetons:
                    drapeaux.append(nom)
            break
    return (f"{nb} cœur(s) · {modele} · drapeaux : "
            + (", ".join(drapeaux) if drapeaux
               else "AUCUN des quatre nommés"))


def constat_accelerateur():
    """L'accélérateur CONSTATÉ (nvidia-smi s'il vit) — le GPU/TPU est
    NOMMÉ au témoin, JAMAIS mesuré par ce kit (l'instrument mesure le
    CPU ; la voie GPU demanderait un instrument à pré-enregistrer)."""
    exe = shutil.which("nvidia-smi")
    if not exe:
        return "aucun accélérateur NVIDIA constaté (session CPU — nommé)"
    try:
        r = subprocess.run([exe, "--query-gpu=name,compute_cap",
                            "--format=csv,noheader"],
                           capture_output=True, text=True, timeout=30)
        retour = (r.stdout or "").strip()
        if retour:
            return f"GPU NVIDIA constaté (nvidia-smi) : {retour} — NOMMÉ, " \
                   "jamais mesuré par ce kit"
        return "nvidia-smi vit mais ne nomme aucun GPU (constaté tel quel)"
    except Exception as e:                    # noqa: BLE001 — refus nommé
        return f"nvidia-smi présent mais muet ({type(e).__name__} — nommé)"


def trouver_cc():
    for c in ("gcc", "clang", "cc"):
        p = shutil.which(c)
        if p:
            return c
    return None


def compiler(cc):
    """Compile la pièce ; les drapeaux SHA-NI d'abord, la version sobre
    en repli (la cible matérielle est alors REFUSÉE PAR NATURE — nommée)."""
    essais = [
        [cc, "-O2", "-msha", "-mssse3", "-msse4.1",
         "-o", "run/dudect_collab", SOURCE, "-lm"],
        [cc, "-O2", "-o", "run/dudect_collab", SOURCE, "-lm"],
    ]
    for i, cmd in enumerate(essais):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and os.path.exists("run/dudect_collab"):
            materiel = "-msha" in cmd
            return (True, " ".join(cmd),
                    "AVEC les drapeaux -msha -mssse3 -msse4.1 (la cible "
                    "matérielle SHA-NI vivra si le noyau expose « sha_ni »)"
                    if materiel else
                    "SANS les drapeaux SHA-NI (la cible matérielle est "
                    "REFUSÉE PAR NATURE — nommée, jamais muette)",
                    r)
        journal(f"T1.compilation — l'essai n° {i+1} a échoué : "
                f"code {r.returncode}")
        for l in (r.stderr or "").strip().splitlines()[:5]:
            journal(f"T1.compilation écart — {l}")
    return (False, "", "", r)


def composer_temoin(chemin, entetes, run_n, code, console_dernieres,
                    sha_binaire, origine, machine, silicium, accelerateur):
    lignes = entetes + [
        f"Le run        : N={run_n} par classe (le protocole "
        f"KAGGLE-X86-1 — échantillons entrelacés)",
        f"Code du run   : {code}",
        f"Le binaire    : run/dudect_collab (sha256 {sha_binaire[:16]}…)",
        f"L'origine     : {origine}",
        f"La machine    : {machine}",
        f"Le silicium   : {silicium}",
        f"L'accélérateur: {accelerateur}",
        "",
        "LA MUTUALISATION (la machine de commodité se nomme, D206) : le "
        "silicium de la session Kaggle est PARTAGÉ aux voisins INCONNUS — "
        "le t mesure AUSSI eux ; le DVFS sous l'hyperviseur est opaque "
        "(aucun cadre de fréquence cockpit : la cadence se constate aux "
        "temps eux-mêmes) ; la hiérarchie d'évidence est INCHANGÉE — le "
        "banc contrôlé (portable, téléphone) demeure la référence.",
        "",
        "LES DERNIÈRES LIGNES DE LA CONSOLE (la sortie complète vit "
        "dans sortie-run-N%d.txt) :" % run_n,
        ""] + ["  " + l for l in console_dernieres] + [
        "",
        "LA LECTURE HONNÊTE : |t| > 5 = dépendance AU SEUIL sur CET "
        "échantillon, CETTE machine mutualisée, consignée telle quelle ; "
        "|t| <= 5 = aucune divergence au seuil sur cet échantillon — "
        "jamais « temps constant prouvé ».",
        "",
        "À COMPLÉTER DE VOTRE MAIN (le mesureur ne peut pas le lire à "
        "votre place) :",
        "  - l'état EFFECTIF du gouverneur de fréquence pendant le run, "
        "si vous le connaissez (sous l'hyperviseur, il est probablement "
        "opaque — constatez-le tel quel) ;",
        "  - vos observations, mêmes défavorables (D189 : rapporter tel "
        "quel).",
        "",
        "PUIS : datez et signez la synthèse de votre main, et "
        "RÉCUPÉREZ le zip de retour preuves-kaggle-<horodatage>.zip "
        "AVANT LA FIN DE LA SESSION (la session Kaggle est ÉPHÉMÈRE : "
        "sauvegardez AUSSI le notebook pour que /kaggle/working vive "
        "dans la version enregistrée), puis téléversez le zip ET le scan "
        "au coffre /test (dossier Drive « Triade » → « test »). Le labo "
        "recoupe sur pièces : jamais avant le run, jamais sans pièces.",
    ]
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")


def main():
    global _journal
    os.makedirs(DEST, exist_ok=True)
    os.makedirs("run", exist_ok=True)
    _journal = open(os.path.join(DEST, "scenario-kaggle-journal.log"),
                    "w", encoding="utf-8")

    journal("=== scenario-kaggle.py — L'ORCHESTRATEUR DU KIT-C "
            "(édition KAGGLE x86-64, 25/11/2026) ===")

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
    accelerateur = constat_accelerateur()
    journal(f"T0.accelerateur — {accelerateur}")
    rendu = hashlib.sha256(b"abc").hexdigest()
    journal(f"T0.lecteur python sha256(abc) = {rendu[:16]}… — "
            f"{'EXACT' if rendu == ABC_SHA256 else 'DIVERGENT'}")
    if rendu != ABC_SHA256:
        journal("T0.lecteur — REFUS : le lecteur Python est faux")
        return 2

    pieces = [(SOURCE, SCELLE_DUDECT_COLLAB_C),
              ("cibles/proxy-image.bin", SCELLE_PROXY_IMAGE),
              ("cibles/manifeste-c.txt", SCELLE_MANIFESTE_C)]
    for chemin, scelle in pieces:
        if not os.path.exists(chemin):
            journal(f"T0.piece — REFUS : {chemin} est ABSENT (copiez le "
                    f"dossier kit-C-kaggle-dudect/ ENTIER — D99)")
            return 2
        empreinte = sha256_fichier(chemin)
        journal(f"T0.piece — sha256({chemin}) = {empreinte}")
        if empreinte != scelle:
            journal(f"T0.piece — REFUS : l'empreinte de {chemin} DIVERGE "
                    f"du scellé — la pièce a bougé, RIEN ne sera compilé "
                    f"ni exécuté. Re-extrayez le zip COMPLET dans un "
                    f"dossier NEUF (D99).")
            return 2
    journal("T0.piece — les trois empreintes recoupent les scellés : les "
            "pièces sont les pièces du labo (l'image scellée comprise — "
            "la pièce du coffre, BYTE-POUR-BYTE celle de l'édition COLLAB)")

    # ---- T1 LA COMPILATION ----
    cc = trouver_cc()
    if cc is None:
        journal("T1.compilateur — REFUS NOMMÉ : aucun compilateur "
                "(gcc/clang/cc). Sur Kaggle :  !apt-get install -y gcc  "
                "puis relancez. Le lanceur du kit tente l'installation "
                "lui-même.")
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
    sha_binaire = sha256_fichier("run/dudect_collab")
    journal(f"T1.binaire — run/dudect_collab sha256 {sha_binaire}")
    origine = (f"RECOMPILÉ SUR CETTE MACHINE ({cmd} — la source est la "
               f"vérité)")

    # ---- T2 L'ÉPREUVE D'APPEL ----
    journal("T2.epreuve — ./run/dudect_collab --fips (le condensé FIPS "
            "« abc » EXACT exigé des TROIS lecteurs : logiciel, SHA-NI "
            "s'il vit, ET LA PIÈCE SCELLÉE tls13-02 avec l'adversaire de "
            "mutation K)")
    r = subprocess.run(["./run/dudect_collab", "--fips"],
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
    journal("T2.epreuve — VÉCUE : les lecteurs sont exacts (la pièce "
            "scellée comprise)")

    # ---- T3 LES RUNS ----
    entetes = [
        "LE TÉMOIN DUDECT-KAGGLE — N{N} (édition KAGGLE x86-64, kit-C-kaggle, v1.0.0)",
        "=" * 64,
        f"L'horodatage  : {datetime.datetime.now().isoformat(timespec='seconds')}",
        f"La pièce      : dudect_collab.c sha256 {SCELLE_DUDECT_COLLAB_C}",
        f"Le scellé     : cibles/proxy-image.bin sha256 {SCELLE_PROXY_IMAGE}",
        "Le protocole  : KAGGLE-X86-1 (l'égalation du COLLAB-X86-1, "
        "pré-enregistrée au LISEZMOI-dudect-kaggle.txt AVANT tout run)",
        "Les cibles    : eq-constant (contrôle positif), eq-branchue "
        "(contrôle négatif), sha256-logiciel, sha256-x86-shani (si le "
        "noyau expose « sha_ni » et le compilateur -msha), tls13-02 / "
        "tls13-13 / tls13-16 / tls13-17 (LES SCELLÉES de proxy-image.bin, "
        "recoupées avant exécution)",
    ]
    codes = {}
    for n in LES_N:
        journal(f"T3.run — N={n} par classe : LE RUN (quelques minutes à "
                "silicium partagé)")
        r = subprocess.run(["./run/dudect_collab", str(n)],
                           capture_output=True, text=True, timeout=3600)
        codes[n] = r.returncode
        console = r.stdout + r.stderr
        chemin_console = os.path.join(DEST, f"sortie-run-N{n}.txt")
        with open(chemin_console, "w", encoding="utf-8") as f:
            f.write(console)
        for l in console.strip().splitlines():
            print(f"  {l}")
        journal(f"T3.run N={n} — code de sortie {r.returncode}")

        # le journal csv du run (le binaire écrit journal-dudect-collab-<epoch>.csv,
        # LA MÊME pièce byte-byte : le réceptacle le renomme au nom de son N)
        csvs = sorted(f for f in os.listdir(".")
                      if f.startswith("journal-dudect-collab-")
                      and f.endswith(".csv"))
        if csvs:
            shutil.move(csvs[-1],
                        os.path.join(DEST, f"journal-dudect-kaggle-N{n}.csv"))
            journal(f"T3.run N={n} — journal csv consigné "
                    f"(journal-dudect-kaggle-N{n}.csv)")

        dernieres = console.strip().splitlines()[-12:]
        composer_temoin(
            os.path.join(DEST, f"temoin-dudect-kaggle-N{n}.txt"),
            [l.replace("{N}", str(n)) for l in entetes],
            n, r.returncode, dernieres, sha_binaire, origine,
            machine, silicium, accelerateur)
        journal(f"T3.run N={n} — témoin composé : temoin-dudect-kaggle-N{n}.txt")

    # ---- T4 LA SYNTHÈSE ET LE ZIP DE RETOUR ----
    synthese = [
        "LA SYNTHÈSE DUDECT-KAGGLE — édition KAGGLE x86-64, kit-C-kaggle, v1.0.0",
        "=" * 64,
        f"La machine    : {machine}",
        f"Le silicium   : {silicium}",
        f"L'accélérateur: {accelerateur}",
        f"La pièce      : dudect_collab.c sha256 {SCELLE_DUDECT_COLLAB_C}",
        f"Le scellé     : cibles/proxy-image.bin sha256 {SCELLE_PROXY_IMAGE}",
        f"Le binaire    : run/dudect_collab sha256 {sha_binaire}",
        f"L'origine     : {origine}",
        f"Le compilateur: {premiere}",
        "",
        "LA MUTUALISATION (D206 : la machine de commodité se nomme) : le "
        "silicium de la session Kaggle est PARTAGÉ aux voisins inconnus — "
        "le t mesure AUSSI eux ; le DVFS sous l'hyperviseur est opaque ; "
        "la hiérarchie d'évidence est inchangée (le banc contrôlé demeure "
        "la référence) ; la session est ÉPHÉMÈRE — le zip de retour est "
        "déjà composé, RÉCUPÉREZ-LE AVANT LA FIN (et sauvegardez le "
        "notebook : /kaggle/working vit dans la version enregistrée).",
        "",
        "LES TROIS RUNS (l'ordre imposé du protocole) :",
    ] + [f"  N={n} — code {codes[n]} (sortie-run-N{n}.txt, "
         f"journal-dudect-kaggle-N{n}.csv, temoin-dudect-kaggle-N{n}.txt)"
         for n in LES_N] + [
        "",
        "LA QUESTION DU KIT (l'avis de l'Entrée 421, l'égalation de "
        "l'édition COLLAB) : les trois divergences |t|>5 du 24/11 au "
        "portable (tls13-02 : −10,64 ; tls13-13 : +9,65 ; tls13-16 : "
        "−9,19 — lues comme DVFS à l'Entrée 416 aux classes "
        "SÉQUENTIELLES) SUIVENT-ELLES LA MACHINE OU LE CODE ? Ce run, "
        "classes ENTRELACÉES sur UN AUTRE silicium serveur mutualisé, "
        "dit ce qu'il dit — la lecture appartient au labo, sur pièces.",
        "",
        "LA LECTURE HONNÊTE (le protocole entier vit au "
        "LISEZMOI-dudect-kaggle.txt) :",
        "  — |t| > 5 = dépendance AU SEUIL sur CET échantillon, CETTE "
        "machine mutualisée, consignée telle quelle ;",
        "  — |t| <= 5 = aucune divergence au seuil sur cet échantillon — "
        "jamais « temps constant prouvé » ;",
        "  — le contrôle négatif eq-branchue DOIT diverger (sinon "
        "l'instrument est CONTESTÉ — nommé) ;",
        "  — le rapport médian logiciel/SHA-NI (s'il vit) est LE CONSTAT "
        "DE CE SILICIUM (jamais une cible : aucune cible pré-enregistrée "
        "n'existe pour ce silicium de commodité).",
        "",
        "LES RÉFÉRENCES : le kit-2 du 24/11 (la machine n° 1) ; le kit-B "
        "du téléphone (le troisième silicium, FEAT_SHA256) ; le kit-C de "
        "l'édition COLLAB (le Xeon Colab, Entrée 426 — le même instrument "
        "BYTE-POUR-BYTE, un terrain de plus) ; le coffre /test pour le "
        "retour des preuves.",
        "",
        "signature du geste : à dater et à signer de la main du "
        "développeur.",
    ]
    with open(os.path.join(DEST, "temoin-dudect-kaggle-SYNTHESE.txt"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(synthese) + "\n")

    vert = all(c == 0 for c in codes.values())
    journal(f"T4.synthese — les codes : "
            + ", ".join(f"N{n}={codes[n]}" for n in LES_N))
    journal("T4.synthese — le réceptacle preuves-kaggle/ : journal, "
            "épreuve FIPS, trois sorties, trois csv, trois témoins, "
            "synthèse")

    # le zip de retour (la session est ÉPHÉMÈRE)
    horodatage = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    nom_zip = f"preuves-kaggle-{horodatage}.zip"
    with zipfile.ZipFile(nom_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for racine, _, fichiers in os.walk(DEST):
            for nom in sorted(fichiers):
                chemin = os.path.join(racine, nom)
                z.write(chemin, os.path.relpath(chemin, "."))
    sha_zip = sha256_fichier(nom_zip)
    journal(f"T4.retour — le zip de retour : {nom_zip} "
            f"({os.path.getsize(nom_zip)} octets, sha256 {sha_zip})")

    print()
    print("=" * 64)
    print(" LE KIT-C EST VÉCU. Les preuves vivent dans preuves-kaggle/")
    print(" ET dans le zip de retour : " + nom_zip)
    print(" À VOTRE MAIN, DANS CET ORDRE :")
    print("   1. RÉCUPÉREZ le zip AVANT LA FIN DE LA SESSION (Kaggle est")
    print("      ÉPHÉMÈRE — sauvegardez AUSSI le notebook, /kaggle/working")
    print("      vit dans la version enregistrée) :")
    print("      → panneau droit de Kaggle, onglet Output / Données de")
    print(f"        sortie, ou dans une cellule :  {nom_zip}")
    print("        (il vit au dossier courant du kit)")
    print("   2. Datez et signez la synthèse (imprimez-la ou recopiez-la,")
    print("      signez, scannez/photographiez).")
    print("   3. Téléversez le zip ET le scan au coffre /test (dossier")
    print("      Drive « Triade » → « test »).")
    print(" Le labo recoupe sur pièces : jamais avant le run, jamais")
    print(" sans pièces.")
    print("=" * 64)
    _journal.close()
    return 0 if vert else 3


if __name__ == "__main__":
    sys.exit(main())
