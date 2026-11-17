// Fiche A4 : avenue Habib Bourguiba (Tunis), coupe avant / apres.
// Usage : node generer.js  ->  ../Avenue_Habib_Bourguiba_avant_apres.pdf (+ .png)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const G = 285;               // ligne de sol
const W = 820, H = 335;
const ROUGE = "#c8402f", VERT = "#2f8f5b";

const tree = (x, h, r, o = {}) => `
  <rect x="${x - 3}" y="${G - h}" width="6" height="${h}" fill="#6b4a32"/>
  <circle cx="${x - r * 0.65}" cy="${G - h + r * 0.05}" r="${r * 0.72}" fill="#4d8f4c"/>
  <circle cx="${x + r * 0.65}" cy="${G - h + r * 0.05}" r="${r * 0.72}" fill="#4d8f4c"/>
  <circle cx="${x}" cy="${G - h - r * 0.3}" r="${r}" fill="#3a7d44"/>
  <circle cx="${x - r * 0.3}" cy="${G - h - r * 0.55}" r="${r * 0.5}" fill="#5fa05a" opacity=".8"/>`;
const ombre = (x, rx) => `<ellipse cx="${x}" cy="${G + 4}" rx="${rx}" ry="7" fill="#1d2b22" opacity=".28"/>`;
const lampe = (x, h, cone, couleur = "#f4c542") => `
  ${cone ? `<polygon points="${x},${G - h} ${x - cone},${G} ${x + cone},${G}" fill="${couleur}" opacity=".22"/>` : ""}
  <line x1="${x}" y1="${G}" x2="${x}" y2="${G - h}" stroke="#2b3138" stroke-width="3"/>
  <rect x="${x - 7}" y="${G - h - 4}" width="14" height="6" rx="2" fill="#2b3138"/>
  <circle cx="${x}" cy="${G - h + 3}" r="3.5" fill="${couleur}"/>`;
const banc = (x) => `
  <rect x="${x - 17}" y="${G - 15}" width="34" height="4" rx="1" fill="#8a5a36"/>
  <rect x="${x - 17}" y="${G - 24}" width="34" height="3" rx="1" fill="#8a5a36"/>
  <line x1="${x - 14}" y1="${G - 11}" x2="${x - 14}" y2="${G}" stroke="#2b3138" stroke-width="2"/>
  <line x1="${x + 14}" y1="${G - 11}" x2="${x + 14}" y2="${G}" stroke="#2b3138" stroke-width="2"/>`;
const poubelle = (x) => `
  <rect x="${x - 6}" y="${G - 20}" width="12" height="20" rx="2" fill="#3d6f55"/>
  <rect x="${x - 7}" y="${G - 23}" width="14" height="4" rx="1" fill="#2b4a3a"/>`;
const personne = (x, couleur, assis = false) => assis
  ? `<circle cx="${x}" cy="${G - 36}" r="4.5" fill="#e0b48a"/><rect x="${x - 5}" y="${G - 31}" width="10" height="13" rx="3" fill="${couleur}"/><rect x="${x - 5}" y="${G - 19}" width="16" height="4" rx="2" fill="#2b3138"/>`
  : `<circle cx="${x}" cy="${G - 40}" r="4.5" fill="#e0b48a"/><rect x="${x - 5}" y="${G - 35}" width="10" height="22" rx="3" fill="${couleur}"/><rect x="${x - 4}" y="${G - 14}" width="3" height="14" fill="#2b3138"/><rect x="${x + 1}" y="${G - 14}" width="3" height="14" fill="#2b3138"/>`;
const voiture = (x, couleur) => `
  <rect x="${x}" y="${G - 22}" width="54" height="14" rx="5" fill="${couleur}"/>
  <rect x="${x + 12}" y="${G - 32}" width="28" height="12" rx="4" fill="${couleur}"/>
  <rect x="${x + 16}" y="${G - 30}" width="20" height="8" rx="2" fill="#cfe3ec"/>
  <circle cx="${x + 12}" cy="${G - 8}" r="6" fill="#222"/><circle cx="${x + 42}" cy="${G - 8}" r="6" fill="#222"/>`;
