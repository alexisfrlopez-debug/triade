#!/usr/bin/env python3
"""debug_s6.py — Reproduit S6 (suite_conn phase 2) et trace l'entrée echo."""
import sys

sys.path.insert(0, "/home/z/my-project/triade/m2")
import layout as L
import oracle_m2 as O
import build_m2 as B

blocs, specs, code, verrous = B.assembler_tout(2)
texte, rdata, data, text2, staging = B.composer_sections(code, blocs, 2)
exe = B.ecrire_pe32plus(texte, rdata, data, text2)

def entree(em, n=16):
    return bytes(em.uc.mem_read(O.IMAGE + L.ECHO_ENTREE, n)).hex()

em = O.Emulateur(exe)
em.installer_shims()

# S5 tel quel
em.reinitialiser_donnees()
em.poser_etat()
em.file_recv += [b"avant le patch\n", ("stop", b"apres le patch\n"), 0]
em.appeler(0x4800, (O.FAKE_SOCK,))
print("S5 arrêt orchestré, attente =", em.attente is not None)
print("  entrée après stop   :", entree(em))
instantane = em.instantane()
em.appeler(0x4400, (0,), pile=O.ALT_SOMMET)
print("  entrée après patch  :", entree(em))
em.restaurer(instantane)
em.reprendre()
print("  entrée après reprise:", entree(em), "envois:", em.envois)

# S6 : réinit puis premier écho
em.reinitialiser_donnees()
em.poser_etat()
print("S6 après réinit      :", entree(em))
print("  .data ETAT_PATCH   :", em.lire_qword(L.R_ETAT_PATCH))
em.file_recv += [b"un\n", ("stop", b"deux\n"), ("stop", b"trois\n"), 0]
em.appeler(0x4800, (O.FAKE_SOCK,))
print("S6 premier écho      :", em.envois, "attendu [b'un\\n']")
print("  entrée à l'arrêt    :", entree(em))
