#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sequestre_d183.py — L'OUTIL DE LA CÉRÉMONIE DE SÉQUESTRE D183 (le kit
préparé au laboratoire, SANS l'appliquer au coffre réel : le geste
appartient au développeur — D183, D87).

L'INSTRUMENT EXISTANT, JAMAIS UNE RÉÉCRITURE (la doctrine D185 : les
instruments existants comme tueurs et juges) : le partage est celui du
coffre CF2 — v06/coffre_cf2.py, decouper()/reconstituer(), GF(2^8) au
polynôme AES, le modèle D120 (D183 : « le partage Shamir à seuil — le
modèle CF2 D120 : 5 parts à seuil 3 »).

DEUX RÉGIMES, SÉPARÉS PAR CONSTRUCTION :

  --autotest   LE GESTE DU LABORATOIRE (exécuté au dépôt, consigné) : la
               preuve à froid de l'OUTIL sur une PHRASE DE TEST publique —
               les C(5,3) = 10 combinaisons de 3 parts reconstituent
               EXACTEMENT la phrase ; les C(5,2) = 10 paires sous le seuil
               rendent un déchet ≠ phrase (l'information-théorique en
               acte) ; LA FALSIFICATION (le rafraîchissement D219) : une
               part forgée (un octet muté) est REFUSÉE par la
               confrontation à l'empreinte de contrôle, le contrôle
               négatif honnête rendu VERT par la même porte ; le rapport
               AUTOTEST.txt est la pièce.

  --verifier <p1> <p2> <p3> <manifeste>   LA PREUVE FAIL-CLOSED (le geste
               du développeur, à SA machine hors-ligne) : reconstitue la
               phrase des TROIS parts, calcule son sha256, le confronte à
               l'empreinte de contrôle du manifeste — ÉGALITÉ exigée,
               tout écart est un REFUS nommé (part fausse, forgée ou
               corrompue), code de sortie 1. La phrase n'est jamais
               affichée. (La variante --reconstituer demeure : elle
               affiche le sha256 SANS confronter — la vérification à la
               main reste possible.)

  --ceremonie <fichier-phrase>   LE GESTE DU DÉVELOPPEUR (à SA machine
               hors-ligne, JAMAIS au bac à sable) : lit SA phrase, la
               découpe en 5 parts à seuil 3 (aléa os.urandom), écrit les
               parts dans des fichiers SÉPARÉS + le manifeste
               (empreintes sha256) + la liste de contrôle du retrait.
               L'outil REFUSE de supprimer quoi que ce soit : le retrait
               de la phrase en clair est un geste humain, listé, jamais
               automatisé.

