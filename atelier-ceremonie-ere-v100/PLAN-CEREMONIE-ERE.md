# PLAN GELÉ — LA CÉRÉMONIE D'ÈRE DE couloir-vaes512.asm (le kit 1-clic à la clé hors-ligne du maître)

> La SUITE de l'Entrée 442 : « la cérémonie d'ère de la notation
> couloir-vaes512.asm à la clé hors-ligne du maître (la dette nommée) », la
> commande du maître « va enchainer sur la campagne au poste réel puis
> cérémonie, comme d'habitude avec GUI 1 clic ». La dette fut nommée À LA
> NAISSANCE (PLAN-W29VAES512.md) : « l'ère n'est scellée que par la clé
> hors-ligne du développeur — le laboratoire ne signe jamais ». Le présent
> plan gèle LE KIT DE CÉRÉMONIE avant toute pièce.

## Le kit

**TRIADE_kit_ceremonie_ere_v100** — un dossier auto-suffisant, un clic
(`CEREMONIE-ICI.bat`), pour la cérémonie de l'ère VAES512 zmm (la notation
couloir-vaes512.asm, sha256 a2c3a393… consignée AVANT l'exécutable — la
notation vit SUR COPIE LABORATOIRE, exécutable et éprouvée à la porte CAVP
20/20 ; l'ère n'est scellée qu'au geste du maître).

1. LA CHARGE (la forme de a-signer du sceau-I — l'OUTIL DU MAÎTRE la signe
   TELLE QUELLE, sans adaptation : trois champs « nom balise empreinte », le
   parseur de ceremonie_hors_ligne.py l'accepte byte pour byte) :
   ```
   ere-notation   couloir-vaes512.asm         <sha256 a2c3a393…>
   ere-schedule   couloir_sched512.S          <sha256 du fichier de l'atelier>
   ere-portage    couloir_vaes512.c           <sha256 du fichier de l'atelier>
   ere-vecteurs   vecteurs-dores-nist.json   <sha256 des 20 CAVP reconduits>
   ```
   La charge est PRÉPARÉE par le moteur (les empreintes RECALCULÉES des
   octets mêmes des pièces portées — jamais recopiées du texte), et la
   notation est PORTÉE au kit byte-byte (le maître re-vérifie l'empreinte À
   SA MACHINE hors-ligne avant de signer : le sceau honnête).

2. LA SIGNATURE HORS-LIGNE (le geste du maître, JAMAIS du laboratoire) :
   le kit porte `a-emporter/` — la charge, la notation, le signeur
   autoporteur `signeur_hors_ligne.py` (la référence Ed25519 RFC 8032 de
   v06/ceremonie_hors_ligne.py, l'autotest fail-closed des vecteurs § 7.1 à
   chaque démarrage, AUCUNE dépendance, AUCUN réseau) et le pas-à-pas. Le
   maître signe À SA CLÉ hors-ligne (la clé I du sceau — la CONTINUITÉ de
   clé D163 : la même clé qui signe les 14 arbres signe l'ère) :
   `python3 signeur_hors_ligne.py signer ere-vaes512-a-signer.txt cle-I-privee.txt`
   → `signatures-I.txt` (« nom balise signature », une ligne par pièce).

3. LA VÉRIFICATION ET LE SCEAU (au retour) : le moteur VÉRIFIE chaque
   signature à la clé publique I PORTÉE au kit (byte-byte de
   v06/sceau-I/cle-publique-I.txt, l'empreinte consignée au manifeste — la
   continuité : la clé de l'ère EST la clé du sceau ; une signature d'une
   autre clé est nommée CLÉ-DIVERGENTE, le sceau REFUSÉ) ; LE SCEAU
   `ere-vaes512-sceau.txt` (la charge + les signatures + la vérification +
   l'horodatage) est écrit ; le zip de preuves `preuves-ceremonie-<ts>.zip`
   retourne au coffre /test.

4. LA GUI (le patron ceremonie_gui.py — tkinter, stdlib seule, zéro pip) :
   un clic `CEREMONIE-ICI.bat` → QUATRE boutons : Préparer la charge ·
   Guider la signature hors-ligne (le pas-à-pas + la liste à emporter) ·
   Vérifier la signature revenue · Installer le sceau d'ère. Le journal en
   direct, le VERT/ROUGE à chaque étape, la forme des pousseur/cockpit.

5. LA GARDE (D87/D183) : le LABORATOIRE NE SIGNE JAMAIS — l'autotest du kit
   s'éprouve à la CLÉ DE TEST (la graine publique constante, l'état « test »
   visible : la non-sécurité de la clé de test EST la preuve de l'état
   laboratoire) ; la clé privée réelle n'entre JAMAIS au bac ; le sceau
   réel ne vit que des mains du maître ; aucun secret committé ; la
   notation couloir-vaes512.asm INTACHE byte-byte (a2c3a393… recoupé au
   chargement et avant le sceau) ; la notation ymm 7911d03f… du sceau des
   arbres INTACTE (aucune pièce scellée touchée).

## Critères d'acceptation
- L'autotest à la clé de test VERT au bac AVANT l'assemblage : preparer →
  signer (clé de test) → verifier → installer, l'aller-retour ENTIER, le
  sceau de test étiqueté TEST jamais confondu (la graine publique) ; le
  refus d'une signature muée ROUGE ; le refus d'une charge muée ROUGE.
- La charge signée par l'outil du maître SANS adaptation (le format trois
  champs — l'épreuve au bac : ceremonie_hors_ligne.py du dépôt, byte
  pour byte la référence, signe la charge du kit à la clé de test).
- Le zip testé au dézippage, les empreintes recoupées byte-byte ; le kit
  déposé au /livrables du coffre au jeton relais + download/ du bac ; le
  sceau-I 14/14 avant et après.
