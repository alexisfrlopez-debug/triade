#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-shani.py — LA MESURE AVANT/APRÈS SHA-NI (kit D205), CORRIGÉE.

LE KIT PORTE TROIS PIÈCES ET UN SCÉNARIO :
  cibles/proxy-image.bin   l'image mémoire ÉTENDUE de la pièce scellée
                           proxy.exe 1.0.0 (sha256 446279f3…, D-密封) —
                           chaque section posée à son RVA, la taille
                           SizeOfImage — la découpe honnête : tls13-02 lit
                           sa table K en .rdata par RIP-relatif (RVA 0x2F00),
                           un bloc isolé FAUT ;
  moteur-shani.bin         le blob moteur du kit (sha256 scellé ci-dessous,
                           source moteur-shani.s jointe — la révision vit
                           aux sources) : la compression SHA-256 par
                           EXTENSIONS SHA (sha256rnds2/msg1/msg2), les deux
                           moteurs de chronométrage RDTSC et la lecture
                           CPUID ;
  le présent script        python SEUL (ctypes, hashlib, os, platform,
                           struct, sys, time — AUCUN paquet à installer).

POURQUOI CETTE VERSION REMPLACE LA PREMIÈRE (le correctif, 12/11) :
  la première livraison plantait au premier geste par « access violation
  writing 0xFFFFFFFFD4991000 ». L'adresse fautive est l'extension de signe
  d'un pointeur 64 bits TRONQUÉ en 32 bits signés (0xD4991000) : un appel
  système rendant un pointeur (VirtualAlloc) avait son type de retour laissé
  par défaut — ctypes le tronque en c_int 32 bits SIGNÉ, le memmove
  l'étendait en négatif. LE CORRECTIF : chaque API rendant un pointeur
  porte restype = c_void_p EXPLICITE, les adresses vivent en entiers NON
  SIGNÉS 64 bits, et CHAQUE écriture dans l'arène est BORNÉE (toute
  écriture hors bornes est un REFUS NOMMÉ avant le premier octet).

