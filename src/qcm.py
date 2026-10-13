"""QCM des activités, sur le modèle du QCM 2.1 du dépôt « Chaîne fonctionnelle » (src/qcm.py de ce dépôt).

Chaque question est une question du gabarit à une seule case (mécanisme « fast-q ») : la case, masquée, reçoit le
repère de la ou des propositions choisies ; le moteur Grading la corrige (« code » pour une réponse unique,
« intset » pour plusieurs réponses). Modes entraînement et examen, note, récapitulatif et impression sont ceux du
gabarit. Le rendu, le style et le script sont repris tels quels ; seule la figure d'une question devient un dessin
SVG intégré (« fig ») au lieu d'une image.
"""
import html


def question(stem, opts, bonnes, why, fig="", multi=None):
    """Bloc « grp » marqué « qcm » pour une partie d'activité. opts : [(repère affiché, texte)], repères du livre
    (a, b, c…) ; bonnes : repères justes. Dans la case masquée, chaque proposition est codée par son rang (1, 2, 3…),
    ce que corrige le moteur (« intset ») quelle que soit la lettre affichée."""
    multi = len(bonnes) > 1 if multi is None else multi
    rang = {k: str(i + 1) for i, (k, _t) in enumerate(opts)}
    if multi:
        g = {"type": "intset", "value": sorted(int(rang[k]) for k in bonnes)}
        hint = "Une ou plusieurs réponses : sélectionne toutes les bonnes, et aucune autre."
    else:
        g = {"type": "code", "equals": [rang[k] for k in bonnes]}
        hint = "Une seule réponse."
    sep = " ; " if multi else " ou "
    attendu = sep.join(f"{k}) {t}" for k, t in opts if k in bonnes)
    return {"kind": "grp", "qcm": True, "stem": stem, "hint": hint, "fields": [("Réponse", g, attendu)],
            "why": why, "opts": [(rang[k], k, t) for k, t in opts], "multi": multi, "fig": fig}


def render_qcm(b):
    """Une question : énoncé, figure éventuelle, propositions ; la case du gabarit est masquée."""
    gid, label, fid = b["id"], b["label"], b["fids"][0]
    fig = f'<figure class="fig-ex qcm-fig">{b["fig"]}</figure>' if b.get("fig") else ""
    role = "group" if b["multi"] else "radiogroup"
    opts = "".join(f'<button type="button" class="qcm-o" data-k="{k}" role="{"checkbox" if b["multi"] else "radio"}" '
                   f'aria-checked="false"><span class="qcm-k">{html.escape(aff)}</span><span class="qcm-t">{t}</span></button>'
                   for k, aff, t in b["opts"])
    return f"""
        <div class="fast-q grp qcm" id="{gid}" data-multi="{1 if b['multi'] else 0}">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{b['stem']}</strong></p>
          <p class="q-hint">{html.escape(b['hint'])}</p>{fig}
          <div class="qcm-opts" role="{role}" aria-label="Propositions de la question {label}">{opts}</div>
          <div class="sol qcm-sol"><input type="hidden" id="in-{fid}" data-q="{fid}"><span class="mark" aria-live="polite"></span></div>
          <div class="fast-foot"><button type="button" class="btn btn-fast" disabled>Valider</button>
            <span class="q-status" aria-live="polite"></span></div>
          <p class="q-msg" role="alert"></p>
          <div class="q-expl" hidden>
            <p class="qcm-rep"><b>Réponse attendue :</b> {html.escape(b['fields'][0][2])}</p>
            <div class="q-why"><p class="why-t">Explication</p>{b['why']}</div>
          </div>
        </div>"""


CONSIGNES = """<p class="only-training"><strong>Mode entraînement.</strong> Choisis ta réponse puis clique sur « Valider » : une réponse validée est définitive, sa correction et son explication s'affichent aussitôt.</p>
    <p class="only-exam"><strong>Mode examen.</strong> Réponds à tout le questionnaire sans correction ni note : tes choix restent modifiables jusqu'au bout. Le bouton « J'ai fini, je fais corriger ma copie », en fin de sujet, dévoile d'un coup les corrections, les notes et la note globale.</p>
    <p><strong>Une ou plusieurs réponses.</strong> L'énoncé précise s'il peut y avoir plusieurs bonnes réponses : il faut alors toutes les sélectionner, et aucune autre.</p>
    <p>Le document technique (DT) s'ouvre avec les onglets sur le bord droit, ou avec les boutons des en-têtes de question.</p>"""

