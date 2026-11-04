#!/usr/bin/env python3
"""demo_patch.py — LA BASCULE PENDANT LE TRAFIC (chantier M6-(d) — M5-(c)
refermé sur le profil Linux).

Le critère M5-(c) reporté (D149-(4)) : « patch appliqué pendant le trafic,
journal cohérent, rollback démontré, zéro régression (suite de conformité
verte) » — démontré SUR L'ARTEFACT SCELLÉ 0.7.0-rc.1 (sha256 dd14195c…,
JAMAIS touché : la démonstration vit dans une cartographie PRIVÉE de
l'image, le fichier demeure en lecture seule — le patch est un fait de la
session, jamais du fichier).

Les pièces du verdict (fail-closed, chacune tranchée binaire) :
  (a) LE TRAFIC EN SESSION, LA BASCULE ENTRE DEUX USAGES (tcp-07:R4 V5) :
      1 200 usages du journal par la boucle d'écriture ; le moteur
      APPLIQUÉ entre les usages 400 et 401 (mode 0), le RETOUR ARRIÈRE
      entre les usages 800 et 801 (mode 1) — la boucle CONTINUE (jamais
      une interruption : chaque usage rend son verdict exact, la pile
      équilibrée, les non volatils intacts) et le journal demeure
      COHÉRENT : usages 0..399 au format v1 EXACT, 400..799 au format v2
      EXACT (marque « j2: »), 800..1199 au format v1 EXACT — jamais une
      ligne déchirée, jamais un format mixte, jamais une ligne perdue ;
  (b) LA BASCULE SOUS CONCURRENCE RÉELLE (Q3 : l'écriture alignée unique)
      : un fil ouvrier journalise en boucle PENDANT que le fil conducteur
      applique le patch, journalise sous v2, revient, journalise sous v1,
      applique encore — le qword de bascule est posé ALORS QUE L'OUVRIER
      VIT dans le bloc (sa vie est PROUVÉE avant la bascule : des lignes
      déjà émis au moment de l'apply). Chaque ligne de l'ouvrier demeure
      ENTIÈRE au format v1 OU v2 (jamais un mélange dans une même ligne),
      aucun index perdu ni dupliqué, le verrou rendu un-pour-un — et les
      DEUX formats sont constatés dans SON trafic : la bascule était
      VIVANTE pendant qu'il journalisait ;
  (c) LE RETOUR À L'ÉTAT IMAGE : l'entrée du journal restaurée OCTET POUR
      OCTET, l'état v1, le remplaçant DORMANT dans la croissance (la
      copie y reste, réactivable — Q2), le verrou rendu ;
  (d) ZÉRO RÉGRESSION SUR PIÈCES : le FICHIER artefact n'a pas bougé d'un
      octet (sha256 re-relu après la démonstration), le rituel REJOUÉ en
      exécution réelle rend exactement ses deux lignes au code 0 — la
      suite de conformité (unix/conformite_profil.py) demeure le témoin
      de jalon, rejouée au chantier même.

Usage : python3 demo_patch.py [chemin_artefact] [--bavard]
Retour : executer() -> (vert, lignes) — le modèle controle_base_reelle.
"""

from __future__ import annotations

import ctypes
import hashlib
import os
import re
import subprocess
import sys
import threading
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
import layout as L  # noqa: E402

import oracle_corpus as OC  # noqa: E402

# L'artefact scellé (le fait de carte du chantier M6-(c) — jamais déplacé)
SHA_SCELLE = "dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7"
RITUEL_L1 = b"TRIADE M1 : minilibc 21/21 OK\n"
RITUEL_L2 = b"corpus : autotest 21 vecteurs\n"

# Le plan du trafic (phase a) : la bascule et le retour ENTRE deux usages
N_TRAFIC = 1200          # usages de la boucle d'écriture
K_APPLY = 400            # l'apply VIVRA entre les usages 399 et 400
M_ROLLBACK = 800         # le rollback entre les usages 799 et 800

# La concurrence (phase b) : l'ouvrier vit, le conducteur bascule
OUVRIER_CAP = 60000      # borne haute (la fin réelle : l'événement d'arrêt)


class EchecDemo(Exception):
    """Tout échec nommé de la démonstration (fail-closed : jamais un faux vert)."""


