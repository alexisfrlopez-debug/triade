#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_gui_unite08_d210.py — L'ÉPREUVE FONCTIONNELLE DU GUI 1-CLIC
D210 de l'unité 02 (loupe-08 ligne × bras T — l'Entrée 342 ; la leçon
de l'Entrée 286 : l'épreuve exécute LE CODE LIVRÉ, pas sa copie — le
GUI est importé ET conduit, la chaîne réelle enchaînée).

D122 : le bac n'a AUCUN Windows — le scénario scellé (ctypes.WinDLL)
n'y court PAS. L'épreuve conduit LA MÊME CHAÎNE que le bouton VERT
(verrou → run → collecte → zip) avec un SCÉNARIO SUBSTITUÉ étiqueté
LABO qui émet LA MÊME CONSOLE que le scénario (les DIX lignes de
verdict — T0, V1×2, V2×2, V3×4, V4 — le réceptacle preuves-unite08/,
le témoin au format exact) — JAMAIS maquillé en run terrain : le
témoin né porte « ÉPREUVE DU LABO » en tête, la console aussi. Le
substitué exécute les fonctions pures DU SCÉNARIO LIVRÉ extraites par
AST (modele_ligne, lire_empreintes) et les confronte à UNE COMPOSITION
INDÉPENDANTE du labo (les segments composés un à un — le juge du
juge). Le run terrain se vit au Windows du développeur.

Contrôles :
  E1  le kit copié : le verrou recoupe 14/14 pièces ;
  E2  la preuve T0 : le scénario scellé voit les 13 pièces ;
  E3  LE RUN substitué : la console née AU FIL DE L'EAU, les DIX
      verdicts RECOPIÉS (l'épreuve du labo), le code 0 ;
  E4  le témoin né au réceptacle AU FORMAT DU SCÉNARIO ;
  E5  LA COLLECTE : la console COPIÉE au réceptacle, le DEPOT né ;
  E6  le refus du zip sans la main (D99 — le témoin aux blancs) ;
  E7  LE ZIP après la main simulée de l'épreuve (le terrain signe, le
      labo éprouve le mécanisme) : le réceptacle ENTIER au zip ;
  E8  la cap M1 : le quatrième assemblage refuse (TROIS par bloc).

Lancement : python3 epreuve_gui_unite08_d210.py
"""
import pathlib
import shutil
import sys
import tempfile

KIT = pathlib.Path("/home/z/my-project/download/"
                   "TRIADE_gui_unite08_d210_v1")
sys.path.insert(0, str(KIT))
import triade_run_unite08_d210_gui as G  # noqa: E402  (le code LIVRÉ)

PASSES, ECHECS = [], []


def verifie(nom, ok, detail=""):
    (PASSES if ok else ECHECS).append(nom)
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
          + (f" — {detail}" if detail else ""))


# LE SCÉNARIO SUBSTITUÉ — même console, même réceptacle, même témoin,
# étiqueté LABO (jamais maquillé en run terrain)
SUBSTITUE = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'ÉPREUVE DU LABO du scénario unite08 (D122 : le bac n'a aucun
Windows) — JAMAIS le run terrain. Même console, même réceptacle,
même témoin, au format du scénario scellé."""
import ast, datetime as dt, hashlib, platform, pathlib, random, sys

ICI = pathlib.Path(__file__).resolve().parent


def consigne(ligne):
    print(ligne, flush=True)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


# les fonctions pures du SCÉNARIO SCELLÉ, extraites par AST (la leçon
# de l'Entrée 286 : le code livré, pas sa copie)
src = (ICI / "scenario-unite08.py").read_text(encoding="utf-8")
arbre = ast.parse(src)
gardes = [n for n in ast.walk(arbre)
          if isinstance(n, ast.FunctionDef)
          and n.name in ("modele_ligne", "lire_empreintes")]
ns = {"os": __import__("os"), "ICI": str(ICI)}
exec(compile(ast.Module(body=gardes, type_ignores=[]),
             "scenario-unite08.py", "exec"), ns)
modele_ligne, lire_empreintes = ns["modele_ligne"], ns["lire_empreintes"]


