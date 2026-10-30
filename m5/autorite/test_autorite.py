#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE M5-b — cahier de falsifiabilité de l'AUTORITÉ DE TEST LOCALE (D136).

Treize contrôles : chaque mode tient sa promesse, chaque refus nommé est
VIVANT (prouvé par le geste qui le déclenche), l'arrêt propre est constaté,
et le juge indépendant OpenSSL croise le verdict du client Python — jamais
une seule source de vérité. Le journal de preuve (D99) est lu comme un
fichier : c'est le DISQUE qui témoigne, pas la console.

Exécution (laboratoire) : python3 test_autorite.py
Code de sortie : 0 = X PASS / 0 ÉCHEC ; 1 = au moins un ÉCHEC.
"""

import os
import pathlib
import socket
import ssl
import subprocess
import sys
import tempfile
import time

ICI = pathlib.Path(__file__).resolve().parent
AUTORITE = ICI / "autorite_test.py"
FIXTURES = ICI / "fixtures"
RACINE = FIXTURES / "racine-autorite.pem"
HOTE = "autorite.test"
PY = sys.executable


# ---------------------------------------------------------------- utilitaires

class AutoriteProc:
    """L'autorité en sous-processus — le journal est lu SUR LE DISQUE."""

    def __init__(self, mode, journal, extra=()):
        self.journal = pathlib.Path(journal)
        self.proc = subprocess.Popen(
            [PY, str(AUTORITE), "--mode", mode, "--port", "0",
             "--journal", str(journal), *extra],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    def attendre_demarrage(self, delai=15):
        """Attend la ligne « en ecoute » du journal — rend le port réel."""
        borne = time.time() + delai
        while time.time() < borne:
            if self.proc.poll() is not None:
                err = self.proc.stderr.read().decode(errors="replace")
                raise AssertionError(
                    f"autorité morte au démarrage (rc={self.proc.returncode})"
                    f" : {err.strip()[:200]}")
            try:
                texte = self.journal.read_text(encoding="utf-8")
            except FileNotFoundError:
                time.sleep(0.1)
                continue
            for ligne in texte.splitlines():
                if "en ecoute" in ligne and "port=" in ligne:
                    return int(ligne.rsplit("port=", 1)[1].split()[0])
            time.sleep(0.1)
        raise AssertionError("aucune ligne « en ecoute » après "
                             f"{delai} s (journal : {self.journal})")

    def lire_journal(self):
        try:
            return self.journal.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ""

    def finir(self, delai=20):
        """Attend la fin propre (ou force, en nommant l'échec)."""
        try:
            reste, _ = self.proc.communicate(timeout=delai)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.communicate()
            raise AssertionError("l'autorité ne s'est pas arrêtée "
                                 f"(dépassé {delai} s)")
        return self.proc.returncode, reste or self.lire_journal()


def client_tls(port, hote=HOTE, cafile=RACINE, chemin="/", delai=10):
    """Client TLS exigeant : racine + nom d'hôte — renvoie la réponse
    complète, lève ssl.SSLCertVerificationError si le certificat ment."""
    ctx = ssl.create_default_context(cafile=str(cafile))
    with socket.create_connection(("127.0.0.1", port), timeout=delai) as brut:
        with ctx.wrap_socket(brut, server_hostname=hote) as tls:
            tls.sendall(f"GET {chemin} HTTP/1.1\r\nHost: {hote}\r\n\r\n"
                        .encode())
            morceaux = []
            while True:
                morceau = tls.recv(65536)
                if not morceau:
                    break
                morceaux.append(morceau)
            return b"".join(morceaux)


def contient(haystack_minuscule, aiguilles):
    return any(a in haystack_minuscule for a in aiguilles)


CONTROLES = []


def controle(nom):
    def decorer(fonction):
        CONTROLES.append((nom, fonction))
        return fonction
    return decorer


# ---------------------------------------------------------------- contrôles

@controle("C0 fixtures présentes + chaînes jugées par OpenSSL (indépendant)")
def c0():
    attendus = ["racine-autorite.pem", "racine-autorite.key",
                "serv-valide.pem", "serv-valide.key",
                "serv-autonome.pem", "serv-autonome.key",
                "serv-autre-hote.pem", "serv-autre-hote.key",
                "serv-expiree.pem", "serv-expiree.key"]
    manquants = [n for n in attendus if not (FIXTURES / n).is_file()]
    assert not manquants, f"fixtures absentes : {manquants}"
    for cert, ok in (("serv-valide.pem", True),
                     ("serv-autre-hote.pem", True),
                     ("serv-expiree.pem", False),
                     ("serv-autonome.pem", False)):
        r = subprocess.run(["openssl", "verify", "-CAfile", str(RACINE),
                            str(FIXTURES / cert)],
                           capture_output=True, timeout=30)
        assert (r.returncode == 0) == ok, \
            f"{cert} : chaîne attendue {'valide' if ok else 'rejetée'}, " \
            f"openssl dit rc={r.returncode} — {r.stdout.decode()[:120]}"
    return "10 fichiers, 4 verdicts de chaîne conformes"


@controle("C1 mode VALIDE : tunnel acceptable — 200 + marqueur + arrêt propre")
def c1():
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "a.log")
        autorite = AutoriteProc("valide", journal,
                                extra=("--arret-apres", "1"))
        try:
            port = autorite.attendre_demarrage()
            reponse = client_tls(port)
        finally:
            rc, _ = autorite.finir()
        texte = reponse.decode(errors="replace")
        assert texte.startswith("HTTP/1.1 200"), \
            f"réponse attendue 200, reçue : {texte[:80]!r}"
        assert "TRIADE-M5B-PAGE-200" in texte, "marqueur de page absent"
        assert rc == 0, f"arrêt propre attendu (rc=0), reçu rc={rc}"
        journal_texte = autorite.lire_journal()
        for attendu in ("en ecoute — mode=valide",
                        "requete servie — GET /",
                        "arret propre — 1 requete(s) servie(s)",
                        "motif=arret-apres"):
            assert attendu in journal_texte, \
                f"ligne de journal attendue manquante : {attendu!r}"
        return f"200 + marqueur, rc=0, 4 lignes de journal exactes (port {port})"


