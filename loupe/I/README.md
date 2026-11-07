# Couche I — le domaine `loupe` (le test grandeur nature, l'application « Loupe »)

> La couche I du test grandeur nature, écrite avant la notation (R2,
> provenance `écrite-avant-code`). Elle instancie le gabarit § 2.2 de la
> spécification et étendra le registre figé du projet (m0/I/README.md,
> § 2.1) : le domaine **`loupe` est créé, réservé M10** (spécifications
> loupe-01 à loupe-18). L'extension du registre VIT À LA CÉRÉMONIE D'ÈRE
> du TGN — m0 est un arbre SIGNÉ, le geste d'ouverture n'y touche pas :
> la dette de cérémonie est nommée à la naissance (le modèle D166/D168).
> Les balises scellées demeurent immuables (§ 9) : win 1.0.0 (l'ère
> refermée D170), linux 0.7.0, riscv 0.8.0 ; la lignée Loupe posera la
> sienne — `loupe 0.1.0-dev.1` au premier build du jalon, geste de BUILD
> jamais scellage (miroir M6/M7/M8).

L'ouverture est la décision du développeur (D171, le modèle D149/D160) :
« on peut commencer le test grandeur nature : coder une appli entièrement
avec Triade. ça n'empêchera pas de continuer le projet Coffre Fort en
parallèle ». Le protocole a prouvé CHAQUE capacité, M0 à M9 — l'outil de
validation l'a fait naître et le septième run l'a scellé (1.0.0, la
session réelle). Le TGN est l'épreuve de la MÉTHODE ENTIÈRE sur une
application réelle NEUVE : le modèle RoomEq (v0.3) s'arrêtait au RECODAGE
d'une application existante ; le TGN exige la CRÉATION — de l'intention
(cette couche I) à l'octet livré (le kit terrain), chaque geste prouvé.

## L'application : « Loupe », l'éditeur hexadécimal au panneau d'empreintes

L'application n'était pas nommée par le message d'ouverture : le choix est
ARBITRÉ (D171) et CONTREDISIBLE au message suivant — la couche I seule
vit, rien n'est scellé, un contre-ordre rouvrirait le choix sans rien
défaire. Les raisons de l'arbitrage :

1. **L'OUTIL DU QUOTIDIEN** — toutes les pièces du projet vivent par leurs
   empreintes (md5/sha-256 consignées à chaque geste, les témoins, les
   artefacts, les bundles) ; Loupe les rend À L'ŒIL : voir les octets,
   leurs lignes, leurs empreintes, leur place. La première application
   du TGN est l'application que le projet utilise déjà tous les jours —
   en ligne de commande, au labo.
2. **L'ÉPREUVE COMPLÈTE** — CINQ familles d'exigences dans UN artefact :
   l'interface graphique (l'héritage démo win-*), les fichiers (lire et
   écrire AUX octets), le hachage cryptographique (l'héritage de la
   famille sha du domaine tls13 — R7, PAR LA CARTE), la libc (l'héritage
   M1), la recherche et l'édition. Aucune capacité ne reste à l'état de
   démonstration : l'application les EXIGE toutes, ensemble.
3. **LE PÉRIMÈTRE TENABLE** — 18 blocs, un jalon (M10), livrable en kit
   terrain au développeur (le modèle m9f : double-clic, témoin, /test).
   L'application est COMPLÈTE à la 0.1.0 sans être démesurée : un fichier
   de 2 Gio s'ouvre (jamais tout en mémoire), l'empreinte se calcule par
   fenêtres glissantes.
4. **LE NEUF** — pas un recodage : une application qui n'existe nulle part
   ailleurs, née de cette couche I.

## Le tableau des blocs (18, cinq familles)

