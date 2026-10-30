#!/usr/bin/env python3
"""sentinelle_cf2.py — la sentinelle du coffre CF2 (D86, v0.6.0 axe 2).

Spécification : v06/I/CF2/README.md § 6 (R2 écrite-avant-code). Un processus
userland long terme qui surveille la COUCHE C (cartes et artefacts) :
lecture de contenu par un processus hors liste blanche -> destruction des
fragments (routine bruler de v06/coffre_cf2.py — source unique de vérité).

Double seuil (spec § 6) : (1) processus hors liste blanche, (2) lecture de
CONTENU — un descripteur ouvert sur un FICHIER de la couche C. Un listage
de répertoire ou un stat() n'ouvre pas de descripteur de fichier : PAS un
signal. Une lecture non attribuée (fd refermé avant le balayage) est
journalée SANS brûler — la discipline du double seuil prime.

D120 (la PORTE de sentinelle — la demande du terrain) : la sentinelle
est EXIGÉE au déverrouillage du coffre — coffre_cf2.porte_sentinelle()
refuse NOMMÉ un heart-beat absent ou périmé AVANT toute reconstitution
de M. « Une sentinelle morte est un avertissement nominal » (ère D86)
est REMPLACÉ par : une sentinelle morte FERME le coffre. Et `demarrer`
REFUSE de lancer une sentinelle là où le moteur n'existe pas (Windows :
exigence consignée spec § 9) — une sentinelle incapable de surveiller ne
battrait qu'un FAUX heart-beat (fail-closed : pas de sécurité de façade).

Moteur de laboratoire (Linux non privilégié — l'utilisateur du bac à sable
n'a pas CAP_SYS_ADMIN, fanotify_init rend EPERM : consigné spec § 6) :
  - inotify (ctypes, autoporté) : IN_OPEN|IN_ACCESS sur fichiers de la
    couche C -> balayage IMMÉDIAT (la latence ne dépend pas du sondage) ;
  - balayage /proc/*/fd : attribution de la lecture à son pid (exe + ligne
    de commande complète), liste blanche par motifs regex ;
  - balayage périodique en secours (robustesse).

Moteur de production Windows : SACL 4663 / ETW — exigence consignée
(spec § 9), même double seuil, même routine de destruction.

Usage (depuis triade/) :
  python3 v06/sentinelle_cf2.py demarrer [--config F]
  python3 v06/sentinelle_cf2.py sante [--config F] [--age-max S]
"""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import re
import select
import signal
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)
from v06 import coffre_cf2 as C                    # noqa: E402

# --- inotify (ctypes) ---------------------------------------------------------

IN_ACCESS = 0x00000001
IN_OPEN = 0x00000020
IN_ISDIR = 0x40000000
MASQUE_SURVEILLANCE = IN_ACCESS | IN_OPEN

_libc = ctypes.CDLL(None, use_errno=True)
try:
    _libc.inotify_init.argtypes = []
    _libc.inotify_init.restype = ctypes.c_int
    _libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p,
                                        ctypes.c_uint32]
    _libc.inotify_add_watch.restype = ctypes.c_int
    _INOTIFY_LIE = True
except AttributeError:
    # D120 : Windows/macOS n'exportent pas inotify — le module reste
    # IMPORTABLE (sante y court), demarrer y refuse NOMMÉ (moteur non
    # livré, exigence consignée spec § 9).
    _INOTIFY_LIE = False


class ArretSentinelle(Exception):
    """SIGTERM/SIGINT -> sortie propre, journalisée."""


def _lire_evenements(fd: int, attente_max: float) -> list[tuple[int, int, str]]:
    """Lit les événements inotify disponibles dans l'attente donnée."""
    selecteur = select.select([fd], [], [], attente_max)
    if not selecteur[0]:
        return []
    brut = os.read(fd, 65536)
    evenements = []
    offset = 0
    while offset + 16 <= len(brut):
        wd = int.from_bytes(brut[offset:offset + 4], "little", signed=True)
        masque = int.from_bytes(brut[offset + 4:offset + 8], "little")
        longueur = int.from_bytes(brut[offset + 12:offset + 16], "little")
        nom = brut[offset + 16:offset + 16 + longueur].split(b"\x00")[0]
        evenements.append((wd, masque, nom.decode("utf-8", "replace")))
        offset += 16 + longueur
    return evenements


