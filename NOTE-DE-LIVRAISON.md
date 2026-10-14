# Note de livraison — Frottement et roulement : cours et activités interactifs

## Construction reprise du dépôt « Chaîne fonctionnelle »

**Sources** : le dépôt « Chaîne fonctionnelle » (construction : générateur, gabarit, accueil en cartes, aiguillage
`?ex=…`, modes entraînement et examen, tests, publication) et deux documents fournis, photographies de pages du
manuel, chapitre 9 « Frottement et roulement » : le cours (pages 123 à 131) et les exercices (pages 138 et 139 :
QCM 3 et 4, exercices 5 à 12). Les pages sont conservées, réduites, dans `src/images/originaux/` (`cours-p123.jpg`
à `cours-p131.jpg`, `exercices-p138.jpg`, `exercices-p139.jpg`).

**Dépôt non modifié** : « Chaîne fonctionnelle », consulté seulement. Son gabarit est copié tel quel dans
`src/gabarit-exercice-interactif.html` (fichier identique, vérifié octet par octet), avec ses moteurs ; comme dans ce
dépôt, seules les entrées réservées au sujet sont remplacées, chaque remplacement étant vérifié (`CONSEIL_MIN`,
`DECOR`, `DR_NAMES`, texte de la fenêtre « Imprimer les DR », libellé « Diagramme validé »). Le workflow de
publication est le même fichier.

**Accueil** (`index.html`), sur le modèle de « Chaîne fonctionnelle » : en-tête et illustration (le cabriolet de
l'exercice 10, avec les résistances de l'air et au roulement), puis les rubriques **Le cours**, **Les activités** et
**Études de cas** (une carte « En cours d'édition », remplacée d'elle-même par les études décrites dans
`activites.EXO_DEFS` avec `"etude": True`). Toutes les cartes ont la même taille, une image, une étiquette, un
titre, 3 à 5 mots-clés et un bouton (test navigateur). Les images des cartes sont photographiées dans les pages
(`outils/captures.js`) puis recadrées en 480 × 270 (`outils/preparer-images.sh`).

**Largeur du texte** : dans le cours, les activités et l'accueil, le texte occupe toute la largeur des blocs blancs.
Le gabarit limite les paragraphes, données, énoncés, indications et corrections à 72 à 80 caractères (ce qui
convient à un sujet imprimé) ; ces limites sont levées dans la feuille de style du contenu (`CONTENT_CSS` de
`src/generer.py`), sans modifier le gabarit. Remarques, définitions et encadrés de formules suivent la même règle. Les
figures gardent leur largeur maximale.

## Pas de résolution graphique

Le site traite le frottement **par le calcul** (principe fondamental de la statique, lois de Coulomb écrites en
égalités et inégalités). La résolution graphique du chapitre n'est pas reprise, ni en cours ni en exercice :

- le cours ne reprend pas ce que les pages 126 à 129 consacrent au cône de frottement et d'adhérence, à la lecture
  graphique des lois (figures 5, 7 et 8) et à l'exercice de la voiture qui monte sur un trottoir (figures 9 à 14) ; la démarche
  générale (figure 6) est écrite avec les seules égalités et inégalités ;
- les **QCM 3 et 4**, qui portent sur la position de l'action de contact par rapport au cône, ne sont pas repris ;
- les **exercices 5, 6 et 12**, que le manuel corrige d'ailleurs par le calcul, sont posés en résolution analytique.

Une première version comportait un cours de résolution graphique, une planche de construction (atelier et
constructions notées dans les activités) et une activité sur les cônes ; elle a été retirée à la demande. Elle reste
dans l'historique du dépôt (commit `fa9694d`) si elle devait resservir.

## Le cours

`?ex=cours-frottement-roulement`, `src/cours.py`. Le texte du manuel est conservé ; ses figures, photographiées
(ombres, pages courbées), sont **redessinées en SVG**. Pourquoi étudier le frottement (frein, courroie, serre-joint,
page 123) ; adhérence et frottement, exemple du colis (repos, adhérence, frottement, µ<sub>s</sub> et µ) avec un
**simulateur** (poussée, matériaux, masse, état, graphique de T en fonction de F, glissement entretenu entre µN et
µ<sub>s</sub>N) ; facteur de frottement et tableau des valeurs indicatives ; lois de Coulomb et démarche générale ;
résistance au roulement (figure 15, tableaux de a et f<sub>R</sub>), exemple 1 de l'automobile avec un **simulateur**
(masse, pneus, diamètre, vitesse ; figure 16 dont les valeurs suivent), exemple 2 de la roue porteuse (torseurs,
principe fondamental) ; l'essentiel en cartes, quiz de 8 questions. Le dernier objectif du chapitre (« applications :
coins et cônes, paliers à butée, système vis-écrou, liens flexibles ») n'est pas traité : les pages correspondantes ne
sont pas dans le document fourni.

