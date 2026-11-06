# Couche I — jalon M8 (syscalls directs, l'ère 0.9.0 des additions mesurées)

> Trois spécifications nouvelles, écrites avant la notation (R2, provenance
> `écrite-avant-code`). Elles instancient le gabarit § 2.2 de la spécification
> et étendent le registre figé du projet (m0/I/README.md, § 2.1) : le domaine
> **`sys` est créé, réservé M8** (spécifications sys-01 à sys-03). La balise
> scellée win `0.6.0` reste immuable (§ 9) ; l'ère posera la sienne —
> `0.9.0-dev.1` au premier build du jalon, geste de BUILD jamais scellage
> (miroir M6/M7).

Le jalon M8 est la PREMIÈRE famille de l'ère d'après M7 (D160) : le **bloc
optionnel de syscalls directs** sur le profil primaire `x86-64-win11-pe`. Le
plan l'attendait : « chaque addition s'appuie sur des résultats mesurés ». Le
domaine sys est la FONDATION I/O de la souveraineté complète — TLS 1.3 pur
(la seconde famille) s'appuiera sur lui : une pile TLS pure qui émettrait
encore par l'IAT userland garderait la surface de hook qu'elle prétend
éliminer. Les profils additionnels (la troisième famille) hériteraient de
l'IAT de la même façon — l'ordre des familles EST la règle (D160).

## Ce que le domaine promet (et comment il se preuve)

Le profil win parle au système par l'IAT depuis M0 (WriteFile, ExitProcess —
le scellé hello). Le domaine sys ouvre le second chemin : **l'appel direct au
noyau par l'instruction `syscall`**, sans aucun import — le numéro de service
lu à l'exécution dans ntdll ELLE-MÊME. La promesse est MESURABLE et DOUBLE :

- **STRUCTURELLE** — les blocs du domaine ne déclarent AUCUNE entrée IAT :
  leur seule interaction système est l'instruction syscall elle-même ; ntdll
  est LUE (son EAT, ses stubs — de la mémoire directe), jamais APPELÉE.
  L'oracle du jalon (chantier (c)) le constatera sur les octets ;
- **D'OBSERVABLE** — la twin de hello-02 (sys-03) émet LA MÊME LIGNE par le
  second chemin, octet pour octet : la ligne est le FIXTURE PARTAGÉ de la
  lignée (celle de hello-02, jamais une seconde copie). Au laboratoire la
  preuve se joue au harnais sur des FIXTURES ntdll synthétiques (le modèle
  différentiel de M4/M5 — jamais une croyance sur un vrai ntdll absent du
  labo) ; sur le terrain du développeur (le kit du chantier (d), modèle
  m6d/m7d), le run lit le VRAI ntdll de SA machine, le motif est confronté,
  la ligne est comparée — le recoup sur pièces tranche.

## Conventions transverses (charte des syscalls directs)

1. **Le SSN est une DONNÉE, jamais un octet de code** — aucun numéro de
   service n'est gravé dans les octets d'un bloc du domaine ; à l'exécution,
   le numéro vient du RÉSOLVEUR (sys-02), lu de l'EAT de ntdll SUR LA MACHINE
   qui exécute. Les numéros varient par build de Windows : une constante
   gravée serait un mensonge par build, faux en silence sur tout terrain
   d'un autre build. Le laboratoire ne connaît pas le SSN du terrain et ne
   le devine jamais.
2. **Le motif du stub est vérifié avant toute extraction** — le résolveur lit
   le stub à l'adresse donnée par l'EAT et confronte ses quatre premiers
   octets au `MOTIF_STUB` (`4C 8B D1 B8` — `mov r10, rcx ; mov eax, imm32`,
   la graphie des stubs Windows 10/11 x64) AVANT de lire l'imm32 du numéro
   (à `+4`). Toute divergence est un REFUS NOMMÉ (verdict -4 : stub
   inattendu — un hook ou une ère inconnue), jamais un numéro extrait d'un
   stub qui n'est pas celui attendu. La constante vit au plan d'adressage
   (`m8/layout.py`, source unique) ; le laboratoire prouve sur FIXTURES, le
   terrain mesure le VRAI — la version Windows du terrain qui constate le
   motif est CONSIGNÉE au témoin du run.
