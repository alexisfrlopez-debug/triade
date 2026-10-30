# Couche I — jalon M5 (outil complet) : chantier (b), interception en VM isolée

> État du jalon (PLAN_MILESTONES) : **(a) empreintes par build — RÉALISÉ
> (D134)** ; **(b) interception en VM isolée — OUVERT (D136, 31/10)** :
> l'autorité de test locale LIVRÉE et PROUVÉE au laboratoire
> (m5/autorite/, 13 contrôles), le kit VM étape 1 LIVRÉ au terrain
> (m5/vm/ — le critère M4 rejoué en VM isolée réseau coupé, sans navigateur
> encore) ; les révisions http-08:R3 / http-10:R3 / http-12:R2 ci-dessous
> sont l'INTENTION ÉCRITE-AVANT-CODE du flux navigateur, en attente de
> notation ; **(c) patch à chaud du journal — pas ouvert**.

## Le constat fondateur (terrain.17, D96)

« Le client qui parle la forme absolue https:// n'existe dans AUCUN outil
standard (curl envoie CONNECT et chiffre lui-même) » — terrain.17 posait
donc un script TCP écrit à la main. Le jalon (b) exige mieux : « un flux
NAVIGATEUR intercepté de bout en bout dans la VM ». Or un navigateur :

- sur une URL https://, parle CONNECT au mandataire puis chiffre LUI-MÊME
  de bout en bout — le proxy ne verrait que des octets opaques (aucune
  interception) et le protocole scellé n'a AUCUN tunnel TLS côté serveur
  (le M4 est un mandataire-client : InitializeSecurityContext, jamais
  AcceptSecurityContext) ;
- sur une URL http://, envoie la forme ABSOLUE http:// — le chemin M3
  SCELLÉ et prouvé terrain (T2, 6 verts consécutifs D64-D71), relayé en
  CLAIR vers l'origine.

La conclusion est structurelle : **le flux navigateur intercepté avec
re-chiffrement amont naît du chemin http:// absolu, relevé vers le tunnel
M4 en amont** — le mandataire reçoit le clair du navigateur (interception)
et chiffre vers l'origine (re-chiffrement, tls-08 TEL QUEL). Aucun tunnel
serveur à inventer, aucune contrebande dans le scellé : le pont tient en
TROIS révisions du domaine http, modèle des révisions inter-jalons
(http-08:R2/http-10:R2 en M4, win-02:R2/tcp-07:R3 avant elles).

## La composition complète du scénario (b)

```
NAVIGATEUR (VM isolée, réseau coupé)
   │  mandataire explicite 127.0.0.1:25000, URL http://autorite.test/…
   ▼
proxy.exe (0.5.0 scellé + R3 : --relever-https)
   │  interception : ligne de FLUX au journal (http-10:R3)
   │  re-chiffrement : tls-08 → autorite.test:443 (tunnel M4 inchangé)
   ▼
AUTORITÉ DE TEST LOCALE (m5/autorite/, livrée D136)
   │  certificat VALIDE → tunnel, page, 200 au navigateur
   │  certificat INVALIDE → Schannel refuse → « certificat rejete »
   ▼
502 « Certificat rejete » AU NAVIGATEUR — le même run (critère (b))
```

Le journal + le TÉMOIN SUR LE DISQUE (leçon D99) portent la preuve ;
l'étape 1 du kit (m5/vm/) prouve DÈS AUJOURD'HUI la moitié amont de la
composition (tunnel + autorité + 502 exacte, en VM isolée, sans navigateur)
avec le client forme-absolue hérité de terrain_m4.ps1.

## Les trois révisions (intention écrite-avant-code — la notation suivra)

Chacune instancie le gabarit § 2.2, cite son ancêtre, ne recopie rien (T5) ;
les contrats complets (pre/post/inv/échecs/vecteurs) seront arrêtés à la
notation, modèle m4/I. Les bornes ci-dessous sont les INVARIANTS déjà
décidés :

