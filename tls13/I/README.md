# Couche I — jalon M9 (TLS 1.3 pur, l'ère 1.0.0 de la grande œuvre)

> Spécifications écrites avant la notation (R2, provenance `écrite-avant-code`).
> Elles instancient le gabarit § 2.2 de la spécification et étendent le registre
> figé du projet (m0/I/README.md, § 2.1) : le domaine **`tls13` est créé,
> réservé M9** — l'identifiant `tls` est PRIS par M4 (la poignée Schannel :
> l'échec propre sur certificat invalide) et « un identifiant n'est jamais
> réutilisé ». La balise scellée win `0.9.0` reste immuable (§ 9) ; l'ère posera
> la sienne — `1.0.0-dev.1` au premier build du jalon, geste de BUILD jamais
> scellage (miroir M8 : D162/D163/D165).

Le jalon M9 est la SECONDE famille de l'ère d'après M7 (D160) : **TLS 1.3 pur
en blocs scellés** — « la grande œuvre de la souveraineté complète ». La
demande du développeur « on ouvre la suite » (05/11, au lendemain de la
finale 0.9.0) EST la décision d'ouverture (D166, le modèle D149/D160 :
l'ordre des familles est LA FONDATION D'ABORD). L'appui est MESURÉ : le
domaine `sys` est scellé (0.9.0 — le second chemin preuve, la même observable
sans un seul import), et la couche I du M8 l'avait nommé : « une pile TLS
pure qui émettrait encore par l'IAT userland garderait la surface de hook
qu'elle prétend éliminer ». Les profils additionnels (la troisième famille)
attendent leur décision propre.

## Ce que le domaine promet (et comment il se preuve)

M4 avait prouvé « HTTPS en transit » PAR DÉLÉGATION : la poignée Schannel de
l'OS, conduite par les blocs, l'échec propre nommé sur certificat invalide.
Le jalon M9 referme la boucle : **le protocole TLS 1.3 (RFC 8446) exécuté
par NOS blocs, du ClientHello aux données applicatives — le client entier,
zéro délégation cryptographique**. La promesse est MESURABLE et DOUBLE :

- **DE PRIMITIVES** — chaque brique cryptographique est prouvée au harnais
  sur les VECTEURS OFFICIELS : SHA-256 (FIPS 180-4), HMAC/HKDF (RFC 2104 /
  5869), X25519 (RFC 7748 § 6.1), AES-128-GCM (NIST SP 800-38D, la suite que
  la RFC 8446 exige de toute implémentation). Une brique qui diverge d'un
  vecteur n'est pas une brique ;
- **D'OBSERVABLE** — la poignée ENTIÈRE rejouée au harnais sur le transcript
  RFC 8448 (les octets enregistrés d'une vraie session, la clé attendue par
  étape, le Finished vérifié) ; puis sur le terrain (le kit du chantier (f),
  modèle m6d/m7d/m8d) : la session RÉELLE avec un serveur réel, la ligne
  applicative chiffrée échangée — le recoup sur pièces tranche.

## La suite est arrêtée (et le reste des frontières)

**TLS_AES_128_GCM_SHA256 + x25519** — la suite que la RFC 8446 impose à
toute implémentation et le groupe RFC 7748 : le choix minimal auditable.
Le ClientHello propose CETTE suite seule ; un ServerHello qui en choisit
une autre est un REFUS NOMMÉ, jamais une adaptation silencieuse.

**Le rôle est CLIENT** — le jalon prouve le client (l'initiateur). Le miroir
serveur est un chantier futur nommé, pas une réduction cachée.

**La décision de confiance est une comparaison, jamais une croyance** — le
certificat du serveur est confronté à l'EMPREINTE ÉPINGLÉE fournie par
l'appelant (le kit). L'analyse X.509 complète (la chaîne, les extensions, la
révocation) est un CHANTIER FUTUR NOMMÉ : le jalon ne fait pas confiance en
silence, il compare — et nomme la frontière.

**Le transport vit au domaine `sys`** — les blocs tls13 sont du CALCUL pur :
aucun import, aucun syscall (charte § 7). L'émission/réception réseau est le
chantier (d) : le socle socket sys-04+ (la fondation I/O nommée par M8). Au
harnais, le transport est un SIMULATEUR (les octets servis par fixtures) ;
au terrain, les sockets par syscalls directs — jamais l'IAT ws2_32 (la
surface de hook que M8 a nommée).

## Conventions transverses (charte du domaine tls13)

1. **La suite est une CONSTANTE du plan d'adressage, pas une négociation** —
   TLS_AES_128_GCM_SHA256 (0x1301) et x25519 (0x001d) vivent dans
   `tls13/layout.py` (source unique) ; le ClientHello les propose, le
   ServerHello qui diverge est le verdict -5 (la négociation refusée). Le
   domaine ne propose JAMAIS ce qu'il ne prouve pas.