Sortie : scripts/kit_ceremonie_d183/ (parts-1.txt … parts-5.txt au
ceremony time, manifeste-sequestre.txt, AUTOTEST.txt à l'autotest).
"""
from __future__ import annotations

import datetime
import itertools
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "v06"))

import coffre_cf2 as cf2  # noqa: E402  — l'instrument D120, tel quel

ICI = pathlib.Path(__file__).resolve().parent
N_PARTS, SEUIL = 5, 3          # D183 : 5 parts à seuil 3
PHRASE_TEST = b"PHRASE-DE-TEST-PUBLIQUE-NON-SECRETE-v0.13.0-D183"


def sha256_hex(b: bytes) -> str:
    import hashlib
    return hashlib.sha256(b).hexdigest()


def decouper_phrase(phrase: bytes) -> list[bytes]:
    """5 parts à seuil 3 par L'INSTRUMENT CF2 (D120), BLOC PAR BLOC :
    l'instrument partage exactement 32 octets (TAILLE_M, la clé maîtresse
    CF2) — la phrase (de longueur libre) est découpée en blocs de 32,
    chaque bloc partagé 5/3 par le MÊME instrument, et chaque part
    concatène ses tranches : part = [len_lo, len_hi, x] + tranches (la
    longueur ET l'indice x sont publics, ils seuls permettent la coupe et
    le Lagrange au rendu — jamais un secret)."""
    longueur = len(phrase)
    parts = [bytearray([longueur & 0xFF, (longueur >> 8) & 0xFF, i + 1])
             for i in range(N_PARTS)]
    for o in range(0, longueur, 32):
        bloc = phrase[o:o + 32].ljust(32, b"\x00")
        for i, (x, tranche) in enumerate(cf2.decouper(bloc, N_PARTS, SEUIL)):
            parts[i].extend(tranche)
    return [bytes(p) for p in parts]


def reconstituer_phrase(parts: list[bytes]) -> bytes:
    """Le miroir exact : chaque bloc de 32 reconstitué au seuil, l'indice
    x de chaque part voyant dans SON en-tête (un sous-ensemble garde ses
    x d'origine — jamais renuméroté), la longueur coupe le padding."""
    longueur = parts[0][0] | (parts[0][1] << 8)
    rendu = bytearray()
    n_blocs = (longueur + 31) // 32
    for b in range(n_blocs):
        frags = [(p[2], p[3 + 32 * b:3 + 32 * (b + 1)]) for p in parts]
        rendu.extend(cf2.reconstituer(frags))
    return bytes(rendu[:longueur])


def autotest() -> int:
    lignes = [
        "AUTOTEST DE L'OUTIL DE SÉQUESTRE D183 — la preuve à froid du geste "
        "du laboratoire",
        f"(phrase de test PUBLIQUE, {len(PHRASE_TEST)} octets ; le partage "
        "CF2 D120 : 5 parts à seuil 3 ; v06/coffre_cf2.py tel quel)",
        "",
    ]
    parts = decouper_phrase(PHRASE_TEST)
    controle = sha256_hex(PHRASE_TEST)   # l'empreinte que le manifeste porte
    ok = True
    # (a) les C(5,3) = 10 combinaisons au seuil reconstituent EXACTEMENT
    combinaisons = list(itertools.combinations(range(N_PARTS), SEUIL))
    for combo in combinaisons:
        rendu = reconstituer_phrase([parts[i] for i in combo])
        ok &= rendu == PHRASE_TEST
        lignes.append(f"  parts {combo} : "
                      f"{'EXACTE' if rendu == PHRASE_TEST else 'FAUX !'}")
    # (b) les C(5,2) = 10 paires SOUS le seuil rendent un déchet ≠ phrase
    for paire in itertools.combinations(range(N_PARTS), 2):
        rendu = reconstituer_phrase([parts[i] for i in paire])
        fuite = rendu == PHRASE_TEST or PHRASE_TEST[:8] in rendu
        ok &= not fuite
        lignes.append(f"  paire {paire} (sous le seuil) : "
                      f"{'DÉCHET (rien ne fuite)' if not fuite else 'FUITE !'}")
    # (c) une part seule ne porte aucune information
    lignes.append("  part seule : par construction GF(2^8) d'un degré 2, "
                  "aucune information (Shamir 1979) — la part 0 ci-dessous "
                  "est publiable :")
    lignes.append(f"    sha256(part-0) = {sha256_hex(parts[0])} "
                  "(une part sous le seuil ne révèle rien)")
    # (d) LA FALSIFICATION (le rafraîchissement D219) : une part forgée
    #     (un octet du corps muté) est REFUSÉE par la porte du manifeste —
    #     la même porte qui rend VERT le contrôle honnête. Le rejet est
    #     NOMMÉ, fail-closed : aucun « à peu près » ne passe.
    lignes += ["",
               "  LA FALSIFICATION (D219) — la porte de l'empreinte de "
               "contrôle confronte chaque reconstitution :"]
    for combo in [(0, 1, 2), (2, 3, 4)]:
        forge = bytearray(parts[combo[0]])
        forge[3 + 5] ^= 0x01          # un octet du corps du premier bloc
        rendu_f = reconstituer_phrase([bytes(forge)] + [parts[i] for i in combo[1:]])
        refuse = sha256_hex(rendu_f) != controle
        ok &= refuse
        lignes.append(f"    parts {combo} dont une FORGÉE (octet muté) : "
                      f"{'REFUSÉE — sha256 ≠ l’empreinte de contrôle' if refuse else 'ACCEPTÉE !'}")
    # (e) LE CONTRÔLE NÉGATIF HONNÊTE : la même porte rend VERT la bonne
    #     combinaison — la preuve que le REFUS vient de la falsification,
    #     pas d'une porte qui refuse tout.
    rendu_h = reconstituer_phrase([parts[0], parts[1], parts[2]])
    honnete = sha256_hex(rendu_h) == controle
    ok &= honnete
    lignes.append(f"    parts (0, 1, 2) honnêtes : "
                  f"{'VERT — sha256 == l’empreinte de contrôle' if honnete else 'ROUGE !'}")
    verdict = "VERT — l'outil est prouvé à froid" if ok else "ROUGE"
    lignes += ["", f"VERDICT : {verdict}",
               f"Exécuté le {datetime.datetime.now().isoformat(timespec='seconds')}",
               "LE COFFRE RÉEL N'A PAS ÉTÉ TOUCHÉ (aucune phrase réelle lue, "
               "aucun conteneur ouvert) — le kit attend le geste du "
               "développeur (D183 : la cérémonie exigée de bout en bout ; "
               "D219 : la transition préparée, le geste au développeur)."]
    (ICI / "AUTOTEST.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))
    return 0 if ok else 1


def ceremonie(fichier: pathlib.Path) -> int:
    phrase = fichier.read_bytes().strip()
    if not phrase:
        raise SystemExit("[D183] le fichier de phrase est vide")
    print("[D183] LA CÉRÉMONIE (le geste du développeur, machine hors-ligne)")
    print(f"[D183] phrase : {len(phrase)} octets — NE JAMAIS l'afficher")
    parts = decouper_phrase(phrase)
    horodatage = datetime.datetime.now().isoformat(timespec="seconds")
    manifeste = [
        "MANIFESTE DU SÉQUESTRE D183 — 5 parts à seuil 3 (CF2 D120)",
        f"ceremonie : {horodatage}",
        f"taille de la phrase : {len(phrase)} octets",
        f"empreinte de contrôle de la phrase (sha256) : {sha256_hex(phrase)}",
        "   (cette empreinte PERMET la vérification à froid SANS la phrase : "
        "comparez le sha256 du rendu de reconstitution à celui-ci)",
        "",
        "LE PLAN DE RÉPARTITION DES MÉDIAS (D183 : au moins DEUX hors nuage) :",
        "  part 1 → USB n°1 (hors nuage, chez le développeur)",
        "  part 2 → USB n°2 (hors nuage, lieu distinct)",
        "  part 3 → papier (hors nuage, coffre physique)",
        "  part 4 → tiers de confiance (hors nuage si possible)",
        "  part 5 → coffre Drive (la part seule est inerte sous le seuil)",
        "",
        "LES EMPREINTES DES PARTS (sha256) :",
    ]
    for i, p in enumerate(parts, 1):
        f = ICI / f"part-{i}.txt"
        f.write_text(p.hex() + "\n", encoding="utf-8")
        manifeste.append(f"  part-{i}.txt : {sha256_hex(p)}")
    manifeste += [
        "",
        "LA PREUVE DE RECONSTITUTION À FROID — AVANT TOUT RETRAIT :",
        "  1. sur une machine propre, reconstituez avec TROIS parts (par ex. "
        "1+2+3) :",
        "     python3 sequestre_d183.py --reconstituer part-1.txt part-2.txt "
        "part-3.txt",
        "  2. comparez le sha256 affiché à l'empreinte de contrôle "
        "ci-dessus : ÉGALITÉ EXIGÉE ;",
        "  3. répétez avec une AUTRE combinaison (par ex. 2+4+5) ;",
        "  4. SEULEMENT ALORS, le retrait de la phrase en clair (la liste de "
        "contrôle du LISEZMOI) ;",
        "",
        "LA LISTE DE CONTRÔLE DU RETRAIT (des gestes humains, jamais "
        "automatisés) :",
        "  [ ] la preuve de reconstitution passée DEUX fois ;",
        "  [ ] les 5 parts réellement réparties sur leurs médias (recoupées "
        "aux empreintes) ;",
        "  [ ] PHRASE-CONTROLE-COFFRE.txt retiré du dépôt git ;",
        "  [ ] PHRASE-CONTROLE-COFFRE.txt retiré de la racine du coffre "
        "Drive ;",
        "  [ ] l'entrée de journal consignée (append-only) : le séquestre "
        "vécu de bout en bout, D81 AMENDÉE ;",
        "  [ ] l'exercice de reconstitution périodique inscrit à l'agenda "
        "(les parts se dégradent : médias perdus, gardiens qui changent).",
        "",
        "L'OUTIL NE SUPPRIME RIEN : le retrait est un geste humain listé.",
    ]
    (ICI / "manifeste-sequestre.txt").write_text("\n".join(manifeste) + "\n",
                                                 encoding="utf-8")
    for i in range(1, N_PARTS + 1):
        print(f"[D183] part-{i}.txt écrit ({sha256_hex(parts[i-1])[:16]}…)")
    print("[D183] manifeste-sequestre.txt écrit — la preuve à froid AVANT "
          "tout retrait (le LISEZMOI pas à pas)")
    return 0


def reconstituer(fichiers: list[pathlib.Path]) -> int:
    parts = [bytes.fromhex(f.read_text(encoding="utf-8").strip())
             for f in fichiers]
    rendu = reconstituer_phrase(parts)
    print(f"[D183] reconstitution de {len(parts)} parts : "
          f"{len(rendu)} octets, sha256 = {sha256_hex(rendu)}")
    print("[D183] comparez à l'empreinte de contrôle du manifeste "
          "(la phrase n'est jamais affichée)")
    return 0


def verifier(fichiers: list[pathlib.Path], manifeste: pathlib.Path) -> int:
    """LA PREUVE FAIL-CLOSED (le rafraîchissement D219) : la reconstitution
    confrontée à l'empreinte de contrôle du manifeste — ÉGALITÉ exigée,
    tout écart un REFUS nommé (part fausse, forgée ou corrompue)."""
    import re as _re
    texte = manifeste.read_text(encoding="utf-8")
    m = _re.search(r"empreinte de contrôle de la phrase \(sha256\) : "
                   r"([0-9a-f]{64})", texte)
    if not m:
        print("[D183] REFUS — l'empreinte de contrôle est introuvable au "
              "manifeste (un manifeste qui ne dit pas quoi vérifier ne "
              "vérifie rien)")
        return 1
    controle = m.group(1)
    parts = [bytes.fromhex(f.read_text(encoding="utf-8").strip())
             for f in fichiers]
    rendu = reconstituer_phrase(parts)
    sha = sha256_hex(rendu)
    if sha == controle:
        print(f"[D183] VERT — {len(parts)} parts, {len(rendu)} octets : le "
              f"sha256 du rendu == l'empreinte de contrôle du manifeste")
        print("[D183] la phrase n'est pas affichée — la preuve est "
              "l'égalité des empreintes")
        return 0
    print("[D183] REFUS — le sha256 du rendu ≠ l'empreinte de contrôle : "
          "une part est fausse, forgée ou corrompue (le rejet est nommé, "
          "fail-closed ; essayez une autre combinaison de TROIS parts "
          "recoupées au manifeste)")
    return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == "--autotest":
        sys.exit(autotest())
    if sys.argv[1] == "--ceremonie" and len(sys.argv) == 3:
        sys.exit(ceremonie(pathlib.Path(sys.argv[2])))
    if sys.argv[1] == "--reconstituer" and len(sys.argv) >= 4:
        sys.exit(reconstituer([pathlib.Path(a) for a in sys.argv[2:]]))
    if sys.argv[1] == "--verifier" and len(sys.argv) == 6:
        sys.exit(verifier([pathlib.Path(a) for a in sys.argv[2:5]],
                          pathlib.Path(sys.argv[5])))
    raise SystemExit(__doc__)
