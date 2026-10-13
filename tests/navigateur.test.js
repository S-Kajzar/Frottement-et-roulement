// Tests navigateur (Playwright + Chromium) : accueil, cours, atelier, activités en entraînement et en examen,
// planche de construction manipulée à la souris comme le fait l'élève.
//   NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const { chromium } = require("playwright");
const REP = require("./reponses.js");

const FILE = path.join(__dirname, "..", "index.html");
const URL = "file://" + FILE;
let browser;

test.before(async () => { browser = await chromium.launch(); });
test.after(async () => { await browser.close(); });

async function open(q, viewport) {
  const context = await browser.newContext({ viewport: viewport || { width: 1366, height: 900 } });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("dialog", (d) => d.accept());
  await page.goto(URL + q);
  return { context, page, errors };
}
const text = (page, sel) => page.locator(sel).first().innerText();
const score = (page) => text(page, "#score-val");

// planche : clic en coordonnées de feuille (mm), saisie dans la petite fenêtre posée sur la feuille
async function clic(page, pl, x, y) {
  await page.locator(pl + " .pl-stage").scrollIntoViewIfNeeded();
  const c = await page.evaluate(([s, x, y]) => {
    const sv = document.querySelector(s + " svg.pl-svg"), pt = sv.createSVGPoint();
    pt.x = x; pt.y = y; const q = pt.matrixTransform(sv.getScreenCTM()); return [q.x, q.y];
  }, [pl, x, y]);
  await page.mouse.move(c[0], c[1]);
  await page.mouse.down(); await page.mouse.up();
}
async function saisir(page, pl, ...v) {
  const ins = page.locator(pl + " .pl-ask input");
  for (let i = 0; i < v.length; i++) await ins.nth(i).fill(v[i]);
  await ins.nth(0).press("Enter");
}
const outil = (page, pl, t) => page.click(`${pl} [data-pl-tool=${t}]`);
// questions à une case : saisie puis validation (entraînement) ou saisie seule (examen)
async function repondre(page, ids, valider = true) {
  for (const id of ids) {
    await page.fill(`#in-${id}`, REP[id]);
    if (valider) await page.click(`#${id} .btn-validate`);
  }
}
const idsDe = (page) => page.evaluate(() => Object.keys(window.__QCFG__));

// la construction complète de la clé à excentrique (activité 2), à la souris
async function construireCle(page) {
  const PL = "#b1_2";
  await page.locator(PL + " .pl-stage").scrollIntoViewIfNeeded();
  await outil(page, PL, "par"); await clic(page, PL, 185, 28); await clic(page, PL, 185, 40);
  await outil(page, PL, "cone"); await clic(page, PL, 57.93, 44); await clic(page, PL, 66.6, 49); await saisir(page, PL, "0,15");
  await outil(page, PL, "pt"); await clic(page, PL, 185, 145.2); await saisir(page, PL, "I");
  await outil(page, PL, "dr"); await clic(page, PL, 75, 40); await clic(page, PL, 185, 145.2);
  await outil(page, PL, "vec"); await clic(page, PL, 20, 92); await clic(page, PL, 20, 102); await saisir(page, PL, "F", "10");
  await outil(page, PL, "par"); await clic(page, PL, 81.4, 62.7); await clic(page, PL, 20, 102);
  await outil(page, PL, "par"); await clic(page, PL, 129.9, 92.5); await clic(page, PL, 20, 92);
  await outil(page, PL, "vec"); await clic(page, PL, 20, 102); await clic(page, PL, 82.5, 151.8); await saisir(page, PL, "A3/1");
  await outil(page, PL, "vec"); await clic(page, PL, 82.5, 151.8); await clic(page, PL, 20, 92); await saisir(page, PL, "B2/1");
}

