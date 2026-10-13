/* =====================================================================
   PLANCHE DE CONSTRUCTION GRAPHIQUE (statique graphique)
   Une feuille cotée en millimètres (le document réponse imprimé à 100 % a
   les mêmes dimensions), un fond (le mécanisme dessiné à l'échelle), des
   éléments donnés (points, directions, forces connues) et les outils du
   tracé à la règle et au rapporteur : point, droite, segment, parallèle,
   perpendiculaire, droite inclinée d'un angle donné, cône de frottement,
   vecteur à l'échelle des forces, mesure de distance et d'angle, texte.
   Les points s'aimantent aux points, aux intersections et aux droites.
   Trois usages :
     - exercice : la planche compte comme un tracé du gabarit (auto-évalué
       par critères), sa correction se superpose une fois les questions qui
       en dépendent validées (ou la copie remise en mode examen) ;
     - démonstration (cours) : la construction se déroule pas à pas ;
     - atelier : feuille libre, fonds au choix.
   Configuration : window.__PLANCHES__[id], écrite par src/generer.py.
   Repère de la feuille : x vers la droite, y vers le bas (SVG), en mm ;
   les angles affichés suivent le sens trigonométrique de l'écran.
   ===================================================================== */
/*GEOM-START*/
var Geom = (function () {
  "use strict";
  var EPS = 1e-9;
  function len(x, y) { return Math.sqrt(x * x + y * y); }
  function unit(x, y) { var l = len(x, y); return l < EPS ? null : { x: x / l, y: y / l }; }
  // droite : point (x, y) et direction unitaire (ux, uy)
  function line(x, y, ux, uy) { var u = unit(ux, uy); return u ? { x: x, y: y, ux: u.x, uy: u.y } : null; }
  function through(p, q) { return line(p.x, p.y, q.x - p.x, q.y - p.y); }
  // rotation d'un angle (degrés) dans le sens trigonométrique de l'écran (y vers le bas)
  function rotScreen(u, deg) {
    var a = deg * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
    return { x: u.x * c + u.y * s, y: -u.x * s + u.y * c };
  }
  function parallel(L, p) { return line(p.x, p.y, L.ux, L.uy); }
  function perpendicular(L, p) { return line(p.x, p.y, -L.uy, L.ux); }
  function inclined(L, p, deg) { var u = rotScreen({ x: L.ux, y: L.uy }, deg); return line(p.x, p.y, u.x, u.y); }
  // intersection de deux droites (null si parallèles) ; t1, t2 : abscisses sur chacune
  function intersect(L1, L2) {
    var d = L1.ux * L2.uy - L1.uy * L2.ux;
    if (Math.abs(d) < 1e-7) return null;
    var dx = L2.x - L1.x, dy = L2.y - L1.y;
    var t1 = (dx * L2.uy - dy * L2.ux) / d, t2 = (dx * L1.uy - dy * L1.ux) / d;
    return { x: L1.x + t1 * L1.ux, y: L1.y + t1 * L1.uy, t1: t1, t2: t2 };
  }
  function project(p, L) {
    var t = (p.x - L.x) * L.ux + (p.y - L.y) * L.uy;
    return { x: L.x + t * L.ux, y: L.y + t * L.uy, t: t };
  }
  function distLine(p, L) { return Math.abs((p.x - L.x) * L.uy - (p.y - L.y) * L.ux); }
  function distSeg(p, a, b) {
    var dx = b.x - a.x, dy = b.y - a.y, L2 = dx * dx + dy * dy;
    var t = L2 ? ((p.x - a.x) * dx + (p.y - a.y) * dy) / L2 : 0;
    t = Math.max(0, Math.min(1, t));
    return len(p.x - a.x - t * dx, p.y - a.y - t * dy);
  }
  // angle aigu entre deux droites, en degrés (0 à 90)
  function acute(L1, L2) {
    var c = Math.abs(L1.ux * L2.ux + L1.uy * L2.uy);
    return Math.acos(Math.min(1, c)) * 180 / Math.PI;
  }
  // direction d'un vecteur par rapport à l'horizontale, sens trigonométrique de l'écran (-180 à 180)
  function heading(x, y) { return Math.atan2(-y, x) * 180 / Math.PI; }
  // portion d'une droite visible dans le rectangle [0, w] × [0, h]
  function clip(L, w, h) {
    var t0 = -Infinity, t1 = Infinity;
    function slab(p, u, lo, hi) {
      if (Math.abs(u) < EPS) return p >= lo - EPS && p <= hi + EPS;
      var a = (lo - p) / u, b = (hi - p) / u;
      if (a > b) { var c = a; a = b; b = c; }
      t0 = Math.max(t0, a); t1 = Math.min(t1, b);
      return t0 <= t1;
    }
    if (!slab(L.x, L.ux, 0, w) || !slab(L.y, L.uy, 0, h)) return null;
    return [{ x: L.x + t0 * L.ux, y: L.y + t0 * L.uy }, { x: L.x + t1 * L.ux, y: L.y + t1 * L.uy }];
  }
  // saisie française : « 0,15 », « 8,5° », « 1 200 »
  function parseNum(s) {
    var t = String(s == null ? "" : s).replace(/[  \s]/g, "").replace(",", ".").replace(/[−–]/g, "-");
    var m = t.match(/^[-+]?(\d+(\.\d*)?|\.\d+)/);
    return m ? parseFloat(m[0]) : null;
  }
  // coefficient de frottement ou angle : « 0,15 » → f ; « 8,5° » ou « 8,5 » (> 1,5) → degrés
  function parsePhi(s) {
    var v = parseNum(s);
    if (v === null || v <= 0) return null;
    var deg = /°|deg/i.test(String(s)) || v > 1.5;
    if (deg) return v < 90 ? v : null;
    return Math.atan(v) * 180 / Math.PI;
  }
  return { len: len, unit: unit, line: line, through: through, rotScreen: rotScreen, parallel: parallel,
           perpendicular: perpendicular, inclined: inclined, intersect: intersect, project: project,
           distLine: distLine, distSeg: distSeg, acute: acute, heading: heading, clip: clip,
           parseNum: parseNum, parsePhi: parsePhi };
})();
if (typeof module !== "undefined") module.exports = Geom;
/*GEOM-END*/

