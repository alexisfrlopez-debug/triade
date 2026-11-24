# PLAN GELÉ — W20SEC (ancrage de transparence, preuves symboliques, durcissement)

> Prompt 5 de l'évaluation v0.26.0. Fail-closed, pré-enregistré, aucun résultat fabriqué.
> Aucun coffre réel approché (D105).

## Périmètre
(a) Ancrage de transparence D267 au geste de release : témoin d'époque (édition, sha256
    artefact/état, date) ancré par RFC 3161 auprès d'une autorité d'horodatage publique ;
    refus ANCRE-INDISPONIBLE / TEMOIN-SANS-ANCHE / ANCRE-INCOHERENTE ; vérification
    cryptographique du jeton hors ligne (openssl) ; chargement R10 sans réseau.
(b) Tamarin/ProVerif : si les binaires sont absents du bac ou si la mémoire < 4 GiB, le
    run est REFUSÉ nommément, avec la commande exacte pour la machine réelle ; aucun
    verdict fabriqué.
(c) Durcissement du coffre sur COPIES : Argon2id 128–256 MiB/t=4/p=1, plancher
    d'entropie ≥ 80 bits (gate 60 bits refusé), prototype média FIDO2 hmac-secret décrit.

## Contraintes
- Aucun secret du coffre réel lu ; phrases de test publiques uniquement.
- Les pièces scellées et le coffre réel restent intacts (empreintes recoupées).

## Critères d'acceptation
- (a) jeton RFC 3161 vérifié (empreinte du témoin == messageImprint), run négatif
  (témoin muté → ANCRE-INCOHERENTE), V6 de la porte vert seulement sur pièce ancrée.
- (b) refus nommé + commande de la machine réelle, ou verdict rendu et consigné.
- (c) autotest : gate d'entropie refuse < 80 bits ; rotation rend l'ancienne phrase
  inopérante ; PV consigné ; D270+ append-only.