| Bloc | Nom | L'intention en une phrase |
|---|---|---|
| loupe-01 | ouvrir | ouvrir le fichier (le chemin donné), rendre la poignée et la taille — les refus nommés (absent, verrouillé) |
| loupe-02 | lire | lire une fenêtre d'octets à un décalage donné, dans le tampon de session — BORNÉ, jamais un octet de trop |
| loupe-03 | fermer | fermer proprement — jamais une poignée pendante, quel que soit l'état |
| loupe-04 | cadre | le cadre de session : la structure unique (chemin, taille, position, tampon, marque sale) que tous les blocs partagent |
| loupe-05 | sha256 | le flux SHA-256 d'une gamme — l'héritage tls13 sha PAR LA CARTE (R7), jamais une copie d'octets |
| loupe-06 | md5 | le flux MD5 d'une gamme — l'empreinte du quotidien du projet, toutes ses pièces la portent |
| loupe-07 | cumul | les empreintes du fichier ENTIER par fenêtres glissantes — un fichier de 2 Gio passe, jamais tout en mémoire |
| loupe-08 | ligne | composer UNE ligne hexadécimale (décalage + 16 octets + le miroir ASCII) — tampon fixe, aucun débordement |
| loupe-09 | ecran | la disposition de l'écran : entête de colonnes, grille, barre d'état — les zones DÉCLARÉES avant la première goutte de peinture |
| loupe-10 | peinture | WM_PAINT — dessiner la fenêtre visible (l'héritage démo, l'IAT gdi32/user32) |
| loupe-11 | defilement | la molette et l'ascenseur — le décalage de vue BORNÉ à la taille réelle |
| loupe-12 | aller | aller à un décalage (saisie hexadécimale) — le refus NOMMÉ hors bornes, jamais un saut silencieux |
| loupe-13 | recherche | chercher une suite d'octets depuis la position — l'algorithme pur, prouvé au labo avant tout embarquement |
| loupe-14 | suivant | l'occurrence suivante — et la FIN NOMMÉE quand il n'y en a plus |
| loupe-15 | curseur | la cellule active — déplacement clavier, surbrillance, jamais perdu hors écran |
| loupe-16 | saisie | écrire un octet dans le tampon — la marque SALE posée, le geste réversible avant sauvegarde |
| loupe-17 | sauver | enregistrer les octets modifiés — l'écriture À L'OCTET, la marque levée, le témoin de ce qui a bougé |
| loupe-18 | quitter | la sortie propre — fermer, détruire, aucun octet perdu, aucune fuite |

## Les conventions transverses (charte du domaine)

1. **Écrit-avant-code (R2)** — les 18 spécifications sont posées AVANT
   toute notation (le chantier M10-(a)) ; aucun octet de code ne naît
   sans son contrat. Les révisions vivantes (R3+) suivent la discipline
   du projet : nommées, motivées, consignées.
2. **L'héritage PAR LA CARTE (R7)** — minilibc (M1), la famille sha
   (tls13), les feuilles win de la lignée démo : l'héritage est DÉCLARÉ
   au plan d'adressage et EMBARQUÉ au build, JAMAIS copié-collé — les
   octets hérités sont byte-identiques à leur scellé d'origine, l'oracle
   le constate.
3. **L'oracle à scénarios + le harnais différentiel** — les familles
   pures (ligne, recherche, empreintes) se prouvent au harnais
   différentiel sur vecteurs (le modèle M4/M5 : FIPS 180-4 pour les
   hash, les fixtures du dépôt pour les lignes) ; l'application entière
   se prouve à l'oracle à scénarios (le modèle M3+ : l'écran attendu
   octet par octet pour des états donnés) ; la falsification est
   DEMANDÉE (une mutation doit être attrapée).
4. **Les budgets déclarés avant la notation** — tailles, slots, zones :
   le plan d'adressage (layout) est ARRÊTÉ sur les longueurs réelles
   AVANT la première notation (le modèle D161) ; un bloc qui dépasse son
   budget est un refus nommé, pas un ajustement silencieux.
5. **Le kit terrain (le modèle m9f)** — l'artefact part au coffre /test
   en kit double-clic avec son LISEZMOI et son réceptacle de preuves ;
   le développeur court LOUPE sur SA machine, le témoin revient au
   réceptacle, le recoup labo tranche sur pièces. L'application finit
   chez son utilisateur — c'est ÇA, le grandeur nature.
