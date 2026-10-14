"""Cours — Frottement et roulement (?ex=cours-frottement-roulement).

Source : manuel, chapitre 9 « Frottement et roulement », pages 123 à 131 (src/images/originaux/cours-p123 à p131).
Le cours reprend ce qui se calcule : adhérence et frottement, coefficients, lois de Coulomb écrites en égalités et
inégalités, résistance au roulement et ses deux exemples. La résolution graphique du chapitre (cône de frottement,
lecture graphique des lois, montée de trottoir, pages 126 à 129) n'est pas traitée sur le site. Le texte du manuel est
conservé ; ses figures, photographiées, sont redessinées en SVG ; le colis de l'exemple 1 et l'automobile de l'exemple
de roulement deviennent des simulateurs.
"""
import math

OBJECTIFS = ["Définir les notions d'adhérence, de frottement et les paramètres utilisés pour l'étude du frottement.",
             "Énoncer les lois du frottement (lois de Coulomb) et les écrire sous forme d'égalités et d'inégalités.",
             "Décrire la notion de résistance au roulement et calculer la force qu'elle oppose au mouvement."]
PREREQUIS = ["Principe fondamental de la statique (solide soumis à des forces, moments).",
             "Trigonométrie du triangle rectangle (tangente d'un angle)."]

MATERIAUX = [("acier sur acier", 0.18, 0.15), ("acier sur fonte", 0.19, 0.16), ("acier sur bronze", 0.11, 0.10),
             ("téflon sur acier", 0.04, 0.04), ("bois sur bois", 0.65, 0.40), ("métaux sur bois", 0.6, 0.5),
             ("pneu de voiture sur route sèche", 0.8, 0.6)]


def svg_exemples():
    """Trois exemples dont le fonctionnement repose sur le frottement (page 123) : frein, courroie, serre-joint."""
    frein = ('<svg viewBox="0 0 200 150" role="img" aria-label="Frein de vélo : deux patins serrés contre la jante">'
             '<circle cx="100" cy="150" r="96" fill="none" stroke="#46525C" stroke-width="10"/>'
             '<circle cx="100" cy="150" r="80" fill="none" stroke="#A5ADAA" stroke-width="3"/>'
             '<rect x="44" y="34" width="16" height="30" rx="3" fill="#B26A00" transform="rotate(-34 52 49)"/>'
             '<rect x="140" y="34" width="16" height="30" rx="3" fill="#B26A00" transform="rotate(34 148 49)"/>'
             '<path d="M30 30l18 12M170 30l-18 12" stroke="#B42318" stroke-width="3"/>'
             '<path d="M52 44l-6-10M148 44l6-10" stroke="#1C2530" stroke-width="2"/>'
             '<text x="100" y="22" text-anchor="middle" font-size="13" font-weight="700">serrage F</text></svg>')
    courroie = ('<svg viewBox="0 0 200 150" role="img" aria-label="Transmission par courroie entre deux poulies">'
                '<circle cx="62" cy="80" r="42" fill="#E4E7EA" stroke="#46525C" stroke-width="2"/>'
                '<circle cx="152" cy="80" r="22" fill="#E4E7EA" stroke="#46525C" stroke-width="2"/>'
                '<path d="M62 38L152 58M62 122L152 102" stroke="#1C2530" stroke-width="5"/>'
                '<path d="M62 38A42 42 0 0 0 62 122M152 58A22 22 0 0 1 152 102" fill="none" stroke="#1C2530" stroke-width="5"/>'
                '<circle cx="62" cy="80" r="5" fill="#1C2530"/><circle cx="152" cy="80" r="4" fill="#1C2530"/>'
                '<path d="M36 70a28 28 0 0 1 20-24" fill="none" stroke="#B42318" stroke-width="2.5"/>'
                '<path d="M60 44l-6 7 9 1z" fill="#B42318"/></svg>')
    serre = ('<svg viewBox="0 0 200 150" role="img" aria-label="Serre-joint : la pièce anti-recul s\'arc-boute sur la '
             'barre de guidage">'
             '<rect x="8" y="64" width="186" height="14" fill="#7FA3CF" stroke="#1F5FA8"/>'
             '<rect x="150" y="36" width="20" height="70" fill="#A5ADAA" stroke="#46525C"/>'
             '<path d="M62 40h40v70H62z" fill="#E4E7EA" stroke="#46525C"/>'
             '<path d="M58 48l14 52" stroke="#B42318" stroke-width="5"/>'
             '<text x="20" y="130" font-size="12" fill="#B42318" font-weight="700">pièce anti-recul arc-boutée</text>'
             '<text x="106" y="30" font-size="12">corps d\'appui fixe</text></svg>')
    return frein, courroie, serre


def svg_roulement():
    """Figure 15 redessinée : bourrelet de matière, actions sur l'élément roulant, trois forces concourantes."""
    s = '<svg viewBox="0 0 760 230" role="img" aria-label="Résistance au roulement : un bourrelet de matière se forme ' \
        'devant la roue ; la résultante R des pressions de contact passe par le centre O, décalée de a vers l\'avant">'
    s += ('<defs><marker id="fr-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
          '<path d="M0 0L10 5L0 10z" fill="#B42318"/></marker></defs>')
    # 1 : la roue et le bourrelet
    s += ('<path d="M20 175H230" stroke="#8A7350" stroke-width="2"/><rect x="20" y="175" width="210" height="14" fill="#E9DCC6"/>'
          '<circle cx="110" cy="115" r="60" fill="#fff" stroke="#1C2530" stroke-width="2"/>'
          '<path d="M128 172q14-6 26 3" fill="#E9DCC6" stroke="#8A7350" stroke-width="2"/>'
          '<circle cx="110" cy="115" r="3" fill="#1C2530"/><text x="96" y="132" font-size="13" font-style="italic">O</text>'
          '<path d="M110 115L150 72" stroke="#1C2530"/><text x="134" y="88" font-size="13" font-style="italic">r</text>'
          '<text x="92" y="172" font-size="12" font-style="italic">a</text><text x="138" y="168" font-size="12" font-style="italic">b</text>'
          '<path d="M60 40a70 70 0 0 1 90 0" fill="none" stroke="#1C2530" marker-end="url(#fr-a)"/>'
          '<text x="78" y="30" font-size="12">mouvement</text>'
          '<text x="125" y="204" font-size="12" text-anchor="middle">bourrelet de matière</text>'
          '<text x="125" y="219" font-size="12" text-anchor="middle">qui s\'oppose au déplacement</text>')
    s += '<text x="260" y="120" font-size="26">⇔</text>'
    # 2 : les actions
    s += ('<circle cx="390" cy="115" r="60" fill="#FBF6EA" stroke="#1C2530" stroke-width="2"/>'
          '<path d="M370 172q20 18 44 2" fill="#E9DCC6" stroke="#8A7350" stroke-width="2"/>'
          '<path d="M390 115V160" stroke="#B42318" stroke-width="2.5" marker-end="url(#fr-a)"/>'
          '<path d="M390 115H436" stroke="#B42318" stroke-width="2.5" marker-end="url(#fr-a)"/>'
          '<text x="374" y="150" font-size="14" font-style="italic" fill="#B42318" font-weight="700">F</text>'
          '<text x="420" y="108" font-size="14" font-style="italic" fill="#B42318" font-weight="700">F<tspan font-size="10" dy="3">R</tspan></text>'
          '<path d="M380 182l6-8M392 186l4-9M404 184l1-9" stroke="#B42318" stroke-width="1.5"/>'
          '<text x="410" y="200" font-size="12">pressions de contact entre a et b</text>')
    s += '<text x="490" y="120" font-size="26">⇔</text>'
    # 3 : trois forces concourantes en O
    s += ('<circle cx="640" cy="115" r="60" fill="#FBF6EA" stroke="#1C2530" stroke-width="2"/>'
          '<path d="M640 115V50" stroke="#46525C" stroke-dasharray="5 3"/>'
          '<path d="M640 115V165" stroke="#B42318" stroke-width="2.5" marker-end="url(#fr-a)"/>'
          '<path d="M640 115H686" stroke="#B42318" stroke-width="2.5" marker-end="url(#fr-a)"/>'
          '<path d="M664 196L642 120" stroke="#1F5FA8" stroke-width="2.5" marker-end="url(#fr-a)"/>'
          '<text x="672" y="186" font-size="14" font-style="italic" fill="#1F5FA8" font-weight="700">R</text>'
          '<text x="624" y="150" font-size="14" font-style="italic" fill="#B42318" font-weight="700">F</text>'
          '<text x="670" y="108" font-size="14" font-style="italic" fill="#B42318" font-weight="700">F<tspan font-size="10" dy="3">R</tspan></text>'
          '<path d="M640 212H664M640 206v12M664 206v12" stroke="#2E7D5B"/><text x="648" y="226" font-size="12" '
          'fill="#2E7D5B" font-style="italic">a</text><text x="628" y="110" font-size="13" font-style="italic">O</text></svg>')
    return s


