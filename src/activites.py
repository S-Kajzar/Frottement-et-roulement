"""Activités tirées des exercices du chapitre « Frottement et roulement » (pages 138 et 139 du manuel).

Chaque exercice devient une activité ; les plus courts sont regroupés (deux ou trois au plus) : QCM 3 et 4 dans
l'activité 1, exercices 7, 8 et 9 (variantes de l'exercice 6) dans l'activité 4. Les exercices à résolution
graphique (5, 6, 12) reçoivent une planche de construction. Toutes les réponses attendues sont calculées ici à
partir des données de l'énoncé ; les réponses du manuel sont vérifiées par tests/correction.test.js.
"""
import math

import construction as C
import figures
import qcm
from construction import Dynamique, Feuille


def fr(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def calc(s):
    return f'<span class="calc">{s}</span>'


def vn(base, sub=""):
    """Nom de vecteur écrit dans le texte : A<sub>3/1</sub> surmonté d'une flèche."""
    return f'<span class="vec">{base}</span>' + (f"<sub>{sub}</sub>" if sub else "")


def nrm(base, sub=""):
    return f"‖{vn(base, sub)}‖"


# ============================================================ correcteurs (moteur Grading du gabarit)
def U(label, *accept):
    return {"label": label, "accept": list(accept)}


U_DAN = U("daN", "dan", "decanewton", "decanewtons")
U_N = U("N", "n", "newton", "newtons")
U_DEG = U("°", "°", "deg", "degre", "degres")
U_MM = U("mm", "mm", "millimetre", "millimetres")
U_NM = U("N·m", "nm", "newtonmetre", "newtonmetres", "newtonsmetres")
U_W = U("W", "w", "watt", "watts")
U_KW = U("kW", "kw", "kilowatt", "kilowatts")


def NUM(v, unit=None, rel=None, tol=None, variants=()):
    g = {"type": "num", "value": round(v, 6)}
    if rel:
        g["relTol"] = rel
    if tol:
        g["absTol"] = tol
    if unit:
        g["unit"] = unit
    if variants:
        g["variants"] = [dict(x, strictUnit=True) for x in variants]
    return g


def DAN(v, rel):
    """Force en daN ; la même valeur écrite en newtons, unité comprise, est acceptée."""
    return NUM(v, U_DAN, rel, variants=[{"value": round(v * 10, 6), "relTol": rel, "unit": U_N}])


def NEWTON(v, rel):
    return NUM(v, U_N, rel, variants=[{"value": round(v / 10, 6), "relTol": rel, "unit": U_DAN}])


def DEG(v, tol):
    return NUM(v, U_DEG, tol=tol)


def YESNO(v):
    return {"type": "yesno", "value": v}


def P(*alts):
    return [a.split("|") for a in alts]


def KW(*motifs, forbid=""):
    g = {"type": "kw", "any": list(motifs)}
    if forbid:
        g["forbid"] = forbid.split("|")
    return g


def Q(stem, hint, grader, expected, why):
    return {"kind": "q", "stem": stem, "hint": hint, "grader": grader, "expected": expected, "why": why}


def HTML(raw):
    return {"kind": "html", "html": raw}


def QBAR(docs, ans="ci-dessous"):
    return {"kind": "qbar", "docs": list(docs), "ans": ans}


def H_UNITE(unite, arrondi=""):
    return (f"{arrondi + ' ' if arrondi else ''}Saisis la valeur <strong>avec son unité</strong> ({unite}) : l'unité vaut "
            "la moitié des points de la question.")


H_LECTURE = ("Lis la valeur sur ta construction (tableau des relevés), à 3 % près. Saisis-la <strong>avec son "
             "unité</strong> (daN).")
H_OUINON = "Commence ta réponse par « oui » ou « non »."


def donnees(*lignes):
    return '<div class="data"><p class="data-title">Données</p><ul>' + "".join(f"<li>{x}</li>" for x in lignes) + "</ul></div>"


# ============================================================ ACTIVITÉ 1 — CÔNES D'ADHÉRENCE ET DE FROTTEMENT (QCM 3 et 4)
FIG_CONE = figures.cone_plan()
PARTS_A1 = [{"title": "Cône d'adhérence et cône de frottement", "minutes": 6, "intro": [
    "<p>Deux solides 0 et 1 sont en contact en A. L'action de contact de 0 sur 1 est schématisée par un vecteur-force "
    f"{vn('A', '0/1')} ; le cône de sommet A, d'axe la normale au contact <i>n</i> et de demi-angle φ, sert à lire "
    "les lois du frottement (cours 2).</p>",
    f'<figure class="fig-ex" style="max-width:460px">{FIG_CONE}<figcaption>Trois positions possibles de l\'action de '
    "contact : a à l'intérieur du cône, b sur le cône, c à l'extérieur.</figcaption></figure>"], "blocks": [
    QBAR(["DT1"]),
    qcm.question("Dans le cas de l'adhérence (µ<sub>s</sub> = f<sub>s</sub> = tan φ<sub>s</sub>), la force de contact "
                 "peut :",
                 [("a", "être située n'importe où à l'intérieur du cône d'adhérence"),
                  ("b", "être située sur le cône d'adhérence"),
                  ("c", "être à l'extérieur du cône d'adhérence")], ["a", "b"],
                 "<p>Tant qu'il y a adhérence, l'action de contact est <b>contenue dans le cône d'adhérence</b> : "
                 "α ≤ φ<sub>s</sub>, soit T<sub>a</sub> ≤ µ<sub>s</sub>·N. Elle est à l'intérieur (α &lt; φ<sub>s</sub>) "
                 "tant qu'on n'est pas à la limite, et <b>sur</b> le cône dans le cas particulier de l'équilibre strict "
                 "(α = φ<sub>s</sub>), juste avant le glissement. Elle n'est jamais à l'extérieur : l'équilibre serait "
                 "impossible.</p>"),
    qcm.question("Dans le cas du frottement (µ = f = tan φ), la force de contact peut :",
                 [("a", "être située n'importe où à l'intérieur du cône de frottement"),
                  ("b", "être située sur le cône de frottement"),
                  ("c", "être située à l'extérieur du cône de frottement")], ["b"],
                 "<p>Quand les surfaces glissent l'une sur l'autre, la force de frottement vaut T = µ·N : l'action de "
                 "contact est toujours <b>sur le cône de frottement</b> (α = φ), du côté opposé à la vitesse de "
                 "glissement.</p>", multi=True),
]}]


# ============================================================ ACTIVITÉ 2 — CLÉ À EXCENTRIQUE (exercice 5)
def _cle():
    F = Feuille(250, 172, 75, 40, 1)
    B, Cc, D = (0.0, 0.0), (110.0, 0.0), (-24.0, 0.0)
    A = (-24 + 4 / math.tan(math.radians(30)), -4.0)
    phi = math.degrees(math.atan(0.15))
    n = C.direction(-30)
    uA = C.direction(-30 - phi)
    I = C.inter(A, uA, Cc, (0, 1))
    uB = C.unit(C.vec(B, I))
    Fv = (0.0, -10.0)
    FA, FB = C.triangle(Fv, uA, uB)
    # fond : corps 2 en forme de larme, écrou 3, manche 1 (bossage, came, poignée moletée)
    r1, r2 = 17.0, 9.0
    ph = math.acos((r1 - r2) / (B[0] - D[0]))
    pts = [(D[0] + r1 * math.cos(ph + (2 * math.pi - 2 * ph) * i / 40), r1 * math.sin(ph + (2 * math.pi - 2 * ph) * i / 40))
           for i in range(41)]
    pts += [(B[0] + r2 * math.cos(-ph + 2 * ph * i / 16), r2 * math.sin(-ph + 2 * ph * i / 16)) for i in range(17)]
    fond = C.poly([F.p(p) for p in pts], "m3")
    Rh = 8 / math.cos(math.radians(30))
    fond += C.poly([F.p((D[0] + Rh * math.cos(math.radians(60 * k)), Rh * math.sin(math.radians(60 * k))))
                    for k in range(6)], "m2")
    fond += C.cercle(F.p(D), 4.2, "m")
    came = [(-18.6, -6.6), (-15.6, -1.4), (-8, 2.6), (0, 7), (6, 4.5), (6, -5), (0, -8.5), (-12, -11.8)]
    fond += C.poly([F.p(p) for p in came], "m")
    fond += C.poly([F.p(p) for p in [(5, 4), (62, 4), (62, -4), (5, -4)]], "m")
    fond += C.poly([F.p(p) for p in [(62, 6.5), (165, 6.5), (165, -6.5), (62, -6.5)]], "m2")
    x = 62.0
    while x < 165:
        for sg in (1, -1):
            x2 = min(165.0, x + 13)
            fond += C.ligne(F.p((x, -6.5 * sg)), F.p((x2, -6.5 * sg + 13 * sg * (x2 - x) / 13)), "hach")
        x += 4
    fond += C.cercle(F.p(B), 7, "m") + C.cercle(F.p(B), 2.6, "noir")
    fond += C.ligne(F.p((-45, 0)), F.p((175, 0)), "ax")
    Dp = F.p(D)
    fond += (f'<path class="tr" d="M{C.num(Dp[0] + 15)} {C.num(Dp[1])}A15 15 0 0 1 '
             f'{C.num(Dp[0] + 15 * math.cos(math.radians(30)))} {C.num(Dp[1] + 15 * math.sin(math.radians(30)))}"/>')
    fond += C.texte((Dp[0] + 17, Dp[1] + 6.5), "30°", "cote-t", 3.4)
    fond += C.cote(F.p(D), F.p(B), "24", 32)
    fond += C.cote(F.p(B), F.p(Cc), "110", 32)
    fond += C.cote(F.p((-40, 0)), F.p((-40, -4)), "", 0, ext=False)
    fond += C.texte(F.p((-47, -3.2)), "4", "cote-t", 3.4)
    fond += C.ligne(F.p((-43, -4)), F.p((A[0] - 2, -4)), "cote")
    for t, P_, Q_ in (("1", (130, 16), (130, 6.5)), ("2", (-2, 22), (-8, 14)), ("3", (-36, 20), (-27, 6))):
        fond += C.ligne(F.p(P_), F.p(Q_), "tr") + C.texte(F.p((P_[0] - 1.2, P_[1] + 1.5)), t, "rep", 4)
    fond += C.texte(F.p((116, 28)), "(10 daN)", "leg", 3.4)
    given = [F.pt(A, "A", dx=-5.2, dy=6.5), F.pt(B, "B", dx=1.8, dy=6.8), F.pt(Cc, "C", dx=1.6, dy=-1.6),
             F.pt(D, "D", dx=-4.6, dy=-2.4), F.dr(A, n, st="n"), F.dr(B, (1, 0), st="n"),
             F.vecteur((110, 22), Cc, "F", st="f", nx=F.p((112, 15))[0], ny=F.p((112, 15))[1]),
             F.tx((A[0] + 31, A[1] - 19), "normale AD", size=3.2)]
    corr = [F.cone(A, n, phi, r=22, n="φ"), F.dr(A, uA), F.dr(Cc, (0, 1)), F.pt(I, "I", dx=1.6, dy=5),
            F.dr(B, uB), F.arc(A, (1, 0), uA, "38,5°", vers=(A[0] + 12, A[1] - 4)),
            F.tx((A[0] + 60, A[1] - 52), "(A3/1)"), F.tx((40, -48), "(B2/1)")]
    corr += Dynamique(20, 92, 1).chaine([(Fv, "F", {}), (FA, "A3/1", {}), (FB, "B2/1", {})])
    cfg = {"w": F.w, "h": F.h, "kL": 1, "given": given, "corr": corr, "outil": "dr",
           "forces": {"u": "daN", "choix": [1], "def": 0},
           "echTxt": "Longueurs à l'échelle 1:1 · forces : 1 mm ↔ 1 daN",
           "titre": "Clé à excentrique — actions en A et B sur le manche (1)"}
    return {"F": F, "cfg": cfg, "fond": fond, "A": A, "I": I, "phi": phi, "FA": FA, "FB": FB, "uA": uA}


CLE = _cle()
CLE_A, CLE_B = math.hypot(*CLE["FA"]), math.hypot(*CLE["FB"])
CLE_AX, CLE_AY = CLE["FA"]
CLE_BX, CLE_BY = CLE["FB"]
CLE_C = 10 * 134 / 100  # daN·mm → N·m


def hero_cle():
    return C.statique(CLE["cfg"], CLE["fond"], "Clé à excentrique : manche 1, corps 2, écrou 3 ; F en C")


PARTS_A2 = [
    {"title": "Actions en A et B : résolution graphique", "minutes": 30, "intro": [
        "<p>La clé à excentrique permet de serrer des écrous ou des vis (3) de dimensions différentes. Le profil en came "
        "du manche (1) est réalisé de façon que la droite AD conserve une direction fixe (30° par rapport au manche), "
        f"quel que soit l'écrou. {vn('F')} (10 daN), perpendiculaire au manche, schématise l'action de l'opérateur ; "
        "les poids sont négligés ; le frottement en A est caractérisé par µ<sub>A</sub> = f<sub>A</sub> = 0,15.</p>",
        donnees(f"{vn('F')} : 10 daN en C, perpendiculaire au manche (vers le bas).",
                "Frottement en A : f<sub>A</sub> = 0,15 ; la normale au contact en A est la droite AD (30° sous le manche).",
                "Le manche (1) est soumis à trois actions : l'opérateur en C, l'écrou (3) en A, le corps (2) en B.",
                "Échelle des forces imposée : 1 mm ↔ 1 daN.")], "blocks": [
        QBAR(["DT1", "DT2"]),
        Q("Calcule l'angle de frottement φ en A.", H_UNITE("°", "Arrondis au centième de degré."),
          DEG(CLE["phi"], 0.06), f"φ = {fr(CLE['phi'], 2)}°",
          f"<p>tan φ = f<sub>A</sub> = 0,15, donc φ = arctan 0,15 = <b>{fr(CLE['phi'], 2)}°</b>. Le cône de frottement en A "
          "a ce demi-angle autour de la normale AD.</p>"),
        {"kind": "pl", "stem": "Isole le manche (1) et construis les actions exercées en A et en B.",
         "consigne": "Méthode des trois forces : les droites d'action sont concourantes, le dynamique est fermé. "
                     "La droite d'action de l'écrou sur le manche est une génératrice du cône de frottement en A ; "
                     "choisis celle qui s'oppose au glissement du manche sur l'écrou au moment du serrage.",
         "cfg": CLE["cfg"], "fond": CLE["fond"], "deps_tout": True,
         "criteria": ["La droite d'action de F (perpendiculaire au manche en C) est tracée.",
                      "Le cône de frottement en A (demi-angle 8,5° autour de la normale AD) est tracé ; la droite "
                      "d'action de A3/1 est sa génératrice inclinée de 38,5° sur le manche.",
                      "Le point de concours I est placé ; la droite d'action de B2/1 passe par B et I.",
                      "Le dynamique est construit à l'échelle : F (10 mm), puis les parallèles aux droites d'action de "
                      "A3/1 et B2/1.",
                      "Les trois vecteurs du dynamique sont orientés bout à bout (F + A3/1 + B2/1 = 0) et nommés."],
         "why": f"<ol><li>Droite d'action de {vn('F')} : la perpendiculaire au manche passant par C.</li>"
                f"<li>Cône de frottement en A : sommet A, axe la normale AD, demi-angle φ = {fr(CLE['phi'], 1)}°. "
                "Au serrage, le manche tourne autour de B et sa came glisse vers le haut sur la face de l'écrou : "
                f"l'action {vn('A', '3/1')} s'incline vers le bas, à 30° + {fr(CLE['phi'], 1)}° = "
                f"{fr(30 + CLE['phi'], 1)}° sous le manche.</li>"
                "<li>Les deux droites se coupent en I, loin sous la clé ; la droite d'action de "
                f"{vn('B', '2/1')} est BI.</li>"
                f"<li>Dynamique : {vn('F')} (10 mm vers le bas), puis une parallèle à la droite d'action de "
                f"{vn('A', '3/1')} à son extrémité et une parallèle à BI à son origine ; le triangle se ferme. "
                f"On lit {nrm('A', '3/1')} ≈ {fr(CLE_A, 1)} daN et {nrm('B', '2/1')} ≈ {fr(CLE_B, 1)} daN.</li></ol>"},
        Q(f"Quelle est la norme de {vn('A', '3/1')}, action de l'écrou sur le manche en A ?", H_LECTURE,
          DAN(CLE_A, 0.03), f"{nrm('A', '3/1')} ≈ {fr(CLE_A, 1)} daN",
          f"<p>Lecture sur le dynamique : le côté parallèle à la droite d'action de {vn('A', '3/1')} mesure environ "
          f"{fr(CLE_A, 1)} mm, soit <b>{fr(CLE_A, 1)} daN</b> à l'échelle 1 mm ↔ 1 daN.</p>"),
        Q(f"Quelle est la norme de {vn('B', '2/1')}, action du corps sur le manche en B ?", H_LECTURE,
          DAN(CLE_B, 0.03), f"{nrm('B', '2/1')} ≈ {fr(CLE_B, 1)} daN",
          f"<p>Le troisième côté du dynamique, parallèle à BI, mesure environ {fr(CLE_B, 1)} mm : "
          f"<b>{fr(CLE_B, 1)} daN</b>. Une petite force F, une grande action en A : c'est l'effet de levier de la "
          "clé (bras de 110 mm contre quelques millimètres).</p>"),
    ]},
    {"title": "Vérification analytique", "minutes": 15, "intro": [
        "<p>On vérifie la construction par le principe fondamental de la statique, dans le repère de la figure : origine "
        "B, x le long du manche vers C, y vers le haut. Le point A est à 4 mm sous l'axe : "
        f"x<sub>A</sub> = −24 + 4 / tan 30° = {fr(CLE['A'][0], 2)} mm, y<sub>A</sub> = −4 mm. "
        f"L'action {vn('A', '3/1')} est inclinée de {fr(30 + CLE['phi'], 2)}° sous l'axe x.</p>"], "blocks": [
        Q(f"Calcule A<sub>x</sub>, composante de {vn('A', '3/1')} sur x.",
          H_UNITE("daN", "Composante algébrique, au dixième."), DAN(CLE_AX, 0.01),
          f"A<sub>x</sub> = {fr(CLE_AX, 1)} daN",
          f"<p>Avec A<sub>y</sub> = −A<sub>x</sub> × tan {fr(30 + CLE['phi'], 2)}° = −{fr(math.tan(math.radians(30 + CLE['phi'])), 4)} "
          "A<sub>x</sub>, le moment en B des trois actions est nul :</p><p>"
          + calc(f"−10 × 110 + x<sub>A</sub>·A<sub>y</sub> − y<sub>A</sub>·A<sub>x</sub> = 0") + "</p><p>"
          + calc(f"−1 100 + ({fr(CLE['A'][0], 2)}) × (−{fr(math.tan(math.radians(30 + CLE['phi'])), 4)} A<sub>x</sub>) + 4 A<sub>x</sub> = 0")
          + f"</p><p>soit {fr(-CLE['A'][0] * math.tan(math.radians(30 + CLE['phi'])) + 4, 2)} A<sub>x</sub> = 1 100 et "
          f"<b>A<sub>x</sub> = {fr(CLE_AX, 1)} daN</b> (réponse du manuel : 62,5 daN).</p>"),
        Q(f"Calcule A<sub>y</sub>, composante de {vn('A', '3/1')} sur y.",
          H_UNITE("daN", "Composante algébrique (avec son signe), au dixième."), DAN(CLE_AY, 0.01),
          f"A<sub>y</sub> = {fr(CLE_AY, 1)} daN",
          f"<p>A<sub>y</sub> = −{fr(math.tan(math.radians(30 + CLE['phi'])), 4)} × {fr(CLE_AX, 2)} = "
          f"<b>{fr(CLE_AY, 1)} daN</b> : l'écrou pousse le manche vers le bas. Le manuel donne « A<sub>y</sub> = 49,8 » "
          "sans signe : c'est la valeur absolue.</p>"),
        Q(f"Calcule B<sub>x</sub>, composante de {vn('B', '2/1')} sur x.",
          H_UNITE("daN", "Composante algébrique, au dixième."), DAN(CLE_BX, 0.01),
          f"B<sub>x</sub> = {fr(CLE_BX, 1)} daN",
          f"<p>Somme des forces sur x : A<sub>x</sub> + B<sub>x</sub> = 0, d'où <b>B<sub>x</sub> = {fr(CLE_BX, 1)} daN</b>.</p>"),
        Q(f"Calcule B<sub>y</sub>, composante de {vn('B', '2/1')} sur y.",
          H_UNITE("daN", "Composante algébrique, au dixième."), DAN(CLE_BY, 0.01),
          f"B<sub>y</sub> = {fr(CLE_BY, 1)} daN",
          f"<p>Somme des forces sur y : A<sub>y</sub> + B<sub>y</sub> − 10 = 0, d'où B<sub>y</sub> = 10 + "
          f"{fr(-CLE_AY, 1)} = <b>{fr(CLE_BY, 1)} daN</b>. On retrouve {nrm('B', '2/1')} = "
          f"√({fr(CLE_BX, 1)}² + {fr(CLE_BY, 1)}²) = {fr(CLE_B, 1)} daN, comme sur le dynamique.</p>"),
    ]},
    {"title": "Couple de serrage", "minutes": 8, "intro": [
        "<p>On isole la clé entière (manche 1 et corps 2). L'écrou, de centre D, oppose un couple résistant au "
        f"serrage ; seule l'action {vn('F')} de l'opérateur vient de l'extérieur.</p>"], "blocks": [
        Q("Calcule le couple de serrage C exercé sur l'écrou.", H_UNITE("N·m", "Au dixième."),
          NUM(CLE_C, U_NM, 0.01), f"C = {fr(CLE_C, 1)} N·m",
          "<p>La clé est en équilibre : le couple de serrage équilibre le moment de F autour du centre D de "
          "l'écrou. Le bras de levier de F par rapport à D vaut 24 + 110 = 134 mm :</p><p>"
          + calc("C = F × 134 = 10 daN × 134 mm = 1 340 daN·mm = 13 400 N·mm") +
          f"</p><p><b>C = {fr(CLE_C, 1)} N·m</b>. Le frottement en A ne change pas ce couple, il change seulement la "
          "façon dont l'écrou est saisi.</p>"),
    ]},
]


# ============================================================ ACTIVITÉ 3 — VOITURE À L'ARRÊT DANS UNE PENTE (exercice 6)
PENTE = 0.20
TH = math.atan(PENTE)
XS = (math.cos(TH), -math.sin(TH))   # le long de la pente, vers le bas (de A vers B)
YS = (math.sin(TH), math.cos(TH))    # normale à la pente
P6 = 3000.0
FS6 = 0.6
L_AG, L_GB, H_G = 2000.0, 1300.0, 900.0


def pente_actions(a=L_AG, b=L_GB, hg=H_G, th=TH, P=P6):
    """Voiture freinée en A seulement (roue libre en B) : N_A, T_A (vers le haut de la pente), N_B."""
    Pn, Pt = P * math.cos(th), P * math.sin(th)
    NB = (Pn * a + Pt * hg) / (a + b)
    return Pn - NB, Pt, NB


NA6, TA6, NB6 = pente_actions()
A6 = math.hypot(NA6, TA6)
ALPHA6 = math.degrees(math.atan(TA6 / NA6))
PHIS6 = math.degrees(math.atan(FS6))
PENTE_LIM = FS6 * L_GB / (L_AG + L_GB + FS6 * H_G)          # tan θ limite
A_LIM7 = (L_AG + L_GB) - (P6 * math.sin(TH) / FS6 * (L_AG + L_GB) + P6 * math.sin(TH) * H_G) / (P6 * math.cos(TH))


def _pente():
    F = Feuille(215, 185, 30, 50, 50)
    A = (0.0, 0.0)
    B = (3300 * XS[0], 3300 * XS[1])
    G = (L_AG * XS[0] + H_G * YS[0], L_AG * XS[1] + H_G * YS[1])
    I = C.inter(G, (0, 1), B, YS)
    uA = C.unit(C.vec(A, I))
    Pv = (0.0, -P6)
    FB, FA = C.triangle(Pv, YS, uA)
    def loc(s, t):
        return (s * XS[0] + t * YS[0], s * XS[1] + t * YS[1])
    fond = C.sol(F, loc(-1300, 0), loc(4700, 0), 4)
    fond += figures.voiture_tt(F, A, XS)
    fond += C.ligne(F.p(G), F.p(loc(4550, H_G)), "ax")
    fond += C.cote(F.p(loc(0, 2150)), F.p(loc(L_AG, 2150)), "a = 2 000", 0, ext=False)
    fond += C.cote(F.p(loc(L_AG, 2150)), F.p(loc(3300, 2150)), "1 300", 0, ext=False)
    fond += C.ligne(F.p(A), F.p(loc(0, 2250)), "cote") + C.ligne(F.p(G), F.p(loc(L_AG, 2250)), "cote")
    fond += C.ligne(F.p(B), F.p(loc(3300, 2250)), "cote")
    fond += C.cote(F.p(loc(4450, 0)), F.p(loc(4450, H_G)), "900", 0, ext=False)
    fond += C.texte(F.p(loc(1450, -520)), "pente de 20 %", "leg", 3.4)
    fond += C.texte(F.p((G[0] + 120, G[1] - 700)), "(3 000 daN)", "leg", 3.2)
    fond += C.texte(F.p(loc(4300, 2000)), "1", "rep", 4) + C.ligne(F.p(loc(4250, 1950)), F.p(loc(3900, 1400)), "tr")
    fond += C.texte(F.p(loc(4700, -350)), "0", "rep", 4)
    Gp = F.p(G)
    given = [F.pt(A, "A", dx=-5.5, dy=5.5), F.pt(B, "B", dx=-2, dy=6.5), F.pt(G, "G", dx=1.6, dy=-1.8),
             F.dr(A, XS, st="n"), {"k": "vec", "x1": Gp[0], "y1": Gp[1], "x2": Gp[0], "y2": Gp[1] + 22, "n": "P",
                                  "st": "f", "nx": Gp[0] - 6, "ny": Gp[1] + 16}]
    corr = [F.dr(B, YS), F.dr(G, (0, 1)), F.pt(I, "I", dx=1.6, dy=-1.5), F.dr(A, uA),
            F.cone(A, YS, PHIS6, r=26, n="φs", une=True), F.arc(A, YS, uA, f"α = {fr(ALPHA6, 1)}°", vers=I)]
    corr += Dynamique(160, 22, 25).chaine([(Pv, "P", {}), (FB, "B0/1", {}), (FA, "A0/1", {})])
    cfg = {"w": F.w, "h": F.h, "kL": 50, "given": given, "corr": corr, "outil": "perp",
           "forces": {"u": "daN", "choix": [25], "def": 0},
           "echTxt": "Longueurs à l'échelle 1:50 · forces : 1 mm ↔ 25 daN",
           "titre": "Voiture à l'arrêt dans une pente de 20 % — actions en A et B"}
    return {"cfg": cfg, "fond": fond, "I": I, "FA": FA, "FB": FB}


PENTE_PL = _pente()


def hero_pente():
    return C.statique(PENTE_PL["cfg"], PENTE_PL["fond"], "Voiture à l'arrêt dans une pente de 20 % : roues en A et B, "
                      "poids P en G")


PARTS_A3 = [
    {"title": "Équilibre de la voiture : résolution graphique", "minutes": 30, "intro": [
        "<p>Une voiture est à l'arrêt dans une pente de 20 % ; le frein à main actionné agit sur les roues avant (en A), "
        f"les roues arrière sont en roue libre (en B). {vn('P')} (3 000 daN) schématise le poids du véhicule ; les "
        "actions exercées sur les roues en A et B sont schématisées par des vecteurs-forces passant par ces mêmes "
        "points. Le frottement en A est caractérisé par µ<sub>A</sub> = f<sub>A</sub> = 0,6.</p>",
        donnees("Pente de 20 % : la route monte de 20 m pour 100 m parcourus à l'horizontale (tan θ = 0,20).",
                "G est à 2 000 mm de A et 1 300 mm de B le long de la pente, à 900 mm au-dessus d'elle.",
                f"{vn('P')} = 3 000 daN ; en A et B : µ<sub>s</sub> = f<sub>s</sub> = tan φ<sub>s</sub> = 0,6.",
                "Roue libre en B : pas de force tangentielle, l'action du sol est normale à la pente.",
                "Échelles imposées : longueurs 1:50, forces 1 mm ↔ 25 daN.")], "blocks": [
        QBAR(["DT1", "DT2"]),
        Q("Calcule l'angle d'adhérence φ<sub>s</sub> en A.", H_UNITE("°", "Au centième de degré."),
          DEG(PHIS6, 0.1), f"φ<sub>s</sub> = {fr(PHIS6, 2)}°",
          f"<p>tan φ<sub>s</sub> = 0,6, donc φ<sub>s</sub> = arctan 0,6 = <b>{fr(PHIS6, 2)}°</b>.</p>"),
        {"kind": "pl", "stem": "Isole la voiture (1) et construis les actions exercées par le sol en A et en B.",
         "consigne": "La voiture est soumise à trois forces : P, B0/1 (direction connue) et A0/1. Trouve leur point "
                     "de concours, puis compare la direction de A0/1 au cône d'adhérence en A.",
         "cfg": PENTE_PL["cfg"], "fond": PENTE_PL["fond"],
         "criteria": ["La droite d'action de B0/1, perpendiculaire à la pente en B (roue libre), est tracée.",
                      "La verticale passant par G (droite d'action de P) est tracée et le point de concours I est placé.",
                      "La droite d'action de A0/1 passe par A et I.",
                      "Le cône d'adhérence en A (demi-angle 31° autour de la normale à la pente) est tracé et comparé "
                      "à la droite AI.",
                      "Le dynamique est fermé à l'échelle : P (120 mm), puis les parallèles à BI et à AI."],
         "why": "<ol><li>Roue libre en B : l'action du sol est normale à la pente, sa droite d'action est la "
                "perpendiculaire à la pente en B.</li><li>Elle coupe la verticale de G en I, à plus de 6 m sous la "
                f"route : la droite d'action de {vn('A', '0/1')} est AI.</li><li>Le cône d'adhérence en A a pour "
                f"demi-angle φ<sub>s</sub> = {fr(PHIS6, 1)}° ; AI fait α = {fr(ALPHA6, 1)}° avec la normale : elle est "
                "<b>dans le cône</b>, de justesse.</li><li>Dynamique : P = 3 000 daN, soit 120 mm ; on ferme le "
                f"triangle avec les parallèles à BI et AI, et on lit {nrm('A', '0/1')} ≈ {fr(A6, 0)} daN, "
                f"{nrm('B', '0/1')} ≈ {fr(NB6, 0)} daN.</li></ol>"},
        Q(f"Quel angle α la droite d'action de {vn('A', '0/1')} fait-elle avec la normale à la pente en A ?",
          H_UNITE("°", "Lis l'angle sur ta construction, au dixième de degré (à 0,3° près)."), DEG(ALPHA6, 0.3),
          f"α = {fr(ALPHA6, 1)}°",
          f"<p>Mesure de l'angle entre AI et la normale en A : α ≈ <b>{fr(ALPHA6, 1)}°</b>. Par le calcul : "
          f"tan α = T<sub>A</sub> / N<sub>A</sub> = {fr(TA6, 1)} / {fr(NA6, 1)} = {fr(TA6 / NA6, 3)}.</p>"),
        Q("L'équilibre de la voiture est-il possible ?", H_OUINON, YESNO(True), "Oui",
          f"<p>α = {fr(ALPHA6, 1)}° &lt; φ<sub>s</sub> = {fr(PHIS6, 1)}° : {vn('A', '0/1')} est à l'intérieur du cône "
          f"d'adhérence, la voiture tient. De justesse : T<sub>A</sub> / N<sub>A</sub> = {fr(TA6 / NA6, 3)}, à peine "
          "moins que 0,6.</p>"),
        Q(f"Quelle est la norme de {vn('A', '0/1')} ?", H_LECTURE, DAN(A6, 0.03), f"{nrm('A', '0/1')} ≈ {fr(A6, 0)} daN",
          f"<p>Lecture sur le dynamique : environ {fr(A6 / 25, 1)} mm, soit <b>{fr(A6, 0)} daN</b>. Ses composantes : "
          f"N<sub>A</sub> = {fr(NA6, 1)} daN (normale) et T<sub>A</sub> = {fr(TA6, 1)} daN (vers le haut de la pente).</p>"),
        Q(f"Quelle est la norme de {vn('B', '0/1')} ?", H_LECTURE, DAN(NB6, 0.03), f"{nrm('B', '0/1')} ≈ {fr(NB6, 0)} daN",
          f"<p>Lecture : environ {fr(NB6 / 25, 1)} mm, soit <b>{fr(NB6, 0)} daN</b>. Par le calcul (moments en A) : "
          f"N<sub>B</sub> × 3 300 = P cos θ × 2 000 + P sin θ × 900, d'où N<sub>B</sub> = {fr(NB6, 1)} daN.</p>"),
    ]},
    {"title": "Pente limite", "minutes": 15, "intro": [
        "<p>On augmente la pente ; le frein agit toujours sur les seules roues avant. On cherche la pente à partir de "
        "laquelle la voiture glisse.</p>"], "blocks": [
        Q("À partir de quelle pente y a-t-il glissement du véhicule ?",
          "Donne la pente en %, au dixième, <strong>sans unité</strong>.", NUM(PENTE_LIM * 100, tol=0.15),
          f"pente ≈ {fr(PENTE_LIM * 100, 1)} %",
          "<p>Le glissement commence quand T<sub>A</sub> = µ<sub>s</sub>·N<sub>A</sub> (équilibre strict : AI sur le "
          "cône). Avec θ l'angle de la pente :</p><p>"
          + calc("T<sub>A</sub> = P sin θ ; N<sub>A</sub> = P (1 300 cos θ − 900 sin θ) / 3 300") + "</p><p>"
          + calc("3 300 sin θ = 0,6 (1 300 cos θ − 900 sin θ)") + " d'où "
          + calc("tan θ = 0,6 × 1 300 / (3 300 + 0,6 × 900) = 780 / 3 840") +
          f"</p><p>tan θ = {fr(PENTE_LIM, 4)} : <b>la voiture glisse à partir d'une pente de {fr(PENTE_LIM * 100, 1)} %</b> "
          f"(θ = {fr(math.degrees(math.atan(PENTE_LIM)), 2)}°). À 20 %, elle est tout près de la limite.</p>"),
    ]},
]


# ============================================================ ACTIVITÉ 4 — VARIANTES : EXERCICES 7, 8 ET 9
NB8, TB8, NA8 = NB6, TA6, NA6  # frein sur les roues arrière : mêmes composantes normales, T en B
B8 = math.hypot(NB8, TB8)
XG9 = L_AG * math.cos(TH) + H_G * math.sin(TH)
XB9 = (L_AG + L_GB) * math.cos(TH)
B9 = P6 * XG9 / XB9
A9 = P6 - B9

PARTS_A4 = [
    {"title": "Exercice 7 : position limite du centre de gravité", "minutes": 10, "intro": [
        "<p>On reprend les données de l'exercice 6 (activité 3) : pente de 20 %, frein à main sur les roues avant (A), "
        "roue libre en B, P = 3 000 daN, f<sub>s</sub> = 0,6, G à 900 mm au-dessus de la pente. La distance AB = "
        "3 300 mm ne change pas ; on fait varier la distance a = AG mesurée le long de la pente.</p>",
        f'<figure class="fig-ex" style="max-width:520px">{hero_pente()}<figcaption>Voiture à l\'arrêt dans une '
        "pente de 20 % (exercice 6).</figcaption></figure>"], "blocks": [
        QBAR(["DT1"]),
        Q("À partir de quelle valeur de a y a-t-il glissement ?", H_UNITE("mm", "À 5 mm près."),
          NUM(A_LIM7, U_MM, tol=5), f"a ≈ {fr(A_LIM7, 0)} mm",
          "<p>Plus G s'éloigne de A, moins la roue avant freinée est chargée : N<sub>A</sub> diminue alors que "
          "T<sub>A</sub> = P sin θ reste le même. Glissement quand T<sub>A</sub> = 0,6 N<sub>A</sub> :</p><p>"
          + calc("N<sub>A</sub> = [P cos θ (3 300 − a) − P sin θ × 900] / 3 300") + "</p><p>"
          + calc(f"{fr(TA6, 1)} = 0,6 × [{fr(P6 * math.cos(TH), 1)} (3 300 − a) − {fr(TA6, 1)} × 900] / 3 300") +
          f"</p><p><b>a = {fr(A_LIM7, 0)} mm</b> (réponse du manuel : 2 020 mm). Avec a = 2 000 mm, la voiture est à "
          "20 mm de la limite.</p>"),
    ]},
    {"title": "Exercice 8 : frein à main sur les roues arrière", "minutes": 12, "intro": [
        "<p>On reprend l'exercice 6 avec le frein à main agissant sur les roues arrière (en B) ; les roues avant (A) "
        "sont en roue libre.</p>"], "blocks": [
        Q("Calcule N<sub>B</sub>, composante normale de l'action du sol en B.", H_UNITE("daN", "Au dixième."),
          DAN(NB8, 0.005), f"N<sub>B</sub> = {fr(NB8, 1)} daN",
          "<p>Les moments en A ne dépendent pas de la roue freinée : N<sub>B</sub> × 3 300 = P cos θ × 2 000 + "
          f"P sin θ × 900, soit <b>N<sub>B</sub> = {fr(NB8, 1)} daN</b> (manuel : 1 942,9).</p>"),
        Q("Calcule T<sub>B</sub>, composante tangentielle de l'action du sol en B.", H_UNITE("daN", "Au dixième."),
          DAN(TB8, 0.005), f"T<sub>B</sub> = {fr(TB8, 1)} daN",
          f"<p>Roue libre en A : toute la retenue vient de B, T<sub>B</sub> = P sin θ = 3 000 × sin {fr(math.degrees(TH), 2)}° "
          f"= <b>{fr(TB8, 1)} daN</b>.</p>"),
        Q("Y a-t-il glissement en B ?", H_OUINON, YESNO(False), "Non",
          f"<p>T<sub>B</sub> / N<sub>B</sub> = {fr(TB8 / NB8, 3)} &lt; 0,6 : l'action en B reste dans le cône "
          "d'adhérence, il n'y a pas glissement. Freiner les roues arrière, plus chargées en descente vers B, "
          "laisse une bonne marge.</p>"),
        Q(f"Calcule la norme de {vn('B', '0/1')}.", H_UNITE("daN", "Au dixième."), DAN(B8, 0.005),
          f"{nrm('B', '0/1')} = {fr(B8, 1)} daN",
          f"<p>{nrm('B', '0/1')} = √(N<sub>B</sub>² + T<sub>B</sub>²) = √({fr(NB8, 1)}² + {fr(TB8, 1)}²) = "
          f"<b>{fr(B8, 1)} daN</b> (manuel : 2 030,4).</p>"),
        Q(f"Calcule la norme de {vn('A', '0/1')}.", H_UNITE("daN", "Au dixième."), DAN(NA8, 0.005),
          f"{nrm('A', '0/1')} = {fr(NA8, 1)} daN",
          f"<p>Roue libre en A : {vn('A', '0/1')} est normale à la pente, {nrm('A', '0/1')} = N<sub>A</sub> = "
          f"P cos θ − N<sub>B</sub> = <b>{fr(NA8, 1)} daN</b> (manuel : 998,4).</p>"),
    ]},
    {"title": "Exercice 9 : frein à pied sur les quatre roues", "minutes": 10, "intro": [
        "<p>On reprend l'exercice 6 avec le frein à pied, qui agit sur les quatre roues. Il y a alors une infinité de "
        "solutions ; on retient celle où les actions en A et B ont la même inclinaison (α<sub>A</sub> = "
        "α<sub>B</sub>).</p>"], "blocks": [
        Q(f"Quelle est alors la direction de {vn('A', '0/1')} et de {vn('B', '0/1')} ?",
          "Réponse courte, en toutes lettres.",
          KW(P("vertical|verticale|verticales|verticalement"), P("parallele|paralleles", "p|poids"),
             forbid="horizontal|horizontale|normale|perpendiculaire"),
          "Verticale : les trois forces sont parallèles à P",
          "<p>Deux droites d'action également inclinées ne peuvent couper la verticale de G en un même point que si "
          f"elles lui sont parallèles : les trois forces sont <b>parallèles à {vn('P')}</b>, donc verticales. Chacune "
          f"fait avec la normale l'angle de la pente, {fr(math.degrees(TH), 1)}° &lt; φ<sub>s</sub> : pas de "
          "glissement.</p>"),
        Q(f"Calcule la norme de {vn('B', '0/1')}.", H_UNITE("daN", "Au dixième."), DAN(B9, 0.005),
          f"{nrm('B', '0/1')} = {fr(B9, 1)} daN",
          "<p>Trois forces parallèles : on écrit les moments en A avec les distances <b>horizontales</b>. G est à "
          f"2 000 cos θ + 900 sin θ = {fr(XG9, 1)} mm de A, B à 3 300 cos θ = {fr(XB9, 1)} mm :</p><p>"
          + calc(f"B<sub>0/1</sub> = 3 000 × {fr(XG9, 1)} / {fr(XB9, 1)}") +
          f" = <b>{fr(B9, 1)} daN</b> (manuel : 1 981,8).</p>"),
        Q(f"Calcule la norme de {vn('A', '0/1')}.", H_UNITE("daN", "Au dixième."), DAN(A9, 0.005),
          f"{nrm('A', '0/1')} = {fr(A9, 1)} daN",
          f"<p>A<sub>0/1</sub> = P − B<sub>0/1</sub> = 3 000 − {fr(B9, 1)} = <b>{fr(A9, 1)} daN</b> (manuel : 1 018,2).</p>"),
    ]},
]


# ============================================================ ACTIVITÉS 5 ET 6 — VOITURE SUR ROUTE MOUILLÉE (exercices 10 et 11)
P10, FAIR, H_AIR, L_A, L_B, F10 = 10790.0, 500.0, 620.0, 1260.0, 1000.0, 0.1
NB10 = (P10 * L_A - FAIR * H_AIR) / (L_A + L_B)
NA10 = P10 - NB10
FRRA, FRRB = 57.0, 72.0
T11 = FAIR + FRRA + FRRB
V90 = 90 / 3.6


def fig_route(roulement=False):
    """Figure 33 du manuel, redessinée : cabriolet à vitesse constante, actions du sol, résistance de l'air."""
    F = Feuille(205, 74, 42, 60, 25)
    A, B, G = (0.0, 0.0), (L_A + L_B, 0.0), (L_A, 520.0)
    s = C.sol(F, (-1300, 0), (4000, 0), 3) + figures.cabriolet(F, A, L_A + L_B)
    def fl(P_, Q_, t, pos, col="#B42318"):
        p, q = F.p(P_), F.p(Q_)
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
        hx, hy = q[0] - ux * 2.6, q[1] - uy * 2.6
        return (f'<path d="M{C.num(p[0])} {C.num(p[1])}L{C.num(hx)} {C.num(hy)}" stroke="{col}" stroke-width=".7"/>'
                f'<path d="M{C.num(q[0])} {C.num(q[1])}L{C.num(hx - uy)} {C.num(hy + ux)}L{C.num(hx + uy)} {C.num(hy - ux)}Z" '
                f'fill="{col}"/><text x="{C.num(F.p(pos)[0])}" y="{C.num(F.p(pos)[1])}" font-size="3.6" fill="{col}" '
                f'font-weight="700">{t}</text>')
    s += fl(G, (L_A, -380), "P", (L_A + 60, -260)) + C.texte(F.p((L_A - 900, -260)), "(10 790 N)", "leg", 3.2)
    s += fl((0, -520), A, "N<tspan font-size=\"2.6\" dy=\".9\">A</tspan>", (-330, -420))
    s += fl((B[0], -520), B, "N<tspan font-size=\"2.6\" dy=\".9\">B</tspan>", (B[0] + 90, -420))
    s += fl(B, (B[0] + 650, 0), "T<tspan font-size=\"2.6\" dy=\".9\">B</tspan>", (B[0] + 380, 120))
    s += fl((3900, H_AIR), (3230, H_AIR), "F<tspan font-size=\"2.6\" dy=\".9\">air</tspan>", (3420, H_AIR + 90))
    s += C.texte(F.p((3380, H_AIR - 230)), "(500 N)", "leg", 3.2)
    if roulement:
        s += fl(A, (-650, 0), "F<tspan font-size=\"2.6\" dy=\".9\">rrA</tspan>", (-900, 120), "#B26A00")
        s += fl((B[0] - 40, 0), (B[0] - 690, 0), "F<tspan font-size=\"2.6\" dy=\".9\">rrB</tspan>", (B[0] - 900, 120),
                "#B26A00")
    s += C.cote(F.p((0, -700)), F.p((L_A, -700)), "1 260", 0, ext=False)
    s += C.cote(F.p((L_A, -700)), F.p((B[0], -700)), "1 000", 0, ext=False)
    s += C.ligne(F.p((0, 0)), F.p((0, -780)), "cote") + C.ligne(F.p((B[0], 0)), F.p((B[0], -780)), "cote")
    s += C.ligne(F.p((L_A, -380)), F.p((L_A, -780)), "cote")
    s += C.cote(F.p((4150, 0)), F.p((4150, 520)), "520", 0, ext=False)
    s += C.cote(F.p((4150, 520)), F.p((4150, H_AIR)), "100", 0, ext=False)
    s += C.ligne(F.p(G), F.p((4250, 520)), "ax") + C.ligne(F.p((3900, H_AIR)), F.p((4250, H_AIR)), "cote")
    s += C.texte(F.p((L_A - 160, 610)), "G", "rep", 3.8) + C.cercle(F.p(G), 0.7, "noir")
    s += C.texte(F.p((-90, -230)), "A", "rep", 3.8) + C.texte(F.p((B[0] - 230, -230)), "B", "rep", 3.8)
    s += C.texte(F.p((900, 1550)), "vitesse constante de 90 km/h →", "leg", 3.4)
    lab = ("Cabriolet roulant à vitesse constante : poids P en G, actions normales N_A et N_B, force T_B à l'avant, "
           "résistance de l'air F_air" + (", résistances au roulement F_rrA et F_rrB" if roulement else ""))
    return f'<svg class="pl-svg pl-fixe" viewBox="0 0 {F.w} {F.h}" role="img" aria-label="{lab}"><g class="pl-bg">{s}</g></svg>'


PARTS_A5 = [
    {"title": "Actions du sol sur les roues", "minutes": 20, "intro": [
        f"<p>La voiture de poids {vn('P')} (10 790 N en G) roule à 90 km/h sur une route horizontale et supporte une "
        f"action {vn('F', 'air')} de 500 N, horizontale, due à la résistance de l'air. Du fait du mauvais temps, le "
        "coefficient d'adhérence entre pneus et sol passe de µ<sub>s</sub> = f<sub>s</sub> = tan φ<sub>s</sub> = 0,6 "
        "à 0,1. Les roues avant (B) sont motrices, les roues arrière (A) porteuses.</p>",
        f'<figure class="fig-ex" style="max-width:640px">{fig_route()}<figcaption>Automobile à vitesse constante sur '
        "route mouillée (dimensions en mm).</figcaption></figure>",
        donnees("Vitesse constante : la voiture est en équilibre (principe fondamental de la statique).",
                f"{vn('F', 'air')} = 500 N, horizontale, à 620 mm du sol (100 mm au-dessus de G).",
                "Roues arrière porteuses : on néglige ici leur résistance au roulement (elle est prise en compte dans "
                "l'activité 6).")], "blocks": [
        QBAR(["DT1"]),
        Q("Calcule N<sub>B</sub>, action normale du sol sur les roues avant.", H_UNITE("N", "Au dixième."),
          NEWTON(NB10, 0.003), f"N<sub>B</sub> = {fr(NB10, 1)} N",
          "<p>Moments en A (les forces au sol ne donnent pas de moment en A) :</p><p>"
          + calc("N<sub>B</sub> × 2 260 − 10 790 × 1 260 + 500 × 620 = 0") +
          f"</p><p>La résistance de l'air, appliquée haut, déleste l'avant : <b>N<sub>B</sub> = {fr(NB10, 1)} N</b>.</p>"),
        Q("Calcule T<sub>B</sub>, action tangentielle du sol sur les roues avant motrices.", H_UNITE("N"),
          NEWTON(FAIR, 0.003), "T<sub>B</sub> = 500 N",
          "<p>Somme des forces horizontales : T<sub>B</sub> − F<sub>air</sub> = 0. Les roues motrices doivent "
          "« pousser » sur le sol autant que l'air retient la voiture : <b>T<sub>B</sub> = 500 N</b>.</p>"),
        Q("Calcule N<sub>A</sub>, action normale du sol sur les roues arrière.", H_UNITE("N", "Au dixième."),
          NEWTON(NA10, 0.003), f"N<sub>A</sub> = {fr(NA10, 1)} N",
          f"<p>Somme des forces verticales : N<sub>A</sub> = P − N<sub>B</sub> = 10 790 − {fr(NB10, 1)} = "
          f"<b>{fr(NA10, 1)} N</b>.</p>"),
    ]},
    {"title": "Roues avant motrices", "minutes": 8, "intro": [], "blocks": [
        Q("Quel coefficient d'adhérence f<sub>B</sub> = T<sub>B</sub> / N<sub>B</sub> est nécessaire en B ?",
          "Au millième, sans unité.", NUM(FAIR / NB10, tol=0.0012), f"f<sub>B</sub> = {fr(FAIR / NB10, 3)}",
          f"<p>f<sub>B</sub> = T<sub>B</sub> / N<sub>B</sub> = 500 / {fr(NB10, 1)} = <b>{fr(FAIR / NB10, 3)}</b>.</p>"),
        Q("Les roues avant motrices sont-elles capables de maintenir la vitesse du véhicule ?", H_OUINON, YESNO(True),
          "Oui",
          f"<p>Il faut {fr(FAIR / NB10, 3)}, la route mouillée offre 0,1 : {fr(FAIR / NB10, 3)} &lt; 0,1, l'action en B "
          "reste dans le cône d'adhérence, <b>oui</b>. Le manuel écrit « f<sub>B</sub> = 0,102 > 0,1 » : il a inversé "
          "les valeurs des deux cas (0,102 est le coefficient nécessaire en A, partie 3) ; sa conclusion « oui » est "
          "juste.</p>"),
    ]},
    {"title": "Roues arrière motrices", "minutes": 10, "intro": [
        "<p>On reprend les questions précédentes en supposant cette fois les roues arrière (A) motrices et les roues "
        "avant (B) porteuses.</p>"], "blocks": [
        Q("Calcule T<sub>A</sub>, action tangentielle du sol sur les roues arrière motrices.", H_UNITE("N"),
          NEWTON(FAIR, 0.003), "T<sub>A</sub> = 500 N",
          "<p>N<sub>A</sub> et N<sub>B</sub> ne changent pas (les forces au sol ne comptent pas dans les moments en "
          "A) ; la poussée passe à l'arrière : <b>T<sub>A</sub> = 500 N</b>.</p>"),
        Q("Quel coefficient d'adhérence f<sub>A</sub> = T<sub>A</sub> / N<sub>A</sub> est nécessaire en A ?",
          "Au millième, sans unité.", NUM(FAIR / NA10, tol=0.0012), f"f<sub>A</sub> = {fr(FAIR / NA10, 3)}",
          f"<p>f<sub>A</sub> = 500 / {fr(NA10, 1)} = <b>{fr(FAIR / NA10, 3)}</b>.</p>"),
        Q("Les roues arrière motrices sont-elles capables de maintenir la vitesse ?", H_OUINON, YESNO(False), "Non",
          f"<p>{fr(FAIR / NA10, 3)} &gt; 0,1 : il faudrait que l'action en A sorte du cône d'adhérence, les roues "
          "arrière <b>patinent</b> (glissement en A). Le manuel écrit ici « 0,085 &lt; 0,1 », valeur du cas "
          "précédent ; sa conclusion « non » est juste.</p>"),
    ]},
]

PARTS_A6 = [
    {"title": "Effort à transmettre au sol", "minutes": 12, "intro": [
        "<p>On reprend l'activité 5 (exercice 10) en tenant compte des résistances au roulement en A et B : "
        "F<sub>rrA</sub> = 57 N et F<sub>rrB</sub> = 72 N. Comme dans l'exemple 1 du cours (figure de l'automobile "
        "de 1 100 kg), on les schématise par des forces horizontales appliquées au contact, opposées au mouvement : "
        "elles ne changent pas N<sub>A</sub> et N<sub>B</sub>.</p>",
        f'<figure class="fig-ex" style="max-width:640px">{fig_route(True)}<figcaption>Les mêmes actions, avec les '
        "résistances au roulement.</figcaption></figure>",
        donnees(f"N<sub>A</sub> = {fr(NA10, 1)} N ; N<sub>B</sub> = {fr(NB10, 1)} N (activité 5).",
                "F<sub>air</sub> = 500 N ; v = 90 km/h ; coefficient d'adhérence de la route mouillée : 0,1.")],
     "blocks": [
        QBAR(["DT1"]),
        Q("Vérifie la résistance au roulement des roues arrière : calcule leur facteur f<sub>R</sub> = "
          "F<sub>rrA</sub> / N<sub>A</sub>.", "À 0,000 1 près, sans unité.", NUM(FRRA / NA10, tol=0.0003),
          f"f<sub>R</sub> = {fr(FRRA / NA10, 4)}",
          f"<p>f<sub>R</sub> = 57 / {fr(NA10, 1)} = <b>{fr(FRRA / NA10, 4)}</b> ; à l'avant, 72 / {fr(NB10, 1)} = "
          f"{fr(FRRB / NB10, 4)}. On retrouve le facteur des pneus usuels du cours (f<sub>R</sub> ≈ 0,012).</p>"),
        Q("Calcule l'effort tangentiel T que les roues motrices doivent transmettre au sol.", H_UNITE("N"),
          NEWTON(T11, 0.003), f"T = {fr(T11, 0)} N",
          "<p>Vitesse constante : la somme des forces horizontales est nulle. Les roues motrices équilibrent la "
          f"résistance de l'air et les deux résistances au roulement : T = 500 + 57 + 72 = <b>{fr(T11, 0)} N</b>.</p>"),
        Q("Quelle puissance faut-il fournir pour vaincre ces résistances à 90 km/h ?", H_UNITE("W", "À 1 % près."),
          NUM(T11 * V90, U_W, 0.01, variants=[{"value": T11 * V90 / 1000, "relTol": 0.01, "unit": U_KW}]),
          f"P = {fr(T11 * V90, 0)} W",
          f"<p>90 km/h = 25 m/s ; P = T × v = {fr(T11, 0)} × 25 = <b>{fr(T11 * V90, 0)} W</b>, soit "
          f"{fr(T11 * V90 / 1000, 1)} kW, dont {fr((FRRA + FRRB) * V90, 0)} W pour le seul roulement.</p>"),
    ]},
    {"title": "Les roues motrices tiennent-elles ?", "minutes": 10, "intro": [], "blocks": [
        Q("Roues avant motrices : quel coefficient d'adhérence T / N<sub>B</sub> est nécessaire en B ?",
          "Au millième, sans unité.", NUM(T11 / NB10, tol=0.0012), f"{fr(T11 / NB10, 3)}",
          f"<p>T / N<sub>B</sub> = {fr(T11, 0)} / {fr(NB10, 1)} = <b>{fr(T11 / NB10, 3)}</b>.</p>"),
        Q("Les roues avant motrices maintiennent-elles la vitesse ?", H_OUINON, YESNO(False), "Non",
          f"<p>{fr(T11 / NB10, 3)} &gt; 0,1 : avec la résistance au roulement, même les roues avant patinent. Sans elle, "
          f"il ne fallait que {fr(FAIR / NB10, 3)} (activité 5).</p>"),
        Q("Roues arrière motrices : quel coefficient d'adhérence T / N<sub>A</sub> est nécessaire en A ?",
          "Au millième, sans unité.", NUM(T11 / NA10, tol=0.0012), f"{fr(T11 / NA10, 3)}",
          f"<p>T / N<sub>A</sub> = {fr(T11, 0)} / {fr(NA10, 1)} = <b>{fr(T11 / NA10, 3)}</b> &gt; 0,1 : les roues "
          "arrière patinent, a fortiori.</p>"),
    ]},
]


# ============================================================ ACTIVITÉ 7 — BARBECUE DE CHEMINÉE : ARC-BOUTEMENT (exercice 12)
F12, P12, E12, H12, D12 = 0.08, 6.0, 24.0, 19.0, 233.0
PHI12 = math.degrees(math.atan(F12))
DMIN12 = (H12 / F12 - E12) / 2
TALPHA12 = H12 / (2 * D12 + E12)
ALPHA12 = math.degrees(math.atan(TALPHA12))
A12 = P12 / 2 / math.sin(math.atan(TALPHA12))


def _barbecue():
    F = Feuille(245, 150, 175, 62, 2)
    A, B = (0.0, 0.0), (E12, H12)
    tf = F12
    K = (-DMIN12, DMIN12 * tf)
    I = (-D12, D12 * TALPHA12)
    uA, uB = C.unit(C.vec(A, I)), C.unit(C.vec(B, I))
    Pv = (0.0, -P12)
    FA, FB = C.triangle(Pv, uA, uB)
    c6, c5 = (-4.0, 0.0), (E12 + 4, H12)
    ub = C.unit(C.vec(c6, c5))
    nb = (-ub[1], ub[0])
    def bar(s0, s1, e):
        return C.poly([F.p((c6[0] + s * ub[0] + t * nb[0], c6[1] + s * ub[1] + t * nb[1])) for s, t in
                       ((s0, -e), (s1, -e), (s1, e), (s0, e))], "m")
    s_g = (-170 - c6[0]) / ub[0]
    fond = C.poly([F.p(p) for p in [(-330, -100), (-150, -100), (-150, -110), (-330, -110)]], "m2")
    fond += bar(s_g, 130, 4)
    fond += bar(130, 200, 7).replace('class="m"', 'class="m3"')
    fond += C.poly([F.p(p) for p in [(0, -190), (E12, -190), (E12, 120), (0, 120)]], "m2")
    fond += C.poly([F.p(p) for p in [(-70, -190), (95, -190), (95, -200), (-70, -200)]], "sol")
    fond += C.cercle(F.p(c6), 2, "m3") + C.cercle(F.p(c5), 2, "m3")
    blob = [(-300, -100), (-305, -80), (-285, -60), (-255, -52), (-225, -55), (-200, -66), (-178, -64), (-170, -80),
            (-185, -100)]
    fond += C.poly([F.p(p) for p in blob], "m3")
    fond += C.cote(F.p((0, -150)), F.p((E12, -150)), "24", 0, ext=False)
    fond += C.cote(F.p((-D12, -150)), F.p((0, -150)), "233", 0, ext=False)
    fond += C.ligne(F.p((-D12, -112)), F.p((-D12, -158)), "cote")
    fond += C.cote(F.p((70, 0)), F.p((70, H12)), "19", 0, ext=False)
    fond += C.ligne(F.p((4, 0)), F.p((74, 0)), "cote") + C.ligne(F.p((E12 + 4, H12)), F.p((74, H12)), "cote")
    for t, P_, Q_ in (("2", (40, -175), (E12, -170)), ("3", (-120, -130), (-150, -106)), ("4", (-280, -30), (-262, -55)),
                      ("5", (40, 45), (c5[0] + 1, c5[1] + 2)), ("6", (-30, 32), (c6[0] - 1, c6[1] + 2))):
        fond += C.ligne(F.p(P_), F.p(Q_), "tr") + C.texte(F.p((P_[0] - 2, P_[1] + 3)), t, "rep", 4)
    Gp = F.p((-D12, -100))
    given = [F.pt(A, "A", dx=-5, dy=6.2), F.pt(B, "B", dx=1.8, dy=-1.6), F.dr(A, (1, 0), st="n"),
             F.dr(B, (1, 0), st="n"), F.dr(A, (0, 1), st="n"),
             {"k": "vec", "x1": Gp[0], "y1": Gp[1], "x2": Gp[0], "y2": Gp[1] + 22, "n": "P", "st": "f",
              "nx": Gp[0] + 1.5, "ny": Gp[1] + 16}]
    W = -340
    zone = [K, (W, -W * tf), (W, H12 + (W - E12) * tf)]
    corr = [F.cone(A, (-1, 0), PHI12, r=60, n="φ"), F.cone(B, (1, 0), PHI12, r=30),
            C.zone(F, zone, "zone d'arc-boutement", pos=(-300, 40)), F.pt(K, "K", dx=-2, dy=-2.5),
            F.dr((-D12, 0), (0, 1)), F.dr(A, uA), F.dr(B, uB), F.pt(I, "I", dx=1.5, dy=-2)]
    corr += Dynamique(100, 12, 1).chaine([(Pv, "P", {}), (FA, "A", {}), (FB, "B", {})])
    cfg = {"w": F.w, "h": F.h, "kL": 2, "given": given, "corr": corr, "outil": "cone",
           "forces": {"u": "daN", "choix": [1], "def": 0},
           "echTxt": "Longueurs à l'échelle 1:2 · forces : 1 mm ↔ 1 daN",
           "titre": "Barbecue de cheminée — arc-boutement en A et B"}
    return {"cfg": cfg, "fond": fond, "FA": FA, "FB": FB}


BBQ = _barbecue()


def hero_bbq():
    return C.statique(BBQ["cfg"], BBQ["fond"], "Barbecue de cheminée : tige 2, grille 3, axes 5 et 6 en B et A, poids P")


PARTS_A7 = [
    {"title": "Arc-boutement : résolution graphique", "minutes": 25, "intro": [
        "<p>Un barbecue pour cheminée d'intérieur se compose d'un socle (2) avec tige verticale parallélépipédique et "
        "d'une grille de cuisson (3) solidaire de deux axes cylindriques (5) et (6). L'ensemble (3 + 4 + 5 + 6) est "
        "réglable en hauteur. P (6 daN) est le poids de l'ensemble ; les actions en A et B entre 2, 5 et 6 sont "
        "schématisées par des vecteurs-forces passant par ces points ; µ = f<sub>A</sub> = f<sub>B</sub> = 0,08.</p>",
        donnees("Tige de 24 mm d'épaisseur ; B est 19 mm plus haut que A, sur la face opposée.",
                "La droite d'action de P est à 233 mm de la face de la tige qui porte A.",
                "Les normales au contact en A et B sont horizontales (perpendiculaires aux faces de la tige).",
                "Échelles imposées : longueurs 1:2, forces 1 mm ↔ 1 daN.")], "blocks": [
        QBAR(["DT1", "DT2"]),
        Q("Calcule l'angle de frottement φ en A et B.", H_UNITE("°", "Au centième de degré."), DEG(PHI12, 0.05),
          f"φ = {fr(PHI12, 2)}°", f"<p>tan φ = 0,08, φ = arctan 0,08 = <b>{fr(PHI12, 2)}°</b> : des cônes très fins.</p>"),
        {"kind": "pl", "stem": "Trace les cônes de frottement en A et B, la zone d'arc-boutement, puis les actions en A et "
                               "B lorsqu'elles ont la même inclinaison.",
         "consigne": "Les génératrices des deux cônes, prolongées vers la grille, délimitent la zone où les deux "
                     "actions peuvent se couper sans sortir de leur cône. Si la droite d'action de P la traverse, il "
                     "y a arc-boutement.",
         "cfg": BBQ["cfg"], "fond": BBQ["fond"], "deps_tout": True,
         "criteria": ["Les cônes de frottement en A et en B (axes horizontaux, demi-angle 4,6°) sont tracés.",
                      "Les génératrices prolongées délimitent la zone commune aux deux cônes, de pointe K, du côté de "
                      "la grille.",
                      "La droite d'action de P (verticale) est tracée et traverse la zone d'arc-boutement.",
                      "Pour α_A = α_B, les droites d'action de A et B passent par le point I de la droite d'action de "
                      "P situé à égale « pente » des deux contacts.",
                      "Le dynamique P + A + B = 0 est fermé à l'échelle."],
         "why": "<ol><li>Cônes : sommets A et B, axes horizontaux, demi-angle φ = "
                f"{fr(PHI12, 2)}°.</li><li>La génératrice supérieure du cône en A et la génératrice inférieure du cône "
                f"en B se coupent en K, à {fr(DMIN12, 1)} mm de la face de la tige : à gauche de K, toute verticale "
                "traverse la zone commune aux deux cônes.</li><li>La droite d'action de P est à 233 mm : elle traverse "
                "la zone, l'ensemble reste en équilibre quel que soit P — c'est l'<b>arc-boutement</b> ; il ne dépend "
                "que de la géométrie et du frottement.</li><li>α<sub>A</sub> = α<sub>B</sub> : I est sur la verticale "
                f"de P, à 233 × tan α au-dessus de A, avec tan α = 19 / (2 × 233 + 24) ; α = {fr(ALPHA12, 2)}°.</li>"
                f"<li>Dynamique : P (6 mm) puis les parallèles à AI et BI ; {nrm('A')} = {nrm('B')} ≈ {fr(A12, 1)} daN.</li></ol>"},
        Q("À quelle distance minimale d de la face de la tige la droite d'action de P doit-elle passer pour qu'il y ait "
          "arc-boutement ?", H_UNITE("mm", "En millimètres réels, à 2 mm près."), NUM(DMIN12, U_MM, tol=2),
          f"d ≈ {fr(DMIN12, 1)} mm",
          "<p>La pointe K de la zone est à l'intersection des génératrices : à la distance d de la face, le cône en A "
          "couvre ± d tan φ, le cône en B, 19 ± (24 + d) tan φ. Ils se touchent quand "
          + calc("d tan φ + (24 + d) tan φ = 19") + f", soit d = (19 / 0,08 − 24) / 2 = <b>{fr(DMIN12, 2)} mm</b>.</p>"),
        Q("L'ensemble (3 + 4 + 5 + 6) reste-t-il en équilibre quelle que soit la valeur de P ?", H_OUINON,
          YESNO(True), "Oui",
          "<p>233 mm &gt; 106,75 mm : la droite d'action de P traverse la zone d'arc-boutement. Les deux actions de "
          "contact peuvent toujours se couper sur elle sans sortir de leur cône, et leurs normes grandissent avec P : "
          "il y a <b>arc-boutement</b>, quelle que soit la charge posée sur la grille.</p>"),
    ]},
    {"title": "Actions en A et B", "minutes": 15, "intro": [
        "<p>On prend P = 6 daN et l'on suppose que les actions en A et B ont la même inclinaison (α<sub>A</sub> = "
        "α<sub>B</sub> = α) sur la normale au contact.</p>"], "blocks": [
        Q("Calcule l'inclinaison α des actions en A et B.", H_UNITE("°", "Au centième de degré."), DEG(ALPHA12, 0.05),
          f"α = {fr(ALPHA12, 2)}°",
          "<p>Les droites d'action AI et BI se coupent sur la verticale de P, à 233 mm de A et 257 mm de B "
          "horizontalement : 233 tan α + 257 tan α = 19, soit tan α = 19 / 490 et <b>α = "
          f"{fr(ALPHA12, 2)}°</b> &lt; φ : chaque action est bien dans son cône.</p>"),
        Q(f"Calcule la norme de {vn('A')} (égale à celle de {vn('B')}).", H_UNITE("daN", "Au dixième."),
          DAN(A12, 0.02), f"{nrm('A')} = {nrm('B')} ≈ {fr(A12, 1)} daN",
          "<p>Même inclinaison : les composantes horizontales s'opposent et sont égales, donc A = B. Les composantes "
          "verticales portent le poids : 2 A sin α = 6 daN, soit "
          + calc(f"A = 3 / sin {fr(ALPHA12, 2)}°") + f" = <b>{fr(A12, 1)} daN</b>. Treize fois le poids : la tige est "
          "fortement serrée, c'est ce qui bloque la grille.</p>"),
        Q("Calcule la composante tangentielle T<sub>A</sub> de l'action en A.", H_UNITE("daN", "Au dixième."),
          DAN(P12 / 2, 0.02), "T<sub>A</sub> = 3 daN",
          "<p>T<sub>A</sub> = A sin α = P / 2 = <b>3 daN</b> : chaque contact porte la moitié du poids. "
          f"N<sub>A</sub> = A cos α ≈ {fr(A12 * math.cos(math.atan(TALPHA12)), 1)} daN, et T<sub>A</sub> / N<sub>A</sub> "
          f"= {fr(TALPHA12, 3)} &lt; 0,08.</p>"),
    ]},
]


# ============================================================ DOCUMENTS DES ACTIVITÉS
TABLE_COEF = ('<table class="t"><thead><tr><th rowspan="2">Matériaux en contact</th><th colspan="2">Adhérence '
              "µ<sub>s</sub> = tan φ<sub>s</sub></th><th colspan=\"2\">Frottement µ = tan φ</th></tr><tr><th>à sec</th>"
              "<th>lubrifié</th><th>à sec</th><th>lubrifié</th></tr></thead><tbody>" + "".join(
                  f"<tr><td>{m}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for m, a, b, c, d in [
                      ("acier sur acier", "0,18", "0,12", "0,15", "0,09"), ("acier sur fonte", "0,19", "0,1", "0,16", "0,08 à 0,04"),
                      ("acier sur bronze", "0,11", "0,1", "0,1", "0,09"), ("téflon sur acier", "0,04", "", "0,04", ""),
                      ("fonte sur bronze", "", "0,1", "0,2", "0,08 à 0,04"), ("nylon sur acier", "", "", "0,35", "0,12"),
                      ("bois sur bois", "0,65", "0,2", "0,4 à 0,2", "0,16 à 0,04"),
                      ("métaux sur bois", "0,6 à 0,5", "0,1", "0,5 à 0,2", "0,08 à 0,02"), ("métal sur glace", "", "", "0,02", ""),
                      ("pneu de voiture sur route", "0,8", "", "0,6", "0,3 à 0,1 sur sol mouillé")]) + "</tbody></table>")