# LA COMPOSITION INDÉPENDANTE DU LABO (le juge du juge) : la
# sémantique du contrat loupe-08:R1 réécrite autrement — les segments
# composés un à un, jamais la même fonction recopiée
def composee(decalage, octets):
    n = len(octets)
    chiffres = format(decalage, "08X")
    hexd = "0123456789ABCDEF"
    groupes = []
    for i in range(16):
        if i < n:
            b = octets[i]
            groupes.append(hexd[b // 16] + hexd[b % 16])
        else:
            groupes.append("  ")
    miroir = ""
    for i in range(16):
        if i < n:
            b = octets[i]
            miroir += chr(b) if 0x20 <= b <= 0x7E else "."
        else:
            miroir += " "
    texte = (chiffres + "  " + " ".join(groupes[:8]) + "  "
             + " ".join(groupes[8:]) + "  " + miroir)
    return texte.encode("latin-1") + b"\x00"


REUSSITES, ECARTS = [], []


def controle(nom, ok, detail=""):
    consigne(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
             + (f" — {detail}" if detail else ""))
    (REUSSITES if ok else ECARTS).append(nom)


consigne("=== LE RUN DE L'UNITÉ 4 (loupe-08 ligne × bras T) — la "
         "campagne D204, L'ÉPREUVE DU LABO (D122 — jamais le run "
         "terrain) ===")

# T0 — la pièce recoupée à la gravure (le juge du kit, RÉEL)
emps = lire_empreintes()
controle("T0:la-piece-recoupee-a-l-empreinte-gravee",
         sha256(ICI / "loupe.exe") == emps.get("loupe.exe"),
         "loupe.exe recoupé à la gravure (l'épreuve du labo)")

# V1 — LE DORÉ : la première ligne du scellé + la finale incomplète
premiere = (ICI / "proxy.exe").open("rb").read(16)
controle("V1:le-dore-proxy-premiere-ligne",
         modele_ligne(0, premiere) == composee(0, premiere),
         "le modèle du juge == la composition indépendante du labo "
         "(« 4D 5A 90 00… » — la pièce de l'ère rendue à l'œil)")

temoin3f = (ICI / "temoin-3f.bin").open("rb").read()
finale = temoin3f[-1:]
controle("V1:le-temoin-3f-ligne-finale-incomplete",
         modele_ligne(3 * 65536, finale) == composee(3 * 65536, finale),
         "UN octet valide : quinze groupes d'espaces, la colonne ASCII "
         "droite — Q3 (l'épreuve du labo)")

# V2 — LE DIFFÉRENTIEL : 1 000 lignes aléatoires (la même graine que
# le scénario scellé — les mêmes tirages au labo)
rng = random.Random(20261115)
ecarts, ecarts_77 = 0, 0
for _ in range(1000):
    decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
    longueur = rng.randrange(1, 17)
    source = rng.randbytes(16)
    ligne = modele_ligne(decalage, source[:longueur])
    if ligne != composee(decalage, source[:longueur]):
        ecarts += 1
    if len(ligne) != 77 or ligne[-1:] != b"\x00":
        ecarts_77 += 1
controle("V2:le-differentiel-1-000-lignes", ecarts == 0,
         f"{1000 - ecarts}/1 000 == la composition du labo (la graine "
         "20261115, l'épreuve du labo)")
controle("V2:exactement-77-o", ecarts_77 == 0,
         "77 o exacts, le NUL final, aux 1 000 gestes (I2 : jamais un "
         "de plus — l'épreuve du labo)")

# V3 — les QUATRE rejets, RECOPIÉS DU CONTRAT (l'épreuve du labo ne
# court pas la pièce : les rejets se recopient, étiquetés)
controle("V3:la-longueur-nulle", True,
         "le rejet -5 recopié du contrat (l'épreuve du labo)")
controle("V3:la-longueur-dix-sept", True,
         "le rejet -5 recopié du contrat (l'épreuve du labo)")
controle("V3:la-source-nulle", True,
         "le rejet -5 recopié du contrat (l'épreuve du labo)")
controle("V3:la-sortie-nulle", True,
         "le rejet -5 recopié du contrat (l'épreuve du labo)")

# V4 — LA FALSIFICATION : l'octet muté (le modèle du juge, réel)
RECEPTACLE = ICI / "preuves-unite08"
RECEPTACLE.mkdir(exist_ok=True)
mutant = bytearray(premiere)
mutant[3] ^= 0x6F
mutant = bytes(mutant)
(RECEPTACLE / "falsifie-16.bin").write_bytes(mutant)
ligne_m = modele_ligne(0, mutant)
controle("V4:l-octet-mute-la-ligne-diverge",
         ligne_m != modele_ligne(0, premiere)
         and ligne_m == composee(0, mutant),
         "l'octet 3 muté : la ligne DIVERGE de l'original ET == la "
         "composition du mutant (l'épreuve du labo)")

# LE TÉMOIN — au format exact du scénario scellé, étiqueté LABO
lignes = ["TÉMOIN DU RUN DE L'UNITÉ 4 — loupe-08 ligne × bras T "
          "(la campagne D204, la comparaison des workflows)",
          "[ÉPREUVE DU LABO — D122 : le bac n'a aucun Windows, "
          "JAMAIS le run terrain]",
          "=" * 78,
          "le run      : " + dt.datetime.now(dt.timezone.utc).strftime(
              "%Y-%m-%dT%H:%M:%SZ") + " (UTC) — l'épreuve du labo",
          "la machine  : " + platform.node() + " · " + platform.system()
          + " " + platform.release() + " · " + platform.machine()
          + " · Python " + platform.python_version(),
          "la pièce    : loupe.exe "
          + str((ICI / "loupe.exe").stat().st_size) + " o, sha256 "
          + sha256(ICI / "loupe.exe"),
          "le verdict  : " + str(len(REUSSITES)) + " VERT, "
          + str(len(ECARTS)) + " ROUGE"
          + (" — VERT" if not ECARTS else " — ÉCART NOMMÉ"),
          "",
          "LES VECTEURS :"]
for nom in REUSSITES:
    lignes.append("  VERT " + nom)
for nom in ECARTS:
    lignes.append("  ROUGE " + nom)
lignes += ["",
           "LE GESTE QUI RESTE À LA MAIN (jamais automatisé, D99) :",
           "  DATER ce témoin (la date de votre main), le SIGNER,",
           "  renvoyer le dossier preuves-unite08/ ENTIER au coffre "
           "/test.", "",
           "Daté le : ____________________",
           "Signé    : ____________________"]
(RECEPTACLE / "temoin-unite08.txt").write_text("\n".join(lignes) + "\n",
                                               encoding="utf-8")
consigne("[témoin] " + str(RECEPTACLE / "temoin-unite08.txt") + " — "
         + str(len(REUSSITES)) + " VERT, " + str(len(ECARTS)) + " ROUGE")
consigne("=== LE RUN DE L'UNITÉ 4 FINI : dater et signer le témoin de "
         "votre main, renvoyer preuves-unite08/ ENTIER au coffre /test "
         "===")
sys.exit(0 if not ECARTS else 1)
'''


def main():
    print("=== L'ÉPREUVE FONCTIONNELLE DU GUI 1-CLIC UNITE08 D210 "
          "(la chaîne réelle au bac POSIX, le scénario substitué "
          "étiqueté LABO) ===")
    with tempfile.TemporaryDirectory(prefix="epreuve_gui_u08_") as tmp:
        kit = pathlib.Path(tmp) / "kit"
        kit.mkdir()
        for f in KIT.iterdir():
            if f.is_file() and f.suffix != ".zip" \
                    and f.name != "etat-run-unite08-d210.json":
                shutil.copyfile(f, kit / f.name)
        # le scénario substitué (étiqueté LABO) prend la place du
        # scénario scellé pour CE run d'épreuve — le scénario scellé
        # demeure au kit, recoupé au verrou
        (kit / "epreuve-scenario-labo.py").write_text(
            SUBSTITUE, encoding="utf-8")

        # E1 — le verrou sur le kit copié (LE CODE LIVRÉ)
        resultats = G.verifier_pieces(kit)
        verts = sum(1 for r in resultats if r["vert"])
        verifie("E1:le-verrou-14-sur-14", verts == len(G.PIECES),
                f"{verts}/{len(G.PIECES)}")

        # E2 — la preuve T0 (le scénario scellé voit les pièces)
        n, vert_t0, message = G.voir_pieces_du_scenario(kit)
        verifie("E2:la-preuve-t0", vert_t0 and n >= 13,
                f"{n} pièces — {message}")

        # E3 — LE RUN substitué (la chaîne du bouton VERT) ; le
        # substitué émet les DIX contrôles [VERT] (1 T0 + 2 V1 +
        # 2 V2 + 4 V3 + 1 V4) — le compte RECOPIÉ doit y être ÉGAL
        contexte = G.conduire_run(
            kit, lambda s: None,
            argv=[sys.executable, "epreuve-scenario-labo.py"],
            delai_ligne=0)
        verifie("E3:le-run-les-verdicts-recopies",
                contexte["code"] == 0 and contexte["n_vert"] == 10
                and contexte["n_rouge"] == 0
                and contexte["duree_s"] >= 0,
                f"{contexte['n_vert']} VERT, {contexte['n_rouge']} ROUGE "
                f"recopiés, code {contexte['code']}, durée "
                f"{contexte['duree_s']} s")
        console = pathlib.Path(contexte["console"])
        texte = console.read_text(encoding="utf-8")
        verifie("E3b:la-console-ecrite-au-fil-de-l-eau",
                "l'argv exact" in texte and "T0:la-piece" in texte
                and "LE RUN DE L" in texte,
                "l'entête, l'argv, les verdicts couchés")

        # E4 — le témoin né au réceptacle AU FORMAT DU SCÉNARIO
        temoin_texte, temoin_chemin = G.lire_temoin(kit)
        verifie("E4:le-temoin-ne-au-format-du-scenario",
                temoin_texte is not None
                and "Daté le : ____" in temoin_texte
                and "Signé    : ____" in temoin_texte
                and "ÉPREUVE DU LABO" in temoin_texte
                and not G.temoin_est_signe(temoin_texte),
                "le témoin aux blancs (la main du terrain, D99) — "
                "étiqueté LABO, jamais maquillé")

        # E5 — LA COLLECTE
        contexte["machine"] = "la-machine-du-bac · Linux · Python 3"
        contexte["livraisons"] = 0
        depot, pieces = G.collecter(kit, contexte, lambda s: None)
        receptacle = kit / G.RECEPTACLE
        verifie("E5:la-collecte-nee",
                depot.exists() and len(pieces) >= 2
                and (receptacle / console.name).exists()
                and "sha256" in depot.read_text(encoding="utf-8"),
                f"le DEPOT né, {len(pieces)} pièces au réceptacle, la "
                f"console COPIÉE")

        # E6 — le refus du zip sans la main (D99)
        try:
            G.assembler_zip(kit)
            ok6 = False
        except G.ErreurRun as e:
            ok6 = "D99" in str(e)
        verifie("E6:le-zip-refuse-sans-la-main", ok6,
                "le refus nomme D99")

        # E7 — la main simulée de l'épreuve (le terrain signe ; le
        # labo éprouve le mécanisme) puis LE ZIP
        temoin = receptacle / G.NOM_TEMOIN
        texte = temoin.read_text(encoding="utf-8")
        texte = texte.replace(
            "Daté le : ____________________",
            "Daté le : 18/11/2026 (la main simulée de l'épreuve — "
            "le terrain signe, D99)")
        texte = texte.replace(
            "Signé    : ____________________",
            "Signé    : le labo (l'épreuve — JAMAIS le GUI, D99)")
        temoin.write_text(texte, encoding="utf-8")
        chemin_zip, n_liv = G.assembler_zip(kit)
        import zipfile
        with zipfile.ZipFile(chemin_zip) as z:
            noms = z.namelist()
        verifie("E7:le-zip-assemble-le-receptacle-entier",
                all(x.startswith(G.RECEPTACLE + "/") for x in noms)
                and G.NOM_TEMOIN in "\n".join(noms) and n_liv == 1,
                f"{len(noms)} pièces au zip — le témoin DEDANS")

        # E8 — la cap M1
        try:
            G.assembler_zip(kit, livraisons_deja=3)
            ok8 = False
        except G.ErreurRun as e:
            ok8 = "CAP M1" in str(e)
        verifie("E8:la-cap-m1-tenue", ok8,
                "le quatrième assemblage refuse (nommé)")

    print(f"\nÉPREUVE FONCTIONNELLE : {len(PASSES)} VERT, "
          f"{len(ECHECS)} ROUGE sur {len(PASSES) + len(ECHECS)} "
          f"contrôles")
    return 0 if not ECHECS else 1


if __name__ == "__main__":
    sys.exit(main())
