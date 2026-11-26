# Les chantiers EN ATTENTE — le registre unique (vague 21, 24/11/2026)

> Un statut cité dans une pièce DOIT exister ici. La porte (classe C16) recompose le compte
> annoncé depuis ce registre et refuse tout écart. Vocabulaire fermé : EN ATTENTE, MESURÉ,
> REFUSÉ, PARTIEL.

| id | chantier | statut | geste qui le lève | décision | inchangée depuis (vagues) |
|---|---|---|---|---|---|
| ATT-METAL | bascule concurrente au métal nu (≥ 2 machines, 30 cas) | EN ATTENTE | run du kit pré-enregistré sur deux machines réelles | D253, D261 | 0 |
| ATT-NV | compteur NV matériel (TPM/RPMB) | EN ATTENTE | run du simulateur sur silicium réel | D263 | 0 |
| ATT-ADD | campagne add structurée servie | EN ATTENTE | serving à structured output | D264 | 0 |
| ATT-ORACLE | mesure native du moteur d'oracle (T < 10 s) | MESURÉ (vague 27, atelier-w27vaes : mmap 0xC000 re-prouvé au bac — mmap_min_addr 4 096 ; la session des 235 vecteurs natifs 0,266 s médiane n=5, classification 235/235 == jumeau, digeste 81/81 ; CIB-ORACLE-T TENUE) | — soldé au bac ; la mesure machine réelle demeure un geste d'échelle, pas une attente de la cible | D264 | 27 |
| ATT-VAES | couloir AES-GCM VAES/VPCLMULQDQ | MESURÉ (vague 27, atelier-w27vaes : le couloir écrit sur notation gelée, la porte verte — 20/20 CAVP, mutant refusé, round-trip VERT — et la cible CIB-AES-105 MANQUÉE à 5,66 × EVP, consignée telle quelle) | la mesure machine réelle goupillée (le kit livré : source + notation + porte) — la cible demeure, jamais re-tirée | OPT | 27 |
| ATT-GARDES | spécialisation des onze gardes (22→7) | EN ATTENTE | modification du corridor scellé et mesure | OPT | 0 |
| ATT-TAMARIN | Tamarin/ProVerif sur machine réelle | PARTIEL (outils AU bac à la vague 27 : L3 rejeu bit-identique, la décomposition L1c/L2a vérifiée ; L1a/L2 entier au mur 4 Gio ; ProVerif absent) | le run machine réelle à empreinte consignée (atelier-w27preuv/kit-run-reel.txt) | P1–P4 | 27 |
| ATT-FIDO2 | prototype média FIDO2 hmac-secret | EN ATTENTE | authentificateur réel | D270 | 0 |
| ATT-DUDECT | dudect matériel n ≥ 10, ≥ 2 machines | EN ATTENTE | run au poste réel | H7 | 0 |
| ATT-REPL | réplication N > 1 (autre famille d'agent) | EN ATTENTE | trois tâches du corpus sur un second agent | D251 | 0 |