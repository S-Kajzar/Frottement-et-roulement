"""Outils de dessin des figures (SVG) : repère réel du mécanisme → repère du dessin, cotes, sol, roues, annotations.

Les figures du manuel sont des photographies de pages, inexploitables telles quelles : elles sont redessinées aux
cotes de l'énoncé. Chaque mécanisme est décrit dans son repère réel (x vers la droite, y vers le haut, en millimètres
réels), puis converti dans le repère du dessin (x vers la droite, y vers le bas, en millimètres de dessin) par
Feuille ; les mêmes données servent aux réponses attendues des activités.
"""
import html
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

# ============================================================ le repère du dessin
class Feuille:
    """Repère du dessin : (ox, oy) position (mm du dessin) de l'origine réelle ; k mm réels par mm de dessin (échelle 1:k)."""

    def __init__(self, w, h, ox, oy, k=1.0):
        self.w, self.h, self.ox, self.oy, self.k = w, h, ox, oy, k

    def p(self, P):
        return (round(self.ox + P[0] / self.k, 3), round(self.oy - P[1] / self.k, 3))

    def d(self, u):
        return (round(u[0], 6), round(-u[1], 6))

    def l(self, L):
        """Longueur réelle → longueur sur la feuille."""
        return L / self.k

    # ---------- annotations du dessin (points, droites, vecteurs, textes), rendues par statique() ----------
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

    def tx(self, P, s, **kw):
        X, Y = self.p(P)
        return dict({"k": "tx", "x": X, "y": Y, "s": s}, **kw)



# ============================================================ éléments SVG (coordonnées du dessin)
def esc(s):
    return html.escape(str(s), quote=True)


def num(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")



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

# ============================================================ rendu des annotations
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


def statique(cfg, fond, label, cls="", vb=None):
    """Figure : le fond et ses annotations (points, droites, vecteurs, textes) ; vb = (x, y, w, h) recadre le dessin."""
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
    x0, y0, vw, vh = vb or (0, 0, w, h)
    return (f'<svg class="dessin {cls}" viewBox="{num(x0)} {num(y0)} {num(vw)} {num(vh)}" role="img" aria-label="{esc(label)}">'
            f'<g class="dessin-fond">{fond}</g>{"".join(out)}</svg>')


# ============================================================ style des figures
DESSIN_CSS = """
/* ---------- figures redessinées (src/dessin.py) ---------- */
svg.dessin{display:block; width:100%; height:auto; font-family:var(--f-texte); background:#fff}
.dessin .dessin-fond .m{fill:#F3F1EA; stroke:#59636B; stroke-width:.35}
.dessin .dessin-fond .m2{fill:#E4E7EA; stroke:#59636B; stroke-width:.35}
.dessin .dessin-fond .m3{fill:#FFF3C4; stroke:#59636B; stroke-width:.35}
.dessin .dessin-fond .vitre{fill:#CFE0EE; stroke:#59636B; stroke-width:.3}
.dessin .dessin-fond .noir{fill:#46525C; stroke:none}
.dessin .dessin-fond .sol{fill:#E9DCC6; stroke:#8A7350; stroke-width:.35}
.dessin .dessin-fond .hach{stroke:#8A7350; stroke-width:.25}
.dessin .dessin-fond .ax{stroke:#59636B; stroke-width:.25; stroke-dasharray:4 1.2 .8 1.2; fill:none}
.dessin .dessin-fond .tr{stroke:#59636B; stroke-width:.35; fill:none}
.dessin .dessin-fond .cote{stroke:#2E7D5B; stroke-width:.22; fill:none}
.dessin .dessin-fond .cote-f{fill:#2E7D5B}
.dessin .dessin-fond .cote-t{fill:#2E7D5B; font-weight:600}
.dessin .dessin-fond .rep{fill:#1C2530; font-weight:700}
.dessin .dessin-fond .leg{fill:#46525C}
.dessin g[class^="o-"]{--c:#1C2530; stroke:var(--c); fill:none}
.dessin .o-giv.s-f{--c:#B42318}
.dessin .o-giv.s-n{--c:#46525C}
.dessin .pl-tr{stroke-width:.32}
.dessin .s-n .pl-tr{stroke-dasharray:4 1.2 .8 1.2}
.dessin .pl-ft{stroke-width:.65; stroke-linecap:round}
.dessin .pl-tete{fill:var(--c); stroke:none}
.dessin .pl-croix{stroke-width:.35}
.dessin .pl-nom,.dessin .pl-txt{fill:var(--c); stroke:#fff; stroke-width:.7; paint-order:stroke; font-weight:700}
.dessin .pl-txt{font-weight:600}
.dessin .pl-fl{stroke-width:.3; fill:none}
"""