def svg_auto():
    """Figure 16 redessinée : automobile de 1 100 kg, actions du sol et forces de résistance au roulement ; les
    valeurs sont posées par le simulateur."""
    return ('<svg viewBox="0 0 760 270" id="ca-auto" role="img" aria-label="Automobile au ralenti à vitesse constante : '
            'actions du sol R_A et R_B, résistances au roulement en A et B, force motrice F_m">'
            '<defs><marker id="ca-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" fill="#B42318"/></marker><marker id="ca-ab" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#1F5FA8"/></marker></defs>'
            '<rect x="0" y="0" width="760" height="270" fill="#fff"/>'
            '<path d="M90 170C92 128 150 116 220 112L300 82C330 66 400 66 440 84L480 108C560 112 620 122 640 144L646 170Z" '
            'fill="#F3F1EA" stroke="#46525C" stroke-width="2"/><path d="M318 88L352 74H418L452 104H318Z" fill="#CFE0EE" stroke="#46525C"/>'
            '<circle cx="190" cy="168" r="34" fill="#46525C"/><circle cx="190" cy="168" r="16" fill="#E4E7EA"/>'
            '<circle cx="540" cy="168" r="34" fill="#46525C"/><circle cx="540" cy="168" r="16" fill="#E4E7EA"/>'
            '<path d="M20 202H740" stroke="#8A7350" stroke-width="2"/>'
            '<text x="452" y="40" font-size="13">déplacement au ralenti à vitesse constante →</text>'
            '<path d="M370 120V200" stroke="#B42318" stroke-width="2.5" marker-end="url(#ca-ar)"/>'
            '<text x="378" y="160" font-size="14" font-style="italic" font-weight="700" fill="#B42318">P</text>'
            '<text x="378" y="177" font-size="12" id="ca-vP" fill="#B42318"></text>'
            '<path d="M190 250V206" stroke="#1F5FA8" stroke-width="2.5" marker-end="url(#ca-ab)"/>'
            '<path d="M540 250V206" stroke="#1F5FA8" stroke-width="2.5" marker-end="url(#ca-ab)"/>'
            '<text x="198" y="242" font-size="14" font-style="italic" font-weight="700" fill="#1F5FA8">R<tspan font-size="10" dy="3">A</tspan></text>'
            '<text x="548" y="242" font-size="14" font-style="italic" font-weight="700" fill="#1F5FA8">R<tspan font-size="10" dy="3">B</tspan></text>'
            '<text x="198" y="258" font-size="12" id="ca-vRA" fill="#1F5FA8"></text><text x="548" y="258" font-size="12" id="ca-vRB" fill="#1F5FA8"></text>'
            '<path d="M188 202H140" stroke="#B42318" stroke-width="2.5" marker-end="url(#ca-ar)"/>'
            '<path d="M538 202H490" stroke="#B42318" stroke-width="2.5" marker-end="url(#ca-ar)"/>'
            '<text x="96" y="194" font-size="13" font-style="italic" font-weight="700" fill="#B42318">F<tspan font-size="9" dy="3">rrA</tspan></text>'
            '<text x="444" y="194" font-size="13" font-style="italic" font-weight="700" fill="#B42318">F<tspan font-size="9" dy="3">rrB</tspan></text>'
            '<text x="70" y="222" font-size="12" id="ca-vFA" fill="#B42318"></text><text x="420" y="222" font-size="12" id="ca-vFB" fill="#B42318"></text>'
            '<path d="M646 150H730" stroke="#B42318" stroke-width="2.5" marker-end="url(#ca-ar)"/>'
            '<text x="660" y="140" font-size="13" font-style="italic" font-weight="700" fill="#B42318">F<tspan font-size="9" dy="3">m</tspan></text>'
            '<text x="660" y="172" font-size="12" id="ca-vFm" fill="#B42318"></text>'
            '<text x="604" y="124" font-size="12">force motrice nécessaire</text>'
            '<text x="182" y="226" font-size="13" font-style="italic" font-weight="700">A</text>'
            '<text x="532" y="226" font-size="13" font-style="italic" font-weight="700">B</text>'
            '<text x="372" y="112" font-size="13" font-style="italic" font-weight="700">G</text>'
            '<path d="M190 262H370M370 262H540" stroke="#2E7D5B"/><text x="270" y="268" font-size="11" fill="#2E7D5B" '
            'id="ca-vAG">1 260</text><text x="446" y="268" font-size="11" fill="#2E7D5B" id="ca-vGB">1 000</text></svg>')


