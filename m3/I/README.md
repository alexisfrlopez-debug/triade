# Couche I — jalon M3 (proxy HTTP, entrées non fiables)

Treize spécifications nouvelles, écrites avant la notation (R2, provenance
`écrite-avant-code`). Elles instancient le gabarit § 2.2 de la spécification
v0.5.0 et étendent le registre figé du projet (m0/I/README.md, § 2.1) : le
domaine **`http` est créé, réservé M3** (douze spécifications http-01 à
http-12) ; l'extension `tcp-13` prolonge le domaine tcp dans le rôle client
(résolution + connexion d'une cible arbitraire), comme libc-09 prolongeait
libc en M2.

Le jalon M3 exige des **contrats renforcés** (PLAN, D45) : chaque octet non
fiable a un comportement défini, chaque échec est nommé, aucune tolérance
de format n'est silencieuse. Les conventions transverses qui suivent lient
les treize spécifications — chacune y renvoie, aucune ne les recopie
(défaut T5 sinon).

## Conventions transverses (charte des contrats renforcés)

1. **Spans partout** — toute entrée réseau est un couple (ptr, longueur) ;
   aucune terminaison NUL n'est jamais supposée. La traduction span →
   chaîne C (exigée par getaddrinfo) existe UNE fois : tcp-13:Q2.
2. **Verdicts eax** — 0 = succès ; chaque valeur non nulle est nommée dans
   la spécification émettrice (bloc Échecs) et mapped à une réponse HTTP
   par http-10, unique propriétaire de la table des réponses.
3. **Constantes nommées, un seul propriétaire** (T1) — MAX_TETE = 8192
   (http-06 ; RFC 7230 §3.1.1 exige ≥ 8000), MAX_CIBLE = 2048 (http-02 ;
   usage navigateur), HOTE_MAX = 255 (tcp-13 ; limite DNS). Pas de
   MAX_LIGNE : la limite de tête borne transitivement toute ligne — une
   limite, un propriétaire.
4. **Casse** — méthodes et versions sensibles (http-02, RFC 7230 §5.1.1),
   schéma « http:// » strict minuscule (http-08, durcissement délibéré) ;
   l'unique comparaison insensible à la casse du domaine est le nom
   d'en-tête (http-04, obligation RFC 7230 §3.2) — propriété unique.
5. **CRLF strict** — un LF non précédé de CR est rejeté (http-06:Q4 →
   400). La RFC 7230 §3.5 PERMET d'accepter le LF nu ; M3 le refuse :
   chaque tolérance de format est une surface de contrebande.
6. **Zéros de tête rejetés** sur les longueurs décimales (http-05:Q6, RFC
   7230 §5.5.1) ; un seul « 0 » est valide.
7. **Une requête par connexion cliente** (M3) ; la réponse n'est JAMAIS
   parsée (relais à fermeture délimitée, http-10:Q4) — ce qui n'est pas
   parsé ne peut pas être mal parsé.
8. **Fermetures à propriétaire unique** — chaque socket est fermée
   exactement une fois, par le thread session (http-10:Q5) ; les pompes ne
   ferment jamais (http-09:Q4) ; les handles de threads sont fermés par
   l'orchestrateur (tcp-06:Q4).
9. **Échec avant l'entrée système** — toute malformation est tranchée par
   les parseurs AVANT getaddrinfo/connect (http-07:E1) : rien d'ambigu
   n'atteint le résolveur.

## Spécifications nouvelles (blocs e5xxxx, génération 4)

| Spécification | Bloc carte | Rôle | Zone prévue (RVA, slot) |
|---|---|---|---|
| http-01:R1 | e50001 | Itérateur de ligne CRLF (propriétaire T5) | http @ 0x4C00, 0x80 |
| http-02:R1 | e50002 | Ligne de requête → champs (méthode/cible/version) | http @ 0x4C80, 0x100 |
| http-03:R1 | e50003 | Ligne d'en-tête → nom/valeur (OWS rognés) | http @ 0x4D80, 0x80 |
| http-04:R1 | e50004 | Premier en-tête nommé (casse insensible unique) | http @ 0x4E00, 0xC0 |
| http-05:R1 | e50005 | Décimal ASCII borné → u32 (anti-débordement) | http @ 0x4EC0, 0x80 |
| http-06:R1 | e50006 | Fin de tête + limite MAX_TETE + LF isolé | http @ 0x4F40, 0xC0 |
| http-07:R1 | e50007 | Autorité « hôte[:port] » (propriétaire T5) | http @ 0x5000, 0xC0 |
| http-08:R1 | e50008 | Cible : forme absolue/origine/autorité + chemin | http @ 0x50C0, 0x100 |
| http-09:R1 | e50009 | Pompe unidirectionnelle (jamais fermer) | http @ 0x51C0, 0xC0 |
| http-10:R1 | e50010 | Session proxy (thread, orchestration complète) | http @ 0x5280, 0x400 |
| http-11:R1 | e50011 | Console (quit) | http @ 0x5680, 0x100 |
| http-12:R1 | e50012 | Orchestration proxy — point d'entrée proxy.exe | app @ 0x1800, 0x480 |
| tcp-13:R1 | e50013 | Connexion cliente résolue (getaddrinfo + connect) | net @ 0x4200, 0x100 |

L'arrangement de zones est une préfiguration arrêtée par le plan
d'adressage M3 (m3/layout.py, étape b) : la zone http étend .text2 au-delà
de 0x4C00 (libre depuis tcp-11 @ 0x4B00), le slot 0x4200 est le trou
libre de la zone net (0x4200-0x42FF, laissé par tcp-05 @ 0x41C0), et
http-12 occupe le slot d'application 0x1800 (celui de tcp-12 dans
echo.exe — exécutables distincts, plans distincts, discipline identique).
Deux entrées IAT ws2_32 sont appendues (getaddrinfo @ 0x2350,
freeaddrinfo @ 0x2358) ; l'IAT existante et les RVA des blocs réutilisés
sont inchangés (R7).

