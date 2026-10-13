"""Environnement de construction graphique : outils Python des planches (src/planche.js, src/planche.css).

Une planche est une feuille cotée en millimètres. Son fond (le mécanisme dessiné à l'échelle), ses éléments donnés,
sa correction et ses démonstrations sont décrits ici dans le repère réel du mécanisme (x vers la droite, y vers le
haut, en millimètres réels), puis convertis dans le repère de la feuille (x vers la droite, y vers le bas, en
millimètres de feuille) par Feuille. Les corrections sont calculées, pas recopiées : les intersections, les
directions et les normes des vecteurs viennent des mêmes données que les réponses attendues des questions.
"""
import html
import json
import math

# ============================================================ géométrie (repère réel, y vers le haut)


def vec(a, b):
    return (b[0] - a[0], b[1] - a[1])


def unit(u):
    n = math.hypot(*u)
    return (u[0] / n, u[1] / n)


def rot(u, deg):
    """Rotation d'un angle en degrés, sens trigonométrique."""
    a = math.radians(deg)
    return (u[0] * math.cos(a) - u[1] * math.sin(a), u[0] * math.sin(a) + u[1] * math.cos(a))


def direction(deg):
    return (math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def inter(p, u, q, v):
    """Intersection des droites (p, u) et (q, v)."""
    d = u[0] * v[1] - u[1] * v[0]
    if abs(d) < 1e-12:
        raise ValueError("droites parallèles")
    t = ((q[0] - p[0]) * v[1] - (q[1] - p[1]) * v[0]) / d
    return (p[0] + t * u[0], p[1] + t * u[1])


def angle_deg(u):
    return math.degrees(math.atan2(u[1], u[0]))


def ecart(u, v):
    """Angle aigu entre deux directions, en degrés."""
    c = abs(u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
    return math.degrees(math.acos(min(1.0, c)))


def triangle(F, u1, u2):
    """Dynamique de trois forces : F connue (vecteur), directions u1 et u2 des deux autres. Renvoie les deux
    vecteurs F1 = a·u1 et F2 = b·u2 tels que F + F1 + F2 = 0."""
    d = u1[0] * u2[1] - u1[1] * u2[0]
    a = (-F[0] * u2[1] + F[1] * u2[0]) / d
    b = (-u1[0] * F[1] + u1[1] * F[0]) / d
    return (a * u1[0], a * u1[1]), (b * u2[0], b * u2[1])


# ============================================================ la feuille
class Feuille:
    """Repère de la feuille : (ox, oy) position (mm de feuille) de l'origine réelle ; k mm réels par mm de feuille."""

    def __init__(self, w, h, ox, oy, k=1.0):
        self.w, self.h, self.ox, self.oy, self.k = w, h, ox, oy, k

    def p(self, P):
        return (round(self.ox + P[0] / self.k, 3), round(self.oy - P[1] / self.k, 3))

    def d(self, u):
        return (round(u[0], 6), round(-u[1], 6))

    def l(self, L):
        """Longueur réelle → longueur sur la feuille."""
        return L / self.k

    # ---------- éléments de la planche (dictionnaires lus par planche.js) ----------
    def pt(self, P, n="", dx=None, dy=None, **kw):
        X, Y = self.p(P)
        o = {"k": "pt", "x": X, "y": Y, "n": n}
        if dx is not None:
            o["dx"], o["dy"] = dx, dy
        o.update(kw)
        return o

    def dr(self, P, u, n="", **kw):
        X, Y = self.p(P)
        ux, uy = self.d(u)
        o = {"k": "dr", "x": X, "y": Y, "ux": ux, "uy": uy}
        if n:
            o["n"] = n
        o.update(kw)
        return o

    def sg(self, P, Q, **kw):
        (x1, y1), (x2, y2) = self.p(P), self.p(Q)
        return dict({"k": "sg", "x1": x1, "y1": y1, "x2": x2, "y2": y2}, **kw)

    def vecteur(self, P, Q, n="", **kw):
        """Vecteur de la feuille de P à Q (points réels)."""
        (x1, y1), (x2, y2) = self.p(P), self.p(Q)
        return dict({"k": "vec", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "n": n}, **kw)

    def cone(self, P, normale, phi, r=30, n="", **kw):
        X, Y = self.p(P)
        ux, uy = self.d(unit(normale))
        return dict({"k": "cone", "x": X, "y": Y, "ux": ux, "uy": uy, "phi": round(phi, 4), "r": r, "n": n}, **kw)

    def arc(self, P, u1, u2, texte, vers=None, **kw):
        X, Y = self.p(P)
        o = {"k": "arc", "x": X, "y": Y, "u1": list(self.d(unit(u1))), "u2": list(self.d(unit(u2))), "s": texte, "v": 0}
        if vers is not None:
            o["hx"], o["hy"] = self.p(vers)
        o.update(kw)
        return o

    def tx(self, P, s, **kw):
        X, Y = self.p(P)
        return dict({"k": "tx", "x": X, "y": Y, "s": s}, **kw)


class Dynamique:
    """Zone du dynamique : les vecteurs y sont tracés à l'échelle des forces (unités de force par mm de feuille),
    à partir d'un point de départ donné sur la feuille."""

    def __init__(self, x0, y0, echelle):
        self.x0, self.y0, self.e = x0, y0, echelle

    def chaine(self, forces):
        """forces : [(vecteur force réel (Fx, Fy), nom, options)] mis bout à bout ; renvoie les vecteurs de la feuille."""
        out, x, y = [], self.x0, self.y0
        for F, n, kw in forces:
            x2, y2 = x + F[0] / self.e, y - F[1] / self.e
            out.append(dict({"k": "vec", "x1": round(x, 3), "y1": round(y, 3), "x2": round(x2, 3), "y2": round(y2, 3),
                             "n": n}, **kw))
            x, y = x2, y2
        return out


# ============================================================ fond de la planche (SVG, coordonnées de feuille)
def esc(s):
    return html.escape(str(s), quote=True)


def num(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def grille(w, h, pas=5):
    fin = "".join(f"M{x} 0V{h}" for x in range(0, int(w) + 1, pas) if x % 10) + \
          "".join(f"M0 {y}H{w}" for y in range(0, int(h) + 1, pas) if y % 10)
    gros = "".join(f"M{x} 0V{h}" for x in range(0, int(w) + 1, 10)) + "".join(f"M0 {y}H{w}" for y in range(0, int(h) + 1, 10))
    return f'<path d="{fin}"/><path class="g10" d="{gros}"/>'


def cote(a, b, texte, decal=6, fs=3.4, ext=True):
    """Cote entre deux points de la feuille, décalée perpendiculairement de decal (mm)."""
    ux, uy = unit((b[0] - a[0], b[1] - a[1]))
    nx, ny = -uy, ux
    A = (a[0] + nx * decal, a[1] + ny * decal)
    B = (b[0] + nx * decal, b[1] + ny * decal)
    h, w = 2.2, 0.75
    def tete(P, s):
        bx, by = P[0] + s * ux * h, P[1] + s * uy * h
        return (f'<path class="cote-f" d="M{num(P[0])} {num(P[1])}L{num(bx - ny * w)} {num(by + nx * w)}'
                f'L{num(bx + ny * w)} {num(by - nx * w)}Z"/>')
    s = ""
    if ext:
        s += (f'<path class="cote" d="M{num(a[0] + nx * 1)} {num(a[1] + ny * 1)}L{num(A[0] + nx * 1.5)} {num(A[1] + ny * 1.5)}'
              f'M{num(b[0] + nx * 1)} {num(b[1] + ny * 1)}L{num(B[0] + nx * 1.5)} {num(B[1] + ny * 1.5)}"/>')
    s += f'<path class="cote" d="M{num(A[0])} {num(A[1])}L{num(B[0])} {num(B[1])}"/>' + tete(A, 1) + tete(B, -1)
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    ang = math.degrees(math.atan2(uy, ux))
    if ang > 90 or ang < -90:
        ang += 180
    s += (f'<text class="cote-t" x="{num(mx)}" y="{num(my)}" font-size="{fs}" text-anchor="middle" '
          f'transform="rotate({num(ang)} {num(mx)} {num(my)}) translate(0 -1)">{esc(texte)}</text>')
    return s


def texte(P, s, cls="leg", fs=3.6, anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text class="{cls}" x="{num(P[0])}" y="{num(P[1])}" font-size="{fs}" text-anchor="{anchor}"{st}>'
            f"{s}</text>")


def poly(pts, cls="m"):
    return f'<path class="{cls}" d="M' + "L".join(f"{num(x)} {num(y)}" for x, y in pts) + 'Z"/>'


def cercle(P, r, cls="m"):
    return f'<circle class="{cls}" cx="{num(P[0])}" cy="{num(P[1])}" r="{num(r)}"/>'


def ligne(P, Q, cls="tr"):
    return f'<path class="{cls}" d="M{num(P[0])} {num(P[1])}L{num(Q[0])} {num(Q[1])}"/>'


def roue(F, C, r):
    """Roue de rayon réel r, centre réel C : pneu, jante et moyeu."""
    X = F.p(C)
    R = F.l(r)
    return (cercle(X, R, "m2") + cercle(X, R * 0.62, "m") + cercle(X, R * 0.16, "m3") +
            "".join(ligne((X[0] + R * 0.18 * math.cos(a), X[1] + R * 0.18 * math.sin(a)),
                          (X[0] + R * 0.6 * math.cos(a), X[1] + R * 0.6 * math.sin(a)))
                    for a in [i * math.pi / 3 for i in range(6)]))


def sol(F, P, Q, ep=4, hachures=True):
    """Sol (ou trottoir) sous le segment réel PQ, épaisseur ep mm de feuille."""
    A, B = F.p(P), F.p(Q)
    ux, uy = unit((B[0] - A[0], B[1] - A[1]))
    nx, ny = -uy, ux
    if ny < 0:
        nx, ny = -nx, -ny
    pts = [A, B, (B[0] + nx * ep, B[1] + ny * ep), (A[0] + nx * ep, A[1] + ny * ep)]
    s = poly(pts, "sol")
    if hachures:
        L = math.hypot(B[0] - A[0], B[1] - A[1])
        k = 0.0
        while k < L - 1:
            x, y = A[0] + ux * k, A[1] + uy * k
            s += ligne((x, y), (x + ux * 2.2 + nx * ep * 0.9, y + uy * 2.2 + ny * ep * 0.9), "hach")
            k += 3
    return s


# ============================================================ la planche dans la page
OUTILS_BAR = [("dr", "Droite"), ("sg", "Segment"), ("par", "Parallèle"), ("perp", "Perpendiculaire"),
              ("inc", "Inclinée"), ("cone", "Cône"), ("vec", "Vecteur"), ("pt", "Point"), ("dist", "Distance"),
              ("ang", "Angle"), ("tx", "Texte"), ("gom", "Gomme"), ("main", "Main")]
COULEURS = [("#1F5FA8", "bleue"), ("#1B7A43", "verte"), ("#1C2530", "noire")]


def barre(label, forces=None, fonds=None):
    outils = "".join(f'<button type="button" data-pl-tool="{k}" aria-pressed="false">{t}</button>' for k, t in OUTILS_BAR)
    sw = "".join(f'<button type="button" class="sw" data-pl-color="{c}" aria-label="Couleur {n}" '
                 f'aria-pressed="{"true" if i == 0 else "false"}" style="background:{c}"></button>'
                 for i, (c, n) in enumerate(COULEURS))
    ech = ""
    if forces and len(forces["choix"]) > 1:
        opts = "".join(f'<option value="{v}"{" selected" if i == forces.get("def", 0) else ""}>1 mm ↔ {num(v)} '
                       f'{forces["u"]}</option>' for i, v in enumerate(forces["choix"]))
        ech = (f'<span class="sep"></span><span class="tb-group"><span class="tb-lab">Échelle des forces</span>'
               f'<select class="pl-scale" aria-label="Échelle des forces">{opts}</select></span>')
    elif forces:
        ech = (f'<span class="sep"></span><span class="tb-group"><span class="tb-lab">Forces</span>'
               f'<b class="pl-scale-v tb-lab"></b></span>')
    fd = ""
    if fonds:
        opts = "".join(f'<option value="{k}">{esc(t)}</option>' for k, t in fonds)
        fd = (f'<span class="sep"></span><span class="tb-group"><span class="tb-lab">Fond</span>'
              f'<select class="pl-fond" aria-label="Fond de la feuille">{opts}</select></span>')
    return (f'<div class="pl-bar" role="toolbar" aria-label="Outils de construction {esc(label)}">{outils}'
            f'<span class="sep"></span>{sw}{ech}{fd}<span class="sep"></span>'
            '<span class="tb-group"><button type="button" data-pl-zoom="out" aria-label="Réduire le zoom">−</button>'
            '<span class="pl-zoom-v">100 %</span><button type="button" data-pl-zoom="in" aria-label="Agrandir le zoom">+</button>'
            '<button type="button" data-pl-zoom="reset">Ajuster</button></span><span class="sep"></span>'
            '<button type="button" data-pl-act="undo">Annuler</button><button type="button" data-pl-act="redo">Rétablir</button>'
            '<button type="button" data-pl-act="clear">Tout effacer</button><span class="spacer"></span>'
            '<button type="button" data-pl-act="print">Imprimer le document réponse</button>'
            '<button type="button" data-pl-act="full" aria-pressed="false">Plein écran</button></div>')


def scene(pid, w, h, fond, label, avec_grille=True):
    g = grille(w, h) if avec_grille else ""
    return (f'<div class="pl-stage" style="--ratio:{w / h:.3f}"><svg class="pl-svg" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}"><g class="pl-grille">{g}</g><g class="pl-bg">{fond}</g><g class="pl-given"></g>'
            '<g class="pl-demo"></g><g class="pl-usr"></g><g class="pl-corr"></g><g class="pl-prev"></g>'
            '<g class="pl-snap"></g></svg></div>')


RELEVES = ('<details class="pl-releves" open><summary>Relevés de ta construction</summary><table class="t">'
           "<thead><tr><th>Élément</th><th>Longueur</th><th>Valeur</th><th>Direction</th></tr></thead><tbody></tbody>"
           "</table></details>")


def planche_exo(b):
    """Planche d'une question d'exercice (bloc « pl » d'une partie) : barre d'outils, feuille, relevés, validation,
    auto-évaluation et correction. b : id, label, stem, cfg (configuration JS), criteria, why, donnees."""
    pid, label, cfg = b["id"], b["label"], b["cfg"]
    crit = "".join(f'<label class="se-item"><input type="checkbox" data-crit="{i}"><span>{c}</span></label>'
                   for i, c in enumerate(b["criteria"]))
    n = len(b["criteria"])
    donnees = "".join(f"<span>{d}</span>" for d in b.get("donnees", []))
    return f"""
        <div class="pl pl-mode-exo" data-planche="{pid}" id="{pid}">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{b['stem']}</strong></p>
          <p class="pl-consigne small">{b.get('consigne', '')}</p>
          <div class="pl-donnees"><span class="pl-ech">{esc(cfg.get('echTxt', ''))}</span>{donnees}</div>
          {barre(label, cfg.get('forces'))}
          <p class="pl-aide" aria-live="polite"></p>
          {scene(pid, cfg['w'], cfg['h'], b['fond'], 'Feuille de construction ' + label)}
          <p class="pl-lect" aria-live="polite"></p>
          {RELEVES}
          <div class="pl-foot">
            <button type="button" class="btn btn-sketch pl-valider">Valider ma construction</button>
            <label class="pl-corr-toggle"><input type="checkbox"> Superposer la correction</label>
            <span class="pl-statut" aria-live="polite"></span>
          </div>
          <p class="pl-wait" aria-live="polite"></p>
          <div class="selfeval" hidden>
            <p class="se-title">Auto-évaluation — {n} point{'s' if n > 1 else ''}</p>
            <p class="se-lead">Compare ta construction à la correction superposée, puis coche uniquement ce que ta construction comporte réellement.</p>
            {crit}
            <div class="se-foot"><button type="button" class="btn btn-self">Valider mon auto-évaluation</button>
              <span class="se-score" aria-live="polite"></span></div>
            <p class="print-only se-print"></p>
          </div>
          <div class="q-expl" hidden><p class="q-expected"><span>Correction de la construction</span></p>{b['why']}</div>
        </div>"""


def planche_demo(pid, cfg, fond, label, intro=""):
    """Planche de démonstration (cours) : scénarios, étapes, puis « Construire moi-même »."""
    scen = "".join(f'<button type="button" data-pl-scen="{i}" aria-pressed="false">{esc(s["titre"])}</button>'
                   for i, s in enumerate(cfg["scenarios"]))
    return f"""
        <div class="pl pl-mode-demo" data-planche="{pid}" id="{pid}">
          {intro}
          <div class="pl-demo">
            <div class="pl-scen" role="group" aria-label="Cas étudiés">{scen}</div>
            <div class="pl-etapes"><button type="button" class="btn ghost" data-pl-act="prev">◀ Étape précédente</button>
              <span class="pl-etape-n" aria-live="polite"></span>
              <button type="button" class="btn" data-pl-act="next">Étape suivante ▶</button>
              <button type="button" class="btn ghost" data-pl-act="allsteps">Toute la construction</button>
              <button type="button" class="btn ghost" data-pl-act="essai" aria-pressed="false">Construire moi-même</button></div>
            <p class="pl-etape-t" aria-live="polite"></p>
          </div>
          <div class="pl-donnees"><span class="pl-ech">{esc(cfg.get('echTxt', ''))}</span></div>
          {barre(label, cfg.get('forces'))}
          <p class="pl-aide" aria-live="polite"></p>
          {scene(pid, cfg['w'], cfg['h'], fond, label)}
          <p class="pl-lect" aria-live="polite"></p>
          {RELEVES}
        </div>"""


def planche_libre(pid, cfg, fond, label, fonds):
    """Planche de l'atelier : feuille libre, fonds au choix (modèles <template id="pl-fond-…">)."""
    return f"""
        <div class="pl pl-mode-libre" data-planche="{pid}" id="{pid}">
          <div class="pl-donnees"><span class="pl-ech">{esc(cfg.get('echTxt', ''))}</span></div>
          {barre(label, cfg.get('forces'), fonds)}
          <p class="pl-aide" aria-live="polite"></p>
          {scene(pid, cfg['w'], cfg['h'], fond, label)}
          <p class="pl-lect" aria-live="polite"></p>
          {RELEVES}
        </div>"""


def config_js(planches):
    return "<script>window.__PLANCHES__ = " + json.dumps(planches, ensure_ascii=False, separators=(",", ":")) + ";</script>"


def zone(F, pts, n="", pos=None, **kw):
    """Zone polygonale de la planche (points réels), nom placé en pos (point réel)."""
    o = {"k": "poly", "pts": [list(F.p(P)) for P in pts], "n": n}
    if pos is not None:
        o["nx"], o["ny"] = F.p(pos)
    o.update(kw)
    return o


# ============================================================ rendu statique (illustrations hors planche)
def _clip(x, y, ux, uy, w, h):
    t0, t1 = -1e9, 1e9
    for p, u, hi in ((x, ux, w), (y, uy, h)):
        if abs(u) < 1e-12:
            if p < 0 or p > hi:
                return None
            continue
        a, b = (0 - p) / u, (hi - p) / u
        a, b = min(a, b), max(a, b)
        t0, t1 = max(t0, a), min(t1, b)
    if t0 > t1:
        return None
    return (x + t0 * ux, y + t0 * uy), (x + t1 * ux, y + t1 * uy)


def _nom(n, x, y, fs, vecteur=False):
    import re
    m = re.match(r"^([A-Za-zÀ-ÿͰ-Ͽ']+?)(?:_?([0-9].*|_.+))?$", n) or None
    base, sub = (m.group(1), (m.group(2) or "").lstrip("_")) if m else (n, "")
    s = (f'<text class="pl-nom" x="{num(x)}" y="{num(y)}" font-size="{fs}"><tspan font-style="italic">{esc(base)}</tspan>' +
         (f'<tspan font-size="{num(fs * 0.68)}" dy="{num(fs * 0.3)}">{esc(sub)}</tspan>' if sub else "") + "</text>")
    if vecteur:
        w = fs * (0.62 * len(base) + (0.5 * len(sub) + 0.1 if sub else 0))
        ya, x2 = y - fs * 0.92, x + max(fs * 0.75, w * (0.72 if sub else 1))
        s += (f'<path class="pl-fl" d="M{num(x)} {num(ya)}H{num(x2)}m-{num(fs * 0.32)} -{num(fs * 0.17)}'
              f'l{num(fs * 0.32)} {num(fs * 0.17)}l-{num(fs * 0.32)} {num(fs * 0.17)}"/>')
    return s


def _fleche(x1, y1, x2, y2, head):
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    h = min(head, L * 0.5)
    b = h * 0.38
    bx, by = x2 - ux * h, y2 - uy * h
    return (f'<path class="pl-ft" d="M{num(x1)} {num(y1)}L{num(bx)} {num(by)}"/>'
            f'<path class="pl-tete" d="M{num(x2)} {num(y2)}L{num(bx - uy * b)} {num(by + ux * b)}L{num(bx + uy * b)} '
            f'{num(by - ux * b)}Z"/>')


def statique(cfg, fond, label, cls=""):
    """Figure figée : le fond et les éléments donnés de la planche (points, droites, vecteurs), sans outils."""
    w, h, fs = cfg["w"], cfg["h"], cfg.get("fs", 4.2)
    out = []
    for o in cfg.get("given", []):
        st = f' s-{o["st"]}' if o.get("st") else ""
        s = ""
        if o["k"] == "pt":
            r = fs * 0.32
            s = (f'<path class="pl-croix" d="M{num(o["x"] - r)} {num(o["y"] - r)}l{num(2 * r)} {num(2 * r)}m0 -{num(2 * r)}'
                 f'l-{num(2 * r)} {num(2 * r)}"/>')
            if o.get("n"):
                s += _nom(o["n"], o["x"] + (o["dx"] if "dx" in o else fs * 0.45), o["y"] + (o["dy"] if "dy" in o else -fs * 0.35), fs)
        elif o["k"] == "dr":
            c = _clip(o["x"], o["y"], o["ux"], o["uy"], w, h)
            if c:
                s = f'<path class="pl-tr" d="M{num(c[0][0])} {num(c[0][1])}L{num(c[1][0])} {num(c[1][1])}"/>'
        elif o["k"] == "vec":
            s = _fleche(o["x1"], o["y1"], o["x2"], o["y2"], fs * 0.85)
            if o.get("n") and "nx" in o:
                s += _nom(o["n"], o["nx"], o["ny"], fs, True)
        elif o["k"] == "tx":
            s = f'<text class="pl-txt" x="{num(o["x"])}" y="{num(o["y"])}" font-size="{num(o.get("size", fs))}">{esc(o["s"])}</text>'
        out.append(f'<g class="o-giv{st}">{s}</g>')
    return (f'<svg class="pl-svg pl-fixe {cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'<g class="pl-bg">{fond}</g>{"".join(out)}</svg>')
