// index.html -> aperçus (vue 3D, gabarits) + gabarits-1-1.pdf (taille réelle, A4)
// Lancer : NODE_PATH=$(npm root -g) node rendu.js <dossier des aperçus>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2] || __dirname;
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1.5 });
  // le CDN n'est pas joignable ici : on sert three.js 0.128.0 depuis une copie locale (THREE_LOCAL = dossier « package » du paquet npm)
  const local = process.env.THREE_LOCAL;
  if (local) await ctx.route('https://cdn.jsdelivr.net/npm/three@0.128.0/**', r => r.fulfill({ path: path.join(local, new URL(r.request().url()).pathname.replace('/npm/three@0.128.0/', '')), contentType: 'application/javascript' }));
  const p = await ctx.newPage();
  p.on('pageerror', e => console.log('erreur:', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  const url = 'file://' + path.resolve(__dirname, 'index.html');
  await p.goto(url); await p.waitForTimeout(2500);
  await p.screenshot({ path: path.join(out, 'apercu-page.png'), fullPage: true });
  await (await p.$('#scene')).screenshot({ path: path.join(out, 'apercu-3d.png') });
  for (const n of [2, 4, 7]) { await p.evaluate(n => allerEtape(n), n); await p.waitForTimeout(1200); await (await p.$('.atelier')).screenshot({ path: path.join(out, `apercu-etape-${n}.png`) }); }
  const q = await ctx.newPage();
  await q.goto(url + '#gabarit'); await q.waitForTimeout(800);
  await q.pdf({ path: path.resolve(__dirname, 'gabarits-1-1.pdf'), width: '210mm', height: '297mm', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await q.setViewportSize({ width: 794, height: 1123 }); await q.screenshot({ path: path.join(out, 'apercu-gabarit.png'), fullPage: true });
  await b.close();
})();