@controle("C2 page STABLE : deux runs, CORPS octets identiques (le témoin "
          "recoupe ; l'en-tête Date vit sa vie — il EST une preuve de run)")
def c2():
    corps = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as tmp:
            journal = os.path.join(tmp, "a.log")
            autorite = AutoriteProc("valide", journal,
                                    extra=("--arret-apres", "1"))
            try:
                port = autorite.attendre_demarrage()
                reponse = client_tls(port)
            finally:
                autorite.finir()
        sep = reponse.find(b"\r\n\r\n")
        corps.append(reponse[sep + 4:] if sep >= 0 else b"")
    assert corps[0] == corps[1], \
        "le CORPS de la page a bougé entre deux runs (date embarquée ?)"
    assert b"TRIADE-M5B-PAGE-200" in corps[0], "marqueur absent du corps"
    return f"{len(corps)} runs, corps de {len(corps[0])} o identiques"


@controle("C3 mode AUTONOME (auto-signée) : rejet client + poignée NOMMÉE "
          "+ l'autorité SURVIT")
def c3():
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "a.log")
        autorite = AutoriteProc("autonome", journal,
                                extra=("--arret-apres-secondes", "6"))
        try:
            port = autorite.attendre_demarrage()
            try:
                client_tls(port)
                raise AssertionError("le certificat auto-signé a été ACCEPTÉ")
            except ssl.SSLCertVerificationError as e:
                message = str(e).lower()
                assert contient(message, ("self-signed", "self signed",
                                          "self signed certificate")), \
                    f"motif attendu auto-signé, reçu : {message[:160]!r}"
        finally:
            rc, _ = autorite.finir()
        assert rc == 0, f"l'autorité devait survivre puis s'arrêter (rc=0), " \
                        f"reçu rc={rc}"
        journal_texte = autorite.lire_journal()
        assert "poignee de main refusee" in journal_texte, \
            "la poignée refusée n'est pas nommée au journal"
        assert "0 requete(s) servie(s), 1 poignee(s) refusee(s)" \
            in journal_texte, "la poignée refusée ne doit PAS compter comme " \
            "requête servie"
        assert "motif=delai" in journal_texte, "l'arrêt par délai attendu"
        return "rejet auto-signé, poignée nommée, survie + arrêt propre délai"


@controle("C4 mode AUTRE-HOTE (mauvais SAN) : rejet nom d'hôte")
def c4():
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "a.log")
        autorite = AutoriteProc("autre-hote", journal,
                                extra=("--arret-apres-secondes", "6"))
        try:
            port = autorite.attendre_demarrage()
            try:
                client_tls(port)
                raise AssertionError("le mauvais nom d'hôte a été ACCEPTÉ")
            except ssl.SSLCertVerificationError as e:
                message = str(e).lower()
                assert contient(message, ("hostname", "not valid for",
                                          "mismatch", "adresse")), \
                    f"motif attendu hôte, reçu : {message[:160]!r}"
        finally:
            rc, _ = autorite.finir()
        assert rc == 0
        assert "poignee de main refusee" in autorite.lire_journal()
        return "rejet : le certificat ment sur l'hôte (SAN autre.test)"


