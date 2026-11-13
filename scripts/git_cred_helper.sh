#!/bin/bash
# Aide d'identification git — lit le jeton GitHub dans .gdrive/token_git.txt
# SECURITE : le jeton n'est jamais affiché, journalisé ni commis (.gdrive/ est gitignoré).
TOK="/home/z/my-project/.gdrive/token_git.txt"
if [ "$1" = "get" ]; then
  tok=$(tr -d ' \t\r\n' < "$TOK" 2>/dev/null)
  [ -n "$tok" ] || exit 1
  echo "username=triade-relais"
  echo "password=$tok"
fi
# store/erase : no-op (le jeton demeure uniquement dans .gdrive/)
exit 0