Tous les identifiants naissent et restent à R1 (aucun cycle de révision
prévu au jalon ; la lignée demo a montré le mécanisme si le terrain
l'exige).

## Blocs réutilisés dans proxy.exe (R7, octets identiques aux artefacts scellés)

| Spécification | Bloc | Rôle | Zone |
|---|---|---|---|
| hello-02:R1 | a10002 | Écriture stdout via WriteFile | io @ 0x1040 |
| hello-03:R1 | a10003 | Sortie propre via ExitProcess | io @ 0x1080 |
| libc-01:R1 | b20001 | Copie mémoire (memcpy) | libc @ 0x1100 |
| libc-02:R1 | b20002 | Comparaison normalisée (memcmp) | libc @ 0x1180 |
| libc-03:R1 | b20003 | Longueur de chaîne (strlen) | libc @ 0x1200 |
| libc-04:R1 | b20004 | Conversion décimale u32 (itoa) | libc @ 0x1280 |
| tcp-01:R1 | c30001 | Initialisation serveur (port 25000) | net @ 0x4000 |
| tcp-02:R1 | c30002 | Acceptation d'une connexion | net @ 0x4100 |
| tcp-03:R1 | c30003 | Réception (recv) | net @ 0x4140 |
| tcp-04:R1 | c30004 | Émission (send) | net @ 0x4180 |
| tcp-05:R1 | c30005 | Fermeture de socket | net @ 0x41C0 |
| tcp-06:R1 | c30006 | Lancement de thread (CreateThread) | thr @ 0x4300 |
| tcp-11:R1 | c30011 | Ligne de journal console (sérialisée) | srv @ 0x4B00 |

Les blocs tcp-07 (moteur de patch), tcp-08 (écho v1/v2), tcp-09 (session
écho), tcp-10 (console écho), tcp-12 (orchestration écho), libc-05/06/07
et libc-09 restent indexés par la carte génération 3 mais ne sont pas
embarqués dans proxy.exe (aucun appelant M3 — le patch à chaud du journal
revient au jalon M5). Les slots 0x4400-0x4AFF et 0x4800-0x49FF restent
int3 dans l'image M3.

## Surface de fuzzing (périmètre du million, critère M3)

Le harnais à propriétés P1-P5 (m3/fuzz.py, D45) étend sa cible aux blocs
http-01 à http-09 (feuilles pures et pompe à shims réseau) et à la chaîne
d'accumulation de http-10 — les V3 de chaque spécification ci-dessus en
sont le lien contractuel. La campagne million (D45, étape d) s'exécute
sur CE périmètre : entrées de têtes hostiles, corps tronqués, autorités
dégénérées, flux de pompe capricieux. Les orchestrateurs (http-10/11/12,
tcp-13) relèvent de l'oracle à scénarios (V2) et du terrain (§ 8.4), pas
du fuzz aveugle — ils n'ont pas d'entrée non fiable DIRECTE : toute
entrée non fiable traverse d'abord un bloc fuzzé.
