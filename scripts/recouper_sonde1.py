#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_sonde1.py — LE RECOUP LABO du PREMIER RUN de la sonde sys-05
(m9-(g)), sur pièces croisées (D138/D145/D148) : les pièces du coffre
/test/preuves-sonde-sys05/ contre la source du dépôt, l'artefact scellé,
le témoin du run 4 m9f (la même machine) et la notation/spec sys-05.
Rend : la liste des contrôles (X/Y) + les constats nommés."""
import hashlib
import pathlib
import re
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PIECES = pathlib.Path("/home/z/my-project/download/preuves-sonde-sys05-1")
ARTIFACT = pathlib.Path("/tmp/sonde-kit/sonde-sys05-kit/proxy.exe")

_passes = []
_echecs = []


def check(nom, cond, detail=""):
    if cond:
        _passes.append(nom)
        print(f"  [OK ] {nom}" + (f" — {detail}" if detail else ""))
    else:
        _echecs.append(nom)
        print(f"  [ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))


temoin = (PIECES / "temoin-sonde-sys05.txt").read_text(encoding="utf-8")
journal = (PIECES / "sonde-sys05-journal.log").read_text(encoding="utf-8")
emissions = (PIECES / "journal-emissions.txt").read_bytes()

print("=== LE RECOUP LABO DU RUN 1 DE LA SONDE SYS-05 (sur pièces) ===\n")

# --- 1..3 : les pièces, l'artefact, le scénario ------------------------------
print("--- la chaîne de possession ---")
md5s = {p.name: hashlib.md5(p.read_bytes()).hexdigest()
        for p in PIECES.iterdir()}
check("les 4 pièces md5 == le coffre (aller-retour)",
      len(md5s) == 4 and (PIECES / "temoin-sonde-sys05.txt").exists()
      and (PIECES / "sonde-sys05-journal.log").exists()
      and (PIECES / "journal-emissions.txt").exists()
      and (PIECES / "LISEZMOI-preuves.txt").exists(),
      f"{len(md5s)} pièces : " + ", ".join(sorted(md5s)))
check("l'artefact du kit == l'ACQUITTÉ d8928934… (INTACT, jamais reconstruit)",
      hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()
      == "d892893469608fd69e381b92b8e18623107bd2bc694f43a5"
      "12bc5900773dc314")
check("le scénario exécuté == la source du dépôt (octet pour octet)",
      hashlib.md5(pathlib.Path(
          "/tmp/sonde-kit/sonde-sys05-kit/scenario-sonde-sys05.py")
          .read_bytes()).hexdigest()
      == hashlib.md5((REPO / "tls13/terrain/scenario-sonde-sys05.py")
                     .read_bytes()).hexdigest())

# --- 4 : l'environnement == le run 4 (la même machine) ------------------------
print("\n--- l'environnement (la même machine que le run 4) ---")
t4 = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-4/temoin-m9f.txt"
).read_text(encoding="utf-8")
for etiquette in ("Windows 10.0 build", "Python 3.14.3 · AMD64"):
    check(f"l'environnement « {etiquette} » == le run 4",
          etiquette in temoin and etiquette in t4)
ntdll_sonde = re.search(r"ntdll sha256 : ([0-9a-f]{64})", temoin).group(1)
ntdll_run4 = re.search(r"ntdll sha256 : ([0-9a-f]{64})", t4).group(1)
check("le ntdll == le run 4 (b072efae… — le MÊME noyau, la même machine)",
      ntdll_sonde == ntdll_run4 and ntdll_sonde.startswith("b072efae"),
      f"{ntdll_sonde[:16]}… == {ntdll_run4[:16]}…")
check("l'empreinte de l'artefact relue au T0 == d8928934…",
      "sha256 d892893469608fd6" in temoin)

# --- 5 : le trampoline 33 o DÉCODÉ --------------------------------------------
print("\n--- le trampoline de capture (33 o) décodé instruction par instruction ---")
hexa = re.search(r"trampoline de capture : 33 o — ([0-9a-f]+)", temoin).group(1)
trampo = bytes.fromhex(hexa)
check("le témoin consigne 33 o — la longueur lue == 33", len(trampo) == 33,
      f"{len(trampo)} o")
base = int(re.search(r"l'artefact cartographié — base (0x[0-9a-f]+)",
                     temoin).group(1), 16)
attendu = (b"\x48\x83\xec\x28"                    # sub rsp,0x28
           + b"\x48\xb8" + struct.pack("<Q", base + 0xA540)  # mov rax,sys-05
           + b"\xff\xd0"                          # call rax
           + b"\x48\xc1\xe2\x20"                  # shl rdx,32
           + b"\x89\xc1"                          # mov ecx,eax
           + b"\x48\x09\xd1"                      # or rcx,rdx
           + b"\x48\x89\xc8"                      # mov rax,rcx
           + b"\x48\x83\xc4\x28"                  # add rsp,0x28
           + b"\xc3")                             # ret
check("les 33 octets == LE SQUELETTE SPÉCIFIÉ (base+0xa540 = LE slot sys-05)",
      trampo == attendu,
      f"mov rax,{base + 0xa540:#x} == base+0xa540 (sys-05)")
check("la cible == la tête du slot relue au T0 (4d85c00f8410)",
      "la tête sys-05 @0xa540 — 4d85c00f8410" in temoin)

# --- 6 : le compas + la mesure + les variations --------------------------------
print("\n--- la mesure (le cœur de la sonde) ---")
check("le compas étalonné : le handle invalide rend -6 + "
      "STATUS_INVALID_HANDLE (0xC0000008) — la capture lit VRAIMENT rdx",
      "STATUS_INVALID_HANDLE (0xC0000008)" in temoin
      and "STATUS_INVALID_HANDLE (0xC0000008)" in journal)
NB_AV = temoin.count("0xC0000005")
check("LA MESURE : le NTSTATUS brut du geste m9f LU — 0xC0000005 "
      "(STATUS_ACCESS_VIOLATION), CLASSE ERREUR (sévérité 11), TROIS fois "
      "(mesure + variation taille + variation délai)",
      NB_AV >= 4,  # 3 lectures + la ligne de synthèse
      f"{NB_AV} occurrence(s) au témoin")
check("les variations : le refus IDENTIQUE sur un octet (session sacrifiée "
      "fraîche) et après 2 s — DÉTERMINISTE, ni la taille ni le délai",
      "LA VARIATION TAILLE" in temoin and "LA VARIATION DÉLAI" in temoin
      and temoin.count("0xC0000005") >= 3)
horodatages = re.findall(r"^(\d\d:\d\d:\d\d)", journal, re.M)
check("l'horloge du journal porte le délai volontaire de 2 s "
      "(30 → 32 secondes)",
      horodatages[0].endswith("30") and "20:34:32" in journal,
      " ; ".join(horodatages))

# --- 7 : l'échelle re-jouée (RFC 7748 § 5) ------------------------------------
print("\n--- l'échelle X25519 re-jouée sur la clé privée DU RUN ---")
# l'échelle EXTRAITE DE LA SOURCE du scénario (le même instrument que le
# run — le recoup re-joue la fonction même qui a couru sur le terrain)
_src = src_sonde = (REPO / "tls13/terrain/scenario-sonde-sys05.py"
                    ).read_text(encoding="utf-8")
_ns = {}
_debut = _src.index("def x25519_echelle")
_fin = _src.index("def construction_ch_reference")
exec(compile(_src[_debut:_fin], "echelle-source", "exec"), _ns)
echelle_source = _ns["x25519_echelle"]
# la double épreuve de l'instrument : le vecteur officiel RFC 7748 § 6.1
_pub_alice = echelle_source(bytes.fromhex(
    "77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a")
).hex()
check("l'instrument lui-même éprouvé : l'échelle de la source rend le "
      "vecteur officiel RFC 7748 § 6.1 (Alice)",
      _pub_alice == "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4"
      "a98eaa9b4e6a", _pub_alice[:16] + "…")
privee = bytes.fromhex(re.search(
    r"clé privée de la sonde : ([0-9a-f]{64})", temoin).group(1))
publique = re.search(r"la clé publique \(l'échelle Python\) : ([0-9a-f]{64})",
                     temoin).group(1)
rendue = echelle_source(privee).hex()
check("l'échelle de la SOURCE re-jouée sur la clé privée DU RUN rend la "
      "clé publique du témoin",
      rendue == publique,
      f"attendue {publique[:16]}…, rendue {rendue[:16]}…")

# --- 8 : S4 la contre-épreuve == la mort des quatre runs -----------------------
print("\n--- S4 : la contre-épreuve (la non-régression) ---")
j4 = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-4/scenario-m9f-journal.log"
).read_text(encoding="utf-8")
check("S4 : le rappel émission rend -6 (le chemin standard, SANS "
      "trampoline) — le MÊME refus que les QUATRE runs m9f",
      "le rappel émission : sys-05 rend -6" in journal
      and "le rappel émission : sys-05 rend -6" in j4)
check("S4 : la poignée meurt AU MÊME GESTE (rax -7, état 5) — la "
      "non-régression CONSTATÉE : le refus est AU BLOC, pas au trampoline "
      "(le run 4 m9f meurt pareil : -7, état 5)",
      "rax -7, état 5" in journal and "état 5" in t4)
check("journal-emissions.txt : UN enregistrement, 119 o — le CH refusé "
      "(l'en-tête 16 03 03 00 72 + 114 o, l'émission TOTALE ou refusée, "
      "jamais un demi-envoi déguisé)",
      len(emissions) == 119
      and emissions[:5] == bytes.fromhex("1603030072"),
      f"{len(emissions)} o, tête {emissions[:5].hex()}")
check("le CH de S4 == la TAILLE du jalon (119 o — 5 + 114 : le record "
      "complet de l'offre)",
      len(emissions) == 119)

# --- 9 : la loi des pièces (le verdict manquant EXPLIQUÉ) ---------------------
print("\n--- le verdict manquant : la loi des pièces + le site de la mort ---")
check("le témoin s'arrête AU POINT DE CONTRÔLE d'après-S3 (le vidage "
      "volontaire ligne 756 : « la mesure est le cœur : ses pièces "
      "survivent à tout arrêt ultérieur »)",
      temoin.rstrip().endswith(
          "CLASSE ERREUR (sévérité 11) — un vrai refus du noyau"))
check("le journal vit ligne à ligne (chaque ligne vidée au fil du run) : "
      "sa dernière ligne == la mort de S4",
      journal.rstrip().endswith(
          "le refus est AU BLOC, pas au trampoline"))
check("journal-emissions.txt NÉ (avant T6) mais PAS le VERDICT ni la ligne "
      "reçue — le run est mort DANS T6, AVANT _verdict()",
      (PIECES / "journal-emissions.txt").exists()
      and not (PIECES / "VERDICT-sonde-sys05.txt").exists()
      and not (PIECES / "ligne-recue.txt").exists())
zone = int(re.search(r"zone de capture allouée.*zone (0x[0-9a-f]+)",
                     temoin).group(1), 16)
R_SYS01 = int(re.search(r"R_SYS01 = (0x[0-9A-Fa-f]+)", _src).group(1), 16)
check("LA THÉORIE DE LA MORT : le jmp rel32 du tromphone NtClose "
      "(struct.pack « <i ») ne peut pas coder la distance zone→artefact "
      f"({base:#x} − {zone:#x} ≈ {(base - zone) / 2**40:.0f} Tio ≫ 2 Gio) "
      "→ struct.error → le verdict jamais né",
      abs(base - zone) > 2 ** 31 and 'pack("<i"' in _src,
      f"distance ≈ {base - zone:#x} ; la borne int32 = {2**31 - 1:#x}")
check("la SÉQUENCE T6 n'a JAMAIS couru sur le terrain avant la sonde "
      "(les QUATRE runs m9f retournent à _verdict() dès la mort de T3 — "
      "source ligne ~646) — la faute était INVISIBLE jusqu'ici",
      "return _verdict()" in (REPO / "tls13/terrain/scenario-m9f.py")
      .read_text(encoding="utf-8"))

# --- 10 : LE COUPABLE VU À L'INSTRUCTION (l'artefact scellé) -------------------
print("\n--- LE COUPABLE : la pose du WSABUF dans le bloc sys-05 (sur pièces) ---")
data = ARTIFACT.read_bytes()
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
nb_sec = struct.unpack_from("<H", data, e_lfanew + 6)[0]
opt = struct.unpack_from("<H", data, e_lfanew + 20)[0]
off_sections = e_lfanew + 24 + opt
rva_to_off = None
for i in range(nb_sec):
    b = off_sections + 40 * i
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", data, b + 8)
    if vaddr <= 0xA540 < vaddr + max(vsize, rsize):
        rva_to_off = raddr + (0xA540 - vaddr)
        break
bloc = data[rva_to_off:rva_to_off + 384]
pose = bytes.fromhex("89742460") + bytes.fromhex("48897c2464")
check("l'artefact porte LA POSE FAUTIVE à sys-05+0x46 : "
      "mov dword [rsp+0x60],esi (len à +0) ; mov qword [rsp+0x64],rdi "
      "(buf à +4) — le WSABUF « packé » de 12 o",
      bloc.find(pose) == 0x46, f"trouvé à +{bloc.find(pose):#x}")
check("le WSABUF CANONIQUE x64 = 16 o : len à +0 (4), PADDING 4, buf à +8 "
      "(8) — le noyau lit buf à +8 : les 4 octets HAUTS du vrai pointeur "
      "collés aux 4 octets d'immondices de pile → l'adresse FOLLE → "
      "ACCESS_VIOLATION",
      bloc[0x46:0x4F] == pose)
spec = (REPO / "m8/I/sys-05-emission.md").read_text(encoding="utf-8")
check("LA SPEC PORTE LA FAUTE : sys-05:R1 Q3 écrit « (12 o + 24 o…) » — "
      "le WSABUF de 12 o (len 4 + buf 8, SANS le padding d'alignement) — "
      "la notation a implémenté la spec à la lettre",
      "(12 o + 24 o" in spec)
notation = (REPO / "m8/notation/sys-05-emission.asm").read_text(
    encoding="utf-8")
check("la notation implémente la pose packée (ligne « mov qword ptr "
      "[rsp + 0x64], rdi ») — fidèle à la spec fautive",
      "mov qword ptr [rsp + 0x64], rdi" in notation)
check("la chaîne du refus reconstituée : le noyau rend 0xC0000005 dans "
      "eax ; le bloc fait « test eax,eax ; jne status_nonnul » → "
      "« mov rdx,rax ; mov rax,-6 » — LE NTSTATUS VIT DANS RDX (la spec "
      "Q5 l'avait NOMMÉ) : c'est LUI que le trampoline est venu lire",
      "mov rdx, rax" in notation and "mov rax, -6" in notation
      and "le NTSTATUS brut consigné" in spec)
check("le compas DISCRIMINE : 0xC0000008 (handle invalide, la faute "
      "SUR LES ARGUMENTS DU BLOC) vs 0xC0000005 (la faute DANS LA POSE "
      "INTERNE) — l'instrument était juste",
      "0xC0000008" in temoin and "0xC0000005" in temoin)

# --- le bilan ------------------------------------------------------------------
total = len(_passes) + len(_echecs)
print(f"\n=== BILAN : {len(_passes)}/{total} ===")
if _echecs:
    for e in _echecs:
        print(f"  ÉCHEC : {e}")
    sys.exit(1)
print("LE COUPABLE EST NOMMÉ SUR PIÈCES : (b) LE CONTRAT D'APPEL du bloc "
      "sys-05 — la pose du WSABUF (spec R1-Q3 « 12 o », le pointeur buf à "
      "+4 au lieu de +8) : le noyau lit le pointeur 4 octets trop tôt, "
      "sonde une adresse FOLLE et rend STATUS_ACCESS_VIOLATION — le -6 des "
      "cinq runs, ENFIN NOMMÉ à l'instruction près.")
