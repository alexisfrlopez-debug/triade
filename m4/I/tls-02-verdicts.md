tls-02 · table des verdicts SSPI · révision 1
Intention : traduire un HRESULT SSPI/Schannel en verdict NOMMÉ du projet —
LE seul propriétaire de la sémantique d'échec cryptographique (contrats
cryptographiques M4) : tout HRESULT du domaine est classé, aucun n'est
jamais propagé brut, toute valeur non documentée est un échec fatal nommé
(fail-closed intégral, charte § 1).
Contrat :
  pre  : P1 rcx contient l'HRESULT (i64, valeur 32 bits signée étendue —
             les codes SEC_E_* négatifs et SEC_I_* positifs) ;
         P2 aucune autre entrée : la classification est une fonction PURE
             de la valeur.
  post : Q1 rax = verdict :
             0 succès              — SEC_E_OK ;
             1 continuer           — SEC_I_CONTINUE_NEEDED (la poignée de
                                     main se poursuit : émettre le jeton,
                                     réceptionner, rappeler) ;
             2 message incomplet   — SEC_E_INCOMPLETE_MESSAGE (réceptionner
                                     davantage, redonner le tampon entier) ;
             3 certificat invalide — SEC_E_UNTRUSTED_ROOT, SEC_E_CERT_
                                     EXPIRED, SEC_E_CERT_UNKNOWN, SEC_E_
                                     CERT_WRONG_USAGE, SEC_E_WRONG_
                                     PRINCIPAL : LA classe du critère M4
                                     « échec propre sur certificat
                                     invalide » ;
             4 fin de contexte     — SEC_I_CONTEXT_EXPIRED (close_notify :
                                     fin PROPRE de flux) ;
             5 échec négocié       — SEC_E_INVALID_TOKEN, SEC_E_DECRYPT_
                                     FAILURE, SEC_E_MESSAGE_ALTERED,
                                     SEC_E_OUT_OF_SEQUENCE : le tunnel est
                                     rompu, proprement ;
             6 fatal inconnu       — TOUTE autre valeur : la bibliothèque a
                                     dit quelque chose que la spécification
                                     n'a pas prévu : échec immédiat, aucun
                                     « au mieux » ;
         Q2 rdx = HRESULT d'origine préservé (l'appelant le consigne en
             verdict nommé, jamais brut — charte § 3 : pas de valeur
             obscure dans les journaux sans nom).
  inv  : I1 feuille pure : aucun appel, aucun IAT, aucun état, aucune
             écriture mémoire ; I2 la table est TOTALE : chaque valeur de
             P1 produit exactement un verdict ; I3 aucun registre non
             volatil modifié ; I4 les valeurs numériques des codes cités
             sont des constantes de la notation (liste blanche — une valeur
             changée d'un bit change de classe si et seulement si la table
             le dit).
Échecs :
  E1 : il n'existe AUCUN échec de contrat — les verdicts 3, 5 et 6 SONT
       les échecs nommés (c'est la fonction même du bloc). Le verdict 6
       n'est pas une surprise : c'est la garantie que rien ne sort de la
       table sans nom.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : les ~ 20 codes documentés en
       valeurs exactes + 100 000 HRESULT aléatoires (y compris voisins à
       un bit des codes réels — contrebande de classe) contre un modèle de
       référence : verdict, HRESULT préservé (couvre P1-P2, Q1-Q2, I1-I4).
  V3 : fuzzing à propriétés : exhaustivité de la totale (I2) — le modèle
       ne connaît pas de « sans opinion ».
  V4 : test de rejet : toute notation appelant, écrivant ou gardant un
       état est refusée (I1).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D45, D77, charte M4 § 1 (fail-closed) et § 2 (certificat).
