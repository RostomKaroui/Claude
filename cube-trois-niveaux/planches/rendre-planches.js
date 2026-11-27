// Les 3 planches A3 (paysage) du cube de 10 cm : démarche, axonométrie 1:1, faces 1:2.
// Lancer : THREE_LOCAL=<dossier package de three@0.128.0> NODE_PATH=$(npm root -g) node planches/rendre-planches.js
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const ICI = __dirname, RACINE = path.resolve(ICI, '..');

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const fr = v => String(Math.round(v * 100) / 100).replace('.', ',');

// ---------------------------------------------------------------- schémas de la démarche (SVG en mm)
function schema(id, M) {
  const B = '#2f4fb3', N = '#1e2322';
  if (id === 'projectif') {
    const k = 5.4, o = 4, c = o + 5 * k, s = 6.3 * k;
    let g = `<rect x="${o}" y="${o}" width="${10 * k}" height="${10 * k}" fill="none" stroke="${N}" stroke-width="0.45"/>`;
    g += `<line x1="${o}" y1="${o}" x2="${o + 10 * k}" y2="${o + 10 * k}" stroke="${B}" stroke-width="0.2" stroke-dasharray="1 0.8"/><line x1="${o + 10 * k}" y1="${o}" x2="${o}" y2="${o + 10 * k}" stroke="${B}" stroke-width="0.2" stroke-dasharray="1 0.8"/>`;
    [0, 15, 30, 45].forEach((a, i) => { g += `<rect x="${c - s / 2}" y="${c - s / 2}" width="${s}" height="${s}" fill="none" stroke="${N}" stroke-width="${0.25 + i * 0.08}" stroke-opacity="${0.35 + i * 0.2}" transform="rotate(${-a} ${c} ${c})"/>`; });
    for (const a of [15, 30, 45]) { const r = s / 2 + 3.5 + a / 15 * 0.0, x = c + (s / 2 + 6) * Math.cos(-a * Math.PI / 180), y = c + (s / 2 + 6) * Math.sin(-a * Math.PI / 180); g += `<text x="${x}" y="${y}" font-size="2.6" fill="${B}" text-anchor="middle">${a}°</text>`; }
    g += `<circle cx="${c}" cy="${c}" r="0.9" fill="${B}"/><text x="${c + 2}" y="${c + 4.5}" font-size="2.4" fill="${B}">centre</text>`;
    // élévation : la pique et les hauteurs
    const ex = o + 10 * k + 16, eb = o + 10 * k, hk = 5.4;
    g += `<line x1="${ex - 8}" y1="${eb}" x2="${ex + 8}" y2="${eb}" stroke="${N}" stroke-width="0.45"/><line x1="${ex}" y1="${eb}" x2="${ex}" y2="${eb - 10 * hk}" stroke="${N}" stroke-width="0.35"/>`;
    [2, 4, 6, 8].forEach((h, i) => { const y = eb - h * hk; g += `<line x1="${ex - 6}" y1="${y}" x2="${ex + 6}" y2="${y}" stroke="${N}" stroke-width="0.4"/><text x="${ex + 7.5}" y="${y + 0.9}" font-size="2.4" fill="${B}">${h} cm · ${[0, 15, 30, 45][i]}°</text>`; });
    g += `<text x="${ex - 8}" y="${eb + 4.5}" font-size="2.3" fill="${N}">élévation</text><text x="${o}" y="${o + 10 * k + 4.5}" font-size="2.3" fill="${N}">vue de dessus : le même carré tourne</text>`;
    return { w: 118, h: 64, g };
  }
  if (id === 'metrique') {
    const k = 13, o = 4, G = [[4, 4, 3, 3], [4, 3, 3, 2], [3, 3, 2, 2], [3, 2, 2, 1]], h = (i, j) => G[j][i];   // modules par case (le plus bas des 4 murs)
    let g = '';
    for (let j = 0; j < 4; j++) for (let i = 0; i < 4; i++) { const v = h(i, j), x = o + i * k, y = o + (3 - j) * k;
      g += `<rect x="${x}" y="${y}" width="${k}" height="${k}" fill="${B}" fill-opacity="${0.08 + v * 0.13}" stroke="${N}" stroke-width="0.3"/><text x="${x + k / 2}" y="${y + k / 2 + 1.6}" font-size="4.6" text-anchor="middle" fill="${N}">${v}</text>`; }
    g += `<rect x="${o}" y="${o}" width="${4 * k}" height="${4 * k}" fill="none" stroke="${N}" stroke-width="0.5"/>`;
    g += `<text x="${o}" y="${o + 4 * k + 5}" font-size="2.4" fill="${N}">nombre de modules de 2,5 cm empilés dans chaque colonne</text>`;
    const tx = o + 4 * k + 8;
    const lignes = ['module = 10 ÷ 4 = 2,5 cm', 'division : 4 × 4 × 4 = 64', 'soustraction en escalier :', 'hauteurs 4 · 3 · 2 · 1', '64 − 20 = 44 modules', 'proportions en quarts :', '10 · 7,5 · 5 · 2,5 cm'];
    lignes.forEach((t, i) => { g += `<text x="${tx}" y="${o + 4 + i * 6.2}" font-size="2.9" fill="${i % 2 === 0 ? N : B}">${t}</text>`; });
    return { w: 118, h: 64, g };
  }
  const k = 13, o = 4;      // topologique : le patron du cube et l'opération de chaque face
  const F = [[1, 0, 'toit', 'éliminé'], [0, 1, 'gauche', 'continu'], [1, 1, 'sol', 'continu'], [2, 1, 'droite', 'éliminée'], [3, 1, 'arrière', 'pivotée 30°'], [1, 2, 'avant', 'pivotée 30°']];
  let g = '';
  for (const [i, j, nom, op] of F) { const x = o + i * k * 1.45, y = o + j * k * 1.05;
    const int = op.startsWith('continu');
    g += `<rect x="${x}" y="${y}" width="${k * 1.4}" height="${k}" fill="${int ? 'none' : B}" fill-opacity="${int ? 0 : 0.12}" stroke="${N}" stroke-width="0.35"/><text x="${x + k * 0.7}" y="${y + k / 2 - 0.5}" font-size="2.8" text-anchor="middle" fill="${N}">${nom}</text><text x="${x + k * 0.7}" y="${y + k / 2 + 3}" font-size="2.3" text-anchor="middle" fill="${B}">${op}</text>`; }
  g += `<text x="${o}" y="${o + 3 * k * 1.05 + 4}" font-size="2.4" fill="${N}">en blanc : ce qui reste en place · en bleu : la rupture · aucune face découpée</text>`;
  return { w: 118, h: 64, g };
}

