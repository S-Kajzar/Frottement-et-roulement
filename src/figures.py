"""Figures SVG partagées : formes de véhicules, cône de frottement, illustration de l'accueil.

Les figures du manuel sont des photographies de pages, inexploitables telles quelles (ombres, déformation) : elles
sont redessinées, aux cotes de l'énoncé quand il en donne (les originaux restent dans src/images/originaux).
"""
import math

import construction as C
from construction import Feuille, num


def forme(F, O, u, pts, cls="m"):
    """Polygone décrit dans un repère local (s le long de u, t selon la normale à u), placé en O (réel)."""
    n = (-u[1], u[0])
    reel = [(O[0] + s * u[0] + t * n[0], O[1] + s * u[1] + t * n[1]) for s, t in pts]
    return C.poly([F.p(P) for P in reel], cls)


# ---------- voiture tout-terrain (exercices 6 à 9), repère local : s le long du sol depuis A, t normal au sol
TT_CAISSE = [(-900, 500), (-950, 1150), (-150, 1260), (600, 1320), (820, 1960), (2780, 1960), (2950, 1360),
             (4100, 1300), (4150, 520), (3820, 480), (-560, 480)]
TT_VITRES = [[(900, 1380), (900, 1860), (1780, 1860), (1780, 1380)], [(1900, 1380), (1900, 1860), (2700, 1860),
                                                                       (2850, 1380)]]
TT_R = 450


def voiture_tt(F, A, u, empattement=3300):
    s = forme(F, A, u, TT_CAISSE, "m3")
    for v in TT_VITRES:
        s += forme(F, A, u, v, "vitre")
    n = (-u[1], u[0])
    for s0 in (0, empattement):
        Cc = (A[0] + s0 * u[0] + TT_R * n[0], A[1] + s0 * u[1] + TT_R * n[1])
        s += C.roue(F, Cc, TT_R)
    return s


# ---------- cabriolet (exercices 10 et 11, exemple 1 du cours) : roues en A (arrière) et B (avant)
CAB_CAISSE = [(-900, 330), (-950, 620), (-620, 760), (200, 790), (650, 1010), (980, 1000), (1350, 780),
              (2700, 720), (3140, 560), (3200, 330), (2900, 260), (-650, 260)]
CAB_R = 300


def cabriolet(F, A, empattement=2260):
    u = (1.0, 0.0)
    s = forme(F, A, u, CAB_CAISSE, "m")
    s += forme(F, A, u, [(700, 1000), (980, 990), (1240, 790), (760, 790)], "vitre")
    for x in (0, empattement):
        s += C.roue(F, (A[0] + x, CAB_R), CAB_R)
    return s


# ---------- voiture ancienne (montée de trottoir, cours 2) : roues avant en A (gauche), arrière en C
ANC_CAISSE = [(-620, 520), (-650, 900), (-300, 980), (500, 1000), (700, 1500), (1900, 1520), (2350, 1450),
              (2600, 1080), (3250, 1050), (3300, 520), (2400, 420), (500, 430)]


def voiture_ancienne(F, A, empattement, r):
    s = forme(F, (A[0], 0), (1.0, 0.0), ANC_CAISSE, "m3")
    s += forme(F, (A[0], 0), (1.0, 0.0), [(800, 1060), (1750, 1060), (1850, 1440), (820, 1460)], "vitre")
    for x in (0, empattement):
        s += C.roue(F, (A[0] + x, r), r)
    return s