CE QUE LE RUN MESURE (chaque constat tranché, le verdict POST-MORTEM —
un échec nommé vaut plus qu'un vert muet) :

  T0 LE TÉMOIN    l'empreinte des DEUX pièces ASSERTÉE avant tout geste ;
                 le silicium lu par CPUID (fabricant, famille, modèle —
                 la disponibilité SHA SE CONSTATE, elle ne se suppose
                 pas : un CPU sans SHA-NI est un ÉCHEC NOMMÉ, pas une
                 panne) ; l'environnement consigné.
  T1 L'ARÈNE      l'allocation exécutable (VirtualAlloc sous Windows,
                 mmap en autotest POSIX) — POINTEURS 64 BITS NON SIGNÉS,
                 écritures bornées fin incluse ; l'image scellée et le
                 blob moteur posés ; (POSIX seulement : les trampolines
                 SysV→Windows — le terrain Windows appelle les entrées
                 DIRECTEMENT, c'est son ABI natif).
  T2 LES LECTEURS le condensé FIPS 180-4 « abc » EXIGÉ IDENTIQUE des
                 TROIS lecteurs : tls13-02 (LA PIÈCE SCELLÉE, appelée à
                 son adresse mappée base+0xC080), shani_compress (le blob
                 moteur), et le miroir python pur du kit ; l'adversaire :
                 UN octet de la table K muté → le condensé de la pièce
                 DOIT diverger, la restauration DOIT rendre l'exact (la
                 preuve que l'image exécutée EST la pièce recoupée).
  T3 LA MESURE    l'affinité posée à UN cœur ; l'échauffement ; N = 101
                 échantillons de 256 compressions par camp, sur TROIS
                 blocs fixes (abc, aléa déterministe, zéros) ; la médiane
                 cycles/compression de CHAQUE camp, le contrepoint
                 horloge (QPC / CLOCK_MONOTONIC), et LE RAPPORT avant/
                 après — le gain DE CETTE MACHINE, consigné comme tel.
  T4 LE TÉMOIN    ./preuves-shani/ : temoin-shani.txt (tout ce qui
                 précède, horodaté), scenario-shani-journal.log,
                 VERDICT-run-shani.txt, moteur-shani-execute.bin (les
                 octets EXACTS exécutés) — à renvoyer ENTIERS au coffre
                 /test (dossier Drive « Triade » → « test »).
  T5 LA CLÔTURE   l'image RELUE dans l'arène après la mesure (empreinte
                 re-vérifiée — la pièce ne fut que lue et exécutée,
                 jamais écrite), l'arène libérée, les fichiers du kit
                 jamais touchés.

L'HONNÊTETÉ DU KIT : le rapport mesuré appartient à LA machine qui
exécute ce scénario — aucun chiffre n'est fabriqué, aucun n'est
généralisé ; l'autotest POSIX du laboratoire (ce script tourne sous
Linux pour éprouver le MÉCANISME) ne confère AUCUN statut terrain.

Usage : scenario-shani.py            (depuis le dossier kit-shani/)
"""

import ctypes
import hashlib
import os
import platform
import struct
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
PREUVES = os.path.join(ICI, "preuves-shani")

# --- les pièces : les empreintes scellées (la source unique) ---------------------
SHA_MOTEUR = ("761ab194d88d527c653111a41324b0bb3e9247b1c56ba8dc9fedeeccb"
              "e04bcec")
SHA_IMAGE = ("0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a"
             "885dff")
SHA_PLAGE_TLS13_02 = ("2ce2517a5eb32c0282b60b6dbac4e7545fc1bd16a7f9ea431b"
                      "bbd4705d022b46")
RVA_TLS13_02 = 0xC080          # la compression SHA-256 de la pièce scellée
TAILLE_SLOT = 0x1C0
RVA_TABLE_K = 0x2F00           # la table K de .rdata (RIP-relative)

# --- le blob moteur : les symboles (consignés par le générateur) ------------------
OFF_SHANI = 0x0                # shani_compress(rcx=etat, rdx=bloc) → rax=0
OFF_AVANT = 0x356              # moteur_avant(rcx=f, rdx=etat, r8=bloc, r9=n)
OFF_APRES = 0x3BD              # moteur_apres(rcx=etat, rdx=bloc, r8=n)
OFF_CPUID = 0x420              # cpuid_bloc(rcx=feuille, rdx=sous-f., r8=sortie)

# --- le protocole de mesure (consigné au témoin) ---------------------------------
N_ECHANTILLONS = 101           # impair : la médiane tombe sur un échantillon
BOUCLES = 256                  # compressions par échantillon
ECHAUFFEMENT = 64

# --- le vecteur FIPS et l'état initial (les mots u32, en MÉMOIRE petit-boutiste) --
H0_MOTS = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
           0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)
H0 = struct.pack("<8I", *H0_MOTS)
FIPS_ABC = ("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f2"
            "0015ad")
K256_MODELE = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

# --- le journal, le témoin, le verdict -------------------------------------------
_journal = []
_temoin = []
_echecs = []
_POSIX = os.name == "posix"


def journal(msg):
    _journal.append(time.strftime("%H:%M:%S") + "  " + msg)
    print("[journal] " + msg)
    _ecrire_journal()


def temoin(msg):
    _temoin.append(msg)
    print("  " + msg)


def verifie(nom, condition, detail=""):
    if condition:
        temoin(f"[ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        temoin(f"[ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))
        _echecs.append(nom)
    return bool(condition)


def _ecrire_journal():
    try:
        os.makedirs(PREUVES, exist_ok=True)
        with open(os.path.join(PREUVES, "scenario-shani-journal.log"), "w",
                  encoding="utf-8") as f:
            f.write("\n".join(_journal) + "\n")
    except OSError:
        pass


def sha256_octets(donnees):
    return hashlib.sha256(donnees).hexdigest()


# --- le miroir python pur de la compression (le troisième lecteur) ---------------
def _ror(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF


def compression_miroir(etat_mots, bloc):
    """La compression FIPS en python pur — le lecteur indépendant."""
    w = list(struct.unpack(">16I", bloc))
    for i in range(16, 64):
        s0 = _ror(w[i-15], 7) ^ _ror(w[i-15], 18) ^ (w[i-15] >> 3)
        s1 = _ror(w[i-2], 17) ^ _ror(w[i-2], 19) ^ (w[i-2] >> 10)
        w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)
    a, b, c, d, e, f, g, h = etat_mots
    for i in range(64):
        s1 = _ror(e, 6) ^ _ror(e, 11) ^ _ror(e, 25)
        ch = (e & f) ^ ((~e & 0xFFFFFFFF) & g)
        t1 = (h + s1 + ch + K256_MODELE[i] + w[i]) & 0xFFFFFFFF
        s0 = _ror(a, 2) ^ _ror(a, 13) ^ _ror(a, 22)
        mj = (a & b) ^ (a & c) ^ (b & c)
        t2 = (s0 + mj) & 0xFFFFFFFF
        h, g, f, e, d, c, b, a = (g, f, e, (d + t1) & 0xFFFFFFFF,
                                  c, b, a, (t1 + t2) & 0xFFFFFFFF)
    return [(x + y) & 0xFFFFFFFF
            for x, y in zip((a, b, c, d, e, f, g, h), etat_mots)]


def mots_vers_hex(mots):
    return "".join(f"{x:08x}" for x in mots)


# --- l'arène : les pointeurs 64 bits NON SIGNÉS, les écritures BORNÉES -----------
class Arene:
    """L'arène exécutable — LE CORRECTIF INCARNÉ : tout pointeur rendu par
    une API porte restype = c_void_p EXPLICITE (le défaut c_int TRONQUE
    en 32 bits signés — la faute 0xFFFFFFFFD4991000 de la première
    livraison), et toute écriture est bornée FIN INCLUSE : un débordement
    est un REFUS NOMMÉ, jamais une écriture chez le voisin."""

    def __init__(self, taille):
        self.taille = taille
        if os.name == "nt":
            k32 = ctypes.windll.kernel32
            # LE CORRECTIF : restype c_void_p, JAMAIS le c_int par défaut
            k32.VirtualAlloc.restype = ctypes.c_void_p
            k32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                         ctypes.c_uint32, ctypes.c_uint32]
            MEM_COMMIT, MEM_RESERVE = 0x1000, 0x2000
            PAGE_EXECUTE_READWRITE = 0x40
            brut = k32.VirtualAlloc(None, taille,
                                    MEM_COMMIT | MEM_RESERVE,
                                    PAGE_EXECUTE_READWRITE)
            if not brut:
                raise RuntimeError("VirtualAlloc refusée")
            self.base = int(brut) & 0xFFFFFFFFFFFFFFFF   # NON SIGNÉ
            self._k32 = k32
        else:
            libc = ctypes.CDLL(None)
            libc.mmap.restype = ctypes.c_void_p          # idem, explicite
            libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                  ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                  ctypes.c_int]
            brut = libc.mmap(None, taille, 7, 0x22, -1, 0)
            if not brut or brut == ctypes.c_void_p(-1).value:
                raise RuntimeError("mmap refusée")
            self.base = int(brut) & 0xFFFFFFFFFFFFFFFF
            self._libc = libc

    def ecrire(self, offset, donnees):
        adr = self.base + offset
        fin = adr + len(donnees)
        if (adr < self.base or fin > self.base + self.taille):
            raise RuntimeError(
                f"[REFUS] écriture hors arène : {adr:#x}+{len(donnees)} o "
                f"(l'arène couvre [{self.base:#x} ; "
                f"{self.base + self.taille:#x}])")
        ctypes.memmove(adr, donnees, len(donnees))

    def lire(self, offset, taille):
        if (self.base + offset < self.base
                or offset + taille > self.taille):
            raise RuntimeError("[REFUS] lecture hors arène")
        return ctypes.string_at(self.base + offset, taille)

    def liberer(self):
        try:
            if os.name == "nt":
                MEM_RELEASE = 0x8000
                self._k32.VirtualFree.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_size_t,
                                                  ctypes.c_uint32]
                self._k32.VirtualFree(ctypes.c_void_p(self.base), 0,
                                      MEM_RELEASE)
            else:
                self._libc.munmap.argtypes = [ctypes.c_void_p,
                                              ctypes.c_size_t]
                self._libc.munmap(ctypes.c_void_p(self.base), self.taille)
        except Exception:
            pass


def _rel32(fin, cible):
    ecart = cible - fin
    if not -(1 << 31) <= ecart < (1 << 31):
        raise RuntimeError(f"[REFUS] saut relatif hors portée : {ecart:#x}")
    return struct.pack("<i", ecart)


# les trampolines SysV → Windows x64 (l'AUTOTEST POSIX SEULEMENT — le
# terrain Windows appelle les entrées natives ; encodages canoniques
# vérifiés par assemblage croisé GAS, jamais écrits de tête)
_TRAMPO_2 = b"\x48\x89\xf9" + b"\x48\x89\xf2"           # rcx←rdi, rdx←rsi
_TRAMPO_3 = (b"\x49\x89\xd0" + b"\x48\x89\xf9" + b"\x48\x89\xf2")
_TRAMPO_4 = (b"\x49\x89\xd0" + b"\x49\x89\xc9" + b"\x48\x89\xf9"
             + b"\x48\x89\xf2")


def poser_trampoline(arene, offset, cible, nargs):
    corps = {2: _TRAMPO_2, 3: _TRAMPO_3, 4: _TRAMPO_4}[nargs]
    ici = arene.base + offset
    arene.ecrire(offset, corps + b"\xe9" + _rel32(ici + len(corps) + 5,
                                                  cible))
    return ici


# --- l'affinité et l'horloge (les deux arrière-pays) -----------------------------
def poser_affinite(coeur):
    if os.name == "nt":
        k32 = ctypes.windll.kernel32
        k32.GetCurrentThread.restype = ctypes.c_void_p
        k32.SetThreadAffinityMask.restype = ctypes.c_uint64
        k32.SetThreadAffinityMask.argtypes = [ctypes.c_void_p,
                                              ctypes.c_uint64]
        return bool(k32.SetThreadAffinityMask(k32.GetCurrentThread(),
                                              1 << coeur))
    try:
        libc = ctypes.CDLL(None)
        libc.sched_setaffinity.argtypes = [ctypes.c_int, ctypes.c_size_t,
                                           ctypes.c_void_p]
        masque = struct.pack("<Q", 1 << coeur)
        return libc.sched_setaffinity(0, 8, masque) == 0
    except Exception:
        return False


def horloge_sec():
    if os.name == "nt":
        k32 = ctypes.windll.kernel32
        c = ctypes.c_int64()
        f = ctypes.c_int64()
        k32.QueryPerformanceCounter(ctypes.byref(c))
        k32.QueryPerformanceFrequency(ctypes.byref(f))
        return c.value / f.value
    return time.monotonic()


# --- LE SCÉNARIO -----------------------------------------------------------------
def main():
    print("=== scenario-shani.py — LA MESURE AVANT/APRÈS SHA-NI "
          "(kit D205, corrigée) ===")
    nom_machine = platform.node() or "?"
    print(f"machine : {nom_machine} · {platform.machine()} · "
          f"{platform.system()} · Python {platform.python_version()}"
          + (" · AUTOTEST LABORATOIRE (POSIX) — le mécanisme seul, "
             "AUCUN statut terrain" if _POSIX else " · LE RUN TERRAIN"))
    print()

    # ---- T0 LE TÉMOIN : les pièces et le silicium --------------------------
    journal("T0 — le témoin : les empreintes et le silicium")
    chemin_moteur = os.path.join(ICI, "moteur-shani.bin")
    chemin_image = os.path.join(ICI, "cibles", "proxy-image.bin")
    try:
        moteur = open(chemin_moteur, "rb").read()
        image = open(chemin_image, "rb").read()
    except OSError as e:
        print(f"[ÉCHEC] pièce introuvable : {e}")
        return 2
    sha_m = sha256_octets(moteur)
    sha_i = sha256_octets(image)
    verifie("T0.moteur : le blob moteur est la pièce scellée",
            sha_m == SHA_MOTEUR, f"sha256 {sha_m[:16]}…")
    verifie("T0.image : l'image étendue est la pièce scellée",
            sha_i == SHA_IMAGE, f"sha256 {sha_i[:16]}…")
    plage = image[RVA_TLS13_02:RVA_TLS13_02 + TAILLE_SLOT]
    sha_p = sha256_octets(plage)
    verifie("T0.plage : tls13-02 à son RVA, la plage scellée",
            sha_p == SHA_PLAGE_TLS13_02, f"RVA {RVA_TLS13_02:#x}, "
            f"sha256 {sha_p[:16]}…")
    if _echecs:
        return 2

    # ---- T1 L'ARÈNE ----------------------------------------------------------
    journal("T1 — l'arène : l'allocation, la pose des pièces")
    arene = Arene(0x20000)
    try:
        arene.ecrire(0x1000, moteur)
        arene.ecrire(0x2000, image)
        shani = arene.base + 0x1000 + OFF_SHANI
        f_avant_adr = arene.base + 0x1000 + OFF_AVANT
        f_apres_adr = arene.base + 0x1000 + OFF_APRES
        cpuid_adr = arene.base + 0x1000 + OFF_CPUID
        tls13_02 = arene.base + 0x2000 + RVA_TLS13_02
        temoin(f"[arène] base {arene.base:#x} — blob à +0x1000, "
               f"l'image scellée à +0x2000, tls13-02 à {tls13_02:#x}")

        # la lecture CPUID par le blob (la disponibilité se CONSTATE)
        F_CPUID = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_uint32,
                                   ctypes.c_uint32, ctypes.c_void_p)
        out_cpuid = ctypes.create_string_buffer(16)
        if os.name == "nt":
            f_cpuid = F_CPUID(cpuid_adr)
        else:
            f_cpuid = F_CPUID(poser_trampoline(arene, 0x1C0, cpuid_adr, 3))
        f_cpuid(0, 0, out_cpuid)
        eax0, ebx0, ecx0, edx0 = struct.unpack("<4I", bytes(out_cpuid))
        vendeur = struct.pack("<3I", ebx0, edx0, ecx0).decode(
            "ascii", "replace")
        f_cpuid(1, 0, out_cpuid)
        eax1 = struct.unpack("<I", bytes(out_cpuid)[:4])[0]
        famille = ((eax1 >> 8) & 0xF) + ((eax1 >> 20) & 0xFF)
        modele = ((eax1 >> 4) & 0xF) | (((eax1 >> 16) & 0xF) << 4)
        pas = eax1 & 0xF
        sha_dispo = False
        if eax0 >= 7:
            f_cpuid(7, 0, out_cpuid)
            ebx7 = struct.unpack("<4I", bytes(out_cpuid))[1]
            sha_dispo = bool(ebx7 & (1 << 29))
        temoin(f"[cpuid] « {vendeur} » · famille {famille} · modèle "
               f"{modele} · pas {pas} · SHA-NI "
               f"{'PRÉSENT' if sha_dispo else 'ABSENT'}")
        if not verifie("T0.silicium : les extensions SHA sont présentes",
                       sha_dispo,
                       "CPUID feuille 7, EBX bit 29 — le kit mesure du "
                       "SHA-NI, sans lui le geste n'existe pas"):
            _ecrire_verdict()
            return 3

        # les appels natifs : DIRECTS sous Windows (c'est l'ABI), par
        # trampoline sous POSIX (l'autotest)
        F2 = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p,
                              ctypes.c_void_p)
        F3 = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p,
                              ctypes.c_void_p, ctypes.c_uint32)
        F4 = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p,
                              ctypes.c_void_p, ctypes.c_void_p,
                              ctypes.c_uint32)
        if os.name == "nt":
            f_shani, f_tls = F2(shani), F2(tls13_02)
            f_avant, f_apres = F4(f_avant_adr), F3(f_apres_adr)
        else:
            f_shani = F2(poser_trampoline(arene, 0x1E0, shani, 2))
            f_tls = F2(poser_trampoline(arene, 0x260, tls13_02, 2))
            f_avant = F4(poser_trampoline(arene, 0x200, f_avant_adr, 4))
            f_apres = F3(poser_trampoline(arene, 0x220, f_apres_adr, 3))

        # ---- T2 LES LECTEURS : le FIPS « abc » par les trois -----------------
        journal("T2 — les lecteurs : le FIPS « abc » et l'adversaire K")
        bloc_abc = b"abc\x80" + b"\x00" * 52 + struct.pack(">Q", 24)
        etat = ctypes.create_string_buffer(H0, 32)
        bloc = ctypes.create_string_buffer(bloc_abc, 64)
        f_shani(etat, bloc)
        c_shani = mots_vers_hex(struct.unpack("<8I", bytes(etat)))
        etat2 = ctypes.create_string_buffer(H0, 32)
        f_tls(etat2, bloc)
        c_tls = mots_vers_hex(struct.unpack("<8I", bytes(etat2)))
        c_miroir = mots_vers_hex(compression_miroir(list(H0_MOTS),
                                                    bloc_abc))
        verifie("T2.shani : le condensé FIPS « abc » EXACT",
                c_shani == FIPS_ABC, c_shani[:32] + "…")
        verifie("T2.pièce : tls13-02 (la pièce scellée) rend le MÊME EXACT",
                c_tls == FIPS_ABC, c_tls[:32] + "…")
        verifie("T2.miroir : le python pur rend le MÊME EXACT",
                c_miroir == FIPS_ABC, c_miroir[:32] + "…")

        # l'adversaire : un octet de la table K muté → la pièce DOIT
        # diverger (la preuve que l'image exécutée EST celle recoupée)
        k_adr = arene.base + 0x2000 + RVA_TABLE_K
        octet_sauve = ctypes.string_at(k_adr, 1)
        ctypes.memmove(k_adr, bytes([octet_sauve[0] ^ 0x01]), 1)
        etat3 = ctypes.create_string_buffer(H0, 32)
        f_tls(etat3, bloc)
        c_mute = mots_vers_hex(struct.unpack("<8I", bytes(etat3)))
        diverge = c_mute != FIPS_ABC
        ctypes.memmove(k_adr, octet_sauve, 1)
        etat4 = ctypes.create_string_buffer(H0, 32)
        f_tls(etat4, bloc)
        c_restaure = mots_vers_hex(struct.unpack("<8I", bytes(etat4)))
        verifie("T2.adversaire : la mutation d'un octet de K fait diverger",
                diverge, "le condensé DIVERGE — la table est BIEN lue "
                "par la pièce")
        verifie("T2.restauration : la table K rendue, le condensé EXACT",
                c_restaure == FIPS_ABC)
        if _echecs:
            _ecrire_verdict()
            return 4

        # ---- T3 LA MESURE ------------------------------------------------------
        journal("T3 — la mesure : l'avant (pièce scellée) contre "
                "l'après (SHA-NI)")
        aff_ok = poser_affinite(0)
        temoin(f"[affinité] cœur 0 "
               f"{'posé' if aff_ok else 'REFUSÉ (consigné, la mesure suit)'}")
        temoin(f"[protocole] {N_ECHANTILLONS} échantillons × "
               f"{BOUCLES} compressions · échauffement {ECHAUFFEMENT} · "
               f"RDTSC sérialisé (lfence) + horloge "
               f"{'QPC' if os.name == 'nt' else 'CLOCK_MONOTONIC'} · "
               f"turbo : état non sondé (à consigner manuellement si le "
               f"BIOS le permet)")

        # les trois blocs : abc, l'aléa déterministe (graine 0xD205),
        # les zéros — les MÊMES entrées pour les deux camps
        graine = 0xD205
        alea = b""
        for _ in range(16):
            graine = (graine * 1664525 + 1013904223) & 0xFFFFFFFF
            alea += struct.pack("<I", graine)
        blocs_mesure = [("abc (le vecteur)", bloc_abc),
                        ("aléa déterministe", alea),
                        ("zéros", b"\x00" * 64)]

        # la pré-vérification : chaque bloc, UNE compression par les
        # trois lecteurs d'accord, PUIS l'enchaînement 256× des natifs
        # confronté au miroir (la preuve que la boucle chronométrée
        # compresse VRAIMENT ce bloc)
        for nom_bloc, donnees in blocs_mesure:
            etat_p = ctypes.create_string_buffer(H0, 32)
            bloc_p = ctypes.create_string_buffer(donnees, 64)
            f_tls(etat_p, bloc_p)
            c1 = mots_vers_hex(struct.unpack("<8I", bytes(etat_p)))
            etat_p2 = ctypes.create_string_buffer(H0, 32)
            f_shani(etat_p2, bloc_p)
            c2 = mots_vers_hex(struct.unpack("<8I", bytes(etat_p2)))
            c3 = mots_vers_hex(compression_miroir(list(H0_MOTS), donnees))
            verifie(f"T3.blocs · {nom_bloc} : une compression, les trois "
                    "lecteurs d'accord", c1 == c3 and c2 == c3)
            etat_q = ctypes.create_string_buffer(H0, 32)
            for _ in range(BOUCLES):
                f_tls(etat_q, bloc_p)
            c4 = mots_vers_hex(struct.unpack("<8I", bytes(etat_q)))
            mots = list(H0_MOTS)
            for _ in range(BOUCLES):
                mots = compression_miroir(mots, donnees)
            verifie(f"T3.blocs · {nom_bloc} : {BOUCLES} enchaînements, "
                    "le natif == le miroir", c4 == mots_vers_hex(mots))

        resultats = {}
        for nom_bloc, donnees in blocs_mesure:
            bloc_m = ctypes.create_string_buffer(donnees, 64)
            # l'échauffement des deux camps
            etat_e = ctypes.create_string_buffer(H0, 32)
            f_avant(tls13_02, etat_e, bloc_m, ECHAUFFEMENT)
            f_apres(etat_e, bloc_m, ECHAUFFEMENT)
            ech_avant, ech_apres, sec_avant, sec_apres = [], [], [], []
            for _ in range(N_ECHANTILLONS):
                etat_s = ctypes.create_string_buffer(H0, 32)
                t0 = horloge_sec()
                ech_avant.append(f_avant(tls13_02, etat_s, bloc_m,
                                         BOUCLES))
                t1 = horloge_sec()
                ech_apres.append(f_apres(etat_s, bloc_m, BOUCLES))
                t2 = horloge_sec()
                sec_avant.append(t1 - t0)
                sec_apres.append(t2 - t1)
            ech_avant.sort()
            ech_apres.sort()
            sec_avant.sort()
            sec_apres.sort()
            med = N_ECHANTILLONS // 2
            c_avant = ech_avant[med] / BOUCLES
            c_apres = ech_apres[med] / BOUCLES
            s_avant = sec_avant[med] / BOUCLES
            s_apres = sec_apres[med] / BOUCLES
            rapport = c_avant / c_apres if c_apres else float("inf")
            resultats[nom_bloc] = (c_avant, c_apres, s_avant, s_apres,
                                   rapport)
            temoin(f"[mesure · {nom_bloc}] avant {c_avant:.1f} cyc/bloc "
                   f"({s_avant*1e9:.1f} ns) — après {c_apres:.1f} "
                   f"cyc/bloc ({s_apres*1e9:.1f} ns) — le rapport "
                   f"{rapport:.2f}× sur CE silicium")

        # ---- T4 LE TÉMOIN ------------------------------------------------------
        journal("T4 — le témoin : la consignation")
        os.makedirs(PREUVES, exist_ok=True)
        principal = resultats["aléa déterministe"]
        lignes = [
            "TÉMOIN SHA-NI (kit D205, la mesure avant/après) — "
            + time.strftime("%Y-%m-%d %H:%M:%S"),
            f"machine : {nom_machine} · {platform.machine()} · "
            f"{platform.system()} · Python {platform.python_version()}",
            f"silicium : {vendeur} · famille {famille} · modèle "
            f"{modele} · pas {pas} · SHA-NI présent",
            f"affinité : cœur 0 "
            f"{'posé' if aff_ok else 'refusée (consigné)'} ; turbo : "
            "état non sondé (à consigner manuellement si le BIOS le "
            "permet)",
            "",
            "LES PIÈCES (recoupées AVANT et APRÈS le run) :",
            f"  proxy-image.bin : sha256 {sha_i} (l'image étendue de la "
            "pièce scellée proxy.exe 1.0.0, 446279f3…)",
            f"  moteur-shani.bin : sha256 {sha_m} (source "
            "moteur-shani.s ; la révision vit aux sources)",
            f"  tls13-02 : RVA {RVA_TLS13_02:#x}, plage scellée "
            f"{sha_p[:16]}… — l'AVANT",
            "",
            f"LE PROTOCOLE : {N_ECHANTILLONS} échantillons × {BOUCLES} "
            f"compressions, échauffement {ECHAUFFEMENT}, médiane ; "
            "RDTSC sérialisé (lfence avant, rdtscp+lfence après) ; "
            "horloge " + ("QPC" if os.name == "nt"
                          else "CLOCK_MONOTONIC") + " en contrepoint.",
            "",
            "L'EXACTITUDE AVANT LA MESURE (les trois lecteurs) :",
            f"  FIPS 180-4 « abc » : tls13-02 (pièce scellée), "
            "shani_compress et le miroir python rendent TOUS",
            f"  {FIPS_ABC}",
            "  l'adversaire : un octet de la table K muté → la pièce "
            "diverge ; restauré → l'exact revient.",
            "",
            "LA MESURE (cycles RDTSC par compression, médiane) :",
        ]
        for nom_bloc, (ca, cp, sa, sp, rap) in resultats.items():
            lignes.append(f"  {nom_bloc} : avant {ca:.1f} — après "
                          f"{cp:.1f} — rapport {rap:.2f}× "
                          f"(horloge : {sa*1e9:.1f} ns → {sp*1e9:.1f} ns)")
        lignes += [
            "",
            f"LE RAPPORT DE CE SILICIUM (bloc aléa, cycles) : "
            f"{principal[4]:.2f}×",
            "",
            "LA PORTÉE : ce témoin consigne la mesure DE CETTE machine, "
            "CE jour, CE protocole — aucun chiffre n'est généralisé, "
            "aucun statut n'est fabriqué ; le run appartient au "
            "développeur qui l'exécute.",
            "",
            "signature du geste : à dater et à signer de la main du "
            "développeur.",
        ]
        with open(os.path.join(PREUVES, "temoin-shani.txt"), "w",
                  encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
        with open(os.path.join(PREUVES, "moteur-shani-execute.bin"),
                  "wb") as f:
            f.write(moteur)
        temoin(f"[témoin] {PREUVES} : temoin-shani.txt, "
               "scenario-shani-journal.log, VERDICT-run-shani.txt, "
               "moteur-shani-execute.bin")

        # ---- T5 LA CLÔTURE ------------------------------------------------
        journal("T5 — la clôture : la pièce relue, l'arène rendue")
        image_relue = arene.lire(0x2000, len(image))
        sha_relu = sha256_octets(image_relue)
        verifie("T5.pièce : l'image relue APRÈS le run, INTACTE",
                sha_relu == SHA_IMAGE,
                f"sha256 {sha_relu[:16]}… — la pièce ne fut que lue et "
                "exécutée")
        blob_relu = arene.lire(0x1000, len(moteur))
        verifie("T5.moteur : le blob relu APRÈS le run, INTACT",
                sha256_octets(blob_relu) == SHA_MOTEUR)
        arene.liberer()
        temoin("[clôture] l'arène libérée — les fichiers du kit jamais "
               "écrits")

        _ecrire_verdict()
        return 0 if not _echecs else 1
    finally:
        try:
            arene.liberer()
        except Exception:
            pass


def _ecrire_verdict():
    critere = ("LA MESURE AVANT/APRÈS SHA-NI : les pièces scellées "
               "recoupées, les trois lecteurs exacts, l'adversaire K "
               "tranché, la mesure consignée, la pièce relue intacte")
    lignes = []
    if not _echecs:
        lignes.append("VERDICT : VERT — " + critere)
        lignes.append("le témoin est à renvoyer ENTIERS au coffre "
                      "/test (dossier Drive « Triade » → « test »)")
    else:
        lignes.append("VERDICT : ÉCHEC NOMMÉ — " + critere)
        lignes.append("les gestes en échec :")
        lignes.extend("  — " + e for e in _echecs)
        lignes.append("un verdict d'échec se renvoie TEL QUEL : la "
                      "ligne nomme le défaut")
    try:
        os.makedirs(PREUVES, exist_ok=True)
        with open(os.path.join(PREUVES, "VERDICT-run-shani.txt"), "w",
                  encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
        print()
        for ligne in lignes:
            print(ligne)
    except OSError:
        pass


if __name__ == "__main__":
    sys.exit(main())