@controle("C5 mode EXPIRÉE : rejet expiration")
def c5():
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "a.log")
        autorite = AutoriteProc("expiree", journal,
                                extra=("--arret-apres-secondes", "6"))
        try:
            port = autorite.attendre_demarrage()
            try:
                client_tls(port)
                raise AssertionError("le certificat expiré a été ACCEPTÉ")
            except ssl.SSLCertVerificationError as e:
                message = str(e).lower()
                assert "expired" in message or "expir" in message, \
                    f"motif attendu expiré, reçu : {message[:160]!r}"
        finally:
            rc, _ = autorite.finir()
        assert rc == 0
        return "rejet : notAfter dans le passé"


@controle("C6 REFUS MODE-INCONNU : nommé, code 2")
def c6():
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "a.log")
        r = subprocess.run([PY, str(AUTORITE), "--mode", "pirate",
                            "--port", "0", "--journal", journal],
                           capture_output=True, timeout=30)
        err = r.stderr.decode(errors="replace")
        assert r.returncode == 2, f"code attendu 2, reçu {r.returncode}"
        assert "REFUS MODE-INCONNU" in err, f"refus non nommé : {err[:160]!r}"
        assert "valide" in err and "expiree" in err, \
            "le refus doit afficher la liste des modes connus"
        return "« pirate » → REFUS MODE-INCONNU, rc=2, liste affichée"


@controle("C7 REFUS FIXTURE-ABSENTE : nommé, fichier coupable nommé")
def c7():
    with tempfile.TemporaryDirectory() as tmp:
        vide = os.path.join(tmp, "fixtures-vides")
        os.makedirs(vide)
        journal = os.path.join(tmp, "a.log")
        r = subprocess.run([PY, str(AUTORITE), "--mode", "valide",
                            "--port", "0", "--fixtures", vide,
                            "--journal", journal],
                           capture_output=True, timeout=30)
        err = r.stderr.decode(errors="replace")
        assert r.returncode == 2, f"code attendu 2, reçu {r.returncode}"
        assert "REFUS FIXTURE-ABSENTE" in err, \
            f"refus non nommé : {err[:160]!r}"
        assert "serv-valide.pem" in err, \
            "le fichier absent doit être nommé dans le refus"
        return "dossier vide → REFUS FIXTURE-ABSENTE, serv-valide.pem nommé"


@controle("C8 REFUS PORT-INDISPONIBLE : nommé (port occupé par un témoin)")
def c8():
    temoin = socket.socket()
    temoin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temoin.bind(("127.0.0.1", 0))
    temoin.listen(1)
    port_occupe = temoin.getsockname()[1]
    try:
        with tempfile.TemporaryDirectory() as tmp:
            journal = os.path.join(tmp, "a.log")
            r = subprocess.run([PY, str(AUTORITE), "--mode", "valide",
                                "--port", str(port_occupe),
                                "--journal", journal],
                               capture_output=True, timeout=30)
            err = r.stderr.decode(errors="replace")
            assert r.returncode == 2, \
                f"code attendu 2, reçu {r.returncode}"
            assert "REFUS PORT-INDISPONIBLE" in err, \
                f"refus non nommé : {err[:160]!r}"
    finally:
        temoin.close()
    return f"port {port_occupe} occupé → REFUS PORT-INDISPONIBLE"


@controle("C9 REFUS JOURNAL-INDICIBLE : nommé (D99 : le journal est exigé)")
def c9():
    with tempfile.TemporaryDirectory() as tmp:
        bloqueur = os.path.join(tmp, "bloqueur")     # un FICHIER là où un
        pathlib.Path(bloqueur).write_text("x")       # dossier serait requis
        journal_impossible = os.path.join(bloqueur, "sous", "a.log")
        r = subprocess.run([PY, str(AUTORITE), "--mode", "valide",
                            "--port", "0",
                            "--journal", journal_impossible],
                           capture_output=True, timeout=30)
        err = r.stderr.decode(errors="replace")
        assert r.returncode == 2, f"code attendu 2, reçu {r.returncode}"
        assert "REFUS JOURNAL-INDICIBLE" in err, \
            f"refus non nommé : {err[:160]!r}"
        return "chemin impossible → REFUS JOURNAL-INDICIBLE"


