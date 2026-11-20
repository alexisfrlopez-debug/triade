#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scenario-fencei-rv64.py — LE TERRAIN fence.i AU SILICIUM : le scénario M7
RETARGETÉ sur une carte RV64GC physique (kit l4nnwqlld, pièce 1-3).

LA RÉSERVE D149 EST LEVÉE ICI OU NULLE PART : les runs M7 vécus (labo et
terrain WSL2) exécutaient l'ISA par qemu-riscv64 — TCG, la sémantique du
cache d'instructions celle de l'HÔTE. Le présent kit demande à une CARTE
RISC-V RÉELLE (RV64GC sous Linux, la fiche ci-dessous) de rejouer le geste
NATIVEMENT : le cœur fetch, le cache d'instructions est LE SIEN, fence.i
invalide CE cache. Aucun émulateur dans la chaîne — le seul instrument est
le cross-assembleur qui bâtit la sonde.

LA CARTE VISÉE (le kit ne pose AUCUNE exigence de marque — la FICHE) :
  - un cœur applicatif RV64GC 64 bits sous Linux (noyau ≥ 5.x, page 4 Kio) ;
  - RV64GC INCLUT Zifencei PAR CONSTRUCTION (la lettre G = IMAFD +
    Zicsr + Zifencei) : fence.i y est une instruction native — l'exécution
    elle-même en fait la preuve (une carte sans Zifenceur SIGILLerait,
    l'échec serait nommé, jamais contourné) ;
  - le psABI autorise un cœur RV64GC à exécuter du RV64IMA (sous-ensemble
    strict, fiche § 1) : les DEUX artefacts scellés du kit (corpus, demo)
    courent Nativement ;
  - chaîne à provisionner : binutils/gcc croisé riscv64-linux-gnu
    (riscv64-linux-gnu-as ≥ 2.36, gcc ≥ 11) AVEC les drapeaux
    -march=rv64ima_zifencei_zicsr -mabi=lp64 (Zifencei pour fence.i,
    Zicsr pour rdcycle, SANS C : .option norvc, 4 o par instruction).

LE CONTENU DU KIT (empreintes consignées à EMPREINTES-KITS.txt AVANT la
remise — la règle du plan) :
  corpus            LE SCELLÉ 0.8.0-rc.1 du jalon M7 (lecture seule) ;
  demo              LE DÉMONSTRATEUR INVITÉ f72001 (lecture seule) ;
  sequence-fencei.S LA SONDE (la source — assemblée SUR LA CARTE au geste) ;
  le présent scénario.

LES TEMPS DU RUN (chaque constat tranché binaire, verdict POST-MORTEM) :
  T0 LE TÉMOIN      les empreintes ASSERTÉES avant tout geste ; la CARTE
                    consignée (cpuinfo : modèle, « isa », MMU ; device-tree ;
                    fréquence courante si exposée ; la chaîne d'assemblage
                    et sa version) ;
  T1 LA SONDE       sequence-fencei.S assemblée SUR LA CARTE (la chaîne
                    documentée), l'empreinte du binaire consignée ;
  T2 LE CRITÈRE     la sonde exécutée : n ≥ 5 runs × DEUX bras —
                    BRAS A (avec fence.i) : le verdict du NOUVEAU mot dans
                    100 % des runs (l'invalidation du cache d'instructions
                    PROUVÉE au témoin) ; la bascule t1 CONSIGNÉE (le scratch
                    vu par le cœur) ; les cycles consignés ;
                    BRAS B (sans fence.i) : l'OBSERVATION du fetch périmé
                    (consignée, JAMAIS une porte — le RISC-V n'exige pas la
                    cohérence I/D, un comportement non garanti ne tranche
                    rien) ;
  T3 LE SCELLÉ AU   le corpus exécuté Nativement ×3 (le rituel : exactement
    SILICIUM        les DEUX lignes au code 0) ; le demo exécuté Nativement
                    (1 200 usages, la bascule PENDANT le trafic, la
                    transcription OCTET POUR OCTET — 15 425 o) ; le DEP
                    falsifié (SIGSEGV, 4 290 o exacts) ;
  T4 ZÉRO RÉGRESSION les fichiers relus ; le rituel REJOUÉ ; le verdict.

Les pièces naissent toutes seules dans ./preuves-fencei/ :
  temoin-fencei.txt, temoin-probe.bin, scenario-fencei-journal.log,
  VERDICT-run-fencei.txt — à renvoyer ENTIÈRES au coffre /test/preuves-fencei/
  avec la signature datée (GRILLE-TEMOIN.txt du kit).

Un verdict ÉCHEC NOMMÉ se renvoie TEL QUEL : la ligne nomme le défaut ;
un échec honnête vaut plus qu'un vert muet.
"""

import hashlib
import os
import platform
import re
import shutil
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
PREUVES = os.path.join(ICI, "preuves-fencei")
TMP = os.path.join(PREUVES, ".tmp")

SHA_CORPUS = "ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799"
SHA_DEMO = "e57fc74be2ea67ab4c05351d0b5e0b93b6147ec34f2fb7aabbfd1ab7f141cde9"

N_RUNS = 5                       # le protocole d'acceptation : n >= 5
MAGIC = 0x45434931               # « ECI1 » little-endian (l'en-tête du témoin)
V1, V2 = 11, 22                  # les verdicts attendus des mots togglés

N_TRAFIC, K_APPLY, M_ROLLBACK = 1200, 400, 800
ATTENDU_TAILLE = 15425           # la transcription intégrale du demo
DEP_TAILLE = 4290                # les 400 lignes v1 du mutant DEP
DEP_OFF = 0x1ad4                 # le site « addi a0, zero, 7 » (l'APPLY)
DEP_OCTETS = bytes.fromhex("13057000")

RITUEL = b"TRIADE M1 : minilibc 21/21 OK\ncorpus : autotest 21 vecteurs\n"

CH_APPLY = b"demo: PASS apply 0 (usages 399/400)\n"
CH_TRAMP = b"demo: PASS trampoline (le mot a bascule)\n"
CH_EFFET = b"demo: PASS effet j2: verdict (v2 effectif)\n"
CH_ROLLB = b"demo: PASS rollback 0 (usages 799/800)\n"
CH_V1 = b"demo: PASS v1-retour (verdict sans marque)\n"
CH_PTRAFIC = b"demo: PASS trafic 1200 verdicts (800 v1 + 400 v2)\n"
CH_REST = b"demo: PASS restauration (entree a l'octet)\n"
CH_DORM = b"demo: PASS dormance (croissance habitee)\n"
CH_VERROU = b"demo: PASS verrou (rendu un-pour-un)\n"
CH_REFMODE = b"demo: PASS refus-mode 1\n"
CH_REFETAT = b"demo: PASS refus-etat 4 (x2)\n"
CH_REFABS = b"demo: PASS refus-absent 2\n"
CH_REFSOM = b"demo: PASS refus-somme 3\n"
CH_FIN = b"demo: VERDICT VERT (fence.i demontre)\n"

_MOTIF_LIGNE = re.compile(rb"^(j2: )?trafic (\d+)$")

# la chaîne d'assemblage : le CROISÉ d'abord (la station de travail), sinon
# le compilateur NATIF de la carte — les MÊMES drapeaux, la version consignée
CHAINES = [
    (["riscv64-linux-gnu-gcc"], "le cross-gcc de la station (riscv64-linux-gnu-)"),
    (["cc"], "le compilateur natif de la carte (cc)"),
    (["gcc"], "le compilateur natif de la carte (gcc)"),
]
DRAPEAUX = ["-nostdlib", "-static",
            "-march=rv64ima_zifencei_zicsr", "-mabi=lp64"]


class EchecScenario(RuntimeError):
    """Tout refus nommé AVANT le run (fail-closed : jamais un faux vert)."""


def sha256_fichier(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


_constats = []
_journal = []


def dire(ligne):
    print(ligne)
    _journal.append(ligne)


def constat(message, ok, detail=""):
    ligne = f"[fencei] {'PASS' if ok else 'ÉCHEC'} : {message}"
    if detail:
        ligne += f" ({detail})"
    _constats.append((ok, ligne))
    dire(ligne)
    return ok


def ecrire_journal(nom, contenu):
    with open(os.path.join(PREUVES, nom), "w", encoding="utf-8") as f:
        f.write(contenu)


def lire_texte(chemin, limite=8192):
    try:
        with open(chemin, encoding="utf-8", errors="replace") as f:
            return f.read(limite)
    except OSError:
        return ""


def lancer(cmd, timeout=180):
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        return r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        return b"", b"<timeout>", -99
    except FileNotFoundError:
        return b"", b"<absent>", -98


def transcription_attendue():
    att = bytearray()
    for i in range(N_TRAFIC):
        if i == K_APPLY:
            att += CH_APPLY + CH_TRAMP + b"j2: verdict\n" + CH_EFFET
        if i == M_ROLLBACK:
            att += CH_ROLLB + b"verdict\n" + CH_V1
        ligne = b"trafic " + str(i).encode() + b"\n"
        att += (b"j2: " + ligne) if K_APPLY <= i < M_ROLLBACK else ligne
    att += (CH_PTRAFIC + CH_REST + CH_DORM + CH_VERROU
            + CH_REFMODE + CH_REFETAT + CH_REFABS + CH_REFSOM + CH_FIN)
    return bytes(att)


def decoder_sonde(brut):
    """Le témoin binaire de la sonde : 48 o par enregistrement, u64 LE.
    En-tête [MAGIC, n_runs, 0xFF, slot, mode, 0] puis les bras
    [run, arm, t1, mot, verdict, cycles]. Retour (en-tete, bras) — un
    MAGIC divergent ou une longueur hors pas : REFUS nommé."""
    if len(brut) % 48 != 0:
        raise EchecScenario(f"le témoin de la sonde fait {len(brut)} o — "
                            "hors pas de 48 o : le binaire n'est pas le témoin "
                            "attendu (refus nommé, jamais un décodage forcé)")
    import struct
    champs = struct.iter_unpack("<6Q", brut)
    entete = next(champs, None)
    if entete is None or entete[0] != MAGIC:
        raise EchecScenario("l'en-tête du témoin diverge (MAGIC attendu "
                            f"{MAGIC:#x}) — le binaire n'est pas la sonde du kit")
    bras = list(champs)
    return entete, bras


def main() -> int:
    debut = time.time()
    os.makedirs(PREUVES, exist_ok=True)
    corpus = os.path.join(ICI, "corpus")
    demo = os.path.join(ICI, "demo")

    # T0 LE TÉMOIN — les empreintes ASSERTÉES avant tout geste -----------------
    sha_corpus = sha256_fichier(corpus)
    sha_demo = sha256_fichier(demo)
    if sha_corpus != SHA_CORPUS:
        raise EchecScenario(f"le corpus n'est pas le scellé 0.8.0-rc.1 "
                            f"(sha256 {sha_corpus[:16]}… != {SHA_CORPUS[:16]}…) — "
                            "un kit corrompu est un refus nommé, jamais un run muet")
    if sha_demo != SHA_DEMO:
        raise EchecScenario(f"le demo n'est pas le démonstrateur éprouvé "
                            f"(sha256 {sha_demo[:16]}… != {SHA_DEMO[:16]}…)")
    bits_retablis = []
    for chemin_artefact in (corpus, demo):
        if not os.access(chemin_artefact, os.X_OK):
            try:
                os.chmod(chemin_artefact, 0o755)
                bits_retablis.append(os.path.basename(chemin_artefact))
            except OSError as exc:
                raise EchecScenario(
                    f"le bit exécutable de {os.path.basename(chemin_artefact)} "
                    f"n'a pu être rétabli ({exc}) — sans lui, pas de run "
                    "(jamais un faux vert d'environnement)")
    if bits_retablis:
        dire("[fencei] le bit exécutable rétabli pour : "
             + ", ".join(bits_retablis)
             + " (perdus au transfert — le geste est nommé ; le chmod ne "
               "touche aucun octet de contenu)")

    cpuinfo = lire_texte("/proc/cpuinfo")
    ligne_isa = next((l.strip() for l in cpuinfo.splitlines()
                      if l.strip().startswith("isa")), "isa : absente")
    dt_model = lire_texte("/proc/device-tree/model", 256).replace("\x00", "")
    freq_cur = lire_texte(
        "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq", 64).strip()
    if not freq_cur:
        freq_cur = lire_texte(
            "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq",
            64).strip() or "non exposée par le noyau"

    # la chaîne d'assemblage : la première qui répond
    chaine, provenance = None, None
    for base, prov in CHAINES:
        sortie_v, _, code_v = lancer(base + ["--version"])
        if code_v == 0:
            chaine, provenance = base, prov
            version_chaine = sortie_v.decode(errors="replace").splitlines()[0]
            break
    if chaine is None:
        raise EchecScenario(
            "AUCUNE chaîne d'assemblage trouvée (riscv64-linux-gnu-gcc, cc, "
            "gcc) — provisionner binutils/gcc pour rv64ima_zifencei_zicsr "
            "(LISEZMOI § 2) ; sans instrument, pas de run")

    temoin = [
        "TÉMOIN DU RUN TERRAIN fence.i AU SILICIUM — le scénario M7 retargeté "
        "sur carte RV64GC physique (kit l4nnwqlld)",
        f"date              : {time.strftime('%Y-%m-%d %H:%M:%S %z')}",
        f"machine            : {platform.platform()}",
        f"noyau              : {platform.release()} ({platform.machine()})",
        f"carte (device-tree): {dt_model or 'non exposée'}",
        f"cœur (cpuinfo isa) : {ligne_isa}",
        f"fréquence courante : {freq_cur}",
        f"python             : {sys.version.split()[0]}",
        f"chaîne d'assemblage: {version_chaine} — {provenance}",
        f"corpus (AVANT)     : sha256 {sha_corpus} — le scellé 0.8.0-rc.1 du jalon M7",
        f"demo (AVANT)       : sha256 {sha_demo} — le démonstrateur invité f72001",
        "la réserve D149 EST LEVÉE sur ce run : l'ISA est exécutée par LA CARTE "
        "elle-même (RV64GC — la lettre G inclut Zifencei), aucun émulateur "
        "dans la chaîne.",
        "",
    ]
    ecrire_journal("temoin-fencei.txt", "\n".join(temoin))
    constat("le témoin consigné : empreintes ASSERTÉES avant tout geste "
            f"(corpus {sha_corpus[:16]}…, demo {sha_demo[:16]}…), la carte "
            f"identifiée ({ligne_isa[:60]}…, {dt_model[:40] or 'device-tree muet'}), "
            f"la chaîne {version_chaine.split()[0]} ({provenance})", True)

    vert = True

    # T1 LA SONDE — assemblée SUR LA CARTE, l'empreinte consignée --------------
    chemin_S = os.path.join(ICI, "sequence-fencei.S")
    chemin_probe = os.path.join(TMP, "fencei-probe")
    os.makedirs(TMP, exist_ok=True)
    cmd_build = chaine + DRAPEAUX + ["-o", chemin_probe, chemin_S]
    sortie_b, err_b, code_b = lancer(cmd_build)
    if code_b != 0:
        raise EchecScenario("l'assemblage de la sonde a ÉCHOUÉ — " +
                            (err_b.decode(errors="replace")[-400:]
                             or "aucun diagnostic") +
                            " (vérifier la chaîne : -march=rv64ima_zifencei"
                            "_zicsr -mabi=lp64, LISEZMOI § 2)")
    sha_probe = sha256_fichier(chemin_probe)
    os.chmod(chemin_probe, 0o755)
    constat("LA SONDE ASSEMBLÉE sur la carte : sequence-fencei.S → "
            f"fencei-probe ({sha_probe[:16]}…, "
            f"{' '.join(DRAPEAUX)}) — la source est la pièce, le binaire "
            "l'instant", True)

    # T2 LE CRITÈRE — la sonde exécutée : n >= 5 runs × DEUX bras -------------
    brut, err_p, code_p = lancer([chemin_probe])
    if code_p != 0:
        raise EchecScenario("la sonde a REFUSÉ (exit "
                            f"{code_p}) : {err_p.decode(errors='replace')[-300:]}"
                            " — un refus nommé de syscall (mmap/mprotect) est "
                            "un échec de la carte à accorder la page, JAMAIS "
                            "un faux vert")
    with open(os.path.join(PREUVES, "temoin-probe.bin"), "wb") as f:
        f.write(brut)
    entete, bras = decoder_sonde(brut)
    n_declare = entete[1]
    vert &= constat(f"l'en-tête du témoin : MAGIC {entete[0]:#x}, {n_declare} "
                    f"runs déclarés, slot {entete[3]:#x}, mode "
                    f"{entete[4]} ({'page RWX mmap' if entete[4] == 0 else 'mprotect sur page dédiée'})",
                    n_declare >= N_RUNS,
                    f"{len(bras)} enregistrements de bras")
    bras_a = [b for b in bras if b[1] == 0x41]
    bras_b = [b for b in bras if b[1] == 0x42]
    vert &= constat(f"le plan des bras : {len(bras_a)} bras A (avec fence.i) / "
                    f"{len(bras_b)} bras B (sans) — {N_RUNS} runs × 2 attendus",
                    len(bras_a) >= N_RUNS and len(bras_b) >= N_RUNS
                    and len(bras) == len(bras_a) + len(bras_b))

    # (a) LA BASCULE VUE PAR LE CŒUR : t1 consigné, le mot relu, cohérents
    bascules_ok = all(b[2] == entete[3] and b[3] in (0x00B00513, 0x01600513)
                      for b in bras)
    vert &= constat("LA BASCULE VUE PAR LE CŒUR : le registre scratch t1 "
                    "consigné à CHAQUE bras == l'adresse du slot, le mot "
                    "togglé relu (la vue données : 0x00B00513 v1 / "
                    "0x01600513 v2) — le saut jalr ra, 0(t1) PAR LE SCRATCH "
                    "a vécu", bascules_ok,
                    f"t1={entete[3]:#x} sur les {len(bras)} bras")

    # (b) L'INVALIDATION PROUVÉE : bras A, verdict du NOUVEAU mot, 100 %
    a_ok = sum(1 for b in bras_a if b[4] == V2)
    vert &= constat(f"L'INVALIDATION DU CACHE D'INSTRUCTIONS PROUVÉE AU "
                    f"TÉMOIN : le bras A (écrire v2 → fence rw,rw → fence.i → "
                    f"saut) rend le verdict du NOUVEAU mot dans "
                    f"{a_ok}/{len(bras_a)} runs — 100 % exigés",
                    len(bras_a) > 0 and a_ok == len(bras_a),
                    f"verdicts: {[b[4] for b in bras_a]}")

    # (c) L'OBSERVATION DU FETCH PÉRIMÉ : bras B, consignée, JAMAIS une porte
    verdicts_b = [b[4] for b in bras_b]
    perimes = sum(1 for v in verdicts_b if v == V2)
    dire(f"[fencei] OBSERVATION (le bras B, sans fence.i — consignée, "
         f"jamais une porte) : {perimes}/{len(verdicts_b)} verdicts périmés "
         f"(v2 servi alors que la mémoire dit v1) ; verdicts: {verdicts_b} ; "
         "lecture : un verdict périmé NOMME la nécessité de fence.i sur CE "
         "cœur ; un verdict frais (11) nomme soit un échec de ligne du cache, "
         "soit un noyau qui invalide au mprotect (mode repli) — les deux "
         "lectures sont honnêtes, le bras A seul tranche")
    cycles_a = [b[5] for b in bras_a]
    cycles_b = [b[5] for b in bras_b]
    dire(f"[fencei] cycles consignés — bras A: {cycles_a} ; bras B: {cycles_b}")

    # T3 LE SCELLÉ AU SILICIUM — le corpus et le demo, Nativement -------------
    for essai in range(1, 4):
        sortie, err, code = lancer([corpus])
        vert &= constat(f"le rituel n°{essai} (NATIF, la carte elle-même) : "
                        "exactement les DEUX lignes au code 0 (LE MÊME verdict "
                        "que les instances win/linux/qemu — la parité § 8.3 "
                        "au silicium)",
                        code == 0 and not err and sortie == RITUEL,
                        f"code={code}, {len(sortie)} o")

    attendu = transcription_attendue()
    if len(attendu) != ATTENDU_TAILLE:
        raise EchecScenario(f"la transcription attendue fait {len(attendu)} o "
                            f"≠ {ATTENDU_TAILLE} o figés au labo — le scénario "
                            "ne correspond pas à l'artefact")
    with open(demo, "rb") as f:
        img_demo = f.read()
    chemin_demo = os.path.join(TMP, "demo")
    with open(chemin_demo, "wb") as f:
        f.write(img_demo)
    os.chmod(chemin_demo, 0o755)
    sortie, err, code = lancer([chemin_demo])
    vert &= constat("LA BASCULE fence.i PENDANT LE TRAFIC AU SILICIUM : "
                    f"1 200 usages, l'apply entre {K_APPLY - 1}/{K_APPLY}, le "
                    f"retour entre {M_ROLLBACK - 1}/{M_ROLLBACK} — la "
                    "transcription OCTET POUR OCTET l'attendu "
                    f"({ATTENDU_TAILLE} o) — le mécanisme mprotect RW → "
                    "écrire → fence rw,rw → LA BASCULE UN MOT → fence.i → RX "
                    "vécu PAR LA CARTE",
                    code == 0 and not err and sortie == attendu,
                    f"code={code}, {len(sortie)} o rendus / {ATTENDU_TAILLE} attendus"
                    + (f", err={err[:60]!r}" if err else ""))
    vues, duplique, fragment, melange = {}, None, None, None
    emissions = {b"j2: verdict", b"verdict"}
    for l in sortie.split(b"\n")[:-1]:
        m = _MOTIF_LIGNE.match(l)
        if not m:
            if l.startswith(b"demo: ") or l in emissions:
                continue
            fragment = fragment or l
            continue
        num = int(m.group(2))
        if num in vues:
            duplique = duplique or num
        vues[num] = m.group(1) is not None
    for i, est_v2 in vues.items():
        if est_v2 != (K_APPLY <= i < M_ROLLBACK):
            melange = melange or i
    vert &= constat("le journal est COHÉRENT : 1 200 lignes ENTIÈRES, indices "
                    "0..1199 chacun EXACTEMENT une fois, aucun mélange",
                    set(vues) == set(range(N_TRAFIC)) and duplique is None
                    and fragment is None and melange is None,
                    f"{sum(1 for v in vues.values() if v)} lignes v2")

    if img_demo[DEP_OFF:DEP_OFF + 4] != DEP_OCTETS:
        raise EchecScenario(f"le site du DEP a bougé : "
                            f"{img_demo[DEP_OFF:DEP_OFF + 4].hex()} "
                            f"≠ {DEP_OCTETS.hex()} — le scénario ne correspond "
                            "pas à l'artefact")
    mutant = bytearray(img_demo)
    mutant[DEP_OFF + 2] = 0x30            # 0x7 → 0x3 (l'imm12 du prot)
    chemin_dep = os.path.join(TMP, "demo-dep")
    with open(chemin_dep, "wb") as f:
        f.write(bytes(mutant))
    os.chmod(chemin_dep, 0o755)
    attendu_dep = b"".join(b"trafic " + str(i).encode() + b"\n"
                           for i in range(K_APPLY))
    sortie_m, err_m, code_m = lancer([chemin_dep])
    vert &= constat("LE DEP FALSIFIÉ (0x7→0x3) : l'exécution FAUTE au retour "
                    "du premier mprotect (page sans X — le fetch suivant) : "
                    f"SIGSEGV, {DEP_TAILLE} o EXACTS (les 400 lignes v1, "
                    "zéro silence)",
                    code_m == -11 and sortie_m == attendu_dep,
                    f"code={code_m}, {len(sortie_m)} o")

    # T4 ZÉRO RÉGRESSION -------------------------------------------------------
    sha_corpus_apres = sha256_fichier(corpus)
    sha_demo_apres = sha256_fichier(demo)
    vert &= constat("ZÉRO RÉGRESSION : les DEUX fichiers relus — le corpus et "
                    "le demo n'ont pas bougé d'un octet (le patch est un fait "
                    "de la session INVITÉE, jamais du fichier)",
                    sha_corpus_apres == SHA_CORPUS and sha_demo_apres == SHA_DEMO,
                    f"corpus {sha_corpus_apres[:16]}…, demo {sha_demo_apres[:16]}…")
    sortie_c, err_c, code_c = lancer([corpus])
    vert &= constat("le rituel du scellé REJOUÉ après la démonstration : "
                    "exactement ses deux lignes au code 0",
                    code_c == 0 and not err_c and sortie_c == RITUEL,
                    f"code={code_c}")

    # Le journal — LA pièce intégrale, puis le verdict POST-MORTEM -------------
    shutil.rmtree(TMP, ignore_errors=True)
    duree = int(time.time() - debut)
    entete_journal = [
        "JOURNAL DU RUN TERRAIN fence.i AU SILICIUM — le M7 retargeté (l4nnwqlld)",
        f"machine : {platform.platform()} — noyau {platform.release()}",
        f"carte : {dt_model or 'non exposée'} — {ligne_isa}",
        f"chaîne : {version_chaine} ({provenance})",
        f"corpus : sha256 {sha_corpus} — le scellé 0.8.0-rc.1 du jalon M7",
        f"demo : sha256 {sha_demo} — le démonstrateur invité f72001",
        f"sonde : fencei-probe sha256 {sha_probe}",
        "",
    ]
    ecrire_journal("scenario-fencei-journal.log",
                   "\n".join(entete_journal + _journal) + "\n")
    verdict = [
        "VERDICT DU RUN TERRAIN fence.i AU SILICIUM (post-mortem, sur pièces "
        "— kit l4nnwqlld)",
        "",
        *[l for _, l in _constats],
        "",
        f"constats : {sum(1 for ok, _ in _constats if ok)} PASS / "
        f"{sum(1 for ok, _ in _constats if not ok)} ÉCHEC ({duree} s)",
        f"carte : {dt_model or 'non exposée'} — {ligne_isa} — fréquence {freq_cur}",
        "frontières nommées : le bras B (sans fence.i) est une OBSERVATION "
        "consignée, jamais une porte (la cohérence I/D n'est pas exigée par "
        "le RISC-V) ; le corpus est LE scellé 0.8.0-rc.1 du jalon, le demo "
        "l'INSTRUMENT du chantier M7-(c) (pas un artefact de la lignée) ; "
        "la sonde assemblée SUR LA CARTE porte la séquence § 5 de la fiche "
        "profil (fence rw,rw → fence.i → saut par le scratch t1) ; "
        "la concurrence réelle reste HORS périmètre (mono-fil — la portée de "
        "fence.i est le cœur courant).",
        "",
        "VERDICT : " + ("VERT" if vert else "KO"),
        "",
        "Si VERT : renvoyer preuves-fencei/ ENTIER au coffre "
        "/test/preuves-fencei/ AVEC la signature datée (GRILLE-TEMOIN.txt) — "
        "le laboratoire recoupe sur pièces (D138/D145/D148) : la ligne "
        "« fence.i on silicon — awaiting hardware run » se fermera SUR "
        "PIÈCES, jamais avant.",
        "Si ÉCHEC NOMMÉ : renvoyer TEL QUEL — la ligne nomme le défaut.",
    ]
    ecrire_journal("VERDICT-run-fencei.txt", "\n".join(verdict) + "\n")
    print()
    print("\n".join(verdict[-9:]))
    return 0 if vert else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except EchecScenario as exc:
        print(f"REFUS (fail-closed) : {exc}", file=sys.stderr)
        print("Aucune pièce n'a été écrite — le refus précède le run "
              "(un kit corrompu ne se joue pas).", file=sys.stderr)
        sys.exit(2)