const jardiniere = (x, w) => `
  <rect x="${x}" y="${G - 12}" width="${w}" height="12" fill="#7a5a40"/>
  ${Array.from({ length: Math.floor(w / 12) }, (_, i) => `<circle cx="${x + 7 + i * 12}" cy="${G - 16}" r="8" fill="${i % 2 ? "#5fa05a" : "#3a7d44"}"/>`).join("")}`;
const fontaine = (x) => `
  <rect x="${x - 22}" y="${G - 10}" width="44" height="10" rx="2" fill="#9fb4bf"/>
  <rect x="${x - 4}" y="${G - 30}" width="8" height="20" fill="#9fb4bf"/>
  <path d="M${x} ${G - 30} Q${x - 22} ${G - 52} ${x - 28} ${G - 12}" fill="none" stroke="#4aa3d8" stroke-width="2.5"/>
  <path d="M${x} ${G - 30} Q${x + 22} ${G - 52} ${x + 28} ${G - 12}" fill="none" stroke="#4aa3d8" stroke-width="2.5"/>
  <path d="M${x} ${G - 30} L${x} ${G - 48}" stroke="#4aa3d8" stroke-width="2.5"/>`;
const marqueur = (x, y, n, couleur, tx, ty) => `${tx === undefined ? "" : `<line x1="${x}" y1="${y}" x2="${tx}" y2="${ty}" stroke="${couleur}" stroke-width="1.8"/><circle cx="${tx}" cy="${ty}" r="3" fill="${couleur}"/>`}<circle cx="${x}" cy="${y}" r="11" fill="${couleur}" stroke="#fff" stroke-width="2"/><text x="${x}" y="${y + 4.5}" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">${n}</text>`;
const manque = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="none" stroke="${ROUGE}" stroke-width="1.6" stroke-dasharray="5 4"/>`;
const batiment = (x, w, cote) => {
  let s = `<rect x="${x}" y="40" width="${w}" height="${G - 40}" fill="${cote === "g" ? "#dccdb2" : "#d4c3a6"}"/><rect x="${x}" y="40" width="${w}" height="8" fill="#b9a784"/>`;
  for (let r = 0; r < 5; r++) for (let c = 0; c < 3; c++) {
    const wx = x + 12 + c * ((w - 24) / 3), wy = 62 + r * 38;
    s += `<rect x="${wx}" y="${wy}" width="22" height="26" fill="#5d6e7a"/><rect x="${wx - 3}" y="${wy + 26}" width="28" height="3" fill="#b9a784"/><line x1="${wx + 11}" y1="${wy}" x2="${wx + 11}" y2="${wy + 26}" stroke="#d4c3a6" stroke-width="1.5"/>`;
  }
  s += `<rect x="${x}" y="${G - 40}" width="${w}" height="40" fill="#bfae8f"/>`;
  return s;
};
const auvent = (x, w) => `<polygon points="${x},${G - 46} ${x + w},${G - 46} ${x + w + 10},${G - 36} ${x - 10},${G - 36}" fill="#c8402f"/><polygon points="${x + 20},${G - 46} ${x + 40},${G - 46} ${x + 40 + 7},${G - 36} ${x + 20 - 7},${G - 36}" fill="#f3e6d0"/><polygon points="${x + 60},${G - 46} ${x + 80},${G - 46} ${x + 87},${G - 36} ${x + 53},${G - 36}" fill="#f3e6d0"/>`;
const table = (x) => `<rect x="${x - 9}" y="${G - 16}" width="18" height="3" fill="#6b4a32"/><line x1="${x}" y1="${G - 13}" x2="${x}" y2="${G}" stroke="#6b4a32" stroke-width="2"/><line x1="${x - 8}" y1="${G - 10}" x2="${x - 8}" y2="${G}" stroke="#6b4a32" stroke-width="1.5"/><line x1="${x + 8}" y1="${G - 10}" x2="${x + 8}" y2="${G}" stroke="#6b4a32" stroke-width="1.5"/>`;
const soleil = (cx, cy, r) => `${Array.from({ length: 12 }, (_, i) => { const a = i / 12 * Math.PI * 2; return `<line x1="${cx + Math.cos(a) * r * 1.35}" y1="${cy + Math.sin(a) * r * 1.35}" x2="${cx + Math.cos(a) * r * 1.9}" y2="${cy + Math.sin(a) * r * 1.9}" stroke="#f0a920" stroke-width="3" stroke-linecap="round"/>`; }).join("")}<circle cx="${cx}" cy="${cy}" r="${r}" fill="#f6b92b"/>`;