const CAPTIONS = {
  projectif: ['le socle, son centre, la pique', 'les arêtes, les carrés à 0° et 15°', 'les carrés à 30° et 45°'],
  metrique: ['les 5 plaques B, tous les 2,5 cm', 'A0 et A1 : le cube entier', 'A2 à A4 : la soustraction'],
  topologique: ['le sol et le côté gauche', 'la face avant pivotée : la fente', "l'arrière pivotée : la limite virtuelle"],
};
const FACES = [['dessus', 'dessus'], ['devant', 'devant'], ['droite', 'côté droit'], ['gauche', 'côté gauche'], ['arriere', 'arrière'], ['dessous', 'dessous']];

function page(id, n, M, D) {
  const s = schema(id, M);
  const idee = M.idee.replace(/<(?!\/?b>)[^>]+>/g, '');
  const img = (d, cls = '') => `<img class="${cls}" src="${d.url}" style="width:${d.w}mm;height:${d.h}mm" alt="">`;
  return `<section class="planche">
  <header><div><div class="sur">Le cube de 10 cm · planche ${n} / 3</div><h1>${M.niveau} · ${esc(M.titre)}</h1></div>
    <div class="droite">Atelier · espaces projectif, métrique, topologique<br>rendu le vendredi 4 décembre 2026, 8 h 30</div></header>
  <div class="grille">
    <div class="col demarche">
      <h2>Démarche</h2>
      <p>${idee}</p>
      <div class="ops">${M.ops.map(o => `<span>${esc(o)}</span>`).join('')}</div>
      <svg viewBox="0 0 ${s.w} ${s.h}" style="width:${s.w}mm;height:${s.h}mm" font-family="DejaVu Sans Mono, monospace">${s.g}</svg>
      <h3>Le montage en 3 temps</h3>
      <div class="etapes">${D.etapes.map((e, i) => `<figure>${img(e)}<figcaption><b>${i + 1}</b> ${CAPTIONS[id][i]}</figcaption></figure>`).join('')}</div>
    </div>
    <div class="col axo"><figure>${img(D.axo)}<figcaption>Axonométrie 30° / 60° · échelle 1:1 · cube de 10 cm d'arête · carton gris 2 mm</figcaption></figure></div>
    <div class="col faces">
      <h2>Les faces <small>échelle 1:2</small></h2>
      <div class="vues">${FACES.map(([k, t]) => `<figure>${img(D.faces[k])}<figcaption>${t}</figcaption></figure>`).join('')}</div>
      <table class="cartouche"><tr><td>Nom</td><td></td></tr><tr><td>Groupe</td><td></td></tr><tr><td>Maquette</td><td>${n} / 3 · ${M.niveau.replace('Espace ', '')}</td></tr><tr><td>Échelles</td><td>axonométrie 1:1 · faces 1:2</td></tr></table>
    </div>
  </div>
</section>`;
}

