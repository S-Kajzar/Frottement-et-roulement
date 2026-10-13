// Tests de la planche de construction : géométrie du moteur (src/planche.js, lue dans la page générée) et
// cohérence des corrections superposées avec les réponses attendues des questions.
//   node --test tests/construction.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
const code = html.slice(html.indexOf("/*GEOM-START*/"), html.indexOf("/*GEOM-END*/"));
const mod = { exports: {} };
new Function("module", code + "\nmodule.exports = Geom;")(mod);
const G = mod.exports;
const PL = JSON.parse(html.match(/window\.__PLANCHES__ = (.*?);<\/script>/)[1]);
const EXOS = JSON.parse(html.match(/window\.__EXOS__ = (.*?);<\/script>/)[1]);
const QCFG = Object.assign({}, ...Object.values(EXOS).map((e) => e.qcfg));
const near = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg || ""} ${a} ≠ ${b} (± ${tol})`);
const len = (v) => Math.hypot(v.x2 - v.x1, v.y2 - v.y1);
const vecs = (objs) => Object.fromEntries(objs.filter((o) => o.k === "vec" && o.n).map((o) => [o.n, o]));
const dynamique = (objs) => objs.filter((o) => o.k === "vec" && o.x1 > -1).slice(-3);

test("géométrie : intersections, parallèles, perpendiculaires, droites inclinées", () => {
  const L1 = G.line(0, 0, 1, 0), L2 = G.line(5, -3, 0, 2);
  const I = G.intersect(L1, L2);
  near(I.x, 5, 1e-9); near(I.y, 0, 1e-9);
  assert.equal(G.intersect(L1, G.line(0, 4, 3, 0)), null, "deux droites parallèles ne se coupent pas");
  const P = G.parallel(G.line(0, 0, 1, 1), { x: 2, y: 0 });
  near(P.ux, Math.SQRT1_2, 1e-9); near(P.x, 2, 1e-9);
  const Q = G.perpendicular(L1, { x: 3, y: 3 });
  near(Math.abs(Q.uy), 1, 1e-9);
  // sens trigonométrique de l'écran (y vers le bas) : +90° tourne l'horizontale vers le haut
  const R = G.inclined(L1, { x: 0, y: 0 }, 90);
  near(R.ux, 0, 1e-9); near(R.uy, -1, 1e-9);
  near(G.heading(1, -1), 45, 1e-9);
  near(G.acute(L1, G.line(0, 0, 1, -Math.sqrt(3))), 60, 1e-9);
  near(G.acute(L1, G.line(0, 0, -1, 0.0001)), 0, 0.01, "l'angle de deux droites est aigu");
});

test("géométrie : découpage d'une droite par la feuille, distances", () => {
  const c = G.clip(G.line(10, 10, 1, 1), 100, 50);
  near(c[0].x, 0, 1e-9); near(c[0].y, 0, 1e-9); near(c[1].x, 50, 1e-9); near(c[1].y, 50, 1e-9);
  assert.equal(G.clip(G.line(0, 80, 1, 0), 100, 50), null, "une droite hors de la feuille n'est pas tracée");
  near(G.distLine({ x: 0, y: 5 }, G.line(0, 0, 1, 0)), 5, 1e-9);
  near(G.distSeg({ x: 15, y: 0 }, { x: 0, y: 0 }, { x: 10, y: 0 }), 5, 1e-9);
});

test("saisie : nombres à la française, coefficient de frottement ou angle", () => {
  near(G.parseNum("1 200,5"), 1200.5, 1e-9);
  near(G.parseNum("−3,2"), -3.2, 1e-9);
  assert.equal(G.parseNum("abc"), null);
  near(G.parsePhi("0,15"), 8.5308, 1e-3, "f = 0,15");
  near(G.parsePhi("8,5°"), 8.5, 1e-9, "φ en degrés");
  near(G.parsePhi("31"), 31, 1e-9, "au-delà de 1,5 : des degrés");
  assert.equal(G.parsePhi("0"), null);
});

test("clé à excentrique : la correction donne les normes attendues et un dynamique fermé", () => {
  const c = PL.b1_2, v = vecs(c.corr), e = c.forces.choix[0];
  near(len(v["A3/1"]) * e, QCFG.b1_3.grader.value, 0.05, "‖A3/1‖");
  near(len(v["B2/1"]) * e, QCFG.b1_4.grader.value, 0.05, "‖B2/1‖");
  near(len(v.F) * e, 10, 1e-6, "F à l'échelle");
  const d = dynamique(c.corr);
  near(d[2].x2, d[0].x1, 1e-6); near(d[2].y2, d[0].y1, 1e-6);
  // A3/1 est inclinée de 30° + φ sous le manche
  near(-G.heading(v["A3/1"].x2 - v["A3/1"].x1, v["A3/1"].y2 - v["A3/1"].y1), 30 + QCFG.b1_1.grader.value, 0.01);
  // le point de concours I est sur la verticale de C
  const I = c.corr.find((o) => o.k === "pt" && o.n === "I"), C = c.given.find((o) => o.k === "pt" && o.n === "C");
  near(I.x, C.x, 1e-6);
});

test("voiture en pente : normes, angle α et concours sous la route", () => {
  const c = PL.c1_2, v = vecs(c.corr), e = c.forces.choix[0];
  near(len(v["A0/1"]) * e, QCFG.c1_5.grader.value, 0.5, "‖A0/1‖");
  near(len(v["B0/1"]) * e, QCFG.c1_6.grader.value, 0.5, "‖B0/1‖");
  near(len(v.P) * e, 3000, 1e-6);
  const I = c.corr.find((o) => o.k === "pt" && o.n === "I"), Gp = c.given.find((o) => o.k === "pt" && o.n === "G");
  near(I.x, Gp.x, 1e-6, "I sur la verticale de G");
  const A = c.given.find((o) => o.k === "pt" && o.n === "A"), cone = c.corr.find((o) => o.k === "cone");
  const al = G.acute(G.line(A.x, A.y, I.x - A.x, I.y - A.y), G.line(0, 0, cone.ux, cone.uy));
  near(al, QCFG.c1_3.grader.value, 0.01, "α");
  assert.ok(al < cone.phi, "A0/1 dans le cône : l'équilibre est possible");
});

test("barbecue : pointe de la zone d'arc-boutement, inclinaison égale, normes", () => {
  const c = PL.g1_2, v = vecs(c.corr), e = c.forces.choix[0];
  const K = c.corr.find((o) => o.k === "pt" && o.n === "K"), A = c.given.find((o) => o.k === "pt" && o.n === "A");
  near((A.x - K.x) * c.kL, QCFG.g1_3.grader.value, 0.01, "distance minimale");
  near(len(v.A) * e, QCFG.g2_2.grader.value, 0.05); near(len(v.B) * e, QCFG.g2_2.grader.value, 0.05);
  const cones = c.corr.filter((o) => o.k === "cone");
  assert.equal(cones.length, 2);
  for (const k of cones) near(k.phi, QCFG.g1_1.grader.value, 0.01);
});

test("cours 2, montée de trottoir : quatre cas, dynamiques fermés, conclusions du manuel", () => {
  const c = PL["pl-trottoir"];
  assert.deepEqual(c.scenarios.map((s) => s.titre), ["a) Roues arrière motrices", "b) Hauteur limite",
    "c) Roues avant motrices", "d) Quatre roues motrices"]);
  const txt = (i) => c.scenarios[i].steps.map((s) => s.t).join(" ");
  assert.match(txt(0), /α &gt; φ/); assert.match(txt(0), /patinent en D/);
  assert.match(txt(2), /patinent en B/);
  assert.match(txt(3), /monte/);
  for (const i of [1, 3]) {
    const d = c.scenarios[i].steps.slice(-1)[0].o.filter((o) => o.k === "vec");
    assert.equal(d.length, 3);
    near(d[2].x2, d[0].x1, 1e-6); near(d[2].y2, d[0].y1, 1e-6);
    near(len(d[0]) * c.forces.choix[0], 1800, 1e-6, "P à l'échelle");
  }
});

test("atelier : feuille vierge et quatre fonds, sans correction", () => {
  const c = PL.atelier;
  assert.deepEqual(Object.keys(c.fonds), ["vierge", "cle", "pente", "barbecue", "trottoir"]);
  for (const f of Object.values(c.fonds)) assert.ok(!("corr" in f) && f.w > 0 && f.h > 0 && f.grille.length > 100);
  assert.ok(c.forces.choix.length > 3);
});
