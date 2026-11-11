#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_edition_v150.py — LA LIVRAISON DE L'ÉDITION v0.15.0 AU COFFRE
(née de livrer_edition_v140.py) ET LA PREMIÈRE APPLICATION DE LA RÈGLE
D197 DU DÉVELOPPEUR (12/11) : « quand tu livres une nouvelle version
d'un document existant, archive les anciennes versions » — les QUINZE
livrables v0.10.0–v0.14.0 (complet/soumission/empreintes) passent
racine → /ARCHIVE par DÉPLACEMENT vérifié (md5 avant/après, aucune
suppression) ; la racine ne porte plus que les versions COURANTES.

Puis l'archivage de l'INSTRUCTION ic09ydeli (/instructions → /ARCHIVE,
md5 recoupé) : son programme (la v0.15.0) est EXÉCUTÉ, l'archive lui
est due — la règle du développeur : l'instruction s'archive APRÈS
exécution."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

LIVRABLES = [
    ("TRIADE_soumission_v0.15.0.zip",
     REPO / "download" / "edition_v0150" / "TRIADE_soumission_v0.15.0.zip"),
    ("TRIADE_complet_v0.15.0.zip",
     REPO / "download" / "edition_v0150" / "TRIADE_complet_v0.15.0.zip"),
    ("empreintes_livrables_v0.15.0.txt",
     REPO / "download" / "edition_v0150" / "empreintes_livrables.txt"),
]

# la règle D197 : les anciennes versions de CHAQUE document livré
ANCIENS = [f"TRIADE_complet_v0.{v}.0.zip" for v in ("10", "11", "12",
                                                    "13", "14")] \
    + [f"TRIADE_soumission_v0.{v}.0.zip" for v in ("10", "11", "12",
                                                   "13", "14")] \
    + [f"empreintes_livrables_v0.{v}.0.txt" for v in ("10", "11", "12",
                                                      "13", "14")]

INSTR_ID = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
FICHIER_INSTRUCTION = "Qwen_text_20261111_ic09ydeli.txt"


def upload_update_or_create(parent_id, chemin, nom):
    ent = ds.list_folder(parent_id)
    if nom in ent:
        ds.upload_update(ent[nom]["id"], chemin)
    else:
        ds.upload_create(parent_id, nom, chemin)


def deplacer(fichier, source_id, dest_id, libelle):
    """Le déplacement vérifié : md5 AVANT == md5 APRÈS, aucune
    suppression, échec si collision."""
    ent_src = ds.list_folder(source_id)
    f = ent_src.get(fichier)
    if not f:
        print(f"[deplacement] {fichier} INTROUVABLE dans {libelle[0]} "
              f"(déjà traité ?)")
        return False
    md5_avant = f.get("md5Checksum")
    ent_dest = ds.list_folder(dest_id)
    if fichier in ent_dest:
        print(f"[deplacement] REFUS : {fichier} existe déjà dans "
              f"{libelle[1]} (collision — traiter à la main)")
        return False
    url = (f"{ds.API}/files/{f['id']}?addParents={dest_id}"
           f"&removeParents={source_id}")
    st, corps, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        raise SystemExit(f"[deplacement] {fichier} impossible "
                         f"(HTTP {st}) : {corps[:200]!r}")
    md5_apres = ds.list_folder(dest_id).get(fichier, {}).get("md5Checksum")
    if md5_avant != md5_apres:
        raise SystemExit(f"[deplacement] ÉCART md5 pour {fichier} : "
                         f"{md5_avant} != {md5_apres}")
    print(f"[deplacement] {fichier} : {libelle[0]} -> {libelle[1]}, "
          f"md5 {str(md5_avant)[:8]}… recoupé")
    return True


def main():
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    archive_id = next(m["id"] for n, m in racine.items()
                      if m.get("mimeType") == ds.FOLDER_MIME
                      and n == "ARCHIVE")

    # 1. la livraison des livrables v0.15.0
    for nom, chemin in LIVRABLES:
        upload_update_or_create(ds.DRIVE_ROOT_ID, chemin, nom)
        racine = ds.list_folder(ds.DRIVE_ROOT_ID)
        md5_local = ds.md5_of(chemin)
        md5_distant = racine.get(nom, {}).get("md5Checksum")
        print(f"[livraison] {nom} : {chemin.stat().st_size} o, "
              f"md5 {md5_local[:8]}… / distant {str(md5_distant)[:8]}… "
              f"{'MATCH' if md5_local == md5_distant else 'ÉCART'}")
        if md5_local != md5_distant:
            raise SystemExit("[livraison] ÉCART md5")

    # 2. LA RÈGLE D197 : archiver les QUINZE anciens livrables
    archives = 0
    for ancien in ANCIENS:
        if deplacer(ancien, ds.DRIVE_ROOT_ID, archive_id,
                    ("racine", "ARCHIVE")):
            archives += 1
    print(f"[regle D197] {archives}/{len(ANCIENS)} anciens livrables "
          f"archivés")

    # 3. l'archivage de l'instruction ic09ydeli (programme EXÉCUTÉ)
    deplacer(FICHIER_INSTRUCTION, INSTR_ID, archive_id,
             ("/instructions", "ARCHIVE"))

    # 4. l'état final de la racine (les versions COURANTES seules)
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    livrables_racine = sorted(n for n in racine
                              if n.startswith(("TRIADE_complet",
                                               "TRIADE_soumission",
                                               "empreintes_livrables")))
    print(f"[etat final] livrables racine : {livrables_racine}")
    instr = ds.list_folder(INSTR_ID)
    print(f"[etat final] /instructions : {sorted(instr)} "
          f"({'VIDE' if not instr else 'NON VIDE'})")
    arch = ds.list_folder(archive_id)
    n_arch = len(arch)
    print(f"[etat final] ARCHIVE : {n_arch} fichiers")


if __name__ == "__main__":
    main()
