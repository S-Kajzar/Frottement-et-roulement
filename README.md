# Frottement et roulement : cours et activités interactifs

Construction reprise du dépôt « Chaîne fonctionnelle » (lui-même repris du dépôt « Résistance des matériaux ») : une
page autonome (un seul fichier HTML, aucune dépendance externe, utilisable hors ligne), publiée par GitHub Pages
depuis `index.html`. L'accueil mène à :

| Adresse | Contenu |
|---|---|
| `index.html` | accueil, en cartes illustrées à mots-clés : le cours, les activités, les études de cas |
| `?ex=cours-frottement-roulement` | Cours — Frottement et roulement (adhérence et frottement, colis simulé, coefficients, lois de Coulomb, résistance au roulement et ses deux exemples, automobile simulée, quiz) |
| `?ex=cle-excentrique` | Activité 1 — Clé à excentrique (exercice 5) : action de l'écrou, principe fondamental de la statique, couple de serrage |
| `?ex=voiture-pente` | Activité 2 — Voiture à l'arrêt dans une pente (exercice 6) : actions du sol, adhérence, pente limite |
| `?ex=voiture-pente-variantes` | Activité 3 — Voiture en pente : trois variantes (exercices 7, 8 et 9, regroupés) |
| `?ex=voiture-route-mouillee` | Activité 4 — Voiture sur route mouillée (exercice 10) |
| `?ex=resistance-roulement` | Activité 5 — Résistance au roulement (exercice 11) |
| `?ex=barbecue-arc-boutement` | Activité 6 — Barbecue de cheminée : arc-boutement (exercice 12) |

Le site traite le frottement **par le calcul** : la résolution graphique du chapitre (cône de frottement, lecture
graphique des lois) n'y figure pas. Chaque activité propose le mode entraînement ou le mode examen, avec sa propre
note pondérée par la durée de ses parties. Corrections apportées aux contenus d'origine et décisions :
[`NOTE-DE-LIVRAISON.md`](NOTE-DE-LIVRAISON.md).

**Ajouter une activité** : décrire ses parties dans `src/activites.py` (sur le modèle de `PARTS_CLE`), puis l'ajouter à
`EXO_DEFS` ; **ajouter une étude de cas** : même chose avec `"etude": True`. La carte apparaît d'elle-même sur
l'accueil (et remplace l'annonce « En cours d'édition »).

## Régénérer la page

La page est produite par un script, à partir du gabarit (`src/gabarit-exercice-interactif.html`, copie conforme de
celui du dépôt « Chaîne fonctionnelle », recopié sans modification de son style ni de ses moteurs) et du contenu
décrit dans `src/`.

```sh
python3 src/generer.py                                   # écrit index.html
NODE_PATH=$(npm root -g) node outils/captures.js         # seulement si les figures des cartes de l'accueil changent
bash outils/preparer-images.sh && python3 src/generer.py # (ImageMagick 6) recadre les cartes, puis régénère
```

## Tester

```sh
node --test tests/correction.test.js                          # moteur de correction : réponses de référence, réponses du manuel, unités, tolérances
NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js # accueil, cours, activités en entraînement et en examen, téléphone
```

`tests/reponses.js` contient la réponse juste de chaque question ; le parcours navigateur vérifie qu'une activité
entièrement juste donne 20/20, sans erreur JavaScript.

## Organisation

| Chemin | Rôle |
|---|---|
| `src/gabarit-exercice-interactif.html` | gabarit de référence (charte, moteurs de correction et d'application), repris tel quel |
| `src/generer.py` | accueil, éléments communs du cours, aiguillage, assemblage |
| `src/cours.py` | le cours : contenu, figures SVG, simulateurs du colis et de l'automobile |
| `src/activites.py` | les six activités : énoncés, questions, correcteurs, réponses calculées, document DT1 |
| `src/dessin.py` | figures redessinées : repère réel → repère du dessin, cotes, sol, roues, annotations, style |
| `src/figures.py` | formes des véhicules (voiture tout-terrain, cabriolet) |
| `src/images/originaux/` | pages photographiées du manuel (cours p. 123 à 131, exercices p. 138 et 139) et captures des cartes |
| `src/images/` | images des cartes de l'accueil (480 × 270), intégrées en data URI |
| `outils/captures.js`, `outils/preparer-images.sh` | photographie des figures pour les cartes (Playwright), recadrage (ImageMagick) |
| `tests/` | tests Node et Playwright |
| `.github/workflows/static.yml` | publication GitHub Pages (déclenchée sur la branche `main`) |
