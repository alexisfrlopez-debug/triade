#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE M5-b — L'AUTORITÉ DE TEST LOCALE (chantier (b) du jalon M5, D136).

Origine HTTP de test, chiffrée, à certificat pilotable : le jalon M5 exige
« une autorité de test locale » (PLAN_MILESTONES, jalon M5) pour juger le
tunnel M4 SANS dépendre d'Internet (example.com / self-signed.badssl.com
des runs terrain.17). Elle sert la requête du tunnel dans LE MÊME run, puis
présente un certificat invalide — le critère (b) : « un flux intercepté de
bout en bout ; échec propre sur certificat invalide constaté dans LE MÊME
run ».

QUATRE MODES, un par hérésie possible du certificat :
  valide      — SAN autorite.test, signée par la racine de test
                (installée dans le magasin de la machine qui juge) ;
  autonome    — AUTO-SIGNÉE (le miroir local de self-signed.badssl.com) ;
  autre-hote  — chaîne VALIDE mais SAN autre.test (l'invariant est l'hôte,
                pas la chaîne) ;
  expiree     — signée, hôte correct, notAfter PASSÉ.

FIXTURES : m5/autorite/fixtures/ (générées au laboratoire par
regenerer_fixtures.sh, OpenSSL ≥ 3.5, empreintes au LISEZMOI). Les clés sont
des CLÉS DE TEST JETABLES : elles ne protègent rien et ne signent que
autorite.test / autre.test — la discipline « aucune clé dans git » du coffre
réel vise les secrets réels, pas les fixtures d'essai d'une autorité qui se
déclare elle-même de test.

REFUS NOMMÉS (un échec muet n'est pas une preuve — discipline maison) :
  MODE-INCONNU         — le mode demandé n'existe pas (liste affichée) ;
  FIXTURE-ABSENTE      — un fichier du mode est absent (nommé) ;
  FIXTURE-ILLISIBLE    — certificat/clé illisibles (erreur ssl nommée) ;
  JOURNAL-INDICIBLE    — le journal de preuve ne peut pas s'ouvrir (D99 :
                         le journal est une preuve, son absence est un
                         refus, pas un silence) ;
  PORT-INDISPONIBLE    — l'adresse/port d'écoute est déjà prise.

JOURNAL (leçon D99 — preuve SUR LE DISQUE) : une ligne par fait —
« en ecoute », « requete servie », « poignee de main refusee », « arret
propre ». Aucun octet de secret n'y vit (les certificats publics et les
messages d'erreur TLS ne sont pas des secrets).