def svg_roue_porteuse():
    """Figure 18 redessinée : actions exercées sur une roue porteuse de véhicule."""
    return ('<svg viewBox="0 0 700 290" role="img" aria-label="Roue porteuse : la charge P et la force motrice F_m sont '
            'appliquées au centre O ; le sol exerce R en A, à la distance a en avant du point I situé sous O, et la '
            'résistance au roulement F_rr">'
            '<defs><marker id="rp-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" fill="#B42318"/></marker></defs><rect width="700" height="290" fill="#fff"/>'
            '<path d="M60 236H640" stroke="#8A7350" stroke-width="2"/><rect x="60" y="236" width="580" height="12" fill="#E9DCC6"/>'
            '<path d="M180 236A170 170 0 0 1 520 236" fill="none" stroke="#46525C" stroke-width="16"/>'
            '<path d="M220 236A130 130 0 0 1 480 236" fill="none" stroke="#A5ADAA" stroke-width="4"/>'
            '<path d="M330 230Q350 244 392 232" fill="#E9DCC6" stroke="#8A7350"/>'
            '<circle cx="350" cy="66" r="6" fill="#1C2530"/><text x="326" y="58" font-size="15" font-style="italic" font-weight="700">O</text>'
            '<path d="M350 66V20" stroke="#1C2530"/><text x="356" y="26" font-size="13" font-style="italic">y</text>'
            '<path d="M350 66V150" stroke="#B42318" stroke-width="2.5" marker-end="url(#rp-a)"/>'
            '<text x="330" y="130" font-size="15" font-style="italic" font-weight="700" fill="#B42318">P</text>'
            '<path d="M350 66H430" stroke="#B42318" stroke-width="2.5" marker-end="url(#rp-a)"/>'
            '<text x="410" y="56" font-size="15" font-style="italic" font-weight="700" fill="#B42318">F<tspan font-size="11" dy="3">m</tspan></text>'
            '<path d="M374 236V156" stroke="#1F5FA8" stroke-width="2.5" marker-end="url(#rp-a)"/>'
            '<text x="382" y="176" font-size="15" font-style="italic" font-weight="700" fill="#1F5FA8">R</text>'
            '<path d="M372 236H300" stroke="#B42318" stroke-width="2.5" marker-end="url(#rp-a)"/>'
            '<text x="296" y="226" font-size="15" font-style="italic" font-weight="700" fill="#B42318">F<tspan font-size="11" dy="3">rr</tspan></text>'
            '<path d="M350 66V236" stroke="#46525C" stroke-dasharray="6 3"/>'
            '<text x="336" y="262" font-size="14" font-style="italic" font-weight="700">I</text>'
            '<text x="378" y="262" font-size="14" font-style="italic" font-weight="700">A</text>'
            '<path d="M350 276H374M350 270v12M374 270v12" stroke="#2E7D5B"/><text x="356" y="290" font-size="12" fill="#2E7D5B" font-style="italic">a</text>'
            '<path d="M560 236H640" stroke="#1C2530"/><text x="630" y="228" font-size="13" font-style="italic">x</text>'
            '<path d="M228 150a150 150 0 0 1 50-70" fill="none" stroke="#1C2530" marker-end="url(#rp-a)"/>'
            '<text x="120" y="112" font-size="13">ω constante</text>'
            '<path d="M320 66V236" stroke="#2E7D5B" stroke-width=".8"/><text x="290" y="160" font-size="12" fill="#2E7D5B" '
            'font-style="italic">r = OI</text></svg>')


def tors(rows, pt):
    cells = "".join(f"<span>{a}</span><span>{b}</span>" for a, b in rows)
    return f'<span class="tors"><span class="cr">{cells}</span><sub class="pt">{pt}</sub></span>'


