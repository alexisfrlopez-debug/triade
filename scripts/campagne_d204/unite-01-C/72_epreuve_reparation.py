#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LES ÉPREUVES DE LA RÉPARATION v2 (D122, au POSIX — le labo n'a
aucun Windows) :
  E1. LA TRAVERSÉE DU SCÉNARIO v2 EXÉCUTÉE cette fois : le texte MÊME du
      scénario livré (les quatre lecteurs + la boucle gardée, extraits
      VERBATIM du fichier du kit) couru contre l'image réelle de la pièce
      mappée par sections — elle doit s'arrêter AU descripteur NUL (2
      descripteurs réels : KERNEL32.dll, msvcrt.dll), résoudre les CINQ
      feuilles, ne RIEN lire hors image ;
  E2. LE CONTRAT ENTIER REJOUÉ : le harnais POSIX (epreuve_posix.c, la pièce
      source incluse TELLE QUELLE + les shims) contre le juge hashlib —
      17 VERT attendus, 0 ROUGE."""
import ctypes
import hashlib
import pathlib
import shutil
import struct
import subprocess
import sys
import textwrap

KIT_V1 = pathlib.Path("/home/z/my-project/download/nouveau-run/"
                      "kit-unite-loupe-01-C-20261114")
V2 = pathlib.Path("/home/z/my-project/work/kit_v2/scenario-unite01C.py")
ATELIER = pathlib.Path("/home/z/my-project/work/triade/scripts/"
                       "campagne_d204/unite-01-C")
GRATTAGE = pathlib.Path("/home/z/my-project/work/epreuve-C-v2")

# ============ E1 : LA TRAVERSÉE DU SCÉNARIO v2, EXÉCUTÉE ======================
src = V2.read_text(encoding="utf-8")
assert hashlib.sha256(V2.read_bytes()).hexdigest().startswith("6340cd3c6308c3ae")

# les quatre lecteurs, VERBATIM (du fichier livré)
debut_lecteurs = src.index("def lire_octets(base: int, rva: int, n: int) -> bytes:")
fin_lecteurs = src.index("def main() -> int:")
lecteurs = src[debut_lecteurs:fin_lecteurs].rstrip() + "\n"

# la boucle gardée, VERBATIM : de slots={} à manquantes (exclu)
debut_boucle = src.index("    slots = {}")
fin_boucle = src.index("    manquantes = [f for f in FEUILLES_KIT if f not in slots]")
boucle = src[debut_boucle:fin_boucle].rstrip()

# l'image de la pièce mappée par sections (comme le chargeur la cartographie)
dll = (KIT_V1 / "loupe-01-c.dll").read_bytes()
assert hashlib.sha256(dll).hexdigest().startswith("85b34ed4c243e977")
e = struct.unpack_from("<I", dll, 0x3C)[0]
opt = e + 24
taille_image = struct.unpack_from("<I", dll, opt + 56)[0]
taille_headers = struct.unpack_from("<I", dll, opt + 60)[0]
nb_sec = struct.unpack_from("<H", dll, e + 6)[0]
tail_opt = struct.unpack_from("<H", dll, e + 20)[0]
image = bytearray(taille_image)
image[:taille_headers] = dll[:taille_headers]
for i in range(nb_sec):
    s = e + 24 + tail_opt + 40 * i
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", dll, s + 8)
    fin = min(rsize, max(vsize, rsize))
    image[vaddr:vaddr + fin] = dll[raddr:raddr + fin]
buf = ctypes.create_string_buffer(bytes(image), taille_image)
base = ctypes.addressof(buf)
rva_exports = struct.unpack_from("<I", dll, opt + 112)[0]
rva_imports = struct.unpack_from("<I", dll, opt + 120)[0]
print(f"[E1] l'image mappée : {taille_image:#x} o à base {base:#x} ; "
      f"export @+{rva_exports:#x}, import @+{rva_imports:#x}")

# la chambre : les lecteurs du scénario + la boucle du scénario, TELS QUELS
messages = []
chambre = lecteurs + "\n\n"
chambre += "def la_traversee(base, rva_imports, opt, consigne, FEUILLES_KIT):\n"
chambre += textwrap.indent(textwrap.dedent(boucle), "    ") + "\n"
chambre += "    return desc, dict(slots)\n"
ns = {"ctypes": ctypes, "struct": struct,
      "consigne": lambda l: messages.append(l),
      "FEUILLES_KIT": ("CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
                       "ReadFile", "CloseHandle", "GetLastError")}
exec(compile(chambre, "<le scénario v2, extrait verbatim>", "exec"), ns)
desc_final, slots = ns["la_traversee"](base, rva_imports, opt,
                                       ns["consigne"], ns["FEUILLES_KIT"])

print(f"[E1] la boucle s'est arrêtée à desc @+{desc_final:#x} "
      f"(le terminateur vit @+{rva_imports + 40:#x})")
print(f"[E1] les feuilles résolues : {sorted(slots)}")
print(f"[E1] les REFUS consignés par les gardes : {messages or 'AUCUN'}")
ok_stop = desc_final == rva_imports + 40
ok_slots = set(slots) == {"CreateFileW", "GetFileSizeEx", "ReadFile",
                          "CloseHandle", "GetLastError"}
ok_gardes = not messages
print(f"[{'VERT' if ok_stop else 'ROUGE'}] E1a : arrêt AU descripteur NUL "
      f"(2 descripteurs réels traversés, jamais au-delà)")
print(f"[{'VERT' if ok_slots else 'ROUGE'}] E1b : les CINQ feuilles kernel32 "
      f"aux slots réels (SetFilePointerEx : l'écart nommé du bras C)")
print(f"[{'VERT' if ok_gardes else 'ROUGE'}] E1c : aucune garde n'a vécu "
      f"(aucun REFUS — la table est saine)")

# ============ E2 : LE CONTRAT ENTIER REJOUÉ ===================================
if GRATTAGE.exists():
    shutil.rmtree(GRATTAGE)
GRATTAGE.mkdir(parents=True)
for piece in ["epreuve_posix.c", "windows.h", "compare_epreuve.py"]:
    shutil.copy2(ATELIER / "epreuves" / piece, GRATTAGE / piece)
for piece in ["loupe-01-c.c", "temoin-1.bin", "temoin-384.bin",
              "temoin-3f.bin", "vide.bin"]:
    shutil.copy2(KIT_V1 / piece, GRATTAGE / piece)
sha_source = hashlib.sha256((KIT_V1 / "loupe-01-c.c").read_bytes()).hexdigest()
assert sha_source.startswith("860ff1cfcf78d5fc"), "le source C a divergé"
print(f"\n[E2] le grattage : {GRATTAGE} — le source C {sha_source[:16]}… "
      f"(INTACT, octet pour octet la livraison)")

r = subprocess.run(["gcc", "-O2", "-I.", "-o", "epreuve", "epreuve_posix.c"],
                   cwd=GRATTAGE, capture_output=True, text=True)
if r.returncode != 0:
    print("[E2] la compilation a refusé :\n" + r.stderr[:1500])
    sys.exit(1)
print("[E2] compilation gcc -O2 VERT")

with (GRATTAGE / "observe.txt").open("w", encoding="utf-8") as f:
    r = subprocess.run(["./epreuve"], cwd=GRATTAGE, stdout=f,
                       stderr=subprocess.STDOUT, timeout=300)
print(f"[E2] le harnais a couru (code {r.returncode})")

r = subprocess.run(["python3", "compare_epreuve.py"], cwd=GRATTAGE,
                   capture_output=True, text=True)
print(r.stdout.rstrip())
if r.returncode != 0:
    print(r.stderr[:800])
    sys.exit(1)

bilan = (ok_stop and ok_slots and ok_gardes and r.returncode == 0)
print("\n" + ("LES ÉPREUVES DE LA RÉPARATION SONT VERTES — la traversée du "
              "scénario v2 s'arrête au terminateur, le contrat entier demeure"
              if bilan else "UN RECOUP A ROUGI"))
sys.exit(0 if bilan else 1)