test("accueil : cartes illustrées à mots-clés (deux cours, atelier, sept activités, études de cas)", async () => {
  const { context, page, errors } = await open("");
  assert.ok(await page.locator("body.hub").count());
  assert.ok(!(await page.isVisible("main.page")));
  assert.match(await text(page, "#home h1"), /Frottement et roulement/);
  assert.deepEqual(await page.locator("#home h2").allInnerTexts(), ["Les cours", "L'atelier graphique", "Les activités", "Études de cas"]);
  const card = (sel) => page.locator(sel).evaluateAll((cs) => cs.map((c) => [
    c.querySelector(".mc-tag").textContent.trim(), c.querySelector("h3").textContent,
    c.querySelector("a") ? c.querySelector("a").getAttribute("href") : null]));
  assert.deepEqual(await card(".cours-grid .mode-card"), [
    ["Cours 1 Analytique", "Frottement et roulement : approche analytique", "?ex=cours-frottement-analytique"],
    ["Cours 2 Graphique", "Frottement : résolution graphique", "?ex=cours-frottement-graphique"]]);
  assert.deepEqual(await card(".atelier-grid .mode-card"), [["Atelier", "Planche de construction graphique", "?ex=atelier-graphique"]]);
  assert.deepEqual((await card(".exo-grid .mode-card")).map((c) => c[0]), ["Activité 1 Graphique", "Activité 2 Graphique",
    "Activité 3 Graphique", "Activité 4 Analytique", "Activité 5 Analytique", "Activité 6 Analytique", "Activité 7 Graphique"]);
  const cartes = await page.locator("#home .carte-v").evaluateAll((cs) => cs.map((c) => ({
    img: c.querySelector("img.cv-img") ? c.querySelector("img.cv-img").naturalWidth : -1,
    mots: c.querySelectorAll(".cv-mots li").length, w: Math.round(c.offsetWidth), h: c.offsetHeight })));
  assert.equal(cartes.length, 11);
  for (const c of cartes) {
    assert.ok(c.img > 0 && c.mots >= 3 && c.mots <= 5, JSON.stringify(c));
    assert.equal(c.w, cartes[0].w); assert.ok(Math.abs(c.h - cartes[0].h) <= 1);
  }
  assert.match(await text(page, ".etude-grid .etat"), /En cours d'édition/);
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  const src = fs.readFileSync(FILE, "utf8").replace(/data:[^"]+/g, "");
  assert.doesNotMatch(src, /\b(BTS|STI2D|bac(calaur[ée]at)?|session \d|[ée]preuve|acad[ée]mie|brevet)\b/i);
  assert.deepEqual(errors, []);
  await context.close();
});

test("adresse inconnue : retour à l'accueil", async () => {
  const { context, page, errors } = await open("?ex=nimporte-quoi");
  assert.ok(await page.locator("body.hub").count());
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1 : le colis (repos, adhérence, glissement), l'automobile au ralenti, le quiz", async () => {
  const { context, page, errors } = await open("?ex=cours-frottement-analytique");
  assert.match(await text(page, "#home h1"), /approche analytique/);
  assert.equal(await page.locator(".cours-sec").count(), 7);
  const F = (v) => page.locator("#ca-F").evaluate((e, v) => { e.value = v; e.dispatchEvent(new Event("input")); }, v);
  assert.match(await text(page, "#ca-etat"), /Repos/);
  await F(100); // 20 kg, pneu sur route sèche : seuil 0,8 × 196,2 = 157 N
  assert.match(await text(page, "#ca-etat"), /Adhérence/);
  assert.equal(await text(page, "#ca-T"), "100,0 N");
  await F(170);
  assert.match(await text(page, "#ca-etat"), /Glissement/);
  assert.equal(await text(page, "#ca-T"), "117,7 N", "en glissement, T = µ·N = 0,6 × 196,2");
  await F(140); // entre µN et µsN : le colis lancé continue de glisser
  assert.match(await text(page, "#ca-etat"), /Glissement/);
  await page.click("#ca-stop");
  assert.match(await text(page, "#ca-etat"), /Repos/);
  // exemple 1 du manuel : 1 100 kg, pneus noirs, 90 km/h
  assert.equal(await text(page, "#ca-rF"), "12,95 daN");
  assert.equal(await text(page, "#ca-rP"), "3,24 kW");
  assert.equal(await text(page, "#ca-ra"), "3,48 mm");
  await page.selectOption("#ca-rp", "0.0085");
  assert.equal(await text(page, "#ca-rF"), "9,17 daN");
  // quiz : toutes les bonnes réponses
  for (const fs_ of await page.locator("#ca-quiz .quiz-q").all()) {
    const ok = await fs_.getAttribute("data-ok");
    await fs_.locator(`input[value="${ok}"]`).check();
  }
  assert.equal(await text(page, "#ca-quiz .qz-score"), "8 / 8");
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 2 : cône manipulable, jeu, démonstration du trottoir pas à pas, construction libre", async () => {
  const { context, page, errors } = await open("?ex=cours-frottement-graphique");
  assert.match(await text(page, "#cg-etat"), /Dans le cône/);
  await page.locator("#cg-cone-svg").focus();
  for (let i = 0; i < 40; i++) await page.keyboard.press("ArrowRight");
  assert.match(await text(page, "#cg-etat"), /Hors du cône/);
  for (const l of await page.locator("#cg-jeu .jeu-l").all()) await l.locator(`button[data-v="${await l.getAttribute("data-ok")}"]`).click();
  assert.equal(await text(page, "#cg-jeu .jeu-s"), "6 / 6");
  const PL = "#pl-trottoir";
  assert.match(await text(page, PL + " .pl-etape-n"), /Étape 0 \/ 4/);
  for (let i = 0; i < 4; i++) await page.click(`${PL} [data-pl-act=next]`);
  assert.match(await text(page, PL + " .pl-etape-t"), /α = 46,1°/);
  assert.ok(await page.locator(`${PL} [data-pl-act=next]`).isDisabled());
  await page.click(`${PL} [data-pl-scen="1"]`);
  await page.click(`${PL} [data-pl-act=allsteps]`);
  assert.match(await text(page, PL + " .pl-etape-t"), /Dynamique/);
  const demo = await page.locator(`${PL} svg .pl-demo > g`).count();
  assert.ok(demo > 5, "la démonstration est tracée");
  assert.ok(!(await page.isVisible(`${PL} .pl-bar`)));
  await page.click(`${PL} [data-pl-act=essai]`);
  assert.ok(await page.isVisible(`${PL} .pl-bar`));
  assert.equal(await page.locator(`${PL} svg .pl-demo > g`).count(), 0, "la démonstration s'efface");
  await outil(page, PL, "dr"); await clic(page, PL, 40, 139.2); await clic(page, PL, 133.3, 150);
  assert.equal(await page.locator(`${PL} svg .pl-usr > g`).count(), 1);
  for (const fs_ of await page.locator("#cg-quiz .quiz-q").all()) await fs_.locator(`input[value="${await fs_.getAttribute("data-ok")}"]`).check();
  assert.equal(await text(page, "#cg-quiz .qz-score"), "8 / 8");
  assert.deepEqual(errors, []);
  await context.close();
});

test("atelier : fonds au choix, outils, annuler, relevés, document réponse à l'échelle", async () => {
  const { context, page, errors } = await open("?ex=atelier-graphique");
  const PL = "#atelier";
  assert.equal(await page.locator(`${PL} svg .pl-given > g`).count(), 0);
  await page.selectOption(`${PL} .pl-fond`, "pente");
  assert.ok(await page.locator(`${PL} svg .pl-given > g`).count() >= 5, "les éléments donnés du fond");
  assert.match(await text(page, `${PL} .pl-ech`), /1:50/);
  await page.selectOption(`${PL} .pl-scale`, "20");
  await outil(page, PL, "vec"); await clic(page, PL, 150, 20); await clic(page, PL, 150, 70); await saisir(page, PL, "P");
  assert.match(await text(page, `${PL} .pl-releves tbody`), /Vecteur P\s+50,0 mm\s+1\s000 daN/);
  await outil(page, PL, "dist"); await clic(page, PL, 150, 20); await clic(page, PL, 150, 70);
  assert.match(await text(page, `${PL} .pl-releves tbody`), /2\s500 mm réels/);
  await page.click(`${PL} [data-pl-act=undo]`);
  assert.equal(await page.locator(`${PL} svg .pl-usr > g`).count(), 1);
  await page.click(`${PL} [data-pl-act=redo]`);
  assert.equal(await page.locator(`${PL} svg .pl-usr > g`).count(), 2);
  await outil(page, PL, "gom"); await clic(page, PL, 150, 45);
  assert.equal(await page.locator(`${PL} svg .pl-usr > g`).count(), 1);
  const [popup] = await Promise.all([page.waitForEvent("popup"), page.click(`${PL} [data-pl-act=print]`)]);
  await popup.waitForLoadState();
  const svg = popup.locator("svg.pl-svg");
  assert.equal(await svg.getAttribute("width"), "215mm", "la feuille garde ses dimensions en millimètres");
  assert.equal(await popup.locator("svg .pl-usr > g").count(), 0, "document réponse vierge");
  assert.deepEqual(errors, []);
  await context.close();
});

test("activité 2 en entraînement : construction à la souris, lectures, correction superposée, 20/20", async () => {
  const { context, page, errors } = await open("?ex=cle-excentrique");
  await page.click("[data-mode=training]");
  await construireCle(page);
  const rel = await text(page, "#b1_2 .pl-releves tbody");
  assert.match(rel, /A3\/1\s+79,9 mm\s+79,9 daN/); assert.match(rel, /B2\/1\s+86,5 mm\s+86,5 daN/);
  await page.click("#b1_2 .pl-valider");
  assert.ok(await page.locator("#b1_2.locked").count());
  assert.match(await text(page, "#b1_2 .pl-wait"), /après validation de : Q1\.1/);
  assert.ok(!(await page.isVisible("#b1_2 .selfeval")));
  await repondre(page, await idsDe(page));
  assert.ok(await page.isVisible("#b1_2 .selfeval"), "toutes les lectures validées : correction et auto-évaluation");
  assert.ok(await page.locator("#b1_2 .pl-corr-toggle input").isChecked());
  assert.ok(await page.locator("#b1_2 svg .pl-corr > g").count() > 8, "correction superposée");
  for (const cb of await page.locator("#b1_2 .selfeval input[data-crit]").all()) await cb.check();
  await page.click("#b1_2 .btn-self");
  assert.equal(await score(page), "20,0/20");
  assert.match(await text(page, "#recap-body"), /Partie 1/);
  assert.deepEqual(errors, []);
  await context.close();
});

test("activité 7 en examen : rien avant la remise, puis planche verrouillée et corrigée", async () => {
  const { context, page, errors } = await open("?ex=barbecue-arc-boutement");
  await page.click("[data-mode=exam]");
  assert.ok(!(await page.isVisible("#g1_2 .pl-valider")), "pas de validation pendant l'examen");
  const PL = "#g1_2";
  await page.locator(PL + " .pl-stage").scrollIntoViewIfNeeded();
  await outil(page, PL, "cone"); await clic(page, PL, 175, 62); await clic(page, PL, 160, 62); await saisir(page, PL, "0,08");
  assert.equal(await page.locator(`${PL} svg .pl-usr > g`).count(), 1);
  await repondre(page, await idsDe(page), false);
  assert.equal(await page.locator(`${PL} svg .pl-corr > g`).count(), 0, "aucune correction avant la remise");
  await page.click("#exam-submit"); await page.click("#exam-submit");
  assert.ok(await page.locator(`${PL}.locked.revealed`).count());
  assert.ok(await page.locator(`${PL} svg .pl-corr > g`).count() > 5);
  assert.ok(await page.isVisible(`${PL} .selfeval`));
  const crit = page.locator(`${PL} .selfeval input[data-crit]`);
  await crit.nth(0).check(); await crit.nth(2).check();
  await page.click(`${PL} .btn-self`);
  // partie 1 : 3 questions justes + 2 critères sur 5 = 5 / 8 ; partie 2 : 3 / 3 ; pondération 25 et 15 min
  assert.equal(await text(page, ".recap-table .final-note"), `${(Math.round((5 / 8 * 20 * 25 + 20 * 15) / 40 * 10) / 10).toLocaleString("fr-FR", { minimumFractionDigits: 1 })}/20`);
  assert.deepEqual(errors, []);
  await context.close();
});

test("activité 1 (QCM) : propositions, marques, 20/20", async () => {
  const { context, page, errors } = await open("?ex=cones-adherence-frottement");
  await page.click("[data-mode=training]");
  await page.click("#a1_1 .qcm-o[data-k='1']"); await page.click("#a1_1 .qcm-o[data-k='2']");
  await page.click("#a1_1 .btn-fast");
  await page.click("#a1_2 .qcm-o[data-k='2']"); await page.click("#a1_2 .btn-fast");
  assert.equal(await page.locator(".qcm-o.ok").count(), 3);
  assert.equal(await score(page), "20,0/20");
  assert.deepEqual(errors, []);
  await context.close();
});

for (const ex of ["voiture-pente-variantes", "voiture-route-mouillee", "resistance-roulement"]) {
  test(`activité analytique ${ex} : toutes les réponses de référence donnent 20/20`, async () => {
    const { context, page, errors } = await open("?ex=" + ex);
    await page.click("[data-mode=training]");
    await repondre(page, await idsDe(page));
    assert.equal(await score(page), "20,0/20");
    assert.equal(await page.locator(".q.is-ok").count(), (await idsDe(page)).length);
    assert.deepEqual(errors, []);
    await context.close();
  });
}

test("téléphone : l'activité graphique tient dans l'écran, sans défilement horizontal", async () => {
  const { context, page, errors } = await open("?ex=voiture-pente", { width: 390, height: 844 });
  await page.click("[data-mode=training]");
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  const w = await page.locator("#c1_2 .pl-stage").evaluate((e) => e.getBoundingClientRect().width);
  assert.ok(w <= 390 && w > 250);
  assert.deepEqual(errors, []);
  await context.close();
});
