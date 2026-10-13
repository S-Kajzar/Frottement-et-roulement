// Réponses justes de référence, telles qu'un élève les saisit, partagées par les tests Node et navigateur.
// Identifiants : <lettre de l'activité><partie>_<question> (a : activité 1 … g : activité 7) ; une question de QCM
// porte une case masquée « _1 » qui reçoit le rang des propositions choisies.
module.exports = {
  // Activité 1 — cônes (QCM 3 et 4)
  a1_1_1: "1,2", a1_2_1: "2",
  // Activité 2 — clé à excentrique (exercice 5)
  b1_1: "8,53°", b1_3: "79,9 daN", b1_4: "86,5 daN",
  b2_1: "62,5 daN", b2_2: "-49,8 daN", b2_3: "-62,5 daN", b2_4: "59,8 daN", b3_1: "13,4 N.m",
  // Activité 3 — voiture à l'arrêt dans une pente (exercice 6)
  c1_1: "30,96°", c1_3: "30,5°", c1_4: "oui", c1_5: "1159 daN", c1_6: "1943 daN", c2_1: "20,3",
  // Activité 4 — variantes (exercices 7, 8, 9)
  d1_1: "2020 mm", d2_1: "1943,3 daN", d2_2: "588,3 daN", d2_3: "non", d2_4: "2030,4 daN", d2_5: "998,4 daN",
  d3_1: "verticales, parallèles au poids", d3_2: "1981,8 daN", d3_3: "1018,2 daN",
  // Activité 5 — route mouillée (exercice 10)
  e1_1: "5878,5 N", e1_2: "500 N", e1_3: "4911,5 N", e2_1: "0,085", e2_2: "oui", e3_1: "500 N", e3_2: "0,102", e3_3: "non",
  // Activité 6 — résistance au roulement (exercice 11)
  f1_1: "0,0116", f1_2: "629 N", f1_3: "15725 W", f2_1: "0,107", f2_2: "non", f2_3: "0,128",
  // Activité 7 — barbecue, arc-boutement (exercice 12)
  g1_1: "4,57°", g1_3: "106,75 mm", g1_4: "oui", g2_1: "2,22°", g2_2: "77,4 daN", g2_3: "3 daN",
};