## Les exercices découpés en activités

Chaque exercice devient une activité ; les plus courts sont regroupés, par deux ou trois au plus :

| Activité | Exercices du manuel | Parties, durée |
|---|---|---|
| 1 — Clé à excentrique | 5 | action de l'écrou, principe fondamental de la statique, couple de serrage ; 48 min |
| 2 — Voiture à l'arrêt dans une pente | 6 | actions du sol, pente limite ; 43 min |
| 3 — Voiture en pente : trois variantes | 7, 8 et 9 (regroupés : variantes courtes de l'exercice 6) | 3 parties, 32 min |
| 4 — Voiture sur route mouillée | 10 | 3 parties, 38 min |
| 5 — Résistance au roulement | 11 | 2 parties, 22 min |
| 6 — Barbecue de cheminée : arc-boutement | 12 | arc-boutement, actions en A et B ; 40 min |

Les questions sont celles du manuel, découpées en réponses notées : valeurs avec unité (la valeur vaut la moitié des
points, l'unité l'autre moitié ; une force s'écrit en daN ou en N), oui / non, réponses courtes. Chaque démarche
corrigée est rédigée ; **toutes les réponses attendues sont calculées** dans `src/activites.py` à partir des données de
l'énoncé, et les réponses du manuel sont vérifiées par les tests. Document consultable : **DT1** (lois du frottement,
valeurs indicatives, résistance au roulement, principe fondamental de la statique). Les figures des énoncés sont
redessinées aux cotes de l'énoncé (`src/dessin.py`, `src/figures.py`).

## Corrections apportées aux contenus d'origine et décisions

- **Exemple 1 de la résistance au roulement** : le manuel annonce des « pneus verts » de facteur f<sub>R2</sub> =
  0,085 et écrit « 0,085 × 1 079 = 9,17 daN » ; ses propres résultats (a<sub>2</sub> = 290 × 0,008 5 = 2,46 mm,
  9,17 daN, 91,7 N) correspondent à **0,008 5**, valeur retenue partout.
- **Exemple 2 (roue porteuse)** : le manuel écrit « F<sub>rr</sub> = −a·P / r = −f<sub>R</sub>·P » et « R = −P » ; le
  signe ne fait qu'indiquer le sens (F<sub>rr</sub> vers l'arrière, P vers le bas). Le cours écrit la charge −P dans le
  torseur du véhicule et conclut R = P, F<sub>rr</sub> = F<sub>m</sub> = f<sub>R</sub>·P, avec une note qui explique
  l'écriture du manuel. La figure 17 (blocs de la bande de roulement) n'est pas redessinée : son contenu est repris
  dans le texte.
- **Exercice 5** : le manuel donne « A<sub>y</sub> = 49,8 » sans signe ; dans le repère de l'activité (x vers C,
  y vers le haut), la composante est **−49,8 daN** (l'écrou pousse le manche vers le bas). La correction le dit ; la
  valeur sans signe est refusée pour une composante algébrique. L'inclinaison de l'action en A (30° + 8,53°) vient de
  la loi du frottement : au serrage, la came glisse sur l'écrou, T<sub>A</sub> = f·N<sub>A</sub>. Le point A est placé
  par les cotes (24, 4 et 30°) : x<sub>A</sub> = −24 + 4 / tan 30°, ce qui redonne exactement les valeurs du manuel.
- **Exercice 6** : le manuel ne donne pas de réponse. L'équilibre est possible, de justesse (T<sub>A</sub>/N<sub>A</sub>
  = 0,589 &lt; 0,6) ; la pente limite est de **20,3 %** (question b). La roue freinée est A, la roue du haut sur la
  figure : c'est ce que confirment les réponses des exercices 7 et 8.
