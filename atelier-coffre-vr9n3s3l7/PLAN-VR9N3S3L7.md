# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 11, L'INSTRUCTION vr9n3s3l7 : LE DURCISSEMENT DU COFFRE SUR COPIES DE LABORATOIRE (a)–(g) + LE MODÈLE FORMEL

> Pré-enregistré AVANT toute modification (l'empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE11.txt, commitée AVANT le premier geste).
> RÈGLE ABSOLUE : AUCUN coffre réel, AUCUNE phrase réelle approchés — tout
> vit sur copies de laboratoire à phrases de test publiques marquées (D105).

## (a) L'EMPREINTE DU CHIFFRETEXTE AVANT L'AEAD (la sentinelle instantanée)

La sentinelle vérifie aujourd'hui l'AEAD puis agit. LA MODIFICATION : la
vérification d'empreinte du chiffretexte AVANT le déchiffrement AEAD — (1)
CORRUPTION (l'empreinte diverge) = REFUS NOMMÉ SANS DESTRUCTION (le
chiffretexte conservé pour l'analyse — jamais la destruction sur un
incident) ; (2) FALSIFICATION À EMPREINTE VALIDE (l'attaquant réécrit le
chiffretexte ET son empreinte) = DESTRUCTION LOCALE + PROCÈS-VERBAL (la
falsification prouvée = la donnée compromise, la destruction la réponse) ;
les deux chemins testés sur la copie de labo (les vecteurs de corruption et
de falsification générés, les verdicts nommés).

## (b) V_piège DÉRIVÉE (liée à S_piège et à l'époque)

La valeur du piège devient une DÉRIVATION : V_piège = HKDF(S_piège,
"piège" || époque) — liée au secret du piège ET à l'époque ; l'information
de vérification PORTÉE À L'ÉPOQUE (le numéro d'époque dans le témoin). Les
vecteurs : la dérivation re-productible à l'époque courante, l'époque
retirée REFUSÉE nommément (anti-rollback au piège).

## (c) LA CÉRÉMONIE DE RE-PARAMÉTRAGE ARGON2 (l'agilité) + LE PLANCHER D'ENTROPIE

La cérémonie : les paramètres Argon2 (mémoire, itérations, parallélisme)
VERSIONNÉS AU CONTENEUR ; la migration = nouvelle cérémonie (l'ancienne
vérifiée, les paramètres neufs dérivés, le conteneur ré-écrit, le
témoin d'époque ancré). LE PLANCHER D'ENTROPIE DE PHRASE vérifié À LA
CÉRÉMONIE : l'estimation d'entropie (le dictionnaire des mots courants,
la longueur, les classes) REFUSANTE sous le plancher nommé (≥ 60 bits la
référence — la valeur gelée au plan de la cérémonie).

## (d) LA CÉRÉMONIE CHANGER-PHRASE CF3 SOUS SÉQUESTRE

La procédure : la phrase changée PAR LA CÉRÉMONIE CF3 (la copie de labo) —
le changement exige la reconstitution À FROID des parts (le seuil 5/3), la
nouvelle phrase vérifiée au plancher d'entropie (c), le conteneur migré,
l'ancienne phrase DÉTRUITE localement avec PV. La phrase JAMAIS écrite au
dépôt (la règle D223 — le refus nommé de la réécriture au dépôt).

## (e) LE BLOC NATIF SCELLÉ « GARDE RAM »

Le bloc garde-RAM écrit SOUS LE PROTOCOLE : la spec I (le contrat : la
page verrouillée mlock/VirtualLock, la destruction SecureZeroMemory/
explicit_bzero, l'exclusion des dumps — le refus nommé si l'OS refuse) ;
la notation x86-64 (les appels à l'interface du profil — IAT win11, syscalls
linux en miroir) ; la vérification par émulation (Unicorn : les effets
observés — la page verrouillée simulée par les hooks, la destruction
vérifiée octet pour octet) ; le scellage en copie de labo ; le terrain au
geste du maître (Windows réel — le gap nommé).

## (f) L'ANCRAGE REKOR/RFC 3161 DES TÉMOINS D'ÉPOQUE (l'extension D219)

L'ancre : le témoin d'époque (le hash du registre) soumis à L'UN des deux
mécanismes — (1) RFC 3161 : la requête de timbrage au TSA (le hash seul
jamais le contenu, la réponse vérifiée à la clé publique du TSA) ; (2)
Rekor : l'entrée au journal de transparence (le hash, l'inclusion prouvée
à la checksum signée). La vérification MACHINE : le timbre recoupé, la
réécriture du témoin REFUSÉE. La connectivité du bac à l'un des deux =
la tentative vécue ; si les deux sont injoignables, L'ÉCART NOMMÉ (le kit
livré, l'ancrage au geste du maître — jamais simulé).

## (g) LE PROTOTYPE FIDO2 HMAC-SECRET (le média)

Le prototype : le protocole dérivé (le médiateur FIDO2 hmac-secret — la
dérivation de la part locale par le token, le CTAP2), le code de labo (la
surface d'appel, la vérification), les vecteurs synthétiques (les clés
dérivées re-productibles aux vecteurs RFC 8236-style). LE TOKEN PHYSIQUE au
geste du maître (le gap nommé — le prototype livré, jamais l'achat simulé).

## LE MODÈLE FORMEL (la mise à jour consécutive)

Le modèle CF3 (TLA+) étendu : les nouvelles actions (la vérification
d'empreinte AVANT AEAD, la dérivation V_piège à l'époque, la cérémonie
d'agilité, le changement sous séquestre) ; l'invariant inductif étendu ;
l'alignement 13 règles re-vérifié (le transpileur strict) ; LES CONTRÔLES
NÉGATIFS : la destruction débordant sur le média (la destruction locale ne
touche JAMAIS les parts — le contrôle qui le tente ATTRAPÉ), la corruption
silencieuse (refusée), l'époque retirée (refusée).

## LA VÉRIFICATION APRÈS MODIFICATION (la lettre de l'instruction)

Les suites CF2/CF3/sceau vertes (re-roulées) ; le modèle étendu
re-déchargé (invariant inductif, alignement 13 règles, contrôles négatifs) ;
la campagne générative re-jouée à zéro divergence ; l'autotest du kit
séquestre vert ; l'ancrage vérifié machine (ou l'écart nommé) ; AUCUN coffre
réel ni phrase réelle approchés ; les décisions append-only.
