// Tests navigateur (Playwright + Chromium) : accueil, cours, activités en entraînement et en examen, téléphone.
//   NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const { chromium } = require("playwright");
const REP = require("./reponses.js");

const FILE = path.join(__dirname, "..", "index.html");
const URL = "file://" + FILE;
const ACTIVITES = ["cle-excentrique", "voiture-pente", "voiture-pente-variantes", "voiture-route-mouillee",
                   "resistance-roulement", "barbecue-arc-boutement"];
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
const idsDe = (page) => page.evaluate(() => Object.keys(window.__QCFG__));
async function repondre(page, ids, valider = true) {
  for (const id of ids) {
    await page.fill(`#in-${id}`, REP[id]);
    if (valider) await page.click(`#${id} .btn-validate`);
  }
}

test("accueil : cartes illustrées à mots-clés (le cours, six activités, études de cas)", async () => {
  const { context, page, errors } = await open("");
  assert.ok(await page.locator("body.hub").count());
  assert.ok(!(await page.isVisible("main.page")));
  assert.match(await text(page, "#home h1"), /Frottement et roulement/);
  assert.deepEqual(await page.locator("#home h2").allInnerTexts(), ["Le cours", "Les activités", "Études de cas"]);
  const card = (sel) => page.locator(sel).evaluateAll((cs) => cs.map((c) => [
    c.querySelector(".mc-tag").textContent.trim(), c.querySelector("h3").textContent,
    c.querySelector("a") ? c.querySelector("a").getAttribute("href") : null]));
  assert.deepEqual(await card(".cours-grid .mode-card"), [["Cours", "Frottement et roulement", "?ex=cours-frottement-roulement"]]);
  assert.deepEqual((await card(".exo-grid .mode-card")).map((c) => c[2]), ACTIVITES.map((a) => "?ex=" + a));
  assert.deepEqual((await card(".exo-grid .mode-card")).map((c) => c[0]), [1, 2, 3, 4, 5, 6].map((n) => "Activité " + n));
  const cartes = await page.locator("#home .carte-v").evaluateAll((cs) => cs.map((c) => ({
    img: c.querySelector("img.cv-img") ? c.querySelector("img.cv-img").naturalWidth : -1,
    mots: c.querySelectorAll(".cv-mots li").length, w: Math.round(c.offsetWidth), h: c.offsetHeight })));
  assert.equal(cartes.length, 8);
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

test("adresse inconnue (ou ancienne page graphique) : retour à l'accueil", async () => {
  for (const q of ["?ex=nimporte-quoi", "?ex=cours-frottement-graphique", "?ex=atelier-graphique"]) {
    const { context, page, errors } = await open(q);
    assert.ok(await page.locator("body.hub").count(), q);
    assert.deepEqual(errors, []);
    await context.close();
  }
});

test("cours : le colis (repos, adhérence, glissement), l'automobile au ralenti, le texte en pleine largeur, le quiz", async () => {
  const { context, page, errors } = await open("?ex=cours-frottement-roulement");
  assert.match(await text(page, "#home h1"), /Frottement et roulement/);
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
  // le texte occupe toute la largeur des sections
  const larg = await page.locator("#ca-adh .part-body > p").first().evaluate((e) =>
    e.getBoundingClientRect().width / e.closest(".part").getBoundingClientRect().width);
  assert.ok(larg > 0.9, String(larg));
  for (const fs_ of await page.locator("#ca-quiz .quiz-q").all()) {
    await fs_.locator(`input[value="${await fs_.getAttribute("data-ok")}"]`).check();
  }
  assert.equal(await text(page, "#ca-quiz .qz-score"), "8 / 8");
  assert.deepEqual(errors, []);
  await context.close();
});

for (const ex of ACTIVITES) {
  test(`activité ${ex} en entraînement : les réponses de référence donnent 20/20`, async () => {
    const { context, page, errors } = await open("?ex=" + ex);
    await page.click("[data-mode=training]");
    const ids = await idsDe(page);
    await repondre(page, ids);
    assert.equal(await text(page, "#score-val"), "20,0/20");
    assert.equal(await page.locator(".q.is-ok").count(), ids.length);
    assert.equal(await page.locator(".q-expl:visible").count(), ids.length, "chaque démarche corrigée s'affiche");
    assert.deepEqual(errors, []);
    await context.close();
  });
}

test("activité 6 en examen : rien avant la remise, puis note pondérée", async () => {
  const { context, page, errors } = await open("?ex=barbecue-arc-boutement");
  await page.click("[data-mode=exam]");
  const ids = await idsDe(page);
  await repondre(page, ids.slice(0, 4), false);   // partie 1 complète, partie 2 vide
  assert.equal(await page.locator(".q-expl:visible").count(), 0, "aucune correction avant la remise");
  await page.click("#exam-submit"); await page.click("#exam-submit");
  assert.equal(await page.locator(".q.is-ok").count(), 4);
  // partie 1 : 20/20 sur 25 min ; partie 2 : 0/20 sur 15 min
  assert.equal(await text(page, ".recap-table .final-note"), "12,5/20");
  assert.deepEqual(errors, []);
  await context.close();
});

test("téléphone : une activité tient dans l'écran, sans défilement horizontal", async () => {
  const { context, page, errors } = await open("?ex=voiture-pente", { width: 390, height: 844 });
  await page.click("[data-mode=training]");
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  assert.deepEqual(errors, []);
  await context.close();
});
