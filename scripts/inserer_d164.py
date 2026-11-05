#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d164.py — DECISIONS.md : insère la décision D164 PAR SCRIPT
(à la suite de D163, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/DECISIONS.md"

D164 = """
## D164 — LA REPRISE CONFRONTE LES TROIS MIROIRS ET S'ALIGNE SUR LA POINTE GITHUB (le bundle Drive peut être UN GESTE EN RETARD : la passation D141 est la DERNIÈRE étape d'un geste — une session qui meurt entre le push et la passation laisse GitHub en avance ; la reprise FETCH GitHub D'ABORD, s'aligne sur la pointe consignée, PUIS rejoue la passation) ; LE RAPATRIEMENT DE LA ZONE download/ PRÉCÈDE maj_kit.py — LE PIÈGE DU MANIFESTE AMPUTÉ S'EST RE-DÉCLENCHÉ (consigné 132/159, rejoué 05/11 : le manifeste régénéré couvrait 56 entrées d'un kit réel de 62 — les 6 LISEZMOI ignorés ; désamorcé PAR LE RAPATRIEMENT CANONIQUE 6/6 md5 MATCH puis rejeu 62/62) ; LE JETON RELAIS MIS À JOUR PAR LE DÉVELOPPEUR REDEVIENT LE CANAL D'ÉCRITURE (le coffre répond 200 : miroir rc=0, kit 62/62, bundle déposé — le compte de service demeure la voie de repli consignée D163)

**Le contexte qui fonde la décision (05/11, la reprise « on reprend ce projet »).** Le développeur annonce la reprise : signatures au /test, jeton relais mis à jour au /Tokens. La reprise depuis le bundle Drive (080-b7b6e01, la pointe consignée par la passation du Task 77) a suivi la méthode A — puis le recoup GitHub a nommé la divergence : **origin à 9193019, UN COMMIT EN AVANCE du bundle**. Le geste absent du bundle était le Task 78 d'une session précédente (la cérémonie installée + le build 0.9.0-dev.1 né, poussé à GitHub) : la session était morte ENTRE le push et la passation — la passation est la DERNIÈRE étape d'un geste, le bundle ne portait donc PAS la pointe. Le travail parallèle refait au labo (cérémonie vérifiée-déposée, garde repassé, build exécuté) a produit un commit DOUBLON du geste consigné : l'écart a été nommé par le recoup ls-remote AVANT toute consignation (aucune entrée de journal doublée), l'alignement s'est fait par reset à la pointe consignée (D159 rejouée : ce qui est consigné revient), et le doublon a été écarté — ses pièces substantielles étaient les MÊMES par déterminisme (l'artefact régénéré au geste de reprise : sha256 1492b0bc… == la pièce de D163 ; les signatures du sceau : identiques — la remise du développeur ne peut donner QUE ces octets). Dans le même geste, maj_kit.py joué depuis un labo amputé a régénéré un MANIFESTE de 56 entrées pour un kit réel de 62 fichiers — le piège des Entrées 132/159, exactement comme documenté ; le rapatriement canonique (6/6 LISEZMOI, md5 contrôlés contre les MÉTADONNÉES Drive après écriture) puis le rejeu ont rendu le manifeste complet (62/62 vérifiés aller-retour).

**Les règles.** (1) **La reprise confronte les TROIS miroirs AVANT de travailler** : le dépôt local (s'il survit), GitHub (ls-remote/fetch — LA POINTE), le bundle Drive (la passation — potentiellement UN GESTE EN RETARD). L'alignement se fait TOUJOURS sur la pointe GitHub consignée ; si GitHub est en avance du bundle, la passation est REJOUÉE au geste de reprise (le bundle rattrape la pointe). (2) **Un geste n'est terminé que par sa passation** : le push GitHub seul ne suffit pas — D141 exige le bundle à la pointe ; une reprise qui constate l'avance GitHub sans rejouer la passation laisse la dette d'infrastructure ouverte. (3) **Le rapatriement de la zone download/ précède maj_kit.py** (la règle des Entrées 132/159, à présent DOCTRINE : le script canonique rapatrier_lisezmoi_ceremonie.py — contrôle md5 par fichier APRÈS écriture — est joué chaque fois que le labo a été recyclé, AVANT tout rejeu du déploiement du kit ; un manifeste amputé est une attestation mensongère, même avec 56/56 verts sur ses 56 entrées). (4) **Le jeton relais du développeur redevient le canal d'écriture quand il répond** : la mise à jour au /Tokens est le geste du développeur qui ROUVRE le canal OAuth (check_auth.py : échange 200, listing 200) ; les gestes d'écriture (miroir, kit, bundle) reprennent par lui ; le relais compte de service (D163) demeure la voie de repli pour la lecture — jamais les deux ne sont requis ensemble, l'un des deux suffit.

**Alternatives rejetées.** Reprendre depuis le bundle sans recouper GitHub (rejeté : c'est le geste de cette session qui le prouve — le bundle était EN RETARD d'un geste ; travailler depuis un état périmé produit des doublons parallèles) ; merger le commit parallèle avec la pointe (rejeté : le journal append-only n'accepte pas deux Entrées 160 — l'alignement à la pointe consignée est la seule voie propre, le parallèle n'apporte RIEN que le déterminisme n'ait déjà prouvé) ; rejouer maj_kit.py sans rapatriement après un recyclage (rejeté : le manifeste amputé est le piège documenté DEUX fois — la troisième fois il est doctrine) ; attendre le canal OAuth pour le recoup de lecture (rejeté : D163 — le compte de service porte la lecture, le geste ne se bloque pas).

**Frontières.** La présente décision est une décision d'INFRASTRUCTURE DE REPRISE : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), l'artefact 0.9.0-dev.1 est INTACT (1492b0bc… — régénéré identique au geste de reprise, la preuve de déterminisme s'accumule), le garde demeure VERT 12/12 (état « reelle »), la passation rejouée porte la série 080 à la pointe 9193019 (l'ancien b7b6e01 archivé versionné — 25 archives, rien supprimé). Les pièces de l'arrêt : le recoup ls-remote (9193019 vs 7079df1), le bundle triade-history-080-9193019.bundle (md5 a8cd69f8…, déposé et relu MATCH), le manifeste complet du kit (62/62), scripts/rapatrier_lisezmoi_ceremonie.py (le rejeu canonique, labo), scripts/passe_bundle_m8c_execution.py (la passation rejouée, dépôt).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## D164" in texte:
    sys.exit("ECHEC : la décision D164 existe déjà")
if "## D163" not in texte:
    sys.exit("ECHEC : la décision D163 introuvable (l'ordre D163<D164)")

# insertion à la suite de D163 (fin du fichier si D163 est la dernière)
i163 = texte.find("## D163")
fin = texte.find("\n## D163", i163 + 1)
if fin < 0:
    # D163 est la dernière décision : append
    if not texte.endswith("\n"):
        texte += "\n"
    nouveau = texte + D164
else:
    nouveau = texte[:fin] + "\n" + D164.strip("\n") + "\n" + texte[fin:]

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Décision D164 insérée (à la suite de D163)")