3. **Aucun IAT dans le domaine** — les blocs du domaine ne déclarent AUCUNE
   entrée d'import : leur seule interaction système est l'instruction syscall
   elle-même (règle STRUCTURELLE ci-dessus). La frontière est explicite :
   l'ère ne prétend PAS à l'IAT-free du PRINCIPAL — le corps hérité 0.6.0
   garde ses imports scellés (R7) ; le domaine sys est la pièce rapportée
   IAT-free, câblée au chantier (c).
4. **L'ABI traversante, un seul remappage** — l'appelant d'un syscall place
   ses arguments EXACTEMENT comme l'API NT les attend (msx64 : rcx, rdx,
   r8, r9, puis la pile à `[rsp+0x28]` au moment du syscall) ; l'émetteur ne
   remappe QUE rcx→r10 (l'instruction syscall détruit rcx — l'adresse de
   retour utilisateur — et r11 — les drapeaux) et ne touche JAMAIS la pile
   entre son entrée et le site syscall : le noyau lit la pile de l'APPELANT,
   l'émetteur n'est qu'un trombone ABI.
5. **Fail-closed intégral, verdicts nommés** — tout NTSTATUS autre que
   STATUS_SUCCESS (0) est un ÉCHEC NOMMÉ du domaine ; jamais un STATUS brut
   propagé comme verdict : le STATUS est CONSIGNÉ À CÔTÉ (miroir de la
   discipline tls-02/D79 — le HRESULT brut n'est jamais muet, il est
   accompagné). La table des verdicts du domaine vit au plan d'adressage :
   `0` résolu/émis ; `-1` le nom est introuvable dans l'EAT ; `-2` la base
   n'est pas un module PE ; `-3` le répertoire export est absent ; `-4` le
   stub diverge du motif ; `-5` le span du nom est invalide ; `-6` le
   syscall a rendu un STATUS non nul (le STATUS rendu est consigné en rdx —
   nommé, jamais muet).
6. **Zéro état détenu** — aucun bloc du domaine ne détient d'état entre deux
   appels : le SSN résolu vit chez l'appelant (qui peut le cacher pour sa
   session — le domaine ne cache rien, miroir de I2 tls-05).
7. **La réserve d'ère** — le domaine vise les builds Windows 10/11 x64 (la
   graphie `4C 8B D1 B8`) ; un terrain d'une autre ère REFUSE NOMMÉMENT
   (règle 2). Le résolveur ne devine jamais et NE S'ADAPTE JAMAIS EN SILENCE :
   pas d'heuristique de secours devant un stub croché — la contre-mesure du
   hooking est un CHANTIER FUTUR NOMMÉ, jamais une contrebande.
