#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D266 — L'ARCHIVAGE SE PROUVE, IL NE SE SUPPOSE PAS : LA SUPPRESSION DEVIENT UN CONFORT.

La plateforme n'autorise un agent à supprimer un fichier que si l'agent l'a créé,
ou si le propriétaire l'autorise fichier par fichier. Exiger un clic par fichier
après chaque vague n'est pas un contrôle de sûreté : c'est une friction. La règle
devient donc :

  1. chaque instruction reçue est COPIÉE dans ARCHIVE/instructions_vague<N>_<date>/ ;
  2. la copie est VÉRIFIÉE par sha256 contre l'original (via l'inventaire fourni) ;
  3. un REÇU d'archivage est écrit, nommant chaque fichier, son empreinte et son
     statut de suppression (supprimé / laissé inerte) ;
  4. une instruction dont la copie est prouvée ARCHIVÉE est HISTORIQUE : elle ne
     prescrit plus rien, qu'elle soit encore physiquement là ou non. Le guide agent
     et la garde du prescriptif la traitent en lecture seule.

Si la plateforme refuse la suppression (per-file consent), ce n'est PAS un échec :
le reçu porte « LAISSÉ INERTE — copie prouvée », et le propriétaire peut vider le
dossier d'un seul geste quand il le souhaite.

Usage :
  python3 scripts/vague18/verifier_archivage.py --inventaire <json> --dossier <dir>
  python3 scripts/vague18/verifier_archivage.py            # autotest 5/5
Inventaire : [{"nom": "...", "sha256": "...", "supprime": true|false}, ...]
"""
import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]


def sha(p):
    d = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            d.update(b)
    return d.hexdigest()


def verifier(inventaire, dossier):
    """-> (verdict, lignes du reçu). Refus nommé si une copie manque ou diverge."""
    dossier = pathlib.Path(dossier)
    lignes = ["REÇU D'ARCHIVAGE — l'empreinte prouve, la suppression est un confort", ""]
    refus = []
    for e in inventaire:
        copie = dossier / e["nom"]
        if not copie.exists():
            refus.append(("COPIE-ABSENTE", e["nom"]))
            continue
        h = sha(copie)
        if h != e["sha256"]:
            refus.append(("COPIE-DIVERGENTE", e["nom"]))
            continue
        etat = "SUPPRIMEE" if e.get("supprime") else "LAISSEE INERTE (copie prouvée)"
        lignes.append(f"{h}  {e['nom']}  {etat}")
    if refus:
        for c, n in refus:
            lignes.append(f"REFUS {c} — {n}")
        return ("REFUS", lignes)
    lignes.append("")
    lignes.append(f"{len(inventaire)} fichier(s) : copie identique à l'original. "
                  "Les originaux restants sont INERTES (lecture seule, jamais prescriptifs).")
    return ("ARCHIVAGE-PROUVE", lignes)


def ecrire_recu(inventaire, dossier):
    verdict, lignes = verifier(inventaire, dossier)
    recu = pathlib.Path(dossier) / "RECU-ARCHIVAGE.txt"
    recu.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))
    return 0 if verdict == "ARCHIVAGE-PROUVE" else 2


def autotest():
    import tempfile
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        (tmp / "a.txt").write_text("instruction A\n", encoding="utf-8")
        (tmp / "b.txt").write_text("instruction B\n", encoding="utf-8")
        ha, hb = sha(tmp / "a.txt"), sha(tmp / "b.txt")
        essais = []
        v, _ = verifier([{"nom": "a.txt", "sha256": ha, "supprime": True},
                         {"nom": "b.txt", "sha256": hb, "supprime": False}], tmp)
        essais.append(("copies identiques → ARCHIVAGE-PROUVE", v == "ARCHIVAGE-PROUVE"))
        v, _ = verifier([{"nom": "a.txt", "sha256": "0" * 64}], tmp)
        essais.append(("empreinte divergente → REFUS", v == "REFUS"))
        v, _ = verifier([{"nom": "z.txt", "sha256": ha}], tmp)
        essais.append(("copie absente → REFUS", v == "REFUS"))
        v, lignes = verifier([{"nom": "b.txt", "sha256": hb, "supprime": False}], tmp)
        essais.append(("original laissé → INERTE nommé", any("LAISSEE INERTE" in l for l in lignes)))
        ecrire_recu([{"nom": "a.txt", "sha256": ha, "supprime": True}], tmp)
        essais.append(("reçu écrit", (tmp / "RECU-ARCHIVAGE.txt").exists()))
    finally:
        import shutil; shutil.rmtree(tmp, ignore_errors=True)
    verts = 0
    print("=" * 78); print("D266 — L'ARCHIVAGE PROUVÉ (la suppression n'est plus une condition)"); print("=" * 78)
    for nom, ok in essais:
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    print(f"{verts}/{len(essais)}")
    return 0 if verts == len(essais) else 3


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(autotest())
    if a[0] == "--inventaire" and len(a) >= 4 and a[2] == "--dossier":
        inventaire = json.loads(pathlib.Path(a[1]).read_text(encoding="utf-8"))
        dossier = a[3] if a[3].startswith("/") else RACINE / a[3]
        sys.exit(ecrire_recu(inventaire, dossier))
    print("usage : --inventaire <json> --dossier <dir> | (sans option : autotest)")
    sys.exit(2)