# --- Attribution /proc --------------------------------------------------------

def _identity(pid: int) -> tuple[str, str]:
    """(exe résolu, ligne de commande complète) — la liste blanche juge les DEUX."""
    exe = ""
    try:
        exe = os.readlink(f"/proc/{pid}/exe")
    except OSError:
        pass
    cmdline = ""
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            cmdline = f.read().replace(b"\x00", b" ").decode(
                "utf-8", "replace").strip()
    except OSError:
        pass
    return exe, cmdline


def _blanchi(exe: str, cmdline: str, motifs) -> bool:
    for motif in motifs:
        try:
            if re.search(motif, exe) or re.search(motif, cmdline):
                return True
        except re.error:
            print(f"[sentinelle] motif de liste blanche invalide ignoré : "
                  f"{motif!r}", file=sys.stderr)
    return False


class Sentinelle:
    """La boucle : événement -> balayage -> double seuil -> bruler."""

    def __init__(self, config: dict):
        self.config = config
        self.gardes = config["gardes"]
        self.motifs = list(config["liste_blanche"])
        self.periode = float(config.get("periode_sondage", 0.25))
        self.chemins_surveilles = []
        for cible in config["couche_c"]:
            reel = os.path.realpath(cible)
            if reel not in self.chemins_surveilles:
                self.chemins_surveilles.append(reel)
        self.fd_inotify = None
        self.montres = {}
        self.stats = {"lectures_blanchies": 0, "lectures_non_attribuees": 0,
                      "brulages": 0, "boucles": 0}
        self.deja_brule = False
        self._hostilite_deja_dite = set()      # (pid, fichier) — anti-bruit
        self._blanchi_deja_dit = set()
        self._non_attribue_deja_dit = set()
        self._arrete = False

    def _dans_couche_c(self, cible: str) -> bool:
        if cible.endswith(" (deleted)"):
            cible = cible[:-len(" (deleted)")]
        for chemin in self.chemins_surveilles:
            if cible == chemin:
                return True
            if os.path.isdir(chemin) and cible.startswith(chemin + os.sep):
                return True
        return False

    def balayage(self, declencheur_fichier: str | None) -> None:
        """Attribue les descripteurs ouverts dans la couche C.

        Retour implicite par effets : journal, incrémentures, brûlage.
        Double seuil : seuls les fds NON BLANCHIS comptent pour brûler.
        """
        pid_propre = os.getpid()
        attires, offenseurs = [], []
        for pid_str in os.listdir("/proc"):
            if not pid_str.isdigit():
                continue
            pid = int(pid_str)
            if pid == pid_propre:
                continue
            try:
                fds = os.listdir(f"/proc/{pid}/fd")
            except OSError:
                continue
            for nom_fd in fds:
                try:
                    cible = os.readlink(f"/proc/{pid}/fd/{nom_fd}")
                except OSError:
                    continue
                if self._dans_couche_c(cible):
                    exe, cmdline = _identity(pid)
                    if _blanchi(exe, cmdline, self.motifs):
                        attires.append((pid, exe, cible))
                    else:
                        offenseurs.append((pid, exe, cmdline, cible))
                    break
        for pid, exe, cible in attires:
            self.stats["lectures_blanchies"] += 1
            if (pid, cible) not in self._blanchi_deja_dit:
                self._blanchi_deja_dit.add((pid, cible))
                C.journaliser(self.config,
                              f"lecture BLANCHIE : pid {pid} "
                              f"({os.path.basename(exe)}) sur {cible}")
        if offenseurs:
            for pid, exe, cmdline, cible in offenseurs:
                cle = (pid, cible)
                if cle in self._hostilite_deja_dite:
                    continue                    # anti-bruit : une fois par (pid, fichier)
                self._hostilite_deja_dite.add(cle)
                declencheur = (f"pid {pid} ({exe} cmdline={cmdline!r}) lisait "
                               f"{cible} — hors liste blanche (double seuil "
                               "réuni, spec § 6)")
                if self.deja_brule:
                    C.journaliser(self.config,
                                  f"NOUVELLE lecture hostile (coffre déjà "
                                  f"brûlé) : {declencheur}")
                else:
                    print(f"[sentinelle] EXFILTRATION DÉTECTÉE — {declencheur}")
                    C.bruler(self.config, declencheur)
                    self.stats["brulages"] += 1
                    self.deja_brule = True
        elif declencheur_fichier is not None and not any(
                cible == declencheur_fichier for _pid, _exe, cible in attires):
            # un événement inotify fichier SANS fd attribuable SUR CE FICHIER :
            # lecture refermée avant balayage — journalée, PAS brûlée (spec § 6)
            self.stats["lectures_non_attribuees"] += 1
            if declencheur_fichier not in self._non_attribue_deja_dit:
                self._non_attribue_deja_dit.add(declencheur_fichier)
                C.journaliser(self.config,
                              f"lecture NON ATTRIBUÉE : {declencheur_fichier} "
                              "(fd refermé avant balayage — pas de brûlage, "
                              "double seuil incomplet, spec § 6)")

    def heartbeat(self) -> None:
        """Test de santé (spec § 6) : horodatage + fragments par garde."""
        import glob as _glob
        etat = {"ts": time.time(), "pid": os.getpid(),
                "fragments_par_garde": [],
                "seuil": self.config.get("t"), "stats": dict(self.stats)}
        for garde in self.gardes:
            etat["fragments_par_garde"].append(
                len(_glob.glob(os.path.join(garde, C.MOTIF_FRAG))))
        chemin = self.config.get("heartbeat")
        if not chemin:
            return
        os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
        tmp = chemin + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(etat, f)
        os.replace(tmp, chemin)

    def demarrer(self) -> None:
        signal.signal(signal.SIGTERM, self._sur_signal)
        signal.signal(signal.SIGINT, self._sur_signal)
        print(f"[sentinelle] démarrage — {len(self.chemins_surveilles)} "
              f"chemin(s) de couche C, période {self.periode}s, "
              f"{len(self.gardes)} gardes")
        # inotify sur chaque chemin (tolérant : sans inotify, le balayage
        # périodique demeure — moteur dégradé CONSIGNÉ)
        try:
            fd, montres_liste = _monter_surveillance_unique(
                self.chemins_surveilles)
            self.fd_inotify = fd
            self.montres = {wd: chemin for wd, chemin in montres_liste}
            print(f"[sentinelle] inotify ARMÉ : {len(self.montres)} montre(s)")
        except RuntimeError as exc:
            print(f"[sentinelle] moteur dégradé : {exc}", file=sys.stderr)
        C.journaliser(self.config, "sentinelle DÉMARRÉE "
                      f"(pid {os.getpid()})")
        prochaine = time.time() + self.periode
        while not self._arrete:
            try:
                attente = max(0.0, prochaine - time.time())
                evenements = []
                if self.fd_inotify is not None:
                    evenements = _lire_evenements(self.fd_inotify, attente)
                for wd, masque, nom in evenements:
                    if masque & IN_ISDIR:
                        continue                    # listage : PAS un signal
                    if not masque & MASQUE_SURVEILLANCE:
                        continue
                    chemin_base = self.montres.get(wd)
                    if chemin_base is None:
                        continue
                    fichier = nom if os.path.isabs(nom) else os.path.join(
                        chemin_base, nom)
                    self.balayage(fichier)
                if time.time() >= prochaine:
                    self.balayage(None)
                    self.stats["boucles"] += 1
                    self.heartbeat()
                    prochaine = time.time() + self.periode
            except ArretSentinelle:
                break
        self.heartbeat()
        C.journaliser(self.config, "sentinelle ARRÊTÉE "
                      f"(pid {os.getpid()}, stats {json.dumps(self.stats)})")
        print(f"[sentinelle] arrêt — stats : {json.dumps(self.stats)}")

    def _sur_signal(self, numero, cadre) -> None:
        self._arrete = True