6. **La balise** — `loupe 0.1.0-dev.1` au premier build ; la 0.1.0
   finale se scellera sur le run terrain vert recoupé (le miroir
   D165/D170 : la porte est de processus). Loupe est UN PROJET DE
   DÉVELOPPEMENT au sens du coffre (D137).
7. **Les frontières** — AUCUNE clé, AUCUN coffre réel, AUCUN fragment,
   AUCUN arbre scellé touchés ; le proxy 1.0.0 et la carte tls13
   demeurent INTACTS (l'anti-rollback armé) ; le TGN vit sa vie dans ce
   domaine.
8. **La dette de cérémonie (nommée à la naissance)** — le 14e arbre
   (loupe) et l'extension du registre figé (m0/I/README.md § 2.1)
   attendent LA CÉRÉMONIE D'ÈRE du TGN : le geste hors-ligne du
   développeur, la re-signature de m0 au registre étendu (le modèle de
   l'ère M8), le garde passant à 14 arbres VERTS. Jusque-là le garde
   demeure à 13 arbres VERTS — AUCUN arbre signé n'est touché.
9. **L'ABI et la table des verdicts (posée au chantier (a))** — ABI msx64
   du profil primaire `x86-64-win11-pe` : les arguments en rcx/rdx/r8/r9
   puis la pile, le verdict en rax ; l'image PI (D33 — aucune adresse
   absolue), l'IAT kernel32/user32/gdi32 (D7/D35 — 34 feuilles au plan
   d'adressage). LA TABLE DES SEPT VERDICTS (0, −1..−7 — l'échec nommé) :
   **0** OK · **−1** FIN (la fin nommée : la plage est épuisée) · **−2**
   ABSENT (le chemin ne désigne rien) · **−3** HORS-BORNES (hors du
   fichier ou du périmètre 0.1.0) · **−4** SESSION (aucun fichier ouvert)
   · **−5** ENTRÉE (l'ordre est refusé en l'état) · **−6** SYSTÈME (l'OS
   refuse, GetLastError consigné) · **−7** VERROUILLÉ (le partage
   refuse). Les blocs SANS entrée IAT propre : loupe-04 (le memset
   hérité), loupe-07 (la composition), loupe-08 et loupe-13 (les
   feuilles pures — le miroir de la charte tls13 § 7) ; la croissance du
   slot est NOP, 0x90 (la convention de la lignée depuis M0) ; tout
   verdict négatif MONTE À LA BARRE (l'écran nomme ce que le domaine
   refuse).