DT1 = ("<div class=\"doc-text\"><h3>Adhérence et frottement</h3><p>Deux surfaces en contact qui glissent l'une sur "
       "l'autre : <b>frottement</b>. Qui tendent à glisser sans se déplacer : <b>adhérence</b>.</p>"
       "<p>Au contact en A, l'action de 0 sur 1 se décompose en une composante normale N et une composante "
       "tangentielle T ; α est son angle avec la normale.</p><ul>"
       "<li><b>Adhérence</b> (pas de mouvement) : T<sub>a</sub> ≤ µ<sub>s</sub>·N, α ≤ φ<sub>s</sub> ; l'action est "
       "dans le cône d'adhérence.</li>"
       "<li><b>Équilibre strict</b> (limite) : T<sub>a</sub> = µ<sub>s</sub>·N, α = φ<sub>s</sub> ; l'action est sur "
       "le cône.</li>"
       "<li><b>Glissement</b> : T = µ·N, α = φ, l'action est sur le cône de frottement et T s'oppose à la vitesse de "
       "glissement.</li></ul><p>µ<sub>s</sub> = f<sub>s</sub> = tan φ<sub>s</sub> ; µ = f = tan φ. Sauf indication, on "
       "confond adhérence et frottement : φ<sub>s</sub> = φ.</p><h3>Valeurs indicatives</h3>" + TABLE_COEF +
       "<h3>Résistance au roulement</h3><p>F<sub>R</sub> = (a / r)·F = f<sub>R</sub>·F, avec a le coefficient de "
       "résistance au roulement (mm), r le rayon de l'élément roulant et f<sub>R</sub> = a / r le facteur de frottement "
       "de roulement (pneus usuels : f<sub>R</sub> ≈ 0,012).</p><h3>Solide soumis à trois forces</h3><p>À l'équilibre, "
       "trois forces non parallèles sont <b>concourantes</b> (leurs droites d'action passent par un même point) et leur "
       "somme est nulle : le <b>dynamique</b> (triangle des forces mises bout à bout) est fermé. Trois forces "
       "parallèles : on écrit les moments.</p></div>")