# ---------- cône de frottement (figure du QCM et du cours)
def cone_plan(w=420, h=240, forces=True):
    """Deux solides en contact en A, plan tangent, normale, cône de demi-angle φ ; trois positions possibles de
    l'action de contact (à l'intérieur, sur, à l'extérieur du cône)."""
    Ax, Ay, R, phi = w / 2, h * 0.62, h * 0.52, 26
    s = (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Cône de frottement de sommet A, d\'axe la normale au '
         f'contact ; trois actions de contact possibles : a à l\'intérieur, b sur le cône, c à l\'extérieur">')
    s += (f'<path d="M20 {Ay + 26}Q{Ax} {Ay - 18} {w - 20} {Ay + 26}L{w - 20} {h}L20 {h}Z" fill="#E4E7EA" '
          'stroke="#59636B"/>'
          f'<path d="M30 {Ay - 30}Q{Ax} {Ay + 16} {w - 30} {Ay - 30}" fill="none" stroke="#59636B" stroke-width="1.5"/>')
    a1, a2 = math.radians(90 - phi), math.radians(90 + phi)
    s += (f'<path d="M{Ax} {Ay}L{Ax + R * math.cos(a1):.1f} {Ay - R * math.sin(a1):.1f}A{R} {R} 0 0 0 '
          f'{Ax + R * math.cos(a2):.1f} {Ay - R * math.sin(a2):.1f}Z" fill="rgba(242,183,5,.25)" stroke="#B26A00" '
          'stroke-dasharray="6 3"/>')
    s += (f'<path d="M{Ax} {Ay}V{Ay - R - 14}" stroke="#46525C" stroke-dasharray="8 3 2 3"/>'
          f'<text x="{Ax + 6}" y="{Ay - R - 6}" font-size="15" font-style="italic" font-weight="700" fill="#1C2530">n</text>'
          f'<path d="M{Ax} {Ay - R * 0.62}A{R * 0.62} {R * 0.62} 0 0 1 {Ax + R * 0.62 * math.cos(a1):.1f} '
          f'{Ay - R * 0.62 * math.sin(a1):.1f}" fill="none" stroke="#B26A00"/>'
          f'<text x="{Ax + 10}" y="{Ay - R * 0.66}" font-size="14" fill="#B26A00" font-weight="700">φ</text>'
          f'<path d="M24 {Ay}H{w - 24}" stroke="#46525C" stroke-dasharray="3 3"/>'
          f'<text x="{w - 26}" y="{Ay - 6}" font-size="13" text-anchor="end" fill="#46525C">plan tangent (t)</text>'
          f'<text x="34" y="{h - 12}" font-size="13" fill="#46525C">solide 0</text>'
          f'<text x="40" y="{Ay - 40}" font-size="13" fill="#46525C">solide 1</text>'
          f'<circle cx="{Ax}" cy="{Ay}" r="3.2" fill="#1C2530"/><text x="{Ax - 16}" y="{Ay + 18}" font-size="15" '
          'font-weight="700" font-style="italic">A</text>')
    if forces:
        for ang, lab, col in ((90 - 10, "a", "#1F5FA8"), (90 - phi, "b", "#1B7A43"), (90 + 48, "c", "#B42318")):
            r = math.radians(ang)
            x2, y2 = Ax + R * 0.92 * math.cos(r), Ay - R * 0.92 * math.sin(r)
            ux, uy = math.cos(r), -math.sin(r)
            hx, hy = x2 - ux * 11, y2 - uy * 11
            s += (f'<path d="M{Ax} {Ay}L{hx:.1f} {hy:.1f}" stroke="{col}" stroke-width="2.6"/>'
                  f'<path d="M{x2:.1f} {y2:.1f}L{hx - uy * 4.5:.1f} {hy + ux * 4.5:.1f}L{hx + uy * 4.5:.1f} '
                  f'{hy - ux * 4.5:.1f}Z" fill="{col}"/>'
                  f'<text x="{x2 + ux * 12 - 4:.1f}" y="{y2 + uy * 12 + 5:.1f}" font-size="16" font-weight="700" '
                  f'fill="{col}">{lab}</text>')
    return s + "</svg>"


# ---------- accueil : la voiture ancienne au pied du trottoir, cône de frottement en D
def hero():
    F = Feuille(150, 80, 40, 66, 40)
    r, h = 360, 200
    A, Cc = (0, r), (2800, r)
    Bx = -math.sqrt(r * r - (r - h) ** 2)
    s = C.poly([F.p((-1500, 0)), F.p((Bx, 0)), F.p((Bx, h)), F.p((-1500, h))], "sol")
    s += C.sol(F, (Bx, 0), (3800, 0), 3)
    s += voiture_ancienne(F, A, 2800, r)
    D, G = (2800, 0), (1600, 700)
    phi = math.degrees(math.atan(0.8))
    Dp = F.p(D)
    R = 46
    for sg in (1, -1):
        a = math.radians(90 + sg * phi)
        s += (f'<path d="M{num(Dp[0])} {num(Dp[1])}L{num(Dp[0] + R * math.cos(a))} {num(Dp[1] - R * math.sin(a))}" '
              'stroke="#B26A00" stroke-width=".5" stroke-dasharray="2 1"/>')
    s += (f'<path d="M{num(Dp[0])} {num(Dp[1])}L{num(Dp[0] + R * math.cos(math.radians(90 + phi)))} '
          f'{num(Dp[1] - R * math.sin(math.radians(90 + phi)))}A{R} {R} 0 0 1 '
          f'{num(Dp[0] + R * math.cos(math.radians(90 - phi)))} {num(Dp[1] - R * math.sin(math.radians(90 - phi)))}Z" '
          'fill="rgba(242,183,5,.22)"/>')
    Gp = F.p(G)
    s += (f'<path d="M{num(Gp[0])} {num(Gp[1])}V{num(Gp[1] + 16)}" stroke="#B42318" stroke-width=".9"/>'
          f'<path d="M{num(Gp[0])} {num(Gp[1] + 19)}l-1.3 -3.4h2.6Z" fill="#B42318"/>'
          f'<text x="{num(Gp[0] + 2)}" y="{num(Gp[1] + 14)}" font-size="5" font-style="italic" font-weight="700" '
          'fill="#B42318">P</text>'
          f'<text x="{num(Dp[0] + 3)}" y="{num(Dp[1] - 3)}" font-size="5" font-style="italic" font-weight="700">D</text>'
          f'<text x="{num(F.p((Bx, h))[0] - 6)}" y="{num(F.p((Bx, h))[1] - 2)}" font-size="5" font-style="italic" '
          'font-weight="700">B</text>')
    return (f'<svg class="pl-svg pl-fixe hero-svg" viewBox="0 0 150 80" role="img" aria-label="Voiture ancienne au pied '
            f'd\'un trottoir : poids P en G, contact B sur le bord du trottoir, cône de frottement en D">'
            f'<g class="pl-bg">{s}</g></svg>')
