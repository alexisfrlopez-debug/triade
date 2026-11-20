#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""garde_ram_demo.py — LE DÉMONSTRATEUR DE LABORATOIRE du bloc natif scellé
« GARDE RAM » (l'atelier coffre-vr9n3s3l7, plan (e)).

NOMMÉ DÉMONSTRATEUR : ceci N'EST PAS le bloc natif scellé (la spec
I-garde-ram.md — notation x86-64, IAT win11/syscalls linux en miroir,
vérification par émulation Unicorn, scellage en copie de labo — vit AU
GESTE DU MAÎTRE, le gap est NOMMÉ au rapport). Le démonstrateur met en
œuvre LES TROIS GESTES DU CONTRAT en Python/ctypes sur l'OS du laboratoire
(Linux) :

  1. LA PAGE VERROUILLÉE : mlock(2) sur le tampon secret (le miroir
     Windows : VirtualLock — spécifié au contrat, nommé) ; REFUS NOMMÉ si
     l'OS refuse (fail-closed : le secret ne vit JAMAIS dans une page non
     verrouillée) ;
  2. LA DESTRUCTION : explicit_bzero(3) (glibc ≥ 2.25 — le miroir Windows
     SecureZeroMemory, spécifié) ; vérifiée OCTET PAR OCTET ; puis
     munlock(2) ;
  3. L'EXCLUSION DES DUMPS : prctl(PR_SET_DUMPABLE, 0) (le processus
     n'émet plus de core dump — vérifié par PR_GET_DUMPABLE) et
     madvise(MADV_DONTDUMP) sur la page (best-effort, nommé) ; le miroir
     Windows (l'exclusion WER de l'application — l'entrée IAT
     WerAddExcludedApplication) est SPÉCIFIÉ au contrat, pas exécuté ici.

AUCUN secret réel : le démonstrateur n'accepte que des octets de TEST
marqués D105.
"""
from __future__ import annotations

import ctypes
import ctypes.util
import os
import sys

try:
    libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
except OSError as exc:  # pragma: no cover
    raise SystemExit(f"[garde-ram] ÉCHEC — libc introuvable ({exc})")

PR_GET_DUMPABLE = 3
PR_SET_DUMPABLE = 4
MADV_DONTDUMP = 16          # Linux ≥ 3.4
PAGE = 4096


class RefusOS(RuntimeError):
    """Le REFUS NOMMÉ : l'OS refuse le geste — fail-closed (spec (e))."""


def _errno_msg(fonction: str) -> str:
    errno = ctypes.get_errno()
    return (f"{fonction} a échoué : errno {errno} ({os.strerror(errno)})")


class PageVerrouillee:
    """Une page allouée, VERROUILLÉE en RAM, détruite octet par octet à la
    sortie — le démonstrateur du contrat de la spec I-garde-ram."""

    def __init__(self, taille: int = PAGE):
        self.taille = taille
        self.buf = ctypes.create_string_buffer(taille)
        self.adresse = ctypes.addressof(self.buf)
        self.verrouillee = False

    def verrouiller(self) -> None:
        """GESTE 1 : mlock — REFUS NOMMÉ si l'OS refuse (le secret ne vit
        JAMAIS dans une page non verrouillée : l'appelant doit REFUSER de
        poursuivre, fail-closed)."""
        if libc.mlock(ctypes.c_void_p(self.adresse),
                      ctypes.c_size_t(self.taille)) != 0:
            raise RefusOS(_errno_msg("mlock")
                          + " — REFUS NOMMÉ : l'OS refuse de verrouiller la "
                          "page (rlimit MEMLOCK ?) ; le secret N'EST PAS "
                          "chargé (fail-closed, spec I-garde-ram Q1)")
        self.verrouillee = True
        # GESTE 3 (best-effort, nommé) : la page exclue des dumps
        if hasattr(libc, "madvise"):
            r = libc.madvise(ctypes.c_void_p(self.adresse),
                             ctypes.c_size_t(self.taille),
                             ctypes.c_int(MADV_DONTDUMP))
            self.madvise_dontdump = (r == 0)

    def ecrire_secret(self, secret: bytes) -> None:
        """Le secret de TEST (D105) entre dans la page verrouillée —
        tronqué à la taille de la page (le démonstrateur)."""
        if not self.verrouillee:
            raise RefusOS("la page n'est PAS verrouillée — REFUS : le "
                          "secret n'entre jamais dans une page non "
                          "verrouillée (l'ordre du contrat)")
        if len(secret) > self.taille:
            raise ValueError("secret plus long que la page (démonstrateur)")
        ctypes.memmove(self.buf, secret, len(secret))

    def lire(self) -> bytes:
        return ctypes.string_at(self.adresse, self.taille)

    def detruire(self) -> tuple[bool, str]:
        """GESTE 2 : explicit_bzero — la destruction SÛRE (pas d'élagage
        par le compilateur — l'appel libc externe est une barrière), puis
        VÉRIFICATION OCTET PAR OCTET (les 4096 octets == 0x00)."""
        if hasattr(libc, "explicit_bzero"):
            libc.explicit_bzero(ctypes.c_void_p(self.adresse),
                                ctypes.c_size_t(self.taille))
            moyen = "explicit_bzero(3)"
        else:
            # SUBSTITUTION NOMMÉE (glibc < 2.25) : memset via un pointeur
            # volatile — la barrière d'asm n'existe pas en Python, la
            # vérification octet par octet fait foi.
            libc.memset(ctypes.c_void_p(self.adresse), 0, self.taille)
            moyen = "memset(3) (SUBSTITUTION NOMMÉE : explicit_bzero absent)"
        reste = ctypes.string_at(self.adresse, self.taille)
        propre = reste == b"\x00" * self.taille
        if not propre:
            raise RefusOS("la destruction a LAISSÉ des octets — REFUS "
                          "NOMMÉ : la page n'est pas prouvée nulle")
        return propre, moyen

    def deverrouiller(self) -> None:
        """munlock — la page rendue à l'OS APRÈS la destruction (l'ordre du
        contrat : détruire, PUIS déverrouiller)."""
        if self.verrouillee:
            if libc.munlock(ctypes.c_void_p(self.adresse),
                            ctypes.c_size_t(self.taille)) != 0:
                raise RefusOS(_errno_msg("munlock")
                              + " — REFUS NOMMÉ : le déverrouillage échoue")
            self.verrouillee = False