const decor = (apres) => `
  <rect width="${W}" height="${H}" fill="${apres ? "#e3f1f3" : "#efe6d3"}"/>
  ${soleil(660, 34, 14)}
  ${batiment(0, 120, "g")}${batiment(700, 120, "d")}
  <rect x="0" y="${G}" width="${W}" height="${H - G}" fill="#8a7f70"/>
  <rect x="0" y="${G}" width="${W}" height="4" fill="#6f6557"/>
  <rect x="120" y="${G}" width="80" height="6" fill="#bdb8ae"/><rect x="620" y="${G}" width="80" height="6" fill="#bdb8ae"/>
  <rect x="200" y="${G}" width="110" height="6" fill="#4c5158"/><rect x="510" y="${G}" width="110" height="6" fill="#4c5158"/>
  <rect x="310" y="${G}" width="200" height="6" fill="${apres ? "#d6cfbf" : "#c4bdae"}"/>
  ${apres ? `<rect x="326" y="${G}" width="30" height="6" fill="#8fbf7f"/><rect x="464" y="${G}" width="30" height="6" fill="#8fbf7f"/><rect x="126" y="${G}" width="12" height="6" fill="#8fbf7f"/><rect x="682" y="${G}" width="12" height="6" fill="#8fbf7f"/>` : ""}
  <g stroke="#e8e8e8" stroke-width="2" stroke-dasharray="14 10"><line x1="255" y1="${G + 3}" x2="255" y2="${G + 3}"/></g>
  <text x="160" y="${G + 24}" text-anchor="middle" font-size="9.5" fill="#f2ece0">trottoir</text>
  <text x="255" y="${G + 24}" text-anchor="middle" font-size="9.5" fill="#f2ece0">chaussée</text>
  <text x="410" y="${G + 24}" text-anchor="middle" font-size="9.5" fill="#f2ece0">promenade centrale</text>
  <text x="565" y="${G + 24}" text-anchor="middle" font-size="9.5" fill="#f2ece0">chaussée</text>
  <text x="660" y="${G + 24}" text-anchor="middle" font-size="9.5" fill="#f2ece0">trottoir</text>
  ${auvent(128, 62)}${auvent(628, 62)}`;

const avant = () => `
  ${decor(false)}
  ${voiture(222, "#7f8c99")}${voiture(540, "#a3b0b9")}
  ${lampe(212, 120, 60)}${lampe(608, 120, 60)}
  ${ombre(350, 38)}${tree(350, 74, 30)}${ombre(470, 38)}${tree(470, 74, 30)}
  ${table(150)}${table(176)}${table(650)}${table(676)}
  ${personne(140, "#b5513a")}${personne(166, "#4a6fa5")}${personne(660, "#6a8f3f")}${personne(686, "#8d5aa6")}
  ${banc(372)}${personne(368, "#d98c2b", true)}
  ${manque(118, G - 72, 88, 72)}${manque(616, G - 72, 86, 72)}${manque(482, G - 28, 18, 28)}${manque(388, G - 40, 50, 40)}
  ${marqueur(410, G - 160, 1, ROUGE, 410, G - 105)}${marqueur(128, G - 135, 2, ROUGE, 140, G - 58)}${marqueur(705, G + 20, 3, ROUGE)}${marqueur(190, G - 105, 4, ROUGE, 178, G - 58)}${marqueur(372, G - 62, 5, ROUGE, 372, G - 30)}${marqueur(491, G - 52, 6, ROUGE)}${marqueur(413, G - 62, 7, ROUGE)}`;