QCM_CSS = """
/* ---------- QCM (questions à propositions) ---------- */
.qcm .fig{margin:8px 0}
.qcm-opts{display:flex; flex-direction:column; gap:6px; margin:8px 0 4px}
.qcm-o{display:flex; align-items:flex-start; gap:10px; width:100%; text-align:left; background:#fff; border:1.5px solid var(--trait); border-radius:3px; padding:8px 12px; font:inherit; font-size:.97rem; color:var(--encre); cursor:pointer}
.qcm-o:hover:not(:disabled){border-color:var(--encre); background:var(--jaune-pale)}
.qcm-o:focus-visible{outline:3px solid var(--jaune); outline-offset:1px}
.qcm-k{flex:0 0 auto; min-width:1.9em; height:1.9em; display:inline-flex; align-items:center; justify-content:center; border:1.5px solid var(--bleu); color:var(--bleu); font:700 .85rem var(--f-titre); border-radius:3px}
.qcm[data-multi="1"] .qcm-k{border-radius:3px} .qcm[data-multi="0"] .qcm-k{border-radius:50%}
.qcm-o[aria-checked="true"]{border-color:var(--bleu); background:var(--bleu-pale); box-shadow:inset 0 0 0 1px var(--bleu)}
.qcm-o[aria-checked="true"] .qcm-k{background:var(--bleu); color:#fff}
.qcm-o:disabled{cursor:default}
.qcm-o.ok{border-color:var(--vert); background:var(--vert-pale)} .qcm-o.ok .qcm-k{border-color:var(--vert); background:var(--vert); color:#fff}
.qcm-o.ko{border-color:var(--rouge); background:var(--rouge-pale)} .qcm-o.ko .qcm-k{border-color:var(--rouge); background:var(--rouge); color:#fff}
.qcm-o .qcm-tag{margin-left:auto; flex:0 0 auto; font:700 .75rem var(--f-titre); padding:1px 7px; color:#fff}
.qcm-o.ok .qcm-tag{background:var(--vert)} .qcm-o.ko .qcm-tag{background:var(--rouge)}
.qcm-sol{min-height:0}
.qcm-sol .mark{flex:0 0 auto}
.qcm-rep{margin:0 0 6px}
@media print{ .qcm-o{padding:2px 8px; font-size:9pt; break-inside:avoid} .qcm{break-inside:avoid} }
"""

QCM_JS = r"""<script>/* QCM : un clic choisit une proposition (ou plusieurs) ; le repère va dans la case masquée du gabarit */
(function () {
  "use strict";
  var parts = document.getElementById("parts");
  if (!parts || !parts.querySelector(".qcm")) return;
  function inp(q) { return q.querySelector(".sol input"); }
  function choisis(q) { return Array.prototype.filter.call(q.querySelectorAll(".qcm-o"), function (o) { return o.getAttribute("aria-checked") === "true"; }); }
  function maj(q) {
    var i = inp(q), v = choisis(q).map(function (o) { return o.getAttribute("data-k"); }).join(",");
    i.value = v;
    var b = q.querySelector(".btn-fast");
    if (!i.disabled) b.disabled = !v;
    i.dispatchEvent(new Event("input", { bubbles: true }));
  }
  parts.addEventListener("click", function (e) {
    var o = e.target.closest(".qcm-o");
    if (!o || o.disabled) return;
    var q = o.closest(".qcm"), multi = q.getAttribute("data-multi") === "1";
    if (inp(q).disabled) return;
    if (multi) o.setAttribute("aria-checked", o.getAttribute("aria-checked") === "true" ? "false" : "true");
    else Array.prototype.forEach.call(q.querySelectorAll(".qcm-o"), function (x) { x.setAttribute("aria-checked", x === o ? "true" : "false"); });
    maj(q);
  });
  // flèches du clavier dans une question à réponse unique
  parts.addEventListener("keydown", function (e) {
    var o = e.target.closest && e.target.closest(".qcm-o");
    if (!o || (e.key !== "ArrowDown" && e.key !== "ArrowUp")) return;
    var all = Array.prototype.slice.call(o.parentNode.querySelectorAll(".qcm-o")), k = all.indexOf(o) + (e.key === "ArrowDown" ? 1 : -1);
    if (all[k]) { e.preventDefault(); all[k].focus(); }
  });
  // une fois la question corrigée par le moteur (champ verrouillé) : propositions justes et fausses marquées
  function corriger(q) {
    var id = inp(q).getAttribute("data-q"), g = (window.__QCFG__[id] || {}).grader || {}, bons = {};
    (g.equals || []).forEach(function (k) { bons[k] = 1; });
    (g.value || []).forEach(function (k) { bons[String(k)] = 1; });
    Array.prototype.forEach.call(q.querySelectorAll(".qcm-o"), function (o) {
      var k = o.getAttribute("data-k").toLowerCase(), sel = o.getAttribute("aria-checked") === "true", tag;
      o.disabled = true;
      if (bons[k] || (sel && !bons[k])) {
        o.classList.add(bons[k] ? "ok" : "ko");
        tag = document.createElement("span"); tag.className = "qcm-tag";
        tag.textContent = bons[k] ? (sel ? "✔ ta réponse" : "✔ bonne réponse") : "✘ ta réponse";
        o.appendChild(tag);
      }
    });
    var juste = q.querySelector(".sol").classList.contains("is-ok");
    q.querySelector(".q-status").textContent = juste ? "Bonne réponse" : (inp(q).value ? "Réponse fausse" : "Pas de réponse");
  }
  new MutationObserver(function (ms) {
    ms.forEach(function (m) {
      var i = m.target;
      if (i.tagName !== "INPUT" || !i.disabled) return;
      var q = i.closest(".qcm");
      if (q && !q.classList.contains("corrigee")) { q.classList.add("corrigee"); corriger(q); }
    });
  }).observe(parts, { subtree: true, attributes: true, attributeFilter: ["disabled"] });
})();
</script>"""
