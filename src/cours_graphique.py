"""Cours 2 — Frottement : résolution graphique (?ex=cours-frottement-graphique).

Source : manuel, chapitre 9, pages 125 à 129 (src/images/originaux/cours-p125 à p129) : angle et cône de frottement,
lecture graphique des lois de Coulomb, exercice de la voiture qui monte sur un trottoir (figures 9 à 14), lecture
graphique de la résistance au roulement. L'exercice du trottoir devient une démonstration pas à pas sur la planche de
construction (quatre cas), que l'élève peut ensuite refaire lui-même sur le même fond.

La figure du manuel n'est pas cotée : les dimensions de la voiture (rayon des roues 360 mm, empattement 2 800 mm,
G à 1 600 mm de l'essieu avant et 700 mm du sol, trottoir de 200 mm) sont choisies ici, de sorte que les quatre
conclusions du manuel soient retrouvées ; elles sont écrites sur la planche.
"""
import math

import construction as C
import cours_analytique
import figures
from construction import Dynamique, Feuille

OBJECTIFS = ["Associer à un contact avec frottement son angle et son cône de frottement (ou d'adhérence).",
             "Lire les lois de Coulomb sur une figure : action de contact dans, sur ou hors du cône.",
             "Résoudre graphiquement l'équilibre d'un solide soumis à trois forces, dont une action avec frottement."]
PREREQUIS = ["Cours 1 : adhérence, frottement, µ<sub>s</sub> et µ.", "Solide soumis à trois forces : forces "
             "concourantes, dynamique fermé."]