8. **La lecture d'EAT est bornée** — la marche des noms s'arrête à
   NumberOfNames (lue une fois, gardée en registre le temps de la boucle) ;
   aucun accès hors des trois tables pointées par le répertoire export
   (AddressOfNames, AddressOfNameOrdinals, AddressOfFunctions) ; la
   comparaison du nom est **libc-02** (memcmp, l'héritage scellé M1 — appel
   direct déclaré, jamais une boucle nouvelle : le domaine ne réécrit pas ce
   que la lignée sait déjà faire).

   *Erratum (M8-(b), sur pièces)* : la couche I naissante citait « libc-04
   (memcmp) » — coquille de citation : memcmp est **libc-02** (b20002), itoa
   est libc-04 (b20004) ; le registre figé m1/I/README.md fait foi. Corrigé
   nommément AVANT la notation (aucun octet n'avait encore été écrit sur la
   citation fausse — la preuve la correction précède l'octet).

## Spécifications nouvelles (génération 8, blocs g9xxxx)

| Spécification | Bloc carte | Rôle | Zone prévue |
|---|---|---|---|
| sys-01:R1 | g90001 | L'émetteur syscall (rcx→r10, syscall, ret — le trombone ABI, six octets) | sys @ .text5, slot 1 |
| sys-02:R1 | g90002 | Le résolveur SSN (l'EAT de ntdll LUE directement, le motif vérifié — la pièce de la fondation) | sys @ .text5, slot 2 |
| sys-03:R1 | g90003 | L'écriture directe — la twin de hello-02 par NtWriteFile (neuf arguments, zéro IAT) | sys @ .text5, slot 3 |

## Le plan d'adressage du jalon (`m8/layout.py`, source unique)

La section **.text5 est NOUVELLE** (0xA000-0xBFFF — SizeOfImage
0xA000 → 0xC000 au build du chantier (c), modèle .text3/.text4) : le corps
hérité 0.6.0 ne bouge pas d'un octet (R7). Les slots sont ARRÊTÉS au
chantier (b) sur les longueurs réelles des notations (**D161**, modèle
D47/D79 : la mesure auteur décide, la préfiguration n'est pas un droit) —
tassés depuis 0xA000 (D8 : multiples de 64, alignés 16, padding >= 16) :
sys-01 @ 0xA000 (0x40 — six octets notés), sys-02 @ 0xA040 (0x140 — 293 o
notés), sys-03 @ 0xA180 (0xC0 — 164 o notés), réserve contiguë
0xA240-0xBFFF (la croissance du domaine). Les fixtures .rdata du domaine
(posées au build (c) dans la zone VIERGE 0x2EB0-0x2FFF du scellé, vérifiée
sur pièces au (b)) : le nom « NtWriteFile » @ 0x2EC0 (11 o), la ligne de
hello-02 @ 0x2ED0 (33 o utiles + NUL, byte-exact le MESSAGE M0), la borne
@ 0x2F00 (fail-closed, miroir D95).

Les constantes du domaine vivent au plan d'adressage — source unique, citée
par les spécifications, jamais recopiée (T5) : le `MOTIF_STUB` et le
décalage du SSN ; les décalages PE/EAT (e_lfanew, le répertoire export, les
trois tables) ; la table des verdicts (règle 5) ; les versions de l'ère
(`0.9.0-dev.1` / `0.9.0` — le plancher R10 demeure 0x00040000, hérité).

## Frontières

Le domaine sys ne touche NI au corps hérité 0.6.0 (R7 — le scellé ne bouge
pas), NI aux lignées des autres profils (unix 0.7.0, riscv 0.8.0 —
INTACTES), NI aux balises (aucune n'est posée par la présente couche I : la
0.9.0-dev.1 viendra du premier build M8, geste de BUILD). La **PEB-walk**
(trouver la base de ntdll sans GetModuleHandleA — l'IAT-free du principal)
est un CHANTIER FUTUR NOMMÉ : en l'état, la base est FOURNIE par l'appelant
(sys-02:R1, P3). La **contre-mesure du hooking** (stubs crochetés) est un
CHANTIER FUTUR NOMMÉ : en l'état, un stub divergent est un refus (règle 7).
TLS 1.3 pur et les profils additionnels demeurent HORS PÉRIMÈTRE jusqu'à
leur ouverture (une décision propre chacun — D160 ne les ouvre pas).

---

# Révision M9-(d) — LE SOCLE SOCKET (l'ère 1.0.0 du transport, le 07/11/2026)

> La présente révision étend le domaine `sys` au chantier M9-(d) du plan :
> la fondation I/O que M8 a nommée (« réserve contiguë 0xA240-0xBFFF : la
> croissance du domaine [sys-04 et suivants] ; TLS 1.3 pur s'appuiera sur
> lui ») — le client TLS 1.3 pur (M9-(b), les 28 blocs notés-mesurés-
> prouvés) attend son socle : une pile TLS pure qui émettrait encore par
> l'IAT userland garderait la surface de hook qu'elle prétend éliminer ;
> le plan M9-(d) le réclame TEL QUEL : « le transport par SYSCALL DIRECT
> (jamais l'IAT ws2_32), l'EAT de ntdll reste la source des SSN (sys-02
> réutilisé), l'établissement/émission/réception par les appels NT du
> transport ». R2 tenue : les TROIS spécifications ci-dessous sont écrites
> AVANT tout octet de notation (provenance `écrite-avant-code`, le geste
> miroir de la couche I fondée à l'ouverture M8) — la notation, le harnais
> et l'arrêt des slots suivront au geste suivant (D161 rejoué), AUCUN
> octet n'est écrit par la présente.

## Ce que le socle promet (et comment il se preuve)

Le transport est le périphérique AFD — le Ring 0 de Winsock — parlé
DIRECTEMENT : le handle d'endpoint naît de NtCreateFile sur
`\Device\Afd\Endpoint` (le nom est une DONNÉE de fixture, jamais un
import), l'échange vit de NtDeviceIoControlFile aux QUATRE IOCTL du
jalon. La promesse est MESURABLE et DOUBLE, miroir de la promesse du
domaine :

- **STRUCTURELLE** — les blocs du socle ne déclarent AUCUNE entrée IAT :
  ws2_32 n'est JAMAIS importé, l'oracle structurel du build (e) le
  constatera sur les octets (la règle 3 TENUE pour le transport) ;
- **D'ÉCHANGE** — les verdicts sont NOMMÉS aux frontières du kit : le
  zéro de réception est LA DEMI-FIN (refus -7), l'émission partielle est
  LE REFUS (-7), le STATUS brut est TOUJOURS consigné (règle 5, la table
  des HUIT) — le socle tls13-28 (M9-(b)) a consigné CES frontières AVANT
  que le socle n'existe : les specs sys-05/06 les instaurent (Q2/Q3 de
  tls13-28 sont le CONTRAT DU KIT, la couche I les cite).

## La charte du transport (§ 9 — les règles transverses, suite de § 1-8)

9. **Le sockaddr est une DONNÉE du kit, en boutisme du FORMAT** — le kit
   construit le sockaddr_in (family en boutisme machine, port et adresse
   en BOUTISME RÉSEAU), le domaine ne convertit JAMAIS en silence (un
   domaine qui convertirait déciderait à la place du kit ; la mesure du
   format fait foi, le kit répond de son boutisme) ;
10. **L'émission est TOTALE ou refusée** — le compteur du IOSB doit
    couvrir la longueur demandée : un envoi partiel est le refus -7
    NOMMÉ, jamais une boucle silencieuse (une boucle d'envoi serait une
    décision de transport que le domaine n'a pas) ;
11. **La réception est BLOQUANTE et le zéro est LA DEMI-FIN** — le handle
    est SYNCHRONE (FILE_SYNCHRONOUS_IO_NONALERT au create : la séquence
    est le contrat de sys-04), la lecture attend ; le compte nul est le
    refus -7 NOMMÉ (le pair a fermé), jamais un succès silencieux ;
12. **Les IOCTL et les structures d'échange sont DES DONNÉES du plan
    d'adressage** — dérivées par la macro canonique (jamais recopiées en
    littéraux de notation, T5), les tailles MESURÉES (20/40/24/12 o), les
    drapeaux MESURÉS (AfdFlags 0x20 au receive : l'erratum de lecture
    consigné à sys-06 — la MESURE en AfdFlags, la littérature en
    TdiFlags, la notation suivra la mesure) ;
13. **Le transport est SANS ÉTAT** — le bloc ne détient rien (règle 6
    TENUE) : ni séquence, ni compte cumulé, ni reste de lecture ; ce que
    le noyau n'a pas livré vit dans la file du NOYAU, jamais chez le
    bloc ;
14. **La fermeture est AU KIT** — « NtClose » résolu par sys-02, émis par
    sys-01 : la fermeture n'est PAS un bloc (le kit orchestre sa
    session), miroir de la règle 6 : l'état vit chez l'appelant.

## Spécifications nouvelles (génération 8 étendue, blocs g9xxxx — suite)

| Spécification | Bloc carte | Rôle | Zone prévue |
|---|---|---|---|
| sys-04:R1 | g90004 | L'établissement — le socket natif par AFD : NtCreateFile (\Device\Afd\Endpoint, EA AfdOpenPacketXX) + le bind implicite WILDCARD + le connect, TROIS SSN résolus au geste même | sys @ .text5, réserve 0xA240 |
| sys-05:R1 | g90005 | L'émission — IOCTL_AFD_SEND, le WSABUF pointant la charge du kit, TOTALE ou refus -7 | sys @ .text5, à la suite |
| sys-06:R1 | g90006 | La réception — IOCTL_AFD_RECEIVE bloquant, le noyau écrit chez le kit, n ≥ 1 ou la demi-fin -7 | sys @ .text5, à la suite |

## La provenance du socle (la couche I la cite — l'instrument la re-dérive)

- les définitions canoniques : **phnt/ntafd.h** — « Ancillary Function
  Driver Definitions », diversenok, Hunt & Hackett, avril 2025
  (systeminformer/phnt, commit 2dda0dd) : AfdOpenPacket,
  _AFD_CONTROL_CODE, AFD_CONNECT_JOIN_INFO_TL (le mode TLI — aucun
  device de transport déclaré : SOCKADDR, PAS TRANSPORT_ADDRESS),
  AFD_BIND_INFO_TL, AFD_SEND_INFO/AFD_RECV_INFO (C_ASSERT : tailles
  égales), AFD_WILDCARDADDRESS, TDI_RECEIVE_NORMAL ;
- les mesures WinDbg **Windows 11 x64** : la série « Under the Hood of
  AFD.sys » (M. Lewczak, leftarcode.com, parties 1-4, juillet-août 2025) :
  le dump du create EA (54 o, EaValueLength 0x1E), le dump du bind
  IMPLICITE mswsock au connect (20 o, flags 2), le dump du connect
  (40 o, les zéros des trois champs acceptés), le dump du send (24 o,
  AfdFlags 0) et du receive (24 o, AfdFlags 0x20) — recopiés OCTET PAR
  OCTET en VECTEURS DORÉS à l'instrument verifier_specs_m9d.py ;
- le laboratoire ne possède AUCUN Windows : la preuve de notation se
  jouera au harnais sur FIXTURES AFD SYNTHÉTIQUES (le modèle
  différentiel M4/M5), le terrain M9-(f) confrontera le VRAI afd.sys de
  la machine du développeur — la version Windows du run consignée au
  témoin (règle 2, la réserve d'ère s'étend au transport).

## Le plan d'adressage étendu (m8/layout.py — la source unique)

Les slots .text5 du socle sont PRÉFIGURÉS dans la réserve contiguë
(0xA240-0xBFFF : « la croissance du domaine » — sys-04 @ 0xA240,
sys-05 @ 0xA540, sys-06 @ 0xA6C0) : l'ARRÊT viendra au geste de la
notation sur les longueurs réelles (D161 rejoué, la préfiguration
n'est pas un droit). Les fixtures du socle vivent en **.text6**
AU-DELÀ des fixtures poignée tls13 (fin 0x10C10) : le nom-device
UTF-16LE @ 0x10C20 (42 o), le EA complet déterministe @ 0x10C50
(54 o), le bind WILDCARD @ 0x10C90 (20 o), les noms de résolution
« NtCreateFile »/« NtDeviceIoControlFile »/« NtClose » @
0x10CB0/0x10CC0/0x10CE0 (SPANS sans NUL) — la réserve .rdata M8 est
ÉPUISÉE par K[64] (Entrée 172, l'ARRÊT nommé tenu : les nouveaux
fixtures en .text6, jamais au-delà de la borne 0x10CF0 sans arrêt).
La table des verdicts passe de SEPT à **HUIT** noms : le -7
TRANSPORT (l'émission partielle, la demi-fin de réception — les
frontières que tls13-28 a consignées AVANT le socle).

## Frontières (la révision)

La présente révision ne touche NI aux spécifications sys-01..03 (les
balises scellées, INTACTES), NI au scellé 0.9.0 (R7), NI aux 28
spécifications tls13 (l'arbre M9 relu VERT — verifier_specs_m9a), NI
aux balises (aucune posée : la 1.0.0-dev.1 viendra du build (e), geste
de BUILD). Le CertificateVerify cryptographique, la PEB-walk et la
contre-mesure du hooking demeurent les CHANTIERS FUTURS NOMMÉS qu'ils
sont. AUCUN octet de notation n'est écrit par la présente (R2 : la
couche I précède — l'instrument verifier_specs_m9d.py en est le juge,
le juge est le code).

## La notation du socle (phase 2 — l'écrit a précédé, la notation a suivi)

La R2 a vécu : les TROIS spécifications ci-dessus ont précédé, la
notation suit. Les brouillons sont assemblés par `outils/auteur.py`
(keystone, rien d'autre — l'arithmétique d'adresses de l'auteur) :

- **sys-04-transport** — 676 o MESURÉS, slot 0xA240/0x300 ARRÊTÉ
  (92 o de NOP) : create + bind WILDCARD + connect, les ONZE/DIX/DIX
  arguments NT, les TROIS résolutions au geste même (l'alternance
  résoudre-émettre × 3 dans les octets), le handle en LOCALE posé à
  [P3] au succès des TROIS gestes SEULEMENT (Q4 : au -6, AUCUNE
  possession partielle) ;
- **sys-05-emission** — 289 o MESURÉS, slot 0xA540/0x180 ARRÊTÉ
  (95 o de NOP) : le WSABUF de pile pointe LA CHARGE du kit (P3
  traverse, AUCUNE copie), TOTALE ou refus -7 (le compte du IOSB
  consigné), la garde -5 AVANT tout ;
- **sys-06-reception** — 287 o MESURÉS, slot 0xA6C0/0x180 ARRÊTÉ
  (97 o de NOP) : AfdFlags = TDI_RECEIVE_NORMAL 0x20 — L'ERRATUM
  TENU (LA MESURE en TROISIÈME champ : la littérature, qui le met en
  TdiFlags, serait REFUSÉE par le noyau strict du harnais), LE ZÉRO
  EST LA DEMI-FIN -7, le noyau ÉCRIT chez le kit.

L'ERRATUM DE NOTATION n° 3 consigné sur pièces : le DesiredAccess
0xC0140000 (bit 31 posé) se charge en `mov edx` ZÉRO-étendu — le
round-trip V1 a attrapé le `mov rdx` fauteur DONT le C7 SIGNERAIT
l'extension (0xFFFFFFFFC0140000 : un refus muet du noyau entier) AVANT
que le noyau simulé ne parle — la preuve a corrigé la notation, la
méthode est la même depuis le geste hkdf.

La preuve : `m8/harnais_sys.py` étendu au noyau AFD STRICT — chaque
geste transport VALIDE ses arguments contre le plan (les VECTEURS
DORÉS rejoués : le EA déterministe, le bind WILDCARD, les zéros du
connect MESURÉS, l'erratum AfdFlags), les verdicts -1/-4/-5/-6/-7
NOMMÉS aux TROIS étages d'échec (le canari de [P3] constate l'absence
de possession partielle), le traceur SOUS-CADRE juge la PROVENANCE de
chaque écriture (les blocs prouvés sys-02/memcmp/sys-01 ou les pushes
des call du bloc — TOUT autre scribble est une faute), la
falsification mute UN point de chaque notation (19 mutantes : les
IOCTL échangés, le sockaddr décalé, l'erratum falsifié DANS LES DEUX
SENS, la demi-fin masquée, la résolution sautée) — **131 contrôles ·
131 VERTS × 3 graines** ; l'instrument `verifier_specs_m9d.py` relu :
**116 VERTS** (phases 1+2 : les specs, les constantes re-dérivées, les
vecteurs dorés, la notation concordante au plan). Le terrain M9-(f)
confrontera le VRAI afd.sys de la machine du développeur.
