# Couche I — jalon M4 (tunnel chiffré, contrats cryptographiques)

Huit spécifications nouvelles, écrites avant la notation (R2, provenance
`écrite-avant-code`). Elles instancient le gabarit § 2.2 de la spécification
v0.5.1 et étendent le registre figé du projet (m0/I/README.md, § 2.1) : le
domaine **`tls` est créé, réservé M4** (spécifications tls-01 à tls-08) ; les
**révisions http-08:R2 et http-10:R2** étendent le domaine http scellé 0.4.0
dans son seul point de contact avec M4 (schéma https + table de réponses) —
modèle des révisions inter-jalons de la lignée démo (win-02:R2, tcp-07:R3) :
la balise scellée reste immuable (§ 9), la révision vit ici et cite son
ancêtre.

Le jalon M4 exige des **contrats cryptographiques** (PLAN, D45) : chaque
retour de la bibliothèque cryptographique a un comportement défini, chaque
échec est nommé, aucune tolérance d'état n'est silencieuse, aucun secret ne
fuit dans un journal. Les conventions transverses qui suivent lient les huit
spécifications et les deux révisions — chacune y renvoie, aucune ne les
recopie (défaut T5 sinon).

## Conventions transverses (charte des contrats cryptographiques)

1. **Fail-closed intégral** — tout HRESULT SSPI qui n'est pas exactement un
   succès attendu (SEC_E_OK) ou une continuation nommée (SEC_I_CONTINUE_
   NEEDED, SEC_E_INCOMPLETE_MESSAGE, SEC_I_CONTEXT_EXPIRED) traverse tls-02,
   la table UNIQUE des verdicts : verdict nommé → échec propre. Aucun
   « continuer au mieux », aucun silence, aucun HRESULT brut propagé.
2. **Le certificat invalide est un ÉCHEC NOMMÉ** (verdict 3) : réponse
   d'erreur propre au client (http-10:R2 : 502), ligne console sans octet de
   secret, session fermée par compensation — jamais un crash, jamais un
   relais aveugle d'octets non déchiffrés.
3. **Zéro divulgation** — aucun journal ne contient un jeton de poignée de
   main, un fragment d'enregistrement, un tampon clair ou le nom traduit ;
   les lignes console portent des états nommés uniquement (modèle tcp-11) ;
   l'échec d'un appel ne recopie JAMAIS ses tampons.
4. **Compensation exacte** — chaque handle acquis est libéré sur TOUT chemin
   (succès, échec nommé, échec système) ; tls-05 est l'unique propriétaire
   du cycle de vie (Acquire / Delete / Free) ; les autres blocs détiennent
   des handles mais ne les libèrent jamais eux-mêmes — ils les rendent.
5. **Spans partout** (héritage M3) — toute entrée réseau reste un couple
   (ptr, longueur) ; aucune terminaison NUL n'est jamais supposée côté
   réseau. La traduction span → UTF-16 (exigée par pTargetName) existe UNE
   fois : tls-01:Q2 — miroir exact de tcp-13:Q2 (span → chaîne C).
6. **État minimal, propriétaire unique** — le contexte SSPI appartient à la
   session (tls-08) ; le tampon résiduel Extra appartient à tls-07 seul ;
   les tailles de flux (STREAM_SIZES) sont acquises une fois par session par
   tls-06 et nullement ailleurs.
7. **La réponse déchiffrée n'est JAMAIS parsée** (héritage http-10:Q4) — le
   clair délivré par tls-07 est pompé tel quel vers le client ; ce qui
   n'est pas parsé ne peut pas être mal parsé.
