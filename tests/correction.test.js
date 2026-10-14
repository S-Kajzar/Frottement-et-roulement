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

test("configuration : six activités analytiques, leurs parties et leurs durées", () => {
  const resume = Object.fromEntries(Object.entries(EXOS).map(([k, e]) =>
    [k, [e.parts.length, Object.keys(e.qcfg).length, e.minutes]]));
  assert.deepEqual(resume, {
    "cle-excentrique": [3, 9, 48], "voiture-pente": [2, 7, 43], "voiture-pente-variantes": [3, 9, 32],
    "voiture-route-mouillee": [3, 8, 38], "resistance-roulement": [2, 6, 22], "barbecue-arc-boutement": [2, 7, 40] });
  for (const e of Object.values(EXOS)) assert.deepEqual(e.skcfg, {}, "aucun tracé");
});

test("chaque question a sa réponse de référence, et elle est juste", () => {
  assert.deepEqual(Object.keys(REP).sort(), Object.keys(QCFG).sort());
  for (const [id, ans] of Object.entries(REP)) assert.equal(score(id, ans), 1, `${id} : ${ans}`);
});

test("les réponses du manuel sont acceptées (unités comprises)", () => {
  const LIVRE = { a2_1: "62,5 daN", a2_4: "59,8 daN", a3_1: "13,4 Nm", c1_1: "2 020 mm", c2_1: "1 942,9 daN",
                  c2_2: "588,3 daN", c2_4: "2 030,4 daN", c2_5: "998,4 daN", c3_2: "1 981,8 daN", c3_3: "1 018,2 daN",
                  d1_1: "5 878,5 N", d1_2: "500 N", d1_3: "4 911,50 N" };
  for (const [id, ans] of Object.entries(LIVRE)) assert.equal(score(id, ans), 1, `${id} : ${ans}`);
  // le manuel donne A_y sans signe : c'est une valeur absolue, la composante algébrique est négative
  assert.equal(score("a2_2", "49,8 daN"), 0);
  // exercice 10 : le manuel a interverti les deux coefficients ; on attend 0,085 à l'avant, 0,102 à l'arrière
  assert.equal(score("d2_1", "0,102"), 0);
  assert.equal(score("d3_2", "0,085"), 0);
});

test("unités : une force s'écrit en daN ou en N ; sans unité ou avec une autre unité, demi-point", () => {
  assert.equal(score("a2_5", "799 N"), 1);
  assert.equal(score("d1_1", "587,85 daN"), 1);
  assert.equal(score("a2_5", "79,9"), 0.5);
  assert.equal(score("a2_5", "79,9 kg"), 0.5);
  assert.equal(score("a2_5", "79,9 N"), 0.5, "valeur juste, unité fausse : demi-point (règle du gabarit)");
  assert.equal(score("a3_1", "13,4 N·m"), 1);
  assert.equal(score("a1_2", "38,5 degrés"), 1);
  assert.equal(score("e1_3", "15,7 kW"), 1);
  assert.equal(score("f1_4", "107 mm"), 1);
});

test("tolérances : 1 % sur les calculs, et pas davantage", () => {
  assert.equal(score("b1_6", "1159 daN"), 1);
  assert.equal(score("b1_6", "1120 daN"), 0);
  assert.equal(score("a2_6", "86 daN"), 1);
  assert.equal(score("a2_6", "84 daN"), 0);
  assert.equal(score("a1_2", "30°"), 0, "la normale seule, sans le frottement");
  assert.equal(score("b1_4", "0,6"), 0, "le rapport nécessaire, pas le coefficient disponible");
});

test("réponses rédigées et oui / non", () => {
  assert.equal(score("b1_5", "Oui, de justesse"), 1);
  assert.equal(score("b1_5", "non"), 0);
  assert.equal(score("c2_3", "Non, T/N = 0,3 < 0,6"), 1);
  assert.equal(score("b1_5", "peut-être"), "invalid");
  for (const a of ["verticales", "elles sont verticales", "parallèles à P", "verticalement"]) assert.equal(score("c3_1", a), 1, a);
  for (const a of ["horizontales", "perpendiculaires à la pente", "normales au sol"]) assert.equal(score("c3_1", a), 0, a);
});

test("la page ne traite pas la résolution graphique", () => {
  const src = html.replace(/data:[^"]+/g, "");
  assert.doesNotMatch(src, /cône|planche|dynamique|résolution graphique/i);
});
