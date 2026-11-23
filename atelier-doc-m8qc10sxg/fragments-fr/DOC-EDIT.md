# DOC-EDIT — l'opération EDIT (le miroir FR, compact)
L'édition vit au gabarit scellé TPL-EDIT-v1 : émets les hunks, jamais
une réécriture en texte libre. Les quatre refus d'édition sont nommés
— HORS-FORMAT (la forme du hunk viole le gabarit), HUNK-INCONNU (le
hunk ne s'applique pas à son ancre), CONTEXTE-DIVERGENT (les octets
environnants ont bougé), ROUND-TRIP-DIVERGENT (ce que tu as écrit ne
revient pas) — répare la cause nommée seule, chaque ligne intacte
octet pour octet. Le patch honore le contrat publié (R4) : même
signature, mêmes pré et post-conditions, les appelants jamais
invalidés. Aucun commit sans l'oracle, les vecteurs dorés et le
round-trip (R5). Le budget : 674 (non arrondi au manifeste) ;
le budget de réparation est 3. La référence est la notation scellée
du bloc — jamais une récitation du voisin, l'exemplaire est une
référence, pas un raccourci.
