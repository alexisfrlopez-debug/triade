#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_vague9.py — LA CAMPAGNE DE L'INSTRUCTION uagz3fby7 (la vague 9,
le PLAN-UAGZ3FBY7 gelé) : QUATRE cellules n=18, la graine 20261117, le
même ordre, le même instrument que la vague 8 (le CLI z-ai, le champ
usage LU, chaque appel journalisé — la reprise idempotente : le journal
fait foi).

LES CELLULES :
  éditer-H2   — la reproduction (la référence de la vague 8 : médiane
                2 452, réponse 40 — les mêmes tâches gelées, le format
                v2 TEL QUEL) ;
  ajouter-H3  — l'amendement v3 : la grammaire v2 + UN EXEMPLE COMPLET
                DE RÉPONSE D'AJOUT (la leçon de la vague 8 : le modèle
                re-dumpait le contexte — l'exemple ENSEIGNE la réponse
                attendue, la prose seule ne l'enseignait pas) ;
  composer-G  — LA NOUVELLE CELLULE (la bibliothèque de gabarits
                porteurs de preuves) : l'unité composée PAR HÉRITAGE
                SCELLÉ — le prompt porte LE CONTRAT + L'INDEX des
                appelés scellés du bloc (leurs signatures et leurs
                adresses du plan, LUS du graphe de dépendances) ; la
                réponse : la notation du bloc où CHAQUE appelé est un
                APPEL DIRECT à son adresse scellée (l'héritage R7 —
                jamais réécrit), le SOUL code nouveau seul écrit ;
  localiser-P — le pointeur seul (OPT-04 D222 : deux champs littéraux,
                le gabarit de la campagne cq01qv1za TEL QUEL).

