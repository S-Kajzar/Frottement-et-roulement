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

**Accueil** (`index.html`), sur le modèle de « Chaîne fonctionnelle » : en-tête et illustration (la voiture au pied du
trottoir, cône de frottement en D), puis les rubriques **Les cours**, **L'atelier graphique**, **Les activités** et
**Études de cas** (une carte « En cours d'édition », remplacée d'elle-même par les études décrites dans
`activites.EXO_DEFS` avec `"etude": True`). Toutes les cartes ont la même taille, une image, une étiquette, un
titre, 3 à 5 mots-clés et un bouton (test navigateur). Les images des cartes sont photographiées dans les pages
(`outils/captures.js`) puis recadrées en 480 × 270 (`outils/preparer-images.sh`).

**Pastilles** : les niveaux (Niveau 1 / Niveau 2) de « Chaîne fonctionnelle » deviennent la **méthode** de résolution,
puisque le cours est scindé en deux : pastille verte **Analytique**, pastille bleue **Graphique**.

## Le cours scindé en deux

Le texte du manuel est conservé, réparti entre les deux cours ; ses figures, photographiées (ombres, pages
courbées), sont toutes **redessinées en SVG**.

- **Cours 1 — approche analytique** (`?ex=cours-frottement-analytique`, `src/cours_analytique.py`) : pourquoi étudier
  le frottement (frein, courroie, serre-joint, page 123) ; adhérence et frottement, exemple du colis (repos,
  adhérence, frottement, µ<sub>s</sub> et µ) avec un **simulateur** (poussée, matériaux, masse, état, graphique de
  T en fonction de F, glissement entretenu entre µN et µ<sub>s</sub>N) ; facteur de frottement et tableau des valeurs
  indicatives ; lois de Coulomb écrites en inégalités et démarche générale (figure 6 du manuel, écrite avec les
  inégalités) ; résistance au roulement (figure 15, tableaux de a et f<sub>R</sub>), exemple 1 de l'automobile avec un
  **simulateur** (masse, pneus, diamètre, vitesse ; figure 16 dont les valeurs suivent), exemple 2 de la roue porteuse
  (torseurs, principe fondamental) ; l'essentiel en cartes, quiz de 8 questions.
- **Cours 2 — résolution graphique** (`?ex=cours-frottement-graphique`, `src/cours_graphique.py`) : angle et cône de
  frottement (figure 5), les trois cas des lois lus sur le cône (figures 7 et 8) avec un **cône manipulable** (on
  incline l'action de contact, à la souris ou au clavier) et un jeu « dans, sur ou hors du cône » ; méthode des trois
  forces avec un cône ; l'exercice de la voiture qui monte sur un trottoir (figures 9 à 14) en **démonstration pas à
  pas sur la planche** : a) roues arrière motrices, b) hauteur limite, c) roues avant motrices, d) quatre roues
  motrices, puis « Construire moi-même » sur le même fond ; lecture graphique de la résistance au roulement ;
  l'essentiel, quiz de 8 questions.
- Objectifs et prérequis sont propres à chaque cours. Le dernier objectif du chapitre (« applications : coins et
  cônes, paliers à butée, système vis-écrou, liens flexibles ») n'est pas traité : les pages correspondantes ne
  sont pas dans le document fourni. L'arc-boutement est abordé par le serre-joint (cours 1), la méthode (cours 2) et
  l'activité 7.

## Les exercices découpés en activités

Chaque exercice devient une activité ; les plus courts sont regroupés, par deux ou trois au plus :

| Activité | Exercices du manuel | Méthode | Parties, durée |
|---|---|---|---|
| 1 — Cônes d'adhérence et de frottement | QCM 3 et 4 (regroupés : deux questions) | Graphique | 1 partie, 6 min |
| 2 — Clé à excentrique | 5 | Graphique | construction, vérification analytique, couple de serrage ; 53 min |
| 3 — Voiture à l'arrêt dans une pente | 6 | Graphique | construction, pente limite ; 45 min |
| 4 — Voiture en pente : trois variantes | 7, 8 et 9 (regroupés : variantes courtes de l'exercice 6) | Analytique | 3 parties, 32 min |
| 5 — Voiture sur route mouillée | 10 | Analytique | 3 parties, 38 min |
| 6 — Résistance au roulement | 11 | Analytique | 2 parties, 22 min |
| 7 — Barbecue de cheminée : arc-boutement | 12 | Graphique | construction, actions en A et B ; 40 min |

Les questions sont celles du manuel, découpées en réponses notées : valeurs avec unité (la valeur vaut la moitié des
points, l'unité l'autre moitié ; une force s'écrit en daN ou en N), oui / non, réponses courtes, QCM. Chaque
démarche corrigée est rédigée ; **toutes les réponses attendues sont calculées** dans `src/activites.py` à partir des
données de l'énoncé, et les réponses du manuel sont vérifiées par les tests. Documents consultables : **DT1** (lois
du frottement, valeurs indicatives, résistance au roulement, solide soumis à trois forces) et **DT2** (mode d'emploi
de la planche, méthode des trois forces).

## L'environnement de construction graphique

La demande parle de « cinématique graphique » ; les exercices de ce chapitre relèvent de la **statique graphique**
(trois forces concourantes, cônes de frottement, dynamique). L'environnement est construit pour eux, mais reste
général : l'unité de l'échelle des vecteurs est un paramètre de la planche (`forces.u`), une activité de cinématique
graphique pourra l'utiliser avec des vitesses.

Les tracés du gabarit (crayon, ligne, flèche, sur une image) ne permettent pas de construire juste. La **planche**
(`src/planche.js`, `src/planche.css`, `src/construction.py`) les remplace pour les constructions, sans toucher au
gabarit :

- une feuille **cotée en millimètres**, quadrillée, dont le fond est le mécanisme dessiné à l'échelle (clé 1:1,
  voiture en pente 1:50, barbecue 1:2, trottoir 1:30), avec ses éléments donnés (points, normales, forces connues) ;
