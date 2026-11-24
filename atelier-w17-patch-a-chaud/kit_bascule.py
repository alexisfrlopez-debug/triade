#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT FALSIFIABLE — LA BASCULE À CHAUD (atelier W17R2PAT, spécification § 7.1.1, D253).

Ce kit ne prétend RIEN mesurer au matériel. Il calcule ce que la PUBLICATION d'un
trampoline peut garantir, refuse ce qui n'est pas garantissable, et laisse les
essais multi-threads au métal (statut EN ATTENTE, jamais simulé).

Modèle :
  - un magasin simple est atomique si (naturellement aligné) ET (taille dans
    {1,2,4,8}) — Intel SDM vol. 3 § 8.1.1 ;
  - une publication de 16 octets n'est atomique que par LOCK CMPXCHG16B, sous
    CPUID.CMPXCHG16B ;
  - un magasin SSE/AVX de 16 octets n'est PAS atomique ;
  - quel que soit le magasin, la publication est REFUSÉE si un thread a RIP dans
    la plage remplacée (l'atomicité ne protège pas le décodeur).

Usage :
  python3 atelier-w17-patch-a-chaud/kit_bascule.py            # autotest complet
  python3 atelier-w17-patch-a-chaud/kit_bascule.py --json     # résultat machine
Sortie : 0 = tous les cas conformes ; 2 = un cas a rendu autre chose que l'attendu.
"""
import argparse
import json
import sys

MAGASINS_ATOMIQUES = (1, 2, 4, 8)


def publication_admise(taille, alignement, primitive, cmpxchg16b, rip_dans_plage):
    """-> (admise: bool, motif: str). Le motif ne cite jamais de valeur secrète."""
    if rip_dans_plage:
        return False, "refus: RIP d'un thread dans la plage remplacée (atomicité sans effet sur le décodeur)"
    if alignement <= 0 or taille % alignement != 0 or (1 << (taille.bit_length() - 1)) != taille:
        return False, "refus: taille non puissance de deux (aucun magasin simple atomique)"
    if primitive == "magasin":
        if taille in MAGASINS_ATOMIQUES and alignement >= taille:
            return True, "magasin simple naturel atomique"
        if taille in MAGASINS_ATOMIQUES:
            return False, "refus: adresse non alignée sur la taille du mot (alignement naturel requis)"
        return False, "refus: un magasin simple n'est pas atomique au-delà de 8 octets naturels"
    if primitive == "cmpxchg16b":
        if taille == 16 and alignement >= 16 and cmpxchg16b:
            return True, "LOCK CMPXCHG16B sur emplacement 16 octets aligné"
        if not cmpxchg16b:
            return False, "refus: CPUID.CMPXCHG16B absent sur ce profil"
        return False, "refus: CMPXCHG16B exige 16 octets et un alignement 16"
    if primitive == "sse":
        return False, "refus: un magasin SSE/AVX de 16 octets n'est pas architecturalement atomique"
    return False, "refus: primitive inconnue"


def etats(publication_ok, verif_ok):
    """La séquence des états ; tout état partiel non exécutable."""
    seq = ["0 préparé", "1 armé", "2 rendez-vous"]
    if not publication_ok:
        return seq + ["refus -> 0"]
    seq += ["3 publication", "4 invalidation", "5 vérification"]
    if not verif_ok:
        seq += ["R rollback (publié-mais-non-vérifié)"]
    else:
        seq += ["6 reprise"]
    return seq




# ---------------------------------------------------------------------------
# LES CINQ ALÉAS RÉSIDUELS DU RENDEZ-VOUS (atelier BHQG73GZH, la spec § 7.6)
# Chacun rend un refus NOMMÉ et laisse un invariant d'état : jamais d'état partiel.
# ---------------------------------------------------------------------------
PORTEE_REL32 = 2 ** 31 - 1  # le déplacement signé 32 bits : ±2 GiB


def aleas_rendez_vous(contexte):
    """-> (admis: bool, motif: str, invariant: str).

    contexte : threads_crees_pendant (bool), retours_pile_dans_plage (bool),
               delta_zone (octets signés), slot_reserve (bool), locks (liste)
    """
    if contexte.get("threads_crees_pendant"):
        return False, "refus: THREAD-CREE-PENDANT-RENDEZ-VOUS — un thread non vérifié est apparu", "aucun thread non énuméré"
    if contexte.get("retours_pile_dans_plage"):
        return False, "refus: RETOUR-PILE-DANS-PLAGE — l'atomicité du magasin ne protège pas un retour", "pile hors de la plage remplacée"
    if abs(int(contexte.get("delta_zone", 0))) > PORTEE_REL32:
        return False, "refus: HORS-PORTEE-REL32 — la zone de croissance est au-delà de ±2 GiB", "delta dans la portée du rel32"
    if not contexte.get("slot_reserve"):
        return False, "refus: SLOT-NON-RESERVE — les 16 octets alignés ne sont pas réservés au build", "slot réservé à la build (granularité R7)"
    if "patcheur" in contexte.get("locks", []):
        return False, "refus: LOCK-DETENU — un thread suspendu détient un verrou requis par le patcheur", "aucun verrou du patcheur détenu"
    return True, "rendez-vous admis", "threads énumérés, pile hors plage, delta porté, slot réservé, aucun verrou"


CAS_ALEAS = [
    ("rendez-vous nominal", dict(threads_crees_pendant=False, retours_pile_dans_plage=False,
                                 delta_zone=0, slot_reserve=True, locks=[]), True),
    ("thread créé pendant le rendez-vous", dict(delta_zone=0, slot_reserve=True, locks=[], threads_crees_pendant=True), False),
    ("retour de pile dans la plage remplacée", dict(delta_zone=0, slot_reserve=True, locks=[], retours_pile_dans_plage=True), False),
    ("rel32 hors portée (±2 GiB)", dict(delta_zone=PORTEE_REL32 + 1, slot_reserve=True, locks=[]), False),
    ("slot de 16 octets non réservé", dict(delta_zone=0, slot_reserve=False, locks=[]), False),
    ("verrou du patcheur détenu (deadlock SuspendThread)", dict(delta_zone=0, slot_reserve=True, locks=["patcheur"]), False),
]


CAS = [
    # (nom, kwargs, admise_attendue)
    ("mot de 8 octets aligné (E9 rel32 + 3 NOP)", dict(taille=8, alignement=8, primitive="magasin", cmpxchg16b=False, rip_dans_plage=False), True),
    ("mot de 8 octets NON aligné", dict(taille=8, alignement=4, primitive="magasin", cmpxchg16b=False, rip_dans_plage=False), False),
    ("trampoline de 12 octets au magasin simple (la promesse v0.15.x)", dict(taille=16, alignement=16, primitive="magasin", cmpxchg16b=True, rip_dans_plage=False), False),
    ("trampoline de 16 octets par LOCK CMPXCHG16B, CPUID présent", dict(taille=16, alignement=16, primitive="cmpxchg16b", cmpxchg16b=True, rip_dans_plage=False), True),
    ("le même sans CPUID.CMPXCHG16B", dict(taille=16, alignement=16, primitive="cmpxchg16b", cmpxchg16b=False, rip_dans_plage=False), False),
    ("magasin SSE de 16 octets", dict(taille=16, alignement=16, primitive="sse", cmpxchg16b=True, rip_dans_plage=False), False),
    ("publication avec RIP d'un thread dans la plage", dict(taille=8, alignement=8, primitive="magasin", cmpxchg16b=False, rip_dans_plage=True), False),
]


def autotest(comme_json=False):
    resultats, ok = [], 0
    for nom, kw, attendu in CAS:
        admise, motif = publication_admise(**kw)
        vert = admise is attendu
        ok += 1 if vert else 0
        resultats.append({"cas": nom, "attendu": attendu, "obtenu": admise, "motif": motif, "vert": vert})
    # la séquence d'états : publication refusée = jamais d'état 3
    seq_refus = etats(False, True)
    seq_ok = etats(True, True)
    seq_rollback = etats(True, False)
    invariants = {
        "refus sans publication": seq_refus[-1] == "refus -> 0",
        "succès jusqu'à la reprise": seq_ok[-1] == "6 reprise",
        "publié-mais-non-vérifié rollbacké": seq_rollback[-1].startswith("R rollback"),
    }
    ok += sum(1 for v in invariants.values() if v)
    for nom, ctx, attendu in CAS_ALEAS:
        admis, motif, invariant = aleas_rendez_vous(ctx)
        vert = admis is attendu
        ok += 1 if vert else 0
        resultats.append({"cas": nom, "attendu": attendu, "obtenu": admis, "motif": motif,
                          "invariant": invariant, "vert": vert})
    total = len(CAS) + len(invariants) + len(CAS_ALEAS)
    if comme_json:
        print(json.dumps({"resultats": resultats, "invariants": invariants, "ok": ok, "total": total,
                          "materiel": "EN ATTENTE DE RUN MATÉRIEL (≥ 2 machines) — aucun résultat annoncé"}, ensure_ascii=False, indent=1))
    else:
        for r in resultats:
            print(f"[kit-bascule] {'VERT' if r['vert'] else 'ROUGE'}  {r['cas']} — {r['motif']}")
        for nom, v in invariants.items():
            print(f"[kit-bascule] {'VERT' if v else 'ROUGE'}  invariant : {nom}")
        print(f"[kit-bascule] autotest {ok}/{total}")
        print("[kit-bascule] matériel : EN ATTENTE DE RUN MATÉRIEL (≥ 2 machines) — aucun résultat annoncé")
    return 0 if ok == total else 2


def main():
    p = argparse.ArgumentParser(description="Kit falsifiable de la bascule à chaud")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    sys.exit(autotest(a.json))


if __name__ == "__main__":
    main()
