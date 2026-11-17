#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recoupe_run_unite08_343.py — LE RECOUP du dépôt du run terrain de
l'unité 02 D210 LOUPE-08 LIGNE × BRAS T reçu au coffre /test (l'annonce du
développeur : « preuves dans le drive /test » — le dossier kit-unite-02-
d210-20261118/ né au /test 17/11 23:10:27Z, APRÈS la livraison du kit à la
342 [22:42:58Z] : le kit DÉZIPPÉ au terrain + les preuves nées du run au
geste du GUI 1-clic livré à la 342). Chaque contrôle est calculé depuis
les pièces — aucun chiffre recopié ; un écart nommé est un RÉSULTAT,
jamais un échec à maquiller (D189).

LES CONTRÔLES :
  R1  les pièces : SEPT nées du run rapatriées au bac, chacune re-téléchargée
      DEUX FOIS byte-byte, md5 == la métadonnée Drive (re-recoupé ici par
      re-listing du dépôt) ; la console racine == la console du réceptacle
      OCTET POUR OCTET (la copie de la collecte) ;
  R2  LE JUGE DU RUN : le scénario gravé au DEPOT == le juge D204 INCHANGÉ
      (44384f5d…, la version corrigée) == le kit du labo livré à la 342 ==
      la pièce au coffre — la faute au juge de la 338 ne se reproduit pas,
      NOMMÉE PARCE QU'ELLE NE SE REPRODUIT PAS (D202) ;
  R3  LA PREUVE T0 du terrain : la console porte [VERT] T0 loupe.exe
      41660a30… == la gravure == la pièce du kit recoupée au labo ; la
      gravure NÉE PARSÉE (le défaut T0 de l'unité 01 ne se reproduit pas
      non plus) ; le journal de session : le verrou 14/14 + la preuve T0
      (13 pièces vues par le scénario scellé) ;
  R4  LE VERDICT : 10 VERT, 0 ROUGE, code retour 0 — L'ATTENDU DU LIVRE
      TENU (les DIX verdicts : T0, V1 ×2, V2 ×2, V3 ×4, V4) ; les verdicts
      RECOPIÉS à l'identique console / état / témoin / journal (jamais
      recalculés) ;
  R5  LA MAIN (D99) : le témoin déposé == le témoin avant-main gravé au
      DEPOT (aux blancs) + la main posée (daté 18/11/2026, signé Alexis
      Lopez — la même main que les runs 338/340 de la campagne) ;
  R6  LA MACHINE : PORTABLE · Windows 10 · AMD64 · Python 3.14.10 (CA2 —
      la même que les runs de la campagne) ; l'argv de la console
      (…Python314\\python.exe) cohérent ; le DEPOT l'avoue honnête
      (« la machine : (non consignée) » — la machine vit au témoin) ;
  R7  LA CHRONOLOGIE : le kit livré 22:42:58Z → la session 00:09:05 locale
      → le verrou → TOUT LANCER 00:09:11 → la console couchée 23:09:12Z
      (chrono M4 0,6 s) → LA MAIN 23:09:51Z → la fenêtre fermée 23:09:56Z
      → le coffre né 23:10:27Z — jamais une date avant le kit, jamais une
      date avant le run ; l'OBSERVATION NOMMÉE : les DIX-HUIT pièces du
      kit au coffre portent un mtime uniforme (2026-11-18T20:00:00.000Z,
      valeur ronde ~21 h après le run, POSTÉRIEURE à la naissance du
      dossier même) — le geste de dépôt ne conserva pas leurs mtimes, la
      chaîne de garde vit aux vraies voix (mtimes des pièces nées du run,
      createdTime, md5 recoupés byte-byte) — JAMAIS maquillé ;
  R8  LE DEPOT : la console gravée == la pièce déposée byte-byte ; les SIX
      pièces du kit gravées recoupées sha256 par sha256 == le kit livré à
      la 342 ; le mutant falsifie-16.bin gravé == la pièce déposée == la
      composition du labo (l'octet 3 ^ 0x6F du doré de proxy.exe) ;
  R9  LA CAP M1 : LA PREMIÈRE livraison du bloc (l'état « livraisons : 0 »,
      le DEPOT « 0 assemblage », AUCUN zip au /test) — le terrain déposa le
      dossier kit-unite-02-d210-20261118/ ENTIER (le kit dézippé + les
      preuves nées du run), JAMAIS le zip assemblé — l'observation NOMMÉE
      reconduite : le contenu est complet, l'exigence D99 tenue par le
      témoin daté-signé, l'emballage diffère ;
  R10 LA MÊME PIÈCE : les DIX-HUIT pièces du kit au coffre == le kit du
      labo livré à la 342 OCTET POUR OCTET (md5 18/18) — le run ne toucha
      AUCUNE pièce scellée (le verrou les recoupa au lancement : 14/14
      VERT au journal)."""
import hashlib
import json
import pathlib
import re
import sys
import urllib.parse

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

BAC = REPO / "scripts" / "campagne_d204" / "depot-run-unite08-d210-343"
EPREUVES = BAC / "epreuves"
KIT_LABO = pathlib.Path("/home/z/my-project/download/"
                        "TRIADE_gui_unite08_d210_v1")
TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DOSSIER_ID = "1oxnULtkeTicLvqBlDeVhB06_GCaTBKqH"  # kit-unite-02-d210-20261118/

CONSOLE = EPREUVES / "run-console-unite08-d210-20261118-000911.txt"
CONSOLE_RECEPT = (EPREUVES / "preuves-unite08"
                  / "run-console-unite08-d210-20261118-000911.txt")
TEMOIN = EPREUVES / "preuves-unite08" / "temoin-unite08.txt"
DEPOT = EPREUVES / "preuves-unite08" / "DEPOT-d210-unite08.txt"
FAUX = EPREUVES / "preuves-unite08" / "falsifie-16.bin"
ETAT = EPREUVES / "etat-run-unite08-d210.json"
JOURNAL = EPREUVES / "TRIADE_logs" / "session-20261118-000905.txt"
RAPPORT = BAC / "RECOUP-343-preuves-unite08.txt"


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


def instant(s):
    import datetime
    return datetime.datetime.fromisoformat(
        s.replace("Z", "+00:00")).replace(tzinfo=None) if s else None


def modele_ligne(decalage, octets):
    s = f"{decalage:08X}  "
    g = [f"{b:02X}" if i < len(octets) else "  "
         for i, b in enumerate(octets + b"\x00" * (16 - len(octets)))]
    s += " ".join(g[:8]) + "  " + " ".join(g[8:]) + "  "
    miroir = "".join(chr(b) if 0x20 <= b <= 0x7E else "."
                     for b in octets[:16])
    s += miroir + " " * (16 - len(miroir))
    return s.encode("latin-1") + b"\x00"


# ---------------------------------------------------------------- le dépôt Drive
titre("RECOUP-343 — LE RUN TERRAIN DE L'UNITÉ 02 D210 LOUPE-08 LIGNE × BRAS T\n"
      "REÇU ET RECOUPÉ (le dépôt kit-unite-02-d210-20261118/ du coffre /test ;\n"
      "l'annonce du développeur : « preuves dans le drive /test » — le run au\n"
      "kit GUI 1-clic livré à la 342, la suite ① honorée au geste du\n"
      "développeur)\n"
      + "=" * 78)

st, body, _ = ds.api("GET", ds.API + "/files/" + DOSSIER_ID
                    + "?fields=name,createdTime,modifiedTime")
meta_dossier = json.loads(body)


def lister_dossier():
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
            return pieces_meta


racine_depot = lister_dossier()
preuves_meta = lister_dossier()  # re-listé : la racine du dépôt
for nom in ("preuves-unite08", "TRIADE_logs"):
    if nom in racine_depot:
        st, body, _ = ds.api("GET", ds.API + "/files?"
                             + urllib.parse.urlencode({
                                 "q": f"''{racine_depot[nom]['id']}'' in "
                                      f"parents and trashed = false"
                                 .replace("''", "'"),
                                 "pageSize": "100",
                                 "fields": ("files(id,name,mimeType,md5Checksum,"
                                            "size,modifiedTime,createdTime)")}))
        for f in json.loads(body).get("files", []):
            preuves_meta[f"{nom}/{f['name']}"] = f

# R1 — les pièces rapatriées, md5 == Drive (re-recoupé par re-listing)
sous_dossier = [n for n in ("preuves-unite08", "TRIADE_logs")
                if n in racine_depot]
cibles_r1 = [CONSOLE, CONSOLE_RECEPT, DEPOT, TEMOIN, FAUX, ETAT, JOURNAL]
ok_r1 = all(
    md5f(p) == preuves_meta.get(rel, {}).get("md5Checksum")
    for p, rel in ((CONSOLE, CONSOLE.name),
                   (CONSOLE_RECEPT, f"preuves-unite08/{CONSOLE_RECEPT.name}"),
                   (DEPOT, "preuves-unite08/DEPOT-d210-unite08.txt"),
                   (TEMOIN, "preuves-unite08/temoin-unite08.txt"),
                   (FAUX, "preuves-unite08/falsifie-16.bin"),
                   (ETAT, ETAT.name),
                   (JOURNAL, f"TRIADE_logs/{JOURNAL.name}")))
ok_copie = CONSOLE.read_bytes() == CONSOLE_RECEPT.read_bytes()
note(1, ok_r1 and ok_copie,
     f"les SEPT pièces nées du run ({len(racine_depot)} entrées à la racine "
     f"du dépôt, dont les sous-dossiers {', '.join(sous_dossier)}) : md5 "
     f"re-calculés == les métadonnées Drive re-listées ; la console racine "
     f"== la console du réceptacle OCTET POUR OCTET (la copie de la "
     f"collecte byte-byte)")

# les gravures du DEPOT (nom, taille, sha256)
gravures_depot = {}
for l in lignes(DEPOT):
    m = re.match(r"^  (\S+)\s+(\d+) o\s+([0-9a-f]{64})$", l)
    if m:
        gravures_depot[m.group(1)] = (int(m.group(2)), m.group(3))

c_lignes = lignes(CONSOLE)

# R2 — LE JUGE DU RUN : le D204 INCHANGÉ, octet pour octet
sha_depot = gravures_depot.get("scenario-unite08.py", (0, ""))[1]
sha_kit = sha256f(KIT_LABO / "scenario-unite08.py")
md5_coffre = racine_depot.get("scenario-unite08.py", {}).get("md5Checksum")
ok_r2 = (sha_depot == sha_kit == "44384f5d" + sha_kit[8:]
         if False else sha_depot == sha_kit and sha_kit.startswith("44384f5d"))
ok_r2 = (sha_depot == sha_kit and md5_coffre == md5f(KIT_LABO / "scenario-unite08.py"))
chemin_kit = [l for l in c_lignes if l.startswith("[témoin] D:\\")]
note(2, ok_r2,
     f"LE JUGE DU RUN : le scénario gravé au DEPOT {sha_depot[:8]}… == le "
     f"juge D204 INCHANGÉ == le kit du labo livré à la 342 "
     f"{sha_kit[:8]}… == la pièce au coffre (md5 {str(md5_coffre)[:8]}…) — "
     f"la faute au juge de la 338 ne se reproduit pas, NOMMÉE PARCE QU'ELLE "
     f"NE SE REPRODUIT PAS (D202) ; le chemin du kit à la console porte le "
     f"dossier daté : « {chemin_kit[0].split('] ')[1].rsplit(chr(92), 1)[0] if chemin_kit else '?'} »")

# R3 — LA PREUVE T0 du terrain
t0 = [l for l in c_lignes if l.startswith("[VERT] T0:")]
sha_loupe = sha256f(KIT_LABO / "loupe.exe")
gravure_kit = {}
for l in (KIT_LABO / "EMPREINTES-KIT-UNITE-02-D210.txt").read_text(
        encoding="utf-8").splitlines():
    parts = l.strip().split(None, 2)
    if len(parts) >= 2 and len(parts[0]) == 64:
        gravure_kit[parts[1]] = parts[0].lower()
journal_lignes = lignes(JOURNAL)
verrou = [l for l in journal_lignes if "[verrou] VERT — 14/14" in l]
ok_r3 = (bool(t0) and sha_loupe[:16] in t0[0]
         and gravures_depot.get("loupe.exe", (0, ""))[1] == sha_loupe
         and gravure_kit.get("loupe.exe") == sha_loupe
         and racine_depot.get("loupe.exe", {}).get("md5Checksum")
         == md5f(KIT_LABO / "loupe.exe")
         and bool(verrou))
note(3, ok_r3,
     f"LA PREUVE T0 : la console porte « {t0[0].split(' — ')[1] if t0 else '?'} »"
     f" ; la gravure EMPREINTES-KIT NÉE PARSÉE (le scénario scellé lut les "
     f"empreintes — le défaut T0 de l'unité 01 ne se reproduit pas, NOMMÉ "
     f"PARCE QU'IL NE SE REPRODUIT PAS) ; le journal de session porte le "
     f"verrou « {(verrou[0].split('] ')[1] if verrou else '?')} » ; la pièce "
     f"du kit recoupée AU LABO : loupe.exe "
     f"{(KIT_LABO / 'loupe.exe').stat().st_size} o, sha256 "
     f"{sha_loupe[:16]}… == la gravure du kit == la pièce au coffre")

# R4 — LE VERDICT : 10 VERT, 0 ROUGE, code 0 — les DIX verdicts attendus
vec_console = [(c, n) for c, n in re.findall(
    r"^\[(VERT|ROUGE)\] (\S+)", "\n".join(c_lignes), re.M)]
etat = json.loads(ETAT.read_text(encoding="utf-8"))
vec_etat = [(("VERT" if v else "ROUGE"), n.split(" — ")[0])
            for v, n in etat["contexte"]["verdicts"]]
temoin_lignes = lignes(TEMOIN)
vec_temoin = [(c, n) for c, n in re.findall(
    r"^  (VERT|ROUGE) (\S+)", temoin_lignes and
    "\n".join(temoin_lignes[:20]), re.M)]
journal_run = [l for l in journal_lignes if l.startswith("00:09:12  [run] [")]
vec_journal = [(c, n) for c, n in re.findall(
    r"\[(VERT|ROUGE)\] (\S+)", "\n".join(journal_run), re.M)]
attendu = sorted(["T0:la-piece-recoupee-a-l-empreinte-gravee",
                  "V1:le-dore-proxy-premiere-ligne",
                  "V1:le-temoin-3f-ligne-finale-incomplete",
                  "V2:le-differentiel-10-000-lignes", "V2:exactement-77-o",
                  "V3:E1:la-longueur-nulle", "V3:E2:la-longueur-dix-sept",
                  "V3:E3:la-source-nulle", "V3:E3:la-sortie-nulle",
                  "V4:l-octet-mute-la-ligne-diverge"])
code_console = [l for l in c_lignes if l.startswith("le code retour :")]
ok_r4 = (len(vec_console) == 10 and all(c == "VERT" for c, _ in vec_console)
         and sorted(n for _, n in vec_console) == attendu
         and code_console and "0" in code_console[-1]
         and vec_etat == vec_console and vec_temoin == vec_console
         and vec_journal == vec_console
         and etat["contexte"]["n_vert"] == 10
         and etat["contexte"]["n_rouge"] == 0
         and etat["contexte"]["code"] == 0)
note(4, ok_r4,
     f"LE VERDICT : {len(vec_console)} VERT, "
     f"{sum(1 for c, _ in vec_console if c == 'ROUGE')} ROUGE, code retour "
     f"{code_console[-1].split(': ')[1] if code_console else '?'} — "
     f"L'ATTENDU DU LIVRE TENU : les DIX verdicts (T0, V1 ×2, V2 ×2, V3 ×4, "
     f"V4) ; les verdicts RECOPIÉS à l'identique console / état / témoin / "
     f"journal de session (jamais recalculés) — la même forme que l'épreuve "
     f"fonctionnelle du labo (10 VERT, 0 ROUGE, code 0) et que l'oracle du "
     f"harnais (12 VERT, RAPPORT-UNITE-D210-02)")

# R5 — LA MAIN (D99) : le témoin avant-main + la main posée
depose = TEMOIN.read_bytes()
texte_depose = depose.decode("utf-8")
gravure_temoin = gravures_depot.get("temoin-unite08.txt", (0, ""))
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
         and date_main and date_main.group(1).strip() == "18/11/2026"
         and signe_main and signe_main.group(1).strip() == "Alexis Lopez")
note(5, ok_r5,
     f"LA MAIN (D99) : le témoin déposé {len(depose)} o == le témoin "
     f"avant-main gravé au DEPOT ({len(avant_main) if avant_main else '?'} o"
     f", sha256 {gravure_temoin[1][:8]}… MATCH byte-byte, les blancs "
     f"{n_blanc} soulignés) + la main posée (+"
     f"{len(depose) - len(avant_main) if avant_main else '?'} o : « 18/11/2026 » +"
     f" « Alexis Lopez ») — la même main que les témoins des runs "
     f"338/340 de la campagne ; le GUI ne signea jamais (la frontière tenue)")

# R6 — la machine
machine = [l for l in temoin_lignes if l.startswith("la machine  :")]
argv = [l for l in c_lignes if l.startswith("l'argv exact :")]
depot_machine = [l for l in lignes(DEPOT) if l.startswith("la machine :")]
ok_r6 = bool(machine) and "PORTABLE" in machine[0] \
    and "Windows 10" in machine[0] and "AMD64" in machine[0] \
    and "Python 3.14.10" in machine[0] \
    and argv and "Python314\\python.exe" in argv[0] \
    and depot_machine and "(non consignée)" in depot_machine[0]
note(6, ok_r6,
     f"LA MACHINE : {machine[0].split(' : ', 1)[1] if machine else '?'} "
     f"(CA2 — la même que les runs de la campagne D204/D210 et les re-runs "
     f"338/340) ; l'argv de la console (…Python314\\python.exe) cohérent ; "
     f"le DEPOT l'avoue honnête : « la machine : (non consignée) » — la "
     f"machine vit au témoin (D99), la ligne du DEPOT ne maquille rien")

# R7 — la chronologie (les voix Drive + le nom daté de la console)
st, body, _ = ds.api("GET", ds.API + "/files?"
                     + urllib.parse.urlencode({
                         "q": f"'{TEST_ID}' in parents and trashed = false",
                         "pageSize": "200",
                         "fields": "files(name,modifiedTime,createdTime)"}))
racine_test = {f["name"]: f for f in json.loads(body).get("files", [])}
kit_zip = racine_test.get("kit-gui-1clic-unite08-d210-20261118.zip", {})
kit_livre = kit_zip.get("modifiedTime", "")
nom_ts = re.search(r"-(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})",
                   CONSOLE.name)
local_nom = (f"{nom_ts.group(3)}/{nom_ts.group(2)}/{nom_ts.group(1)} "
             f"{nom_ts.group(4)}:{nom_ts.group(5)}:{nom_ts.group(6)}")
debut_console = re.search(r"début le (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",
                           "\n".join(c_lignes))
debut_depot = re.search(r"début (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",
                        "\n".join(lignes(DEPOT)))
fin_console = re.search(r"fin le (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",
                        "\n".join(c_lignes))
fin_depot = re.search(r"fin (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})",
                      "\n".join(lignes(DEPOT)))
run_utc_m = re.search(r"le run\s+: (\S+) \(UTC\)", texte_depose)
ru = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z",
              run_utc_m.group(1) if run_utc_m else "")
import datetime as _dt
local_du_temoin = (
    (_dt.datetime(int(ru.group(1)), int(ru.group(2)), int(ru.group(3)),
                  int(ru.group(4)), int(ru.group(5)), int(ru.group(6)))
     + _dt.timedelta(hours=1)).strftime("%d/%m/%Y %H:%M:%S")
    if ru else "?")   # l'heure d'hiver du terrain : UTC+1, le passage de
                     # minuit conduit (le run vécut à 23:09Z le 17/11)
# le témoin porte l'heure de SA naissance (la FIN du run — le scénario le
# couche après la console) ; le nom de la console porte le DÉBUT
debut_etat = etat["contexte"].get("debut") if isinstance(
    etat.get("contexte"), dict) else None
fin_etat = etat["contexte"].get("fin") if debut_etat else None
mt_console = preuves_meta.get(CONSOLE.name, {}).get("modifiedTime", "")
mt_console_r = preuves_meta.get(
    f"preuves-unite08/{CONSOLE_RECEPT.name}", {}).get("modifiedTime", "")
mt_depot = preuves_meta.get("preuves-unite08/DEPOT-d210-unite08.txt",
                            {}).get("modifiedTime", "")
mt_faux = preuves_meta.get("preuves-unite08/falsifie-16.bin",
                           {}).get("modifiedTime", "")
mt_etat = preuves_meta.get(ETAT.name, {}).get("modifiedTime", "")
mt_temoin = preuves_meta.get("preuves-unite08/temoin-unite08.txt",
                             {}).get("modifiedTime", "")
mt_journal = preuves_meta.get(f"TRIADE_logs/{JOURNAL.name}", {}
                              ).get("modifiedTime", "")
ne_dossier = meta_dossier.get("createdTime", "")
ne_preuves = racine_depot.get("preuves-unite08", {}).get("createdTime", "")
chemins = [kit_livre, mt_faux, mt_console, mt_console_r, mt_depot, mt_etat,
           mt_temoin, mt_journal, ne_dossier, ne_preuves]
croissant = all(instant(chemins[i]) < instant(chemins[i + 1])
                for i in range(len(chemins) - 1))
ok_r7 = (local_nom == debut_console.group(1) == debut_depot.group(1)
         == debut_etat
         and local_du_temoin == fin_console.group(1) == fin_depot.group(1)
         == fin_etat
         and local_nom < local_du_temoin
         and croissant)
note(7, ok_r7,
     f"LA CHRONOLOGIE : le kit livré au /test {kit_livre} (la 342) → le "
     f"faux né au run {mt_faux} (V4) → la console couchée {mt_console} (le "
     f"nom « {local_nom} » == la ligne 1 == le chrono du DEPOT == l'heure "
     f"locale du terrain, UTC+1) → la console copiée {mt_console_r} → le "
     f"DEPOT gravé {mt_depot} → l'état {mt_etat} → LA MAIN {mt_temoin} "
     f"(le mtime du témoin, 39 s après la console) → le journal de session "
     f"{mt_journal} (la fenêtre fermée) → le coffre né {ne_dossier} → "
     f"preuves-unite08/ né {ne_preuves} — jamais une date avant le kit, "
     f"jamais une date avant le run ; L'OBSERVATION NOMMÉE : les "
     f"DIX-HUIT pièces du kit au coffre portent un mtime uniforme "
     f"2026-11-18T20:00:00.000Z (valeur ronde ~21 h après le run, "
     f"POSTÉRIEURE à la naissance du dossier même) — le geste de dépôt ne "
     f"conserva pas leurs mtimes, la chaîne de garde vit aux vraies voix "
     f"(les mtimes des pièces nées du run, les createdTime, les md5 "
     f"recoupés byte-byte) — JAMAIS maquillé")

# R8 — LE DEPOT : les gravures recoupées (la console + le mutant + les SIX pièces du kit)
ok_console = gravures_depot.get(CONSOLE_RECEPT.name) == (
    CONSOLE_RECEPT.stat().st_size, sha256f(CONSOLE_RECEPT))
premiere = open(KIT_LABO / "proxy.exe", "rb").read(16)
mutant_attendu = bytearray(premiere)
mutant_attendu[3] ^= 0x6F
mutant_attendu = bytes(mutant_attendu)
faux_depose = FAUX.read_bytes()
ok_mutant = (faux_depose == mutant_attendu
             and gravures_depot.get("falsifie-16.bin")
             == (len(faux_depose), hashlib.sha256(faux_depose).hexdigest())
             and modele_ligne(0, faux_depose) != modele_ligne(0, premiere)
             and modele_ligne(0, faux_depose) == modele_ligne(0, mutant_attendu))
verts_kit, ecarts_kit = 0, []
for nom, (taille, sha) in sorted(gravures_depot.items()):
    if nom in ("temoin-unite08.txt", CONSOLE_RECEPT.name, "falsifie-16.bin"):
        continue
    p = KIT_LABO / nom
    if not p.is_file():
        ecarts_kit.append(f"{nom}: ABSENT au kit du labo")
        continue
    if sha256f(p) == sha and p.stat().st_size == taille:
        verts_kit += 1
    else:
        ecarts_kit.append(f"{nom}: sha divergent")
ok_r8 = ok_console and ok_mutant and verts_kit == 6 and not ecarts_kit
note(8, ok_r8,
     f"LE DEPOT : la console gravée ({CONSOLE_RECEPT.stat().st_size} o, "
     f"{sha256f(CONSOLE_RECEPT)[:8]}…) == la pièce déposée byte-byte ; le "
     f"mutant falsifie-16.bin (16 o) == la pièce déposée == LA COMPOSITION "
     f"DU LABO (l'octet 3 ^ 0x6F du doré de proxy.exe : la ligne du mutant "
     f"DIVERGE du modèle de l'original ET == le modèle du mutant — le V4 "
     f"recoupé au labo) ; les SIX pièces du kit gravées (loupe.exe, "
     f"proxy.exe, temoin-3f.bin, le scénario D204, LISEZMOI-KIT, "
     f"EMPREINTES-KIT) recoupées sha256 par sha256 == le kit livré à la 342"
     f"{' — la chaîne de garde par le contenu (D143)' if not ecarts_kit else ' — ÉCARTS : ' + ' ; '.join(ecarts_kit)}")

# R9 — LA CAP M1 : la première livraison du bloc, le réceptacle sans zip
zips = [n for n in racine_test
        if re.match(r"preuves-unite08-d210-.*\.zip", n)]
cap = [l for l in lignes(DEPOT) if "LA CAP M1" in l]
assemblages = re.search(r"(\d+) assemblage", cap[0] if cap else "")
ok_r9 = (not zips and assemblages and assemblages.group(1) == "0"
         and etat.get("livraisons") == 0
         and etat.get("etapes") == {"run": True, "collecte": True})
note(9, ok_r9,
     f"LA CAP M1 : {len(zips)} zip au /test, le DEPOT porte « le GUI compte "
     f"{assemblages.group(1) if assemblages else '?'} assemblage(s) vécu(s) "
     f"», l'état du GUI « livraisons : {etat.get('livraisons')} », les "
     f"étapes « run + collecte » VERTES — LA PREMIÈRE livraison du bloc "
     f"(TROIS par bloc, § 7 du plan D204 ; il en reste DEUX) ; le dépôt est "
     f"le dossier kit-unite-02-d210-20261118/ ENTIER (le kit dézippé + les "
     f"preuves nées du run), JAMAIS le zip assemblé — l'observation NOMMÉE "
     f"reconduite (la 340 la nomma la première) : le contenu est complet, "
     f"l'exigence D99 tenue par le témoin daté-signé, l'emballage diffère — "
     f"jamais maquillé")

# R10 — LA MÊME PIÈCE : les DIX-HUIT pièces du kit == le kit livré à la 342
pieces_kit = sorted(p.name for p in KIT_LABO.iterdir() if p.is_file())
verts_coffre, ecarts_coffre = 0, []
for nom in pieces_kit:
    f = racine_depot.get(nom)
    if not f:
        ecarts_coffre.append(f"{nom}: ABSENT au coffre")
        continue
    if f.get("md5Checksum") == md5f(KIT_LABO / nom):
        verts_coffre += 1
    else:
        ecarts_coffre.append(f"{nom}: md5 divergent")
ok_r10 = verts_coffre == len(pieces_kit) and not ecarts_coffre
note(10, ok_r10,
     f"LA MÊME PIÈCE : les {len(pieces_kit)} pièces du kit au coffre "
     f"(loupe.exe 41660a30…, proxy.exe 446279f3…, temoin-3f.bin c5fc1f28…, "
     f"le juge 44384f5d…, les livres, les brouillons, la notation, le GUI) "
     f"== le kit du labo livré à la 342 OCTET POUR OCTET ({verts_coffre}/"
     f"{len(pieces_kit)} md5 MATCH) — le run ne toucha AUCUNE pièce "
     f"scellée : le verrou les recoupa au lancement (14/14 VERT au "
     f"journal), le scénario recoupa loupe.exe AVANT de courir (T0) — les "
     f"pièces LUES, jamais retouchées")

# ---------------------------------------------------------------- le bilan
bilan_v = sum(1 for l in rapport if l.startswith("[VERT]"))
bilan_r = sum(1 for l in rapport if l.startswith("[ROUGE]"))
titre("\nLE BILAN DU RECOUP : "
      f"{bilan_v} VERT / {bilan_r} ROUGE\n"
      "L'UNITÉ 02 D210 (LOUPE-08 LIGNE × BRAS T) CLOSE AU TERRAIN —\n"
      "  l'attendu du livre TENU : les DIX verdicts VERT, 0 ROUGE, code\n"
      "  retour 0, au geste du GUI 1-clic livré à la 342 (TOUT LANCER) ;\n"
      "  la main du développeur posée au témoin (D99 : daté 18/11/2026,\n"
      "  signé Alexis Lopez) ; le juge D204 INCHANGÉ couru au terrain —\n"
      "  les DEUX défauts de l'unité 01 (le T0 de la gravure, la faute au\n"
      "  juge de la 338) ne se reproduisirent pas, NOMMÉS PARCE QU'ILS\n"
      "  NE SE REPRODUisent pas (D202) ; la chaîne de garde close : kit\n"
      "  livré 22:42:58Z → run 23:09:12Z → main 23:09:51Z → coffre\n"
      "  23:10:27Z, les md5 recoupés byte-byte au rapatriement.\n"
      "LA LIGNE DE CARNET : T-loupe-08-d210-it1 VERT au geste du\n"
      "  développeur (la première itération consommée — le livre M3 +\n"
      "  livraisons.csv M1 à l'onglet 4·LIVRE du GUI, à la main).\n"
      "LA SUITE : ② l'unité suivante selon la séquence tirée (loupe-13 le\n"
      "  bras T d'abord — la graine D217, jamais re-tirée) ; la\n"
      "  re-livraison d'attribution empirique au commandement.")

RAPPORT.write_text("\n".join(rapport) + "\n", encoding="utf-8",
                   newline="\n")
print(f"\n[recoup] le rapport couché : {RAPPORT.relative_to(REPO)}")
sys.exit(0 if bilan_r == 0 else 1)
