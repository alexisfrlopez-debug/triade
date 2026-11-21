# PLAN GELÉ — X705M50VL (la vague 12)
> Deux variantes à la marge VIERGE du laboratoire : le v5-entrelacé (k ∈ {4, 8}) et l'AVX2 après hissage.
> Gelé AVANT toute mesure, cible pré-enregistrée falsifiable.

## Le mandat
Deux variantes à la marge VIERGE du laboratoire (0xD200/0xD400/0xD800/0xDC00/0xDE00),
convention du rig 8z4hj76w4 (octets position-indépendants), scellé tls13-16 assemblé à
son slot puis posé en copie :

1. **v5-entrelacé** : k ∈ {4, 8} calendriers de clés à adresses INDÉPENDANTES, les corps
   aesenc des k blocs entrelacés pour masquer la latence (le levier nommé de v4 :
   l'indépendance d'adressage, pas la précalculée). Cible : ≤3 c/bloc enveloppe comprise
   aux 64 et 256 blocs ; si non atteinte, l'écart est nommé par mesure (latence vs
   débit, port pressure).

2. **AVX2 après hissage** : le sondage cpuid hissé UNE fois par session (la condition
   nommée de fnvan0zes), le dispatch résolu au chargement sous R10 ; re-mesurer le
   couloir de recherche 4 096 octets absent, n≥20, cœur épinglé, RDTSC, IQR publié.

Parité exigée aux deux variantes : calendrier des clés confronté au juge FIPS 197 §5.2,
vecteur FIPS C.1, différentielle 64/64 et 256/256 octet pour octet contre le scellé
appelé, replis forcés exercés, borne N≤256 fail-closed, round-trip 100 %.

## Les gestes
1. Ce plan gelé AVANT toute mesure.
2. Atelier atelier-marge-vierge-x705m50vl/ : les notations tls13-16-ni-v5-ent4.asm et
   tls13-16-ni-v5-ent8.asm (calendriers à adresses indépendantes, corps entrelacés) à
   la marge 0xE200/0xE400, la notation loupe-13-avx2-hisse (sondage hissé, dispatch sous
   R10) à 0xE600 ; la copie du scellé tls13-16 posée à son slot.
3. Les mesures : le compte d'instructions Unicorn aux 64 et 256 blocs (l'enveloppe
   comprise — prologue/épilogue dans le compte), le temps réel RDTSC si le bac le permet
   (cœur épinglé, n≥20, IQR) — sinon le gap nommé (une seule machine virtualisée, la
   convention des vagues précédentes).
4. La parité : juge FIPS 197 §5.2 (le calendrier des clés), vecteur FIPS C.1,
   différentielle 64/64 et 256/256 contre le scellé, replis forcés, borne N≤256,
   round-trip 100 %.

## La vérification après modifications
- contrôle négatif (un octet du corps entrelacé muté) ATTRAPÉ au premier vecteur ;
- compteur hors borne → rax=-2, rien chiffré ;
- les scellés INTACTS avant/après chaque exécution (la marge vierge seule écrite) ;
- les cycles publiés enveloppe comprise avec médiane non arrondie et IQR ;
- la batterie 559 re-roulée sur le couloir AVX2 hissé → zéro divergence ;
- si la cible ≤3 n'est pas atteinte, le rapport publie l'écart et sa cause mesurée,
  jamais un chiffre ajusté.

## Les refus
Aucun scellé modifié ; la marge vierge seule écrite ; l'écart nommé par mesure ; la
cible falsifiable pré-enregistrée.
