# CELLULE DE SECOURS 5 — LE RUN EN UNE SEULE CELLULE (la demande du maître
# du 27/11 : « tu pourrais lancer le run toi même avec Colab CLI ? » portée
# au plus près du possible — la SONDE du labo fit foi : AUCUNE voie ne lance
# un run Colab à distance [pas de CLI Colab ; l'API Colab Enterprise du
# projet : 404, le service n'est pas activé] et le bac ne porte pas le
# modèle [4 Gio, la limite structurelle nommée aux plans gelés] — le geste
# compute ne peut partir QUE du poste réel). ALORS LA VOIE LA PLUS COURTE :
# UNE SEULE CELLULE court LES CINQ ÉTAPES du plan gelé PUIS dépose le zip de
# preuves au /test du coffre — le même moteur TEL QUEL, le même ordre que la
# GUI, chaque journal vit EN DIRECT ; un ROUGE ARRÊTE la marche (fail-closed)
# — un échec nommé vaut plus qu'un vert muet.
#
# L'USAGE : après la cellule 5 (le serving — clic droit sur la cellule 5 →
# « Exécuter l'objet avant l'exécution » porte les cellules 1 → 5 d'un seul
# geste ; la cellule 7 ne court PAS), colle la présente en NOUVELLE cellule
# sous la cellule 6, exécute — puis NE TOUCHE À RIEN : la campagne court
# (dizaines de minutes à ~2 heures au MODE-B sur T4), le journal vit en
# direct, au terme le zip vit au /test du coffre ET le labo est prévenu par
# le /test même. Le MODE-B (llama.cpp, le bord natif, nprobs 64) est porté —
# le mode conseillé au T4.
import hashlib
import pathlib
import shutil
import subprocess
import sys

MOTEUR = "/content/kit/moteur_campagne.py"
DOS_MOTEUR = "/content/kit"
CHEMIN_ENDPOINT = pathlib.Path("/content/endpoint_serving.txt")

try:
    COFFRE_TEST
except NameError:
    COFFRE_TEST = pathlib.Path("/content/drive/MyDrive/Triade/test")

if not pathlib.Path(MOTEUR).exists():
    raise SystemExit("CLI-ABSENT : aucun /content/kit/moteur_campagne.py — "
                     "la cellule 2 (le kit au coffre) d'abord.")
if not CHEMIN_ENDPOINT.exists():
    raise SystemExit("CLI-ABSENT : aucun /content/endpoint_serving.txt — "
                     "la cellule 5 (le serving) d'abord.")
if not COFFRE_TEST.exists():
    raise SystemExit(f"COFFRE-ABSENT : le dossier {COFFRE_TEST} n'est pas monté — "
                     "la cellule 2 (le montage du Drive) d'abord : sans coffre, "
                     "le zip de preuves n'aurait nulle part où vivre (le refus "
                     "vient AVANT la campagne, jamais deux heures après).")
endpoint = CHEMIN_ENDPOINT.read_text(encoding="utf-8").strip()
print(f"[RUN] l'endpoint lu du serving : {endpoint}")
print("[RUN] le coffre /test monté — la marche peut courir.\n")

ETAPES = [
    ("1 · Vérifier le kit (le manifeste)", ["--verifier-kit"]),
    ("2 · Le gate (la sonde du décodeur client)", ["--gate"]),
    ("3 · Le canari (la violation ordonnée refusée)",
     ["--canari", "--mode", "B", "--url", endpoint, "--nprobs", "64"]),
    ("4 · LA CAMPAGNE (éditer 18 + ajouter 18 + la seconde famille)",
     ["--campagne", "--mode", "B", "--url", endpoint, "--nprobs", "64"]),
    ("5 · Le zip de preuves", ["--zip"]),
]

for titre, arguments in ETAPES:
    print(f"\n[RUN] === L'ÉTAPE : {titre} ===", flush=True)
    code = subprocess.call([sys.executable, "-X", "utf8", MOTEUR] + arguments,
                           cwd=DOS_MOTEUR)
    if code != 0:
        raise SystemExit(f"[RUN] ROUGE (code {code}) — {titre}. La marche s'arrête "
                         "(fail-closed) ; le journal TEL QUEL ci-dessus nomme l'écart.")
    print(f"[RUN] VERT — {titre}", flush=True)

# ---- LE RETOUR AU COFFRE (le geste de la cellule 8 reconduit) ---------------
def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for morceau in iter(lambda: f.read(1 << 20), b""):
            h.update(morceau)
    return h.hexdigest()


zips = sorted(pathlib.Path("/content/kit").glob("preuves-campagne-*.zip"),
              key=lambda p: p.stat().st_mtime)
if not zips:
    raise SystemExit("ZIP-ABSENT : l'étape 5 vient pourtant de courir VERT et "
                     "aucun preuves-campagne-*.zip ne vit au kit — l'écart se "
                     "consigne au labo (le journal TEL QUEL ci-dessus).")
source = zips[-1]
destination = COFFRE_TEST / source.name
shutil.copy2(source, destination)
recoup = sha256f(destination) == sha256f(source)
empreinte = sha256f(source)
print(f"\n[retour] {source.name} ({source.stat().st_size} o)")
print(f"[retour] déposé à {destination}")
print(f"[retour] sha256 : {empreinte}")
if not recoup:
    raise SystemExit("RECOP-ROUGE : la pièce déposée diverge de la pièce du kit — re-déposer.")
print("[retour] recoupé byte-byte par relecture — VERT. Le labo lira les verdicts TELS QUELS.")
print("\n[RUN] LES CINQ ÉTAPES VERTES + LE RETOUR AU COFFRE — LE RUN EST CLOSE :")
print(f"[RUN] le zip de preuves vit au {COFFRE_TEST} ; les verdicts (tenue ou")
print("[RUN] manquée, jamais habillée) y sont portés TELS QUELS — le labo les lira.")
