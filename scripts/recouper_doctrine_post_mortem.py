#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_doctrine_post_mortem.py — LA RECOUPURE POST-MORTEME PROMISE DES
TROIS DÉCISIONS D138 / D145 / D148 (la reprise de session M7 l'exigeait :
les trois décisions sont L'INSTRUMENT de tous les verdicts de run à venir —
D154 : l'instrument est lui-même soupçonnable, on le recoupe SUR PIÈCES).

Les pièces originales fondatrices, rapatriées du coffre /test/archives-preuves
(rapatrier_preuves_doctrine.py, md5 contrôlés) :

  preuves-run-v6 (28 pièces)  → D138 — la lecture virtualisée est aveugle ;
  preuves-run-e2 (7 pièces)   → D145 — aucune garde ne dépend d'une lecture
                                  en live d'un fichier en cours d'écriture ;
  preuves-run-v8 (ciblé : la matrice S3 + hosts — la revendication D148
                  « v6, v8, e4 : pièces identiques octet pour octet ») ;
  preuves-run-e4 (37 pièces)  → D148 — les verdicts se rendent post-mortem.

Chaque contrôle tranché binaire (PASS / ÉCHEC nommé, fail-closed) :
  A. les pièces présentes, md5 locaux == métadonnées Drive RE-LUES ;
  B. D138 sur pièces v6 : page-d2b 279 o + marqueur complet + identique
     v6/e4 ; l'étiquette auto-contradictoire « ECHEC … rc=0 » ; les lectures
     in-VM vides («  ») ; le renversement S2→S3 ; AUTORITE-B « arret propre
     — motif=delai » contre rc capturé vide ; AUTORITE-A jamais arrêtée
     (0 requête servie, pas de ligne d'arrêt) contre rc capturé vide ;
  C. D145 sur pièces e2 : le REFUS PROXY-SANS-ARMEMENT sur lecture 0 o ;
     la sonde TCP à 00:13:17 ; la pièce post-mortem 128 o / 7 lignes avec
     « relever-https arme » ; le contraste (le mécanisme fondateur) ;
     l'application e4 (garde FONCTIONNELLE + verdict POST-MORTEM) ;
  D. D148 sur pièces e4 : « ÉCHEC NOMMÉ (5) » ; les CINQ refus aux noms
     exacts ; le rc d'Edge capturé VIDE (quatre refus d'une seule cécité) ;
     dom-b.txt VIDE + nav-b.png ABSENTE ; la réception TRIPLEMENT recoupée
     (certificat rejete + s=34 + poignee refusee + ERR_HTTP_RESPONSE_CODE_
     FAILURE) ; la matrice S3 stationnaire v6/v8/e4 — d2a/d3/d5 + hosts-lu
     OCTET POUR OCTET, d2b SAUF LA LIGNE DATE (la précision nommée) ; le
     libellé « REGRESSION a nommer » (l'expectation périmée, SUR PIÈCE).

Si tout est vert : « RECOUP : VERT — les décisions D138/D145/D148 sont
FIDÈLES à leurs pièces originales ». Le verdict est écrit à côté des
pièces : download/recoup-post-mortem/VERDICT-recoup-doctrine.txt.

Usage : python3 scripts/recouper_doctrine_post_mortem.py
Code de sortie : 0 = recoup VERT ; 1 = écart nommé ; 2 = erreur fatale.
"""

import datetime
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DL = pathlib.Path("/home/z/my-project/download")
V6 = DL / "preuves-run-v6"
E2 = DL / "preuves-run-e2"
V8 = DL / "preuves-run-v8"
E4 = DL / "preuves-run-e4"
SORTIE = DL / "recoup-post-mortem"

V8_CIBLE = ["curl-d2a.txt", "curl-d2b.txt", "curl-d3.txt",
            "curl-d5.txt", "hosts-lu.txt"]

MARQUEUR_VIDE = "«  »"          # la lecture in-VM vide (guillemets, 2 espaces)


class Recoup:
    def __init__(self):
        self.lignes: list[str] = []
        self.ok = True

    def passe(self, nom: str, ok: bool, detail: str = "") -> bool:
        ok = bool(ok)
        self.ok = self.ok and ok
        self.lignes.append(f"[recoup-doctrine] {'PASS' if ok else 'ECHEC'} : {nom}"
                           + (f" ({detail})" if detail else ""))
        return ok


def md5f(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def texte(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8")


def lignes_de(p: pathlib.Path) -> list[str]:
    return texte(p).splitlines()


def aplatir(s: str) -> str:
    """Replie les fins de ligne en espaces simples — les pièces VERDICT
    wrapent leurs phrases (ex. « UNE WriteFile PAR\nLIGNE ») ; la matching
    se fait sur le texte aplati, jamais sur une graphie de wrap."""
    return " ".join(s.split())


def recontrole(r: Recoup, dossier: str, dest: pathlib.Path,
               attendus: list[str] | None = None) -> dict:
    """A : le dossier d'archives, les pièces locales md5 == coffre RE-LU."""
    test = ds.list_folder(TEST_ID)
    arch = ds.list_folder(test["archives-preuves"]["id"])
    d = arch.get(dossier)
    r.passe(f"A : {dossier} présent aux archives du coffre", bool(d),
            dossier)
    distants = ds.list_folder(d["id"])
    noms = (attendus if attendus is not None
            else sorted(n for n, m in distants.items()
                        if m.get("mimeType") != ds.FOLDER_MIME))
    for nom in noms:
        f = distants.get(nom)
        local = dest / nom
        r.passe(f"A : {dossier}/{nom} md5 == coffre",
                bool(f) and local.exists()
                and md5f(local) == (f.get("md5Checksum") or "").lower(),
                f"md5 {md5f(local)[:10]}…" if local.exists() else "ABSENTE")
    # le jeu local : toute pièce du coffre présente (contrôlée ci-dessus) ;
    # les extras locaux sont NOMMÉS — le seul légitime est le LISEZMOI du
    # réceptacle (posé avec les pièces au dépôt Task 61, jamais une pièce)
    extras = sorted(p.name for p in dest.iterdir() if p.is_file()
                    and p.name not in noms)
    r.passe(f"A : {dossier} — toute pièce du coffre présente localement, "
            f"les extras locaux nommés ({len(noms)} pièce(s))",
            set(noms) <= {p.name for p in dest.iterdir()}
            and set(extras) <= {"LISEZMOI-preuves.txt"},
            f"{len(noms)} pièce(s)"
            + (f" ; extra(s) NOMMÉ(S) : {extras}" if extras else ""))
    return {n: dest / n for n in noms}


# ---------------------------------------------------------------- D138 (v6)
def section_d138(r: Recoup) -> None:
    r.lignes.append("[recoup-doctrine] --- D138 : la lecture virtualisée est "
                    "aveugle (pièces v6) ---")
    jrn = lignes_de(V6 / "scenario-m5b-journal.log")
    vrd = texte(V6 / "VERDICT-run-v6-branche-S3.txt")

    # B1 — la pièce page-d2b : 279 o, marqueur complet, identique v6/e4
    p279 = V6 / "page-d2b.txt"
    r.passe("B1 : page-d2b.txt = 279 o EXACT + marqueur complet sur le "
            "disque hôte + identique v6/e4 (la MÊME page réelle)",
            p279.stat().st_size == 279
            and "TEMOIN-PAGE : TRIADE-M5B-PAGE-200" in texte(p279)
            and md5f(p279) == md5f(E4 / "page-d2b.txt"),
            f"{p279.stat().st_size} o, md5 {md5f(p279)[:10]}…")

    # B2 — l'étiquette auto-contradictoire ECHEC … rc=0 (le T2b réussi)
    contra = [l for l in jrn if "ECHEC DIAG-CURL-IP-SANS-REVOCATION" in l
              and "rc=0" in l]
    r.passe("B2 : l'étiquette « ECHEC … rc=0 » auto-contradictoire SUR "
            "PIÈCE (le T2b réussi étiqueté ÉCHEC)",
            len(contra) == 1,
            contra[0][11:96] if contra else "ABSENTE")

    # B3 — les lectures in-VM vides + le mauvais nommage S2 renversé en S3
    vides = sum(1 for l in jrn if MARQUEUR_VIDE in l)
    r.passe("B3 : les lectures in-VM VUES VIDES («  ») au journal + la "
            "branche S2 nommée À TORT, renversée S3 par le labo sur pièces",
            vides >= 2
            and any("diagnostic branche nommee : S2" in l for l in jrn)
            and "BRANCHE S3" in vrd
            and "renverse" in vrd,
            f"{vides} lecture(s) vide(s) ; S2→S3 renversé (VERDICT §3-4)")

    # B4 — AUTORITE-B : arrêt propre dans SA pièce, rc capturé vide au témoin
    log_b = texte(V6 / "autorite-b.log")
    r.passe("B4 : AUTORITE-B « arret propre … motif=delai » DANS SA PIÈCE "
            "tandis que le rc capturé reste vide (« recu »)",
            "arret propre" in log_b and "motif=delai" in log_b
            and "2 poignee(s) refusee(s)" in log_b
            and any("ECHEC AUTORITE-B-ARRET" in l and "recu" in l
                    for l in jrn),
            "arret propre — 0 requete(s) servie(s), 2 poignee(s) "
            "refusee(s) — motif=delai")

    # B5 — AUTORITE-A : jamais arrêtée (0 requête servie → Kill), rc vide
    log_a = texte(V6 / "autorite-a.log")
    r.passe("B5 : AUTORITE-A jamais arrêtée — SA pièce sans « requete "
            "servie » NI « arret propre » (0 servie → --arret-apres 1 "
            "jamais atteint → Kill) — rc capturé vide au témoin",
            "requete servie" not in log_a and "arret propre" not in log_a
            and any("ECHEC AUTORITE-A-ARRET" in l and "recu" in l
                    for l in jrn),
            f"pièce {len(log_a.splitlines())} ligne(s), aucun arrêt")
    r.lignes.append("[recoup-doctrine] NOTE B6 : les instances v2/v3 (« en "
                    "ecoute » à +1 s, vue 0 octet) sont des consignations "
                    "antérieures à D138 — leurs pièces vivent au coffre "
                    "(preuves-run-v2-depot1/2/3) ; le décompte « quatrième "
                    "instance » est PORTÉ PAR LA PIÈCE VERDICT v6 (§1 et §7) : "
                    + ("PRÉSENT" if "quatre fois désormais" in vrd
                       and "4e instance" in vrd else "ABSENT"))


# ---------------------------------------------------------------- D145 (e2)
def section_d145(r: Recoup) -> None:
    r.lignes.append("[recoup-doctrine] --- D145 : aucune garde ne dépend "
                    "d'une lecture en live (pièces e2) ---")
    jrn = lignes_de(E2 / "scenario-m5b-journal.log")
    vrd = texte(E2 / "VERDICT-run-e2-vues-vides.txt")
    pj = E2 / "proxy-journal.log"
    pj_lignes = lignes_de(pj)

    # C1 — le REFUS sur la garde en live (lecture 0 o d'un fichier vivant)
    r.passe("C1 : le REFUS PROXY-SANS-ARMEMENT SUR PIÈCE — la garde en "
            "live a lu 0 o (« journal : 0 o ») sous 20 s",
            any("REFUS PROXY-SANS-ARMEMENT" in l and "journal : 0 o" in l
                for l in jrn),
            "le run REFUSÉ, le navigateur jamais lancé")

    # C2 — la sonde TCP à 00:13:17 (l'écoute posée ⇒ bannière+armement déjà écrites)
    r.passe("C2 : la sonde TCP réussit à 00:13:17 SUR PIÈCE (l'écoute était "
            "posée — bannière et armement, qui la PRÉCÈDENT au contrat "
            "http-12:R3 Q3, étaient déjà écrites)",
            any(l.startswith("[2026-11-04T00:13:17Z]")
                and "proxy demarre" in l
                and "connect 127.0.0.1:25000 reussi" in l for l in jrn)
            and any(l.startswith("[2026-11-04T00:13:16Z]")
                    and "connect 127.0.0.1:443 reussi" in l for l in jrn),
            "00:13:16 (autorité A) + 00:13:17 (proxy)")

    # C3 — la pièce post-mortem : 128 o, 7 lignes, « relever-https arme »
    r.passe("C3 : la pièce post-mortem proxy-journal.log = 128 o EXACT, "
            "7 lignes EXACTES, ligne 2 « relever-https arme »",
            pj.stat().st_size == 128 and len(pj_lignes) == 7
            and pj_lignes[1] == "relever-https arme"
            and pj_lignes[0] == "TRIADE M3 : proxy demarre (port 25000)",
            f"{pj.stat().st_size} o, {len(pj_lignes)} lignes")

    # C4 — le contraste C1↔C3 = le mécanisme fondateur (0 o vivant / 128 o mort)
    vrd_aplati = aplatir(vrd)
    r.passe("C4 : le CONTRASTE SUR PIÈCES — le MÊME fichier lu 0 o TANT QUE "
            "LE PRODUCTEUR VIT, 128 o POST-MORTEM (le contenu n'apparaît "
            "qu'à la fermeture du handle) — le mécanisme fondateur de D145",
            "ZÉRO octet" in vrd_aplati
            and "7 lignes COMPLÈTES" in vrd_aplati
            and "UNE WriteFile PAR LIGNE" in vrd_aplati,
            "la pièce VERDICT e2 §4 le consigne mot pour mot (texte aplati)")

    # C5 — l'application e4 : la garde FONCTIONNELLE, le verdict POST-MORTEM
    jrn_e4 = lignes_de(E4 / "scenario-m5b-journal.log")
    r.passe("C5 : l'application e4 SUR PIÈCE — la garde d'armement "
            "FONCTIONNELLE (« armement PROUVE PAR OPERATION ») et le "
            "verdict post-mortem après le quit (« VERDICT POST-MORTEM "
            "apres le quit, D145 »)",
            any("armement PROUVE PAR OPERATION" in l for l in jrn_e4)
            and any("VERDICT POST-MORTEM apres le quit" in l for l in jrn_e4)
            and any("PASS RELEVER-ARME" in l for l in jrn_e4),
            "la sonde garde, la ligne constate")


# ---------------------------------------------------------------- D148 (e4)
def section_d148(r: Recoup) -> None:
    r.lignes.append("[recoup-doctrine] --- D148 : les verdicts se rendent "
                    "post-mortem et sur pièces (pièces e4) ---")
    jrn = lignes_de(E4 / "scenario-m5b-journal.log")
    pj = lignes_de(E4 / "proxy-journal.log")

    # D1 — le verdict du scénario : ÉCHEC NOMMÉ (5)
    r.passe("D1 : le verdict du scénario SUR PIÈCE — « VERDICT : M5-B "
            "ETAPE 2 — ECHEC NOMMÉ (5) »",
            any("VERDICT : M5-B ETAPE 2" in l and "ECHEC NOMM" in l
                and "(5)" in l for l in jrn),
            "ÉCHEC NOMMÉ (5)")

    # D2 — les CINQ refus aux noms exacts
    noms = ["NAVIGATEUR-A", "AUTORITE-A-SERVIE", "NAVIGATEUR-B",
            "DOM-B-INVALIDE", "POIGNEE-B-REFUSEE"]
    trouves = [n for n in noms if any(f"ECHEC {n}" in l for l in jrn)]
    r.passe("D2 : les CINQ refus aux NOMS EXACTS du scénario",
            len(trouves) == 5,
            " ; ".join(trouves) if len(trouves) == 5
            else f"MANQUANTS : {sorted(set(noms) - set(trouves))}")

    # D3 — le rc d'Edge capturé VIDE (la cécité unique derrière quatre refus)
    rc_vides = [l for l in jrn if l.rstrip().endswith("code de sortie")]
    producteur_vide = [l for l in jrn if "producteur rc= —" in l]
    r.passe("D3 : le rc d'Edge capturé VIDE SUR PIÈCE — « code de sortie » "
            "vide (NAVIGATEUR-A/B) et « producteur rc= » vide "
            "(AUTORITE-A-SERVIE/POIGNEE-B-REFUSEE transformées de RÉSERVE "
            "en ÉCHEC par le témoin aveugle)",
            len(rc_vides) >= 2 and len(producteur_vide) >= 2,
            f"{len(rc_vides)} « code de sortie » vide(s), "
            f"{len(producteur_vide)} « producteur rc= » vide(s)")

    # D4 — le DOM vide du run B + la capture absente (le headless muet)
    domb = E4 / "dom-b.txt"
    r.passe("D4 : dom-b.txt VIDE (0 o) + « DOM B vu : 0 o » + "
            "« nav-b.png ABSENTE » — le headless n'émet NI DOM NI CAPTURE "
            "pour la navigation échouée (la 502 nue)",
            domb.stat().st_size == 0
            and any("DOM B vu : 0 o" in l for l in jrn)
            and any("nav-b.png ABSENTE" in l for l in jrn),
            "0 o, md5 d41d8cd98f… (le fichier vide)")

    # D5 — la réception TRIPLEMENT recoupée (quatre producteurs indépendants)
    r.passe("D5 : la réception TRIPLEMENT recoupée — « certificat rejete » + "
            "la ligne de flux servie « s=34 » (journal proxy) ; « poignee "
            "de main refusee » (journal autorité) ; "
            "ERR_HTTP_RESPONSE_CODE_FAILURE (le navigateur)",
            sum(1 for l in pj if "certificat rejete" in l) >= 1
            and any("v=3" in l and "s=34" in l for l in pj)
            and "poignee de main refusee" in texte(E4 / "autorite-b.log")
            and "ERR_HTTP_RESPONSE_CODE_FAILURE"
            in texte(E4 / "nav-b-err.txt"),
            "les quatre producteurs indépendants")

    # D6 — la 502 NUE : s=34 == TXT_502_CERT 34 o
    r.passe("D6 : la 502 NUE servie — « s=34 » sur la ligne de flux v=3 "
            "(TXT_502_CERT 34 o, la réponse sans corps)",
            any("flux GET 127.0.0.1:443 v=3" in l and "s=34" in l
                for l in pj),
            "s=34 (34 octets exacts)")

    # D7 — la matrice S3 stationnaire v6/v8/e4 (+ LA PRÉCISION NOMMÉE)
    identiques = all(
        md5f(a / n) == md5f(b / n) == md5f(c / n)
        for n in ("curl-d2a.txt", "curl-d3.txt", "curl-d5.txt",
                  "hosts-lu.txt")
        for a, b, c in [(V6, V8, E4)])
    tailles = {p.name: p.stat().st_size
               for p in (V6 / "curl-d2b.txt", V8 / "curl-d2b.txt",
                         E4 / "curl-d2b.txt")}

    # la pièce T2b est un fichier CRLF : splitlines rend 38 lignes, la
    # ligne « Date: » vit à l'index 24 (constaté sur les TROIS pièces —
    # le premier jet de l'instrument la cherchait à 17 : ÉCHEC NOMMÉ de
    # l'INSTRUMENT, corrigé sur pièces, les pièces immuables — D154)
    IDX_DATE = 24

    def divergence(pa: pathlib.Path, pb: pathlib.Path) -> tuple:
        la, lb = lignes_de(pa), lignes_de(pb)
        if len(la) != len(lb):
            return False, "longueurs différentes"
        idx = [i for i, (x, y) in enumerate(zip(la, lb)) if x != y]
        if idx != [IDX_DATE]:
            return False, f"divergences aux rangs {idx}"
        if not (la[IDX_DATE].startswith("< Date:")
                and lb[IDX_DATE].startswith("< Date:")):
            return False, "la ligne divergente n'est pas la ligne Date"
        return True, "exactement UNE ligne : la Date du run"
    

    paires = [(V6, V8), (V8, E4), (V6, E4)]
    diffs = [divergence(a / "curl-d2b.txt", b / "curl-d2b.txt")
             for a, b in paires]
    d2b_ok = (len(set(tailles.values())) == 1
              and all(ok for ok, _ in diffs))
    r.passe("D7 : la matrice S3 stationnaire v6/v8/e4 — d2a/d3/d5 + "
            "hosts-lu OCTET POUR OCTET ; d2b SAUF LA LIGNE DATE (l'unique "
            "divergence : la Date du run, pièce CRLF — taille 946 o "
            "constante)",
            identiques and d2b_ok,
            "identiques : d2a/d3/d5/hosts ; d2b : "
            + " ; ".join(d for _, d in diffs))
    if identiques and d2b_ok:
        r.lignes.append(
            "[recoup-doctrine] PRÉCISION NOMMÉE (D148, matrice S3) : la "
            "formulation « pièces identiques octet pour octet » est EXACTE "
            "pour curl-d2a/d3/d5 + hosts-lu ; pour la pièce T2b "
            "(curl-d2b.txt) elle vaut SAUF LA LIGNE Date — la seule ligne "
            "qui varie entre v6/v8/e4 est la Date du run (pièce CRLF de "
            "longueur fixe : même taille 946 o, trois md5 distincts). LA "
            "STATIONNARITÉ S3 EST CONFIRMÉE EN SUBSTANCE — la précision "
            "sera consignée (append-only ; la règle D148 elle-même est "
            "CONFIRMÉE, seule la formulation factuelle est à préciser).")

    # D8 — le libellé périmé « REGRESSION a nommer » SUR PIÈCE + le tunnel
    r.passe("D8 : le libellé « REGRESSION a nommer » SUR PIÈCE (l'expectation "
            "périmée que D148 déclare) + le tunnel du run A établi hors "
            "ligne (D140 concernait les credentials DU PROXY, jamais curl)",
            any("REGRESSION a nommer" in l for l in jrn)
            and sum(1 for l in pj if "tunnel chiffre etabli" in l) >= 1,
            "le libellé présent au journal ; le tunnel présent au journal "
            "proxy")


def main() -> int:
    r = Recoup()
    r.lignes.append("[recoup-doctrine] === RECOUPURE POST-MORTEM DES "
                    "DÉCISIONS D138 / D145 / D148 — sur pièces, jamais sur "
                    "copier-coller ===")
    r.lignes.append(f"[recoup-doctrine] recoup rendu le "
                    f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                    f"au laboratoire")

    try:
        # ---- A. les pièces, md5 re-contrôlés contre le coffre ------------
        r.lignes.append("[recoup-doctrine] --- A : les pièces originales, "
                        "md5 == coffre RE-LU ---")
        recontrole(r, "preuves-run-v6", V6)
        recontrole(r, "preuves-run-e2", E2)
        recontrole(r, "preuves-run-v8", V8, attendus=V8_CIBLE)
        recontrole(r, "preuves-run-e4", E4)
    except Exception as exc:  # noqa: BLE001
        print(f"[recoup-doctrine] ERREUR FATALE : coffre illisible : {exc}",
              file=sys.stderr)
        return 2

    section_d138(r)
    section_d145(r)
    section_d148(r)

    # ---- le jugement -------------------------------------------------------
    for l in r.lignes:
        print(l)
    jugement = ("RECOUP : VERT — les décisions D138/D145/D148 sont FIDÈLES à "
                "leurs pièces originales : chaque fait fondateur cité par "
                "les trois décisions est RETROUVÉ SUR PIÈCE, mot pour mot "
                "et octet pour octet ; UNE PRÉCISION NOMMÉE (D148, matrice "
                "S3 : la pièce T2b porte la Date du run — l'identité octet "
                "pour octet vaut pour d2a/d3/d5 + hosts-lu, pour d2b elle "
                "vaut SAUF la ligne Date ; la stationnarité S3 est "
                "CONFIRMÉE, la formulation sera consignée append-only)"
                if r.ok else
                "RECOUP : ÉCHEC NOMMÉ — au moins un fait fondateur diverge "
                "des pièces : la décision concernée sera instruite (D154 : "
                "l'instrument d'abord, les pièces immuables)")
    print(f"[recoup-doctrine] {jugement}")

    SORTIE.mkdir(parents=True, exist_ok=True)
    rendu = ["=== RECOUPURE POST-MORTEM DES DÉCISIONS D138 / D145 / D148 ===",
             "(la promesse de reprise M7 : les trois décisions sont "
             "l'instrument de tous les verdicts de run — D154 : "
             "l'instrument est lui-même soupçonnable)",
             f"rendu le {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
             " au laboratoire",
             "les pièces originales : coffre /test/archives-preuves/ —",
             "  preuves-run-v6 (28) → D138 ; preuves-run-e2 (7) → D145 ;",
             "  preuves-run-v8 (matrice S3 ciblée) + preuves-run-e4 (37) → "
             "D148 ;",
             "rapatriées par rapatrier_preuves_doctrine.py, md5 contrôlés "
             "contre le coffre.", ""] + r.lignes[1:] + ["", jugement]
    (SORTIE / "VERDICT-recoup-doctrine.txt").write_text(
        "\n".join(rendu) + "\n", encoding="utf-8")
    print(f"[recoup-doctrine] le verdict du recoup écrit : "
          f"{SORTIE / 'VERDICT-recoup-doctrine.txt'}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
