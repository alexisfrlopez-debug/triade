#!/usr/bin/env python3
"""controle_base_reelle.py — LE CONTRÔLE D146 ADAPTÉ au profil x86-64-linux-elf64.

D146 (Entrée 141) : AUCUN scellage rc/final SANS un contrôle d'exécution À LA
BASE RÉELLE de l'image — l'émulation à base 0 n'est pas un témoin de
l'exécution réelle (un RVA nu y résout par accident ; c'est ainsi que le
scellé 0.6.0-rc.1 est mort à la première requête routée du run e3, oracles de
labo verts). L'ADAPTATION au profil Linux (fiche § 8, D149-(6)) : le contrôle
N'ÉMULE RIEN — le bac à sable EST Linux x86-64, l'image PIE est EXÉCUTÉE par
le NOYAU lui-même (execve), à une base que LUI choisit. La base est CONSTATÉE,
jamais décrétée : le fils passe PTRACE_TRACEME avant son exec, le noyau
l'arrête À L'EXEC, le contrôle lit la base dans /proc/<pid>/maps (le mapping
du fichier à l'offset 0 — aligné page, jamais 0).

Les pièces du verdict (fail-closed, chacune tranchée binaire) :
  (a) L'EXÉCUTION PLEINE À LA BASE RÉELLE : SIX exécutions témoignées — une
      base DISTINCTE à chaque fois (l'ASLR du noyau CONSTATÉ, alignée 0x1000,
      >= 0x10000), la sortie EXACTEMENT les deux lignes nominales et le code 0
      — le comportement identique à CHAQUE base (corpus-13:R1 V2) ;
  (b) LE RECOUPEMENT ADDR_NO_RANDOMIZE (personality 0x0040000, le mécanisme
      même de setarch -R) : DEUX exécutions à base figée — la MÊME base deux
      fois (la base vient du noyau, pas du programme), comportement identique ;
  (c) LA FALSIFIABILITÉ — la classe EXACTE du défaut qui tua le rc.1 : un
      mutant « RVA nu » (le lea rip de la chaîne du journal réécrit
      mov edi, 0x280 — l'adresse .rodata SANS la base, le geste de la ligne
      de flux fautive d'http-10:R3) meurt à la base réelle : SIGSEGV NOMMÉ
      (adresse fautive 0x280, RIP rapporté au bloc du plan) — en base
      aléatoire ET en base figée (la base figée du noyau n'est JAMAIS 0 :
      même le témoin unique à base fixe attraperait la classe) — le contrôle
      est falsifiable, zéro silence ;
  (d) FRONTIÈRE NOMMÉE : le moteur de patch n'est PAS dans le flot du rituel
      (corpus-13:R1 I1 — tcp-07 vit pour l'oracle et le chantier (d)) : sa
      démonstration vit à l'oracle natif (mprotect réel, refus EACCES du
      noyau, DEP V7) — une frontière du plan, pas une lacune du contrôle.

Le mutant vit en COPIE temporaire (jamais l'artefact), supprimée au retour.

Usage : python3 controle_base_reelle.py [chemin_artefact] [--bavard]
Retour : executer() -> (vert, lignes) — invoqué par build_corpus._sceller.
"""

from __future__ import annotations

import ctypes
import os
import struct
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import layout as L  # noqa: E402


class EchecControle(Exception):
    """Tout échec nommé du contrôle (fail-closed : jamais un faux vert)."""


# --- Le témoin ptrace : la base CONSTATÉE depuis le noyau -----------------------

PTRACE_TRACEME = 0
PTRACE_CONT = 7
PTRACE_GETSIGINFO = 0x4202
PTRACE_GETREGS = 12
ADDR_NO_RANDOMIZE = 0x0040000
SIGTRAP, SIGSEGV = 5, 11

_libc = ctypes.CDLL("libc.so.6", use_errno=True)
_libc.ptrace.restype = ctypes.c_long
_libc.personality.restype = ctypes.c_int


def _ptrace(fonction, pid, addr=0, donnee=0):
    r = _libc.ptrace(ctypes.c_long(fonction), ctypes.c_long(pid),
                     ctypes.c_void_p(addr), ctypes.c_void_p(donnee))
    if r == -1:
        err = ctypes.get_errno()
        raise EchecControle(f"ptrace({fonction}, {pid}) : errno {err}")
    return r


