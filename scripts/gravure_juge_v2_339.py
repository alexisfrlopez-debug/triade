#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gravure_juge_v2_339.py — LA GRAVURE DU KIT v2 (l'Entrée 339, la
correction commandée) : EMPREINTES-PIECES-RUN.txt régénérée au format
« sha256 en tête » QUE LE SCÉNARIO SCELLÉ PARSE (lire_empreintes :
split(None, 2), parts[0] == 64 hex) — la ligne du scénario porte LE
JUGE v2 RÉPARÉ (302fa3a1…, R_JOURNAL = 0xE4A0, la vérité du layout),
les QUATORZE autres pièces INCHANGÉES celles du kit v1 (D143 : le kit
v1 demeure au coffre, INTACT). Le BOM UTF-8 et les fins de ligne LF de
la gravure v1 sont conservés à l'octet près (seuls l'en-tête libre et
la ligne du scénario bougent)."""
import hashlib
import pathlib

V1 = pathlib.Path("/home/z/my-project/download/TRIADE_gui_unite02_d210_v1")
V2 = pathlib.Path("/home/z/my-project/download/TRIADE_gui_unite02_d210_v2")

ENTETE = """EMPREINTES-PIECES-RUN — LES PIÈCES DU RUN AU FORMAT DU SCÉNARIO SCELLÉ
(la gravure du kit GUI 1-clic, l'édition v2 du 18/11/2026 — LE JUGE
RÉPARÉ : le scénario scenario-unite02.py porte le juge v2 302fa3a1…
(R_JOURNAL = 0xE4A0, la vérité du layout D161 — la re-livraison de la
339, la cause des deux rouge du terrain nommée à la 338 : la faute au
juge, jamais à la pièce) ; il lit les gravures « sha256 en tête » ;
l'EMPREINTES-KIT du 17/11 portait « nom en tête » : le run terrain
aurait REFUSÉ à T0. La présente gravure porte LES QUINZE pièces du
kit au format parsé ; l'originale EMPREINTES-KIT-UNITE-01-D210.txt
demeure inchangée à ses côtés.)
"""

# LES QUINZE pièces (l'ordre de la gravure v1 — l'ordre alphabétique du
# kit du 17/11) : quatorze INCHANGÉES + le scénario v2
PIECES = [
    "GRAINE-D210.txt",
    "LANCEUR-UNITE-02-T.bat",
    "LISEZMOI-KIT-UNITE-01-D210.txt",
    "NOTE-REPRISE-ATELIER.txt",
    "brouillon-loupe-02-lire.asm",
    "journal-tokens-d210.jsonl",
    "loupe.exe",
    "notation-loupe-02-lire.asm",
    "scenario-unite02.py",
    "source-loupe-02-C.c",
    "temoin-1.bin",
    "temoin-384.bin",
    "temoin-3f.bin",
    "tests-loupe-02-C.md",
    "vide.bin",
]


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def main():
    # la gravure v1 relue : quatorze lignes doivent rester IDENTIQUES
    v1_texte = (V1 / "EMPREINTES-PIECES-RUN.txt").read_text(
        encoding="utf-8-sig")
    v1_lignes = {}
    for ligne in v1_texte.splitlines():
        parts = ligne.strip().split(None, 2)
        if len(parts) >= 2 and len(parts[0]) == 64:
            v1_lignes[parts[1]] = parts[0].lower()

    corps = []
    for nom in PIECES:
        attendu = v1_lignes.get(nom, "")
        if nom == "scenario-unite02.py":
            h = sha256f(V2 / nom)
            print(f"[gravure] {nom} : LE JUGE v2 {h[:16]}… "
                  f"(la v1 portait {attendu[:16]}…)")
        else:
            h = sha256f(V2 / nom)
            if h != attendu:
                raise SystemExit(
                    f"[REFUS] {nom} diverge de la gravure v1 — la pièce "
                    f"devait demeurer INCHANGÉE (D143)")
            print(f"[gravure] {nom} : INCHANGÉ {h[:16]}…")
        corps.append(f"{h}  {nom}")

    # BOM + LF + l'en-tête libre + une ligne vide + les quinze lignes
    contenu = ENTETE + "\n" + "\n".join(corps) + "\n"
    (V2 / "EMPREINTES-PIECES-RUN.txt").write_bytes(
        b"\xef\xbb\xbf" + contenu.encode("utf-8"))

    h_final = sha256f(V2 / "EMPREINTES-PIECES-RUN.txt")
    taille = (V2 / "EMPREINTES-PIECES-RUN.txt").stat().st_size
    print(f"[gravure] EMPREINTES-PIECES-RUN.txt v2 né : {taille} o, "
          f"sha256 {h_final}")
    print(f"[à reporter au GUI] gravure sha256 = {h_final}")

    # la preuve immédiate : le parseur DU SCÉNARIO LIVRÉ v2 (l'extraction
    # AST — la leçon de l'Entrée 286 : le code livré, pas sa copie)
    import ast
    src = (V2 / "scenario-unite02.py").read_text(encoding="utf-8")
    arbre = ast.parse(src)
    gardes = [n for n in ast.walk(arbre)
              if isinstance(n, ast.FunctionDef)
              and n.name == "lire_empreintes"]
    ns = {"os": __import__("os"), "ICI": str(V2)}
    exec(compile(ast.Module(body=gardes, type_ignores=[]),
                 "scenario-unite02.py", "exec"), ns)
    vues = ns["lire_empreintes"]()
    print(f"[preuve] lire_empreintes DU SCÉNARIO v2 LIVRÉ, exécuté sur le "
          f"kit v2 : {len(vues)} pièces vues, loupe.exe "
          f"{'recoupé' if vues.get('loupe.exe') == v1_lignes['loupe.exe'] else 'ÉCART'}")
    ok = len(vues) == 15 and vues.get("loupe.exe") == v1_lignes["loupe.exe"] \
        and vues.get("scenario-unite02.py") == sha256f(V2 / "scenario-unite02.py")
    print(f"[preuve] T0 {'VERT — le juge v2 voit LES QUINZE pièces' if ok else 'ROUGE'}")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