ARRÊT PROPRE : --arret-apres N requêtes servies, ou --arret-apres-secondes S
— l'autorité s'arrête ELLE-MÊME, code de sortie 0, ligne d'arrêt nommée ;
la poignée refusée ne compte PAS comme requête servie (un tunnel qui
échoue n'est pas un service rendu).

Utilisation (scénario VM M5-b, cf. m5/vm/) :
  python autorite_test.py --mode valide --port 443 \
      --journal C:\\preuves\\autorite-a.log --arret-apres 1

Code de sortie : 0 = arrêt propre ; 2 = refus nommé.
"""

import argparse
import datetime
import http.server
import pathlib
import signal
import socket
import ssl
import sys
import threading

MODES = ("valide", "autonome", "autre-hote", "expiree")
FIXTURES_MODE = {           # (certificat, clé) par mode
    "valide": ("serv-valide.pem", "serv-valide.key"),
    "autonome": ("serv-autonome.pem", "serv-autonome.key"),
    "autre-hote": ("serv-autre-hote.pem", "serv-autre-hote.key"),
    "expiree": ("serv-expiree.pem", "serv-expiree.key"),
}
REFUS = 2                   # code de sortie d'un refus nommé
MARQUEUR_PAGE = "TRIADE-M5B-PAGE-200"


def refus(nom, detail):
    """Refus nommé : message unique, code de sortie dédié."""
    print(f"[autorite] REFUS {nom} : {detail}", file=sys.stderr)
    sys.exit(REFUS)


def heure_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def page_de(mode, hote):
    """Page servie — STABLE (aucune date) : deux runs la recoupent octet
    pour octet, le témoin du scénario peut la hacher."""
    return ("<!DOCTYPE html>\n"
            "<html><head><meta charset=\"utf-8\">"
            "<title>TRIADE M5-b — autorite de test</title></head>\n"
            "<body>\n"
            "<h1>TRIADE-M5B — page de l'autorite de test locale</h1>\n"
            f"<p>mode : {mode} &middot; hote : {hote}</p>\n"
            f"<!-- TEMOIN-PAGE : {MARQUEUR_PAGE} -->\n"
            "</body></html>\n")


# ---------------------------------------------------------------- serveur

class Traiteur(http.server.BaseHTTPRequestHandler):
    """Un GET par connexion (M3 : une requête par connexion cliente)."""
    protocol_version = "HTTP/1.1"
    timeout = 15          # lecteur borné — un client muet ne pend pas

    def log_message(self, fmt, *args):          # pas de stderr par défaut :
        pass                                     # le journal est à NOUS

    def _refuser(self, code, nom):
        corps = f"{nom}\n".encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(corps)))
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            self.wfile.write(corps)
        except OSError:
            pass
        self.close_connection = True

    def do_GET(self):
        serv = self.server
        corps = serv.page.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corps)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(corps)
        self.close_connection = True
        serv.requete_servie(self.command, self.path, self.client_address,
                            len(corps))

    def do_POST(self):
        self._refuser(405, "METHODE-NON-GRATIFIEE (l'autorite ne sert que GET)")
        serv = self.server
        serv.journal(f"requete refusee — POST {self.path} — 405 "
                     "METHODE-NON-GRATIFIEE (l'autorite ne sert que GET)")

    do_PUT = do_POST
    do_DELETE = do_POST

    def finish(self):
        """Fermeture TLS CIVILISÉE : close_notify AVANT la fermeture TCP,
        bornée à 2 s (un pair muet ne retarde pas l'autorité) — le tunnel
        M4 DISTINGUE la fin de contexte (SEC_I_CONTEXT_EXPIRED) d'une
        rupture ; l'autorité de test se comporte comme une origine réelle."""
        try:
            self.connection.settimeout(2.0)
            self.connection.unwrap()
        except (OSError, ssl.SSLError, ValueError):
            pass
        try:
            super().finish()
        except (OSError, ssl.SSLError):
            pass


class Autorite(http.server.ThreadingHTTPServer):
    """Origine TLS de test : poignée NOMMÉE en cas d'échec, arrêt propre."""

    daemon_threads = True

    def __init__(self, adresse, contexte, journal_ligne, page, arret_apres):
        super().__init__(adresse, Traiteur)
        self.contexte = contexte
        self.journal = journal_ligne
        self.page = page
        self.arret_apres = arret_apres
        self.servies = 0
        self.refusees = 0
        self.socket.settimeout(5.0)     # accept borné : un client muet ne
        self._motif_arret = "interruption"   # pend pas l'autorité

    def get_request(self):
        """Accepte puis chiffre — la poignée refusée est NOMMÉE au journal
        (le proxy rejette le certificat AVANT toute requête : sans cette
        ligne, l'échec du tunnel serait invisible côté autorité)."""
        sock, addr = self.socket.accept()
        try:
            sock.settimeout(15.0)
            tls = self.contexte.wrap_socket(sock, server_side=True)
        except (ssl.SSLError, OSError) as e:
            self.refusees += 1
            self.journal(f"poignee de main refusee — "
                         f"{type(e).__name__} : {e}")
            try:
                sock.close()
            except OSError:
                pass
            raise ConnectionResetError("poignee de main refusee") from None
        return tls, addr

    def requete_servie(self, methode, chemin, client, taille):
        self.servies += 1
        self.journal(f"requete servie — {methode} {chemin} depuis "
                     f"{client[0]}:{client[1]} — 200, {taille} o")
        if self.arret_apres and self.servies >= self.arret_apres:
            self._motif_arret = "arret-apres"
            threading.Timer(0.05, self.shutdown).start()

    def arret(self):
        return (self._motif_arret, self.servies, self.refusees)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description="TRIADE M5-b — autorite de test locale (origine HTTPS "
                    "a certificat pilotable)")
    ap.add_argument("--mode", required=True,
                    help="valide | autonome | autre-hote | expiree")
    ap.add_argument("--hote", default="autorite.test",
                    help="hôte servi (affiché dans la page ; defaut "
                         "autorite.test)")
    ap.add_argument("--adresse", default="127.0.0.1",
                    help="adresse d'écoute (defaut 127.0.0.1)")
    ap.add_argument("--port", type=int, default=443,
                    help="port d'écoute (defaut 443 ; 0 = libre au choix "
                         "du système, affiché au démarrage)")
    ap.add_argument("--fixtures", default=str(pathlib.Path(__file__).resolve()
                    .parent / "fixtures"),
                    help="dossier des fixtures (defaut : fixtures/ voisin)")
    ap.add_argument("--journal", default="autorite-journal.log",
                    help="fichier journal de preuve (defaut : "
                         "autorite-journal.log dans le répertoire courant)")
    ap.add_argument("--arret-apres", type=int, default=0,
                    help="arrêt propre après N requêtes SERVIES (0 = sans "
                         "limite)")
    ap.add_argument("--arret-apres-secondes", type=float, default=0,
                    help="arrêt propre après S secondes (0 = sans limite)")
    args = ap.parse_args()

    # ---------------------------------------------------------- refus d'entrée
    if args.mode not in MODES:
        refus("MODE-INCONNU",
              f"« {args.mode} » — modes connus : {' | '.join(MODES)}")
    dossier = pathlib.Path(args.fixtures)
    cert_nom, cle_nom = FIXTURES_MODE[args.mode]
    cert = dossier / cert_nom
    cle = dossier / cle_nom
    for f in (cert, cle):
        if not f.is_file():
            refus("FIXTURE-ABSENTE",
                  f"mode « {args.mode} » — {f} est absent du dossier "
                  f"{dossier} (regenerer_fixtures.sh au laboratoire)")
    try:
        contexte = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        contexte.load_cert_chain(str(cert), str(cle))
    except (ssl.SSLError, OSError) as e:
        refus("FIXTURE-ILLISIBLE",
              f"{cert_nom} / {cle_nom} — {type(e).__name__} : {e}")

    # ------------------------------------------------------------- le journal
    try:
        fichier_journal = pathlib.Path(args.journal)
        if fichier_journal.parent and not fichier_journal.parent.exists():
            fichier_journal.parent.mkdir(parents=True, exist_ok=True)
        fich = open(fichier_journal, "a", encoding="utf-8")
    except OSError as e:
        refus("JOURNAL-INDICIBLE",
              f"{args.journal} — {type(e).__name__} : {e} "
              "(le journal de preuve est exigé, D99)")

    def journal_ligne(message):
        ligne = f"[{heure_utc()}] [autorite] {message}"
        fich.write(ligne + "\n")
        fich.flush()
        print(ligne, flush=True)

    # ------------------------------------------------------------- l'écoute
    try:
        serveur = Autorite((args.adresse, args.port), contexte,
                           journal_ligne, page_de(args.mode, args.hote),
                           args.arret_apres)
    except OSError as e:
        refus("PORT-INDISPONIBLE",
              f"{args.adresse}:{args.port} — {type(e).__name__} : {e}")

    port_reel = serveur.server_address[1]
    journal_ligne(f"en ecoute — mode={args.mode} "
                  f"adresse={args.adresse} port={port_reel}")

    minuteur = None
    if args.arret_apres_secondes > 0:
        def _buzzer():
            serveur._motif_arret = "delai"
            serveur.shutdown()
        minuteur = threading.Timer(args.arret_apres_secondes, _buzzer)
        minuteur.daemon = True
        minuteur.start()

    def _sigterm(_sig, _cadre):
        raise KeyboardInterrupt
    try:
        signal.signal(signal.SIGTERM, _sigterm)
    except (ValueError, OSError):
        pass                                    # Windows : le délai couvre

    code = 0
    try:
        serveur.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        code = 0                                # arrêt demandé = arrêt propre
    finally:
        if minuteur is not None:
            minuteur.cancel()
        motif, servies, refusees = serveur.arret()
        journal_ligne(f"arret propre — {servies} requete(s) servie(s), "
                      f"{refusees} poignee(s) refusee(s) — motif={motif}")
        fich.close()
    sys.exit(code)


if __name__ == "__main__":
    main()
