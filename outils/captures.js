// Images des cartes de l'accueil, photographiées dans les pages (Playwright + Chromium) :
// src/images/originaux/carte-*.png, recadrées ensuite en 480 × 270 par outils/preparer-images.sh.
//   python3 src/generer.py && NODE_PATH=$(npm root -g) node outils/captures.js && bash outils/preparer-images.sh && python3 src/generer.py
const path = require("node:path");
const { chromium } = require("playwright");
const racine = path.join(__dirname, "..");
const ORIG = path.join(racine, "src/images/originaux");
const URL = "file://" + path.join(racine, "index.html");
const FIGE = "*{animation:none!important;transition:none!important}";

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 1.5 });
  const shot = async (sel, nom) => { await p.addStyleTag({ content: FIGE }); await p.locator(sel).first().screenshot({ path: path.join(ORIG, nom + ".png") }); };

  // le cours : le colis poussé, en adhérence ; l'étude à venir : le frein de vélo
  await p.goto(URL + "?ex=cours-frottement-roulement");
  await p.locator("#ca-F").evaluate((e) => { e.value = Math.round(e.max * 0.5); e.dispatchEvent(new Event("input")); });
  await shot("#ca-colis-svg", "carte-cours");
  await shot("#ca-intro .ca-ex figure:first-child svg", "carte-etude");

  // les activités : la figure de leur page d'accueil
  const heros = { "cle-excentrique": "carte-cle", "voiture-pente": "carte-pente", "voiture-route-mouillee": "carte-route",
                  "resistance-roulement": "carte-roulement", "barbecue-arc-boutement": "carte-barbecue" };
  for (const [ex, nom] of Object.entries(heros)) {
    await p.goto(URL + "?ex=" + ex);
    await shot("#home .home-hero svg", nom);
  }
  // activité 3 (variantes) : la même voiture, cadrée sur la roue arrière et le centre de gravité
  await p.goto(URL + "?ex=voiture-pente-variantes");
  const bb = await p.locator("#home .home-hero svg").boundingBox();
  await p.screenshot({ path: path.join(ORIG, "carte-variantes.png"),
                       clip: { x: bb.x + bb.width * 0.3, y: bb.y, width: bb.width * 0.7, height: bb.height * 0.8 } });
  await b.close();
})();