const apres = () => `
  ${decor(true)}
  ${voiture(222, "#7f8c99")}${voiture(540, "#a3b0b9")}
  ${lampe(212, 120, 60)}${lampe(608, 120, 60)}
  ${ombre(193, 34)}${tree(193, 66, 22)}${ombre(627, 34)}${tree(627, 66, 22)}
  ${ombre(142, 26)}${ombre(678, 26)}
  ${table(150)}${table(176)}${table(650)}${table(676)}
  ${personne(138, "#b5513a", true)}${personne(166, "#4a6fa5")}${personne(655, "#6a8f3f", true)}${personne(690, "#8d5aa6")}
  <polygon points="120,${G - 92} 166,${G - 76} 166,${G - 70} 120,${G - 86}" fill="#e7a63a"/><line x1="166" y1="${G - 73}" x2="166" y2="${G}" stroke="#2b3138" stroke-width="2.5"/>
  <polygon points="700,${G - 92} 654,${G - 76} 654,${G - 70} 700,${G - 86}" fill="#e7a63a"/><line x1="654" y1="${G - 73}" x2="654" y2="${G}" stroke="#2b3138" stroke-width="2.5"/>
  ${poubelle(124)}${poubelle(696)}
  ${ombre(350, 46)}${tree(350, 76, 32)}${ombre(470, 46)}${tree(470, 76, 32)}
  ${lampe(338, 62, 30)}${lampe(390, 62, 28)}${lampe(438, 62, 28)}${lampe(500, 62, 30)}
  ${jardiniere(322, 28)}${jardiniere(484, 22)}
  ${banc(372)}${personne(368, "#d98c2b", true)}${banc(455)}${personne(450, "#3f8fa5", true)}${poubelle(397)}${poubelle(490)}
  ${fontaine(416)}
  ${marqueur(420, G - 150, 1, VERT, 390, G - 60)}${marqueur(128, G - 135, 2, VERT, 190, G - 92)}${marqueur(705, G + 20, 3, VERT)}${marqueur(120, G - 110, 4, VERT, 140, G - 82)}${marqueur(372, G - 62, 5, VERT, 372, G - 30)}${marqueur(491, G - 52, 6, VERT, 490, G - 24)}${marqueur(416, G - 68, 7, VERT)}`;