### http-08:R3 — cible : le verdict « à relever »

Ancêtre http-08:R2 (D77, cité). La forme absolue « http:// » (8 octets
exacts, minuscules — R1 inchangé) reçoit, SI ET SEULEMENT SI la politique
de relevement est armée au démarrage (http-12:R2), un verdict PROPRE
« cible à relever », distinct des verdicts http/TLS de R2 ; l'autorité et
le chemin découpés aux règles R1 ; port implicite **443 au relevement**
(l'origine est l'HTTPS de l'hôte demandé, consigné DANS la sortie — la
décision de relever appartient à http-10:R3). SANS politique armée :
R2 octet pour octet (le chemin M3 scellé T2 reste vert — anti-régression
R7). AUCUN relevement implicite, aucun relèvement d'une forme origine ou
autorité : la surface de contrebande n'augmente que du verdict, jamais
d'une tolérance.

### http-10:R3 — session proxy : le routage du relevement ET la ligne de flux

Ancêtre http-10:R2 (D77, cité). (1) Routage : verdict « cible à relever »
→ LE MÊME chemin que Q2' de R2 — paquet de session tls-08 (autorité
découpée, requête réécrite en forme origine, port 443), cadre TLS vierge,
verdicts transportés tels quels, table des réponses Q3' INCHANGÉE (le
certificat invalide d'une cible relevée reçoit la 502 étiquetée — c'est LE
critère (b) vu du navigateur). (2) **La ligne de flux naît ici** : une
ligne par session cliente ABOUTIE — méthode, hôte:port, verdict de session,
octets clairs entrés/sortis — modèle tcp-11 (états nommés, AUCUN octet de
secret, charte § 3 : ce qui n'est pas journalisé ne peut pas fuir) ;
propriété unique T5 (l'appartenance ligne-de-flux vs console http-11 sera
arrêtée à la notation — la question est consignée, pas tranchée en silence).

### http-12:R2 — principal : la politique de démarrage (la CLI naît)

Ancêtre http-12:R1 (D46, cité). Au démarrage, l'orchestrateur lit ses
arguments : `--relever-https` ARME la politique (le verdict R3 devient
possible) ; TOUT argument inconnu est un REFUS NOMMÉ au démarrage — le
processus ne démarre jamais en silence avec un drapeau mal orthographié
(l'échec muet n'est pas une preuve). Sans argument : comportement scellé
inchangé. C'est la graine de « l'interface en ligne de commande » du jalon
M5 — chaque drapeau futur suivra la même loi : nommé, documenté, refusé
s'il n'est pas reconnu.

## Ce que la notation devra livrer (le chantier après le verdict terrain 1)

1. m5/layout.py (plan d'adressage, modèle m4/layout.py — les slots des
   révisions mesurés sur les notations réelles, l'héritage M3/M4
   réexporté inchangé) ;
2. les notations à la main + l'oracle à scénarios étendu (scénarios :
   cible relevée saine, certificat invalide relevé, politique absente →
   chemin M3 octet pour octet, argument inconnu → refus nommé) ;
3. proxy.exe reconstruit + carte + conformité + falsifiabilité (le modèle
   D104 entier) ;
4. le kit VM ÉTAPE 2 : le même scénario-m5b avec le NAVIGATEUR du bac à
   sable (Edge du sandbox, mandataire 127.0.0.1:25000, page
   http://autorite.test/) — le critère (b) complet.

## Bornes du présent document

Il ne NOTATIONNE rien (aucun octet de code n'a bougé : le proxy 0.5.0
scellé est intact, sha256 b9264e0b…) ; il ne touche AUCUN arbre scellé ;
il consigne l'INTENTION et ses invariants pour que la notation suivante
écrive les contrats complets sur des bases déjà arbitrées par le
développeur (le relevement http→https amont est la composition retenue —
le tunnel serveur / MITM CONNECT est REJETÉ : il exigerait un domaine TLS
serveur entier pour un résultat que le relevement atteint avec l'existant
prouvé).