def exclusion_des_dumps() -> int:
    """GESTE 3 : prctl(PR_SET_DUMPABLE, 0) — le processus ne peut plus être
    dumpé (core, ptrace d'un débogueur non-root) ; retourne la valeur
    PR_GET_DUMPABLE APRÈS le geste (0 attendu)."""
    avant = libc.prctl(PR_GET_DUMPABLE, 0, 0, 0, 0)
    if libc.prctl(PR_SET_DUMPABLE, 0, 0, 0, 0) != 0:
        raise RefusOS(_errno_msg("prctl(PR_SET_DUMPABLE, 0)")
                      + " — REFUS NOMMÉ : l'exclusion des dumps échoue "
                      "(spec I-garde-ram Q3)")
    apres = libc.prctl(PR_GET_DUMPABLE, 0, 0, 0, 0)
    return int(avant), int(apres)


def demonstration(secret_test: bytes = b"SECRET-DE-TEST-PUBLIQUE-D105"
                                  b"-garde-ram-labo") -> list[str]:
    """LE SCÉNARIO COMPLET DU DÉMONSTRATEUR — chaque geste nommé, chaque
    valeur consignée. Retourne les lignes du PV."""
    lignes = ["DÉMONSTRATEUR GARDE RAM (labo vr9n3s3l7, plan (e)) — "
              "DÉMONSTRATEUR Python/ctypes, PAS le bloc natif scellé",
              f"page : {PAGE} octets, libc : "
              f"{ctypes.util.find_library('c')}"]
    avant, apres = exclusion_des_dumps()
    lignes.append(f"GESTE 3 exclusions des dumps : prctl(PR_SET_DUMPABLE,0) "
                  f"— dumpable {avant} -> {apres} "
                  f"{'(VERT)' if apres == 0 else '(ROUGE)'}")
    page = PageVerrouillee()
    page.verrouiller()
    lignes.append(f"GESTE 1 page verrouillée : mlock({page.taille} o) VERT — "
                  f"madvise(MADV_DONTDUMP) : "
                  f"{'posé' if getattr(page, 'madvise_dontdump', False) else 'refusé (best-effort, nommé)'}")
    page.ecrire_secret(secret_test)
    lu = page.lire()[:len(secret_test)]
    lignes.append(f"le secret de TEST ({len(secret_test)} o, D105) est dans "
                  f"la page verrouillée : "
                  f"{'relu EXACT' if lu == secret_test else 'RELU FAUX !'}")
    propre, moyen = page.detruire()
    lignes.append(f"GESTE 2 destruction : {moyen} — {page.taille} octets "
                  f"vérifiés NULS octet par octet : "
                  f"{'VERT' if propre else 'ROUGE !'}")
    page.deverrouiller()
    lignes.append("munlock : VERT — la page rendue à l'OS APRÈS la "
                  "destruction (l'ordre du contrat)")
    lignes.append("MIROIRS WINDOWS SPÉCIFIÉS (non exécutés au labo — le "
                  "terrain au geste du maître) : VirtualLock/VirtualUnlock, "
                  "SecureZeroMemory, WerAddExcludedApplication (IAT win11)")
    return lignes


if __name__ == "__main__":
    for ligne in demonstration():
        print("[garde-ram]", ligne)