(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 1200, height: 900 } });
  const local = process.env.THREE_LOCAL;
  if (local) await ctx.route('https://cdn.jsdelivr.net/npm/three@0.128.0/**', r => r.fulfill({ path: path.join(local, new URL(r.request().url()).pathname.replace('/npm/three@0.128.0/', '')), contentType: 'application/javascript' }));
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('erreur:', e.message));
  await p.goto('file://' + path.join(RACINE, 'index.html')); await p.waitForTimeout(1200);
  await p.addScriptTag({ path: path.join(ICI, 'axo-planches.js') });
  const pages = [];
  for (const [n, id] of [[1, 'projectif'], [2, 'metrique'], [3, 'topologique']]) {
    const D = await p.evaluate(id => PLANCHES.planche(id), id);
    const M = await p.evaluate(id => { const M = MAQUETTES[id]; return { titre: M.titre, niveau: M.niveau, idee: M.idee, ops: M.ops }; }, id);
    console.log(id, 'axo', D.axo.w.toFixed(1), '×', D.axo.h.toFixed(1), 'mm');
    pages.push(page(id, n, M, D));
  }
  const css = fs.readFileSync(path.join(ICI, 'planches.css'), 'utf8');
  const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Le cube de 10 cm · planches A3</title><style>${css}</style></head><body>${pages.join('')}</body></html>`;
  fs.writeFileSync(path.join(ICI, 'planches.html'), html);
  const q = await b.newPage({ viewport: { width: 1588, height: 1123 } });
  await q.goto('file://' + path.join(ICI, 'planches.html')); await q.waitForTimeout(600);
  await q.pdf({ path: path.join(ICI, 'planches-A3.pdf'), width: '420mm', height: '297mm', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  const secs = await q.$$('.planche');
  for (let i = 0; i < secs.length; i++) await secs[i].screenshot({ path: path.join(ICI, `planche-${i + 1}.png`) });
  const deb = await q.evaluate(() => [...document.querySelectorAll('.planche')].map(s => { const r = s.getBoundingClientRect(); let m = 0; s.querySelectorAll('*').forEach(e => { const q = e.getBoundingClientRect(); if (q.height) m = Math.max(m, q.bottom - r.top); }); return [Math.round(r.height), Math.round(m)]; }));
  console.log('hauteur / contenu', JSON.stringify(deb));
  await b.close();
})();