def _monter_surveillance_unique(chemins: list):
    """Monte inotify pour TOUS les chemins sur un seul fd."""
    if not _INOTIFY_LIE:
        raise RuntimeError("inotify non disponible sur cette plateforme "
                           "(moteur non livré — spec § 9)")
    fd = _libc.inotify_init()
    if fd < 0:
        errno = ctypes.get_errno()
        raise RuntimeError(f"inotify_init échoue (errno {errno})")
    montres = []
    for cible in chemins:
        if os.path.isdir(cible):
            a_monter = [cible]
            for racine_dir, dirs, _fichiers in os.walk(cible):
                a_monter.extend(os.path.join(racine_dir, d) for d in dirs)
        else:
            a_monter = [cible]
        for chemin in a_monter:
            wd = _libc.inotify_add_watch(fd, os.path.realpath(chemin).encode(),
                                         MASQUE_SURVEILLANCE)
            if wd < 0:
                errno = ctypes.get_errno()
                print(f"[sentinelle] AVERTISSEMENT : add_watch({chemin}) "
                      f"errno {errno} — sondage seul", file=sys.stderr)
                continue
            montres.append((wd, os.path.realpath(chemin)))
    return fd, montres


# --- Santé (spec § 6) ---------------------------------------------------------

def sante(config: dict, age_max: float) -> int:
    exiger = bool(config.get("exiger_sentinelle", False))
    print("[sentinelle] PORTE D120 : exiger_sentinelle="
          f"{str(exiger).lower()}"
          + (" — le déverrouillage du coffre REFUSE sans heart-beat frais"
             if exiger else
             " — le déverrouillage AVERTIT dans cette ère (moteur non "
             "livré, exigence consignée spec § 9)"))
    chemin = config.get("heartbeat")
    if not chemin or not os.path.isfile(chemin):
        print("[sentinelle] SANTÉ : heart-beat ABSENT — sentinelle jamais "
              "démarrée (ou tuée)")
        if exiger:
            print("[sentinelle] D120 : le déverrouillage REFUSERA tant "
                  "qu'elle n'est pas relancée — python3 "
                  "v06/sentinelle_cf2.py demarrer")
        return 1
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            etat = json.load(f)
    except (OSError, ValueError) as exc:
        print(f"[sentinelle] SANTÉ : heart-beat illisible ({exc})")
        return 1
    age = time.time() - etat.get("ts", 0)
    frais = age <= age_max
    print(f"[sentinelle] SANTÉ : {'VIVANTE' if frais else 'MORTE'} "
          f"(heart-beat vieux de {age:.2f}s, borne {age_max}s)")
    print(f"[sentinelle] fragments par garde : "
          f"{etat.get('fragments_par_garde')} — seuil {etat.get('seuil')}")
    stats = etat.get("stats", {})
    print(f"[sentinelle] stats : blanchies={stats.get('lectures_blanchies', 0)} "
          f"non-attribuées={stats.get('lectures_non_attribuees', 0)} "
          f"brûlages={stats.get('brulages', 0)} boucles={stats.get('boucles', 0)}")
    return 0 if frais else 1