var Planche = (function () {
  "use strict";
  var G = Geom;
  var CFG = window.__PLANCHES__ || {};
  var all = {};
  var COULEURS = [["#1F5FA8", "bleue"], ["#1B7A43", "verte"], ["#1C2530", "noire"]];
  var LETTRES = "IJKMNHLQRSTUVWXYZ";
  var OUTILS = {
    pt: ["Point", ["Clique pour placer un point : il s'aimante aux points, aux intersections et aux droites."]],
    dr: ["Droite", ["Clique un premier point de la droite.", "Clique un second point de la droite."]],
    sg: ["Segment", ["Clique la première extrémité.", "Clique la seconde extrémité."]],
    par: ["Parallèle", ["Clique la droite (ou le vecteur) de référence.", "Clique le point par lequel passe la parallèle."]],
    perp: ["Perpendiculaire", ["Clique la droite (ou le vecteur) de référence.", "Clique le point par lequel passe la perpendiculaire."]],
    inc: ["Inclinée", ["Clique la direction de référence (une zone vide : l'horizontale).", "Clique le point par lequel passe la droite.", "Indique l'angle en degrés (positif dans le sens trigonométrique)."]],
    cone: ["Cône", ["Clique le point de contact (sommet du cône).", "Clique la normale au contact.", "Indique le coefficient f (ex. 0,15) ou le demi-angle φ (ex. 8,5°)."]],
    vec: ["Vecteur", ["Clique l'origine du vecteur.", "Clique son extrémité : sa norme s'affiche à l'échelle des forces."]],
    dist: ["Distance", ["Clique le premier point.", "Clique le second point."]],
    ang: ["Angle", ["Clique la première droite (ou le vecteur).", "Clique la seconde droite."]],
    tx: ["Texte", ["Clique où placer le texte."]],
    gom: ["Gomme", ["Clique un élément de ta construction pour l'effacer (les éléments donnés restent)."]],
    main: ["Main", ["Fais glisser la feuille pour te déplacer quand elle est agrandie."]]
  };
  var ZOOMS = [1, 1.5, 2, 3, 4];

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function fr(x, d) {
    return x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d }).replace(/^-/, "−");
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function n2(v) { return Math.round(v * 100) / 100; }

  // ---------- rendu SVG ----------
  // nom d'un vecteur ou d'un point : « A0/1 » → A et l'indice 0/1 ; « F_air » → F et l'indice air
  function nom(n, x, y, size, vecteur, cls) {
    var m = String(n).match(/^([A-Za-zÀ-ÿͰ-Ͽ']+?)(?:_?([0-9].*|_.+))?$/) || [null, n, ""];
    var base = m[1], sub = (m[2] || "").replace(/^_/, "");
    var w = size * (0.62 * base.length + (sub ? 0.5 * sub.length + 0.1 : 0));
    var s = '<text class="pl-nom ' + (cls || "") + '" x="' + n2(x) + '" y="' + n2(y) + '" font-size="' + size + '">' +
      '<tspan font-style="italic">' + esc(base) + "</tspan>" +
      (sub ? '<tspan font-size="' + n2(size * 0.68) + '" dy="' + n2(size * 0.3) + '">' + esc(sub) + "</tspan>" : "") + "</text>";
    if (vecteur) {
      var ya = y - size * 0.92, x2 = x + Math.max(size * 0.75, w * (sub ? 0.72 : 1));
      s += '<path class="pl-fl ' + (cls || "") + '" d="M' + n2(x) + " " + n2(ya) + "H" + n2(x2) + "m-" + n2(size * 0.32) + " -" +
        n2(size * 0.17) + "l" + n2(size * 0.32) + " " + n2(size * 0.17) + "l-" + n2(size * 0.32) + " " + n2(size * 0.17) + '"/>';
    }
    return s;
  }
  function fleche(x1, y1, x2, y2, head) {
    var u = G.unit(x2 - x1, y2 - y1);
    if (!u) return "";
    var L = G.len(x2 - x1, y2 - y1), h = Math.min(head, L * 0.5), b = h * 0.38;
    var bx = x2 - u.x * h, by = y2 - u.y * h;
    return '<path class="pl-ft" d="M' + n2(x1) + " " + n2(y1) + "L" + n2(bx) + " " + n2(by) + '"/>' +
      '<path class="pl-tete" d="M' + n2(x2) + " " + n2(y2) + "L" + n2(bx - u.y * b) + " " + n2(by + u.x * b) + "L" +
      n2(bx + u.y * b) + " " + n2(by - u.x * b) + 'Z"/>';
  }

  // ---------- la planche ----------
  function Pl(root, cfg, opts) {
    var self = this;
    this.root = root; this.id = root.getAttribute("data-planche"); this.cfg = cfg; this.opts = opts || {};
    this.W = cfg.w; this.H = cfg.h; this.kL = cfg.kL || 1;
    this.svg = $("svg.pl-svg", root);
    this.stage = $(".pl-stage", root);
    this.L = {}; ["grille", "given", "demo", "usr", "corr", "prev", "snap"].forEach(function (k) { self.L[k] = $(".pl-svg .pl-" + k, root); });
    this.objs = []; this.hist = []; this.redo = []; this.tool = cfg.outil || "dr"; this.stepN = 0; this.pend = [];
    this.color = COULEURS[0][0]; this.zoom = 1; this.locked = false; this.revealed = false; this.showCorr = false;
    this.scale = cfg.forces ? cfg.forces.choix[cfg.forces.def || 0] : null;
    this.given = (cfg.given || []).map(function (o) { return self.prep(o); });
    this.corr = (cfg.corr || []).map(function (o) { return self.prep(o); });
    this.scen = 0; this.step = cfg.scenarios ? cfg.scenarios[0].steps.length : 0;
    this.selfDone = false;

    $$("[data-pl-tool]", root).forEach(function (b) {
      b.addEventListener("click", function () { self.setTool(b.getAttribute("data-pl-tool")); });
    });
    $$("[data-pl-color]", root).forEach(function (b) {
      b.addEventListener("click", function () {
        self.color = b.getAttribute("data-pl-color");
        $$("[data-pl-color]", root).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      });
    });
    var sc = $(".pl-scale", root);
    if (sc) sc.addEventListener("change", function () { self.scale = +sc.value; self.draw(); });
    $$("[data-pl-zoom]", root).forEach(function (b) { b.addEventListener("click", function () { self.setZoom(b.getAttribute("data-pl-zoom")); }); });
    this.act("undo", function () { self.undo(); });
    this.act("redo", function () { self.redoOne(); });
    var clr = $("[data-pl-act=clear]", root), clrT;
    if (clr) clr.addEventListener("click", function () {
      if (self.locked) return;
      if (clr.dataset.armed) {
        self.commit(function () { self.objs = []; });
        delete clr.dataset.armed; clr.textContent = "Tout effacer"; clearTimeout(clrT); return;
      }
      clr.dataset.armed = "1"; clr.textContent = "Confirmer l'effacement";
      clrT = setTimeout(function () { delete clr.dataset.armed; clr.textContent = "Tout effacer"; }, 3000);
    });
    this.act("full", function () { self.toggleFull(); });
    this.act("print", function () { self.printDR(); });
    var tg = $(".pl-corr-toggle input", root);
    if (tg) tg.addEventListener("change", function () { self.showCorr = tg.checked; self.draw(); });
    var bv = $(".pl-valider", root);
    if (bv) bv.addEventListener("click", function () { if (!self.opts.app || self.opts.app.mode() === "training") self.validate(); });
    var bs = $(".btn-self", root);
    if (bs) bs.addEventListener("click", function () { self.selfAssess(); });
    $$(".selfeval input[data-crit]", root).forEach(function (cb) { cb.addEventListener("change", function () { self.refreshSelf(); }); });
    // démonstration pas à pas
    $$("[data-pl-scen]", root).forEach(function (b) {
      b.addEventListener("click", function () { self.setScen(+b.getAttribute("data-pl-scen")); });
    });
    this.act("prev", function () { self.setStep(self.step - 1); });
    this.act("next", function () { self.setStep(self.step + 1); });
    this.act("allsteps", function () { self.setStep(Infinity); });
    this.act("essai", function () { self.toggleEssai(); });
    // atelier : choix du fond
    var fd = $(".pl-fond", root);
    if (fd) fd.addEventListener("change", function () { self.setFond(fd.value); });

    var sv = this.svg;
    sv.addEventListener("pointerdown", function (e) { self.down(e); });
    sv.addEventListener("pointermove", function (e) { self.move(e); });
    sv.addEventListener("pointerup", function (e) { self.up(e); });
    sv.addEventListener("pointerleave", function () { self.hover = null; self.drawPrev(); });
    root.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && (self.pend.length || $(".pl-ask", root))) { e.stopPropagation(); self.cancel(); }
    });
    this.setTool(this.tool);
    if (cfg.scenarios) this.setScen(0); else this.draw();
  }
  Pl.prototype.act = function (k, fn) { var b = $("[data-pl-act=" + k + "]", this.root); if (b) b.addEventListener("click", fn); };

  // éléments donnés ou corrigés : les droites sont normalisées une fois pour toutes
  Pl.prototype.prep = function (o) {
    o = JSON.parse(JSON.stringify(o));
    if (o.k === "dr" || o.k === "cone") { var u = G.unit(o.ux, o.uy); o.ux = u.x; o.uy = u.y; }
    return o;
  };
  // droites portées par un élément : [{L, a, b}] (a, b : bornes pour un segment ou un vecteur)
  Pl.prototype.lignes = function (o) {
    if (o.k === "dr") return [{ L: G.line(o.x, o.y, o.ux, o.uy) }];
    if (o.k === "sg" || o.k === "vec") {
      var L = G.through({ x: o.x1, y: o.y1 }, { x: o.x2, y: o.y2 });
      return L ? [{ L: L, a: { x: o.x1, y: o.y1 }, b: { x: o.x2, y: o.y2 } }] : [];
    }
    if (o.k === "cone") {
      var n = { x: o.ux, y: o.uy }, e1 = G.rotScreen(n, o.phi), e2 = G.rotScreen(n, -o.phi);
      return [{ L: G.line(o.x, o.y, e1.x, e1.y) }, { L: G.line(o.x, o.y, e2.x, e2.y) }];
    }
    return [];
  };
  Pl.prototype.visibles = function () {
    var v = this.given.concat(this.demoObjs || []);
    if (!this.essai || !this.cfg.scenarios) v = v.concat(this.objs);
    else v = this.given.concat(this.objs);
    return v;
  };
  // points d'accroche : points nommés, extrémités, sommets de cônes, intersections
  Pl.prototype.cibles = function () {
    var self = this, pts = [], lig = [];
    this.visibles().forEach(function (o) {
      if (o.k === "pt") pts.push({ x: o.x, y: o.y, n: o.n });
      else if (o.k === "sg" || o.k === "vec") { pts.push({ x: o.x1, y: o.y1 }); pts.push({ x: o.x2, y: o.y2 }); }
      else if (o.k === "cone") pts.push({ x: o.x, y: o.y });
      self.lignes(o).forEach(function (l) { lig.push(l); });
    });
    var inter = [];
    for (var i = 0; i < lig.length; i++) for (var j = i + 1; j < lig.length; j++) {
      var p = G.intersect(lig[i].L, lig[j].L);
      if (!p || p.x < -1 || p.y < -1 || p.x > this.W + 1 || p.y > this.H + 1) continue;
      if (!dans(lig[i], p) || !dans(lig[j], p)) continue;
      inter.push({ x: p.x, y: p.y });
    }
    function dans(l, p) { return !l.a || G.distSeg(p, l.a, l.b) < 0.05; }
    return { pts: pts, inter: inter, lig: lig };
  };
  Pl.prototype.tol = function () {
    var r = this.svg.getBoundingClientRect();
    return r.width ? 13 * this.W / r.width : 4;
  };
  Pl.prototype.snap = function (p) {
    var c = this.cible || (this.cible = this.cibles()), t = this.tol(), best = null, d, i;
    for (i = 0; i < c.pts.length; i++) {
      d = G.len(c.pts[i].x - p.x, c.pts[i].y - p.y);
      if (d < t && (!best || d < best.d)) best = { x: c.pts[i].x, y: c.pts[i].y, d: d, type: "point", n: c.pts[i].n };
    }
    if (best) return best;
    for (i = 0; i < c.inter.length; i++) {
      d = G.len(c.inter[i].x - p.x, c.inter[i].y - p.y);
      if (d < t && (!best || d < best.d)) best = { x: c.inter[i].x, y: c.inter[i].y, d: d, type: "inter" };
    }
    if (best) return best;
    var l = this.ligneProche(p, t * 0.8);
    if (l) { var q = G.project(p, l.L); return { x: q.x, y: q.y, type: "ligne" }; }
    return { x: p.x, y: p.y, type: "libre" };
  };
  Pl.prototype.ligneProche = function (p, t) {
    var c = this.cible || (this.cible = this.cibles()), best = null;
    c.lig.forEach(function (l) {
      var d = l.a ? G.distSeg(p, l.a, l.b) : G.distLine(p, l.L);
      if (d < t && (!best || d < best.d)) best = { L: l.L, d: d };
    });
    return best;
  };
  Pl.prototype.pos = function (e) {
    var pt = this.svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    var m = this.svg.getScreenCTM();
    var q = m ? pt.matrixTransform(m.inverse()) : { x: 0, y: 0 };
    return { x: q.x, y: q.y };
  };

  Pl.prototype.setTool = function (t) {
    if (!OUTILS[t]) return;
    this.cancel(); this.tool = t;
    $$("[data-pl-tool]", this.root).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-pl-tool") === t ? "true" : "false"); });
    this.root.classList.toggle("pl-t-main", t === "main");
    this.root.classList.toggle("pl-t-gom", t === "gom");
    this.aide();
  };
  Pl.prototype.aide = function (msg) {
    var el = $(".pl-aide", this.root);
    if (!el) return;
    var o = OUTILS[this.tool];
    el.innerHTML = msg || ("<b>" + o[0] + "</b> — " + o[1][Math.min(this.pend.length, o[1].length - 1)]);
  };
  Pl.prototype.cancel = function () {
    this.pend = []; var a = $(".pl-ask", this.root); if (a) a.remove();
    this.drawPrev(); this.aide();
  };
  Pl.prototype.down = function (e) {
    if (e.button > 0) return;
    if (this.tool === "main") {
      this.pan = { x: e.clientX, y: e.clientY, l: this.stage.scrollLeft, t: this.stage.scrollTop };
      this.svg.setPointerCapture(e.pointerId); return;
    }
    if (this.locked || !this.editable() || $(".pl-ask", this.root)) return;
    e.preventDefault();
    var p = this.pos(e), t = this.tool, self = this, s = this.snap(p);
    if (t === "gom") { this.gomme(p); return; }
    if (t === "tx") { this.ask(e, [["Texte", ""]], function (v) { if (v[0].trim()) self.add({ k: "tx", x: s.x, y: s.y, s: v[0].trim() }); }); return; }
    if (t === "pt") {
      this.ask(e, [["Nom du point", this.lettre()]], function (v) { self.add({ k: "pt", x: s.x, y: s.y, n: v[0].trim() }); });
      return;
    }
    var refTools = { par: 1, perp: 1, inc: 1, ang: 1 };
    var needRef = (refTools[t] && this.pend.length === 0) || (t === "ang" && this.pend.length === 1) || (t === "cone" && this.pend.length === 1);
    if (needRef) {
      var l = this.ligneProche(p, this.tol());
      if (!l && t !== "inc") { this.aide("<b>" + OUTILS[t][0] + "</b> — aucune droite ici : clique plus près d'une droite ou d'un vecteur."); return; }
      this.pend.push({ ref: l ? l.L : G.line(0, 0, 1, 0), p: p });
    } else this.pend.push(s);
    this.etape(e);
  };
  Pl.prototype.etape = function (e) {
    var t = this.tool, P = this.pend, self = this, a = P[0], b = P[1];
    function fin() { self.pend = []; self.drawPrev(); self.aide(); }
    if ((t === "dr" || t === "sg" || t === "dist") && P.length === 2) {
      if (G.len(b.x - a.x, b.y - a.y) < 0.3) { P.pop(); return; }
      if (t === "dr") this.add({ k: "dr", x: a.x, y: a.y, ux: b.x - a.x, uy: b.y - a.y });
      else if (t === "sg") this.add({ k: "sg", x1: a.x, y1: a.y, x2: b.x, y2: b.y });
      else this.add({ k: "mes", x1: a.x, y1: a.y, x2: b.x, y2: b.y });
      fin(); return;
    }
    if ((t === "par" || t === "perp") && P.length === 2) {
      var L = (t === "par" ? G.parallel : G.perpendicular)(a.ref, b);
      this.add({ k: "dr", x: b.x, y: b.y, ux: L.ux, uy: L.uy }); fin(); return;
    }
    if (t === "inc" && P.length === 2) {
      this.ask(e, [["Angle (°)", ""]], function (v) {
        var d = G.parseNum(v[0]);
        if (d === null) return;
        var L = G.inclined(a.ref, b, d);
        self.add({ k: "dr", x: b.x, y: b.y, ux: L.ux, uy: L.uy });
      }, fin); return;
    }
    if (t === "ang" && P.length === 2) {
      var I = G.intersect(a.ref, b.ref);
      var ang = G.acute(a.ref, b.ref);
      var o = { k: "arc", v: ang };
      if (I) { o.x = I.x; o.y = I.y; o.u1 = [a.ref.ux, a.ref.uy]; o.u2 = [b.ref.ux, b.ref.uy]; o.hx = (a.p.x + b.p.x) / 2; o.hy = (a.p.y + b.p.y) / 2; }
      else { o.x = b.p.x; o.y = b.p.y; }
      this.add(o); this.aide("<b>Angle</b> — angle aigu entre les deux droites : <b>" + fr(ang, 1) + " °</b>."); this.pend = []; this.drawPrev(); return;
    }
    if (t === "cone" && P.length === 2) {
      this.ask(e, [["f ou φ (°)", ""]], function (v) {
        var phi = G.parsePhi(v[0]);
        if (phi === null) return;
        // la normale est orientée vers le côté où l'on a cliqué
        var n = { x: b.ref.ux, y: b.ref.uy };
        if ((b.p.x - a.x) * n.x + (b.p.y - a.y) * n.y < 0) n = { x: -n.x, y: -n.y };
        self.add({ k: "cone", x: a.x, y: a.y, ux: n.x, uy: n.y, phi: phi, r: Math.min(self.W, self.H) * 0.22 });
      }, fin); return;
    }
    if (t === "vec" && P.length === 2) {
      if (G.len(b.x - a.x, b.y - a.y) < 0.3) { P.pop(); return; }
      var L0 = G.len(b.x - a.x, b.y - a.y), champs = [["Nom", ""]];
      if (this.scale) champs.push(["Norme (" + this.cfg.forces.u + ")", fr(L0 * this.scale, L0 * this.scale < 100 ? 1 : 0)]);
      this.ask(e, champs, function (v) {
        var x2 = b.x, y2 = b.y;
        if (self.scale && v[1] !== undefined) {
          var F = G.parseNum(v[1]);
          if (F !== null && F > 0 && Math.abs(F - L0 * self.scale) > 1e-6 * F) {
            var k = F / self.scale / L0; x2 = a.x + (b.x - a.x) * k; y2 = a.y + (b.y - a.y) * k;
          }
        }
        self.add({ k: "vec", x1: a.x, y1: a.y, x2: x2, y2: y2, n: v[0].trim(), c: self.color });
      }, fin); return;
    }
    this.aide(); this.drawPrev();
  };
  Pl.prototype.lettre = function () {
    var pris = {};
    this.visibles().forEach(function (o) { if (o.n) pris[o.n] = 1; });
    for (var i = 0; i < LETTRES.length; i++) if (!pris[LETTRES[i]]) return LETTRES[i];
    return "";
  };
  // petite fenêtre de saisie posée sur la feuille
  Pl.prototype.ask = function (e, champs, ok, after) {
    var self = this, r = this.stage.getBoundingClientRect(), f = document.createElement("form");
    f.className = "pl-ask";
    f.innerHTML = champs.map(function (c, i) {
      return '<label><span>' + esc(c[0]) + '</span><input type="text" value="' + esc(c[1]) + '" data-i="' + i + '" autocomplete="off" spellcheck="false"></label>';
    }).join("") + '<button type="submit" class="btn">OK</button><button type="button" class="btn ghost pl-ask-x">Annuler</button>';
    var x = Math.min(Math.max(4, e.clientX - r.left + this.stage.scrollLeft + 10), this.stage.scrollWidth - 230);
    var y = Math.max(4, e.clientY - r.top + this.stage.scrollTop + 10);
    f.style.left = x + "px"; f.style.top = y + "px";
    this.stage.appendChild(f);
    var ins = $$("input", f); setTimeout(function () { ins[0].focus(); ins[0].select(); }, 0);
    function close() { f.remove(); if (after) after(); else { self.pend = []; self.drawPrev(); self.aide(); } }
    f.addEventListener("submit", function (ev) { ev.preventDefault(); var v = ins.map(function (i) { return i.value; }); f.remove(); ok(v); if (after) after(); else self.aide(); });
    $(".pl-ask-x", f).addEventListener("click", close);
    f.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { ev.preventDefault(); ev.stopPropagation(); close(); } });
  };
  Pl.prototype.move = function (e) {
    if (this.pan) {
      this.stage.scrollLeft = this.pan.l - (e.clientX - this.pan.x);
      this.stage.scrollTop = this.pan.t - (e.clientY - this.pan.y); return;
    }
    if (this.locked || !this.editable() || this.tool === "main") return;
    var p = this.pos(e);
    this.hover = { p: p, s: this.snap(p) };
    this.drawPrev();
    this.lecture();
  };
  Pl.prototype.up = function () { this.pan = null; };
  Pl.prototype.editable = function () { return !this.cfg.fig && (!this.cfg.scenarios || this.essai); };

  Pl.prototype.add = function (o) {
    if (o.k === "dr") { var u = G.unit(o.ux, o.uy); if (!u) return; o.ux = u.x; o.uy = u.y; }
    if (!o.c) o.c = this.color;
    this.commit(function (objs) { objs.push(o); });
  };
  Pl.prototype.commit = function (fn) {
    this.hist.push(JSON.stringify(this.objs)); this.redo = [];
    fn(this.objs);
    this.changed();
  };
  Pl.prototype.changed = function () {
    this.cible = null; this.draw(); this.releves();
    if (this.opts.onChange) this.opts.onChange(this);
  };
  Pl.prototype.undo = function () {
    if (this.locked || !this.hist.length) return;
    this.redo.push(JSON.stringify(this.objs)); this.objs = JSON.parse(this.hist.pop()); this.changed();
  };
  Pl.prototype.redoOne = function () {
    if (this.locked || !this.redo.length) return;
    this.hist.push(JSON.stringify(this.objs)); this.objs = JSON.parse(this.redo.pop()); this.changed();
  };
  Pl.prototype.gomme = function (p) {
    var self = this, t = this.tol(), best = -1, bd = t;
    this.objs.forEach(function (o, i) {
      var d = self.distObj(o, p);
      if (d < bd) { bd = d; best = i; }
    });
    if (best >= 0) this.commit(function (objs) { objs.splice(best, 1); });
  };
  Pl.prototype.distObj = function (o, p) {
    if (o.k === "pt" || o.k === "tx" || o.k === "arc") return G.len(o.x - p.x, o.y - p.y);
    if (o.k === "poly") return Infinity;
    if (o.k === "mes") return G.distSeg(p, { x: o.x1, y: o.y1 }, { x: o.x2, y: o.y2 });
    var l = this.lignes(o), d = Infinity;
    l.forEach(function (x) { d = Math.min(d, x.a ? G.distSeg(p, x.a, x.b) : G.distLine(p, x.L)); });
    return d;
  };

  // ---------- dessin ----------
  Pl.prototype.rendu = function (o, cls) {
    var W = this.W, H = this.H, s = "", st = (o.st ? " s-" + o.st : "") + (o.d ? " pl-pointille" : ""),
      col = cls === "usr" && o.c ? ' style="--c:' + o.c + '"' : "", fs = this.cfg.fs || 4.2, self = this;
    var g = '<g class="o-' + cls + st + '"' + col + ">";
    if (o.k === "pt") {
      var r = fs * 0.32;
      s = '<path class="pl-croix" d="M' + n2(o.x - r) + " " + n2(o.y - r) + "l" + n2(2 * r) + " " + n2(2 * r) + "m0 -" + n2(2 * r) + "l-" + n2(2 * r) + " " + n2(2 * r) + '"/>';
      if (o.n) s += nom(o.n, o.x + (o.dx != null ? o.dx : fs * 0.45), o.y + (o.dy != null ? o.dy : -fs * 0.35), fs, false);
    } else if (o.k === "dr") {
      var seg = G.clip(G.line(o.x, o.y, o.ux, o.uy), W, H);
      if (seg) s = '<path class="pl-tr" d="M' + n2(seg[0].x) + " " + n2(seg[0].y) + "L" + n2(seg[1].x) + " " + n2(seg[1].y) + '"/>';
      if (o.n && seg) s += nom(o.n, o.nx != null ? o.nx : (seg[1].x * 0.9 + seg[0].x * 0.1), o.ny != null ? o.ny : (seg[1].y * 0.9 + seg[0].y * 0.1), fs * 0.9, false);
    } else if (o.k === "sg") {
      s = '<path class="pl-tr" d="M' + n2(o.x1) + " " + n2(o.y1) + "L" + n2(o.x2) + " " + n2(o.y2) + '"/>';
    } else if (o.k === "vec") {
      s = fleche(o.x1, o.y1, o.x2, o.y2, fs * 0.85);
      if (o.n) {
        var u = G.unit(o.x2 - o.x1, o.y2 - o.y1) || { x: 1, y: 0 }, mx = (o.x1 + o.x2) / 2, my = (o.y1 + o.y2) / 2;
        var off = fs * 0.75, nx = -u.y, ny = u.x;
        if (ny > 0) { nx = -nx; ny = -ny; }
        s += nom(o.n, o.nx != null ? o.nx : mx + nx * off + (nx < 0 ? -fs * 1.3 : fs * 0.2), o.ny != null ? o.ny : my + ny * off + fs * 0.2, fs, true);
      }
    } else if (o.k === "cone") {
      var n = { x: o.ux, y: o.uy }, e1 = G.rotScreen(n, o.phi), e2 = G.rotScreen(n, -o.phi), R = o.r || 30;
      var sw = (e1.x * e2.y - e1.y * e2.x) > 0 ? 1 : 0;
      [1, -1].forEach(function (sg) {
        if (sg < 0 && o.une) return;
        s += '<path class="pl-cone-f" d="M' + n2(o.x) + " " + n2(o.y) + "L" + n2(o.x + sg * R * e1.x) + " " + n2(o.y + sg * R * e1.y) +
          "A" + R + " " + R + " 0 0 " + sw + " " + n2(o.x + sg * R * e2.x) + " " + n2(o.y + sg * R * e2.y) + 'Z"/>';
      });
      self.lignes(o).forEach(function (l) {
        var sgm = G.clip(l.L, W, H);
        if (sgm) s += '<path class="pl-cone-l" d="M' + n2(sgm[0].x) + " " + n2(sgm[0].y) + "L" + n2(sgm[1].x) + " " + n2(sgm[1].y) + '"/>';
      });
      if (o.n) s += '<text class="pl-txt" x="' + n2(o.x + n.x * R * 0.82 + 1) + '" y="' + n2(o.y + n.y * R * 0.82) + '" font-size="' + n2(fs * 0.8) + '">' + esc(o.n) + "</text>";
    } else if (o.k === "poly") {
      s = '<path class="pl-poly" d="M' + o.pts.map(function (q) { return n2(q[0]) + " " + n2(q[1]); }).join("L") + 'Z"/>';
      if (o.n) s += '<text class="pl-txt" x="' + n2(o.nx) + '" y="' + n2(o.ny) + '" font-size="' + n2(fs * 0.8) + '">' + esc(o.n) + "</text>";
    } else if (o.k === "tx") {
      s = '<text class="pl-txt" x="' + n2(o.x) + '" y="' + n2(o.y) + '" font-size="' + n2(o.size || fs) + '">' + esc(o.s) + "</text>";
    } else if (o.k === "mes") {
      var L = G.len(o.x2 - o.x1, o.y2 - o.y1), ux = (o.x2 - o.x1) / (L || 1), uy = (o.y2 - o.y1) / (L || 1);
      s = '<path class="pl-mes" d="M' + n2(o.x1) + " " + n2(o.y1) + "L" + n2(o.x2) + " " + n2(o.y2) + '"/>' +
        '<text class="pl-txt pl-mes-t" x="' + n2((o.x1 + o.x2) / 2 - uy * fs * 0.6) + '" y="' + n2((o.y1 + o.y2) / 2 + ux * fs * 0.6) + '" font-size="' + n2(fs * 0.8) + '">' + esc(this.texteMesure(L)) + "</text>";
    } else if (o.k === "arc") {
      var rr = fs * 2.6, t = o.s || (fr(o.v, 1) + " °");
      if (o.u1) {
        var a1 = { x: o.u1[0], y: o.u1[1] }, a2 = { x: o.u2[0], y: o.u2[1] };
        // côtés de l'angle orientés vers l'endroit cliqué (ou donné)
        if (o.hx != null) {
          if ((o.hx - o.x) * a1.x + (o.hy - o.y) * a1.y < 0) a1 = { x: -a1.x, y: -a1.y };
          if ((o.hx - o.x) * a2.x + (o.hy - o.y) * a2.y < 0) a2 = { x: -a2.x, y: -a2.y };
        }
        if (a1.x * a2.x + a1.y * a2.y < 0 && !o.obtus) a2 = { x: -a2.x, y: -a2.y };
        var sw2 = (a1.x * a2.y - a1.y * a2.x) > 0 ? 1 : 0, bx = a1.x + a2.x, by = a1.y + a2.y, bl = G.len(bx, by) || 1;
        s = '<path class="pl-arc" d="M' + n2(o.x + rr * a1.x) + " " + n2(o.y + rr * a1.y) + "A" + rr + " " + rr + " 0 0 " + sw2 + " " + n2(o.x + rr * a2.x) + " " + n2(o.y + rr * a2.y) + '"/>' +
          '<text class="pl-txt pl-arc-t" x="' + n2(o.x + (rr + fs * 0.6) * bx / bl) + '" y="' + n2(o.y + (rr + fs * 0.6) * by / bl + fs * 0.3) + '" font-size="' + n2(fs * 0.8) + '" text-anchor="middle">' + esc(t) + "</text>";
      } else s = '<text class="pl-txt" x="' + n2(o.x) + '" y="' + n2(o.y) + '" font-size="' + n2(fs * 0.8) + '">' + esc(t) + "</text>";
    }
    return g + s + "</g>";
  };
  Pl.prototype.texteMesure = function (L) {
    var t = fr(L, 1) + " mm";
    if (this.kL !== 1) t += " (" + fr(L * this.kL, 0) + " mm réels)";
    if (this.scale) t += " ≙ " + fr(L * this.scale, L * this.scale < 100 ? 1 : 0) + " " + this.cfg.forces.u;
    return t;
  };
  Pl.prototype.draw = function () {
    var self = this;
    this.L.given.innerHTML = this.given.map(function (o) { return self.rendu(o, "giv"); }).join("");
    this.L.demo.innerHTML = (this.essai ? [] : (this.demoObjs || [])).map(function (o) { return self.rendu(o, "dem"); }).join("");
    this.L.usr.innerHTML = this.objs.map(function (o) { return self.rendu(o, "usr"); }).join("");
    var corr = this.showCorr && this.revealed;
    this.L.corr.innerHTML = corr ? this.corr.map(function (o) { return self.rendu(o, "cor"); }).join("") : "";
    var se = $(".pl-scale-v", this.root);
    if (se && this.scale) se.textContent = "1 mm ↔ " + fr(this.scale, this.scale < 10 ? 1 : 0) + " " + this.cfg.forces.u;
    this.drawPrev();
  };
  Pl.prototype.drawPrev = function () {
    var h = this.hover, s = "", P = this.pend, t = this.tool, fs = this.cfg.fs || 4.2;
    if (h && !this.locked && this.editable() && t !== "main" && t !== "gom") {
      var q = h.s, a = P[0];
      if (a && a.x !== undefined && (t === "dr" || t === "sg" || t === "vec" || t === "dist")) {
        if (t === "dr") { var sg = G.clip(G.through(a, q) || G.line(a.x, a.y, 1, 0), this.W, this.H); if (sg) s += '<path class="pl-prev" d="M' + n2(sg[0].x) + " " + n2(sg[0].y) + "L" + n2(sg[1].x) + " " + n2(sg[1].y) + '"/>'; }
        else if (t === "vec") s += '<g class="pl-prev-v">' + fleche(a.x, a.y, q.x, q.y, fs * 0.85) + "</g>";
        else s += '<path class="pl-prev" d="M' + n2(a.x) + " " + n2(a.y) + "L" + n2(q.x) + " " + n2(q.y) + '"/>';
      }
      if (P.length === 1 && P[0].ref && (t === "par" || t === "perp" || t === "inc")) {
        var L = t === "par" ? G.parallel(P[0].ref, q) : (t === "perp" ? G.perpendicular(P[0].ref, q) : null);
        if (L) { var c = G.clip(L, this.W, this.H); if (c) s += '<path class="pl-prev" d="M' + n2(c[0].x) + " " + n2(c[0].y) + "L" + n2(c[1].x) + " " + n2(c[1].y) + '"/>'; }
      }
      var R = fs * 0.55;
      if (q.type === "point" || q.type === "inter") s += '<circle class="pl-aim" cx="' + n2(q.x) + '" cy="' + n2(q.y) + '" r="' + n2(R) + '"/>';
      else if (q.type === "ligne") s += '<rect class="pl-aim" x="' + n2(q.x - R * 0.7) + '" y="' + n2(q.y - R * 0.7) + '" width="' + n2(R * 1.4) + '" height="' + n2(R * 1.4) + '"/>';
    }
    // référence choisie : surlignée
    P.forEach(function (x) {
      if (x.ref) { var c = G.clip(x.ref, this.W, this.H); if (c) s += '<path class="pl-ref" d="M' + n2(c[0].x) + " " + n2(c[0].y) + "L" + n2(c[1].x) + " " + n2(c[1].y) + '"/>'; }
      else if (x.x !== undefined) s += '<circle class="pl-aim pl-aim-on" cx="' + n2(x.x) + '" cy="' + n2(x.y) + '" r="' + n2(fs * 0.4) + '"/>';
    }, this);
    this.L.prev.innerHTML = s;
  };
  // lecture au survol : où s'aimante le pointeur, longueur en cours
  Pl.prototype.lecture = function () {
    var el = $(".pl-lect", this.root), h = this.hover;
    if (!el || !h) return;
    var q = h.s, txt = { point: "sur le point " + (q.n || ""), inter: "sur une intersection", ligne: "sur une droite", libre: "" }[q.type];
    var a = this.pend[0];
    if (a && a.x !== undefined && (this.tool === "vec" || this.tool === "dist" || this.tool === "sg")) {
      var L = G.len(q.x - a.x, q.y - a.y);
      txt = (txt ? txt + " · " : "") + "longueur " + this.texteMesure(L);
      if (this.tool === "vec") txt += " · direction " + fr(G.heading(q.x - a.x, q.y - a.y), 1) + " °";
    }
    el.textContent = txt ? "Pointeur " + txt.replace(/^sur/, "sur") : "";
  };
  // relevés : vecteurs, distances et angles de l'élève
  Pl.prototype.releves = function () {
    var el = $(".pl-releves tbody", this.root), self = this;
    if (!el) return;
    var rows = [];
    this.objs.forEach(function (o) {
      if (o.k === "vec") {
        var L = G.len(o.x2 - o.x1, o.y2 - o.y1);
        rows.push("<tr><td>Vecteur " + esc(o.n || "sans nom") + "</td><td>" + fr(L, 1) + " mm</td><td>" +
          (self.scale ? fr(L * self.scale, L * self.scale < 100 ? 1 : 0) + " " + self.cfg.forces.u : "—") + "</td><td>" +
          fr(G.heading(o.x2 - o.x1, o.y2 - o.y1), 1) + " °</td></tr>");
      } else if (o.k === "mes") {
        var D = G.len(o.x2 - o.x1, o.y2 - o.y1);
        rows.push("<tr><td>Distance</td><td>" + fr(D, 1) + " mm</td><td>" + (self.kL !== 1 ? fr(D * self.kL, 0) + " mm réels" :
          (self.scale ? fr(D * self.scale, 1) + " " + self.cfg.forces.u : "—")) + "</td><td></td></tr>");
      } else if (o.k === "arc") rows.push("<tr><td>Angle mesuré</td><td></td><td></td><td>" + fr(o.v, 1) + " °</td></tr>");
    });
    el.innerHTML = rows.join("") || '<tr><td colspan="4" class="small">Tes vecteurs, distances et angles mesurés s\'affichent ici.</td></tr>';
  };

  Pl.prototype.setZoom = function (w) {
    var i = ZOOMS.indexOf(this.zoom); if (i < 0) i = 0;
    if (w === "in") i = Math.min(ZOOMS.length - 1, i + 1); else if (w === "out") i = Math.max(0, i - 1); else i = 0;
    var st = this.stage, cx = (st.scrollLeft + st.clientWidth / 2) / Math.max(1, st.scrollWidth), cy = (st.scrollTop + st.clientHeight / 2) / Math.max(1, st.scrollHeight);
    this.zoom = ZOOMS[i];
    st.classList.toggle("zoomed", this.zoom > 1);
    this.svg.style.width = this.zoom > 1 ? this.zoom * 100 + "%" : "";
    var zv = $(".pl-zoom-v", this.root); if (zv) zv.textContent = Math.round(this.zoom * 100) + " %";
    requestAnimationFrame(function () { st.scrollLeft = cx * st.scrollWidth - st.clientWidth / 2; st.scrollTop = cy * st.scrollHeight - st.clientHeight / 2; });
  };
  Pl.prototype.toggleFull = function () {
    var on = !this.root.classList.contains("is-full");
    this.root.classList.toggle("is-full", on);
    document.body.classList.toggle("sk-full-open", on);
    var b = $("[data-pl-act=full]", this.root);
    if (b) { b.textContent = on ? "Quitter le plein écran" : "Plein écran"; b.setAttribute("aria-pressed", on ? "true" : "false"); }
    if (!on) this.root.scrollIntoView({ block: "start" });
  };
  // document réponse à imprimer à 100 % : la feuille garde ses dimensions en millimètres
  Pl.prototype.printDR = function () {
    var w = window.open("", "_blank");
    if (!w) { alert("La fenêtre d'impression a été bloquée par le navigateur. Autorise les fenêtres surgissantes pour ce fichier, puis réessaie."); return; }
    var clone = this.svg.cloneNode(true);
    ["demo", "usr", "corr", "prev", "snap"].forEach(function (k) { var g = clone.querySelector(".pl-" + k); if (g) g.innerHTML = ""; });
    clone.setAttribute("width", this.W + "mm"); clone.setAttribute("height", this.H + "mm"); clone.removeAttribute("style");
    var titre = this.cfg.titre || "Document réponse", css = $("#pl-css") ? $("#pl-css").textContent : "";
    w.document.write('<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>' + esc(titre) + "</title><style>" + css +
      "@page{size:A4 landscape;margin:8mm}body{margin:0;font:13px/1.4 system-ui,Segoe UI,Arial,sans-serif;color:#1C2530}" +
      "header{display:flex;gap:16px;align-items:baseline;border-bottom:1.5px solid #1C2530;margin-bottom:3mm}h2{font-size:12pt;margin:0}" +
      ".bar{background:#1C2530;color:#fff;padding:8px 14px;display:flex;gap:12px;align-items:center}.bar p{margin:0;flex:1}" +
      ".bar button{border:0;background:#F2B705;font-weight:700;padding:8px 14px;cursor:pointer}@media print{.bar{display:none}}</style></head><body>" +
      '<div class="bar"><p>Imprime à 100 % (sans « ajuster à la page ») : la feuille garde ses dimensions, ' + esc(this.cfg.echTxt || "") + '.</p><button type="button" onclick="window.print()">Imprimer</button></div>' +
      "<header><h2>" + esc(titre) + "</h2><span>" + esc(this.cfg.echTxt || "") + "</span><span>Nom : ________________________</span></header>" +
      clone.outerHTML + "</body></html>");
    w.document.close();
  };

  // ---------- exercice : validation, correction, auto-évaluation ----------
  Pl.prototype.validate = function () {
    if (this.locked) return;
    this.locked = true; this.cancel(); this.root.classList.add("locked");
    $$(".pl-bar button", this.root).forEach(function (b) {
      var k = b.getAttribute("data-pl-act");
      if (!(k === "full" || k === "print" || b.hasAttribute("data-pl-zoom") || b.getAttribute("data-pl-tool") === "main")) b.disabled = true;
    });
    var bv = $(".pl-valider", this.root); if (bv) { bv.disabled = true; bv.textContent = "Construction validée"; }
    var st = $(".pl-statut", this.root); if (st) st.textContent = this.objs.length ? "Construction enregistrée" : "Construction validée vide";
    this.setTool("main");
    this.checkReveal();
  };
  Pl.prototype.checkReveal = function () {
    var app = this.opts.app;
    if (!this.locked || this.revealed || !app) return;
    var deps = (window.__SKCFG__[this.id] || {}).deps || [], state = app.state;
    var manque = deps.filter(function (d) { return !(state[d] && state[d].validated); });
    var wt = $(".pl-wait", this.root);
    if (manque.length) {
      if (wt) wt.textContent = "La correction et l'auto-évaluation s'afficheront après validation de : " +
        manque.map(function (d) { return window.__QCFG__[d].label; }).join(", ") + ".";
      return;
    }
    if (wt) wt.textContent = "";
    this.revealed = true; this.root.classList.add("revealed");
    var tg = $(".pl-corr-toggle input", this.root); if (tg) { tg.checked = true; this.showCorr = true; }
    $$(".q-expl, .selfeval", this.root).forEach(function (x) { x.hidden = false; x.classList.add("reveal"); });
    this.refreshSelf(); this.draw();
  };
  Pl.prototype.boxes = function () { return $$(".selfeval input[data-crit]", this.root); };
  Pl.prototype.refreshSelf = function () {
    if (this.selfDone) return;
    var n = this.boxes().filter(function (c) { return c.checked; }).length, pts = this.boxes().length, el = $(".se-score", this.root);
    if (el) el.textContent = n + " / " + pts + " critère" + (pts > 1 ? "s" : "") + " coché" + (n > 1 ? "s" : "");
  };
  Pl.prototype.selfAssess = function () {
    var app = this.opts.app;
    if (this.selfDone || !app) return;
    var bx = this.boxes(), n = bx.filter(function (c) { return c.checked; }).length, pts = bx.length;
    this.selfDone = true;
    app.state[this.id] = { validated: true, sketch: true, score: pts ? n / pts : 0, self: n };
    bx.forEach(function (c) { c.disabled = true; });
    var b = $(".btn-self", this.root); b.disabled = true; b.textContent = "Auto-évaluation validée";
    var txt = n + " point" + (n > 1 ? "s" : "") + " sur " + pts + " attribué" + (n > 1 ? "s" : "") + " à cette construction";
    $(".se-score", this.root).textContent = txt;
    var pr = $(".se-print", this.root); if (pr) pr.textContent = "Auto-évaluation : " + txt + ".";
    this.root.classList.add(n === pts ? "is-ok" : (n ? "is-half" : "is-ko"));
    app.updateScore();
  };

  // ---------- démonstration pas à pas ----------
  Pl.prototype.setScen = function (k) {
    var sc = this.cfg.scenarios;
    this.scen = Math.max(0, Math.min(sc.length - 1, k));
    $$("[data-pl-scen]", this.root).forEach(function (b, i) { b.setAttribute("aria-pressed", i === this.scen ? "true" : "false"); }, this);
    this.setStep(0);
  };
  Pl.prototype.setStep = function (k) {
    var self = this, steps = this.cfg.scenarios[this.scen].steps;
    this.step = Math.max(0, Math.min(steps.length, k));
    this.demoObjs = [];
    for (var i = 0; i < this.step; i++) steps[i].o.forEach(function (o) { self.demoObjs.push(self.prep(o)); });
    var t = $(".pl-etape-t", this.root), n = $(".pl-etape-n", this.root);
    if (n) n.textContent = "Étape " + this.step + " / " + steps.length;
    if (t) t.innerHTML = this.step ? steps[this.step - 1].t : this.cfg.scenarios[this.scen].intro;
    var p = $("[data-pl-act=prev]", this.root), nx = $("[data-pl-act=next]", this.root);
    if (p) p.disabled = this.step === 0;
    if (nx) nx.disabled = this.step === steps.length;
    this.cible = null; this.draw();
  };
  Pl.prototype.toggleEssai = function () {
    this.essai = !this.essai;
    this.root.classList.toggle("pl-essai", this.essai);
    var b = $("[data-pl-act=essai]", this.root);
    if (b) { b.textContent = this.essai ? "Revoir la démonstration" : "Construire moi-même"; b.setAttribute("aria-pressed", this.essai ? "true" : "false"); }
    this.cible = null; this.cancel(); this.draw(); this.releves();
  };
  // ---------- atelier : changer de fond ----------
  Pl.prototype.setFond = function (key) {
    var f = (this.cfg.fonds || {})[key];
    if (!f) return;
    var bg = $(".pl-svg .pl-bg", this.root), tpl = document.getElementById("pl-fond-" + key);
    bg.innerHTML = tpl ? tpl.innerHTML : "";
    this.W = f.w; this.H = f.h; this.kL = f.kL || 1; this.cfg.echTxt = f.echTxt; this.cfg.titre = f.titre;
    this.svg.setAttribute("viewBox", "0 0 " + f.w + " " + f.h);
    $(".pl-svg .pl-grille", this.root).innerHTML = f.grille || "";
    this.given = (f.given || []).map(function (o) { return this.prep(o); }, this);
    var ech = $(".pl-ech", this.root); if (ech) ech.textContent = f.echTxt || "";
    this.objs = []; this.hist = []; this.redo = []; this.changed();
  };

  function init(root, opts) {
    var id = root.getAttribute("data-planche");
    if (all[id] && all[id].root === root) return all[id];
    var cfg = CFG[id];
    if (!cfg) return null;
    all[id] = new Pl(root, cfg, opts);
    all[id].releves();
    return all[id];
  }
  function initAll(scope, opts) {
    return $$(".pl[data-planche]", scope || document).map(function (r) { return init(r, opts); });
  }
  return { init: init, initAll: initAll, all: all, Geom: G };
})();