DT2 = ("<div class=\"doc-text\"><h3>La planche de construction</h3><p>La feuille est cotée en millimètres : imprimée "
       "à 100 % (« Imprimer le document réponse »), elle garde ses dimensions, ses échelles et permet de construire à la "
       "règle et au rapporteur.</p><ul>"
       "<li><b>Aimantation</b> : en approchant un point, une intersection ou une droite, le pointeur s'y accroche "
       "(cercle orange : point ou intersection ; carré : sur une droite).</li>"
       "<li><b>Droite</b>, <b>Segment</b> : deux clics. <b>Parallèle</b>, <b>Perpendiculaire</b> : clique la "
       "référence (droite ou vecteur), puis le point de passage.</li>"
       "<li><b>Inclinée</b> : clique la référence (une zone vide : l'horizontale), le point de passage, puis saisis "
       "l'angle (positif dans le sens trigonométrique).</li>"
       "<li><b>Cône</b> : clique le point de contact, puis la normale du côté du solide isolé ; saisis f (0,15) ou φ "
       "(8,5°). Les deux génératrices sont des droites : leurs intersections s'aimantent.</li>"
       "<li><b>Vecteur</b> : clique l'origine puis l'extrémité ; la norme s'affiche à l'échelle des forces. Dans la "
       "fenêtre qui s'ouvre, nomme-le (A0/1 s'écrit A0/1) et, si besoin, corrige sa norme : il garde sa direction.</li>"
       "<li><b>Distance</b>, <b>Angle</b> : mesures (en millimètres de feuille et réels, en degrés), reportées dans le "
       "tableau des relevés.</li>"
       "<li><b>Gomme</b>, <b>Annuler</b>, <b>Rétablir</b> ; <b>Main</b> pour se déplacer en zoom ; Échap annule le "
       "tracé en cours.</li></ul><h3>Méthode des trois forces</h3><ol><li>Isoler le solide, faire le bilan : forces "
       "connues, directions connues, inconnues.</li><li>Tracer les deux droites d'action connues ; leur intersection "
       "est le point de concours I.</li><li>La troisième passe par son point d'application et par I. Avec frottement, "
       "la comparer au cône (dedans : adhérence ; sur : limite ; dehors : impossible).</li><li>Dynamique : tracer la "
       "force connue à l'échelle, puis les parallèles aux deux autres droites d'action à ses extrémités ; lire les "
       "normes.</li></ol></div>")

