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
