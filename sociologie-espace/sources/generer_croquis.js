// Fiche A4 « croquis a la main » : avenue Habib Bourguiba (Tunis), coupe avant / apres.
// Les traits sont tremblés par rough.js (graine fixe -> resultat identique a chaque fois).
// Usage : node generer_croquis.js  ->  ../Avenue_Habib_Bourguiba_croquis.pdf (+ .png)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const LEG = [
  ["1", "Éclairage", "Lampadaires hauts tournés vers la chaussée : promenade sombre le soir.", "Lampes basses (≈ 4 m) le long des allées, lumière chaude."],
  ["2", "Végétation", "Arbres seulement au centre ; trottoirs nus.", "Arbres d'alignement sur les trottoirs, jardinières, bandes plantées."],
  ["3", "Minéralité", "Tout est dur (dalles, béton) : chaleur, eau qui ruisselle.", "Sols mixtes : dalles claires + bandes perméables plantées."],
  ["4", "Ombrage et lumière", "Terrasses et trottoirs en plein soleil, éblouissement.", "Ombre des arbres + voiles d'ombrage sur les terrasses."],
  ["5", "Places pour s'asseoir", "Un seul banc pour toute la promenade.", "Bancs sous les arbres, régulièrement espacés."],
  ["6", "Poubelles", "Aucune près des assises et des terrasses.", "Poubelles de tri près des bancs et sur les trottoirs."],
  ["7", "Fraîcheur (bonus)", "Aucun point d'eau.", "Fontaine / brumisateur au centre de la promenade."],
];

