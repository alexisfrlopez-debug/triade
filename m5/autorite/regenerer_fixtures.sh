#!/usr/bin/env bash
# TRIADE M5-b — génération des fixtures de l'AUTORITÉ DE TEST LOCALE.
# Laboratoire uniquement (OpenSSL ≥ 3.5 exigé : -not_before/-not_after) ;
# le terrain reçoit les fixtures DÉJÀ GÉNÉRÉES (m5/autorite/fixtures/) —
# il ne génère rien, il ne vérifie que des empreintes.
#
# Cinq couples (certificat + clé) — les clés sont des clés de TEST, jetables :
# elles ne protègent rien, ne signent que autorite.test / autre.test, et
# vivent au dépôt PAR CHOIX (l'autorité est un appareil de test explicite —
# la discipline « aucune clé dans git » du coffre réel vise les secrets
# réels, pas les fixtures d'essai ; empreintes consignées au LISEZMOI).
#
# Modes :
#   valide      — serv-valide      : SAN autorite.test, signée par la racine
#   autonome    — serv-autonome    : AUTO-SIGNÉE (miroir de self-signed.badssl.com)
#   autre-hote  — serv-autre-hote  : signée par la racine MAIS SAN autre.test
#   expiree     — serv-expiree     : SAN autorite.test, signée, notAfter PASSÉ
#
set -euo pipefail
ICI="$(cd "$(dirname "$0")" && pwd)"
FIX="$ICI/fixtures"
mkdir -p "$FIX"
cd "$FIX"

RACINE="racine-autorite"

# ---------------------------------------------------------------- la racine
openssl genrsa -out "$RACINE.key" 2048 2>/dev/null
openssl req -x509 -new -key "$RACINE.key" -out "$RACINE.pem" \
  -days 3650 -subj "/CN=TRIADE Autorite de Test M5-b (jetable)" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign" \
  -addext "subjectKeyIdentifier=hash" 2>/dev/null

# ------------------------------------------------- feuille signée (gabarit)
feuille () {  # $1=nom  $2=SAN  $3=serial  [$4=not_before $5=not_after]
  local nom="$1" san="$2" serial="$3"
  openssl genrsa -out "serv-$nom.key" 2048 2>/dev/null
  openssl req -new -key "serv-$nom.key" -out "serv-$nom.csr" \
    -subj "/CN=$san" 2>/dev/null
  local ext="ext-$nom.tmp"
  printf 'subjectAltName=DNS:%s\nbasicConstraints=CA:FALSE\nkeyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth\n' \
    "$san" > "$ext"
  local args=(-req -in "serv-$nom.csr" -CA "$RACINE.pem" -CAkey "$RACINE.key"
    -set_serial "$serial" -out "serv-$nom.pem" -extfile "$ext")
  if [ $# -ge 5 ]; then
    args+=(-not_before "$4" -not_after "$5")
  else
    args+=(-days 730)
  fi
  openssl x509 "${args[@]}" 2>/dev/null
  rm -f "serv-$nom.csr" "$ext"
}

feuille valide     autorite.test 0x1001
feuille autre-hote autre.test    0x1002
feuille expiree    autorite.test 0x1003 20240101000000Z 20250101000000Z

# ---------------------------------------------------------- l'auto-signée
openssl req -x509 -newkey rsa:2048 -nodes -keyout serv-autonome.key \
  -out serv-autonome.pem -days 730 -subj "/CN=autorite.test" \
  -addext "subjectAltName=DNS:autorite.test" \
  -addext "basicConstraints=CA:FALSE" 2>/dev/null

# ------------------------------------------------------------- vérifications
echo "== vérifications de chaîne (le juge indépendant du laboratoire) =="
ok () { echo "  OK   $1 : $2"; }
ko () { echo "  ÉCHEC $1 : $2"; EXIT=1; }
EXIT=0
openssl verify -CAfile "$RACINE.pem" serv-valide.pem >/dev/null 2>&1 \
  && ok serv-valide "chaîne valide" || ko serv-valide "chaîne attendue valide"
openssl verify -CAfile "$RACINE.pem" serv-autre-hote.pem >/dev/null 2>&1 \
  && ok serv-autre-hote "chaîne valide (l'INVARIABLE est l'HÔTE, pas la chaîne)" \
  || ko serv-autre-hote "chaîne attendue valide"
openssl verify -CAfile "$RACINE.pem" serv-expiree.pem >/dev/null 2>&1 \
  && ko serv-expiree "attendue EXPIRÉE" \
  || ok serv-expiree "rejetée : expirée (attendu)"
openssl verify -CAfile "$RACINE.pem" serv-autonome.pem >/dev/null 2>&1 \
  && ko serv-autonome "attendue AUTO-SIGNÉE donc rejetée" \
  || ok serv-autonome "rejetée : auto-signée (attendu)"
openssl verify -CAfile "$RACINE.pem" -verify_hostname autorite.test \
  serv-autre-hote.pem >/dev/null 2>&1 \
  && ko autre-hote/hostname "mismatch d'hôte attendu" \
  || ok autre-hote/hostname "rejetée : mauvais hôte (attendu)"
openssl verify -CAfile "$RACINE.pem" -verify_hostname autorite.test \
  serv-valide.pem >/dev/null 2>&1 \
  && ok valide/hostname "hôte conforme" || ko valide/hostname "hôte attendu conforme"

echo "== empreintes (sha256, 12 premiers) =="
for f in "$RACINE.pem" serv-valide.pem serv-autonome.pem serv-autre-hote.pem serv-expiree.pem; do
  printf '  %-22s %s\n' "$f" "$(openssl x509 -in "$f" -noout -fingerprint -sha256 \
    | cut -d= -f2 | tr -d : | cut -c1-12)"
done

exit $EXIT