def render(h):
    obj = "".join(f"<li>{o}</li>" for o in OBJECTIFS)
    pre = "".join(f"<li>{p}</li>" for p in PREREQUIS)
    fiche = (f'<div class="c-fiche"><div><h3>Objectifs</h3><ul>{obj}</ul></div>'
             f"<div><h3>Prérequis</h3><ul>{pre}</ul></div></div>")
    frein, courroie, serre = svg_exemples()
    sections = [("ca-intro", "Pourquoi étudier le frottement ?"), ("ca-adh", "Adhérence et frottement : le colis"),
                ("ca-coef", "Le facteur de frottement"), ("ca-lois", "Les lois du frottement (lois de Coulomb)"),
                ("ca-roul", "La résistance au roulement"), ("ca-ess", "L'essentiel"), ("ca-quiz", "Quiz")]
    s1 = h.course_section(1, "ca-intro", "Pourquoi étudier le frottement ?",
        "<p>Dans les chapitres précédents, les actions mécaniques de contact ont été schématisées par des vecteurs-forces "
        "perpendiculaires (ou normales) aux surfaces en contact : les frottements étaient négligés. Cette schématisation "
        "amène des erreurs systématiques relativement faibles dans la plupart des problèmes. Cependant, dans un certain "
        "nombre de cas, la prise en compte du frottement est nécessaire, soit pour en <b>diminuer les effets</b> (pertes "
        "d'énergie, amélioration du rendement…), soit pour l'<b>utiliser avec bénéfice</b> (freins, embrayages, "
        "courroies, arc-boutement, équilibre ou stabilité de certains mécanismes…).</p>"
        "<p>Voici des exemples dont le fonctionnement est lié aux propriétés du frottement :</p>"
        '<div class="ca-ex">'
        f'<figure>{frein}<figcaption><b>Système de freinage</b> : les patins serrés contre la jante freinent la roue ; '
        "le frottement transforme l'énergie du mouvement en chaleur.</figcaption></figure>"
        f'<figure>{courroie}<figcaption><b>Transmission par courroie</b> : c\'est l\'adhérence de la courroie sur les '
        "poulies qui transmet le mouvement, sans glissement.</figcaption></figure>"
        f'<figure>{serre}<figcaption><b>Serre-joint</b> : la pièce anti-recul s\'<b>arc-boute</b> sur la barre de '
        "guidage ; plus on serre, plus elle bloque (activité 6, le barbecue).</figcaption></figure></div>")
    mats = "".join(f'<option value="{i}"{" selected" if i == 6 else ""}>{n}</option>' for i, (n, _a, _b) in enumerate(MATERIAUX))
    s2 = h.course_section(2, "ca-adh", "Adhérence et frottement : le colis",
        '<div class="definition"><p>Si deux surfaces en contact se déplacent ou glissent l\'une par rapport à l\'autre, '
        "on dit qu'il y a <b>frottement</b>.</p><p>Lorsque ces deux surfaces tendent à glisser mais ne se déplacent pas, "
        "on dit qu'il y a <b>adhérence</b>.</p></div>"
        "<h3>Exemple 1 : un colis poussé sur un plan horizontal</h3>"
        "<p>Soit un colis (1) de poids <i>P</i> et de centre de gravité G, en équilibre sur un plan horizontal (0). "
        "Analysons le comportement du colis et l'évolution des actions de contact (plan/colis) lorsqu'on exerce une "
        "poussée latérale <i>F</i> graduellement croissante.</p>"
        "<p><b>a) Cas du repos.</b> <i>N</i> schématise la résultante des actions de contact exercées par le sol sur le "
        "colis. Celui-ci est en équilibre sous l'action des deux forces <i>N</i> et <i>P</i>, qui doivent être égales "
        "et opposées (ligne d'action : la verticale passant par G). Si on exerce sur le colis une poussée latérale "
        "<i>F</i> passant par G, deux cas sont possibles : adhérence ou frottement.</p>"
        "<p><b>b) Cas de l'adhérence.</b> Il n'y a pas de mouvement, le colis est en équilibre et le principe "
        "fondamental met en évidence une force d'adhérence <i>T</i><sub>a</sub> égale à <i>F</i> et de sens opposé : "
        "<i>T</i><sub>a</sub> s'oppose au déplacement éventuel de l'objet vers la droite ; <i>N</i> garde la même "
        "valeur : <i>N</i> = <i>P</i>. Si <i>F</i> devient assez grande (<i>F</i> &gt; <i>F</i><sub>limite</sub>), "
        "l'objet se met à glisser dans le même sens que <i>F</i> : on passe en phase de frottement.</p>"
        "<p>La valeur limite permet de définir le <b>rapport de frottement statique</b> µ<sub>s</sub> (ou "
        "<i>f</i><sub>s</sub>), encore appelé coefficient de frottement d'adhérence :</p>"
        '<div class="formule"><span class="f-main">µ<sub>s</sub> = f<sub>s</sub> = F<sub>limite</sub> / N = '
        'T<sub>a limite</sub> / N</span><span class="f-units">µ se lit « mu » ; µ<sub>s</sub> n\'a pas d\'unité</span></div>'
        "<p><b>c) Cas du frottement.</b> Si <i>F</i> &gt; <i>F</i><sub>limite</sub> = µ<sub>s</sub>·<i>N</i>, le colis se "
        "met à glisser. Il y a frottement entre le sol et le colis. Le glissement continuera à vitesse uniforme si "
        "<i>F</i> = µ·<i>N</i> (la valeur de µ·<i>N</i> étant légèrement inférieure à µ<sub>s</sub>·<i>N</i>). Le "
        "mouvement sera accéléré si <i>F</i> est supérieure à cette nouvelle valeur limite.</p>"
        '<div class="formule"><span class="f-main">N = P ; T = F = µ·N</span><span class="f-units">µ = f : facteur '
        "(ou coefficient) de frottement</span></div>"
        '<div class="remarque"><p><b>Remarques :</b> la force de frottement <i>T</i> = µ·<i>N</i> = <i>f</i>·<i>N</i> '
        "s'oppose au mouvement du colis et est à l'origine des pertes d'énergie par frottement. Si l'objet est arrêté, "
        "il faudra, pour le remettre en mouvement, fournir un effort <i>F</i> ≥ µ<sub>s</sub>·<i>N</i>. Les phases "
        "observées sont résumées par le graphique du simulateur ci-dessous.</p></div>"
        '<div class="simu" id="ca-colis"><h3>Simulateur : pousse le colis</h3>'
        '<div class="simu-grid"><label><span>Poussée <i>F</i> : <output id="ca-F-o">0 N</output></span>'
        '<input type="range" id="ca-F" min="0" max="100" step="1" value="0" aria-describedby="ca-etat"></label>'
        f'<label><span>Matériaux en contact</span><select id="ca-mat">{mats}</select></label>'
        '<label><span>Masse du colis : <output id="ca-m-o">20 kg</output></span>'
        '<input type="range" id="ca-m" min="5" max="60" step="1" value="20"></label>'
        '<label class="chk"><span>Après le démarrage</span><button type="button" class="btn ghost" id="ca-stop">'
        "Arrêter le colis</button></label></div>"
        '<svg viewBox="0 0 640 230" id="ca-colis-svg" role="img" aria-label="Le colis, les forces P, N, F et T, et le '
        'graphique de la force de contact tangentielle T en fonction de la poussée F"></svg>'
        '<div class="simu-out"><div><span>Action normale N</span><b id="ca-N">–</b></div>'
        '<div><span>Force tangentielle T</span><b id="ca-T">–</b></div><div><span>T / N</span><b id="ca-TN">–</b></div>'
        '<div><span>Seuil µ<sub>s</sub>·N</span><b id="ca-lim">–</b></div></div>'
        '<p class="simu-verdict" id="ca-etat" aria-live="polite"></p>'
        '<details class="simu-defi"><summary>Défi : à quelle poussée le colis de 20 kg démarre-t-il sur une route sèche '
        "(pneu sur route) ? Et quelle poussée suffit ensuite pour le faire glisser à vitesse constante ?</summary>"
        "<p>N = P = 20 × 9,81 = 196,2 N ; il démarre quand F dépasse µ<sub>s</sub>·N = 0,8 × 196,2 ≈ 157 N ; ensuite "
        "µ·N = 0,6 × 196,2 ≈ 118 N suffit à le faire glisser à vitesse constante.</p></details></div>")
    s3 = h.course_section(3, "ca-coef", "Le facteur de frottement",
        "<p>µ ou <i>f</i>, µ<sub>s</sub> ou <i>f</i><sub>s</sub> ne "
        "dépendent ni de l'intensité des efforts exercés, ni de l'étendue des surfaces en contact. Ils dépendent "
        "essentiellement de la <b>nature des matériaux</b> en contact et, dans une moindre mesure, de la qualité "
        "(<b>rugosité</b>) des surfaces en contact. µ varie aussi avec la <b>vitesse</b> relative de déplacement des "
        "surfaces en contact.</p>"
        "<h3>Valeurs indicatives de µ<sub>s</sub> et µ</h3>" + _table_coef() +
        '<p class="cours-defi">À toi : retrouve dans le tableau pourquoi on lubrifie les guidages et pourquoi on '
        "conduit moins vite sur route mouillée.</p>")
    s4 = h.course_section(4, "ca-lois", "Les lois du frottement (lois de Coulomb)",
        "<p>Les lois sont exprimées pour deux solides (0) et (1) en contact en un point A ; <i>A</i><sub>0/1</sub> "
        "schématise l'action exercée par 0 sur 1. On la décompose en une composante normale <i>N</i> (perpendiculaire "
        "au plan tangent du contact) et une composante tangentielle <i>T</i>.</p>"
        '<div class="ca-lois">'
        '<div class="ca-loi"><h3>a) Adhérence</h3><ul><li>Il n\'y a pas de mouvement.</li><li>La force d\'adhérence '
        "<i>T</i><sub>a</sub> s'oppose au mouvement éventuel de (1) par rapport à (0).</li></ul>"
        '<p class="f-main">T<sub>a</sub> ≤ µ<sub>s</sub>·N</p></div>'
        '<div class="ca-loi"><h3>b) Équilibre limite (ou strict)</h3><ul><li>Il y a adhérence, mais le glissement est sur '
        "le point de commencer.</li></ul>"
        '<p class="f-main">T<sub>a</sub> = µ<sub>s</sub>·N = f<sub>s</sub>·N</p></div>'
        '<div class="ca-loi"><h3>c) Frottement avec glissement</h3><ul><li><i>V</i><sub>A1/0</sub> caractérise la vitesse '
        "de glissement du point A appartenant au solide (1) par rapport au solide (0).</li><li>La force de frottement "
        "<i>T</i> est opposée à <i>V</i><sub>A1/0</sub> : elle s'oppose au mouvement.</li></ul>"
        '<p class="f-main">T = µ·N = f·N</p></div></div>'
        "<h3>Démarche générale</h3>" + _demarche() +
        '<div class="remarque"><p><b>Remarque :</b> dans la plupart des exercices, et dans un but de simplification, on '
        "confond adhérence et frottement : µ<sub>s</sub> = µ. On écrit alors une seule condition : il n'y a pas "
        "glissement tant que <i>T</i> ≤ µ·<i>N</i>.</p></div>"
        '<div class="exemple"><h3>Exemple : la voiture freinée dans une pente</h3><p>Une voiture de 3 000 daN est '
        "arrêtée dans une pente de 20 % ; seules les roues avant (A) sont freinées. Le principe fondamental donne, en A, "
        "N<sub>A</sub> ≈ 998 daN et T<sub>A</sub> ≈ 588 daN. Avec µ<sub>s</sub> = 0,6 : µ<sub>s</sub>·N<sub>A</sub> ≈ "
        "599 daN ≥ T<sub>A</sub> : il y a adhérence, la voiture tient — de justesse. Activités 2 et 3.</p></div>")
    s5 = h.course_section(5, "ca-roul", "La résistance au roulement",
        f'<figure class="c-fig">{svg_roulement()}<figcaption>Phénomène de résistance au roulement : définition de '
        "a.</figcaption></figure>"
        "<p>Au cours du roulement sous la charge <i>F</i>, un <b>bourrelet de matière</b> se forme devant l'élément "
        "roulant et s'oppose au mouvement : c'est la résistance au roulement. <i>R</i> schématise la résultante des "
        "pressions de contact exercées par le bourrelet sur l'élément roulant entre a et b. <i>F</i><sub>R</sub> "
        "représente la force qu'il faut exercer pour assurer ou maintenir le roulement de l'élément roulant.</p>"
        "<p>L'application du principe fondamental de la statique (trois forces : F et F<sub>R</sub> en O, R entre a et "
        "b ; moments en O) donne :</p>"
        '<div class="formule"><span class="f-main">F<sub>R</sub> = (a / r)·F = f<sub>R</sub>·F</span>'
        '<span class="f-units">a : coefficient de résistance au roulement (mm) ; f<sub>R</sub> = a / r : facteur de '
        "frottement de roulement ; r : rayon de l'élément roulant</span></div>"
        '<div class="remarque"><p><b>Remarque :</b> a dépend de nombreux paramètres : élasticité des matériaux, rayon de '
        "la roue, vitesse de déplacement, rugosité des surfaces… Un facteur f<sub>R</sub> de 0,012 donne une "
        "résistance de 12 kg pour 1 000 kg (une tonne).</p></div>"
        '<div class="c-split"><div><table class="t"><thead><tr><th>Matériaux en contact</th><th>a (mm)</th></tr></thead><tbody>'
        + "".join(f"<tr><td>{m}</td><td>{a}</td></tr>" for m, a in [("acier sur acier", "0,4"), ("fonte sur acier", "0,5"),
                                                                     ("élastomère sur bitume", "3 à 15"), ("pneu sur bitume", "20 à 30"),
                                                                     ("roue métallique sur béton", "10 à 15"), ("roue de wagon sur rail", "0,5 à 1")]) +
        '</tbody></table></div><div><table class="t"><thead><tr><th>Dispositifs</th><th>f<sub>R</sub></th></tr></thead><tbody>'
        "<tr><td>roulements à billes</td><td>0,001 5</td></tr><tr><td>roulements à rouleaux</td><td>0,002</td></tr>"
        "<tr><td>roulements à aiguilles</td><td>0,004</td></tr></tbody></table></div></div>"
        "<h3>Exemple 1 : la résistance au roulement d'une automobile</h3>"
        "<p>Déterminons la force de résistance au roulement exercée sur une automobile de masse 1 100 kg à vide, équipée "
        "de pneus usuels (« pneus noirs », f<sub>R1</sub> = 0,012) ou de « pneus verts » (pneus spéciaux, "
        "f<sub>R2</sub> = 0,008 5). Diamètre de roulement : 580 mm.</p>"
        '<div class="simu" id="ca-roul-simu"><h3>Simulateur : l\'automobile au ralenti</h3>'
        '<div class="simu-grid"><label><span>Masse : <output id="ca-rm-o">1 100 kg</output></span>'
        '<input type="range" id="ca-rm" min="600" max="2400" step="50" value="1100"></label>'
        '<label><span>Pneus</span><select id="ca-rp"><option value="0.012">pneus noirs (fR = 0,012)</option>'
        '<option value="0.0085">pneus verts (fR = 0,008 5)</option></select></label>'
        '<label><span>Diamètre de roulement : <output id="ca-rd-o">580 mm</output></span>'
        '<input type="range" id="ca-rd" min="400" max="800" step="10" value="580"></label>'
        '<label><span>Vitesse : <output id="ca-rv-o">90 km/h</output></span>'
        '<input type="range" id="ca-rv" min="10" max="130" step="5" value="90"></label></div>'
        f'<figure class="c-fig">{svg_auto()}<figcaption>Forces de résistance au roulement exercées sur l\'automobile '
        "(distances en mm).</figcaption></figure>"
        '<div class="simu-out"><div><span>Coefficient a = r·f<sub>R</sub></span><b id="ca-ra">–</b></div>'
        '<div><span>Résistance totale F<sub>rr</sub></span><b id="ca-rF">–</b></div>'
        '<div><span>Puissance consommée</span><b id="ca-rP">–</b></div><div><span>Poids P = m·g</span><b id="ca-rW">–</b></div></div>'
        '<p class="small">Hypothèses : g = 9,81 m/s² ; centre de gravité à 1 260 mm des roues arrière (A) et 1 000 mm '
        "des roues avant (B), comme sur la figure du manuel.</p></div>"
        "<p><b>a) Coefficients a de résistance au roulement</b> : a = r·f<sub>R</sub> = 290·f<sub>R</sub> ; pneus noirs : "
        "a<sub>1</sub> = 290 × 0,012 = 3,48 mm ; pneus verts : a<sub>2</sub> = 290 × 0,008 5 = 2,46 mm.</p>"
        "<p><b>b) Force de résistance au roulement</b> : F<sub>rr</sub> = F<sub>rrA</sub> + F<sub>rrB</sub> = "
        "f<sub>R</sub>·(R<sub>A</sub> + R<sub>B</sub>) = f<sub>R</sub>·P. Pneus noirs : F<sub>rr1</sub> = 0,012 × 1 079 "
        "= 12,95 daN ; pneus verts : F<sub>rr2</sub> = 0,008 5 × 1 079 = 9,17 daN.</p>"
        '<div class="remarque"><p><b>Remarque :</b> si la voiture roule à 90 km/h (V = 25 m/s), la puissance consommée '
        "est : pneus noirs, F<sub>rr1</sub>·V = (129,5 N) × (25 m/s) = 3 237,5 W, soit 3,24 kW ; pneus verts, "
        "F<sub>rr2</sub>·V = (91,7 N) × (25 m/s) = 2 292,5 W, soit 2,29 kW. Sur un parcours routier normal, sans "
        "accélération, avec des pneus noirs, la résistance au roulement représente environ 22 % de la consommation ; "
        "elle est de 16 % avec des pneus verts.</p></div>"
        "<h3>Exemple 2 : actions exercées sur une roue porteuse de véhicule</h3>"
        "<p><b>a) Actions exercées sur la bande de roulement du pneumatique.</b> Chaque bloc en caoutchouc appartenant à "
        "la bande de roulement d'un pneu en contact avec le sol supporte à la fois des contraintes de compression et de "
        "cisaillement. L'ensemble des contraintes de compression peut être modélisé par une pression de contact dont la "
        "résultante <i>R</i> est appliquée en A, à la distance IA = a en amont de I. L'ensemble des contraintes de "
        "cisaillement sur chaque bloc engendre une petite force de résistance au roulement, orientée vers l'arrière ou "
        "vers l'avant ; la résultante de toutes ces forces donne <i>F</i><sub>rr</sub> vers l'arrière, opposée au "
        "mouvement. (Ordres de grandeur de la pression de contact : environ 3 bar pour une voiture de tourisme, gonflée à "
        "2 bar ; environ 11 bar pour un camion, gonflé à 8 bar.)</p>"
        f'<figure class="c-fig" style="max-width:640px">{svg_roue_porteuse()}<figcaption>Actions exercées sur une roue '
        "porteuse de véhicule (pivot d'axe (O, z)).</figcaption></figure>"
        "<p><b>b) Bilan des actions.</b> La roue supporte deux torseurs d'actions, l'un en A (le sol), l'autre en O (le "
        "véhicule, par le pivot). En appelant <i>F</i><sub>m</sub> la force motrice exercée par le véhicule sur la roue "
        "et <i>P</i> la charge résultant des différents poids (roue et véhicule) :</p>"
        f'<p class="eq">{{sol → roue}} = {tors([("−F<sub>rr</sub>", "0"), ("R", "0"), ("0", "0")], "A")} ; '
        f'{{véhicule → roue}} = {tors([("F<sub>m</sub>", "L"), ("−P", "M"), ("Z", "0")], "O")}</p>'
        "<p>Principe fondamental de la statique, les deux torseurs transportés au point I (sous O, au contact) : le "
        "moment en I de <i>R</i>, appliquée en A à la distance a, vaut a·R·<i>z</i> ; celui de <i>F</i><sub>m</sub>, "
        "appliquée en O à la hauteur r, vaut −r·F<sub>m</sub>·<i>z</i>.</p>"
        '<p class="eq">'
        "Résultantes : F<sub>m</sub> − F<sub>rr</sub> = 0 ; R − P = 0 ; Z = 0. Moments en I : L = 0 ; M = 0 ; "
        "a·R − r·F<sub>m</sub> = 0.</p>"
        '<div class="formule"><span class="f-main">R = P ; F<sub>rr</sub> = F<sub>m</sub> = a·P / r = f<sub>R</sub>·P</span>'
        '<span class="f-units">la force motrice qui entretient le roulement équilibre exactement la résistance au '
        "roulement</span></div>"
        '<div class="remarque"><p><b>Note :</b> le manuel écrit le moment de R sous la forme « IA ∧ (−F<sub>rr</sub>·x + '
        "R·y) = a·R·z » et conclut « F<sub>rr</sub> = −a·P / r = −f<sub>R</sub>·P » ; le signe moins exprime "
        "seulement que <i>F</i><sub>rr</sub> est dirigée vers l'arrière (−x). En norme, F<sub>rr</sub> = "
        "f<sub>R</sub>·P.</p></div>")
    cartes = [("Adhérence", "Pas de glissement : T<sub>a</sub> ≤ µ<sub>s</sub>·N. La force d'adhérence s'oppose au "
               "mouvement qui se produirait sans elle."),
              ("Équilibre strict", "La limite : T<sub>a</sub> = µ<sub>s</sub>·N. Un rien de plus et le solide glisse."),
              ("Frottement", "Glissement : T = µ·N, opposée à la vitesse de glissement. µ est un peu plus petit que "
               "µ<sub>s</sub> : il faut moins d'effort pour entretenir le glissement que pour le déclencher."),
              ("Coefficients", "µ<sub>s</sub> et µ dépendent des matériaux et de l'état des surfaces, pas de la force ni "
               "de l'aire de contact. Acier sur acier ≈ 0,15 ; pneu sur route sèche ≈ 0,6."),
              ("Roulement", "Un bourrelet se forme devant la roue : F<sub>R</sub> = (a / r)·F = f<sub>R</sub>·F. Pneus "
               "usuels : f<sub>R</sub> ≈ 0,012, soit 12 kg pour une tonne.")]
    s6 = h.course_section(6, "ca-ess", "L'essentiel à retenir",
        '<div class="cartes">' + "".join(f'<button type="button" class="carte" aria-expanded="false"><b>{t}</b>'
                                          f'<span class="dos">{d}</span></button>' for t, d in cartes) + "</div>")
    quiz = [
        ("Un colis immobile est poussé horizontalement, sans bouger. La force d'adhérence vaut :",
         ["µ<sub>s</sub>·N", "la poussée F, en sens opposé", "zéro"], 1,
         "Tant qu'il n'y a pas glissement, l'équilibre impose T<sub>a</sub> = F ; µ<sub>s</sub>·N n'est que la valeur "
         "maximale qu'elle peut atteindre."),
        ("On double l'aire de contact d'un patin (même charge, mêmes matériaux). Le facteur de frottement :",
         ["double", "reste le même", "est divisé par deux"], 1,
         "µ ne dépend pas de l'étendue des surfaces en contact, seulement des matériaux et de l'état des surfaces."),
        ("Un objet glisse. La force de frottement est :", ["T = µ·N, opposée à la vitesse de glissement",
                                                            "T ≤ µ·N, dans le sens du mouvement", "nulle à vitesse constante"], 0,
         "En glissement, T atteint µ·N et s'oppose au mouvement relatif ; à vitesse constante, c'est la poussée qui "
         "l'équilibre."),
        ("Pour remettre en mouvement un objet arrêté, il faut fournir :", ["F ≥ µ·N", "F ≥ µ<sub>s</sub>·N", "F ≥ N"], 1,
         "Il faut vaincre l'adhérence : F ≥ µ<sub>s</sub>·N, un peu plus que l'effort qui entretient le glissement."),
        ("µ<sub>s</sub> = 0,6 et N = 1 000 daN. Quelle force tangentielle le contact peut-il transmettre au plus sans "
         "glisser ?", ["60 daN", "600 daN", "1 600 daN"], 1, "T<sub>a max</sub> = µ<sub>s</sub>·N = 0,6 × 1 000 = 600 daN."),
        ("Le bourrelet de matière responsable de la résistance au roulement se forme :",
         ["derrière la roue", "devant la roue", "sous l'axe de la roue"], 1,
         "Il se forme devant l'élément roulant et s'oppose au mouvement : la résultante R est décalée de a vers "
         "l'avant."),
        ("Une voiture de 1 000 daN a des pneus de facteur f<sub>R</sub> = 0,012. Sa résistance au roulement vaut :",
         ["1,2 daN", "12 daN", "120 daN"], 1, "F<sub>rr</sub> = f<sub>R</sub>·P = 0,012 × 1 000 = 12 daN."),
        ("Le coefficient a de résistance au roulement s'exprime :", ["sans unité", "en millimètres", "en newtons"], 1,
         "a est une longueur (le décalage de R) ; f<sub>R</sub> = a / r, lui, n'a pas d'unité."),
    ]
    quiz_s = h.quiz_section(7, "ca-quiz", quiz, "ca-q")
    foot = ('<div class="cours-foot no-print"><a class="btn" href="?ex=voiture-pente">S\'entraîner : Activité 2</a>'
            '<a class="btn ghost" href="?ex=voiture-route-mouillee">Activité 4</a>'
            '<a class="btn ghost" href="?ex=resistance-roulement">Activité 5</a>'
            f'<a class="btn ghost" href="?">{h.HOUSE} Accueil</a></div>')
    head = h.course_head("Cours", "Frottement et roulement",
                         "Adhérence et frottement, coefficients, lois de Coulomb et résistance au roulement. "
                         "Simulateurs, synthèse et quiz.")
    return (f'<div class="cours">{head}<nav class="c-top" aria-label="Navigation"><a href="?">{h.HOUSE} Accueil</a></nav>'
            f"{fiche}{h.course_nav(sections)}{s1}{s2}{s3}{s4}{s5}{s6}{quiz_s}{foot}</div>")