# --- La capture cumulée (le flux de la boucle d'écriture, pompé en live) --------

class CaptureFlux:
    """Détourne fd 1 vers un tube ; `pomper()` draine SANS consommer le
    producteur (les morceaux s'accumulent — la relecture est post-mortem)."""

    def __init__(self):
        self.lecture, self.ecriture = os.pipe()
        os.set_blocking(self.lecture, False)
        self.sauve = None
        self.morceaux = []

    def __enter__(self):
        self.sauve = os.dup(1)
        os.dup2(self.ecriture, 1)
        return self

    def pomper(self) -> int:
        while True:
            try:
                m = os.read(self.lecture, 65536)
            except BlockingIOError:
                break
            if not m:
                break
            self.morceaux.append(m)
        return sum(len(m) for m in self.morceaux)

    def flux(self) -> bytes:
        return b"".join(self.morceaux)

    def __exit__(self, *a):
        os.dup2(self.sauve, 1)
        os.close(self.sauve)


# --- Le démonstrateur ------------------------------------------------------------

def executer(chemin: str | None = None, bavard: bool = True) -> tuple[bool, list]:
    chemin = chemin or os.path.join(ICI, "corpus")
    lignes: list[str] = []
    vert = True

    def constat(message: str, ok: bool, detail: str = "") -> None:
        nonlocal vert
        vert = vert and ok
        l = f"[demo] {'PASS' if ok else 'ECHEC'} : {message}"
        if detail:
            l += f" ({detail})"
        lignes.append(l)

    # (0) L'ARTEFACT SCELLÉ RELU — la démonstration porte sur LE scellé
    with open(chemin, "rb") as f:
        artefact = f.read()
    sha_art = hashlib.sha256(artefact).hexdigest()
    constat("l'artefact est le scellé relu (0.7.0-rc.1, le fait de carte du "
            "chantier (c))", sha_art == SHA_SCELLE and len(artefact) == 12288,
            f"sha256 {sha_art[:16]}…, {len(artefact)} o")

    # Les tampons du trafic (buffers fixes — la discipline de l'appelant)
    cart = OC.Cartouche()
    libc = cart._libc

    def tampon(donnees: bytes) -> int:
        p = libc.mmap(ctypes.c_void_p(0), ctypes.c_size_t(64),
                      ctypes.c_int(1 | 2),            # PROT_READ | PROT_WRITE
                      ctypes.c_int(0x02 | 0x20),      # MAP_PRIVATE | MAP_ANONYMOUS
                      ctypes.c_int(-1), ctypes.c_size_t(0))
        if not p or p == ctypes.c_void_p(-1).value:
            raise EchecDemo("tampon : mmap impossible")
        ctypes.memmove(p, donnees, len(donnees))
        return p

    P_TRAFIC, LP_TRAFIC = tampon(b"trafic "), 7
    P_OUVRIERE, LP_OUVRIERE = tampon(b"ouvriere "), 9
    P_CONDUCTEUR, LP_CONDUCTEUR = tampon(b"contremaitre "), 13
    P_NL, LP_NL = tampon(b"\n"), 1

    def v1(prefixe: bytes, i: int) -> bytes:
        return prefixe + str(i).encode() + b"\n"

    # =====================================================================
    # (a) LE TRAFIC EN SESSION — la bascule ENTRE DEUX USAGES (V5)
    # =====================================================================
    lignes.append(f"[demo] (a) LE TRAFIC EN SESSION — {N_TRAFIC} usages de la "
                  f"boucle d'écriture, l'apply entre les usages {K_APPLY - 1} et "
                  f"{K_APPLY}, le retour arrière entre {M_ROLLBACK - 1} et {M_ROLLBACK}")
    img = OC.Image(chemin, "prive")
    entree_originale = img.octets(L.A_JOURNAL, 8)
    if img.qword(L.R_ETAT_PATCH_CORPUS) != 0:
        raise EchecDemo("(a) l'état patch n'est pas né v1 (P4)")

    attendus: list[bytes] = []
    premiere_anomalie = None      # (i, attendu, rendu) — le verdict d'un usage
    premiere_pile = None          # i — pile ou non volatils rompus
    with CaptureFlux() as cap:
        for i in range(N_TRAFIC):
            if i == K_APPLY:
                r = cart.appeler(img.adr(L.A_PATCH), [0])
                constat("l'application PENDANT le trafic rend 0 (mode 0, la "
                        "boucle ne s'arrête pas)", r["rax"] == 0, f"rax={r['rax']}")
                constat("l'état passe à v2 (1) en pleine session",
                        img.qword(L.R_ETAT_PATCH_CORPUS) == 1)
            if i == M_ROLLBACK:
                r = cart.appeler(img.adr(L.A_PATCH), [1])
                constat("le retour arrière PENDANT le trafic rend 0 (mode 1, la "
                        "boucle ne s'arrête pas)", r["rax"] == 0, f"rax={r['rax']}")
                constat("l'état revient à v1 (0) en pleine session",
                        img.qword(L.R_ETAT_PATCH_CORPUS) == 0)
            en_v2 = K_APPLY <= i < M_ROLLBACK
            ligne = v1(b"trafic ", i)
            attendus.append(b"j2: " + ligne if en_v2 else ligne)
            r = cart.appeler(img.adr(L.A_JOURNAL),
                             [P_TRAFIC, LP_TRAFIC, i, P_NL, LP_NL])
            if r["rax"] != len(attendus[-1]):
                premiere_anomalie = premiere_anomalie or (i, len(attendus[-1]), r["rax"])
            if not cart.non_volatils_intacts(r) or r["rsp"] != r["sommet"]:
                premiere_pile = premiere_pile or i
        cap.pomper()
        flux = cap.flux()
    constat(f"les {N_TRAFIC} usages rendent leur verdict exact, la pile "
            "équilibrée, les non volatils intacts — JAMAIS une interruption "
            "de service (l'usage suit la bascule sans la voir)",
            premiere_anomalie is None and premiere_pile is None,
            (f"première anomalie @{premiere_anomalie[0]}: "
             f"{premiere_anomalie[2]} != {premiere_anomalie[1]}") if premiere_anomalie
            else (f"pile/non-volatils rompus @{premiere_pile}") if premiere_pile
            else f"{N_TRAFIC}/{N_TRAFIC}")
    nb_v1 = sum(1 for i in range(N_TRAFIC) if not (K_APPLY <= i < M_ROLLBACK))
    constat(f"le journal est COHÉRENT : le flux est OCTET POUR OCTET l'attendu — "
            f"{nb_v1} lignes v1, {M_ROLLBACK - K_APPLY} lignes v2 (marque j2:), "
            "aucune déchirée, aucune perdue, aucun mélange de formats",
            flux == b"".join(attendus),
            f"{len(flux)} o émis, {sum(len(a) for a in attendus)} o attendus, "
            f"{flux.count(chr(10).encode())} lignes")

    # =====================================================================
    # (b) LA BASCULE SOUS CONCURRENCE RÉELLE — le qword posé pendant que
    #     l'ouvrier VIT dans le bloc (Q3 : l'écriture alignée unique)
    # =====================================================================
    lignes.append("[demo] (b) LA BASCULE SOUS CONCURRENCE RÉELLE — le fil ouvrier "
                  "journalise en boucle, le fil conducteur bascule PENDANT son trafic")
    img2 = OC.Image(chemin, "prive")           # session NEUVE : croissance int3, état né v1
    if img2.octets(L.A_CROISSANCE, 8) != b"\xcc" * 8 or img2.qword(L.R_ETAT_PATCH_CORPUS) != 0:
        raise EchecDemo("(b) la session neuve n'est pas à l'état image (croissance int3, état v1)")

    arret = threading.Event()
    fautes_ouvriere: list[tuple] = []
    compte_ouvriere = {"n": 0}

    def ouvrierere() -> None:
        i = 0
        while not arret.is_set() and i < OUVRIER_CAP:
            l1 = len(v1(b"ouvriere ", i))
            r = cart.appeler(img2.adr(L.A_JOURNAL),
                             [P_OUVRIERE, LP_OUVRIERE, i, P_NL, LP_NL])
            if r["rax"] not in (l1, l1 + 4):
                fautes_ouvriere.append((i, r["rax"], l1))
            i += 1
        compte_ouvriere["n"] = i

    with CaptureFlux() as cap2:
        t = threading.Thread(target=ouvrierere)
        t.start()
        # LA PREUVE DE VIE : l'ouvrier a déjà émis AVANT la première bascule —
        # le qword sera posé pendant un trafic VIVANT, pas autour d'un silence
        vivante = False
        for _ in range(400):                    # borne : 2 s max
            time.sleep(0.005)
            if cap2.pomper() >= LP_OUVRIERE + 2:
                vivante = True
                break
        constat("la preuve de vie de l'ouvrier AVANT la bascule (des lignes "
                "déjà émises au moment de l'apply — la bascule tombera dans "
                "un trafic vivant)", vivante,
                f"{cap2.pomper()} o déjà émis" if vivante else "l'ouvrier n'a pas démarré")

        # Fenêtre 1 : APPLY — l'ouvrier continue, le conducteur journalise sous v2
        r = cart.appeler(img2.adr(L.A_PATCH), [0])
        ok_a1 = r["rax"] == 0 and img2.qword(L.R_ETAT_PATCH_CORPUS) == 1
        cm1 = []
        for j in (100, 101):
            l1 = len(v1(b"contremaitre ", j))
            rj = cart.appeler(img2.adr(L.A_JOURNAL),
                              [P_CONDUCTEUR, LP_CONDUCTEUR, j, P_NL, LP_NL])
            cm1.append(rj["rax"] == l1 + 4)     # sous v2 : la marque en plus
        cap2.pomper()
        time.sleep(0.004)
        cap2.pomper()

        # Fenêtre 2 : RETOUR ARRIÈRE — le conducteur journalise sous v1
        r = cart.appeler(img2.adr(L.A_PATCH), [1])
        ok_r1 = r["rax"] == 0 and img2.qword(L.R_ETAT_PATCH_CORPUS) == 0
        cm2 = []
        for j in (200, 201):
            l1 = len(v1(b"contremaitre ", j))
            rj = cart.appeler(img2.adr(L.A_JOURNAL),
                              [P_CONDUCTEUR, LP_CONDUCTEUR, j, P_NL, LP_NL])
            cm2.append(rj["rax"] == l1)         # sous v1 : la marque absente
        cap2.pomper()
        time.sleep(0.004)
        cap2.pomper()

        # Fenêtre 3 : APPLY ENCORE — la fenêtre v2 élargie, l'ouvrier toujours là
        r = cart.appeler(img2.adr(L.A_PATCH), [0])
        ok_a2 = r["rax"] == 0 and img2.qword(L.R_ETAT_PATCH_CORPUS) == 1
        time.sleep(0.004)
        cap2.pomper()

        # La fin : l'ouvrier s'arrête PROPREMENT, puis le retour arrière final
        arret.set()
        t.join()
        r = cart.appeler(img2.adr(L.A_PATCH), [1])
        ok_r2 = r["rax"] == 0 and img2.qword(L.R_ETAT_PATCH_CORPUS) == 0
        cap2.pomper()
        flux2 = cap2.flux()

    constat("les TROIS fenêtres rendent 0 et les états 1→0→1→0 constatés à "
            "chaque geste (le moteur idempotent par refus — E2)",
            ok_a1 and ok_r1 and ok_a2 and ok_r2)
    constat("le conducteur journalise sous CHAQUE version : 2 usages v2 "
            "(verdict = ligne + marque) puis 2 usages v1 (verdict = ligne) — "
            "le comportement change À L'USAGE SUIVANT, sans interruption",
            all(cm1) and all(cm2))

    # Le flux de l'ouvrier : chaque ligne ENTIÈRE au format v1 OU v2
    motif = re.compile(rb"^(j2: )?(ouvriere|contremaitre) (\d+)$")
    vues_ouv: dict[int, bool] = {}      # index -> est_v2
    vues_cm: dict[int, bool] = {}
    duplique = fragment = None
    for l in flux2.split(b"\n")[:-1] if flux2.endswith(b"\n") else flux2.split(b"\n"):
        m = motif.match(l)
        if not m:
            fragment = fragment or l
            continue
        est_v2 = m.group(1) is not None
        qui, num = m.group(2), int(m.group(3))
        table = vues_ouv if qui == b"ouvriere" else vues_cm
        if num in table:
            duplique = duplique or num
        table[num] = est_v2
    n_ouv = compte_ouvriere["n"]
    indices_ok = set(vues_ouv) == set(range(n_ouv)) and duplique is None
    v2_ouv = sum(1 for b in vues_ouv.values() if b)
    v1_ouv = n_ouv - v2_ouv
    cm_ok = vues_cm == {100: True, 101: True, 200: False, 201: False}
    constat(f"l'ouvrier : {n_ouv} lignes ENTIÈRES, indices 0..{n_ouv - 1} "
            "chacun EXACTEMENT une fois (aucune perdue, aucune dupliquée), "
            "verdicts exacts à chaque usage",
            indices_ok and not fautes_ouvriere and fragment is None,
            (f"fragment {fragment!r}") if fragment is not None
            else (f"faute @{fautes_ouvriere[0][0]}") if fautes_ouvriere
            else (f"dupliqué {duplique}") if duplique is not None
            else f"{n_ouv} lignes / {n_ouv} indices")
    constat("la bascule était VIVANTE pendant le trafic de l'ouvrier : SON "
            "flux porte les DEUX formats (v1 et j2:) — le qword a été posé "
            "pendant qu'il journalisait, chaque ligne demeure d'UNE seule "
            "version (jamais un mélange — Q3, l'écriture alignée unique)",
            v1_ouv > 0 and v2_ouv > 0,
            f"{v1_ouv} lignes v1, {v2_ouv} lignes v2 (j2:)")
    constat("le conducteur vu du flux : les 2 lignes v2 puis les 2 lignes v1 "
            "exactement (les formats des DEUX côtés — le verdict et les octets)",
            cm_ok)

    # =====================================================================
    # (c) LE RETOUR À L'ÉTAT IMAGE
    # =====================================================================
    lignes.append("[demo] (c) LE RETOUR À L'ÉTAT IMAGE — la session rend l'image")
    staging_rva = int.from_bytes(img2.octets(L.R_TAB_SUM_CORPUS, 4), "little")
    staging_taille = int.from_bytes(img2.octets(L.R_TAB_SUM_CORPUS + 4, 4), "little")
    etat_image = (img2.octets(L.A_JOURNAL, 8) == entree_originale
                  and img2.qword(L.R_ETAT_PATCH_CORPUS) == 0
                  and img2.qword(L.R_VERROU) == 0
                  and img2.octets(L.A_CROISSANCE, staging_taille)
                  == img2.octets(staging_rva, staging_taille))
    constat("l'entrée du journal restaurée OCTET POUR OCTET, l'état v1, le "
            "verrou rendu, le remplaçant DORMANT dans la croissance (la copie "
            "y reste, réactivable — Q2)",
            etat_image,
            f"staging {staging_taille} o @ {staging_rva:#x}, croissance "
            f"@ {L.A_CROISSANCE:#x} identiques")

    # =====================================================================
    # (d) ZÉRO RÉGRESSION SUR PIÈCES
    # =====================================================================
    lignes.append("[demo] (d) ZÉRO RÉGRESSION SUR PIÈCES")
    with open(chemin, "rb") as f:
        sha_apres = hashlib.sha256(f.read()).hexdigest()
    constat("le FICHIER artefact n'a pas bougé d'un octet (le patch est un "
            "fait de la session, jamais du fichier — re-relu après la "
            "démonstration)", sha_apres == SHA_SCELLE, f"sha256 {sha_apres[:16]}…")
    proc = subprocess.run([chemin], capture_output=True, cwd=ICI)
    constat("le rituel REJOUÉ en exécution réelle : exactement les deux "
            "lignes nominales au code 0 (le patrimoine intègre après la "
            "démonstration)",
            proc.stdout == RITUEL_L1 + RITUEL_L2 and proc.returncode == 0,
            f"code={proc.returncode}, {len(proc.stdout)} o")

    lignes.append(f"[demo] VERDICT : {'VERT' if vert else 'KO'} — le patch "
                  "pendant le trafic, le journal cohérent, le rollback et la "
                  "zéro régression démontrés sur pièces (M5-(c) refermé sur "
                  "le profil Linux — tcp-07 EMBARQUÉ, la bascule V5, "
                  "l'atomicité Q3 sous concurrence réelle)")
    if bavard:
        print("\n".join(lignes))
    return vert, lignes


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    chemin = args[0] if args else None
    try:
        ok, _ = executer(chemin, bavard=True)
        sys.exit(0 if ok else 1)
    except EchecDemo as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