# --- CLI ----------------------------------------------------------------------

def main() -> int:
    parseur = argparse.ArgumentParser(
        description="Sentinelle du coffre CF2 (D86, v0.6.0 axe 2)")
    parseur.add_argument("--config", default=C.CHEMIN_CONFIG_DEFAUT)
    parseur.add_argument("mode", choices=["demarrer", "sante"])
    parseur.add_argument("--age-max", type=float, default=1.0,
                         help="sante : fraîcheur maximale du heart-beat (s)")
    args = parseur.parse_args()
    try:
        config = C.lire_config(args.config)
    except C.ErreurCoffre as exc:
        print(f"ECHEC : {exc}", file=sys.stderr)
        return 1
    if args.mode == "sante":
        return sante(config, args.age_max)
    if not C.moteur_sentinelle_disponible():
        print("ECHEC : moteur de sentinelle NON LIVRÉ sur cette plateforme "
              "(exigence consignée spec § 9) — démarrage REFUSÉ : une "
              "sentinelle incapable de surveiller ne battrait qu'un FAUX "
              "heart-beat (fail-closed D120). Dans cette ère, la porte du "
              "coffre AVERTIT à chaque déverrouillage, elle ne refuse pas ; "
              "santé et diagnostic restent disponibles (mode sante).",
              file=sys.stderr)
        return 1
    try:
        Sentinelle(config).demarrer()
    except KeyboardInterrupt:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
