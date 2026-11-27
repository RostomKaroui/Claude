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
    // la face vue de front : carré, bande, croix, et au fond le carré sur pointe (le même sur les 6 faces)
    const face = (o, oy, k, fin) => {
      let g = `<rect x="${o}" y="${oy}" width="${10 * k}" height="${10 * k}" fill="none" stroke="${N}" stroke-width="${fin ? 0.3 : 0.45}"/>`;
      for (const [a0, a1] of [[0.8, 4.6], [5.4, 9.2]]) for (const [b0, b1] of [[0.8, 4.6], [5.4, 9.2]])
        g += `<rect x="${o + a0 * k}" y="${oy + b0 * k}" width="${(a1 - a0) * k}" height="${(b1 - b0) * k}" fill="none" stroke="${N}" stroke-width="${fin ? 0.2 : 0.3}"/>`;
      const c = 5 * k, r = 4.8 * k;
      g += `<polygon points="${o + c},${oy + c - r} ${o + c + r},${oy + c} ${o + c},${oy + c + r} ${o + c - r},${oy + c}" fill="${B}" fill-opacity="0.10" stroke="${B}" stroke-width="${fin ? 0.25 : 0.35}"/>`;
      return g;
    };
    const k = 5.4, o = 4;
    let g = face(o, o, k, false);
    g += `<circle cx="${o + 5 * k}" cy="${o + 5 * k}" r="0.9" fill="${B}"/><text x="${o + 5 * k + 2}" y="${o + 5 * k - 2}" font-size="2.4" fill="${B}">centre</text>`;
    g += `<text x="${o + 5 * k}" y="${o + 0.2 * k - 1.2}" font-size="2.3" fill="${B}" text-anchor="middle">45°</text>`;
    g += `<text x="${o}" y="${o + 10 * k + 4.5}" font-size="2.3" fill="${N}">une face (les 6 sont pareilles)</text>`;
    const x2 = o + 10 * k + 10, k2 = 1.6;
    ['posée sur une face', 'retournée', 'tournée de côté'].forEach((t, i) => {
      const y = o + i * (10 * k2 + 3);
      g += face(x2, y, k2, true) + `<text x="${x2 + 10 * k2 + 3}" y="${y + 5 * k2 + 1}" font-size="2.4" fill="${N}">${t}</text>`;
    });
    g += `<text x="${x2}" y="${o + 10 * k + 4.5}" font-size="2.3" fill="${B}">même vue : sans base</text>`;
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
  const F = [[1, 0, 'toit', 'continu'], [0, 1, 'gauche', 'continu'], [1, 1, 'sol', 'séparé en 2'], [2, 1, 'droite', 'continu'], [3, 1, 'arrière', 'pivotée 30°'], [1, 2, 'avant', 'remontée']];
  let g = '';
  for (const [i, j, nom, op] of F) { const x = o + i * k * 1.45, y = o + j * k * 1.05;
    const int = op.startsWith('continu');
    g += `<rect x="${x}" y="${y}" width="${k * 1.4}" height="${k}" fill="${int ? 'none' : B}" fill-opacity="${int ? 0 : 0.12}" stroke="${N}" stroke-width="0.35"/><text x="${x + k * 0.7}" y="${y + k / 2 - 0.5}" font-size="2.8" text-anchor="middle" fill="${N}">${nom}</text><text x="${x + k * 0.7}" y="${y + k / 2 + 3}" font-size="2.3" text-anchor="middle" fill="${B}">${op}</text>`; }
  g += `<text x="${o}" y="${o + 3 * k * 1.05 + 4}" font-size="2.4" fill="${N}">en blanc : le tunnel continu · en bleu : ce qui est déplacé</text>`;
  return { w: 118, h: 64, g };
}

const CAPTIONS = {
  projectif: ['la face du dessous', 'les 3 carrés sur pointe au centre', 'les 6 faces : le cube fermé'],
  metrique: ['les 5 plaques B, tous les 2,5 cm', 'A0 et A1 : le cube entier', 'A2 à A4 : la soustraction'],
  topologique: ['le sol séparé, les deux côtés', 'le toit et la bande remontée', "l'arrière pivotée : la fente"],
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
    <div class="col axo"><figure>${img(D.axo)}<figcaption>Axonométrie ${id === 'topologique' ? 'éclatée (toit enlevé) ' : ''}30° / 60° · échelle 1:1 · cube de 10 cm d'arête · carton gris 2 mm</figcaption></figure></div>
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
