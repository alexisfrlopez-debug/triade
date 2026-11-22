# PLAN GELÉ — QA3K5PUTF (la vague 15)
> L'atelier de preuve formelle : mener CF3-v2-amende.spthy à verdict complet sous
> Tamarin 1.12.0/Maude 3.4 — les 36 avertissements de wellformedness résolus un à
> un, les SIX lemmes exécutés, le contrôle négatif vécu, le port ProVerif livré.
> Gelé AVANT tout run ; l'empreinte du modèle amendé consignée avant la première exécution.

## Le mandat
Le modèle CF3-v2-amende.spthy (l'amendement écrit à la vague 14 après le lemme
d'implication FALSIFIÉ — le défaut de modélisation nommé, jamais une attaque) doit
atteindre le verdict machine. Le premier run Tamarin de la vague 14 a produit le
falsifié ; le présent atelier reprend l'amendement et le mène à terme :

(1) **WELLFORMEDNESS** : nommer les 36 avertissements et les résoudre UN PAR UN —
les parts fraîches via Fr (le K réservé en prémisse ×10, le Fr($p) public à la
création), les relations d'attaquant hors K ; le lemme d'implication
secret-appris ⇒ adversaire-détient-≥3-parts REFORMULÉ sur variables privées ;
chaque résolution consignée par numéro et nature.
(2) **LES SIX LEMMES UN PAR UN** : budget (temps/borne) consigné PAR lemme AVANT
le run ; les witnesses de non-vacuité et de reachability du seuil CONSERVÉS ;
chaque trace archivée en JSON, chaque verdict consigné (VERIFIED/INCOMPLETE/FALSIFIED —
aucun verdict fabriqué, un INCOMPLETE nommé est une pièce aussi précieuse qu'un vert).
(3) **LE CONTRÔLE NÉGATIF** : une version affaiblie du modèle (part publique
réintroduite) DOIT falsifier le lemme — la preuve reste portante ; si le négatif
ne falsifie pas, le constat est consigné comme échec mesuré.
(4) **LE PORT PROVERIF** : le même modèle porté en contre-vérification ; tout
écart de sémantique entre les deux outils NOMMÉ (jamais masqué).

## Les gestes
1. Le plan gelé ; l'empreinte sha256 de CF3-v2-amende.spthy consignée AVANT tout run.
2. Tamarin 1.12.0 + Maude au bac (installation consignée, versions vérifiées).
3. La passe wellformedness (les 36 nommés et résolus) ; CF3-v3.spthy né — l'amendé
   demeure verbatim, le v3 est la pièce courante.
4. Les six lemmes un par un, budgets consignés, traces JSON archivées.
5. Le contrôle négatif (la part publique réintroduite).
6. Le port ProVerif + la table des écarts de sémantique.
7. La table des statuts mise à jour ; la confrontation aux quatre propriétés
   P1–P4 déjà prouvées par invariant inductif (aucune contradiction silencieuse).

## La vérification après modifications
Rejeu à versions/graines identiques (verdicts bit-identiques) ; wellformedness
0 avertissement résiduel ; chaque lemme VERIFIED ou INCOMPLETE nommé avec budget ;
les empreintes du modèle amendé et des traces consignées ; sceau 14/14 ;
entrée append-only au journal.

## Les refus
Jamais « prouvé » sans verdict machine ; jamais un lemme affaibli pour verdir ;
jamais le négatif escamoté ; jamais l'écart ProVerif/Tamarin masqué.
