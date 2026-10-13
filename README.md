# Frottement et roulement : cours et activités interactifs

Construction reprise du dépôt « Chaîne fonctionnelle » (lui-même repris du dépôt « Résistance des matériaux ») : une
page autonome (un seul fichier HTML, aucune dépendance externe, utilisable hors ligne), publiée par GitHub Pages
depuis `index.html`. L'accueil mène à :

| Adresse | Contenu |
|---|---|
| `index.html` | accueil, en cartes illustrées à mots-clés : les cours (pastilles Analytique / Graphique), l'atelier graphique, les activités, les études de cas |
| `?ex=cours-frottement-analytique` | Cours 1 — Frottement et roulement : approche analytique (adhérence et frottement, colis simulé, coefficients, lois de Coulomb, résistance au roulement et ses deux exemples, automobile simulée, quiz) |
| `?ex=cours-frottement-graphique` | Cours 2 — Frottement : résolution graphique (angle et cône de frottement, cône manipulable, jeu, méthode des trois forces, montée de trottoir construite pas à pas en quatre cas puis à refaire soi-même, quiz) |
| `?ex=atelier-graphique` | Atelier — la planche de construction en accès libre : feuille quadrillée ou fonds des activités, mode d'emploi |
| `?ex=cones-adherence-frottement` | Activité 1 — Cônes d'adhérence et de frottement (QCM 3 et 4, regroupés) |
| `?ex=cle-excentrique` | Activité 2 — Clé à excentrique (exercice 5) : construction, vérification analytique, couple de serrage |
| `?ex=voiture-pente` | Activité 3 — Voiture à l'arrêt dans une pente (exercice 6) : construction, pente limite |
| `?ex=voiture-pente-variantes` | Activité 4 — Voiture en pente : trois variantes (exercices 7, 8 et 9, regroupés) |
| `?ex=voiture-route-mouillee` | Activité 5 — Voiture sur route mouillée (exercice 10) |
| `?ex=resistance-roulement` | Activité 6 — Résistance au roulement (exercice 11) |
| `?ex=barbecue-arc-boutement` | Activité 7 — Barbecue de cheminée : arc-boutement (exercice 12) : construction, actions en A et B |

Chaque activité propose le mode entraînement ou le mode examen, avec sa propre note pondérée par la durée de ses
parties. Corrections apportées aux contenus d'origine et décisions : [`NOTE-DE-LIVRAISON.md`](NOTE-DE-LIVRAISON.md).

## La planche de construction graphique

Les résolutions graphiques se font sur une **planche** (`src/planche.js`, `src/planche.css`, `src/construction.py`) :
une feuille cotée en millimètres, son fond (le mécanisme dessiné à l'échelle), ses éléments donnés et les outils du
tracé à la règle et au rapporteur — droite, segment, parallèle, perpendiculaire, droite inclinée d'un angle donné,
**cône de frottement** (f ou φ), **vecteur à l'échelle des forces** (norme lue ou imposée), distance, angle, texte,
gomme, annuler, rétablir, zoom, plein écran. Le pointeur s'aimante aux points, aux intersections et aux droites ;
un tableau de relevés donne longueurs, normes et directions. Le document réponse s'imprime à 100 % avec ses vraies
dimensions, pour construire aussi à la main.

Dans une activité, la planche compte comme un tracé du gabarit : validée, elle reçoit sa correction superposée
une fois validées les questions qui en lisent les résultats (ou à la remise de la copie en examen), puis l'élève
s'attribue ses points avec une grille de critères. Dans le cours 2, la même planche déroule une démonstration pas à
pas ; dans l'atelier, elle est libre. Les corrections sont **calculées** par `src/construction.py` à partir des
données de l'énoncé, comme les réponses attendues.

**Ajouter une activité** : décrire ses parties dans `src/activites.py` (sur le modèle de `PARTS_A2`), avec, pour une
construction, un bloc `{"kind": "pl", …}` dont la configuration (`cfg` : dimensions, échelles, éléments donnés,
correction) et le fond SVG sont produits comme dans `_cle()` ; puis l'ajouter à `EXO_DEFS`. **Ajouter une étude de
cas** : même chose avec `"etude": True`. La carte apparaît d'elle-même sur l'accueil (et remplace l'annonce « En
cours d'édition »).

## Régénérer la page

La page est produite par un script, à partir du gabarit (`src/gabarit-exercice-interactif.html`, copie conforme de
celui du dépôt « Chaîne fonctionnelle », recopié sans modification de son style ni de ses moteurs), de la planche et
du contenu décrit dans `src/`.

```sh
python3 src/generer.py                                   # écrit index.html
NODE_PATH=$(npm root -g) node outils/captures.js         # seulement si les figures des cartes de l'accueil changent
bash outils/preparer-images.sh && python3 src/generer.py # (ImageMagick 6) recadre les cartes, puis régénère
```

## Tester

```sh
node --test tests/correction.test.js                          # moteur de correction : réponses de référence, réponses du manuel, unités, tolérances
node --test tests/construction.test.js                        # planche : géométrie, saisie, cohérence des corrections avec les réponses attendues
NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js # accueil, cours, atelier, activités en entraînement et en examen, constructions à la souris
```

`tests/reponses.js` contient la réponse juste de chaque question ; le parcours navigateur construit la clé à
excentrique à la souris, vérifie les relevés (79,9 daN et 86,5 daN), puis la note de 20/20, sans erreur JavaScript.

## Organisation

| Chemin | Rôle |
|---|---|
| `src/gabarit-exercice-interactif.html` | gabarit de référence (charte, moteurs de correction et d'application), repris tel quel |
| `src/generer.py` | accueil, cours (éléments communs), aiguillage, liaison des planches avec le moteur, assemblage |
| `src/planche.js`, `src/planche.css` | planche de construction : géométrie (bloc `GEOM`, testé), outils, démonstrations, correction, impression à l'échelle |
| `src/construction.py` | géométrie des corrections (repère réel → feuille), fonds SVG (cotes, sol, roues), rendu des planches |
| `src/activites.py` | les sept activités : énoncés, questions, correcteurs, planches, documents DT1 et DT2 |
| `src/cours_analytique.py` | cours 1 : contenu, figures SVG, simulateurs du colis et de l'automobile |
| `src/cours_graphique.py` | cours 2 : contenu, cône manipulable, démonstration du trottoir (quatre cas) |
| `src/atelier.py` | atelier : planche libre et fonds au choix |
| `src/figures.py` | figures partagées : véhicules, cône de frottement, illustration de l'accueil |
| `src/qcm.py` | questions à propositions (repris du QCM du dépôt « Chaîne fonctionnelle ») |
| `src/images/originaux/` | pages photographiées du manuel (cours p. 123 à 131, exercices p. 138 et 139) et captures des cartes |
| `src/images/` | images des cartes de l'accueil (480 × 270), intégrées en data URI |
| `outils/captures.js`, `outils/preparer-images.sh` | photographie des figures pour les cartes (Playwright), recadrage (ImageMagick) |
| `tests/` | tests Node et Playwright |
| `.github/workflows/static.yml` | publication GitHub Pages (déclenchée sur la branche `main`) |
