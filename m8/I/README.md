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
   comparaison du nom est **libc-04** (memcmp, l'héritage scellé M1 — appel
   direct déclaré, jamais une boucle nouvelle : le domaine ne réécrit pas ce
   que la lignée sait déjà faire).

## Spécifications nouvelles (génération 8, blocs g9xxxx)

| Spécification | Bloc carte | Rôle | Zone prévue |
|---|---|---|---|
| sys-01:R1 | g90001 | L'émetteur syscall (rcx→r10, syscall, ret — le trombone ABI, six octets) | sys @ .text5, slot 1 |
| sys-02:R1 | g90002 | Le résolveur SSN (l'EAT de ntdll LUE directement, le motif vérifié — la pièce de la fondation) | sys @ .text5, slot 2 |
| sys-03:R1 | g90003 | L'écriture directe — la twin de hello-02 par NtWriteFile (neuf arguments, zéro IAT) | sys @ .text5, slot 3 |

## Le plan d'adressage du jalon (`m8/layout.py`, source unique)

La section **.text5 est NOUVELLE** (préfigurée 0xA000-0xBFFF — SizeOfImage
0xA000 → 0xC000 au build du chantier (c), modèle .text3/.text4) : le corps
hérité 0.6.0 ne bouge pas d'un octet (R7). Les slots préfigurés (D8 —
multiples de 64, alignés 16, padding >= 16) : sys-01 @ 0xA000 (0x80),
sys-02 @ 0xA400 (0x400), sys-03 @ 0xB000 (0x800), réserve 0xB800-0xBFFF —
**les RVA et tailles définitifs seront ARRÊTÉS au chantier (b) sur les
longueurs réelles des notations** (modèle D47/D79 : la mesure auteur
décide, la préfiguration n'est pas un droit).

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
