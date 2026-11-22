# LES RECETTES SFT/DPO/RLVR (3x9cf4e5d) — agnostiques en famille

SFT : les triples VERTS du TRAIN (atelier-corpus-2i7iy3xmg/dataset/
train.jsonl — le champ reponse des verdicts VERTS, le contrat au
contexte) ; format : (contexte = le contrat, cible = la réponse validée) ;
hyperparams consignés au run (lr 1e-5..2e-5, 2-3 époques, le budget
compute au registre) — la faisabilité mesurée au plan headline GELÉ.

DPO : les paires (choisie = la notation verte, rejetée = le refus au
MÊME contrat — registres/paires-dpo.jsonl, extraites MÉCANIQUEMENT du
corpus) ; format : (prompt = le contrat, chosen, rejected) ; β 0.1..0.3 ;
les paires JAMAIS retapées.

RLVR : la récompense = LE VERDICT DU JUGE par triade_gym.py episode
(la récompense typée multi-niveaux : syntaxe → expansion → round-trip →
oracle → mutation — CUMULATIVE ET STRICTE, un niveau ne s'ouvre que si
le précédent est vert) ; JAMAIS la similarité à une référence
(anti-récitation par construction) ; les checks anti-hacking DE P2 à la
récompense (le jeu du juge refusé au niveau mutation) ; le rung terrain
JAMAIS une récompense barato (le geste développeur).

LES ADAPTERS DE RÉFÉRENCE : optionnels aux versions majeures du kit —
≥ 2 familles SI compute, SINON LE GAP NOMMÉ (aucun chiffre fabriqué).
LES CAS DIFFICILES des rapports adopteurs (le feedback F/L) entrent au
curriculum comme nouveaux exemples + nouvelles tâches held-out (la
boucle witgt6qta → e1lr9i8ts → le corpus).