8. **Constantes nommées, un seul propriétaire** (T1) — MAX_JETON = 16384
   (tls-03 ; TLS 1.3 enchaîne certificats + fin d'extension sur ~ 16 Kio),
   HOTE_MAX = 255 (hérité tcp-13, borne tls-01), MAX_MESSAGE (propriété de
   tls-06 : la valeur négociée, jamais une constante inventée — la source
   est QueryContextAttributes, pas la spécification).

## Spécifications nouvelles (génération 6, blocs g7xxxx)

| Spécification | Bloc carte | Rôle | Zone prévue |
|---|---|---|---|
| tls-01:R1 | g70001 | Hôte span → UTF-16 (propriétaire T5) | tls @ .text3, slot 1 |
| tls-02:R1 | g70002 | Table des verdicts SSPI (HRESULT → verdict nommé) | tls @ .text3, slot 2 |
| tls-03:R1 | g70003 | Jetons SSPI (SecBufferDesc en cadre propre) | tls @ .text3, slot 3 |
| tls-04:R1 | g70004 | Poignée de main cliente (boucle ISC) | tls @ .text3, slot 4 |
| tls-05:R1 | g70005 | Cycle de vie des handles (acquis/libérés) | tls @ .text3, slot 5 |
| tls-06:R1 | g70006 | Émission chiffrée (tailles + EncryptMessage) | tls @ .text3, slot 6 |
| tls-07:R1 | g70007 | Réception déchiffrée (Extra, incomplet, fin) | tls @ .text3, slot 7 |
| tls-08:R1 | g70008 | Session TLS cliente (orchestration complète) | tls @ .text3, slot 8 |

Le plan d'adressage définitif (étape b du jalon, modèle D47) arrêtera les
RVA exacts dans une nouvelle section .text3 — la zone http s'arrête à
0x5780 (fin prévisionnelle de http-11) et .text2 est complète : l'extension
suivante du plan d'adressage est une section nouvelle, mesurée sur les
longueurs réelles des notations. Sept entrées IAT secur32 (Schannel) sont
ajoutées : AcquireCredentialsHandleW, FreeCredentialsHandle,
InitializeSecurityContextW, DeleteSecurityContext,
QueryContextAttributesW, EncryptMessage, DecryptMessage.

## Révisions du domaine http (scellé 0.4.0 — citées, jamais réécrites)

| Révision | Rôle | Ancêtre |
|---|---|---|
| http-08:R2 | Cible : schéma « https:// » strict minuscule → verdict étendu | http-08:R1 (D46) |
| http-10:R2 | Session proxy : routage https → tls-08 + réponses d'échec TLS | http-10:R1 (D46) |

Les autres spécifications http restent à R1 et SONT réutilisées octet pour
octet (R7) : le parseur, la pompe, la console et l'orchestration ne savent
même pas que le tunnel existe — seul http-08 (forme absolue) et http-10
(routage + table des réponses) changent, chacun d'une révision minimale
qui cite son ancêtre.

## Blocs réutilisés dans proxy.exe M4 (R7, octets identiques)

La totalité des blocs embarqués en M3 (hello-02/03, libc-01..04, tcp-01..06,
tcp-11, tcp-13, http-01..07, http-09, http-11, http-12) à l'exception des
DEUX blocs révisés (http-08:R2, http-10:R2 — notations nouvelles, ancêtres
cités) : proxy.exe 0.5.0-dev partage son squelette avec le scellé 0.4.0, le
verrou croisé attendu couvre les deux générations (carte génération 6).

## Surface de vérification (critère M4)

Les feuilles pures (tls-01, tls-02, tls-03) et les boucles à shims (tls-04,
tls-06, tls-07) relèvent du harnais à propriétés (V3 hérité de D45 : survie,
terminaison, verdict conforme au modèle, aucune écriture hors cadre) avec
des générateurs d'HRESULT hostiles (toutes les valeurs non documentées, les
jetons tronqués, les Extra incohérents). L'orchestration (tls-08, http-10:R2)
relève de l'oracle à scénarios : poignées de main complètes, certificat
invalide (SEC_E_ non nul simulé), fin de contexte, échec système au pire
moment — chaque scénario se termine par une compensation EXACTE (handles,
sockets, threads) constatée par l'oracle. Le terrain (§ 8.4) jugera :
curl https:// par le proxy, puis certificat invalide → 502 propre.
