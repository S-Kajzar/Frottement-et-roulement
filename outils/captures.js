// Images des cartes de l'accueil, photographiées dans les pages (Playwright + Chromium) :
// src/images/originaux/carte-*.png, recadrées ensuite en 480 × 270 par outils/preparer-images.sh.
//   python3 src/generer.py && NODE_PATH=$(npm root -g) node outils/captures.js && bash outils/preparer-images.sh && python3 src/generer.py
const path = require("node:path");
const { chromium } = require("playwright");
const racine = path.join(__dirname, "..");
const ORIG = path.join(racine, "src/images/originaux");
const URL = "file://" + path.join(racine, "index.html");
const FIGE = "*{animation:none!important;transition:none!important}";

// sur une planche : clic en coordonnées de feuille (mm)
async function clic(p, sel, x, y) {
  const c = await p.evaluate(([s, x, y]) => {
    const sv = document.querySelector(s + " svg.pl-svg"), pt = sv.createSVGPoint();
    pt.x = x; pt.y = y; const q = pt.matrixTransform(sv.getScreenCTM()); return [q.x, q.y];
  }, [sel, x, y]);
  await p.mouse.click(c[0], c[1]);
}
async function saisir(p, sel, ...v) {
  const ins = p.locator(sel + " .pl-ask input");
  for (let i = 0; i < v.length; i++) await ins.nth(i).fill(v[i]);
  await ins.nth(0).press("Enter");
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 1.5 });
  const shot = async (sel, nom) => { await p.addStyleTag({ content: FIGE }); await p.locator(sel).first().screenshot({ path: path.join(ORIG, nom + ".png") }); };

  // cours 1 : le colis poussé, en adhérence
  await p.goto(URL + "?ex=cours-frottement-analytique");
  await p.locator("#ca-F").evaluate((e) => { e.value = Math.round(e.max * 0.5); e.dispatchEvent(new Event("input")); });
  await shot("#ca-colis-svg", "carte-cours-1");
  // cours 2 : les cônes d'adhérence et de frottement ; atelier : la montée de trottoir, quatre roues motrices
  await p.goto(URL + "?ex=cours-frottement-graphique");
  await shot("#cg-cone .c-fig svg", "carte-cours-2");
  await p.click("#pl-trottoir [data-pl-scen='3']");
  await p.click("#pl-trottoir [data-pl-act=allsteps]");
  await shot("#pl-trottoir .pl-stage", "carte-atelier");
  await p.goto(URL + "?ex=cours-frottement-analytique");
  await shot("#ca-intro .ca-ex figure:first-child svg", "carte-etude");

  // activités : leur figure d'accueil, et la clé construite
  const heros = { "cones-adherence-frottement": "carte-a1", "voiture-route-mouillee": "carte-a5",
                  "resistance-roulement": "carte-a6", "barbecue-arc-boutement": "carte-a7" };
  for (const [ex, nom] of Object.entries(heros)) {
    await p.goto(URL + "?ex=" + ex);
    await shot("#home .home-hero svg", nom);
  }
  // voiture en pente : le haut de la figure (activité 4) ; la planche et sa correction superposée (activité 3)
  await p.goto(URL + "?ex=voiture-pente-variantes");
  const bb = await p.locator("#home .home-hero svg").boundingBox();
  await p.screenshot({ path: path.join(ORIG, "carte-a4.png"), clip: { x: bb.x, y: bb.y, width: bb.width, height: bb.height * 0.42 } });
  await p.goto(URL + "?ex=voiture-pente");
  await p.click("[data-mode=training]");
  await p.evaluate(() => { const q = Planche.all.c1_2; q.revealed = true; q.showCorr = true; q.draw(); });
  await p.addStyleTag({ content: FIGE });
  const st = await p.locator("#c1_2 .pl-stage").boundingBox();
  await p.locator("#c1_2 .pl-stage").scrollIntoViewIfNeeded();
  const st2 = await p.locator("#c1_2 .pl-stage").boundingBox();
  await p.screenshot({ path: path.join(ORIG, "carte-a3.png"), clip: { x: st2.x, y: st2.y, width: st2.width, height: st2.height * 0.62 } });
  await p.goto(URL + "?ex=cle-excentrique");
  await p.click("[data-mode=training]");
  const PL = "#b1_2", t = (o) => p.click(`${PL} [data-pl-tool=${o}]`);
  await p.locator(PL + " .pl-stage").scrollIntoViewIfNeeded();
  await t("par"); await clic(p, PL, 185, 28); await clic(p, PL, 185, 40);
  await t("cone"); await clic(p, PL, 57.93, 44); await clic(p, PL, 66.6, 49); await saisir(p, PL, "0,15");
  await t("dr"); await clic(p, PL, 75, 40); await clic(p, PL, 185, 145.2);
  await t("vec"); await clic(p, PL, 20, 92); await clic(p, PL, 20, 102); await saisir(p, PL, "F", "10");
  await t("par"); await clic(p, PL, 81.4, 62.7); await clic(p, PL, 20, 102);
  await t("par"); await clic(p, PL, 129.9, 92.5); await clic(p, PL, 20, 92);
  await t("vec"); await clic(p, PL, 20, 102); await clic(p, PL, 82.5, 151.8); await saisir(p, PL, "A3/1");
  await t("vec"); await clic(p, PL, 82.5, 151.8); await clic(p, PL, 20, 92); await saisir(p, PL, "B2/1");
  await p.mouse.move(5, 5);
  await shot(PL + " .pl-stage", "carte-a2");
  await b.close();
})();
