#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/fixtures/rfc8446.py — LES VECTEURS RFC 8446 AU CORPUS DE FIXTURES
PARTAGÉES (la commande v0.11.0, chantier 4 : « ajouter les vecteurs RFC 8446
disponibles au corpus de fixtures partagées »).

Le RFC 8446 (TLS 1.3) ne porte pas de banc d'essai complet — c'est le rôle
du RFC 8448 (déjà rejoué au harnais poignée, bloc par bloc). Les vecteurs
NATIFS disponibles du RFC 8446 sont ses CONSTANTES NORMATIVES, ici posées
au corpus avec leur paragraphe d'origine — chaque valeur est la citation
d'une norme, jamais une mesure :

  § 4.1.2  ClientHello.random        : 32 octets OBLIGATOIREMENT CSPRNG
             (le contrat de tls13-29, la spec source CSPRNG) ;
  § 4.1.3  la sentinelle de rétrogradation : le ServerHello d'un serveur
             TLS 1.3 qui négocie une version inférieure porte, dans son
             random, les 8 octets « DOWNGRD » + 0x00 (TLS 1.1 et moins)
             ou 0x01 (TLS 1.2) aux positions 24..31 — un client DOIT
             s'arrêter sur la détection ;
  § 4.1.3  la valeur magique HelloRetryRequest : SHA-256("HelloRetryRequest")
             aux positions 24..31 du random du HRR (déjà au plan :
             R_HRR — la présente entrée la RECROISE) ;
  § 5.1     les types d'enregistrement : 20 alerte · 22 poignée · 23
             données applicatives · 24 tickets de session ;
  § 6       la suite obligatoire du profil : TLS_AES_128_GCM_SHA256
             (0x1301) — la valeur SUITE du plan, recroisée ;
  § 4.2.7   le groupe x25519 : 0x001D — la valeur GROUPE du plan, recroisée.

Ces vecteurs servent : (a) le contrôle des constantes du plan (SUITE,
GROUPE, HRR_MAGIQUE — tout écart NOMME une dérive du plan) ; (b) la
sentinelle DOWNGRD, NOUVELLE AU CORPUS, donnée citée que le laboratoire
garde pour l'avenir (la charte § 3 : le vecteur AVANT usage — jamais
l'inverse).
"""

import hashlib
import importlib.util
import pathlib

# § 4.1.3 — les sentinelles de rétrogradation (8 octets, positions 24..31
# du ServerHello.random ; le client TLS 1.3 DOIT refuser)
DOWNGRD_TLS11_ET_MOINS = b"DOWNGRD\x00"   # le serveur a négocié ≤ TLS 1.1
DOWNGRD_TLS12 = b"DOWNGRD\x01"            # le serveur a négocié TLS 1.2

# § 4.1.3 — la valeur magique HelloRetryRequest (déjà au plan R_HRR)
HRR_MAGIQUE = hashlib.sha256(b"HelloRetryRequest").digest()

# § 5.1 — les types d'enregistrement
TYPE_ALERTE = 20
TYPE_POIGNEE = 22
TYPE_DONNEES = 23
TYPE_TICKETS = 24

# § 6 — la suite obligatoire du profil (recroisement du plan)
SUITE_TLS_AES_128_GCM_SHA256 = 0x1301

# § 4.2.7 — le groupe x25519 (recroisement du plan)
GROUPE_X25519 = 0x001D

# § 4.1.2 — la LONGUEUR du random (le contrat CSPRNG de tls13-29)
RANDOM_LONGUEUR = 32


def recroise_plan() -> list[tuple[str, bool, str]]:
    """Le corpus recroise les constantes DU PLAN (tls13/layout.py) — tout
    écart NOMME une dérive. Retourne la liste des contrôles."""
    spec = importlib.util.spec_from_file_location(
        "lay_fixture", pathlib.Path(__file__).resolve().parents[1] / "layout.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [
        ("SUITE == 0x1301 (RFC 8446 § 6)",
         mod.SUITE == SUITE_TLS_AES_128_GCM_SHA256, f"plan {mod.SUITE:#x}"),
        ("GROUPE == 0x001D (RFC 8446 § 4.2.7)",
         mod.GROUPE == GROUPE_X25519, f"plan {mod.GROUPE:#x}"),
        ("HRR_MAGIQUE == SHA-256(\"HelloRetryRequest\") (§ 4.1.3)",
         mod.HRR_MAGIQUE == HRR_MAGIQUE,
         f"corpus {HRR_MAGIQUE[:8].hex()}… / plan {mod.HRR_MAGIQUE[:8].hex()}…"),
    ]


if __name__ == "__main__":
    print("=== LE CORPUS RFC 8446 — les vecteurs natifs, cités ===")
    print(f"DOWNGRD (≤ TLS 1.1) : {DOWNGRD_TLS11_ET_MOINS.hex()}")
    print(f"DOWNGRD (TLS 1.2)   : {DOWNGRD_TLS12.hex()}")
    print(f"HRR magique         : {HRR_MAGIQUE.hex()}")
    for nom, ok, detail in recroise_plan():
        print(f"[{'ok' if ok else 'ÉCART'}] {nom} ({detail})")
