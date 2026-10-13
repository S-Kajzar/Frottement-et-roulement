// Tests unitaires du moteur de correction appliqué aux activités.
//   node --test tests/correction.test.js
// Le moteur (Grading) et la configuration (__EXOS__) sont lus dans la page générée : on teste exactement ce que
// l'élève utilisera.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
const code = html.slice(html.indexOf("/*GRADING-START*/"), html.indexOf("/*GRADING-END*/"));
const mod = { exports: {} };
new Function("module", code + "\nmodule.exports = Grading;")(mod);
const G = mod.exports;
const EXOS = JSON.parse(html.match(/window\.__EXOS__ = (.*?);<\/script>/)[1]);
const REP = require("./reponses.js");
const QCFG = Object.assign({}, ...Object.values(EXOS).map((e) => e.qcfg));
const score = (id, ans) => { const r = G.grade(ans, QCFG[id].grader); return r.invalid ? "invalid" : r.score; };

test("configuration : sept activités, leurs parties, leurs durées et leurs constructions", () => {
  const resume = Object.fromEntries(Object.entries(EXOS).map(([k, e]) =>
    [k, [e.parts.length, Object.keys(e.qcfg).length, Object.keys(e.skcfg).length, e.minutes]]));
  assert.deepEqual(resume, {
    "cones-adherence-frottement": [1, 2, 0, 6], "cle-excentrique": [3, 8, 1, 53], "voiture-pente": [2, 6, 1, 45],
    "voiture-pente-variantes": [3, 9, 0, 32], "voiture-route-mouillee": [3, 8, 0, 38],
    "resistance-roulement": [2, 6, 0, 22], "barbecue-arc-boutement": [2, 6, 1, 40] });
  // chaque construction attend les questions dont sa correction donne la réponse
  assert.deepEqual(EXOS["voiture-pente"].skcfg.c1_2.deps, ["c1_1", "c1_3", "c1_4", "c1_5", "c1_6"]);
  assert.equal(EXOS["cle-excentrique"].skcfg.b1_2.deps.length, 8);
  assert.equal(EXOS["barbecue-arc-boutement"].skcfg.g1_2.pts, 5);
});

test("chaque question a sa réponse de référence, et elle est juste", () => {
  assert.deepEqual(Object.keys(REP).sort(), Object.keys(QCFG).sort());
  for (const [id, ans] of Object.entries(REP)) assert.equal(score(id, ans), 1, `${id} : ${ans}`);
});

test("les réponses du manuel sont acceptées (unités comprises)", () => {
  const LIVRE = { b2_1: "62,5 daN", b2_4: "59,8 daN", b3_1: "13,4 Nm", d1_1: "2 020 mm", d2_1: "1 942,9 daN",
                  d2_2: "588,3 daN", d2_4: "2 030,4 daN", d2_5: "998,4 daN", d3_2: "1 981,8 daN", d3_3: "1 018,2 daN",
                  e1_1: "5 878,5 N", e1_2: "500 N", e1_3: "4 911,50 N", b1_3: "80 daN" };
  for (const [id, ans] of Object.entries(LIVRE)) assert.equal(score(id, ans), 1, `${id} : ${ans}`);
  // le manuel donne A_y sans signe : c'est une valeur absolue, la composante algébrique est négative
  assert.equal(score("b2_2", "49,8 daN"), 0);
  // exercice 10 : le manuel a interverti les deux coefficients ; on attend 0,085 à l'avant, 0,102 à l'arrière
  assert.equal(score("e2_1", "0,102"), 0);
  assert.equal(score("e3_2", "0,085"), 0);
});

test("unités : une force s'écrit en daN ou en N ; sans unité ou avec une autre unité, demi-point", () => {
  assert.equal(score("b1_3", "799 N"), 1);
  assert.equal(score("e1_1", "587,85 daN"), 1);
  assert.equal(score("b1_3", "79,9"), 0.5);
  assert.equal(score("b1_3", "79,9 kg"), 0.5);
  assert.equal(score("b1_3", "79,9 N"), 0.5, "valeur juste, unité fausse : demi-point (règle du gabarit)");
  assert.equal(score("b3_1", "13,4 N·m"), 1);
  assert.equal(score("c1_3", "30,5 degrés"), 1);
  assert.equal(score("f1_3", "15,7 kW"), 1);
  assert.equal(score("g1_3", "107 mm"), 1);
});

test("lectures graphiques : tolérance de 3 % sur les normes, 0,3° sur les angles", () => {
  assert.equal(score("c1_5", "1125 daN"), 1);
  assert.equal(score("c1_5", "1100 daN"), 0);
  assert.equal(score("b1_4", "84 daN"), 1);
  assert.equal(score("b1_4", "80 daN"), 0);
  assert.equal(score("c1_3", "30,8°"), 1);
  assert.equal(score("c1_3", "31,0°"), 0);
});

test("réponses rédigées et oui / non", () => {
  assert.equal(score("c1_4", "Oui, de justesse"), 1);
  assert.equal(score("c1_4", "non"), 0);
  assert.equal(score("d2_3", "Non, T/N = 0,3 < 0,6"), 1);
  assert.equal(score("c1_4", "peut-être"), "invalid");
  for (const a of ["verticales", "elles sont verticales", "parallèles à P", "verticalement"]) assert.equal(score("d3_1", a), 1, a);
  for (const a of ["horizontales", "perpendiculaires à la pente", "normales au sol"]) assert.equal(score("d3_1", a), 0, a);
});

test("QCM : toutes les bonnes propositions, et aucune autre", () => {
  assert.equal(score("a1_1_1", "1,2"), 1);
  assert.equal(score("a1_1_1", "1"), 0);
  assert.equal(score("a1_1_1", "1,2,3"), 0);
  assert.equal(score("a1_2_1", "2"), 1);
  assert.equal(score("a1_2_1", "1,2"), 0);
});