def _exec_temoin(chemin: str, fige: bool):
    """Exécute le fils sous PTRACE_TRACEME ; CONSTATE la base à l'arrêt d'exec,
    continue, collecte la fin. Retourne un dictionnaire :
    base, code (exit ou -signal), sortie, faute (si_addr, rva_rip) ou None."""
    chemin_abs = os.path.abspath(chemin)

    def pre():
        # Dans le fils, AVANT l'exec : demander la trace (l'arrêt à l'exec
        # est garanti par le noyau) puis figer l'ASLR si demandé.
        _libc.ptrace(PTRACE_TRACEME, 0, None, None)
        if fige:
            _libc.personality(ADDR_NO_RANDOMIZE)

    p = subprocess.Popen([chemin_abs], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, preexec_fn=pre)
    try:
        pid, statut = os.waitpid(p.pid, 0)
        if not os.WIFSTOPPED(statut) or os.WSTOPSIG(statut) != SIGTRAP:
            raise EchecControle(
                f"le fils ne s'est pas arrêté à l'exec (statut {statut:#x}) — "
                f"le témoin de base est muet, le contrôle refuse")
        # La base : le mapping du FICHIER à l'offset 0 (le premier du PIE)
        base = None
        with open(f"/proc/{pid}/maps", encoding="ascii") as f:
            for ligne in f:
                champs = ligne.split()
                if len(champs) >= 6 and champs[-1] == chemin_abs \
                        and champs[2] == "00000000":
                    base = int(champs[0].split("-")[0], 16)
                    break
        if base is None:
            raise EchecControle("aucun mapping du fichier à l'offset 0 — "
                                "la base n'est pas constatable")
        # Continuer ; la suite : sortie normale, ou arrêt-signal (mutant)
        _ptrace(PTRACE_CONT, pid)
        pid, statut2 = os.waitpid(pid, 0)
        faute = None
        if os.WIFSTOPPED(statut2):
            signo = os.WSTOPSIG(statut2)
            # arrêt de remise du signal : LIRE la faute, puis la DÉLIVRER
            # (la livrer est la preuve de mort par le signal même)
            siginfo = ctypes.create_string_buffer(128)
            _ptrace(PTRACE_GETSIGINFO, pid, 0, ctypes.addressof(siginfo))
            si_addr = struct.unpack_from("<Q", siginfo, 16)[0]
            regs = ctypes.create_string_buffer(27 * 8)
            _ptrace(PTRACE_GETREGS, pid, 0, ctypes.addressof(regs))
            rip = struct.unpack_from("<Q", regs, 16 * 8)[0]
            faute = (signo, si_addr, rip)
            _ptrace(PTRACE_CONT, pid, 0, signo)
            pid, statut2 = os.waitpid(pid, 0)
        # Les tuyaux : le fils est terminé, la lecture est totale
        sortie = p.stdout.read()
        p.stdout.close()
        p.stderr.read()
        p.stderr.close()
        if os.WIFEXITED(statut2):
            code = os.WEXITSTATUS(statut2)
        elif os.WIFSIGNALED(statut2):
            code = -os.WTERMSIG(statut2)
        else:
            raise EchecControle(f"fin inattendue du fils (statut {statut2:#x})")
        p.returncode = code          # le fils est déjà récolté (jamais p.wait)
        return {"base": base, "code": code, "sortie": sortie, "faute": faute}
    finally:
        if p.poll() is None and p.returncode is None:
            try:
                os.kill(p.pid, 9)
                os.waitpid(p.pid, 0)
            except (ProcessLookupError, ChildProcessError):
                pass


def _bloc_depuis_rva(rva: int) -> str:
    # la plage EXACTE du slot du plan (jamais une approximation : la faute
    # est NOMMÉE, son bloc aussi)
    for bid, spec, _, r, slot in L.BLOCS_CORPUS:
        if r <= rva < r + slot:
            return f"{bid} ({spec})"
    return f"hors blocs (rva {rva:#x})"


# --- Le mutant « RVA nu » : la classe du défaut du rc.1, en COPIE ---------------

def _fabriquer_mutant(chemin: str) -> str:
    """Le lea rdi, [rip - 0x19cf] de corpus-13 (0x1c48, 7 o — la chaîne du
    journal @J_PREF) réécrit mov edi, 0x280 + NOP x2 : l'adresse .rodata SANS
    la base — exactement le geste RVA-nu de la ligne de flux fautive du
    0.6.0-rc.1 (Entrée 141). La copie porte l'extension .mutant-rva."""
    with open(chemin, "rb") as f:
        art = bytearray(f.read())
    attendu = bytes.fromhex("488d3d31e6ffff")       # lea rdi, [rip - 0x19cf]
    if bytes(art[0x1C48:0x1C4F]) != attendu:
        raise EchecControle("corpus-13 @0x1C48 : le lea de @J_PREF introuvable — "
                            "la notation a changé, le mutant doit être réécrit "
                            "(le contrôle refuse de tester la mauvaise classe)")
    art[0x1C48:0x1C4F] = bytes.fromhex("bf8002000090" + "90")  # mov edi,0x280 ; nop ; nop
    chemin_mutant = os.path.join(ICI, "corpus.mutant-rva")
    with open(chemin_mutant, "wb") as f:
        f.write(bytes(art))
    os.chmod(chemin_mutant, 0o755)
    return chemin_mutant