2. **Chaque brique est prouvée sur les VECTEURS OFFICIELS AVANT usage** —
   le harnais joue FIPS 180-4 (SHA-256), RFC 5869 (HKDF), RFC 7748 (X25519),
   SP 800-38D (GCM) et RFC 8448 (le transcript) ; une composition dont une
   brique n'a pas passé ses vecteurs est un REFUS de composition (le
   harnais l'exige, l'ordre n'est jamais inversé).
3. **Le temps constant est une exigence NOMMÉE par bloc** — tout bloc qui
   touche une DONNÉE SECRÈTE (la clé privée x25519, les clés dérivées, les
   comparaisons de tags et de Finished) s'exécute en temps constant PAR
   RAPPORT À CES DONNÉES : l'échelle de Montgomery sans branche de données,
   le OU cumulatif pour les comparaisons, aucune table indexée par donnée
   secrète. Les données publiques (en-têtes, certificats) ne sont pas
   concernées. La spec de chaque bloc le NOMME ; un bloc qui ne peut pas le
   prouver sur pièces ne naît pas.
4. **Le transcript est la source de vérité de la poignée** — le hash SHA-256
   courant du transcript est mis à jour à CHAQUE message de poignée dans
   l'ordre exact d'émission/réception (RFC 8446 § 4.4.1) ; les dérivals de
   clés (HKDF) le consomment ; le Finished EST le HMAC du transcript — la
   preuve de possession des clés n'est jamais une parole.
5. **L'échec est PROPRE et NOMMÉ** — chaque défaut a son verdict de la table
   des SEPT verdicts (le miroir sys : -1 l'argument invalide, -2 la taille,
   -3 l'état du domaine invalide, -4 la cryptographie divergente [tag AEAD,
   Finished], -5 la négociation refusée, -6 l'épinglage divergent, -7 le
   transport en échec) ; la session meurt SANS émettre autre chose que ce
   que la RFC exige (close_notify quand il est atteignable — jamais un
   octet applicatif après un échec).
6. **Le bloc ne détient RIEN** — tout état est un ARGUMENT (le pointeur),
   jamais une adresse fixe : TLS 1.3 exige des hachages MULTIPLES simultanés
   (le transcript, les dérivations) et des clés par étape ; le modèle `ah` à
   contexte unique d'adresse fixe ne survivrait pas. La disposition de chaque
   contexte est déclarée par la spec qui le définit (miroir ah : H, tampon,
   remplissage, total — les mêmes champs, l'adresse choisie par l'appelant).
7. **Aucun import, aucun syscall** — les blocs du domaine sont du calcul pur
   (l'oracle structurel du jalon : AUCUN IAT PAR BLOC tls13, AUCUN SITE
   SYSCALL — le miroir exact de la règle M8) ; le transport et l'horloge
   vivent au domaine sys, appelés par le principal, jamais dans les briques.
8. **La croissance du slot est NOP, 0x90** (la convention de la lignée win
   depuis M0) ; les zones RÉSERVÉES inter-blocs seules sont int3.

## Le tableau du domaine (la découpe préfigurée — D161 : la préfiguration
n'est pas un droit, les slots/tailles s'arrêtent à la notation sur les
longueurs réelles ; les identifiants machine h10xxxx naissent de la table,
la carte génération 9 les portera)

