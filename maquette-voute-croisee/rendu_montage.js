// Ouvre montage.html dans Chromium, vérifie qu'il n'y a aucune erreur, compare la géométrie JS à celle de Python,
// et enregistre une image 3D de chaque étape (vue-etape-N.png, dans le dossier indiqué en 2e argument).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const dir = process.argv[2] || __dirname;
  const out = process.argv[3] || dir;
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1.5 });
  const erreurs = [];
  p.on('pageerror', e => erreurs.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') erreurs.push('console: ' + m.text()); });
  await p.goto('file://' + path.resolve(dir, 'montage.html'));
  await p.waitForFunction(() => window.__pret === true, null, { timeout: 15000 });
  // géométrie JS : quelques points, à comparer à voutain_3d (Python)
  const pts = await p.evaluate(() => [[0, 3, 4], [1, -2, 5.5], [2, 6.9, 4.5], [3, 0, 0], [0, 0, 6]].map(([k, s, w]) => webPoint(k, s, w, 1 / A)));
  console.log('JS_POINTS ' + JSON.stringify(pts));
  for (let i = 0; i <= 8; i++) {
    await p.evaluate(n => window.__aller(n, true), i);
    await p.waitForTimeout(450);
    await (await p.$('#scene')).screenshot({ path: path.resolve(out, `vue-etape-${i}.png`) });
  }
  await p.evaluate(() => window.__aller(5, true)); await p.waitForTimeout(300);
  await p.screenshot({ path: path.resolve(out, 'page-etape-5.png'), fullPage: false });
  console.log('ERREURS ' + JSON.stringify(erreurs));
  await b.close();
})();