# --- Le contrôle ----------------------------------------------------------------

SORTIE_ATTENDUE = (b"TRIADE M1 : minilibc 21/21 OK\n"
                   b"corpus : autotest 21 vecteurs\n")


def executer(bavard: bool = True) -> tuple[bool, list[str]]:
    """Le verdict : (vert, lignes). Fail-closed — toute pièce manquante = KO."""
    chemin = os.path.join(ICI, "corpus")
    lignes = []
    vert = True

    def constat(nom, ok, detail=""):
        nonlocal vert
        vert &= bool(ok)
        lignes.append(f"[D146] {'PASS' if ok else 'ECHEC'} : {nom}"
                      + (f" ({detail})" if detail else ""))

    # (a) six exécutions à la base réelle — bases DISTINCTES, comportement identique
    bases, verts = [], 0
    for _ in range(6):
        r = _exec_temoin(chemin, fige=False)
        bases.append(r["base"])
        if r["code"] == 0 and r["sortie"] == SORTIE_ATTENDUE:
            verts += 1
    distinctes = len(set(bases))
    constat("l'exécution pleine à la base réelle : 6/6 vertes "
            "(deux lignes exactes, code 0)", verts == 6)
    constat("l'ASLR du noyau CONSTATÉ : 6 bases DISTINCTES sur 6 exécutions "
            "(alignées 0x1000, jamais décrétées — le témoin ptrace/maps)",
            distinctes == 6 and all(b & 0xFFF == 0 and b >= 0x10000 for b in bases),
            f"{distinctes}/6 distinctes ; ex. {min(bases):#x}")
    if bavard:
        for b in bases:
            lignes.append(f"[D146]   base noyau : {b:#x}")

    # (b) ADDR_NO_RANDOMIZE : la MÊME base deux fois (elle vient du noyau)
    r1 = _exec_temoin(chemin, fige=True)
    r2 = _exec_temoin(chemin, fige=True)
    constat("ADDR_NO_RANDOMIZE : même base deux fois (le mécanisme de "
            "setarch -R), comportement identique",
            r1["base"] == r2["base"]
            and r1["code"] == r2["code"] == 0
            and r1["sortie"] == r2["sortie"] == SORTIE_ATTENDUE,
            f"base figée {r1['base']:#x}")

    # (c) la falsifiabilité : le RVA nu meurt à la base réelle, NOMMÉ
    chemin_mutant = _fabriquer_mutant(chemin)
    try:
        m1 = _exec_temoin(chemin_mutant, fige=False)
        m2 = _exec_temoin(chemin_mutant, fige=True)
        for r, eti in ((m1, "base aléatoire"), (m2, "base figée")):
            nomme = (r["faute"] is not None and r["faute"][0] == SIGSEGV
                     and r["code"] == -SIGSEGV)
            detail = ""
            if nomme:
                signo, si_addr, rip = r["faute"]
                rva = rip - r["base"]
                detail = (f"SIGSEGV à {si_addr:#x} (le RVA nu 0x280 sans la base), "
                          f"RIP=base+{rva:#x} {_bloc_depuis_rva(rva)}")
            constat(f"le mutant RVA nu meurt à la base réelle ({eti}) : "
                    "SIGSEGV nommé — la classe du crash rc.1 attrapée, zéro silence",
                    nomme, detail)
    finally:
        if os.path.exists(chemin_mutant):
            os.unlink(chemin_mutant)

    # (d) la frontière nommée : le patch vit à l'oracle (le chantier (d))
    lignes.append("[D146] LIMITE : le moteur de patch n'est pas dans le flot du "
                  "rituel (corpus-13:R1 I1) — sa démonstration est à l'oracle "
                  "natif (mprotect réel, EACCES, DEP V7) et au chantier (d) : "
                  "frontière du plan, pas une lacune du contrôle")

    lignes.append(f"[D146] VERDICT : {'VERT' if vert else 'KO'} — l'image PIE "
                  f"exécutée par le noyau à {distinctes} bases réelles distinctes, "
                  f"le comportement identique à chaque base, le RVA nu nommé mort")
    if bavard:
        print("\n".join(lignes))
    return vert, lignes


if __name__ == "__main__":
    try:
        ok, _ = executer(bavard=True)
        sys.exit(0 if ok else 1)
    except EchecControle as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