DOCS = [("DT1", "Lois du frottement et du roulement", "Dossier technique", True, DT1),
        ("DT2", "La planche de construction", "Dossier technique", True, DT2)]


# ============================================================ consignes
_C_MODES = """<p class="only-training"><strong>Mode entraînement.</strong> Réponds dans chaque champ puis clique sur « Valider » : une réponse validée est définitive et sa correction s'affiche aussitôt.</p>
    <p class="only-exam"><strong>Mode examen.</strong> Compose tout le sujet sans correction ni note : tes réponses et tes constructions restent modifiables jusqu'au bout. Le bouton « J'ai fini, je fais corriger ma copie », en fin de sujet, dévoile d'un coup les corrections, les notes par partie et la note globale.</p>
    <p><strong>Les unités sont notées.</strong> Pour toute question numérique avec unité, la valeur vaut la moitié des points et l'unité l'autre moitié : une valeur juste écrite sans unité, ou avec une unité fausse, ne rapporte qu'un demi-point. Une force peut s'écrire en daN ou en N.</p>"""
_C_PLANCHE = """<p><strong>Les constructions se font sur la planche.</strong> Ses outils tracent à la règle et au rapporteur : droites, parallèles, perpendiculaires, droites inclinées, cônes de frottement, vecteurs à l'échelle des forces ; le pointeur s'aimante aux points et aux intersections, les relevés donnent longueurs, normes et angles. Tes lectures se saisissent dans les questions qui suivent la planche. Une construction validée reçoit sa correction superposée une fois ces questions validées : tu t'attribues alors toi-même ses points avec une grille de critères. Le document réponse s'imprime à l'échelle pour construire à la main.</p>"""
_C_BAREME = """<p><strong>Barème pondéré par la durée conseillée</strong> : chaque partie est notée sur 20, puis pèse au prorata de son temps. Le récapitulatif de fin de sujet donne le détail partie par partie.</p>"""
CONSIGNES_CALC = (_C_MODES + """
    <p>Le dossier technique (DT1 : lois du frottement, valeurs indicatives) s'ouvre avec les onglets sur le bord droit, ou avec les boutons des en-têtes de question.</p>
    """ + _C_BAREME)