LA CONFRONTATION : chaque réponse édit/compose confrontée par LE CLIENT
HUNKS v2 (appliquer, reconstruire, round-trip — les QUATRE refus nommés) ;
localiser confronté à la vérité-terrain (l'identifiant et l'empreinte
recopiés tels quels)."""
from __future__ import annotations

import json
import pathlib
import sys
import time

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
V8 = REPO / "atelier-opt05-pe6iv71fj"
sys.path.insert(0, str(V8))

from instrument_opt05 import appeler_et_compter  # noqa: E402
from client_hunks_v2 import traiter as traiter_v2, Refus  # noqa: E402
from campagne_opt05 import (gabarit_editer_hunk, GABARIT_BASE,  # noqa: E402
                            CONVENTIONS, FORMAT_HUNK)
from campagne_opt05 import charger as charger_v8

VT = REPO / "atelier-localiser-5gfx6pwkj" / "verites-terrain.json"
GRAPHE = REPO / "atelier-boucle-bkobf06nu" / "graphe_deps.json"
journal = V8 / "journal_tokens.jsonl"      # LE MÊME journal que
garde = V8 / "garde-brut.jsonl"             # l'instrument (la vague 8)
resultats = ICI / "resultats_vague9.jsonl"

# L'INDEX DES SCELLÉS (la bibliothèque de gabarits porteurs de preuves —
# les adresses du plan, les signatures des contrats I)
HERITAGES = {
    "libc-01": ("memcpy (dst, src, n) → la copie", 0x1100),
    "libc-02": ("memcmp (a, b, n) → la comparaison", 0x1180),
    "libc-07": ("memset (dst, octet, n) → le remplissage", 0x13C0),
    "win-03": ("la boucle de messages Windows", 0x15C0),
    "tls13-01": ("sha256-init (ctx 112 o) — FIPS 180-4", 0xC000),
    "tls13-02": ("sha256-comprimer (ctx, bloc 64 o)", 0xC080),
    "tls13-03": ("sha256-absorber (ctx, données, n)", 0xC400),
    "tls13-04": ("sha256-finaliser (ctx, sortie 32 o)", 0xC5C0),
}

# LE GABARIT COMPOSER — l'héritage scellé : l'index des appelés, le
# contrat, la réponse = la notation du bloc où les appelés sont des
# APPELS DIRECTS (le code nouveau seul écrit)
def gabarit_composer(contrat: str, appeles: list[tuple[str, str, int]],
                     exemple: str) -> str:
    index = "\n".join(
        f"  — {nom} @ 0x{adr:x} : {sig} — SCELLÉ (l'appel DIRECT à son "
        f"adresse, JAMAIS réécrit)" for nom, sig, adr in appeles)
    return (
        "L'OPÉRATION COMPOSER DE LA CARTE TRIADE (la bibliothèque de "
        "gabarits porteurs de preuves — l'unité se compose PAR HÉRITAGE "
        "SCELLÉ, R7 : les briques existantes sont APPELÉES à leurs "
        "adresses, jamais réécrites ; le code NOUVEAU seul s'écrit).\n\n"
        f"LE CONTRAT DE COUCHE I (mot pour mot) :\n{contrat}\n\n"
        f"L'INDEX DES APPELÉS SCELLÉS (les briques héritées du plan) :\n"
        f"{index}\n\n"
        f"{CONVENTIONS}\n"
        "L'EXEMPLE DU FORMAT DE NOTATION (loupe-13, la notation RÉELLE du "
        "domaine — le format à suivre EXACTEMENT : l'en-tête commenté, les "
        "adresses absolues, AUCUNE directive NASM, AUCUN label à "
        "deux-points, les appels aux adresses du plan — TES appelés "
        "hérités s'appellent ainsi : « call 0x1180 » pour libc-02) :\n"
        f"{exemple}\n\n"
        "REQUÊTE : compose LA NOTATION COMPLÈTE du bloc qui honore le "
        "contrat — chaque capacité héritée est UN APPEL DIRECT à l'adresse "
        "scellée de l'index (jamais la logique réécrite), le code nouveau "
        "seul est écrit. Rien d'autre.\n"
    )


# L'AMENDEMENT v3 — UN EXEMPLE COMPLET DE RÉPONSE D'AJOUT (la leçon de la
# vague 8 : le re-dump du contexte — l'exemple ENSEIGNE la réponse)
def gabarit_ajouter_h3(contrat: str, exemple: str) -> str:
    return (
        "L'OPÉRATION AJOUTER DE LA CARTE TRIADE (le mode HUNKS — l'unité se\n"
        "compose PAR HÉRITAGE du gabarit de famille : la réponse ne rend QUE\n"
        "les hunks, le client les applique au gabarit et confronte).\n\n"
        f"LE CONTRAT DE COUCHE I (mot pour mot) :\n{contrat}\n\n"
        f"{CONVENTIONS}\n"
        "L'EXEMPLE DU FORMAT DE NOTATION (loupe-13, la notation RÉELLE du\n"
        "domaine — le format des lignes « + » de tes hunks) :\n"
        f"{exemple}\n\n"
        f"{FORMAT_HUNK}\n"
        "UN EXEMPLE COMPLET DE RÉPONSE D'AJOUT (le bloc qui vérifie un "
        "tampon non vide et rend sa taille — la réponse ENTIÈRE, "
        "caractère pour caractère, telle que le client l'attend) :\n"
        "@@ hunk 1\n"
        "base: ; --- LE CORPS DU BLOC ICI ---\n"
        "+ test rcx, rcx\n"
        "+ jz 0x1234\n"
        "+ mov rax, rdx\n"
        "+ jmp 0x1250\n"
        "+ mov eax, -5\n"
        "+ jmp 0x1250\n"
        "@@ hunk 2\n"
        "base: add rsp, 0x20\n"
        "+ nop\n"
        "FIN-HUNKS\n"
        "(REMARQUE : la réponse ci-dessus est TOUTE la réponse — elle "
        "commence à « @@ hunk 1 » et finit à « FIN-HUNKS », AUCUNE ligne "
        "de la notation du gabarit n'est re-dumpée, AUCUNE explication.)\n"
        "REQUÊTE : compose le bloc et rends UNIQUEMENT les hunks qui "
        "insèrent le corps dans le gabarit — la première ligne de ta "
        "réponse est EXACTEMENT « @@ hunk 1 », la dernière exactement « "
        "FIN-HUNKS ».\n"
    )


def deja_faits() -> set:
    if not journal.exists():
        return set()
    faits = set()
    for ligne in journal.read_text(encoding="utf-8").splitlines():
        if ligne.strip():
            faits.add(json.loads(ligne)["tache"])
    return faits


def main() -> int:
    vt, taches = charger_v8()
    ordre = vt["ordre"]
    par_id = {b["id"]: b for b in vt["blocs"]}
    graphe = json.loads(GRAPHE.read_text(encoding="utf-8"))["aretes"]
    exemple = (REPO / "loupe/notation/loupe-13-recherche.asm").read_text(
        encoding="utf-8")

    # LES APPELÉS SCELLÉS DU DOMAINE LOUPE EUX-MÊMES (leurs adresses du
    # plan — la bibliothèque porte TOUT le scellé, pas seulement les familles)
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("lay_l_camp", REPO / "loupe" / "layout.py")
    _lay = _ilu.module_from_spec(_spec)
    sys.modules["lay_l_camp"] = _lay
    _spec.loader.exec_module(_lay)
    SIGS_LOUPE = {
        "loupe-01": "ouvrir (chemin) — la session ouverte",
        "loupe-02": "lire (décalage) — la fenêtre relue",
        "loupe-03": "fermer () — la session close",
        "loupe-04": "cadre () — le cadre de session né",
        "loupe-05": "sha256 (fenêtre, n) — le condensé SHA-256",
        "loupe-06": "md5 (fenêtre, n) — le condensé MD5",
        "loupe-07": "cumul (fichier, n) — les empreintes du panneau",
        "loupe-08": "ligne (données, n, sortie) — la ligne hex composée",
        "loupe-13": "recherche (fenêtre, n, motif, m, départ) — la première occurrence",
        "loupe-14": "suivant (…) — l'occurrence suivante",
        "loupe-15": "curseur (pas) — le curseur déplacé",
        "loupe-16": "saisie (touche) — l'octet saisi au journal",
        "loupe-17": "sauver () — le journal écrit au disque",
        "loupe-18": "quitter () — la sortie propre",
    }
    for _bid, (_rva, _slot) in _lay.SLOTS_LOUPE.items():
        _num = int(_bid[1:]) - 110000
        _nom = f"loupe-{_num:02d}"
        if _nom in SIGS_LOUPE:
            HERITAGES[_nom] = (SIGS_LOUPE[_nom], _rva)

    # l'index des appelés scellés par bloc (le graphe lu de la notation)
    def appeles_du(nom: str) -> list[tuple[str, str, int]]:
        cle = "-".join(nom.split("-")[:2])
        deps = graphe.get(cle, [])
        out = []
        for d in deps:
            if d in HERITAGES:
                sig, adr = HERITAGES[d]
                out.append((d, sig, adr))
        return out or [("libc-02", "memcmp (a, b, n)", 0x1180),
                       ("libc-01", "memcpy (dst, src, n)", 0x1100)]

    # LE GABARIT P (le pointeur seul — la campagne cq01qv1za TEL QUEL)
    GABARIT_P = (
        "L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le mode pointeur seul — "
        "la\n"
        "réponse tient en une ligne, le client expande le pointeur auprès "
        "de la\n"
        "carte et confronte l'empreinte aux octets réels).\n"
        "\n"
        "BLOC DE LA CARTE (entête lu du fichier même) :\n"
        "{entete}\n"
        "Empreinte notation : sha256:{empreinte}\n"
        "\n"
        "REQUÊTE : localise le bloc ci-dessus dans la carte et réponds AU "
        "FORMAT\n"
        "POINTEUR SEUL, une seule ligne exactement :\n"
        "IDENTIFIANT · sha256:<empreinte>\n"
        "— IDENTIFIANT : l'identifiant de bloc de la carte (la forme "
        "iNNNNNN de\n"
        "l'entête) ;\n"
        "— <empreinte> : l'empreinte sha256 recopiée TELLE QUELLE de la "
        "ligne\n"
        "« Empreinte notation » ci-dessus (64 hexadécimaux, aucun calcul).\n"
        "Rien d'autre.\n"
    )

    def empreinte_de(nom: str) -> str:
        import hashlib
        return hashlib.sha256(
            (REPO / "loupe/notation" / f"{nom}.asm").read_bytes()).hexdigest()

    cellules = [
        ("editer-H2", lambda nom: gabarit_editer_hunk(
            (REPO / "loupe/notation" / f"{nom}.asm").read_text(
                encoding="utf-8"),
            taches[nom]["consigne"])),
        ("ajouter-H3", lambda nom: gabarit_ajouter_h3(
            (REPO / "loupe/I" / f"{nom}.md").read_text(encoding="utf-8"),
            exemple)),
        ("composer-G", lambda nom: gabarit_composer(
            (REPO / "loupe/I" / f"{nom}.md").read_text(encoding="utf-8"),
            appeles_du(nom), exemple)),
        ("localiser-P", lambda nom: None),   # traité à part (le gabarit P)
    ]

    faits = deja_faits()
    for mode, fabrique in cellules:
        manquants = [bid for bid in ordre if f"{mode}-{bid}" not in faits]
        print(f"[{mode}] {len(manquants)} appel(s) à vivre (l'ordre de la "
              f"graine {vt['graine']})", flush=True)
        for bid in manquants:
            nom = par_id[bid]["nom"]
            tache = f"{mode}-{bid}"
            if mode == "localiser-P":
                entete = "\n".join(
                    (REPO / "loupe/notation" / f"{nom}.asm").read_text(
                        encoding="utf-8").splitlines()[:1])
                prompt = GABARIT_P.format(entete=entete,
                                          empreinte=empreinte_de(nom))
            else:
                prompt = fabrique(nom)
            try:
                texte, ligne = appeler_et_compter("T", "vague9", tache,
                                                  prompt)
            except Exception as e:
                print(f"  ÉCHEC API {tache}: {e}", flush=True)
                time.sleep(20)
                continue
            verdict = ""
            try:
                if mode == "editer-H2":
                    base = (REPO / "loupe/notation" /
                            f"{nom}.asm").read_text(encoding="utf-8")
                    _, detail = traiter_v2(base, texte)
                    verdict = f"APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
                elif mode in ("ajouter-H3",):
                    _, detail = traiter_v2(GABARIT_BASE, texte)
                    verdict = f"APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
                elif mode == "composer-G":
                    from client_hunks import round_trip, extraire_notation
                    ok, detail = round_trip(extraire_notation(texte))
                    verdict = ("ROUND-TRIP:OK" if ok else
                               f"ROUND-TRIP-DIVERGENT:{detail[:60]}")
                elif mode == "localiser-P":
                    ident = bid
                    emp = empreinte_de(nom)
                    voulu = f"{ident} · sha256:{emp}"
                    verdict = ("CONFORME (le pointeur exact)" if
                               texte.strip() == voulu else
                               f"DIVERGENT: {texte.strip()[:60]!r}")
            except Refus as e:
                verdict = f"REFUS {e.nom}: {e.detail[:80]}"
            except Exception as e:
                verdict = f"ERREUR: {str(e)[:80]}"
            with open(resultats, "a", encoding="utf-8") as f:
                f.write(json.dumps({"tache": tache, "mode": mode,
                                    "bloc": nom, "verdict": verdict,
                                    "tokens": ligne["total_tokens"],
                                    "prompt_tokens":
                                        ligne["prompt_tokens"],
                                    "completion_tokens":
                                        ligne["completion_tokens"]},
                                   ensure_ascii=False) + "\n")
            print(f"  {tache}: {ligne['total_tokens']} tokens — "
                  f"{verdict[:80]}", flush=True)
            faits.add(tache)
            time.sleep(6)
    print("LA CAMPAGNE VAGUE 9 : les quatre cellules visitées.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