- **Exercice 8** : N<sub>B</sub> = 1 943,3 daN par le calcul (manuel : 1 942,9, écart d'arrondi) ; les deux valeurs sont
  acceptées, comme toutes les réponses du manuel (test).
- **Exercice 10** : dans les réponses b) et c), le manuel a **interverti les coefficients** : « f<sub>B</sub> = 0,102 &gt;
  0,1 » et « f<sub>A</sub> = 0,085 &lt; 0,1 ». Le calcul donne 500 / 5 878,5 = 0,085 à l'avant et 500 / 4 911,5 = 0,102
  à l'arrière ; ses conclusions (oui, puis non) sont justes. Les corrections le signalent.
- **Exercice 11** : le manuel ne donne pas de réponse, et la réponse dépend du modèle. L'activité retient celui du
  cours (figure 16 : résistances au roulement schématisées par des forces horizontales au contact), écrit dans
  l'énoncé : T = 500 + 57 + 72 = 629 N, et **les roues patinent dans les deux cas** (0,107 et 0,128 &gt; 0,1). **À
  valider** : avec un modèle plus fin, la résistance au roulement d'une roue motrice est un moment, pas une force à
  transmettre par adhérence ; la traction avant n'aurait alors à transmettre que 557 N (0,095 &lt; 0,1). Deux
  questions ont été ajoutées pour relier l'exercice au cours : le facteur f<sub>R</sub> ≈ 0,012 et la puissance à
  90 km/h (15,7 kW).
- **Exercice 12** : pas de réponse dans le manuel. Résolution analytique : avec des actions également inclinées
  (T<sub>A</sub> = T<sub>B</sub> = P / 2), les moments en A donnent N = (233 + 12)·P / 19 ≈ 12,89·P, d'où T / N = 19 / 490
  ≈ 0,039 &lt; 0,08, indépendant de P : arc-boutement quelle que soit la charge. Question ajoutée : la distance minimale
  de la charge à la tige, **106,75 mm** : en deçà, aucune répartition des efforts tangentiels entre A et B ne respecte
  l'adhérence aux deux contacts. Pour P = 6 daN : N = 77,4 daN, T = 3 daN.
- **Passages délavés** des photographies, lus après renforcement du contraste : la remarque sur la puissance et la
  part de la consommation (22 % et 16 %, page 130), l'introduction de l'exemple 2, les questions a) et b) des exercices
  6 et 12.
- **Les QCM 1 et 2** sont sur la page précédant les exercices, absente du document fourni ; les QCM 3 et 4 ne sont
  pas repris (résolution graphique).

## Points signalés sans modification

- **À vérifier** : les pages photographiées du manuel (`src/images/originaux/cours-p*.jpg`, `exercices-p*.jpg`) sont
  dans le dépôt, qui est publié en entier par GitHub Pages (`path: '.'`) ; leur publication suppose l'accord de
  l'éditeur. Elles ne sont pas intégrées dans la page (toutes les figures sont redessinées) : on peut les retirer du
  dépôt sans rien casser, ou les exclure de la publication.
- La publication se déclenche sur la branche `main` (workflow repris tel quel) ; `main` ne contient pour l'instant qu'un
  commit initial vide, base de la pull request.
- Poids : `index.html` environ 445 Kio, dont 92 Kio d'images (les cartes de l'accueil).

## Vérifications effectuées

- `node --test tests/correction.test.js` : 7 tests — configuration (6 activités, parties, durées, aucun tracé),
  réponse de référence juste pour chaque question, réponses du manuel acceptées (et ses erreurs refusées :
  A<sub>y</sub> sans signe, coefficients intervertis de l'exercice 10), unités (daN ou N, demi-point sans unité ou avec
  une autre unité), tolérances, oui / non et réponses courtes, absence de toute résolution graphique dans la page.
- `tests/navigateur.test.js` (Playwright, Chromium) : 11 parcours, tous réussis — accueil (8 cartes illustrées de même
  taille, rubriques, téléphone, aucune mention de diplôme ou d'épreuve) ; adresses inconnues et anciennes pages
  graphiques renvoyées à l'accueil ; cours (colis : repos, adhérence, glissement, glissement entretenu, arrêt ;
  automobile : 12,95 daN, 3,24 kW, 3,48 mm, pneus verts 9,17 daN ; texte en pleine largeur ; quiz 8/8) ; chacune des six
  activités en entraînement (20/20, toutes les démarches affichées) ; activité 6 en examen (rien avant la remise, note
  pondérée 12,5/20 pour une partie sur deux) ; téléphone (sans défilement horizontal).
- Aucune erreur JavaScript dans aucun parcours.