def _table_coef():
    rows = [("acier sur acier", "0,18", "0,12", "0,15", "0,09"), ("acier sur fonte", "0,19", "0,1", "0,16", "0,08 à 0,04"),
            ("acier sur bronze", "0,11", "0,1", "0,1", "0,09"), ("téflon sur acier", "0,04", "", "0,04", ""),
            ("fonte sur bronze", "", "0,1", "0,2", "0,08 à 0,04"), ("nylon sur acier", "", "", "0,35", "0,12"),
            ("bois sur bois", "0,65", "0,2", "0,4 à 0,2", "0,16 à 0,04"), ("métaux sur bois", "0,6 à 0,5", "0,1", "0,5 à 0,2", "0,08 à 0,02"),
            ("métal sur glace", "", "", "0,02", ""), ("pneu de voiture sur route", "0,8", "", "0,6", "0,3 à 0,1 sur sol mouillé")]
    return ('<div class="ca-tab"><table class="t"><thead><tr><th rowspan="2">Nature des matériaux en contact</th>'
            '<th colspan="2">Adhérence µ<sub>s</sub> = f<sub>s</sub></th><th colspan="2">Frottement (glissement) µ = f</th></tr>'
            "<tr><th>à sec</th><th>lubrifié</th><th>à sec</th><th>lubrifié</th></tr></thead><tbody>" +
            "".join(f"<tr><td>{m}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for m, a, b, c, d in rows) +
            "</tbody></table></div>")


def _demarche():
    """Figure 6 du manuel (démarche générale), écrite avec les égalités et inégalités des lois de Coulomb."""
    return ('<div class="ca-dem" role="group" aria-label="Démarche générale des lois du frottement">'
            '<p class="ca-dq">Les surfaces en contact glissent-elles l\'une sur l\'autre ?</p>'
            '<div class="ca-dcols"><div class="ca-dcol oui"><p class="ca-dr">Oui : cas c), le frottement</p>'
            "<p>f = µ</p><p>La force de frottement s'oppose au mouvement des surfaces en contact : "
            "T = f·N = µ·N.</p></div>"
            '<div class="ca-dcol non"><p class="ca-dr">Non : l\'adhérence (pas de mouvement au contact)</p>'
            "<p>f<sub>s</sub> = µ<sub>s</sub></p><p class=\"ca-dq2\">Est-on à la limite entre "
            "glissement et adhérence (équilibre strict) ?</p><div class=\"ca-dcols\"><div><p class=\"ca-dr\">Oui : "
            "cas b)</p><p>T<sub>a</sub> = f<sub>s</sub>·N = µ<sub>s</sub>·N : le glissement est sur le point de "
            "commencer.</p></div><div><p class=\"ca-dr\">Non : cas a)</p><p>T<sub>a</sub> &lt; "
            "f<sub>s</sub>·N : il reste une marge avant le glissement.</p></div>"
            "</div></div></div></div>")


JS = r"""
  function initCours(root) {
    var NS = "http://www.w3.org/2000/svg";
    function $(s) { return root.querySelector(s); }
    var MAT = __MAT__;
    // ---------- le colis ----------
    var sv = $("#ca-colis-svg");
    if (sv) {
      var F = $("#ca-F"), mat = $("#ca-mat"), mm = $("#ca-m"), glisse = false, x = 0, raf = null, last = 0;
      function dims() {
        var m = MAT[+mat.value], P = +mm.value * 9.81;
        return { mus: m[1], mu: m[2], N: P, lim: m[1] * P, dyn: m[2] * P, P: P, nom: m[0] };
      }
      function setMax() { var d = dims(); F.max = Math.ceil(d.lim * 1.45 / 5) * 5; F.step = Math.max(1, Math.round(F.max / 200)); }
      function fl(x1, y1, x2, y2, c, w) {
        var L = Math.hypot(x2 - x1, y2 - y1); if (L < 1) return "";
        var ux = (x2 - x1) / L, uy = (y2 - y1) / L, hx = x2 - ux * 10, hy = y2 - uy * 10;
        return '<path d="M' + x1 + " " + y1 + "L" + hx + " " + hy + '" stroke="' + c + '" stroke-width="' + (w || 3) + '"/>' +
          '<path d="M' + x2 + " " + y2 + "L" + (hx - uy * 5) + " " + (hy + ux * 5) + "L" + (hx + uy * 5) + " " + (hy - ux * 5) + 'Z" fill="' + c + '"/>';
      }
      function draw() {
        var d = dims(), f = +F.value, T, etat, cls;
        if (!glisse && f > d.lim + 1e-9) glisse = true;
        if (glisse && f < d.dyn - 1e-9) glisse = false;
        if (!glisse) { T = f; etat = f === 0 ? "Repos : N et P sont égales et opposées, aucune force tangentielle." :
          (Math.abs(f - d.lim) < F.step ? "Équilibre strict : T atteint µs·N, le colis est sur le point de glisser." :
           "Adhérence : le colis ne bouge pas, la force d'adhérence T équilibre exactement la poussée F (T < µs·N).");
          cls = f && Math.abs(f - d.lim) < F.step ? "lim" : "ok"; }
        else { T = d.dyn; etat = f > d.dyn + F.step ? "Glissement accéléré : T = µ·N est dépassée par F, le colis accélère (a = " +
          fr((f - d.dyn) / (+mm.value), 2) + " m/s²)." : "Glissement à vitesse constante : F = µ·N équilibre le frottement.";
          cls = "ko"; }
        $("#ca-F-o").textContent = fr(f, 0) + " N"; $("#ca-m-o").textContent = mm.value + " kg";
        $("#ca-N").textContent = fr(d.N, 1) + " N"; $("#ca-T").textContent = fr(T, 1) + " N";
        $("#ca-TN").textContent = fr(T / d.N, 3); $("#ca-lim").textContent = fr(d.lim, 1) + " N";
        var e = $("#ca-etat"); e.textContent = etat; e.className = "simu-verdict " + cls;
        // dessin : le plan, le colis, les forces ; à droite, T en fonction de F
        var bx = 60 + (x % 180), s = '<rect width="640" height="230" fill="#fff"/><path d="M10 170H330" stroke="#8A7350" stroke-width="2"/>' +
          '<rect x="10" y="170" width="320" height="10" fill="#E9DCC6"/>' +
          '<rect x="' + bx + '" y="100" width="90" height="70" fill="#F2E3C2" stroke="#8A6D3B" stroke-width="2"/>' +
          '<path d="M' + (bx + 8) + ' 108L' + (bx + 82) + ' 162M' + (bx + 82) + ' 108L' + (bx + 8) + ' 162" stroke="#C9A96E"/>';
        var gx = bx + 45, gy = 135, k = 60 / Math.max(d.P, 1);
        s += fl(gx, gy, gx, gy + d.P * k, "#B42318") + '<text x="' + (gx + 6) + '" y="' + (gy + 40) + '" font-size="14" font-style="italic" font-weight="700" fill="#B42318">P</text>';
        s += fl(gx, 170 + 0, gx, 170 - d.N * k, "#1F5FA8") + '<text x="' + (gx + 6) + '" y="' + (170 - d.N * k + 14) + '" font-size="14" font-style="italic" font-weight="700" fill="#1F5FA8">N</text>';
        if (f > 0) s += fl(gx - 45 - f * k, gy, gx - 45, gy, "#1B7A43") + '<text x="' + (gx - 60 - f * k) + '" y="' + (gy - 8) + '" font-size="14" font-style="italic" font-weight="700" fill="#1B7A43">F</text>';
        if (T > 0) s += fl(gx, 172, gx - T * k, 172, "#B26A00") + '<text x="' + (gx - T * k - 4) + '" y="196" font-size="14" font-style="italic" font-weight="700" fill="#B26A00">T</text>';
        s += '<circle cx="' + gx + '" cy="' + gy + '" r="3" fill="#1C2530"/><text x="' + (gx + 5) + '" y="' + (gy - 5) + '" font-size="12" font-style="italic">G</text>';
        // graphique T(F)
        var X0 = 380, Y0 = 200, W = 240, H = 160, fm = +F.max, sx = W / fm, sy = H / (d.lim * 1.25);
        s += '<path d="M' + X0 + " " + Y0 + "H" + (X0 + W) + "M" + X0 + " " + Y0 + "V" + (Y0 - H) + '" stroke="#1C2530"/>' +
          '<text x="' + (X0 + W - 6) + '" y="' + (Y0 + 16) + '" font-size="12" font-style="italic" text-anchor="end">F</text>' +
          '<text x="' + (X0 - 14) + '" y="' + (Y0 - H + 8) + '" font-size="12" font-style="italic">T</text>' +
          '<path d="M' + X0 + " " + Y0 + "L" + (X0 + d.lim * sx) + " " + (Y0 - d.lim * sy) + '" stroke="#1F5FA8" stroke-width="2"/>' +
          '<path d="M' + (X0 + d.lim * sx) + " " + (Y0 - d.lim * sy) + "V" + (Y0 - d.dyn * sy) + "H" + (X0 + W) + '" stroke="#B42318" stroke-width="2" fill="none"/>' +
          '<path d="M' + X0 + " " + (Y0 - d.lim * sy) + "H" + (X0 + d.lim * sx) + "M" + X0 + " " + (Y0 - d.dyn * sy) + "H" + (X0 + d.lim * sx) + '" stroke="#A5ADAA" stroke-dasharray="4 3"/>' +
          '<text x="' + (X0 + 4) + '" y="' + (Y0 - d.lim * sy - 5) + '" font-size="11">µs·N</text><text x="' + (X0 + 4) + '" y="' + (Y0 - d.dyn * sy + 13) + '" font-size="11">µ·N</text>' +
          '<text x="' + (X0 + 8) + '" y="' + (Y0 - 6) + '" font-size="11" fill="#1F5FA8">adhérence</text>' +
          '<text x="' + (X0 + W - 4) + '" y="' + (Y0 - d.dyn * sy - 6) + '" font-size="11" fill="#B42318" text-anchor="end">glissement</text>' +
          '<circle cx="' + (X0 + f * sx) + '" cy="' + (Y0 - T * sy) + '" r="5" fill="#F2B705" stroke="#1C2530"/>';
        sv.innerHTML = s;
      }
      function anim(t) {
        if (glisse && +F.value > 0) { x += Math.min(40, (t - last) || 16) * 0.08; draw(); last = t; raf = requestAnimationFrame(anim); }
        else { raf = null; last = 0; }
      }
      function maj() { draw(); if (glisse && !raf && !(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) raf = requestAnimationFrame(anim); }
      F.addEventListener("input", maj);
      mat.addEventListener("change", function () { glisse = false; setMax(); maj(); });
      mm.addEventListener("input", function () { glisse = false; setMax(); maj(); });
      $("#ca-stop").addEventListener("click", function () { glisse = false; F.value = 0; maj(); });
      setMax(); draw();
    }
    // ---------- l'automobile au ralenti ----------
    var rm = $("#ca-rm");
    if (rm) {
      var rp = $("#ca-rp"), rd = $("#ca-rd"), rv = $("#ca-rv");
      function majR() {
        var m = +rm.value, f = +rp.value, D = +rd.value, v = +rv.value / 3.6;
        var P = m * 9.81 / 10, RA = P * 1000 / 2260, RB = P * 1260 / 2260, FA = f * RA, FB = f * RB, Fr = FA + FB;
        $("#ca-rm-o").textContent = fr(m, 0) + " kg"; $("#ca-rd-o").textContent = D + " mm"; $("#ca-rv-o").textContent = rv.value + " km/h";
        $("#ca-ra").textContent = fr(D / 2 * f, 2) + " mm"; $("#ca-rF").textContent = fr(Fr, 2) + " daN";
        $("#ca-rP").textContent = fr(Fr * 10 * v / 1000, 2) + " kW"; $("#ca-rW").textContent = fr(P, 0) + " daN";
        var t = { "ca-vP": "(" + fr(P, 0) + " daN)", "ca-vRA": "(" + fr(RA, 0) + " daN)", "ca-vRB": "(" + fr(RB, 0) + " daN)",
                  "ca-vFA": "(" + fr(FA, 2) + " daN)", "ca-vFB": "(" + fr(FB, 2) + " daN)", "ca-vFm": "(" + fr(Fr, 2) + " daN)" };
        Object.keys(t).forEach(function (k) { var el = root.querySelector("#" + k); if (el) el.textContent = t[k]; });
      }
      [rm, rp, rd, rv].forEach(function (el) { el.addEventListener("input", majR); el.addEventListener("change", majR); });
      majR();
    }
  }
""".replace("__MAT__", repr([[n, a, b] for n, a, b in MATERIAUX]).replace("'", '"'))

CSS = """
/* ---------- cours ---------- */
.ca-ex{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin:10px 0}
.ca-ex figure{margin:0; background:#fff; border:1px solid var(--trait-fin); padding:8px}
.ca-ex svg{display:block; width:100%; height:auto; font-family:var(--f-texte)}
.ca-ex figcaption{font-size:.88rem; margin-top:6px}
@media (max-width:760px){ .ca-ex{grid-template-columns:1fr} }
.ca-tab{overflow-x:auto}
.ca-tab table{min-width:560px}
.ca-lois{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; margin:10px 0}
.ca-loi{background:#fff; border:2px solid var(--encre); padding:6px 14px 10px}
.ca-loi h3{margin:6px 0 4px!important}
.ca-loi ul{padding-left:1.1rem; margin:0 0 6px; font-size:.93rem}
.ca-loi .f-main{font:700 1.2rem var(--f-titre); color:var(--rouge); margin:6px 0 0}
@media (max-width:860px){ .ca-lois{grid-template-columns:1fr} }
.ca-dem{border:1.5px solid var(--encre); background:#fff; padding:10px 12px; margin:10px 0; font-size:.93rem}
.ca-dq,.ca-dq2{margin:0 0 8px; text-align:center; font-weight:700; border:1.5px solid var(--encre); border-radius:18px; padding:6px 12px}
.ca-dq2{font-weight:600; font-size:.9rem}
.ca-dcols{display:grid; grid-template-columns:1fr 1fr; gap:10px}
.ca-dcol{padding:6px 10px; border-top:4px solid var(--trait)}
.ca-dcol.oui{background:var(--vert-pale); border-top-color:var(--vert)} .ca-dcol.non{background:var(--bleu-pale); border-top-color:var(--bleu)}
.ca-dcol p{margin:.25rem 0}
.ca-dr{font-weight:700}
.ca-dcol .ca-dcols>div{background:#fff; padding:4px 8px; border:1px solid var(--trait-fin)}
@media (max-width:640px){ .ca-dcols{grid-template-columns:1fr} }
.simu label.chk{justify-content:flex-end}
"""