10. **La barre-saisie et le journal (posées au chantier (a))** — la
   saisie d'aller et de recherche vit À LA BARRE (aucun contrôle enfant :
   l'écran appartient à Loupe) ; l'édition vit AU JOURNAL (256 octets
   distincts, l'entrée par décalage, le disque intact jusqu'à la
   sauvegarde) ; la sortie exige le DOUBLE-GESTE quand la marque sale
   est posée (la perte est une volonté deux fois nommée, jamais un
   accident d'un seul Alt+F4).

## Le tableau du domaine (la découpe préfigurée — D161 : la
## préfiguration n'est pas un droit, les slots/tailles s'arrêtent à la
## notation sur les longueurs réelles ; les identifiants machine i11xxxx
## naissent de la table) — la lignée des identifiants :
## g9 [M8] → h10 [M9] → i11 [M10] — la carte du domaine les portera
## dès sa première génération

| Spécification | Bloc machine (carte) | Rôle | Famille |
|---|---|---|---|
| loupe-01 | i110001 | ouvrir : CreateFileW + la taille, la session née entière (le cadre, la vue, le panneau) | fichier |
| loupe-02 | i110002 | lire : la fenêtre de 384 o au tampon, bornée, le recouvrement du journal | fichier |
| loupe-03 | i110003 | fermer : la poignée rendue, les zones d'hygiène vidées, idempotent | fichier |
| loupe-04 | i110004 | le cadre : la structure unique (960 o) posée vierge — la disposition source unique | fichier |
| loupe-05 | i110005 | sha256 d'une gamme : tls13-01..04 PAR LA CARTE, les fenêtres de 64 Kio | empreintes |
| loupe-06 | i110006 | md5 d'une gamme : la notation neuve (RFC 1321, les tables dérivées par arithmétique) | empreintes |
| loupe-07 | i110007 | le cumul : MD5 + SHA-256 du fichier entier au panneau (la composition seule) | empreintes |
| loupe-08 | i110008 | la ligne : 77 o exacts — le décalage, les 16 groupes, le miroir ASCII (feuille pure) | rendu |
| loupe-09 | i110009 | l'écran : WinMain, la vitrine, LA PROCÉDURE, les trois zones déclarées (2320 o) | rendu |
| loupe-10 | i110010 | peinture : WM_PAINT, l'unique peintre — composer l'ECRAIN puis TextOutW, la cellule en inverse | rendu |
| loupe-11 | i110011 | défilement : la molette (3 lignes/cran) et l'ascenseur, bornés — la dernière fenêtre voit la fin | rendu |
| loupe-12 | i110012 | aller : la barre-saisie hexa, le saut exact, LA RÈGLE DE RECADRAGE (citée par 14/15) | navigation |
| loupe-13 | i110013 | recherche : l'algorithme pur — la première occurrence par memcmp hérité, ou FIN (feuille pure) | navigation |
| loupe-14 | i110014 | suivant : l'occurrence suivante au fichier, le recouvrement de frontière, la FIN nommée | navigation |
| loupe-15 | i110015 | curseur : la cellule active, les bords nommés (le clamp), la vue suit — jamais perdue | édition |
| loupe-16 | i110016 | saisie : l'octet au journal (par décalage, remplace), la marque sale, le disque intact | édition |
| loupe-17 | i110017 | sauver : chaque octet à son décalage (WriteFile 1 o), la marque levée, le panneau re-naît, le témoin | édition |
| loupe-18 | i110018 | quitter : le double-geste garanti (la perte est une volonté), DestroyWindow, la sortie sans fuite | édition |

L'héritage PAR LA CARTE (charte § 2) déclaré au plan d'adressage : la
famille sha tls13 (tls13-01..04, scellée 1.0.0), la minilibc M1
(libc-01 memcpy, libc-02 memcmp, libc-07 memset) et la
boucle de messages de la démo (win-03, scellée) — **embarqués au build
byte-identiques AUX ADRESSES SCELLÉES D'ORIGINE** (la règle du chantier
(b) : les octets hérités ne bougent JAMAIS d'un pouce — le tls13-02
scellé porte « lea rbp, [rip - 0x91a4] », un déplacement RIP codé pour
son adresse 0xC080 qui vise la table K[64] @0x2F00 : une relocalisation
ré-écrite serait une contrebande de R7 ET un déplacement faux ; le plan
d'adressage réserve donc .text 0x1000-0x1FFF la minilibc aux adresses M1,
0xC000-0xC3C0 la famille sha aux adresses M9, K[64] @0x2F00 la table du
scellé), jamais copiés (l'héritage déclaré est l'héritage utilisé :
chaque entrée est citée par ses specs). **Le chantier (a) est COMPLET : les 18
spécifications sont POSÉES** (révision 1, provenance écrite-avant-code,
le gabarit § 2.2 aux sept blocs, chaque exigence reliée à son vecteur)
— le plan d'adressage (loupe/layout.py) arrête la table des verdicts,
le cadre, le format de ligne, les tables MD5 dérivées par arithmétique,
les zones .data, l'héritage et l'IAT ; l'instrument du chantier
(scripts/verifier_specs_m10a.py) constate le tout sur pièces. **Le
chantier (b) est COMPLET : le noyau loupe-01..07 NOTÉ-MESURÉ-PROUVÉ**
(fichier + empreintes : la notation 47/388/296/122/312/879/102 o aux
slots ARRÊTÉS sur les mesures — D161 rejoué, le mode --mesurer de
l'auteur ; loupe-06 LA NOTATION NEUVE RFC 1321 : les 64 tours, les 4
rounds, le couplage, le bourre, l'extraction — le plus grand bloc du
noyau, 879 o ; les révisions nommées de loupe-01 : r2 l'erratum de la
taille de la pièce [65 024 o], r3 LE VIDE [le fichier de taille zéro
s'ouvre sans fenêtre, son panneau existe : d41d8cd9… + e3b0c442…]) ;
l'instrument loupe/harnais_noyau.py — LE MINI-OS VIRTUEL (les six shims
kernel32 du noyau, le système de fichiers virtuel aux témoins réels
dont proxy.exe scellé, les échecs paramétrables, le journal des gle)
— 59 contrôles · 59 VERTS × 3 graines : les SEPT vecteurs RFC 1321 au
fichier, 1 000 gammes md5 + 200 sha contre hashlib, LA PIÈCE DE L'ÈRE
JUGÉE PAR SA PROPRE APPLICATION (loupe-05 sur proxy.exe scellé ==
446279f3…), l'héritage R7 CONSTATÉ BYTE-IDENTIQUE (la double preuve :
les extraits des scellés ET les notations d'origine ré-assemblées),
les ONZE rejets nommés, la falsification attrapée par les vecteurs
officiels. R2 tenue : AUCUN build — la cérémonie d'ère précède (le 14e
arbre, la dette D166/D171 demeure).