- les outils de la règle et du rapporteur : droite, segment, parallèle, perpendiculaire, droite **inclinée** d'un
  angle saisi, **cône de frottement** (on clique le contact et la normale, on saisit f ou φ ; ses génératrices sont
  des droites, leurs intersections s'aimantent), **vecteur à l'échelle des forces** (norme affichée pendant le tracé,
  nom et norme saisis ensuite : le vecteur garde sa direction), point nommé, distance (en mm de feuille et réels),
  angle aigu entre deux droites, texte, gomme, annuler, rétablir, tout effacer, trois couleurs, zoom, main, plein
  écran ;
- l'**aimantation** aux points, aux intersections et aux droites, signalée sous le pointeur ; un **tableau des
  relevés** (vecteurs, normes, directions, distances, angles) où l'élève lit les valeurs qu'il saisit ensuite ;
- l'**impression du document réponse à l'échelle** (fenêtre à imprimer en A4 paysage à 100 % : la feuille garde ses
  dimensions en millimètres), pour construire aussi à la main ;
- dans une activité, la planche compte comme un **tracé du gabarit** (entrée `__SKCFG__`, critères d'auto-évaluation,
  note de la partie) : en entraînement, « Valider ma construction » la verrouille, et sa **correction superposée**
  (rouge) s'affiche quand les questions qui en lisent les résultats sont validées (sinon elle les donnerait) ; en
  examen, tout apparaît à la remise de la copie ; l'élève coche ensuite les critères que sa construction remplit ;
- dans le cours 2, la planche déroule une **démonstration** par étapes (texte et tracés), cas par cas ; dans
  l'atelier, elle est **libre**, avec cinq fonds au choix et l'échelle des forces réglable.

Les corrections sont **calculées**, pas recopiées : `src/construction.py` place chaque élément dans le repère réel du
mécanisme, calcule intersections, directions et dynamiques (mêmes données que les réponses attendues), puis convertit
en coordonnées de feuille. `tests/construction.test.js` vérifie que les vecteurs corrigés, mesurés à l'échelle,
donnent les réponses attendues, que les dynamiques sont fermés et que les points de concours sont au bon endroit.

## Corrections apportées aux contenus d'origine et décisions

- **Exemple 1 de la résistance au roulement** : le manuel annonce des « pneus verts » de facteur f<sub>R2</sub> =
  0,085 et écrit « 0,085 × 1 079 = 9,17 daN » ; ses propres résultats (a<sub>2</sub> = 290 × 0,008 5 = 2,46 mm,
  9,17 daN, 91,7 N) correspondent à **0,008 5**, valeur retenue partout.
- **Exemple 2 (roue porteuse)** : le manuel écrit « F<sub>rr</sub> = −a·P / r = −f<sub>R</sub>·P » et « R = −P » ; le
  signe ne fait qu'indiquer le sens (F<sub>rr</sub> vers l'arrière, P vers le bas). Le cours écrit la charge −P dans le
  torseur du véhicule et conclut R = P, F<sub>rr</sub> = F<sub>m</sub> = f<sub>R</sub>·P, avec une note qui explique
  l'écriture du manuel. La figure 17 (blocs de la bande de roulement) n'est pas redessinée : son contenu est repris
  dans le texte (compression, cisaillement, pressions de contact).