| Spécification | Bloc machine (carte) | Rôle | Famille |
|---|---|---|---|
| tls13-01 | h100001 | SHA-256 : initialisation du contexte (H0, FIPS 180-4 § 5.3.1) | sha |
| tls13-02 | h100002 | SHA-256 : compression d'un bloc de 64 o (§ 6.2.2) | sha |
| tls13-03 | h100003 | SHA-256 : absorption tamponnée (invariance de découpage) | sha |
| tls13-04 | h100004 | SHA-256 : finalisation — bourrage, longueur, extraction 32 o | sha |
| tls13-05 | h100005 | HMAC-SHA-256 (RFC 2104 : ipad/opad, la clé expulsée à la taille du bloc) | hkdf |
| tls13-06 | h100006 | HKDF-Extract (RFC 5869 § 2.1 : le sel, l'IKM → le PRK) | hkdf |
| tls13-07 | h100007 | HKDF-Expand (RFC 5869 § 2.3 : le PRK, l'info, la longueur) | hkdf |
| tls13-08 | h100008 | HKDF-Expand-Label (RFC 8446 § 7.1 : « tls13 » + étiquette + contexte) | hkdf |
| tls13-09 | h100009 | f25519 : addition réduite (radix 2^51, 5 membres u64) | x25519 |
| tls13-10 | h100010 | f25519 : soustraction réduite | x25519 |
| tls13-11 | h100011 | f25519 : multiplication (l'école, la chaîne de retenue) | x25519 |
| tls13-12 | h100012 | f25519 : propagation des retenues + gel modulo p = 2^255 − 19 | x25519 |
| tls13-13 | h100013 | X25519 : l'échelle de Montgomery (RFC 7748 § 5, sans branche de données) | x25519 |
| tls13-14 | h100014 | X25519 : la clé publique (le clamp du scalaire × le point de base 9) | x25519 |
| tls13-15 | h100015 | AES-128 : déploiement des clés de tour (SP 800-38A, 11 tours) | aead |
| tls13-16 | h100016 | AES-128 : chiffrement d'un bloc (l'arrêt AES-NI nommé — voir la spec) | aead |
| tls13-17 | h100017 | GHASH : la multiplication GF(2^128) (SP 800-38D, sans table par donnée) | aead |
| tls13-18 | h100018 | GCM : sceller (le CTR + le GHASH → le texte chiffré + l'étiquette) | aead |
| tls13-19 | h100019 | GCM : ouvrir (l'étiquette VÉRIFIÉE avant la restitution — jamais l'inverse) | aead |
| tls13-20 | h100020 | L'enregistrement : protéger (le n° de séquence, l'AAD, l'AEAD — § 5.2) | enregistrement |
| tls13-21 | h100021 | L'enregistrement : déprotéger (l'inverse exact, l'échec -4 nommé) | enregistrement |
| tls13-22 | h100022 | La poignée : composer le ClientHello (legacy + key_share x25519) | poignée |
| tls13-23 | h100023 | La poignée : traiter le ServerHello (l'avance du calendrier de clés) | poignée |
| tls13-24 | h100024 | Le calendrier de clés (§ 7.1 : early → handshake → application) | poignée |
| tls13-25 | h100025 | Le Finished : calculer/vérifier (le HMAC du transcript, § 4.4.4) | poignée |
| tls13-26 | h100026 | L'épinglage : confronter le certificat à l'empreinte attendue | poignée |
| tls13-27 | h100027 | Le principal : la machine d'états du client (l'orchestration) | principal |
| tls13-28 | h100028 | Le socle d'appel : le principal ↔ les blocs sys-04+ (le transport) | principal |

Les familles s'héritent par MESURE : `sha` est le miroir win des contrats
`ah-04..07` (M6, la même sémantique FIPS — l'ABI change, l'intention non) ;
`x25519` hérite de l'arithmétique f25519 prouvée par `av-05..11` (M7) — la
notation win ré-écrit, les contrats se citent. **Le chantier (a) est
COMPLET : les 28 spécifications sont POSÉES** — la famille `sha` à
l'ouverture (05/11, Entrée 165), les 24 suivantes au geste du 05/11 au
soir (Entrée 166) : R2 tenue de bout en bout, AUCUN octet de notation
n'existe — la cérémonie de l'ère précède tout build (la dette est nommée,
le garde refuse jusqu'à la remise du développeur, et c'est son travail).

*Erratum (M9, sur pièces, AVANT la notation — le modèle M8-(b) libc-02)* :
la spec av-10 (M7) écrit « 0x7ffffffffffedc » pour le membre 0 de p —
coquille d'ÉCRITURE : quatorze chiffres hexadécimaux feraient 55 bits, un
membre de 51 bits en a treize, et le membre 0 de p = 2^255 − 19 est
0x7ffffffffffed ; l'oracle différentiel d'av-10 (V2 : « p → 0 ») ne
pouvait passer qu'avec la valeur juste — l'écriture seule est fautive,
jamais la notation prouvée. Le miroir M9 (tls13-12) re-dérive les membres
PAR ARITHMÉTIQUE au plan d'adressage (le juge est le code) : la preuve
que le miroir ne copie JAMAIS l'hexadécimal d'une spec, il le re-dérive.

## Le plan d'adressage préfiguré (tls13/layout.py — la source unique)

La 8e section `.text6` suit `.text5` du scellé 0.9.0 (raw 0xAE00, RVA
0xC000 — les SEPT en-têtes existants + le huitième tiennent dans la marge
SizeOfHeaders 0x400 : le constat se refera au chantier (e), le décalage de
packaging D94 n'est pas rejoué). Les versions de l'ère : `1.0.0-dev.1` =
0x01000001 (geste de BUILD), la finale `1.0.0` = 0x01000000 (le scellage est
un fait de carte, D165). Les fixtures .rdata du domaine se posent après la
borne M8 (0x2F00) dans la zone vierge restante — la mesure décide (D161).

L'ère M9 exigera sa CÉRÉMONIE DU SCEAU I (le modèle D162 : le registre figé
m0 s'étend au domaine tls13 — un diff d'intention qui exige la clé hors-ligne
du développeur AVANT tout build ; le garde refusera nommément jusque-là, et
c'est son travail).
