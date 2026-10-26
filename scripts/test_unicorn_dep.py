#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test D39 (v2, pile corrigée) : fidélité DEP d'Unicorn.

Questions :
  Q1 : fetch depuis page RW (sans exec) → faute ?            [UC_ERR_FETCH_PROT]
  Q2 : écriture PAR LE CODE ÉMULÉ dans page RW-sans-exec → OK ?
  Q3 : re-protection RWX + remove_cache → l'exec revient ?
  Q4 : scénario tcp-07 EXACT : shim hooké (fausse adresse d'IAT) re-protège
       la page du code EN COURS en RW, retour au code, fetch suivant → faute ?
       a) avec ctl_remove_cache  b) sans ctl_remove_cache
  Q5 : après la faute Q4a, re-protection RWX par LE SHIM (mode restore) :
       l'exécution peut-elle repartir (uc.emu_start rejoué) ?
"""

from unicorn import *
from unicorn.x86_const import *
import struct

PROT_RW = UC_PROT_READ | UC_PROT_WRITE
PROT_RX = UC_PROT_READ | UC_PROT_EXEC
PROT_RWX = UC_PROT_ALL

# code : mov eax, 0x33 ; mov ebx, 0x44 ; mov eax, 0x55 ; (ret)
CODE = bytes.fromhex("b833000000" + "bb44000000" + "b855000000" + "c3")
FIN = 0x20000 + len(CODE)


def setup():
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(0x20000, 0x1000, PROT_RWX)
    uc.mem_write(0x20000, CODE)
    uc.mem_map(0x80000, 0x2000, PROT_RWX)
    uc.reg_write(UC_X86_REG_RSP, 0x81000)
    # adresse de retour valide : une page « épilogue » mappée (ret y atterrit)
    uc.mem_map(0x90000, 0x1000, PROT_RWX)
    uc.mem_write(0x81000, struct.pack("<Q", 0x90000))
    return uc


def essai(nom, fn):
    print(f"— {nom}")
    try:
        fn()
    except Exception as e:
        print(f"  !! exception test : {e!r}")


# ---- Q1
def q1():
    uc = setup()
    uc.mem_protect(0x20000, 0x1000, PROT_RW)
    try:
        uc.emu_start(0x20000, 0x90000, count=1)
        print("  OK — PAS de faute (unicorn n'applique pas exec)")
    except UcError as e:
        print(f"  FAUTE {e.errno} : {e}  ← attendu (FETCH_PROT)")


essai("Q1 : fetch depuis page RW", q1)


# ---- Q2
def q2():
    uc = setup()
    uc.mem_protect(0x20000, 0x1000, PROT_RW)     # page de code en RW
    # code alternatif à 0x21000 (page 0x20000 — même page ! non exec…) →
    # il faut un code exécutable AILLEURS écrivant dans la page RW.
    uc.mem_map(0x30000, 0x1000, PROT_RWX)
    # mov rax, 0x20080 ; mov qword ptr [rax], 0x5A ; mov eax, 7 ; ret
    code = bytes.fromhex("48b88000020000000000" + "48c7005a000000" + "b807000000" + "c3")
    uc.mem_write(0x30000, code)
    uc.mem_write(0x81000, struct.pack("<Q", 0x90000))
    try:
        uc.emu_start(0x30000, 0x90000)
        print(f"  OK — eax={uc.reg_read(UC_X86_REG_EAX)} ; mot=@0x20080 : "
              f"{struct.unpack('<Q', uc.mem_read(0x20080, 8))[0]:#x} "
              f"← le code émulé écrit dans une page RW-sans-exec : OK attendu")
    except UcError as e:
        print(f"  FAUTE {e.errno} : {e}  ← PROBLÈME (l'écriture doit être permise)")


essai("Q2 : code émulé écrit dans page RW", q2)


# ---- Q3
def q3():
    uc = setup()
    uc.mem_protect(0x20000, 0x1000, PROT_RW)
    uc.mem_protect(0x20000, 0x1000, PROT_RWX)
    uc.ctl_remove_cache(0x20000, 0x21000)
    try:
        uc.emu_start(0x20000, 0x90000)
        print(f"  OK — eax={uc.reg_read(UC_X86_REG_EAX):#x}  ← exec revenue après RWX (attendu 0x55)")
    except UcError as e:
        print(f"  FAUTE {e.errno} : {e}  ← PROBLÈME")


essai("Q3 : re-protection RWX → exec revient", q3)


# ---- Q4 : scénario tcp-07 EXACT
def q4(remove_cache: bool):
    uc = setup()
    # IAT factice : call [0x2F000] → saute à FAKE_VP (hook code)
    uc.mem_map(0x2F000, 0x1000, PROT_RWX)
    FAKE_VP = 0x2F800
    uc.mem_write(0x2F000, struct.pack("<Q", FAKE_VP))
    # code appelant dans SA page (0x20000) :
    #   mov eax, 0x11
    #   call qword ptr [0x2F000]      ← le « VirtualProtect » du shim
    #   mov eax, 0x22                 ← FETCH ICI après retour : page devenue RW ?
    #   ret
    code = bytes.fromhex("b811000000"
                         + "ff25" + struct.pack("<I", 0x2F000 - (0x20000 + 9 + 6)).hex()
                         + "b822000000" + "c3")
    uc.mem_write(0x20000, code)
    fin = 0x20000 + len(code)
    uc.mem_write(0x81000, struct.pack("<Q", 0x90000))
    etat = {"protect_fait": False}

    def hook_vp(uc_, addr, size, _):
        if addr != FAKE_VP or etat["protect_fait"]:
            return
        etat["protect_fait"] = True
        print(f"  [shim] VirtualProtect détecté — re-protection de la page 0x20000 en RW"
              f"{' + remove_cache' if remove_cache else ''}")
        uc_.mem_protect(0x20000, 0x1000, PROT_RW)
        if remove_cache:
            uc_.ctl_remove_cache(0x20000, 0x21000)
        # retour de fonction : pop l'adresse de retour et saute
        rsp = uc_.reg_read(UC_X86_REG_RSP)
        ret = struct.unpack("<Q", uc_.mem_read(rsp, 8))[0]
        uc_.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc_.reg_write(UC_X86_REG_RIP, ret)

    uc.hook_add(UC_HOOK_CODE, hook_vp, begin=FAKE_VP, end=FAKE_VP)
    try:
        uc.emu_start(0x20000, fin)
        print(f"  OK sans faute — eax={uc.reg_read(UC_X86_REG_EAX):#x}"
              + ("  ← FAUX VERT : le fetch a continué depuis une page RW (TCG non invalidé)"
                 if not remove_cache else "  ← INATTENDU (remove_cache sans effet)"))
    except UcError as e:
        print(f"  FAUTE {e.errno} : {e}  ← comportement DEP réel : le fetch"
              f" post-retour faute depuis la page RW ✓")


essai("Q4a : shim re-protège la page du code (AVEC remove_cache)", lambda: q4(True))
essai("Q4b : shim re-protège la page du code (SANS remove_cache)", lambda: q4(False))


# ---- Q5 : après faute, le restore RWX permet-il de rejouer ?
def q5():
    uc = setup()
    uc.mem_protect(0x20000, 0x1000, PROT_RW)
    try:
        uc.emu_start(0x20000, 0x90000, count=1)
        print("  pas de faute ?!")
        return
    except UcError as e:
        print(f"  1re exécution : faute {e.errno} (attendu)")
    uc.mem_protect(0x20000, 0x1000, PROT_RWX)
    uc.ctl_remove_cache(0x20000, 0x21000)
    try:
        uc.emu_start(0x20000, 0x90000)
        print(f"  reprise après restore RWX : OK — eax={uc.reg_read(UC_X86_REG_EAX):#x} (attendu 0x55)")
    except UcError as e:
        print(f"  reprise : faute {e.errno} : {e}  ← PROBLÈME pour l'oracle")


essai("Q5 : faute puis restore → reprise", q5)
