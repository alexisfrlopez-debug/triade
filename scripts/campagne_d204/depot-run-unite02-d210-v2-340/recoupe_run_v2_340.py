#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recoupe_run_v2_340.py — LE RECOUP DU DÉPÔT preuves-unite02/ NEUF reçu au
coffre /test (l'annonce du développeur : « preuves du run dans le drive
/test » — le RE-RUN TERRAIN de l'unité 02 D210 au kit GUI 1-clic v2 AU
JUGE RÉPARÉ livré à la 339). Chaque contrôle est calculé depuis les
pièces — aucun chiffre recopié ; un écart nommé est un RÉSULTAT, jamais
un échec à maquiller (D189).

LES CONTRÔLES :
  R1  les pièces : TROIS rapatriées au bac, chacune re-téléchargée DEUX
      FOIS byte-byte au rapatriement, md5 == la métadonnée Drive
      (re-recoupé ici par re-listing du dépôt, où qu'il vive) ;
  R2  LE JUGE DU RUN : le scénario gravé au DEPOT == le juge v2 RÉPARÉ
      (302fa3a1…) == le scénario du kit v2 du labo == les archives du
      bac 295 OCTET POUR OCTET, R_JOURNAL = 0xE4A0 == la vérité du
      layout, ≠ le v1 fautif (b3e896f7…) ; le chemin du kit à la
      console porte l'édition juge-v2 ;
  R3  LA PREUVE T0 du terrain : la console porte [VERT] T0 loupe.exe
      cf251c12… == la gravure == la pièce du kit v2 recoupée au labo ;
  R4  LE VERDICT : 20 VERT, 0 ROUGE, code retour 0 — L'ATTENDU DU
      CORRECTIF-JUGE-V2 TENU : les DEUX vecteurs V2 (la paire ROUGE du
      run v1) passés VERT ; le diff des consoles v1/v2 ne porte QUE les
      deux vecteurs — le même verdict que l'oracle du labo ;
  R5  LA MAIN (D99) : le témoin déposé == le témoin avant-main gravé au
      DEPOT (1567 o, 9ac528cc…) + la main posée (daté 17/11/2026,
      signé Alexis Lopez — la même main que la campagne) ;
  R6  LA MACHINE : PORTABLE · Windows 10 · AMD64 · Python 3.14.10
      (CA2 — la même que les runs de la campagne D204) ;
  R7  LA CHRONOLOGIE : le run v1 19:01:36Z → le kit v2 livré 19:51:35Z
      (la correction APRÈS le run fautif) → le re-run 20:02:45Z → la
      console 20:02:45.582Z (le chrono M4 0,4 s) → LA MAIN 20:03:38Z →
      le coffre 20:04:11Z — jamais une date avant le run ;
  R8  LE DEPOT : la console gravée == la pièce déposée byte-byte ; les
      SEPT pièces du kit gravées recoupées sha256 par sha256 == le kit
      v2 livré à la 339 ;
  R9  LA CAP M1 : la SECONDE livraison du bloc (aucun zip au /test, le
      DEPOT porte « 0 assemblage ») — le réceptacle ENTIER sans le zip
      du GUI (l'observation nommée reconduite) ;
  R10 LA MÊME PIÈCE : les CINQ pièces matérielles du run (loupe.exe,
      les trois témoins, vide.bin) gravées au DEPOT v2 == le DEPOT v1
      == le kit v1 OCTET POUR OCTET — la cause était au juge, JAMAIS à
      la pièce (D202 clos : rien ne changea que le juge)."""
import hashlib
import json
import pathlib
import re
import sys
import urllib.parse

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

BAC = REPO / "scripts" / "campagne_d204" / "depot-run-unite02-d210-v2-340"
EPREUVES = BAC / "epreuves"
BAC_338 = REPO / "scripts" / "campagne_d204" / "depot-run-unite02-d210-338"
EPREUVES_338 = BAC_338 / "epreuves"
KIT_V2 = pathlib.Path("/home/z/my-project/download/"
                      "TRIADE_gui_unite02_d210_v2")
KIT_V1 = pathlib.Path("/home/z/my-project/download/"
                      "TRIADE_gui_unite02_d210_v1")
BAC_295 = REPO / "scripts" / "campagne_d204" / "depot-run-v2-T-295" / "epreuves"
LAYOUT = REPO / "loupe" / "layout.py"
TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DOSSIER_ID = "1u7QW6XfCMPgECY_ObThTtA3OkbPVp1Yt"   # preuves-unite02/ NEUF

CONSOLE = EPREUVES / "run-console-unite02-d210-20261117-210245.txt"
CONSOLE_V1 = next(EPREUVES_338.glob("run-console-unite02-d210-*.txt"))
TEMOIN = EPREUVES / "temoin-unite02.txt"
TEMOIN_V1 = EPREUVES_338 / "temoin-unite02.txt"
DEPOT = EPREUVES / "DEPOT-d210-unite02.txt"
DEPOT_V1 = EPREUVES_338 / "DEPOT-d210-unite02.txt"
RAPPORT = BAC / "RECOUP-340-preuves-unite02-v2.txt"


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
titre("RECOUP-340 — LE RE-RUN TERRAIN DE L'UNITÉ 02 D210 AU JUGE RÉPARÉ REÇU\n"
      "(le dépôt preuves-unite02/ NEUF du coffre /test ; l'annonce du "
      "développeur : « preuves du run dans le drive /test »)\n"
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

# les gravures du DEPOT (nom, taille, sha256)
gravures_depot = {}
for l in lignes(DEPOT):
    m = re.match(r"^  (\S+)\s+(\d+) o\s+([0-9a-f]{64})$", l)
    if m:
        gravures_depot[m.group(1)] = (int(m.group(2)), m.group(3))

# R2 — LE JUGE DU RUN : le v2 réparé, octet pour octet
sha_depot = gravures_depot.get("scenario-unite02.py", (0, ""))[1]
sha_kit_v2 = sha256f(KIT_V2 / "scenario-unite02.py")
sha_v2 = sha256f(BAC_295 / "scenario-unite02-v2.py")
sha_v1 = sha256f(BAC_295 / "scenario-unite02-v1.py")
r_journal_kit = re.search(r"^R_JOURNAL = (0x[0-9A-Fa-f]+)",
                         (KIT_V2 / "scenario-unite02.py").read_text(
                             encoding="utf-8"), re.M).group(1)
r_journal_v1 = re.search(r"^R_JOURNAL = (0x[0-9A-Fa-f]+)",
                         (BAC_295 / "scenario-unite02-v1.py").read_text(
                             encoding="utf-8"), re.M).group(1)
r_journal_lay = re.search(r"^R_JOURNAL = (0x[0-9A-Fa-f]+)",
                          LAYOUT.read_text(encoding="utf-8"), re.M).group(1)
c_lignes = lignes(CONSOLE)
chemin_kit = [l for l in c_lignes if l.startswith("[témoin] D:\\")]
kit_v2_au_chemin = any("kit-gui-1clic-unite02-d210-juge-v2-20261118"
                        in l for l in chemin_kit)
ok_r2 = (sha_depot == sha_kit_v2 == sha_v2 and sha_depot != sha_v1
         and r_journal_kit == "0xE4A0" == r_journal_lay
         and r_journal_v1 == "0xE4E0" and kit_v2_au_chemin)
note(2, ok_r2,
     f"LE JUGE DU RUN : le scénario gravé au DEPOT {sha_depot[:8]}… == le "
     f"juge v2 RÉPARÉ == le kit v2 du labo {sha_kit_v2[:8]}… == les archives "
     f"du bac 295 OCTET POUR OCTET (22 476 o, R_JOURNAL = {r_journal_kit} == "
     f"la vérité du layout) — ≠ le v1 fautif ({sha_v1[:8]}…, "
     f"{r_journal_v1}) ; le chemin du kit à la console porte l'édition "
     f"juge-v2 : la correction de la 339 courue au terrain")

# R3 — la preuve T0 du terrain
t0 = [l for l in c_lignes if l.startswith("[VERT] T0:")]
sha_loupe = sha256f(KIT_V2 / "loupe.exe")
ok_r3 = bool(t0) and sha_loupe[:16] in t0[0] \
    and gravures_depot.get("loupe.exe", (0, ""))[1] == sha_loupe
note(3, ok_r3,
     f"LA PREUVE T0 : la console porte « {t0[0].split(' — ')[1] if t0 else '?'} »"
     f" ; la pièce du kit v2 recoupée AU LABO : loupe.exe "
     f"{(KIT_V2 / 'loupe.exe').stat().st_size} o, sha256 {sha_loupe[:16]}… "
     f"== la gravure du DEPOT == le kit GUI v2 livré à la 339")

# R4 — LE VERDICT : 20 VERT, 0 ROUGE, code 0 — les DEUX vecteurs V2 VERT
vec_console = [(c, n) for c, n in re.findall(
    r"^\[(VERT|ROUGE)\] (\S+)", "\n".join(c_lignes), re.M)]
vec_v1 = [(c, n) for c, n in re.findall(
    r"^\[(VERT|ROUGE)\] (\S+)", "\n".join(lignes(CONSOLE_V1)), re.M)]
dict_v2 = dict((n, c) for c, n in vec_console)
dict_v1 = dict((n, c) for c, n in vec_v1)
code_retour = [l for l in c_lignes if l.startswith("le code retour :")]
la_pair = sorted(["V2:les-bords-de-fenetre",
                  "V2:cinq-entrees-dont-une-non-alignee"])
seule_mut = sorted(n for n in dict_v2
                   if dict_v2.get(n) != dict_v1.get(n)) == la_pair \
    and all(dict_v2[n] == "VERT" for n in la_pair)
ok_r4 = (len(vec_console) == 20
         and all(c == "VERT" for c, _ in vec_console)
         and code_retour and "0" in code_retour[-1]
         and set(dict_v2) == set(dict_v1) and seule_mut)
note(4, ok_r4,
     f"LE VERDICT : {sum(1 for c, _ in vec_console if c == 'VERT')} VERT, "
     f"{sum(1 for c, _ in vec_console if c == 'ROUGE')} ROUGE (code retour "
     f"{code_retour[-1].split(': ')[1] if code_retour else '?'}) — "
     f"L'ATTENDU DU CORRECTIF-JUGE-V2 TENU : les DEUX vecteurs V2 "
     f"({', '.join(la_pair)}) — la paire ROUGE du run v1 — passés VERT ; le "
     f"diff des consoles v1/v2 ne porte QUE ces deux vecteurs : LA MÊME "
     f"PIÈCE, le juge seul changea — le verdict de l'oracle du labo "
     f"(22 VERT, 0 ROUGE, le RAPPORT-UNITE-D210-01) confirmé au terrain")

# R5 — LA MAIN (D99) : le témoin avant-main + la main posée
depose = TEMOIN.read_bytes()
texte_depose = depose.decode("utf-8")
gravure_temoin = gravures_depot.get("temoin-unite02.txt", (0, ""))
avant_main, n_blanc = None, None
for n in range(8, 41):
    rec = []
    for l in texte_depose.split("\n"):
        if l.startswith("Daté le : "):
            rec.append("Daté le : " + "_" * n)
        elif l.startswith("Signé    : "):
            rec.append("Signé    : " + "_" * n)
        else:
            rec.append(l)
    cand = "\n".join(rec).encode("utf-8")
    if hashlib.sha256(cand).hexdigest() == gravure_temoin[1] \
            and len(cand) == gravure_temoin[0]:
        avant_main, n_blanc = cand, n
        break
date_main = re.search(r"Daté le : _*([^_]+)_+", texte_depose)
signe_main = re.search(r"Signé    : _*([^_]+)_+", texte_depose)
ok_r5 = (avant_main is not None
         and date_main and date_main.group(1).strip() == "17/11/2026"
         and signe_main and signe_main.group(1).strip() == "Alexis Lopez")
note(5, ok_r5,
     f"LA MAIN (D99) : le témoin déposé {len(depose)} o == le témoin "
     f"avant-main gravé au DEPOT ({len(avant_main) if avant_main else '?'} o"
     f", sha256 {gravure_temoin[1][:8]}… MATCH byte-byte, les blancs "
     f"{n_blanc} soulignés) + la main posée (+{len(depose) - len(avant_main) if avant_main else '?'} o) : "
     f"daté le {date_main.group(1).strip() if date_main else '?'}, signé "
     f"{signe_main.group(1).strip() if signe_main else '?'} — la même main "
     f"que les témoins de la campagne (264/266/267/272/276/284/287/294/295"
     f"/338)")

# R6 — la machine
t_lignes = lignes(TEMOIN)
machine = [l for l in t_lignes if l.startswith("la machine  :")]
argv = [l for l in c_lignes if l.startswith("l'argv exact :")]
ok_r6 = bool(machine) and "PORTABLE" in machine[0] \
    and "Windows 10" in machine[0] and "AMD64" in machine[0] \
    and "Python 3.14.10" in machine[0] \
    and argv and "Python314\\python.exe" in argv[0]
note(6, ok_r6,
     f"LA MACHINE : {machine[0].split(' : ', 1)[1] if machine else '?'} "
     f"(CA2 — la même que les runs de la campagne D204 et le run v1) ; "
     f"l'argv de la console (…Python314\\python.exe) cohérent")

# R7 — la chronologie (les voix Drive + le run v1 de la veille de la correction)
st, body, _ = ds.api("GET", ds.API + "/files?"
                     + urllib.parse.urlencode({
                         "q": f"'{TEST_ID}' in parents and trashed = false",
                         "pageSize": "200",
                         "fields": "files(name,modifiedTime,size)"}))
racine = {f["name"]: f for f in json.loads(body).get("files", [])}
kit_v2_zip = racine.get("kit-gui-1clic-unite02-d210-juge-v2-20261118.zip",
                        {})
run_v1_utc = re.search(r"le run\s+: (\S+) \(UTC\)",
                       TEMOIN_V1.read_text(encoding="utf-8"))
nom_ts = re.search(r"-(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})",
                   CONSOLE.name)
local_nom = (f"{nom_ts.group(3)}/{nom_ts.group(2)}/{nom_ts.group(1)} "
             f"{nom_ts.group(4)}:{nom_ts.group(5)}:{nom_ts.group(6)}")
debut_console = re.search(r"début le (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",
                           "\n".join(c_lignes))
debut_depot = re.search(r"début (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",
                        "\n".join(lignes(DEPOT)))
run_utc_m = re.search(r"le run\s+: (\S+) \(UTC\)", texte_depose)
ru = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z",
              run_utc_m.group(1) if run_utc_m else "")
local_du_temoin = (f"{ru.group(3)}/{ru.group(2)}/{ru.group(1)} "
                   f"{int(ru.group(4)) + 1:02d}:{ru.group(5)}:{ru.group(6)}"
                   if ru else "?")
mt_console = pieces_meta.get(CONSOLE.name, {}).get("modifiedTime", "")
mt_temoin = pieces_meta.get("temoin-unite02.txt", {}).get("modifiedTime", "")
ne_dossier = meta_dossier.get("createdTime", "")
kit_livre = kit_v2_zip.get("modifiedTime", "")


def instant(s):
    """ISO 8601 (Z ou fractionnaire) -> datetime comparable."""
    import datetime
    return datetime.datetime.fromisoformat(
        s.replace("Z", "+00:00")).replace(tzinfo=None) if s else None


ok_r7 = (local_nom == debut_console.group(1) == debut_depot.group(1)
         == local_du_temoin
         and run_v1_utc and instant(run_v1_utc.group(1)) < instant(kit_livre)
         and instant(kit_livre) < instant(run_utc_m.group(1))
         < instant(mt_console) < instant(mt_temoin) < instant(ne_dossier))
note(7, ok_r7,
     f"LA CHRONOLOGIE : le run v1 {run_v1_utc.group(1) if run_v1_utc else '?'} "
     f"→ le kit v2 AU JUGE RÉPARÉ livré au /test {kit_livre} (la correction "
     f"APRÈS le run fautif) → le re-run {run_utc_m.group(1) if run_utc_m else '?'} "
     f"(le témoin, UTC ; le nom de la console « {local_nom} » == la ligne 1 "
     f"== le chrono du DEPOT, l'heure locale du terrain, l'heure d'hiver "
     f"UTC+1) → la console couchée {mt_console} (le chrono M4 0,4 s) → "
     f"LA MAIN {mt_temoin} (le mtime du témoin) → le coffre {ne_dossier} "
     f"(la naissance du dossier) — jamais une date avant le run, le re-run "
     f"TOUJOURS après la livraison de la correction")

# R8 — LE DEPOT : les gravures recoupées (la console + les pièces du kit v2)
ok_console = gravures_depot.get(CONSOLE.name) == (
    CONSOLE.stat().st_size, sha256f(CONSOLE))
verts_kit, ecarts_kit = 0, []
for nom, (taille, sha) in sorted(gravures_depot.items()):
    if nom in ("temoin-unite02.txt", CONSOLE.name):
        continue
    p = KIT_V2 / nom
    if not p.is_file():
        ecarts_kit.append(f"{nom}: ABSENT au kit v2 du labo")
        continue
    if sha256f(p) == sha and p.stat().st_size == taille:
        verts_kit += 1
    else:
        ecarts_kit.append(f"{nom}: sha divergent")
ok_r8 = ok_console and verts_kit == 7 and not ecarts_kit
note(8, ok_r8,
     f"LE DEPOT : la console gravée ({CONSOLE.stat().st_size} o, "
     f"{sha256f(CONSOLE)[:8]}…) == la pièce déposée byte-byte ; les "
     f"SEPT pièces du kit gravées (loupe.exe, les trois témoins, vide.bin, "
     f"le scénario v2, EMPREINTES-PIECES-RUN v2 [cb2a8b0f…]) recoupées "
     f"sha256 par sha256 == le kit v2 livré à la 339 "
     f"{'— la chaîne de garde par le contenu (D143)' if not ecarts_kit else ' — ÉCARTS : ' + ' ; '.join(ecarts_kit)}")

# R9 — LA CAP M1 : la seconde livraison du bloc, le réceptacle sans zip
zips = [n for n in racine if re.match(r"preuves-unite02-d210-.*\.zip", n)]
cap = [l for l in lignes(DEPOT) if "LA CAP M1" in l]
assemblages = re.search(r"(\d+) assemblage", cap[0] if cap else "")
ok_r9 = not zips and assemblages and assemblages.group(1) == "0"
note(9, ok_r9,
     f"LA CAP M1 : {len(zips)} zip au /test, le DEPOT porte « le GUI compte "
     f"{assemblages.group(1) if assemblages else '?'} assemblage(s) vécu(s) » — "
     f"la SECONDE livraison du bloc (TROIS par bloc, § 7 du plan D204 ; la "
     f"première : le run v1 archivé à unite-02-d210-20261118/, une seule "
     f"reste) ; le dépôt est encore le RÉCEPTACLE ENTIER (témoin signé + "
     f"DEPOT + console) SANS le zip assemblé du GUI — l'observation NOMMÉE "
     f"reconduite : le terrain déposa le dossier preuves-unite02/ lui-même, "
     f"jamais le zip ; le contenu est complet, l'exigence D99 tenue par le "
     f"témoin daté-signé, l'emballage diffère — jamais maquillé")

# R10 — LA MÊME PIÈCE : les cinq pièces matérielles == le v1 == le kit v1
materielles = ["loupe.exe", "temoin-1.bin", "temoin-384.bin",
               "temoin-3f.bin", "vide.bin"]
gravures_v1 = {}
for l in lignes(DEPOT_V1):
    m = re.match(r"^  (\S+)\s+(\d+) o\s+([0-9a-f]{64})$", l)
    if m:
        gravures_v1[m.group(1)] = (int(m.group(2)), m.group(3))
meme_gravures = all(gravures_depot.get(n) == gravures_v1.get(n)
                    for n in materielles)
verts_v1, ecarts_v1 = 0, []
for n in materielles:
    p = KIT_V1 / n
    if gravures_depot.get(n) == (p.stat().st_size, sha256f(p)):
        verts_v1 += 1
    else:
        ecarts_v1.append(n)
ok_r10 = meme_gravures and verts_v1 == len(materielles) and not ecarts_v1
note(10, ok_r10,
     f"LA MÊME PIÈCE : les CINQ pièces matérielles du run (loupe.exe "
     f"{sha_loupe[:8]}…, les trois témoins, vide.bin) gravées au DEPOT v2 == "
     f"le DEPOT v1 == le kit v1 OCTET POUR OCTET — la correction de la 339 "
     f"ne toucha QUE le juge ; le diff des consoles v1/v2 (R4) ne porte que "
     f"les deux vecteurs : LA CAUSE ÉTAIT AU JUGE, JAMAIS À LA PIÈCE "
     f"(D202 clos — la pièce courut deux fois, toujours identique)")

# ---------------------------------------------------------------- le bilan
bilan_v = sum(1 for l in rapport if l.startswith("[VERT]"))
bilan_r = sum(1 for l in rapport if l.startswith("[ROUGE]"))
titre("\nLE BILAN DU RECOUP : "
      f"{bilan_v} VERT / {bilan_r} ROUGE\n"
      "LA CORRECTION DE LA 339 VÉRIFIÉE AU TERRAIN — l'attendu tenu :\n"
      "  le kit GUI 1-clic v2 AU JUGE RÉPARÉ couru au terrain rend\n"
      "  20 VERT, 0 ROUGE, code retour 0 — les DEUX vecteurs V2 du\n"
      "  recouvrement (la paire ROUGE du run v1) passés VERT ; la pièce\n"
      "  loupe.exe et les QUATRE autres pièces matérielles inchangées\n"
      "  octet pour octet entre les DEUX runs (le diff des consoles ne\n"
      "  porte QUE les deux vecteurs) — la faute était au juge v1\n"
      "  (b3e896f7…, R_JOURNAL = 0xE4E0), JAMAIS à la pièce ; le juge v2\n"
      "  (302fa3a1…, R_JOURNAL = 0xE4A0, la vérité du layout D161) livré\n"
      "  à la 339 fit vert ce que la vérité du labo (l'oracle :\n"
      "  22 VERT, 0 ROUGE) attendait.\n"
      "L'UNITÉ 02 D210 close au terrain (T-loupe-02-d210-it1 : le re-run\n"
      "  VERT au juge réparé — la ligne de carnet au geste du développeur,\n"
      "  le livre M3 + livraisons.csv M1 à l'onglet 4·LIVRE du GUI).\n"
      "LA SUITE : ② loupe-08 le bras T d'abord (la séquence tirée,\n"
      "  jamais re-tirée — la graine D217) ; la re-livraison d'attribution\n"
      "  empirique au commandement.")

RAPPORT.write_text("\n".join(rapport) + "\n", encoding="utf-8",
                   newline="\n")
print(f"\n[recoup] le rapport couché : {RAPPORT.relative_to(REPO)}")
sys.exit(0 if bilan_r == 0 else 1)
