"""Atelier graphique (?ex=atelier-graphique) : la planche de construction en accès libre.

Une feuille quadrillée vierge, ou l'un des fonds des activités et du cours 2 (mécanisme dessiné à l'échelle et ses
éléments donnés, sans correction), l'échelle des forces au choix, le mode d'emploi des outils et la méthode des
trois forces. Rien n'est noté : c'est la feuille de brouillon de la statique graphique.
"""
import activites
import construction as C
import cours_graphique

W0, H0 = 260, 180
FORCES = {"u": "daN", "choix": [0.5, 1, 2, 5, 10, 20, 25, 50, 100], "def": 3}


def _fonds():
    """(clé, intitulé, configuration, fond SVG) ; la première est le fond de départ."""
    vierge = {"w": W0, "h": H0, "kL": 1, "given": [], "echTxt": "Feuille quadrillée (mm) · longueurs à l'échelle 1:1",
              "titre": "Feuille de construction"}
    out = [("vierge", "Feuille quadrillée", vierge, "")]
    for k, t, src in (("cle", "Clé à excentrique (activité 2)", activites.CLE),
                      ("pente", "Voiture en pente (activité 3)", activites.PENTE_PL),
                      ("barbecue", "Barbecue de cheminée (activité 7)", activites.BBQ),
                      ("trottoir", "Montée de trottoir (cours 2)", cours_graphique.TROTTOIR)):
        c = src["cfg"]
        e = c["echTxt"].split(" · forces")[0]
        out.append((k, t, {"w": c["w"], "h": c["h"], "kL": c["kL"], "given": c["given"], "echTxt": e,
                           "titre": c["titre"]}, src["fond"]))
    return out


FONDS = _fonds()


def fonds_templates():
    return [f'<template id="pl-fond-{k}">{fond}</template>' for k, _t, _c, fond in FONDS]


def render(h, planches):
    fonds = {k: dict(c, grille=C.grille(c["w"], c["h"])) for k, _t, c, _f in FONDS}
    cfg = {"w": W0, "h": H0, "kL": 1, "given": [], "outil": "dr", "forces": FORCES, "fonds": fonds,
           "echTxt": FONDS[0][2]["echTxt"], "titre": "Feuille de construction"}
    planches["atelier"] = cfg
    head = h.course_head("Atelier", "", "Planche de construction graphique",
                         "La feuille de brouillon de la statique graphique : droites d'action, parallèles, cônes de "
                         "frottement, vecteurs à l'échelle des forces. Choisis un fond, construis, mesure, imprime à "
                         "l'échelle. Rien n'est noté ni enregistré.")
    mode = activites.DT2.replace('<div class="doc-text">', '<div class="at-doc">')
    planche = C.planche_libre("atelier", cfg, "", "Planche de construction libre", [(k, t) for k, t, _c, _f in FONDS])
    return (f'<div class="cours atelier">{head}<nav class="c-top" aria-label="Navigation"><a href="?">{h.HOUSE} '
            f"Accueil</a></nav>"
            + h.course_section(1, "at-planche", "La planche",
                               '<p class="small">Astuce : commence par un fond d\'activité, puis retrouve sa correction '
                               "en ouvrant l'activité (mode entraînement).</p>" + planche)
            + h.course_section(2, "at-mode", "Mode d'emploi et méthode", mode)
            + '<div class="cours-foot no-print"><a class="btn" href="?ex=cours-frottement-graphique">Cours 2 : résolution '
              'graphique</a><a class="btn ghost" href="?ex=cle-excentrique">Activité 2</a><a class="btn ghost" '
              'href="?ex=voiture-pente">Activité 3</a><a class="btn ghost" href="?ex=barbecue-arc-boutement">Activité 7</a>'
              f'<a class="btn ghost" href="?">{h.HOUSE} Accueil</a></div></div>')


JS = r"""
  function initAtelier(root) { /* la planche est initialisée par initCommun (Planche.initAll) */ }
"""

CSS = """
/* ---------- atelier graphique ---------- */
.at-doc{columns:2; column-gap:28px; font-size:.95rem}
.at-doc h3{break-after:avoid; font:700 1.05rem var(--f-titre); margin:6px 0 4px}
.at-doc ul,.at-doc ol{padding-left:1.2rem}
.at-doc li{margin:.2rem 0; break-inside:avoid}
@media (max-width:860px){ .at-doc{columns:1} }
.atelier .pl{border-left:0; padding-left:0}
"""
