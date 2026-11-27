# PLAN GELÉ — CAMPAGNE AU POSTE RÉEL (le kit 1-clic : W29DECCO + W29FAMILLE au geste compute)

> La SUITE de l'Entrée 442 : « les campagnes au geste compute du poste réel (la
> campagne contrainte du plan w29decco, la seconde famille du plan w29famille —
> les harnais livrés) », la commande du maître « va enchainer sur la campagne au
> poste réel puis cérémonie, comme d'habitude avec GUI 1 clic ». Le présent plan
> gèle LE KIT DE LIVRAISON avant toute pièce. Les plans gelés PLAN-W29DECCO.md
> et PLAN-W29FAMILLE.md demeurent LA LOI des campagnes (aucune cible re-tirée,
> aucune graine re-tirée, aucun chiffre fabriqué au bac).

## Le kit

**TRIADE_kit_campagne_poste_v100** — un dossier auto-suffisant, un clic
(`COMMENCER-ICI.bat`), pour le poste réel du maître (la machine qui porte le
compute : le modèle choisi **Qwen/Qwen2.5-Coder-7B-Instruct**, identifiant et
empreintes consignés au plan W29DECCO — tokenizer.json c0382117…, config.json
c0242402…, portés byte-byte au harnais du kit).

1. LA FORME (les patrons vécus : le pousseur 1-clic des Entrées 429-430, le
   kit terrain v0150, la maquette parfaite de W27DECCO) :
   - `COMMENCER-ICI.bat` — LE CLIC UNIQUE : il trouve Python 3.10+, bâtit le
     venv, installe `llguidance` + `tokenizers` (+ `keystone-engine` +
     `capstone` pour le round-trip de l'éditer), ouvre la GUI ;
   - `gui_campagne.py` — LA GUI (tkinter, stdlib seule, zéro pip — le patron
     ceremonie_gui.py D87) : l'état du kit, l'endpoint du modèle local, le
     journal en direct, CINQ boutons — Vérifier le kit · Le gate · Le canari ·
     LA CAMPAGNE · Le zip de preuves ;
   - `moteur_campagne.py` — LE MOTEUR (toute la logique, exécutable en CLI —
     la GUI ne fait que l'appeler ; le bac éprouve le moteur, la GUI suit) ;
   - `maquette_endpoint.py` — LA MAQUETTE (le bord scripté OpenAI-compatible :
     le chemin vert de W27DECCO reconduit — l'autotest SANS modèle) ;
   - `harnais/` — LES PIÈCES GELÉES au MANIFESTE sha256 (recoupées AU
     CHARGEMENT, byte-byte, AVANT toute étape) : le juge D264
     `expandeur_add.py` INTACT (9fc325e2… — JUGE-MODIFIÉ est le refus), le
     round-trip `client_gabarits_rt.py` (byte-identique à w28opt16), les 18
     tâches `taches-edition.json` (byte-identique à opt05, graine 20261117,
     l'ordre JAMAIS re-tiré), les 18 notations .asm aux empreintes recoupées,
     `tokenizer.json` + `config.json` (le modèle consigné), les cibles
     pré-inscrites, les 128 constantes du domaine (le volet spec) ;
   - `LISEZMOI-CAMPAGNE-POSTE.txt` — le pas-à-pas (servir le modèle, le clic,
     le retour du zip au coffre /test).

2. LE DÉCODAGE CONTRAINT CÔTÉ CLIENT (la lettre du plan W29DECCO) : la
   grammaire du schéma fermé D264/OPT-16 ÉTENDU (l'union éditer/ajouter)
   compilée par llguidance sur le vocabulaire du modèle choisi ; LE MASQUE DE
   BITS appliqué à CHAQUE PAS de génération. DEUX MODES portés :
   - MODE-A transformers (in-process) — le masque appliqué aux LOGITS ENTIERS
     du modèle (le mot à mot du plan : « le harnais applique la grammaire au
     masque de logits du modèle ») ; torch + transformers requis (documentés
     au LISEZMOI) ;
   - MODE-B llama.cpp (le bord natif /completion, n_predict=1, n_probs=64,
     cache_prompt) — le masque appliqué AU TOP-64 du bord : la meilleure
     PERMISE au top-64 choisie à chaque pas ; AUCUNE permise au top-64 = le
     pas REFUSÉ fail-closed (AUCUNE-PERMISE, nommé — jamais un chiffre
     habillé).

3. LES PHASES DE LA CAMPAGNE (l'ordre du plan gelé, chaque phase PRÉCÉDÉE du
   canari — le garde continu W29FAMILLE) :
   - LE CANARI DE FIDÉLITÉ CONTINU : la violation ordonnée (l'op hors enum
     SUBVERSION-HORS-ENUM, l'offset 999999) soumise à LA PIPELINE ENTIÈRE ;
     si la violation passe au texte final : PIPELINE-INFIDELE — la session
     INVALIDÉE fail-closed, aucune campagne courue ;
   - ÉDITER : les 18 tâches au protocole OPT-16 RECONDUIT VERBATIM (le prompt
     de campagne_opt16.py, la validation client aux QUATRE refus nommés
     HORS-FORMAT/SCHÉMA-VIOLÉ/POINTEUR-INCONNU/EMPREINTE-DIVERGENTE +
     ROUND-TRIP-DIVERGENT, l'expansion + le round-trip keystone↔capstone, la
     boucle de réparation ≤ 3 tours réinjectant le refus exact), la
     génération CONTRAINTE par la grammaire, le budget usage natif JOURNALISÉ
     (le compte est le LOG : le tokenizer natif du modèle compte le prompt
     et la réponse de chaque tour) ;
   - AJOUTER : les 18 pointeurs au harnais D264 RECONDUIT VERBATIM (les
     fixtures du juge, valider_schema_client, la boucle de réparation du
     juge, l'agrégateur fail-closed APPEL-MANQUANT, les médianes sur les 18
     ET sur les vertes, la re-tokenisation indépendante à écart ≤ 1), la
     génération CONTRAINTE (le prompt rend la ligne canonique attendue à
     l'offset, le modèle rend l'objet pointeur) ;
   - LA SECONDE FAMILLE : les DEUX SONDES DE RÉCITATION (MD5 T[64] de la
     RFC 1321, SHA-256 K[64]) — le modèle récite la table entière sous
     contrainte (le schéma de récitation gelé au présent plan : un objet
     {"table": …, "valeurs": [64 chaînes "0x…" à 8 hex]}), la confrontation
     TRIPARTITE : spec (constants-spec.json, le volet du domaine) ↔ le
     modèle (la récitation) ↔ les définitions (la dérivation aux décimales
     par la série entière + la racine cubique par Newton, recalculées AU
     POSTE par le moteur) — tout écart NOMMÉ avec son index, la valeur du
     modèle et celle de la spec ;
   - LES VERDICTS : les cibles pré-inscrites DU REGISTRE (jamais re-tirées,
     portées au harnais/cibles-preinscrites.json recoupé au manifeste) :
     éditer ≥ 17/18 à ≤ 150 tokens natifs médians par changement validé ;
     CIB-EDIT-FAISAB ≥ 15/18 ; CIB-EDIT-AMORTI ≤ 150 (la somme des tours et
     tentatives ÷ les vertes) ; CIB-ADD-STRUC ≥ 15/18 à ≤ 3 000 tokens —
     chaque verdict TENU/MANQUÉ publié TEL QUEL ; la seconde famille :
     FAMILY-ABSENT devient la MESURE (X/128 nommé, jamais maquillée).

4. L'AUTOTEST (vécu AU BAC et AU POSTE avant tout run réel) : la maquette —
   le bord scripté qui rejoue LE CHEMIN VERT (un éditer honnête bout en
   bout : le masque, la boucle, le juge, le journal) ET LE CANARI (la
   violation tentée au top-1 du bord maqué : REFUSÉE AU MASQUE, la preuve au
   journal) — AUCUN chiffre de campagne fabriqué par la maquette (elle est
   l'instrument, jamais la mesure).

5. LA GARDE : aucun secret dans le kit ; aucune cible re-tirée ; aucune
   graine re-tirée (20261117 l'éditer, 20261124 l'ajouter — les graines des
   plans gelés) ; le juge D264 INTACT à l'empreinte consignée ; les notations
   recoupées aux empreintes AVANT chaque tâche ; aucun verdict fabriqué : un
   échec mesuré au poste réel est une pièce aussi précieuse qu'un vert.

## Critères d'acceptation
- Le manifeste recoupé 100 % au chargement ; le sceau-I 14/14 avant et après
  (au bac) ; le juge expandeur_add.py byte-identique (9fc325e2…).
- L'autotest maquette VERT au bac (le chemin vert + le canari refusé + les
  négatifs du client) AVANT l'assemblage du zip.
- Les deux modes documentés au LISEZMOI avec les COMMANDES EXACTES du
  serving (llama.cpp : llama-server -m <gguf> --port 8080 -c 8192 ; le mode A :
  pip install torch transformers + le chemin local du modèle).
- Le zip testé au dézippage, les empreintes recoupées byte-byte ; le kit
  déposé au /livrables du coffre au jeton relais + download/ du bac.
