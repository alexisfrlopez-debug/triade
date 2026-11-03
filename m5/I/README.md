# Couche I — jalon M5 (outil complet) : les trois révisions du relèvement (0.6.0)

> État du jalon (PLAN_MILESTONES) : **(a) empreintes par build — RÉALISÉ
> (D134)** ; **(b) interception en VM isolée — EN COURS (D136, 31/10)** :
> l'autorité de test locale LIVRÉE et PROUVÉE au laboratoire (m5/autorite/,
> 13 contrôles), le kit VM étape 1 LIVRÉ au terrain (m5/vm/) et PROUVÉ EN
> RUN DEUX FOIS (v7 puis v8 — jalon 0.5.1 CLOS, verdicts OK 0 réserve ;
> le décor « parefeu muet » est verrouillé par la section 0bis v8, D142/D143).
> Les trois révisions http-08:R3 / http-10:R3 / http-12:R3 ci-dessous sont
> l'ÉCRITURE-AVANT-CODE du flux navigateur — la notation les porte en .text4 ;
> **(c) patch à chaud du journal — pas ouvert**.

## Ce qui tient en trois révisions (l'arbitrage D136, inchangé)

Le navigateur parle « http:// » absolu au mandataire explicite ; le proxy
RELEVÉ la cible vers l'HTTPS de l'hôte demandé et la traverse par le tunnel
M4 TEL QUEL (tls-08, Schannel, aucune contrebande dans le scellé). Le MITM
CONNECT / tunnel serveur reste REJETÉ (D136 : un domaine
AcceptSecurityContext entier pour un résultat que le relèvement atteint avec
l'existant prouvé). La composition du scénario (b) vit dans m5/I/README.md
(depuis D136) — le présent document n'y ajoute que les conventions que la
notation a dû ARRÊTER (les questions ouvertes de D136 trouvent ici leur
réponse écrite-avant-code).

## RENUMÉROTATION (verdict v8)

L'intention de D136 disait « http-12:R2 » ; le nom est PRIS par le câblage
D95 (embarqué 0.5.1, R7). La révision CLI est **http-12:R3**, ancêtre
http-12:R2. Les deux autres numéros de D136 (http-08:R3, http-10:R3) étaient
libres et restent.

## Conventions transverses (charte des révisions 0.6.0)

1. **La politique est un ÉTAT, jamais un paramètre caché** — R_POLITIQUE
   (.data 0x3860, u64) est écrit UNE fois par http-12:R3 au démarrage (avant
   toute initialisation), lu par http-10:R3 et passé en CINQUIÈME argument à
   http-08:R3 (feuille pure : aucune lecture .data, I1 de sa spec). Sans
   politique armée : R2 OCTET POUR OCTET sur tout chemin (le différentiel
   d'ancêtre R1/R3 rejoué à politique absente exige ZÉRO écart — l'oracle
   le vérifie ligne de console comprise).
2. **La ligne de flux est une pièce d'interception** — elle naît AVEC la
   politique (Q7 de http-10:R3) : sans elle, le journal du chemin M3 scellé
   reste identique à l'artefact (anti-régression R7 au niveau du journal).
   Elle appartient au **JOURNAL tcp-11** (arbitrage de la question T5 de
   D136, consigné au contrat http-10:R3 : émise par la session, modèle
   tcp-11 — états nommés, zéro secret, charte § 3 ; http-11 est la console
   interactive et ne porte rien de la session).
3. **Les compteurs ne mentent pas** — la ligne porte les octets clairs vus
   PAR LA SESSION (entrés : accumulation + corps pompé ; sortis : émissions
   .emettre) ; les octets des relais délégués (HTTP_POMPE R1, tls-08)
   appartiennent à leurs propriétaires exacts et ne sont PAS comptés deux
   fois — sur un relèvement réussi, s=0 est la signature honnête du relais
   tls-08 (consigné au contrat http-10:R3, P8).
4. **Les bornes de ligne sont des états nommés** — tcp-11 borne toute ligne
   (préfixe + 12 + suffixe <= 64, P4) : l'hôte est porté TRONQUÉ à 14
   octets (FLUX_HOTE_MAX, layout) au-delà ; le port du navigateur sur
   http://hote:8080/ est PERDU au relèvement (l'origine est l'HTTPS standard
   de l'hôte, port 443) — la ligne porte le port EFFECTIF, jamais le port
   perdu (consigné http-10:R3 E2/E3).
5. **Le verdict de session est un domaine TOTAL** (layout) : -1 sentinelle
   (pas de ligne), 0 aboutie, 2..7 verdicts tls-08 TRANSPORTÉS TELS QUELS
   (3 = certificat rejeté — LE critère (b) vu du navigateur), 400..505 la
   réponse d'erreur nommée. La LIGNE nomme la CAUSE (verdict tls-08), la
   RÉPONSE nomme l'effet (502) — jamais de remappage muet.
6. **La CLI est une loi, pas un cas** — chaque drapeau futur suivra la même
   loi (D136) : nommé, documenté, CASE-SENSITIVE, refusé s'il n'est pas
   reconnu (ExitProcess 3, ligne « TRIADE M5 : argument inconnu, arret »,
   AVANT toute initialisation). La ligne « relever-https arme » nomme
   l'armement au journal (une fois, entre la bannière et l'écoute).
7. **La porte M5 est le miroir exact de la porte D95** — une table pleine
   d'UNE entrée (0x8000, 0x2000, somme .text4) marchée aux bornes
   (R_TAB_SUM_M5 → R_BORNE_M5), fail-closed sur entrée trouée, la porte se
   garde elle-même ; les tables héritées (28 entrées M3/M4) restent
   marchées à l'identique (Q1 de http-12:R3) — DEUX marches, une version.
8. **Constantes nommées, un seul propriétaire** (T1) — VERDICT_RELEVER = 5,
   FLUX_HOTE_MAX = 14, R_POLITIQUE = 0x3860, ZONE_FLUX_* @+0x7030..0x70EF
   (le trou documenté du cadre R2 — TAILLE_CADRE_SESSION inchangée 0x13390,
   l'ABI P5 et le probing D63 restent exacts).

## Surface de vérification (critère (b))

Les feuilles relèvent des harnais à propriétés hérités (http-08:R3 : le
domaine de http-08:R2 étendu au 5e argument et au verdict 5 — différentiel
R2-sans-politique exigé). L'orchestration (http-10:R3) relève de l'oracle à
scénarios ÉTENDU (D136) : cible relevée saine (ligne de flux exacte, page
relayée, verdict 0), certificat invalide relevé (verdict 3, 502 étiquetée),
politique absente (zéro écart contre R1/R2), ligne de flux vérifiée OCTET
PAR OCTET contre le modèle de composition. L'orchestrateur (http-12:R3)
relève du harnais principal étendu : différentiel R2/R3 (sans argument) +
les scénarios CLI (drapeau, casse mixte, guillemets, inconnu → ExitProcess
3, politique armée → ligne nommée) + le fuzz de la porte M5. Le terrain
(§ 8.4, run M5-b étape 2) jugera : le navigateur du bac à sable, mandataire
127.0.0.1:25000, page http://autorite.test/ — la page servie ET, sur la
cible autonome, la 502 « Certificat rejete » reçue PAR LE NAVIGATEUR.