- **Exercice 5** : le manuel donne « A<sub>y</sub> = 49,8 » sans signe ; dans le repère de l'activité (x vers C,
  y vers le haut), la composante est **−49,8 daN** (l'écrou pousse le manche vers le bas). La correction le dit ; la
  valeur sans signe est refusée pour une composante algébrique. Le point A est placé par les cotes (24, 4 et 30°) :
  x<sub>A</sub> = −24 + 4 / tan 30° ; l'écrou dessiné a 16 mm sur plats, A au milieu de sa face, la normale passant
  par D, ce qui redonne exactement les valeurs du manuel.
- **Exercice 6** : le manuel ne donne pas de réponse. L'équilibre est possible, de justesse (T<sub>A</sub>/N<sub>A</sub>
  = 0,589 &lt; 0,6, α = 30,5° &lt; φ<sub>s</sub> = 31,0°) ; la pente limite est de **20,3 %** (question b). La roue
  freinée est A, la roue du haut sur la figure : c'est ce que confirment les réponses des exercices 7 et 8.
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
- **Exercice 12** : pas de réponse dans le manuel. Arc-boutement si la droite d'action de P passe à plus de
  **106,75 mm** de la face de la tige (question ajoutée, lue sur la zone d'arc-boutement) ; 233 mm : arc-boutement quel
  que soit P. Avec α<sub>A</sub> = α<sub>B</sub> : tan α = 19 / 490, α = 2,22°, A = B = 77,4 daN, T = 3 daN.
- **QCM 3 et 4** : pas de corrigé dans le manuel. Q3 (adhérence) : a et b — l'action peut être n'importe où dans le
  cône, ou sur lui à l'équilibre strict ; Q4 (frottement) : b seulement. Les deux questions sont à réponses multiples,
  pour ne pas souffler la réponse. **Les QCM 1 et 2** sont sur la page précédente, absente du document fourni.
- **Montée de trottoir (cours 2)** : la figure du manuel n'est pas cotée. Les dimensions sont choisies (roues de
  360 mm de rayon, empattement 2 800 mm, G à 1 600 mm de l'essieu avant et 700 mm du sol, trottoir de 200 mm) et
  écrites sur la planche ; elles redonnent les quatre conclusions du manuel (α = 46,1° &gt; φ = 38,7° en D ;
  α<sub>B</sub> = 63,6° &gt; φ en B ; une infinité de solutions entre M et N à quatre roues motrices) et une hauteur
  limite d'environ 151 mm.
- **Passages délavés** des photographies, lus après renforcement du contraste : la remarque sur la puissance et la
  part de la consommation (22 % et 16 %, page 130), l'introduction de l'exemple 2, les questions a) et b) des exercices
  6 et 12.
- Les noms de l'exercice (clé « à excentrique », « barbecue de cheminée ») et les valeurs numériques du manuel sont
  conservés ; « µ » se lit « mu ».

## Points signalés sans modification

- **À vérifier** : les pages photographiées du manuel (`src/images/originaux/cours-p*.jpg`, `exercices-p*.jpg`) sont
  dans le dépôt, qui est publié en entier par GitHub Pages (`path: '.'`) ; leur publication suppose l'accord de
  l'éditeur. Elles ne sont pas intégrées dans la page (toutes les figures sont redessinées) : on peut les retirer du
  dépôt sans rien casser, ou les exclure de la publication.
- La publication se déclenche sur la branche `main` (workflow repris tel quel) ; ce travail est sur la branche
  `claude/friction-roulement-skeleton-pvlqfj`, la première du dépôt.
- La planche se manipule à la souris, au doigt ou au stylet ; ses outils sont accessibles au clavier, mais pas le tracé
  lui-même (comme les tracés du gabarit).
- Poids : `index.html` environ 690 Kio, dont 157 Kio d'images (les cartes de l'accueil).

## Vérifications effectuées

- `node --test tests/correction.test.js` : 7 tests — configuration (7 activités, parties, durées, constructions et
  leurs dépendances), réponse de référence juste pour chaque question, réponses du manuel acceptées (et ses erreurs
  refusées : A<sub>y</sub> sans signe, coefficients intervertis de l'exercice 10), unités (daN ou N, demi-point sans
  unité), tolérances des lectures graphiques (3 % sur les normes, 0,3° sur les angles), oui / non et réponses courtes,
  QCM à réponses multiples.
- `node --test tests/construction.test.js` : 8 tests — géométrie (intersections, parallèles, perpendiculaires,
  rotations dans le sens trigonométrique de l'écran, découpage par la feuille, distances), saisie (« 0,15 », « 8,5° »),
  corrections des trois planches cohérentes avec les réponses attendues (normes à l'échelle, dynamiques fermés, point
  de concours, α dans le cône, pointe de la zone d'arc-boutement), démonstration du trottoir (quatre cas, dynamiques
  fermés, conclusions), fonds de l'atelier sans correction.
- `tests/navigateur.test.js` (Playwright, Chromium) : 12 parcours, tous réussis — accueil (11 cartes illustrées de même
  taille, rubriques, téléphone, aucune mention de diplôme ou d'épreuve) ; adresse inconnue ; cours 1 (colis : repos,
  adhérence, glissement, glissement entretenu, arrêt ; automobile : 12,95 daN, 3,24 kW, 3,48 mm, pneus verts 9,17 daN ;
  quiz 8/8) ; cours 2 (cône manipulable au clavier, jeu 6/6, démonstration pas à pas, construction libre, quiz 8/8) ;
  atelier (changement de fond, vecteur à l'échelle, distance réelle, annuler, rétablir, gomme, document réponse de
  215 mm de large) ; activité 2 en entraînement (construction complète à la souris, relevés 79,9 et 86,5 daN,
  correction après validation des lectures, auto-évaluation, 20/20) ; activité 7 en examen (rien avant la remise,
  planche verrouillée et corrigée ensuite, note pondérée exacte) ; activité 1 (QCM, 20/20) ; activités 4, 5 et 6
  (20/20) ; téléphone (planche dans l'écran, sans défilement horizontal).
- Aucune erreur JavaScript dans aucun parcours.
