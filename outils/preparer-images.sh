#!/usr/bin/env bash
# Prépare les images intégrées dans la page (ImageMagick 6 requis).
#   - src/images/originaux/cours-p*.jpg, exercices-p*.jpg : pages du manuel (photographies), sources du contenu ;
#     elles ne sont pas intégrées dans la page : toutes les figures sont redessinées en SVG.
#   - src/images/originaux/carte-*.png : images des cartes de l'accueil, photographiées dans les pages par
#     outils/captures.js : NODE_PATH=$(npm root -g) node outils/captures.js
#   - src/images/carte-*.png : les mêmes, recadrées au format 480 × 270 (16:9) et quantifiées (PNG 8 bits).
# Usage : bash outils/preparer-images.sh   (depuis la racine du dépôt)
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=src/images/originaux
OUT=src/images

# une figure très allongée (ou presque carrée) est réduite entière et bordée de blanc ; les autres remplissent la carte
for f in "$SRC"/carte-*.png; do
  b=$(basename "$f")
  r=$(identify -format '%[fx:w/h]' "$f")
  if awk "BEGIN{exit !($r > 2.2 || $r < 1.45)}"; then geo='480x270'; else geo='480x270^'; fi
  convert "$f" -background white -alpha remove -alpha off -resize "$geo" -gravity center -extent 480x270 \
    -strip -colors 128 "PNG8:$OUT/$b"
done
# carte de l'étude à venir : grisée par la page (classe en-edition), rien à faire ici
ls -l "$OUT"/carte-*.png