const script = `
const W = 820, H = 335, G = 285;
const INK = "#23262b", ROUGE = "#c8402f", VERT = "#2f8f5b";
let SEED = 7;
const base = { stroke: INK, strokeWidth: 1.5, roughness: 1.7, bowing: 1.6 };
const o = (x = {}) => ({ ...base, seed: SEED++, ...x });
const hach = (couleur, gap = 4, angle = -45, w = 1) => ({ fill: couleur, fillStyle: "hachure", hachureGap: gap, hachureAngle: angle, fillWeight: w });
// petit generateur pseudo-aleatoire fixe
let rs = 12345; const rnd = () => (rs = (rs * 1664525 + 1013904223) % 4294967296) / 4294967296;

function dessiner(svg, apres) {
  const rc = rough.svg(svg);
  const add = (n) => { svg.appendChild(n); return n; };
  const texte = (t, x, y, o2 = {}) => {
    const e = document.createElementNS("http://www.w3.org/2000/svg", "text");
    e.setAttribute("x", x); e.setAttribute("y", y);
    e.setAttribute("font-family", "Caveat"); e.setAttribute("font-size", o2.taille || 19);
    e.setAttribute("font-weight", o2.gras ? 700 : 400); e.setAttribute("fill", o2.couleur || INK);
    if (o2.ancre) e.setAttribute("text-anchor", o2.ancre);
    if (o2.rot) e.setAttribute("transform", "rotate(" + o2.rot + " " + x + " " + y + ")");
    e.textContent = t; add(e);
  };
  const fleche = (x1, y1, x2, y2, c) => {
    add(rc.line(x1, y1, x2, y2, o({ stroke: c, strokeWidth: 1.6, roughness: 1 })));
    const a = Math.atan2(y2 - y1, x2 - x1);
    [0.45, -0.45].forEach((d) => add(rc.line(x2, y2, x2 - 9 * Math.cos(a + d), y2 - 9 * Math.sin(a + d), o({ stroke: c, strokeWidth: 1.6, roughness: 0.8 }))));
  };

  // ---------- batiments ----------
  const batiment = (x, w) => {
    add(rc.rectangle(x, 40, w, G - 40, o({ ...hach("#d9c6a0", 7, -35, 0.7), roughness: 1.3 })));
    add(rc.line(x - 4, 40, x + w + 4, 40, o({ strokeWidth: 2.4 })));
    add(rc.line(x - 2, 52, x + w + 2, 52, o({ roughness: 1 })));
    for (let r = 0; r < 5; r++) for (let c = 0; c < 3; c++) {
      const wx = x + 14 + c * ((w - 28) / 3), wy = 64 + r * 38;
      add(rc.rectangle(wx, wy, 20, 26, o({ ...hach("#5d7080", 3, 60, 0.9), strokeWidth: 1.2, roughness: 1 })));
      add(rc.line(wx - 3, wy + 28, wx + 23, wy + 28, o({ strokeWidth: 1.2, roughness: 0.8 })));
    }
    add(rc.line(x - 1, G - 40, x + w + 1, G - 40, o({ strokeWidth: 1.8 })));
  };
  batiment(-6, 126); batiment(700, 126);

  // ---------- sol ----------
  add(rc.line(-4, G, W + 4, G, o({ strokeWidth: 2.6, roughness: 1.2 })));
  add(rc.rectangle(-4, G + 3, W + 8, 9, o({ ...hach("#8a7f70", 3, 45, 0.9), stroke: "none", roughness: 1 })));
  [[120, 8], [200, 8], [310, 8], [510, 8], [620, 8], [700, 8]].forEach(([x]) => add(rc.line(x, G, x, G - 7, o({ strokeWidth: 2, roughness: 0.8 }))));
  add(rc.rectangle(200, G + 3, 110, 9, o({ ...hach("#3b4047", 2.5, 45, 1), stroke: "none", roughness: 1 })));
  add(rc.rectangle(510, G + 3, 110, 9, o({ ...hach("#3b4047", 2.5, 45, 1), stroke: "none", roughness: 1 })));
  if (apres) [[326, 30], [464, 30], [126, 14], [682, 14]].forEach(([x, w]) => add(rc.rectangle(x, G + 1, w, 8, o({ ...hach("#4f9a4a", 2.5, -45, 1.4), stroke: "#2f6a31", strokeWidth: 1.2, roughness: 1.2 }))));
  [["trottoir", 160], ["chaussée", 255], ["promenade centrale", 410], ["chaussée", 565], ["trottoir", 660]].forEach(([t, x]) => texte(t, x, G + 32, { taille: 17, couleur: "#555", ancre: "middle" }));

  // ---------- elements ----------
  const ombre = (x, rx) => add(rc.ellipse(x, G + 4, rx * 2, 9, o({ ...hach("#3a3f45", 3, 55, 1), stroke: "none", roughness: 1 })));
  const nuage = (cx, cy, r, couleur) => {
    const pts = []; const n = 18;
    for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2; const k = 1 + 0.2 * Math.sin(a * 5 + 1) + (rnd() - 0.5) * 0.12; pts.push([cx + Math.cos(a) * r * k * 1.1, cy + Math.sin(a) * r * k * 0.95]); }
    add(rc.polygon(pts, o({ ...hach(couleur, 3.2, -50, 1.3), stroke: "#2c5a32", strokeWidth: 1.4, roughness: 1.8 })));
    for (let i = 0; i < 4; i++) { const a = rnd() * 6.28, d = rnd() * r * 0.5; add(rc.arc(cx + Math.cos(a) * d, cy + Math.sin(a) * d, r * 0.55, r * 0.4, 0.3, 2.6, false, o({ stroke: "#2c5a32", strokeWidth: 1, roughness: 1.4 }))); }
  };
  const arbre = (x, h, r) => {
    add(rc.line(x - 3, G, x - 2.5, G - h, o({ strokeWidth: 1.8 })));
    add(rc.line(x + 3, G, x + 2.5, G - h, o({ strokeWidth: 1.8 })));
    add(rc.line(x, G - h + 6, x - r * 0.5, G - h - r * 0.4, o({ strokeWidth: 1.4, roughness: 1 })));
    add(rc.line(x, G - h + 6, x + r * 0.5, G - h - r * 0.4, o({ strokeWidth: 1.4, roughness: 1 })));
    nuage(x, G - h - r * 0.35, r, "#6fae5c");
  };
  const lampe = (x, h, cone, jaune = true) => {
    if (cone) add(rc.polygon([[x, G - h], [x - cone, G], [x + cone, G]], o({ ...hach("#f4cf4a", 4.5, 70, 0.9), stroke: "none", roughness: 1 })));
    add(rc.line(x, G, x, G - h, o({ strokeWidth: 2.2, roughness: 1 })));
    add(rc.rectangle(x - 8, G - h - 5, 16, 6, o({ fill: INK, fillStyle: "solid", roughness: 0.8 })));
    add(rc.circle(x, G - h + 5, 7, o({ fill: "#f4cf4a", fillStyle: "solid", strokeWidth: 1, roughness: 0.8 })));
  };
  const banc = (x) => {
    add(rc.rectangle(x - 17, G - 16, 34, 4, o({ ...hach("#a06b3f", 2, 45), roughness: 1 })));
    add(rc.rectangle(x - 17, G - 26, 34, 3, o({ ...hach("#a06b3f", 2, 45), roughness: 1 })));
    add(rc.line(x - 14, G - 12, x - 14, G, o({ strokeWidth: 1.6, roughness: 0.8 })));
    add(rc.line(x + 14, G - 12, x + 14, G, o({ strokeWidth: 1.6, roughness: 0.8 })));
    add(rc.line(x - 15, G - 16, x - 15, G - 26, o({ strokeWidth: 1.2, roughness: 0.8 })));
  };
  const poubelle = (x) => {
    add(rc.rectangle(x - 6, G - 20, 12, 20, o({ ...hach("#3d8a63", 2.5, 60, 1.1), roughness: 1.1 })));
    add(rc.line(x - 8, G - 21, x + 8, G - 21, o({ strokeWidth: 2.2, roughness: 0.8 })));
  };
  const personne = (x, couleur, assis) => {
    const ty = assis ? G - 15 : G - 14;
    add(rc.circle(x, assis ? G - 38 : G - 41, 9, o({ fill: "#f2cba3", fillStyle: "solid", strokeWidth: 1.3, roughness: 0.9 })));
    add(rc.rectangle(x - 5, assis ? G - 33 : G - 36, 10, 18, o({ ...hach(couleur, 2.2, 50, 1.3), strokeWidth: 1.3, roughness: 1 })));
    if (assis) { add(rc.line(x - 2, G - 16, x + 12, G - 16, o({ strokeWidth: 1.6, roughness: 0.8 }))); add(rc.line(x + 12, G - 16, x + 12, G, o({ strokeWidth: 1.6, roughness: 0.8 }))); }
    else { add(rc.line(x - 2.5, ty + 2, x - 3, G, o({ strokeWidth: 1.6, roughness: 0.8 }))); add(rc.line(x + 2.5, ty + 2, x + 3, G, o({ strokeWidth: 1.6, roughness: 0.8 }))); }
  };
  const voiture = (x, couleur) => {
    add(rc.polygon([[x, G - 8], [x, G - 20], [x + 12, G - 22], [x + 18, G - 33], [x + 40, G - 33], [x + 48, G - 22], [x + 56, G - 20], [x + 56, G - 8]], o({ ...hach(couleur, 3, 45, 1), roughness: 1.4 })));
    add(rc.rectangle(x + 21, G - 30, 22, 8, o({ fill: "#cfe3ec", fillStyle: "solid", strokeWidth: 1, roughness: 0.8 })));
    [x + 12, x + 44].forEach((cx) => add(rc.circle(cx, G - 7, 12, o({ fill: INK, fillStyle: "solid", roughness: 0.8 }))));
  };
  const table = (x) => {
    add(rc.line(x - 10, G - 16, x + 10, G - 16, o({ strokeWidth: 2, roughness: 0.8 })));
    add(rc.line(x, G - 16, x, G, o({ strokeWidth: 1.5, roughness: 0.8 })));
    add(rc.line(x - 8, G - 8, x - 9, G, o({ strokeWidth: 1.2, roughness: 0.8 }))); add(rc.line(x + 8, G - 8, x + 9, G, o({ strokeWidth: 1.2, roughness: 0.8 })));
  };
  const auvent = (x, w) => {
    add(rc.polygon([[x, G - 48], [x + w, G - 48], [x + w + 9, G - 36], [x - 9, G - 36]], o({ ...hach("#d9573d", 3, 60, 1.2), roughness: 1.2 })));
  };
  const jardiniere = (x, w) => {
    add(rc.rectangle(x, G - 12, w, 12, o({ ...hach("#8a6a4a", 3, 45), roughness: 1.1 })));
    for (let i = 0; i < Math.floor(w / 12); i++) add(rc.circle(x + 8 + i * 12, G - 17, 14, o({ ...hach("#5fae58", 2.8, -45, 1.1), stroke: "#2c5a32", strokeWidth: 1.2, roughness: 1.4 })));
  };
  const fontaine = (x) => {
    add(rc.rectangle(x - 22, G - 10, 44, 10, o({ ...hach("#8fb4cc", 3, 45), roughness: 1.2 })));
    add(rc.rectangle(x - 4, G - 30, 8, 20, o({ ...hach("#8fb4cc", 3, 45), roughness: 1 })));
    add(rc.curve([[x, G - 30], [x - 14, G - 46], [x - 26, G - 36], [x - 28, G - 12]], o({ stroke: "#2b8fd0", strokeWidth: 2, roughness: 1 })));
    add(rc.curve([[x, G - 30], [x + 14, G - 46], [x + 26, G - 36], [x + 28, G - 12]], o({ stroke: "#2b8fd0", strokeWidth: 2, roughness: 1 })));
    add(rc.line(x, G - 30, x, G - 48, o({ stroke: "#2b8fd0", strokeWidth: 2, roughness: 0.8 })));
  };
  const soleil = (cx, cy, r) => {
    add(rc.circle(cx, cy, r * 2, o({ ...hach("#f6b92b", 3, 45, 1.6), stroke: "#d98e0b", roughness: 1.4 })));
    for (let i = 0; i < 12; i++) { const a = (i / 12) * Math.PI * 2; add(rc.line(cx + Math.cos(a) * r * 1.35, cy + Math.sin(a) * r * 1.35, cx + Math.cos(a) * r * 1.95, cy + Math.sin(a) * r * 1.95, o({ stroke: "#d98e0b", strokeWidth: 1.8, roughness: 1 }))); }
  };
  const marqueur = (x, y, n, c, tx, ty) => {
    if (tx !== undefined) { add(rc.line(x, y, tx, ty, o({ stroke: c, strokeWidth: 1.8, roughness: 1.1 }))); add(rc.circle(tx, ty, 6, o({ fill: c, fillStyle: "solid", stroke: c, roughness: 0.6 }))); }
    add(rc.circle(x, y, 26, o({ fill: c, fillStyle: "solid", stroke: INK, strokeWidth: 1.6, roughness: 1.2 })));
    texte(String(n), x, y + 7, { taille: 22, gras: true, couleur: "#fff", ancre: "middle" });
  };
  const manque = (x, y, w, h) => add(rc.rectangle(x, y, w, h, o({ stroke: ROUGE, strokeWidth: 1.7, strokeLineDash: [7, 6], roughness: 1.5 })));

  // ---------- composition ----------
  soleil(660, 40, 15);
  add(rc.rectangle(122, G - 8, 78, 8, o({ stroke: "none", ...hach("#b7ad9a", 3, 45), roughness: 1 })));
  auvent(128, 62); auvent(628, 62);
  voiture(222, "#7d8a97"); voiture(540, "#9aa7b2");
  if (!apres) {
    lampe(212, 120, 60); lampe(608, 120, 60);
    ombre(350, 38); arbre(350, 74, 30); ombre(470, 38); arbre(470, 74, 30);
    [150, 176, 650, 676].forEach(table);
    personne(140, "#b5513a"); personne(166, "#4a6fa5"); personne(660, "#6a8f3f"); personne(686, "#8d5aa6");
    banc(372); personne(368, "#d98c2b", true);
    manque(118, G - 72, 88, 72); manque(616, G - 72, 86, 72); manque(482, G - 28, 18, 28); manque(388, G - 40, 50, 40);
    marqueur(410, G - 160, 1, ROUGE, 410, G - 105);
    marqueur(128, G - 135, 2, ROUGE, 140, G - 58);
    marqueur(705, G + 22, 3, ROUGE);
    marqueur(190, G - 105, 4, ROUGE, 178, G - 58);
    marqueur(372, G - 62, 5, ROUGE, 372, G - 30);
    marqueur(491, G - 52, 6, ROUGE);
    marqueur(413, G - 62, 7, ROUGE);
    texte("promenade sombre le soir", 440, G - 175, { couleur: ROUGE, taille: 20, rot: -3 });
    texte("trottoirs nus, plein soleil", 150, G - 172, { couleur: ROUGE, taille: 20, rot: -2 });
    texte("plein soleil !", 535, 55, { couleur: "#b8780b", taille: 21, rot: -4 });
    fleche(595, 62, 628, 52, "#b8780b");
    texte("rien pour s'abriter", 505, G - 140, { couleur: ROUGE, taille: 19, rot: 2 });
  } else {
    lampe(212, 120, 60); lampe(608, 120, 60);
    ombre(193, 34); arbre(193, 66, 22); ombre(627, 34); arbre(627, 66, 22); ombre(142, 26); ombre(678, 26);
    [150, 176, 650, 676].forEach(table);
    personne(138, "#b5513a", true); personne(166, "#4a6fa5"); personne(655, "#6a8f3f", true); personne(690, "#8d5aa6");
    add(rc.polygon([[120, G - 92], [166, G - 76], [166, G - 70], [120, G - 86]], o({ ...hach("#e7a63a", 2.2, 50, 1.4), roughness: 1.2 })));
    add(rc.line(166, G - 73, 166, G, o({ strokeWidth: 2, roughness: 0.9 })));
    add(rc.polygon([[700, G - 92], [654, G - 76], [654, G - 70], [700, G - 86]], o({ ...hach("#e7a63a", 2.2, 50, 1.4), roughness: 1.2 })));
    add(rc.line(654, G - 73, 654, G, o({ strokeWidth: 2, roughness: 0.9 })));
    poubelle(124); poubelle(696);
    ombre(350, 46); arbre(350, 76, 32); ombre(470, 46); arbre(470, 76, 32);
    [338, 388, 438, 500].forEach((x) => lampe(x, 62, 28));
    jardiniere(322, 28); jardiniere(484, 22);
    banc(372); personne(368, "#d98c2b", true); banc(455); personne(450, "#3f8fa5", true); poubelle(397); poubelle(490);
    fontaine(416);
    marqueur(420, G - 150, 1, VERT, 390, G - 60);
    marqueur(128, G - 135, 2, VERT, 190, G - 92);
    marqueur(705, G + 22, 3, VERT);
    marqueur(120, G - 110, 4, VERT, 140, G - 82);
    marqueur(372, G - 62, 5, VERT, 372, G - 30);
    marqueur(491, G - 52, 6, VERT, 490, G - 24);
    marqueur(416, G - 68, 7, VERT);
    texte("lumière basse et chaude", 445, G - 168, { couleur: VERT, taille: 20, rot: -3 });
    texte("arbres + ombre sur les trottoirs", 150, G - 172, { couleur: VERT, taille: 20, rot: -2 });
    texte("ombre : on peut rester", 505, G - 140, { couleur: VERT, taille: 20, rot: 2 });
  }
  // cadre dessine a la main
  add(rc.rectangle(3, 3, W - 6, H - 6, o({ strokeWidth: 2.2, roughness: 1.6 })));
}

document.fonts.ready.then(() => {
  document.querySelectorAll("svg.dessin").forEach((s) => { SEED = 7; rs = 12345; dessiner(s, s.dataset.apres === "1"); });
  document.querySelectorAll("svg.trait").forEach((s, i) => {
    const rc = rough.svg(s); const w = +s.getAttribute("data-w"), h = +s.getAttribute("data-h");
    s.appendChild(rc.line(2, h / 2, w - 2, h / 2, { stroke: s.dataset.c || "#23262b", strokeWidth: +(s.dataset.sw || 1.4), roughness: 1.8, bowing: 2, seed: 100 + i }));
  });
  document.body.dataset.pret = "1";
});
`;

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face { font-family: "Caveat"; font-weight: 400; src: url("fonts/caveat-latin-400-normal.woff2"); }
@font-face { font-family: "Caveat"; font-weight: 700; src: url("fonts/caveat-latin-700-normal.woff2"); }
@font-face { font-family: "Patrick"; font-weight: 400; src: url("fonts/patrick-hand-latin-400-normal.woff2"); }
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { width: 297mm; height: 210mm; font-family: "Patrick", cursive; color: #23262b; background: #fbf8f0; padding: 6mm 9mm 4mm; overflow: hidden; display: flex; flex-direction: column; }
header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1mm; }
h1 { font-family: "Caveat", cursive; font-weight: 700; font-size: 29pt; line-height: .95; }
header p { font-size: 11pt; color: #555; text-align: right; line-height: 1.25; }
.trait { display: block; width: 100%; height: 3mm; }
.corps { display: flex; gap: 5mm; flex: 1; min-height: 0; margin-top: 2.5mm; }
.dessins { width: 198mm; display: flex; flex-direction: column; gap: 2.5mm; }
.cadre { position: relative; line-height: 0; }
.cadre svg.dessin { width: 100%; height: auto; display: block; }
.etiquette { position: absolute; left: 3mm; top: 2.5mm; font: 700 17pt "Caveat"; padding: 0 3mm; color: #fff; line-height: 1.25; transform: rotate(-1.5deg); border-radius: 2mm; }
.avant .etiquette { background: #c8402f; } .apres .etiquette { background: #2f8f5b; }
aside { flex: 1; display: flex; flex-direction: column; }
aside h2 { font-family: "Caveat"; font-weight: 700; font-size: 19pt; line-height: 1; margin-bottom: 1mm; }
.ligne { display: grid; grid-template-columns: 7mm 1fr; gap: 2mm; padding: 1.2mm 0 1.3mm; }
.num { width: 6.5mm; height: 6.5mm; border: .5mm solid #23262b; border-radius: 50%; font: 700 12pt "Caveat"; display: flex; align-items: center; justify-content: center; transform: rotate(-4deg); }
.ligne b { font-family: "Caveat"; font-size: 14pt; font-weight: 700; display: block; line-height: 1; margin-bottom: .4mm; }
.ligne div { font-size: 9.2pt; line-height: 1.22; }
.x { color: #c8402f; font-weight: 700; } .v { color: #2f8f5b; font-weight: 700; }
.note { margin-top: auto; font-size: 8.8pt; color: #555; line-height: 1.25; padding-top: 1.5mm; }
</style></head><body>
<header><h1>Avenue Habib Bourguiba (Tunis) :<br>ce qui manque, et ce qu'on corrige</h1>
<p>Sociologie · 1re année Architecture · ESAD Tunis<br>Coupe transversale (croquis), sans échelle · Nom : ____________</p></header>
<svg class="trait" data-w="1000" data-h="12" viewBox="0 0 1000 12" preserveAspectRatio="none" data-sw="2.2"></svg>
<div class="corps">
 <div class="dessins">
  <div class="cadre avant"><span class="etiquette">AVANT · l'existant et ses manques</span><svg class="dessin" data-apres="0" viewBox="0 0 820 335"></svg></div>
  <div class="cadre apres"><span class="etiquette">APRÈS · notre proposition</span><svg class="dessin" data-apres="1" viewBox="0 0 820 335"></svg></div>
 </div>
 <aside><h2>7 manques → 7 réponses</h2>
 ${LEG.map(([n, t, a, b]) => `<svg class="trait" data-w="300" data-h="6" viewBox="0 0 300 6" preserveAspectRatio="none" data-c="#999" data-sw="1"></svg><div class="ligne"><span class="num">${n}</span><div><b>${t}</b><span class="x">✗ </span>${a}<br><span class="v">✓ </span>${b}</div></div>`).join("")}
 <p class="note">Pointillés rouges : endroits où l'aménagement fait défaut. Les numéros de « Après » reprennent ceux de « Avant ».</p></aside>
</div>
<script src="vendor/rough.js"></script><script>${script}</script></body></html>`;

(async () => {
  const dir = path.join(__dirname, "..");
  fs.writeFileSync(path.join(__dirname, "croquis.html"), html);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 2 });
  page.on("pageerror", (e) => console.log("ERREUR PAGE:", e.message));
  await page.goto("file://" + path.join(__dirname, "croquis.html"));
  await page.waitForFunction(() => document.body.dataset.pret === "1", null, { timeout: 20000 });
  await page.pdf({ path: path.join(dir, "Avenue_Habib_Bourguiba_croquis.pdf"), format: "A4", landscape: true, printBackground: true, preferCSSPageSize: true });
  await page.screenshot({ path: path.join(dir, "Avenue_Habib_Bourguiba_croquis.png") });
  await browser.close();
  console.log("OK");
})();