CONSIGNES_GRAPH = (_C_MODES + "\n    " + _C_PLANCHE + """
    <p>Le dossier technique (DT1 : lois du frottement ; DT2 : mode d'emploi de la planche et méthode des trois forces) s'ouvre avec les onglets sur le bord droit, ou avec les boutons des en-têtes de question.</p>
    """ + _C_BAREME)

# ============================================================ ACTIVITÉS (accueil et configuration)
# Ajouter une activité : décrire ses parties (comme PARTS_A2), puis l'ajouter ici ; "etude": True la range dans la
# rubrique « Études de cas ». La carte apparaît d'elle-même sur l'accueil.
SRC = "Source : manuel, chapitre 9 « Frottement et roulement », "
EXO_DEFS = [
    {"key": "cones-adherence-frottement", "prefix": "a", "tag": "Activité 1", "meth": "Graphique",
     "title": "Cônes d'adhérence et de frottement", "parts": PARTS_A1, "docs": ["DT1"], "consignes": qcm.CONSIGNES,
     "source": SRC + "QCM, questions 3 et 4 (regroupées : questions courtes).",
     "hero": lambda: f'<div class="hero-cone">{FIG_CONE}</div>', "hero_cap": "Où peut se trouver l'action de contact ?",
     "mots": ["Cône d'adhérence", "Cône de frottement", "QCM"], "vign": "carte-a1", "valt": "Cône de frottement",
     "sub": "Deux questions pour situer l'action de contact par rapport au cône, selon qu'il y a adhérence ou "
            "glissement."},
    {"key": "cle-excentrique", "prefix": "b", "tag": "Activité 2", "meth": "Graphique",
     "title": "Clé à excentrique", "parts": PARTS_A2, "docs": ["DT1", "DT2"], "consignes": CONSIGNES_GRAPH,
     "source": SRC + "exercice 5.", "hero": hero_cle,
     "hero_cap": "La droite AD garde la même direction quel que soit l'écrou.",
     "mots": ["Trois forces", "Cône en A", "Dynamique", "Couple de serrage"], "vign": "carte-a2",
     "valt": "Clé à excentrique",
     "sub": "Construire les actions sur le manche d'une clé à excentrique avec le cône de frottement, les vérifier par "
            "le calcul, puis en déduire le couple de serrage."},
    {"key": "voiture-pente", "prefix": "c", "tag": "Activité 3", "meth": "Graphique",
     "title": "Voiture à l'arrêt dans une pente", "parts": PARTS_A3, "docs": ["DT1", "DT2"],
     "consignes": CONSIGNES_GRAPH, "source": SRC + "exercice 6.", "hero": hero_pente,
     "hero_cap": "Frein à main sur les roues avant, roues arrière libres.",
     "mots": ["Frein à main", "Cône d'adhérence", "Point de concours", "Pente limite"], "vign": "carte-a3",
     "valt": "Voiture tout-terrain dans une pente",
     "sub": "La voiture freinée par ses seules roues avant tient-elle dans une pente de 20 % ? Construction des "
            "actions du sol, puis pente limite."},
    {"key": "voiture-pente-variantes", "prefix": "d", "tag": "Activité 4", "meth": "Analytique",
     "title": "Voiture en pente : trois variantes", "parts": PARTS_A4, "docs": ["DT1"], "consignes": CONSIGNES_CALC,
     "source": SRC + "exercices 7, 8 et 9 (regroupés : exercices courts, variantes de l'exercice 6).",
     "hero": hero_pente, "hero_cap": "Position de G, roue freinée, frein sur les quatre roues.",
     "mots": ["Position limite", "Frein arrière", "Quatre roues", "Forces parallèles"], "vign": "carte-a4",
     "valt": "Voiture tout-terrain dans une pente",
     "sub": "Trois variantes de la voiture en pente : jusqu'où peut reculer le centre de gravité, freiner à l'arrière, "
            "freiner les quatre roues."},
    {"key": "voiture-route-mouillee", "prefix": "e", "tag": "Activité 5", "meth": "Analytique",
     "title": "Voiture sur route mouillée", "parts": PARTS_A5, "docs": ["DT1"], "consignes": CONSIGNES_CALC,
     "source": SRC + "exercice 10.", "hero": fig_route, "hero_cap": "90 km/h, résistance de l'air, adhérence 0,1.",
     "mots": ["Adhérence", "Traction ou propulsion", "Résistance de l'air"], "vign": "carte-a5",
     "valt": "Cabriolet sur route mouillée",
     "sub": "Sous la pluie, l'adhérence tombe à 0,1 : les roues motrices peuvent-elles encore maintenir 90 km/h ? "
            "Traction avant et propulsion comparées."},
    {"key": "resistance-roulement", "prefix": "f", "tag": "Activité 6", "meth": "Analytique",
     "title": "Résistance au roulement", "parts": PARTS_A6, "docs": ["DT1"], "consignes": CONSIGNES_CALC,
     "source": SRC + "exercice 11.", "hero": lambda: fig_route(True),
     "hero_cap": "Les résistances au roulement s'ajoutent à celle de l'air.",
     "mots": ["Facteur f_R", "Effort moteur", "Puissance", "Patinage"], "vign": "carte-a6",
     "valt": "Cabriolet et résistances au roulement",
     "sub": "La même voiture, en tenant compte de la résistance au roulement : effort et puissance à fournir, tenue "
            "des roues motrices."},
    {"key": "barbecue-arc-boutement", "prefix": "g", "tag": "Activité 7", "meth": "Graphique",
     "title": "Barbecue de cheminée : arc-boutement", "parts": PARTS_A7, "docs": ["DT1", "DT2"],
     "consignes": CONSIGNES_GRAPH, "source": SRC + "exercice 12.", "hero": hero_bbq,
     "hero_cap": "La grille tient seule sur la tige, quelle que soit la charge.",
     "mots": ["Arc-boutement", "Deux cônes", "Zone commune"], "vign": "carte-a7", "valt": "Barbecue de cheminée",
     "sub": "Pourquoi la grille réglable ne glisse-t-elle pas le long de sa tige ? Zone d'arc-boutement, puis actions "
            "en A et B."},
]