@controle("C10 POST refusé : 405 + ligne de journal nommée")
def c10():
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "a.log")
        autorite = AutoriteProc("valide", journal,
                                extra=("--arret-apres-secondes", "8"))
        try:
            port = autorite.attendre_demarrage()
            ctx = ssl.create_default_context(cafile=str(RACINE))
            with socket.create_connection(("127.0.0.1", port),
                                          timeout=10) as brut:
                with ctx.wrap_socket(brut, server_hostname=HOTE) as tls:
                    tls.sendall(f"POST / HTTP/1.1\r\nHost: {HOTE}\r\n"
                                f"Content-Length: 0\r\n\r\n".encode())
                    morceaux = []
                    while True:
                        m = tls.recv(65536)
                        if not m:
                            break
                        morceaux.append(m)
                    reponse = b"".join(morceaux).decode(errors="replace")
            assert reponse.startswith("HTTP/1.1 405"), \
                f"405 attendu, reçu : {reponse[:60]!r}"
            assert "METHODE-NON-GRATIFIEE" in reponse, \
                "le corps du 405 doit porter le refus nommé"
        finally:
            rc, _ = autorite.finir()
        assert rc == 0
        assert "requete refusee — POST /" in autorite.lire_journal(), \
            "le POST refusé n'est pas journalisé"
        return "405 METHODE-NON-GRATIFIEE, journal nommé"


@controle("C11 juge croisé CURL (le client M3 du terrain) : valide 200 / "
          "autonome rejeté code 60")
def c11():
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "a.log")
        autorite = AutoriteProc("valide", journal,
                                extra=("--arret-apres", "1"))
        try:
            port = autorite.attendre_demarrage()
            r = subprocess.run(
                ["curl", "-s", "--cacert", str(RACINE), "--resolve",
                 f"{HOTE}:{port}:127.0.0.1", f"https://{HOTE}:{port}/"],
                capture_output=True, timeout=30)
            assert r.returncode == 0, \
                f"valide : curl attendu rc=0, reçu {r.returncode} — " \
                f"{r.stderr.decode(errors='replace')[:200]!r}"
            page = r.stdout.decode(errors="replace")
            assert "TRIADE-M5B-PAGE-200" in page, \
                "la page devait revenir au juge indépendant"
        finally:
            autorite.finir()
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "b.log")
        autorite = AutoriteProc("autonome", journal,
                                extra=("--arret-apres-secondes", "12"))
        try:
            port = autorite.attendre_demarrage()
            r = subprocess.run(
                ["curl", "-s", "--cacert", str(RACINE), "--resolve",
                 f"{HOTE}:{port}:127.0.0.1", f"https://{HOTE}:{port}/"],
                capture_output=True, timeout=30)
            assert r.returncode == 60, \
                f"autonome : curl attendu rc=60 (certificat), reçu " \
                f"{r.returncode} — {r.stderr.decode(errors='replace')[:200]!r}"
        finally:
            autorite.finir()
        assert "poignee de main refusee" in autorite.lire_journal()
        return "curl : 200 + marqueur sur valide, code 60 sur autonome"


@controle("C12 arrêt propre par DÉLAI sans aucune requête")
def c12():
    with tempfile.TemporaryDirectory() as tmp:
        journal = os.path.join(tmp, "a.log")
        autorite = AutoriteProc("valide", journal,
                                extra=("--arret-apres-secondes", "2"))
        debut = time.time()
        rc, _ = autorite.finir()
        duree = time.time() - debut
        assert rc == 0, f"rc=0 attendu, reçu {rc}"
        assert duree < 10, f"l'arrêt a traîné : {duree:.1f} s"
        journal_texte = autorite.lire_journal()
        assert "motif=delai" in journal_texte, "motif=delai attendu"
        assert "arret propre — 0 requete(s) servie(s), 0 poignee(s) " \
            "refusee(s)" in journal_texte, "comptes d'arrêt inexacts"
        return f"arrêt propre en {duree:.1f} s, motif=delai, comptes exacts"


# ---------------------------------------------------------------- exécution

def main():
    print(f"[test_autorite] {len(CONTROLES)} contrôles — juge indépendant : "
          f"OpenSSL {ssl.OPENSSL_VERSION}")
    echecs = []
    for nom, fonction in CONTROLES:
        try:
            detail = fonction()
            print(f"  PASS  {nom} — {detail}")
        except Exception as e:
            echecs.append((nom, e))
            print(f"  ÉCHEC {nom} — {e}")
    total = len(CONTROLES)
    print(f"[test_autorite] VERDICT : {total - len(echecs)} PASS / "
          f"{len(echecs)} ÉCHEC")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