def fr(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


# ============================================================ la voiture et le trottoir
R_T, H_T, EMP, XG_T, YG_T, P_T, F_T = 360.0, 200.0, 2800.0, 1600.0, 700.0, 1800.0, 0.8
PHI_T = math.degrees(math.atan(F_T))


def _trottoir():
    F = Feuille(262, 168, 40, 150, 30)
    A, Cc, G = (0.0, R_T), (EMP, R_T), (XG_T, YG_T)
    B = (-math.sqrt(R_T ** 2 - (R_T - H_T) ** 2), H_T)
    D = (EMP, 0.0)
    up = (0.0, 1.0)
    uBA = C.unit(C.vec(B, A))
    Pv = (0.0, -P_T)
    dyn = Dynamique(195, 14, 20)
    fond = C.poly([F.p((-1200, 0)), F.p((B[0], 0)), F.p((B[0], H_T)), F.p((-1200, H_T))], "sol")
    fond += C.sol(F, (B[0], 0), (3700, 0), 4)
    fond += figures.voiture_ancienne(F, A, EMP, R_T)
    fond += C.cote(F.p((-1050, 0)), F.p((-1050, H_T)), "h = 200", 0, ext=False)
    fond += C.cote(F.p((0, -260)), F.p((XG_T, -260)), "1 600", 0, ext=False)
    fond += C.cote(F.p((XG_T, -260)), F.p((EMP, -260)), "1 200", 0, ext=False)
    for x in (0, XG_T, EMP):
        fond += C.ligne(F.p((x, 0 if x else R_T)), F.p((x, -330)), "cote")
    fond += C.cote(F.p((3500, 0)), F.p((3500, YG_T)), "700", 0, ext=False)
    fond += C.ligne(F.p(G), F.p((3580, YG_T)), "ax")
    fond += C.texte(F.p((2950, 1650)), "roues : r = 360 mm", "leg", 3.2)
    fond += C.texte(F.p((2950, 1500)), "f = 0,8 en B et D", "leg", 3.2)
    fond += C.texte(F.p((-1150, 1650)), "Dimensions choisies : la figure", "leg", 2.9)
    fond += C.texte(F.p((-1150, 1530)), "du manuel n'est pas cotée.", "leg", 2.9)
    Gp = F.p(G)
    given = [F.pt(A, "A", dx=1.5, dy=-2), F.pt(B, "B", dx=-5.5, dy=-1.5), F.pt(Cc, "C", dx=1.5, dy=-2),
             F.pt(D, "D", dx=1.5, dy=5.5), F.pt(G, "G", dx=1.5, dy=-1.5), F.dr(D, (1, 0), st="n"),
             {"k": "vec", "x1": Gp[0], "y1": Gp[1], "x2": Gp[0], "y2": Gp[1] + 22, "n": "P", "st": "f",
              "nx": Gp[0] + 1.5, "ny": Gp[1] + 18}]
    T = lambda o, st: dict(o, st=st)

    # a) roues arrière motrices
    Ia = C.inter(G, up, B, uBA)
    uDa = C.unit(C.vec(D, Ia))
    al_a = C.ecart(uDa, up)
    sa = [{"t": "Isolons les <b>roues avant (3)</b>, porteuses : elles ne reçoivent que deux actions, celle du trottoir en B "
                "et celle de l'essieu en A. Deux forces égales et opposées : leur droite d'action commune est <b>AB</b>, "
                "B<sub>0/3</sub> = −A<sub>1/3</sub>.",
           "o": [T(F.dr(B, uBA), "t"), F.tx((-1150, 950), "droite d'action de B0/3", size=3.2)]},
          {"t": "Isolons l'ensemble du véhicule (1 + 2 + 3) : il est soumis à <b>trois forces</b>, P (verticale en G), "
                "B<sub>0/3</sub> (droite AB) et D<sub>0/2</sub>. Trois forces non parallèles en équilibre sont "
                "concourantes : la verticale de G et la droite AB se coupent en <b>I</b>.",
           "o": [T(F.dr(G, up), "f"), T(F.pt(Ia, "I", dx=1.5, dy=-1.5), "r")]},
          {"t": "La troisième action, D<sub>0/2</sub>, passe donc par D et par I.",
           "o": [T(F.dr(D, uDa), "f")]},
          {"t": f"Traçons le <b>cône de frottement en D</b> : sommet D, axe la normale (verticale), demi-angle "
                f"φ = arctan 0,8 = {fr(PHI_T, 1)}°. La droite DI fait α = {fr(al_a, 1)}° avec la normale : "
                f"<b>α &gt; φ</b>, D<sub>0/2</sub> serait hors du cône. C'est contraire aux lois du frottement : les "
                "roues arrière <b>patinent en D</b>, la voiture ne peut pas monter sur le trottoir.",
           "o": [T(F.cone(D, up, PHI_T, r=40, n="φ"), "c"), T(F.arc(D, up, uDa, f"α = {fr(al_a, 1)}°", vers=Ia), "r")]}]

    # b) hauteur limite, roues arrière motrices
    eg = C.rot(up, PHI_T)               # génératrice du cône en D, vers l'avant (gauche) et le haut
    N = C.inter(D, eg, G, up)
    uAN = C.unit(C.vec(A, N))
    Bl = (A[0] - R_T * uAN[0], A[1] - R_T * uAN[1])
    h_lim = Bl[1]
    FBb, FDb = C.triangle(Pv, C.unit(C.vec(Bl, N)), C.unit(C.vec(D, N)))
    sb = [{"t": f"À la limite de l'adhérence, D<sub>0/2</sub> est <b>sur</b> le cône en D (équilibre strict) : sa "
                f"génératrice coupe la verticale de G en <b>N</b>, le point de concours limite.",
           "o": [T(F.cone(D, up, PHI_T, r=40, n="φ"), "c"), T(F.dr(G, up), "f"), T(F.dr(D, eg), "f"),
                 T(F.pt(N, "N", dx=1.5, dy=-1.5), "r")]},
          {"t": "B<sub>0/3</sub> passe toujours par le centre A de la roue avant : la droite <b>NA</b> donne sa "
                "direction. Elle coupe la roue au point de contact limite B', au bord du plus haut trottoir que la "
                "voiture puisse gravir.",
           "o": [T(F.dr(A, uAN), "f"), T(F.pt(Bl, "B'", dx=-6, dy=-1), "r"),
                 T(F.sg((-1200, h_lim), Bl), "r")]},
          {"t": f"<b>h<sub>limite</sub> ≈ {fr(h_lim, 0)} mm</b> : avec ces dimensions, un trottoir de 200 mm est trop "
                "haut pour une voiture à roues arrière motrices.",
           "o": [F.tx((-1150, 1150), f"h limite ≈ {fr(h_lim, 0)} mm", size=3.4)]},
          {"t": f"Dynamique à l'équilibre strict (1 mm ↔ 20 daN) : P = 1 800 daN (90 mm), puis les parallèles à "
                f"B'N et DN. On lit B<sub>0/3</sub> ≈ {fr(math.hypot(*FBb), 0)} daN et D<sub>0/2</sub> ≈ "
                f"{fr(math.hypot(*FDb), 0)} daN.",
           "o": [T(o, "f") for o in dyn.chaine([(Pv, "P", {}), (FBb, "B0/3", {}), (FDb, "D0/2", {})])]}]

    # c) roues avant motrices
    al_c = C.ecart(uBA, up)
    sc = [{"t": "Les <b>roues arrière (2)</b> sont maintenant porteuses : deux forces, en D et en C. D<sub>0/2</sub> "
                "passe par D et par le centre C de la roue : elle est <b>verticale</b>.",
           "o": [T(F.dr(D, up), "f")]},
          {"t": "P et D<sub>0/2</sub> sont parallèles : l'équilibre n'est possible que si B<sub>0/3</sub> leur est "
                "aussi parallèle, donc verticale en B.",
           "o": [T(F.dr(G, up), "f"), T(F.dr(B, up), "f")]},
          {"t": f"Cône de frottement en B : axe la normale BA, demi-angle {fr(PHI_T, 1)}°. La verticale fait "
                f"α<sub>B</sub> = {fr(al_c, 1)}° avec la normale : <b>α<sub>B</sub> &gt; φ</b>. Les roues avant "
                "<b>patinent en B</b> : la voiture ne monte pas davantage.",
           "o": [T(F.dr(B, uBA), "n"), T(F.cone(B, uBA, PHI_T, r=34, n="φ"), "c"),
                 T(F.arc(B, uBA, up, f"αB = {fr(al_c, 1)}°", vers=(B[0] + 300, B[1] + 900)), "r")]}]

    # d) quatre roues motrices
    eB = C.rot(uBA, PHI_T)
    M = C.inter(B, eB, G, up)
    def ecarts(y):
        I = (XG_T, y)
        return C.ecart(C.vec(D, I), up) - (C.angle_deg(C.vec(B, I)) - C.angle_deg(uBA))
    lo, hi = N[1], M[1]
    for _ in range(80):
        mid = (lo + hi) / 2
        if ecarts(mid) > 0:
            lo = mid
        else:
            hi = mid
    Id = (XG_T, (lo + hi) / 2)
    al_d = C.ecart(C.vec(D, Id), up)
    uBd, uDd = C.unit(C.vec(B, Id)), C.unit(C.vec(D, Id))
    FBd, FDd = C.triangle(Pv, uBd, uDd)
    sd = [{"t": f"Quatre roues motrices : il y a frottement en B et en D. Traçons les deux cônes (demi-angle "
                f"{fr(PHI_T, 1)}°) : en B d'axe BA, en D d'axe vertical.",
           "o": [T(F.dr(B, uBA), "n"), T(F.cone(B, uBA, PHI_T, r=34, n="φ"), "c"), T(F.cone(D, up, PHI_T, r=40, n="φ"), "c")]},
          {"t": "Leurs génératrices coupent la verticale de G en <b>M</b> (cône en B) et <b>N</b> (cône en D). Tout point "
                "de concours I pris entre M et N laisse B<sub>0/3</sub> et D<sub>0/2</sub> dans leurs cônes : il "
                "existe une infinité de solutions, la voiture <b>monte</b> sur le trottoir.",
           "o": [T(F.dr(G, up), "f"), T(F.dr(B, eB), "c"), T(F.dr(D, eg), "c"), T(F.pt(M, "M", dx=1.5, dy=-1.5), "r"),
                 T(F.pt(N, "N", dx=1.5, dy=4.5), "r"), T(F.sg(M, N), "r")]},
          {"t": f"Une solution parmi d'autres : α<sub>B</sub> = α<sub>D</sub>. Le point I qui la réalise est à "
                f"{fr(Id[1], 0)} mm du sol ; α ≈ {fr(al_d, 1)}° &lt; φ.",
           "o": [T(F.pt(Id, "I", dx=-5, dy=-1.5), "r"), T(F.dr(B, uBd), "f"), T(F.dr(D, uDd), "f")]},
          {"t": f"Dynamique (1 mm ↔ 20 daN) : P puis les parallèles à BI et DI ; B<sub>0/3</sub> ≈ "
                f"{fr(math.hypot(*FBd), 0)} daN, D<sub>0/2</sub> ≈ {fr(math.hypot(*FDd), 0)} daN.",
           "o": [T(o, "f") for o in dyn.chaine([(Pv, "P", {}), (FBd, "B0/3", {}), (FDd, "D0/2", {})])]}]

    cfg = {"w": F.w, "h": F.h, "kL": 30, "given": given, "outil": "dr",
           "forces": {"u": "daN", "choix": [20], "def": 0},
           "echTxt": "Longueurs à l'échelle 1:30 · forces : 1 mm ↔ 20 daN · P = 1 800 daN · f = 0,8",
           "titre": "Montée de trottoir sans élan",
           "scenarios": [
               {"titre": "a) Roues arrière motrices", "steps": sa,
                "intro": "Roues arrière motrices, roues avant porteuses. La voiture peut-elle monter sur le trottoir "
                         "sans élan ? Avance étape par étape."},
               {"titre": "b) Hauteur limite", "steps": sb,
                "intro": "Toujours roues arrière motrices : quelle est la plus grande hauteur de trottoir que la "
                         "voiture puisse gravir ?"},
               {"titre": "c) Roues avant motrices", "steps": sc,
                "intro": "Roues avant motrices, roues arrière porteuses : est-ce mieux ?"},
               {"titre": "d) Quatre roues motrices", "steps": sd,
                "intro": "Les quatre roues sont motrices : frottement en B et en D."}]}
    return {"cfg": cfg, "fond": fond, "al_a": al_a, "h_lim": h_lim, "al_c": al_c, "Id": Id, "al_d": al_d}


TROTTOIR = _trottoir()


# ============================================================ figures
def svg_cones():
    """Figure 5 redessinée : cône d'adhérence (φs) et cône de frottement (φ), de sommet A, d'axe la normale."""
    W, H, Ax, Ay = 640, 330, 320, 170
    def nappe(phi, L, col, sg):
        dx, dy = L * math.tan(math.radians(phi)), L
        y = Ay - sg * dy
        return (f'<path d="M{Ax} {Ay}L{Ax - dx:.1f} {y:.1f}M{Ax} {Ay}L{Ax + dx:.1f} {y:.1f}" stroke="{col}" '
                f'stroke-width="2" fill="none"/><ellipse cx="{Ax}" cy="{y:.1f}" rx="{dx:.1f}" ry="{dx * 0.22:.1f}" '
                f'fill="none" stroke="{col}" stroke-width="1.6"/>')
    s = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Cône d\'adhérence de demi-angle φs et cône de frottement '
         f'de demi-angle φ, de sommet le point de contact A et d\'axe la normale n ; φs est plus grand que φ">'
         f'<rect width="{W}" height="{H}" fill="#fff"/>'
         f'<path d="M110 {Ay + 12}L250 {Ay - 36}L530 {Ay - 36}L390 {Ay + 12}Z" fill="#EEF0EC" stroke="#A5ADAA"/>'
         f'<path d="M120 {Ay - 50}Q{Ax} {Ay + 40} 520 {Ay - 50}" fill="none" stroke="#1B7A43" stroke-width="10" opacity=".35"/>'
         f'<path d="M120 {Ay + 60}Q{Ax} {Ay - 30} 520 {Ay + 60}" fill="none" stroke="#B26A00" stroke-width="10" opacity=".3"/>')
    s += nappe(36, 120, "#B42318", 1) + nappe(26, 120, "#1F5FA8", 1) + nappe(36, 120, "#B42318", -1) + nappe(26, 120, "#1F5FA8", -1)
    s += (f'<path d="M{Ax} {Ay + 150}V{Ay - 160}" stroke="#46525C" stroke-dasharray="8 3 2 3"/>'
          f'<path d="M{Ax} {Ay - 160}l-5 10h10z" fill="#46525C"/>'
          f'<text x="{Ax + 8}" y="{Ay - 150}" font-size="15" font-style="italic" font-weight="700">n</text>'
          f'<circle cx="{Ax}" cy="{Ay}" r="4" fill="#1C2530"/><text x="{Ax + 8}" y="{Ay + 18}" font-size="15" '
          'font-style="italic" font-weight="700">A</text>'
          f'<path d="M{Ax} {Ay - 70}A70 70 0 0 1 {Ax + 70 * math.sin(math.radians(36)):.1f} {Ay - 70 * math.cos(math.radians(36)):.1f}" '
          'fill="none" stroke="#B42318"/>'
          f'<text x="{Ax + 22}" y="{Ay - 76}" font-size="14" fill="#B42318" font-weight="700">φs</text>'
          f'<path d="M{Ax} {Ay - 100}A100 100 0 0 0 {Ax - 100 * math.sin(math.radians(26)):.1f} {Ay - 100 * math.cos(math.radians(26)):.1f}" '
          'fill="none" stroke="#1F5FA8"/>'
          f'<text x="{Ax - 40}" y="{Ay - 104}" font-size="14" fill="#1F5FA8" font-weight="700">φ</text>'
          '<text x="20" y="120" font-size="13" fill="#1B7A43">solide 1</text><text x="20" y="250" font-size="13" '
          'fill="#B26A00">solide 2</text>'
          f'<text x="450" y="{Ay - 42}" font-size="13" fill="#46525C">plan tangent (t) en A</text>'
          '<text x="440" y="300" font-size="13" fill="#B42318">cône d\'adhérence (φs)</text>'
          '<text x="440" y="318" font-size="13" fill="#1F5FA8">cône de frottement (φ)</text>'
          '<text x="20" y="30" font-size="14" font-weight="700">φs &gt; φ</text></svg>')
    return s