const LEG = [
  ["1", "Éclairage", "Lampadaires hauts tournés vers la chaussée : promenade sombre le soir.", "Lampes basses (≈ 4 m) le long des allées, lumière chaude et douce."],
  ["2", "Végétation", "Arbres seulement au centre ; trottoirs nus.", "Arbres d'alignement sur les trottoirs, jardinières, bandes plantées."],
  ["3", "Minéralité", "Tout est dur (dalles, béton) : chaleur, eau qui ruisselle.", "Sols mixtes : dalles claires + bandes perméables plantées."],
  ["4", "Ombrage et lumière", "Terrasses et trottoirs en plein soleil, éblouissement.", "Canopée des arbres et voiles d'ombrage au-dessus des terrasses."],
  ["5", "Places pour s'asseoir", "Un seul banc pour toute la promenade.", "Bancs sous les arbres, régulièrement espacés."],
  ["6", "Poubelles", "Aucune à proximité des assises et terrasses.", "Poubelles de tri près des bancs et sur les trottoirs."],
  ["7", "Fraîcheur (bonus)", "Aucun point d'eau.", "Fontaine / brumisateur au centre de la promenade."],
];

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face { font-family: "Inter"; font-weight: 400; src: url("../../sociologie-goffman/sources/fonts/inter-latin-400-normal.woff2"); }
@font-face { font-family: "Inter"; font-weight: 600; src: url("../../sociologie-goffman/sources/fonts/inter-latin-600-normal.woff2"); }
@font-face { font-family: "Inter"; font-weight: 800; src: url("../../sociologie-goffman/sources/fonts/inter-latin-800-normal.woff2"); }
@font-face { font-family: "Playfair"; font-weight: 700; src: url("../../sociologie-goffman/sources/fonts/playfair-display-latin-700-normal.woff2"); }
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { width: 297mm; height: 210mm; font-family: "Inter", sans-serif; color: #1f2328; background: #fffdf8; padding: 8mm 8mm 6mm; display: flex; flex-direction: column; }
svg text { font-family: "Inter", sans-serif; }
header { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: .5mm solid #1f2328; padding-bottom: 2mm; margin-bottom: 3mm; }
h1 { font-family: "Playfair", serif; font-size: 20pt; line-height: 1.05; }
header p { font-size: 8.5pt; color: #5f6670; text-align: right; line-height: 1.35; }
.corps { display: flex; gap: 5mm; flex: 1; min-height: 0; }
.dessins { width: 205mm; display: flex; flex-direction: column; gap: 3mm; }
.cadre { position: relative; border: .3mm solid #1f2328; border-radius: 2mm; overflow: hidden; line-height: 0; }
.cadre svg { width: 100%; height: auto; display: block; }
.etiquette { position: absolute; left: 2.5mm; top: 2.5mm; font: 800 8.5pt "Inter"; padding: 1.2mm 3mm; border-radius: 10mm; color: #fff; line-height: 1.2; }
.avant .etiquette { background: #c8402f; } .apres .etiquette { background: #2f8f5b; }
aside { flex: 1; display: flex; flex-direction: column; }
aside h2 { font-family: "Playfair", serif; font-size: 12.5pt; margin-bottom: 2mm; }
.ligne { display: grid; grid-template-columns: 6.5mm 1fr; gap: 2mm; padding: 1.8mm 0; border-top: .2mm solid #dfe3e8; }
.num { width: 5.5mm; height: 5.5mm; border-radius: 50%; background: #1f2328; color: #fff; font: 800 8pt "Inter"; display: flex; align-items: center; justify-content: center; }
.ligne b { font-size: 8.8pt; display: block; margin-bottom: .6mm; }
.ligne div { font-size: 7.6pt; line-height: 1.3; }
.x { color: #c8402f; font-weight: 600; } .v { color: #2f8f5b; font-weight: 600; }
.note { margin-top: auto; font-size: 7pt; color: #5f6670; line-height: 1.35; border-top: .2mm solid #dfe3e8; padding-top: 1.5mm; }
</style></head><body>
<header><h1>Avenue Habib Bourguiba (Tunis) :<br>ce qui manque, et ce qu'on corrige</h1>
<p>Sociologie · 1re année Architecture · ESAD Tunis<br>Coupe transversale schématique, sans échelle · Nom : ____________</p></header>
<div class="corps">
 <div class="dessins">
  <div class="cadre avant"><span class="etiquette">AVANT · l'existant et ses manques</span><svg viewBox="0 0 ${W} ${H}">${avant()}</svg></div>
  <div class="cadre apres"><span class="etiquette">APRÈS · notre proposition</span><svg viewBox="0 0 ${W} ${H}">${apres()}</svg></div>
 </div>
 <aside><h2>7 manques → 7 réponses</h2>
 ${LEG.map(([n, t, a, b]) => `<div class="ligne"><span class="num">${n}</span><div><b>${t}</b><span class="x">✗ </span>${a}<br><span class="v">✓ </span>${b}</div></div>`).join("")}
 <p class="note">Zones en pointillés rouges : endroits où l'aménagement fait défaut. Les numéros du dessin « Après » reprennent ceux de « Avant ».</p></aside>
</div></body></html>`;

(async () => {
  const dir = path.join(__dirname, "..");
  fs.writeFileSync(path.join(__dirname, "fiche.html"), html);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 2 });
  await page.goto("file://" + path.join(__dirname, "fiche.html"));
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(dir, "Avenue_Habib_Bourguiba_avant_apres.pdf"), format: "A4", landscape: true, printBackground: true, preferCSSPageSize: true });
  await page.screenshot({ path: path.join(dir, "Avenue_Habib_Bourguiba_avant_apres.png") });
  await browser.close();
  console.log("OK");
})();