**Le chantier (c) est COMPLET : les familles rendu + navigation
loupe-08..14 NOTÉES-MESURÉES-PROUVÉES** — LE CRITÈRE DU PLAN TENU :
*l'oracle à scénarios VERT (l'écran attendu octet par octet pour des
états donnés) ; la falsification attrapée*. La notation 271/1614/568/
796/126/983/874 o aux slots ARRÊTÉS sur les mesures (D161, la troisième
passe : tassés à la contiguïté du noyau 0x49C0→0x5F80 — loupe-10 LE
PLUS GRAND BLOC DU GESTE, 1614 o ; loupe-09 DERNIER du tassement : le
bloc d'entrée dont la table de routage S'ÉTENDRA au chantier (d) sans
cascade sur les autres notations, la révision nommée à venir). LES
HÉRITAGES AUX ADRESSES SCELLÉES (la règle du geste (b) exécutée) :
libc-02 memcmp @0x1180 (loupe-13 — chaque candidat du scellé M1) et
win-03 LA BOUCLE @0x15C0 (loupe-09 — les octets de demo.exe 0.3.0, ses
TROIS déplacements RIP visant l'IAT démo réservée @0x2818/0x2820/
0x2828 : la double entrée n'est pas une redondance, c'est le PRIX du
déplacement scellé) — la DOUBLE PREUVE R7 : les extraits des scellés ==
les octets émulés ET les notations d'origine ré-assemblées == les
extraits. L'INSTRUMENT loupe/harnais_rendu.py — LE MINI-GUI VIRTUEL
(la file de messages SCRIPTÉE, le Dispatch qui APPELLE LA PROCÉDURE au
pointeur enregistré — la mécanique d'USER32 réduite au laboratoire,
la réponse par l'adresse magique ; le DC qui ENREGISTRE chaque goutte
avec ses couleurs ; la police mesurée une fois ; les échecs
paramétrables ; ExitProcess qui termine) — 53 contrôles · 53 VERTS ×
3 graines (20261108, 424242, 777777) : le doré (la première ligne de
proxy.exe + la ligne finale incomplète du témoin 3f) + 1 500 lignes
différentielles == le modèle indépendant ; le corpus de l'école +
1 500 cas == bytes.find ; LA CHAÎNE au fichier entier + LE
RECOUVREMENT PAR CONSTRUCTION (un témoin où l'occurrence n'existe QU'à
cheval sur chaque frontière de 64 Kio : TROUVÉE — **LE PLANCHER QUI NE
RECULE JAMAIS**, la correction du premier jet, attrapée par le témoin
à frontières : une fenêtre manquée y avance le premier départ non
examiné, jamais le muté ne re-trouve l'occurrence courante) ; les
bornes rejouées (vue_max/clamp sur 10 000 tailles) ; LES SCÉNARIOS DE
LA VITRINE (la file scriptée : WM_PAINT/WM_SIZE/WM_VSCROLL/
WM_MOUSEWHEEL/F5/F3/WM_CHAR chez leurs blocs, les appels comptés,
DefWindowProcW pour le reste ; l'écran attendu OCTET PAR OCTET sur les
2320 o — la vitrine vide, le témoin ouvert par la ligne de commande
lue À LA MAIN, la cellule active INVERSÉE à l'abscisse exacte, la
marque sale nommée ; le refus à l'ouverture « fichier introuvable » à
la barre, la vitrine VIDE VRAIE ; E1/E2 : l'explication fatale PUIS
ExitProcess(1), la boucle jamais lancée) ; LA FALSIFICATION DANS LES
DEUX SENS (le remplissage d'espaces muté → l'écran diverge ; la
constante de recadrage mutée → le saut diverge ; la table HEX mutée →
chaque ligne diverge ; LE RECOUVREMENT MUTÉ → l'occurrence à cheval
MANQUÉE puis, restauré, TROUVÉE — l'anti-muet aux 332 positions). LES
LECTURES DU GESTE consignées (D174) : la barre-état aux QUATRE modes
(MESSAGE = aucune saisie + le refus nommé au tampon — le « mode = 0 »
des specs se lit LA SAISIE FERMÉE) ; la barre ANCRÉE AU BAS (le
panneau d'empreintes TOUJOURS visible — la grille cède la place,
lignes_affichables − 3) ; le tiret ASCII et le point médian 0xB7
(l'expansion latin-1 I4 de loupe-10 n'élève que 0x00-0xFF, l'ém-dash
U+2014 ne vit qu'aux chaînes UTF-16 pilotées aux API) ; les codes de
contrôle 0x06/0x07 par WM_CHAR (Ctrl+F/Ctrl+G — aucune feuille
GetKeyState au plan, l'état du clavier ne se sonde pas) ; le cadre RBP
de loupe-10 (les sous-routines locales partagent le cadre — chaque
local à son déplacement STABLE, le 5e argument des TextOutW dans la
zone libre du bas) ; le hInstance de l'ABI de WinMain
(GetModuleHandleW attend son geste, le mort le garde). R2 tenue :
AUCUN build — la cérémonie d'ère précède (le 14e arbre, la dette
D166/D171 demeure).

## Ce que le domaine promet (et comment il se preuve)

La promesse est MESURABLE et TRIPLE :

- **STRUCTURELLE** — chaque bloc porte sa spécification AVANT ses octets
  (R2), ses adresses déclarées AVANT sa notation, ses héritages
  byte-identiques à l'origine (R7) : l'oracle du jalon le constate sur
  les octets et sur la carte ;
- **D'OBSERVABLE AU LABO** — les familles pures rendent les vecteurs
  officiels octet pour octet (FIPS 180-4), l'écran attendu est rendu
  octet par octet pour des états donnés, la falsification est attrapée ;
- **D'OBSERVABLE CHEZ LE DÉVELOPPEUR** — le kit terrain s'ouvre d'un
  double-clic sur SA machine, charge SES fichiers, rend leurs empreintes
  — recoupées contre l'outil du labo — et rend son témoin au réceptacle
  du coffre /test ; le recoup sur pièces tranche (le modèle de chaque
  jalon depuis M4).

La preuve finale du TGN n'est pas « l'application tourne » — c'est :
**l'application vit chez son utilisateur, et chaque geste de sa naissance
est prouvé sur pièces.** C'est la méthode TRIADE entière, au grandeur
nature.