def render(h, planches):
    obj = "".join(f"<li>{o}</li>" for o in OBJECTIFS)
    pre = "".join(f"<li>{p}</li>" for p in PREREQUIS)
    fiche = (f'<div class="c-fiche"><div><h3>Objectifs</h3><ul>{obj}</ul></div>'
             f"<div><h3>Prérequis</h3><ul>{pre}</ul></div></div>")
    planches["pl-trottoir"] = TROTTOIR["cfg"]
    sections = [("cg-cone", "Angle et cône de frottement"), ("cg-lois", "Les lois du frottement, lues sur une figure"),
                ("cg-trois", "Méthode : trois forces et un cône"), ("cg-trottoir", "La voiture monte-t-elle sur le trottoir ?"),
                ("cg-roul", "Résistance au roulement : lecture graphique"), ("cg-ess", "L'essentiel"), ("cg-quiz", "Quiz")]
    s1 = h.course_section(1, "cg-cone", "Angle et cône de frottement",
        "<p>Chacun des coefficients du cours 1 est la tangente d'un angle. On définit ainsi un <b>angle de frottement "
        "statique</b> φ<sub>s</sub>, ou angle d'adhérence, et un <b>angle de frottement</b> φ :</p>"
        '<div class="formule"><span class="f-main">µ<sub>s</sub> = f<sub>s</sub> = tan φ<sub>s</sub> ; µ = f = tan φ</span>'
        '<span class="f-units">φ<sub>s</sub> est l\'inclinaison limite de l\'action de contact sur la normale quand il '
        "y a adhérence ; φ, son inclinaison quand il y a glissement</span></div>"
        "<p>Utilisé avec les résolutions graphiques, le <b>cône de frottement</b> permet de donner une « image » au "
        "frottement et de simplifier les études.</p>"
        '<div class="c-split"><div><h3>Caractéristiques</h3><ul>'
        "<li>(A) est le point de contact entre les solides (1) et (2).</li>"
        "<li>(t) est le plan tangent en A au contact entre (1) et (2).</li>"
        "<li>(<i>n</i>), appelée <b>normale au contact</b>, est perpendiculaire en A à (t).</li>"
        "<li>Le cône de frottement est le cône de sommet A, d'axe <i>n</i>, et de demi-angle au sommet φ (cône de "
        "frottement) ou φ<sub>s</sub> (cône d'adhérence).</li></ul></div>"
        f'<figure class="c-fig">{svg_cones()}<figcaption>Cône de frottement et cône d\'adhérence.</figcaption></figure></div>'
        '<div class="remarque"><p><b>Remarque :</b> dans la plupart des exercices, et dans un but de simplification, on '
        "confond adhérence et frottement (φ<sub>s</sub> = φ et µ<sub>s</sub> = µ = tan φ). Ce qui est vrai dans un plan "
        "l'est également dans toutes les directions de l'espace autour de l'axe <i>n</i> : c'est pourquoi on parle de "
        "<b>cône</b>.</p></div>")
    s2 = h.course_section(2, "cg-lois", "Les lois du frottement, lues sur une figure",
        "<p>Les lois sont exprimées pour deux solides (0) et (1) en contact en un point A ; <i>A</i><sub>0/1</sub> "
        "schématise l'action exercée par 0 sur 1, α est son inclinaison sur la normale. Un cône de frottement aide à "
        "comprendre et simplifie les interprétations.</p>"
        '<div class="cg-cas"><div><h3>a) Adhérence</h3><p>Il n\'y a pas de mouvement ; la force d\'adhérence '
        "<i>T</i><sub>a</sub> s'oppose au mouvement éventuel de (1) par rapport à (0) ; <i>A</i><sub>0/1</sub> est "
        "<b>contenue dans le cône d'adhérence</b> :</p><p class=\"f-main\">α ≤ φ<sub>s</sub> ⇔ T<sub>a</sub> ≤ "
        "µ<sub>s</sub>·N</p></div>"
        "<div><h3>b) Équilibre limite (strict)</h3><p>Il y a adhérence, dans le cas particulier où "
        "<i>A</i><sub>0/1</sub> est <b>située sur le cône d'adhérence</b> :</p><p class=\"f-main\">α = φ<sub>s</sub> "
        "⇔ T<sub>a</sub> = µ<sub>s</sub>·N</p></div>"
        "<div><h3>c) Frottement avec glissement</h3><p>La force de frottement <i>T</i> est opposée à la vitesse de "
        "glissement <i>V</i><sub>A1/0</sub> ; <i>A</i><sub>0/1</sub> est <b>toujours sur le cône de frottement</b>, du "
        "côté opposé au mouvement :</p><p class=\"f-main\">α = φ ⇔ T = µ·N</p></div></div>"
        '<div class="simu" id="cg-cone-simu"><h3>Manipule : où est l\'action de contact ?</h3>'
        "<p>Fais glisser l'extrémité de <i>A</i><sub>0/1</sub> (ou utilise les flèches du clavier sur la figure). Le "
        "solide 1 tend à glisser vers la gauche : la composante tangentielle doit s'opposer à ce mouvement.</p>"
        '<div class="simu-grid"><label><span>Coefficient f = tan φ : <output id="cg-f-o">0,40</output></span>'
        '<input type="range" id="cg-f" min="0.05" max="1" step="0.01" value="0.4"></label></div>'
        '<svg viewBox="0 0 640 300" id="cg-cone-svg" tabindex="0" role="img" aria-label="Contact en A, cône de '
        'frottement et action de contact déplaçable ; son inclinaison et son état s\'affichent sous la figure"></svg>'
        '<div class="simu-out"><div><span>Inclinaison α</span><b id="cg-al">–</b></div><div><span>Demi-angle φ</span>'
        '<b id="cg-phi">–</b></div><div><span>T / N</span><b id="cg-tn">–</b></div><div><span>f</span><b id="cg-fv">–</b></div></div>'
        '<p class="simu-verdict" id="cg-etat" aria-live="polite"></p></div>'
        "<h3>Jeu : dans, sur ou hors du cône ?</h3>" +
        h.jeu_html([("Un colis immobile, poussé doucement", "dans"),
                    ("Un colis qui glisse à vitesse constante", "sur"),
                    ("Une voiture garée, juste avant de glisser dans la pente", "sur"),
                    ("Un équilibre que le frottement ne permet pas", "hors"),
                    ("Une courroie qui entraîne sa poulie sans patiner", "dans"),
                    ("Un patin de frein qui frotte sur la jante", "sur")],
                   [("dans", "Dans le cône"), ("sur", "Sur le cône"), ("hors", "Hors du cône")], "cg-jeu"))
    s3 = h.course_section(3, "cg-trois", "Méthode : trois forces et un cône",
        "<p>Un solide soumis à trois forces non parallèles est en équilibre si leurs droites d'action sont "
        "<b>concourantes</b> et si leur somme est nulle (le <b>dynamique</b> est fermé). Avec un contact frottant, le "
        "cône dit où peut passer l'action de contact :</p><ol class=\"cg-meth\">"
        "<li><b>Isoler</b> le solide et faire le bilan : forces connues, directions connues, inconnues.</li>"
        "<li>Tracer les <b>deux droites d'action connues</b> : leur intersection est le point de concours I.</li>"
        "<li>La troisième action passe par son point d'application et par I.</li>"
        "<li>La <b>comparer au cône</b> en son point de contact : dedans, adhérence (l'équilibre est possible) ; sur, "
        "équilibre strict ou glissement ; dehors, l'équilibre est impossible : il y a glissement.</li>"
        "<li><b>Dynamique</b> : tracer la force connue à l'échelle, puis les parallèles aux deux autres droites "
        "d'action ; lire les normes.</li></ol>"
        "<p>Quand le point de concours n'est pas imposé (deux contacts frottants), les deux cônes délimitent une "
        "<b>zone</b> où I peut se trouver : c'est le cas de la voiture à quatre roues motrices (section suivante) et "
        "de l'<b>arc-boutement</b> (activité 7, le barbecue).</p>"
        '<p class="cours-defi">Toutes ces constructions se font sur la planche : '
        '<a href="?ex=atelier-graphique">atelier graphique</a>.</p>')
    s4 = h.course_section(4, "cg-trottoir", "La voiture monte-t-elle sur le trottoir ?",
        "<p>La voiture proposée est en équilibre dans la position indiquée : les roues avant sont décollées du sol (pas "
        "de contact en E) et sont en contact en B avec un trottoir de hauteur h. Les frottements en B et D sont "
        "caractérisés par f<sub>B</sub> = f<sub>D</sub> = 0,8. P (1 800 daN) schématise le poids du véhicule. La "
        "voiture peut-elle monter sur le trottoir sans élan ? On suppose f = f<sub>s</sub>.</p>"
        "<p>Choisis un cas, puis avance <b>étape par étape</b> ; « Construire moi-même » efface la démonstration et "
        "donne les outils de la planche sur le même fond.</p>" +
        C.planche_demo("pl-trottoir", TROTTOIR["cfg"], TROTTOIR["fond"], "Montée de trottoir sans élan") +
        '<div class="remarque"><p><b>Conclusion :</b> deux roues motrices ne suffisent pas, ni à l\'arrière (α = '
        f"{fr(TROTTOIR['al_a'], 1)}° &gt; φ en D), ni à l'avant (α<sub>B</sub> = {fr(TROTTOIR['al_c'], 1)}° &gt; φ en B) ; "
        "avec quatre roues motrices, une infinité de positions de I entre M et N conviennent : la voiture monte. Avec "
        f"les roues arrière seules, le plus haut trottoir franchissable mesure environ {fr(TROTTOIR['h_lim'], 0)} mm.</p></div>")
    s5 = h.course_section(5, "cg-roul", "Résistance au roulement : lecture graphique",
        f'<figure class="c-fig">{cours_analytique.svg_roulement()}<figcaption>L\'élément roulant est soumis à trois '
        "forces : la charge F et la force F<sub>R</sub>, appliquées en O, et l'action R du sol.</figcaption></figure>"
        "<p>Trois forces concourantes : l'action <i>R</i> du sol passe par le centre O. Comme le bourrelet la décale de "
        "a vers l'avant, elle est inclinée : sa composante horizontale équilibre <i>F</i><sub>R</sub>, sa composante "
        "verticale équilibre <i>F</i>. Les triangles semblables donnent directement :</p>"
        '<div class="formule"><span class="f-main">F<sub>R</sub> / F = a / r ⇔ F<sub>R</sub> = (a / r)·F = '
        "f<sub>R</sub>·F</span></div>"
        "<p>C'est la même lecture que pour le frottement : a / r joue le rôle de tan φ.</p>")
    cartes = [("Angle de frottement", "µ = tan φ : un coefficient de 0,8 donne φ ≈ 38,7° ; 0,15 donne 8,5°."),
              ("Cône", "Sommet : le point de contact ; axe : la normale ; demi-angle : φ (ou φ<sub>s</sub>)."),
              ("Dans le cône", "Adhérence : l'équilibre est possible, l'action peut prendre toute direction du cône."),
              ("Sur le cône", "Équilibre strict, ou glissement : l'action fait l'angle φ avec la normale, du côté opposé "
               "à la vitesse de glissement."),
              ("Hors du cône", "Impossible : il y a glissement, l'équilibre supposé n'existe pas."),
              ("Trois forces", "Concourantes, dynamique fermé ; la troisième droite d'action passe par le point de "
               "concours, puis on la compare au cône.")]
    s6 = h.course_section(6, "cg-ess", "L'essentiel à retenir",
        '<div class="cartes">' + "".join(f'<button type="button" class="carte" aria-expanded="false"><b>{t}</b>'
                                          f'<span class="dos">{d}</span></button>' for t, d in cartes) + "</div>")
    quiz = [("Le cône de frottement a pour sommet :", ["le centre de gravité", "le point de contact", "le point de concours"],
             1, "Son sommet est le point de contact, son axe la normale au contact."),
            ("f = 0,6. Le demi-angle du cône vaut environ :", ["31°", "37°", "60°"], 0, "φ = arctan 0,6 ≈ 30,96°."),
            ("L'action de contact est à l'intérieur du cône. Il y a :", ["glissement", "adhérence", "arc-boutement forcément"], 1,
             "Dans le cône : α < φ<sub>s</sub>, T < µ<sub>s</sub>·N, pas de glissement."),
            ("En glissement, l'action de contact est :", ["dans le cône", "sur le cône, du côté opposé au mouvement",
                                                          "perpendiculaire au contact"], 1,
             "T = µ·N : l'action est inclinée de φ, et sa composante tangentielle s'oppose à la vitesse de glissement."),
            ("Trois forces non parallèles en équilibre sont :", ["parallèles", "concourantes", "de même norme"], 1,
             "Leurs droites d'action se coupent en un même point ; leur somme est nulle."),
            ("La troisième droite d'action tombe hors du cône. Conclusion :", ["l'équilibre est impossible : il y a glissement",
                                                                             "l'équilibre est strict", "il faut changer d'échelle"], 0,
             "Le contact ne peut pas transmettre une action hors de son cône : l'équilibre supposé n'existe pas."),
            ("Dans l'exemple du trottoir, pourquoi la voiture à quatre roues motrices monte-t-elle ?",
             ["elle est plus légère", "il existe des points I entre M et N où les deux actions restent dans leurs cônes",
              "les roues avant ne touchent pas le trottoir"], 1,
             "Avec deux contacts frottants, la position de I n'est plus imposée : il suffit qu'elle soit dans la zone "
             "commune aux deux cônes."),
            ("Dans le dynamique, les forces sont mises :", ["bout à bout, à l'échelle", "toutes au même point",
                                                           "sur leurs droites d'action"], 0,
             "Mises bout à bout à l'échelle des forces, elles forment un triangle fermé : leur somme est nulle.")]
    quiz_s = h.quiz_section(7, "cg-quiz", quiz, "cg-q")
    foot = ('<div class="cours-foot no-print"><a class="btn" href="?ex=atelier-graphique">Atelier : la planche de '
            'construction</a><a class="btn ghost" href="?ex=cle-excentrique">S\'entraîner : Activité 2</a>'
            '<a class="btn ghost" href="?ex=barbecue-arc-boutement">Activité 7</a>'
            '<a class="btn ghost" href="?ex=cours-frottement-analytique">Cours 1</a>'
            f'<a class="btn ghost" href="?">{h.HOUSE} Accueil</a></div>')
    head = h.course_head("Cours 2", "Graphique", "Frottement : résolution graphique",
                         "Angle et cône de frottement, lecture graphique des lois de Coulomb, méthode des trois forces : "
                         "la montée de trottoir construite pas à pas sur la planche, puis à refaire soi-même.")
    return (f'<div class="cours">{head}<nav class="c-top" aria-label="Navigation"><a href="?">{h.HOUSE} Accueil</a></nav>'
            f"{fiche}{h.course_nav(sections)}{s1}{s2}{s3}{s4}{s5}{s6}{quiz_s}{foot}</div>")


