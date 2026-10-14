"""Figures SVG partagées : formes de véhicules.

Les figures du manuel sont des photographies de pages, inexploitables telles quelles (ombres, déformation) : elles
sont redessinées, aux cotes de l'énoncé quand il en donne (les originaux restent dans src/images/originaux).
"""
import math

import dessin as C


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
