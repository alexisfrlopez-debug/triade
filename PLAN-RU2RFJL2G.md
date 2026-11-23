# PLAN GELÉ — RU2RFJL2G (l'ancrage de transparence, la sentinelle Windows, la garde RAM, le FIDO2)

> Le mandat : implémenter l'ancrage de transparence publique du témoin d'époque
> CF3 (Rekor/Sigstore ou RFC 3161), le moteur sentinelle Windows de
> production, la garde RAM native et le prototype FIDO2 du média piège. Tous
> les gestes réseau et le jeton physique restent au développeur ; le laboratoire
> prépare et vérifie sur copies de laboratoire à phrase de test marquée (D105),
> jamais le coffre réel. Gelé AVANT tout geste ; l'empreinte précède la donnée.

## Le mandat

(1) **L'ANCRAGE** (documenté-non-appliqué à D219, DEVENANT APPLIQUÉ AU
FORMAT) : le format du témoin signé, le vérificateur machine **OFFLINE
fail-closed** (aucune dépendance réseau au chargement, R10), et le delta au
modèle de menace **AUX DEUX BORDS** — ce que l'ancrage ajoute contre le
roll-back admin, ce qu'il n'ajoute pas.

(2) **LA SENTINELLE WINDOWS DE PRODUCTION** (SACL + journal 4663 ou ETW) pour
fermer l'ère D120 « avertissement SANS sentinelle ».

(3) **LA GARDE RAM NATIVE** (mlock + SecureZeroMemory, le drapeau dumpable
effacé) au-delà du best-effort Python.

(4) **LE PROTOTYPE FIDO2** du média piège — le support change, pas la serrure.

## Les gestes

1. Le plan gelé ; l'empreinte consignée ; LE COMMIT D'ABORD.
2. **LE TÉMOIN ET SON VÉRIFICATEUR** : le format du témoin d'époque signé, le
   vérificateur offline (fail-closed, zéro réseau au chargement), le delta au
   modèle de menace aux deux bords.
3. **LA SENTINELLE** : le moteur Windows (SACL + 4663 ou ETW), le harnais
   (lecture non blanchie → destruction + PV, zéro fausse alerte en nominal,
   latence bornée assertée).
4. **LA GARDE RAM** : mlock + SecureZeroMemory, le drapeau dumpable effacé, la
   preuve octet pour octet de la zéroïsation effective.
5. **LE FIDO2** : le prototype du média piège — le jeton physique restant au
   développeur, l'écart nommé si le matériel est absent.
6. **LA TABLE DES STATUTS** et le rapport append-only.

## La vérification après modifications

L'autotest du vérificateur d'ancrage (témoin valide VERT, témoin muté REFUSÉ
nommé, absence réseau simulée → refus propre) ; le harnais sentinelle Windows
(lecture non blanchie → destruction + PV, fausses alertes nulles en nominal,
latence bornée assertée) ; la garde RAM vérifiée octet pour octet (zéroïsation
effective, dumpable effacé) ; le sceau-I 14/14 avant et après ; la table des
statuts mise à jour ; le rapport append-only.

## Les refus

Jamais le coffre réel ; jamais un appel réseau au chargement ; jamais un refus
silencieux ; jamais un PV sans la destruction ; jamais le jeton physique au
laboratoire ; jamais une fausse alerte comptée pour une alerte ; jamais le
modèle de menace écrit d'un seul bord.