JS = r"""
  function initCoursGraphique(root) {
    var sv = root.querySelector("#cg-cone-svg");
    if (!sv) return;
    var fIn = root.querySelector("#cg-f"), ang = 14, drag = false;   // ang : inclinaison sur la normale (°, + vers la droite)
    var Ax = 320, Ay = 210, L = 150;
    function deg(a) { return a * Math.PI / 180; }
    function draw() {
      var f = +fIn.value, phi = Math.atan(f) * 180 / Math.PI, a = ang, al = Math.abs(a), R = 175;
      var tx = Ax + L * Math.sin(deg(a)), ty = Ay - L * Math.cos(deg(a));
      var e1x = Ax + R * Math.sin(deg(phi)), e1y = Ay - R * Math.cos(deg(phi)), e2x = Ax - R * Math.sin(deg(phi));
      var s = '<rect width="640" height="300" fill="#fff"/>' +
        '<path d="M60 250Q320 170 580 250L580 300L60 300Z" fill="#E4E7EA" stroke="#59636B"/>' +
        '<path d="M150 170Q320 250 490 170L490 112L150 112Z" fill="#F3F1EA" stroke="#59636B"/>' +
        '<path d="M' + Ax + " " + Ay + "L" + e1x + " " + e1y + "A" + R + " " + R + " 0 0 0 " + e2x + " " + e1y + 'Z" fill="rgba(242,183,5,.22)" stroke="#B26A00" stroke-dasharray="6 3"/>' +
        '<path d="M' + Ax + " " + Ay + "V20" + '" stroke="#46525C" stroke-dasharray="8 3 2 3"/><text x="' + (Ax + 6) + '" y="30" font-size="15" font-style="italic" font-weight="700">n</text>' +
        '<path d="M70 ' + Ay + 'H570" stroke="#A5ADAA" stroke-dasharray="4 3"/><text x="570" y="' + (Ay - 6) + '" font-size="13" text-anchor="end" fill="#46525C">t</text>' +
        '<text x="160" y="132" font-size="13">solide 1</text><text x="70" y="290" font-size="13">solide 0</text>' +
        '<path d="M110 52H50" stroke="#1C2530" stroke-width="2"/><path d="M44 52l9-5v10z"/><text x="40" y="40" font-size="12">mouvement éventuel de 1 par rapport à 0</text>';
      // composantes N et T
      var N = L * Math.cos(deg(a)), T = L * Math.sin(deg(a));
      s += '<path d="M' + Ax + " " + Ay + "V" + (Ay - N) + "H" + tx + '" stroke="#1F5FA8" stroke-dasharray="4 3" fill="none"/>' +
        '<text x="' + (Ax - 18) + '" y="' + (Ay - N / 2) + '" font-size="13" font-style="italic" fill="#1F5FA8" font-weight="700">N</text>' +
        '<text x="' + (Ax + T / 2 - 4) + '" y="' + (Ay - N - 6) + '" font-size="13" font-style="italic" fill="#1F5FA8" font-weight="700">T</text>';
      var out = al > phi + 0.25, on = Math.abs(al - phi) <= 0.25, col = out ? "#B42318" : (on ? "#B26A00" : "#1B7A43");
      var hx = tx - 12 * Math.sin(deg(a)), hy = ty + 12 * Math.cos(deg(a));
      s += '<path d="M' + Ax + " " + Ay + "L" + hx + " " + hy + '" stroke="' + col + '" stroke-width="4"/>' +
        '<path d="M' + tx + " " + ty + "L" + (hx - 6 * Math.cos(deg(a))) + " " + (hy - 6 * Math.sin(deg(a))) + "L" + (hx + 6 * Math.cos(deg(a))) + " " + (hy + 6 * Math.sin(deg(a))) + 'Z" fill="' + col + '"/>' +
        '<circle cx="' + tx + '" cy="' + ty + '" r="11" fill="rgba(242,183,5,.35)" stroke="#1C2530" class="cg-poignee"/>' +
        '<text x="' + (tx + 14) + '" y="' + (ty - 4) + '" font-size="15" font-style="italic" font-weight="700" fill="' + col + '">A0/1</text>' +
        '<circle cx="' + Ax + '" cy="' + Ay + '" r="4" fill="#1C2530"/><text x="' + (Ax - 18) + '" y="' + (Ay + 18) + '" font-size="15" font-style="italic" font-weight="700">A</text>';
      sv.innerHTML = s;
      root.querySelector("#cg-f-o").textContent = fr(f, 2);
      root.querySelector("#cg-al").textContent = fr(al, 1) + " °"; root.querySelector("#cg-phi").textContent = fr(phi, 1) + " °";
      root.querySelector("#cg-tn").textContent = fr(Math.abs(Math.tan(deg(a))), 2); root.querySelector("#cg-fv").textContent = fr(f, 2);
      var e = root.querySelector("#cg-etat"), wrong = a < -0.25;
      if (out) { e.textContent = "Hors du cône (α > φ) : le contact ne peut pas transmettre cette action. L'équilibre est impossible, il y a glissement."; e.className = "simu-verdict ko"; }
      else if (on) { e.textContent = "Sur le cône (α = φ) : équilibre strict, ou glissement avec T = µ·N."; e.className = "simu-verdict lim"; }
      else { e.textContent = "Dans le cône (α < φ) : adhérence, l'équilibre est possible sans glissement (T < µ·N)."; e.className = "simu-verdict ok"; }
      if (wrong && !out) e.textContent += " Attention : ici T est dirigée vers la gauche, dans le sens du mouvement éventuel ; la force d'adhérence doit s'y opposer.";
    }
    function fromEvent(ev) {
      var r = sv.getBoundingClientRect(), x = (ev.clientX - r.left) * 640 / r.width, y = (ev.clientY - r.top) * 300 / r.height;
      var a = Math.atan2(x - Ax, Ay - y) * 180 / Math.PI;
      ang = Math.max(-80, Math.min(80, Math.round(a * 2) / 2)); draw();
    }
    sv.addEventListener("pointerdown", function (ev) { drag = true; sv.setPointerCapture(ev.pointerId); fromEvent(ev); });
    sv.addEventListener("pointermove", function (ev) { if (drag) fromEvent(ev); });
    sv.addEventListener("pointerup", function () { drag = false; });
    sv.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowLeft" || ev.key === "ArrowDown") { ang = Math.max(-80, ang - 0.5); ev.preventDefault(); draw(); }
      if (ev.key === "ArrowRight" || ev.key === "ArrowUp") { ang = Math.min(80, ang + 0.5); ev.preventDefault(); draw(); }
    });
    fIn.addEventListener("input", draw);
    draw();
  }
"""

CSS = """
/* ---------- cours 2 : résolution graphique ---------- */
.cg-cas{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; margin:10px 0}
.cg-cas>div{background:#fff; border:2px solid var(--encre); padding:4px 14px 10px; font-size:.95rem}
.cg-cas h3{margin:6px 0 4px!important}
.cg-cas .f-main{font:700 1.1rem var(--f-titre); color:var(--rouge); margin:6px 0 0}
@media (max-width:860px){ .cg-cas{grid-template-columns:1fr} }
#cg-cone-svg{touch-action:none; cursor:grab}
.cg-meth li{margin:.3rem 0}
"""
