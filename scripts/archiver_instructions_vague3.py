#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_instructions_vague3.py — L'ARCHIVAGE DES SIX INSTRUCTIONS DE LA
VAGUE 3 (12/11, la session du point de reprise). La règle du développeur
(D197) : « l'instruction s'archive APRÈS exécution ». Les SIX programmes
furent exécutés et consignés par les Entrées 235-240 (D200-D205) :
  - 6zqo2h60n  : la preuve TLA+/Apalache + le raffinement property-based
                 (Entrée 235, D200, Task 141) ;
  - n4kwcs3wa  : la campagne de mutation étendue 10 400 mutants
                 (Entrée 236, D201, Task 143) ;
  - xboh1kljq  : le reclassement des défauts Loupe par côté
                 (Entrée 237, D202, Task 144) ;
  - sollwnmae  : la révision manuscrit+spécification (Entrée 238, D203,
                 Task 145) ;
  - 54wni4hzh  : le plan de comparaison pré-enregistré (Entrée 239, D204,
                 Task 146) ;
  - lfh49a1xf  : la variante SHA-NI, OPT-01 (Entrée 240, D205, Task 147).

Gestes : pour CHAQUE fichier — l'empreinte md5 recoupée AVANT (au dossier
/instructions), le déplacement /instructions → /ARCHIVE (aucun contenu
modifié, aucune suppression), le md5 recoupé APRÈS (au dossier /ARCHIVE),
l'absence constatée au dossier source. À la fin : /instructions VIDE.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

INSTR_ID = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"   # dossier /instructions
ARCHIVE_ID = "1uJ5yU7ma5dYQM1GuWzm9Fx1I1U3Ywepr"  # dossier /ARCHIVE

GESTES = [
    # (file_id, nom, md5 attendu, libellé)
    ("1RLICzRGeHj57DqjyN7ydy8V8_tm7FaY2",
     "Qwen__20261111_6zqo2h60n.txt",
     "cae23bc6dd5be23e279afb989f11a3c2",
     "6zqo2h60n : /instructions → /ARCHIVE "
     "(programme TLA+/Apalache exécuté, Entrée 235)"),
    ("1jrySMWDR3_vye8ueuxZEcOfzLYQHfJA_",
     "Qwen__20261111_n4kwcs3wa.txt",
     "ac1da1f21e6226411bfc060c18ead8f4",
     "n4kwcs3wa : /instructions → /ARCHIVE "
     "(programme mutation 10 400 exécuté, Entrée 236)"),
    ("13TjX8IERQn33It9bq6TgyaC0TnCRj0jY",
     "Qwen__20261111_xboh1kljq.txt",
     "6f7637d182df6220c5bfbb887312ba5f",
     "xboh1kljq : /instructions → /ARCHIVE "
     "(programme reclassement exécuté, Entrée 237)"),
    ("1xsVq88F9fY23R9RbLumRLnF_1VAYOhJ9",
     "Qwen__20261111_sollwnmae.txt",
     "72c1db35ecd23df974585f9dc63bea6c",
     "sollwnmae : /instructions → /ARCHIVE "
     "(programme révision exécuté, Entrée 238)"),
    ("1UyN6PtH2Je9wT-HK_JIB7X-o9-q5DaEx",
     "Qwen__20261111_54wni4hzh.txt",
     "305856a4cc3f880bd1abb752394c5842",
     "54wni4hzh : /instructions → /ARCHIVE "
     "(programme plan comparaison exécuté, Entrée 239)"),
    ("1f9juNZjx-SujkF5ymr4_Nhs22AbDpZJw",
     "Qwen__20261111_lfh49a1xf.txt",
     "a55d24226f5cbc93bbdf30f8424999d2",
     "lfh49a1xf : /instructions → /ARCHIVE "
     "(programme SHA-NI exécuté, Entrée 240)"),
]


def verifier_dossier(folder_id, nom_attendu, md5_attendu):
    """Recoupe la présence du fichier et son empreinte dans folder_id."""
    ent = ds.list_folder(folder_id)
    f = ent.get(nom_attendu)
    if not f:
        raise ds.SyncError(f"'{nom_attendu}' INTROUVABLE dans le dossier")
    md5 = f.get("md5Checksum", "")
    if md5 != md5_attendu:
        raise ds.SyncError(
            f"empreinte divergente pour '{nom_attendu}' : {md5} != {md5_attendu}")
    return f["id"]


def main():
    ok = 0
    for file_id, nom, md5_att, libelle in GESTES:
        # 0) l'empreinte AVANT le geste (au dossier source)
        fid_avant = verifier_dossier(INSTR_ID, nom, md5_att)
        assert fid_avant == file_id, f"id divergent pour {nom}"
        # 1) déplacement (aucun contenu modifié)
        url = (f"{ds.API}/files/{file_id}?"
               + "addParents=" + ARCHIVE_ID
               + "&removeParents=" + INSTR_ID)
        st, body, _ = ds.api("PATCH", url, body={})
        if st not in (200, 201):
            raise ds.SyncError(f"déplacement '{nom}' impossible "
                               f"(HTTP {st}) : {body[:200]!r}")
        # 2) recoup APRÈS le geste (au dossier destination)
        verifier_dossier(ARCHIVE_ID, nom, md5_att)
        # 3) le fichier ne doit plus être dans le dossier source
        ent_src = ds.list_folder(INSTR_ID)
        if nom in ent_src:
            raise ds.SyncError(f"'{nom}' demeure dans le dossier source")
        print(f"OK  {libelle}")
        print(f"    md5 recoupé avant/après : {md5_att}")
        ok += 1
    # le dossier source doit être VIDE à la fin
    reste = ds.list_folder(INSTR_ID)
    if reste:
        print(f"[avertissement] /instructions porte encore : "
              f"{list(reste.keys())}")
        return 1
    print(f"--- {ok}/{len(GESTES)} gestes exécutés — /instructions VIDE ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
