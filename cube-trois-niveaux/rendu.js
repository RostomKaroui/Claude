// index.html -> aperçus + gabarits-taille-reelle.pdf (A4)
// Lancer : THREE_LOCAL=<dossier package de three@0.128.0> NODE_PATH=$(npm root -g) node rendu.js <dossier des aperçus>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2] || __dirname;
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const local = process.env.THREE_LOCAL;
  if (local) await ctx.route('https://cdn.jsdelivr.net/npm/three@0.128.0/**', r => r.fulfill({ path: path.join(local, new URL(r.request().url()).pathname.replace('/npm/three@0.128.0/', '')), contentType: 'application/javascript' }));
  const p = await ctx.newPage();
  p.on('pageerror', e => console.log('erreur:', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  const url = 'file://' + path.resolve(__dirname, 'index.html');
  for (const id of ['projectif', 'metrique', 'topologique']) {
    await p.goto(url + '#' + id); await p.waitForTimeout(1500);
    for (const n of [0, 2, 5]) { await p.evaluate(n => aller(n), n); await p.waitForTimeout(1300); await (await p.$(".atelier")).screenshot({ path: path.join(out, `${id}-${n + 1}.png`) }); }
    await (await p.$('#gabarits')).screenshot({ path: path.join(out, `${id}-gabarits.png`) });
  }
  await p.goto(url + '#projectif'); await p.waitForTimeout(1200); await p.screenshot({ path: path.join(out, 'page.png'), fullPage: false });
  const q = await ctx.newPage(); q.on('pageerror', e => console.log('erreur:', e.message));
  await q.goto(url + '#gabarits'); await q.waitForTimeout(800);
  await q.pdf({ path: path.resolve(__dirname, 'gabarits-taille-reelle.pdf'), width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true, scale: 1 });
  const m = await b.newPage({ viewport: { width: 390, height: 800 } }); await m.goto(url + '#metrique'); await m.waitForTimeout(800);
  console.log('mobile largeur', await m.evaluate(() => document.documentElement.scrollWidth));
  await b.close();
})();
