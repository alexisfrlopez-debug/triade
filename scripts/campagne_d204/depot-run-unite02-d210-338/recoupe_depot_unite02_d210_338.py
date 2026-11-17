#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recoupe_depot_unite02_d210_338.py — LE RECOUP DU DÉPÔT preuves-unite02/
reçu au coffre /test (l'annonce du développeur : « preuves deposees dans
le drive /test » — le run terrain de l'unité 02 D210 au kit GUI 1-clic
livré à la 337). Chaque contrôle est calculé depuis les pièces — aucun
chiffre recopié ; un écart nommé est un RÉSULTAT, jamais un échec à
maquiller (D189).

LES CONTRÔLES :
  R1  les pièces : TROIS rapatriées au bac, chacune re-téléchargée DEUX
      FOIS byte-byte au rapatriement, md5 == la métadonnée Drive
      (re-recoupé ici par re-listing du dépôt, où qu'il vive) ;
  R2  LE JUGE LIVRÉ : le scenario-unite02.py du kit == le juge v1 de
      D204 OCTET POUR OCTET (b3e896f7…) — le juge FAUTIF nommé aux
      283/284 (« la faute était au juge du labo »), réparé au v2
      (302fa3a1…, R_JOURNAL 0xE4E0→0xE4A0) demeurant AUX ARCHIVES du
      bac 295 ; le kit D210 embarqua le v1 : R_JOURNAL = 0xE4E0,
      SOIXANTE-QUATRE octets au-dessus de la vérité du layout
      (loupe/layout.py : 0xE4A0) ;
  R3  LA PREUVE T0 du terrain : la console porte [VERT] T0 loupe.exe
      cf251c12… == la gravure == la pièce du kit GUI recoupée au labo ;
  R4  LE VERDICT : 18 VERT, 2 ROUGE — les DEUX ROUGE sont EXACTEMENT
      les DEUX vecteurs V2 du recouvrement du journal, LA MÊME PAIRE
      que le juge v1 fautif fit rouge à D204 (le témoin v1 aux archives
      en regard) ; le code retour 1 ;
  R5  LE REJEU FORENSIQUE (à la manière de la 333 : la cause confirmée
      sur les deux rives) : l'oracle du bloc couru DEUX FOIS — TEL QUEL
      (le témoignage : 22 VERT attendu, le RAPPORT-UNITE-D210-01) et
      GREFFÉ de la constante du scénario livré (L.R_JOURNAL = 0xE4E0
      pour la section V2 seule) : les DEUX MÊMES vecteurs DOIVENT
      basculer ROUGE, tout le demeurant VERT — le verdict du terrain
      REPRODUIT au labo PAR LA CONSTANTE SEULE : la cause est le JUGE
      livré, JAMAIS la pièce ;
  R6  LA MAIN (D99) : le témoin déposé == le témoin avant-main gravé
      au DEPOT (1578 o, sha256 0c1ce902…) + la main posée (daté
      17/11/2026, signé Alexis Lopez — la même main que la campagne) ;
  R7  LA MACHINE : PORTABLE · Windows 10 · AMD64 · Python 3.14.10
      (CA2 — la même que les runs de la campagne D204) ;
  R8  LA CHRONOLOGIE : le kit livré au /test 17:15Z → le run 19:01:36Z
      → la fin 19:01:37Z (0,5 s) → LA MAIN 19:02:41Z → le coffre
      19:03:26Z — jamais une date avant le run ;
  R9  LE DEPOT : les gravures qu'il porte (la console, les SEPT pièces
      du kit) recoupées sha256 par sha256 contre les pièces déposées
      et le kit GUI du labo ;
  R10 LA CAP M1 : la PREMIÈRE livraison du bloc (aucun zip au /test, le
      DEPOT porte « 0 assemblage ») — le dépôt est le réceptacle ENTIER
      sans le zip du GUI (nommé, jamais maquillé)."""
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

BAC = REPO / "scripts" / "campagne_d204" / "depot-run-unite02-d210-338"
EPREUVES = BAC / "epreuves"
KIT_GUI = pathlib.Path("/home/z/my-project/download/"
                       "TRIADE_gui_unite02_d210_v1")
BAC_295 = REPO / "scripts" / "campagne_d204" / "depot-run-v2-T-295" / "epreuves"
ORACLE = (REPO / "scripts" / "campagne_d204" / "unite-02-T-d210"
          / "oracle_unite02.py")
LAYOUT = REPO / "loupe" / "layout.py"
TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DOSSIER_ID = "1K0lmnAOaJmo7yL1RnXrxXiXuOlS8-3vt"   # preuves-unite02/ au /test

CONSOLE = next(EPREUVES.glob("run-console-unite02-d210-*.txt"))
TEMOIN = EPREUVES / "temoin-unite02.txt"
DEPOT = EPREUVES / "DEPOT-d210-unite02.txt"
RAPPORT = BAC / "RECOUP-338-preuves-unite02.txt"


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def md5f(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def lignes(p):
    return [l.rstrip("\r") for l in p.read_text(encoding="utf-8",
                                                errors="replace").split("\n")]


rapport = []


def note(num, vert, texte):
    ligne = f"[{'VERT' if vert else 'ROUGE'}] R{num}: {texte}"
    print(ligne, flush=True)
    rapport.append(ligne)


def titre(texte):
    print(texte, flush=True)
    rapport.append(texte)


# ---------------------------------------------------------------- le dépôt Drive
titre("RECOUP-338 — LE RUN TERRAIN DE L'UNITÉ 02 D210 AU KIT GUI 1-CLIC REÇU\n"
      "(le dépôt preuves-unite02/ du coffre /test ; l'annonce du développeur : "
      "« preuves deposees dans le drive /test »)\n"
      + "=" * 78)

# le dépôt, où qu'il vive (racine ou archives après le rangement éventuel)
st, body, _ = ds.api("GET", ds.API + "/files/" + DOSSIER_ID
                     + "?fields=name,createdTime,modifiedTime")
meta_dossier = json.loads(body)
pieces_meta = {}
token_pages = None
while True:
    params = {"q": f"'{DOSSIER_ID}' in parents and trashed = false",
              "pageSize": "100",
              "fields": ("nextPageToken,files(id,name,mimeType,md5Checksum,"
                         "size,modifiedTime,createdTime)")}
    if token_pages:
        params["pageToken"] = token_pages
    st, body, _ = ds.api("GET", ds.API + "/files?"
                         + urllib.parse.urlencode(params))
    obj = json.loads(body)
    for f in obj.get("files", []):
        pieces_meta[f["name"]] = f
    token_pages = obj.get("nextPageToken")
    if not token_pages:
        break

# R1 — les pièces rapatriées, md5 == Drive
ok_r1 = all(md5f(EPREUVES / n) == pieces_meta.get(n, {}).get("md5Checksum")
            for n in ("temoin-unite02.txt", "DEPOT-d210-unite02.txt",
                      CONSOLE.name))
note(1, ok_r1,
     f"les TROIS pièces du bac ({len(pieces_meta)} au dépôt Drive) : md5 "
     f"re-calculés == les métadonnées Drive ({', '.join(sorted(pieces_meta))})")

# R2 — LE JUGE LIVRÉ : le v1 fautif de D204, octet pour octet
sha_kit = sha256f(KIT_GUI / "scenario-unite02.py")
sha_v1 = sha256f(BAC_295 / "scenario-unite02-v1.py")
sha_v2 = sha256f(BAC_295 / "scenario-unite02-v2.py")
r_journal_v1 = re.search(r"^R_JOURNAL = (0x[0-9A-Fa-f]+)",
                         (KIT_GUI / "scenario-unite02.py").read_text(
                             encoding="utf-8"), re.M).group(1)
r_journal_v2 = re.search(r"^R_JOURNAL = (0x[0-9A-Fa-f]+)",
                         (BAC_295 / "scenario-unite02-v2.py").read_text(
                             encoding="utf-8"), re.M).group(1)
r_journal_lay = re.search(r"^R_JOURNAL = (0x[0-9A-Fa-f]+)",
                          LAYOUT.read_text(encoding="utf-8"), re.M).group(1)
ok_r2 = (sha_kit == sha_v1 and sha_kit != sha_v2
         and r_journal_v1 == "0xE4E0" and r_journal_v2 == "0xE4A0"
         and r_journal_lay == "0xE4A0")
note(2, ok_r2,
     f"LE JUGE LIVRÉ : le scénario du kit {sha_kit[:8]}… == le juge v1 de "
     f"D204 {sha_v1[:8]}… OCTET POUR OCTET (le juge FAUTIF des 283/284) ; "
     f"le v2 réparé ({sha_v2[:8]}…) AUX ARCHIVES, non livré ; R_JOURNAL : "
     f"livré {r_journal_v1} vs la vérité du layout {r_journal_lay} "
     f"(le v2 porte {r_journal_v2}) — SOIXANTE-QUATRE octets d'écart")

# R3 — la preuve T0 du terrain
c_lignes = lignes(CONSOLE)
t0 = [l for l in c_lignes if l.startswith("[VERT] T0:")]
sha_loupe = sha256f(KIT_GUI / "loupe.exe")
ok_r3 = bool(t0) and sha_loupe[:16] in t0[0] and "127488" in str(
    (KIT_GUI / "loupe.exe").stat().st_size)
note(3, ok_r3,
     f"LA PREUVE T0 : la console porte « {t0[0].split(' — ')[1] if t0 else '?'} »"
     f" ; la pièce du kit recoupée AU LABO : loupe.exe "
     f"{(KIT_GUI / 'loupe.exe').stat().st_size} o, sha256 {sha_loupe[:16]}… "
     f"== la gravure du kit GUI livré à la 337")

# R4 — le verdict : la même paire ROUGE que le juge v1 fautif de D204
vec_console = [(c, n) for c, n in re.findall(
    r"^\[(VERT|ROUGE)\] (\S+)", "\n".join(c_lignes), re.M)]
rouges_console = sorted(n for c, n in vec_console if c == "ROUGE")
verts_console = sorted(n for c, n in vec_console if c == "VERT")
t_v1 = (BAC_295 / "temoin-unite02-v1-en-regard.txt").read_text(
    encoding="utf-8")
rouges_v1 = sorted(n for c, n in re.findall(r"^  (VERT|ROUGE) (\S+)$",
                                            t_v1, re.M) if c == "ROUGE")
code_retour = [l for l in c_lignes if l.startswith("le code retour :")]
ok_r4 = (rouges_console == rouges_v1 == sorted([
    "V2:les-bords-de-fenetre", "V2:cinq-entrees-dont-une-non-alignee"])
    and len(verts_console) == 18 and len(rouges_console) == 2
    and code_retour and "1" in code_retour[-1])
note(4, ok_r4,
     f"LE VERDICT : {len(verts_console)} VERT, {len(rouges_console)} ROUGE "
     f"(code retour {code_retour[-1].split(': ')[1] if code_retour else '?'}) "
     f"— les DEUX ROUGE : {', '.join(rouges_console)} == LA MÊME PAIRE que "
     f"le juge v1 fautif fit rouge à D204 (le témoin v1 aux archives en "
     f"regard) — la signature du JUGE, pas de la pièce")

# R5 — LE REJEU FORENSIQUE : l'oracle tel quel vs greffé de la constante
titre("\nLE REJEU FORENSIQUE — l'oracle du bloc couru DEUX FOIS "
      "(tel quel / greffé de la constante du scénario livré) :")
ANCRE = ("    # ---- V2 : LE RECOUVREMENT DU JOURNAL "
         "-------------------------------------")
GREFFE = (ANCRE + "\n"
          "    # LE REJEU FORENSIQUE 338 : la constante du scénario LIVRÉ au "
          "kit\n"
          "    # (le juge v1 de D204) — le juge fautif pose le journal "
          "SOIXANTE-QUATRE\n"
          "    # octets au-dessus de la vérité du layout (0xE4A0).\n"
          "    L.R_JOURNAL = 0xE4E0\n")
src_oracle = ORACLE.read_text(encoding="utf-8")
assert src_oracle.count(ANCRE) == 1, "l'ancre V2 introuvable à l'oracle"
fautif = BAC / "oracle_rejeu_fautif_338.py"
fautif.write_text(src_oracle.replace(ANCRE, GREFFE), encoding="utf-8")


def courir_oracle(script, sortie):
    p = subprocess.run([sys.executable, "-u", str(script)],
                       capture_output=True, timeout=240, cwd=str(BAC))
    (BAC / sortie).write_bytes(p.stdout + p.stderr)
    return p.stdout.decode("utf-8", "replace")


def parse_oracle(txt):
    vecs = re.findall(r"^\[(VERT|ROUGE)\] (\S+)", txt, re.M)
    m = re.search(r"=== L'ORACLE DU BLOC : (\d+) VERT, (\d+) ROUGE", txt)
    return vecs, m


txt_verite = courir_oracle(ORACLE, "rejeu-338-oracle-verite.txt")
vecs_a, m_a = parse_oracle(txt_verite)
txt_fautif = courir_oracle(fautif, "rejeu-338-oracle-fautif.txt")
vecs_b, m_b = parse_oracle(txt_fautif)
rouges_b = sorted(n for c, n in vecs_b if c == "ROUGE")
verts_b = [n for c, n in vecs_b if c == "VERT"]
rouges_attendus = sorted(set(rouges_console))
ok_r5 = (m_a and m_b and m_a.group(1) == "22" and m_a.group(2) == "0"
         and m_b.group(2) == "2" and rouges_b == rouges_attendus
         and len(verts_b) == len(vecs_a) - 2
         and all(c == "VERT" for c, _ in vecs_a))
note(5, ok_r5,
     f"L'ORACLE TEL QUEL : {m_a.group(1)} VERT, {m_a.group(2)} ROUGE "
     f"(la pièce CORRECTE, le RAPPORT-UNITE-D210-01 re-vécu) ; L'ORACLE "
     f"GREFFÉ (R_JOURNAL = 0xE4E0, la constante du scénario livré, la "
     f"section V2 seule) : {m_b.group(1)} VERT, {m_b.group(2)} ROUGE — "
     f"les DEUX MÊMES vecteurs ({', '.join(rouges_b)}) ROUGE, tout le "
     f"demeurant VERT — LE VERDICT DU TERRAIN REPRODUIT AU LABO PAR LA "
     f"CONSTANTE SEULE : la cause est le JUGE livré, JAMAIS la pièce "
     f"(les consoles aux rejeu-338-oracle-*.txt du bac)")

# R6 — LA MAIN (D99) : le témoin avant-main + la main posée
t_lignes = lignes(TEMOIN)
depose = TEMOIN.read_bytes()
rec = []
for l in depose.decode("utf-8").split("\n"):
    if l.startswith("Daté le : "):
        rec.append("Daté le : " + "_" * 20)
    elif l.startswith("Signé    : "):
        rec.append("Signé    : " + "_" * 20)
    else:
        rec.append(l)
avant_main = "\n".join(rec).encode("utf-8")
gravures_depot = {}
section_kit = False
for l in lignes(DEPOT):
    m = re.match(r"^  (\S+)\s+(\d+) o\s+([0-9a-f]{64})$", l)
    if m:
        gravures_depot[m.group(1)] = (int(m.group(2)), m.group(3))
date_main = re.search(r"Daté le : _*([^_]+)_+", depose.decode("utf-8"))
signe_main = re.search(r"Signé    : _*([^_]+)_+", depose.decode("utf-8"))
ok_r6 = (gravures_depot.get("temoin-unite02.txt")
         == (len(avant_main), hashlib.sha256(avant_main).hexdigest())
         and date_main and date_main.group(1).strip() == "17/11/2026"
         and signe_main and signe_main.group(1).strip() == "Alexis Lopez")
note(6, ok_r6,
     f"LA MAIN (D99) : le témoin déposé {len(depose)} o == le témoin "
     f"avant-main gravé au DEPOT ({len(avant_main)} o, sha256 "
     f"{hashlib.sha256(avant_main).hexdigest()[:8]}… MATCH byte-byte) + la "
     f"main posée (+{len(depose) - len(avant_main)} o) : daté le "
     f"{date_main.group(1).strip() if date_main else '?'}, signé "
     f"{signe_main.group(1).strip() if signe_main else '?'} — la même main "
     f"que les témoins de la campagne (264/266/267/272/276/284/287/294/295)")

# R7 — la machine
machine = [l for l in t_lignes if l.startswith("la machine  :")]
ok_r7 = bool(machine) and "PORTABLE" in machine[0] \
    and "Windows 10" in machine[0] and "AMD64" in machine[0] \
    and "Python 3.14.10" in machine[0]
note(7, ok_r7,
     f"LA MACHINE : {machine[0].split(' : ', 1)[1] if machine else '?'} "
     f"(CA2 — la même que les runs de la campagne D204) ; l'argv de la "
     f"console (…Python314\\python.exe) cohérent")

# R8 — la chronologie (les voix Drive : naissance du dossier, mtimes,
# la livraison du kit au /test ; le nom de la console et le témoin
# vivent à l'heure LOCALE du terrain, l'heure d'hiver UTC+1)
st, body, _ = ds.api("GET", ds.API + "/files/?"
                     + urllib.parse.urlencode({
                         "q": f"'{TEST_ID}' in parents and trashed = false",
                         "pageSize": "200",
                         "fields": "files(name,modifiedTime,size)"}))
racine = {f["name"]: f for f in json.loads(body).get("files", [])}
kit_zip = racine.get("kit-gui-1clic-unite02-d210-20261118.zip", {})
nom_ts = re.search(r"-(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})",
                   CONSOLE.name)
local_nom = (f"{nom_ts.group(3)}/{nom_ts.group(2)}/{nom_ts.group(1)} "
             f"{nom_ts.group(4)}:{nom_ts.group(5)}:{nom_ts.group(6)}")
debut_console = re.search(r"début le (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",
                           "\n".join(c_lignes))
debut_depot = re.search(r"début (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",
                        "\n".join(lignes(DEPOT)))
run_utc_m = re.search(r"le run\s+: (\S+) \(UTC\)", depose.decode("utf-8"))
ru = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z",
              run_utc_m.group(1) if run_utc_m else "")
local_du_temoin = (f"{ru.group(3)}/{ru.group(2)}/{ru.group(1)} "
                   f"{int(ru.group(4)) + 1:02d}:{ru.group(5)}:{ru.group(6)}"
                   if ru else "?")
mt_console = pieces_meta.get(CONSOLE.name, {}).get("modifiedTime", "")
mt_temoin = pieces_meta.get("temoin-unite02.txt", {}).get("modifiedTime", "")
ne_dossier = meta_dossier.get("createdTime", "")
kit_livre = kit_zip.get("modifiedTime", "")
ok_r8 = (local_nom == debut_console.group(1) == debut_depot.group(1)
         == local_du_temoin
         and kit_livre < mt_console < mt_temoin < ne_dossier
         and run_utc_m and run_utc_m.group(1) < mt_console)
note(8, ok_r8,
     f"LA CHRONOLOGIE : le kit livré au /test {kit_livre} → le run "
     f"{run_utc_m.group(1) if run_utc_m else '?'} (le témoin, UTC ; le nom "
     f"de la console « {local_nom} » == la ligne 1 == le chrono du DEPOT, "
     f"l'heure locale du terrain, l'heure d'hiver UTC+1) → la console "
     f"couchée {mt_console} (le chrono M4 0,5 s) → LA MAIN {mt_temoin} "
     f"(le mtime du témoin) → le coffre {ne_dossier} (la naissance du "
     f"dossier) — jamais une date avant le run")

# R9 — LE DEPOT : les gravures recoupées (la console + les pièces du kit)
ok_console = gravures_depot.get(CONSOLE.name) == (
    CONSOLE.stat().st_size, sha256f(CONSOLE))
verts_kit, ecarts_kit = 0, []
for nom, (taille, sha) in sorted(gravures_depot.items()):
    if nom in ("temoin-unite02.txt", CONSOLE.name):
        continue
    p = KIT_GUI / nom
    if not p.is_file():
        ecarts_kit.append(f"{nom}: ABSENT au kit GUI du labo")
        continue
    if sha256f(p) == sha and p.stat().st_size == taille:
        verts_kit += 1
    else:
        ecarts_kit.append(f"{nom}: sha divergent")
ok_r9 = ok_console and verts_kit == 7 and not ecarts_kit
note(9, ok_r9,
     f"LE DEPOT : la console gravée ({CONSOLE.stat().st_size} o, "
     f"{sha256f(CONSOLE)[:8]}…) == la pièce déposée byte-byte ; les "
     f"SEPT pièces du kit gravées (loupe.exe, les trois témoins, vide.bin, "
     f"le scénario, EMPREINTES-PIECES-RUN) recoupées sha256 par "
     f"sha256 == le kit GUI livré à la 337 "
     f"{'— la chaîne de garde par le contenu (D143)' if not ecarts_kit else ' — ÉCARTS : ' + ' ; '.join(ecarts_kit)}")

# R10 — LA CAP M1 : la première livraison du bloc, le réceptacle sans zip
zips = [n for n in racine if re.match(r"preuves-unite02-d210-.*\.zip", n)]
cap = [l for l in lignes(DEPOT) if "LA CAP M1" in l]
assemblages = re.search(r"(\d+) assemblage", cap[0] if cap else "")
ok_r10 = not zips and assemblages and assemblages.group(1) == "0"
note(10, ok_r10,
     f"LA CAP M1 : {len(zips)} zip au /test, le DEPOT porte « le GUI compte "
     f"{assemblages.group(1) if assemblages else '?'} assemblage(s) vécu(s) » — "
     f"la PREMIÈRE livraison du bloc (TROIS par bloc, § 7 du plan D204) ; "
     f"le dépôt est le RÉCEPTACLE ENTIER (témoin signé + DEPOT + console) "
     f"SANS le zip assemblé du GUI — l'observation NOMMÉE : le terrain "
     f"déposa le dossier preuves-unite02/ lui-même, jamais le zip ; le "
     f"contenu est complet, l'exigence D99 tenue par le témoin daté-signé, "
     f"l'emballage diffère — jamais maquillé")

# ---------------------------------------------------------------- le bilan
bilan_v = sum(1 for l in rapport if l.startswith("[VERT]"))
bilan_r = sum(1 for l in rapport if l.startswith("[ROUGE]"))
titre("\nLE BILAN DU RECOUP : "
      f"{bilan_v} VERT / {bilan_r} ROUGE\n"
      "LA CAUSE DES DEUX ROUGE DU TERRAIN — nommée avant toute correction "
      "(D202) :\n"
      "  le kit GUI livré à la 337 embarque le juge v1 de D204 (octet pour "
      "octet,\n"
      "  b3e896f7…) — le juge FAUTIF de l'histoire D204 (R_JOURNAL = "
      "0xE4E0,\n"
      "  soixante-quatre octets au-dessus de la vérité du layout 0xE4A0) ; "
      "la\n"
      "  pièce D210 est CORRECTE (l'oracle au harnais : 22 VERT, 0 ROUGE ; "
      "le\n"
      "  rejeu R5 : la seule constante fautive reproduit le verdict "
      "terrain).\n"
      "  Le run terrain NE CONSOMME PAS d'itération (le précédent 295 : la "
      "faute\n"
      "  au juge, jamais à la pièce) — T-loupe-02-d210-it1 attend le re-run "
      "au\n"
      "  juge réparé.\n"
      "LA CORRECTION (au commandement) : la re-livraison du kit avec le "
      "juge v2\n"
      "  (302fa3a1…, R_JOURNAL = 0xE4A0 — la vérité du layout) aux "
      "archives du\n"
      "  bac 295, puis le re-run terrain au geste du développeur.\n"
      "LA SUITE : ① la correction commandée ; ② loupe-08 le bras T d'abord "
      "(la\n"
      "  séquence tirée, jamais re-tirée) ; la re-livraison d'attribution "
      "empirique\n"
      "  au commandement.")

RAPPORT.write_text("\n".join(rapport) + "\n", encoding="utf-8",
                   newline="\n")
print(f"\n[recoup] le rapport couché : {RAPPORT.relative_to(REPO)}")
sys.exit(0 if bilan_r == 0 else 1)
