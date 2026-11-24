// axo.html -> axonometrie-pavillon.pdf (A4, taille réelle) + apercu.png
// Lancer : NODE_PATH=$(npm root -g) node rendu.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  p.on('pageerror', e => console.log('erreur:', e.message)); p.on('console', m => console.log('console:', m.text()));
  await p.goto('file://' + path.resolve(__dirname, 'axo.html'));
  await p.waitForFunction(() => window.PRET, null, { timeout: 120000 });
  console.log(JSON.stringify(await p.evaluate(() => window.PRET)));
  await p.waitForTimeout(500);
  await p.pdf({ path: path.resolve(__dirname, 'axonometrie-pavillon.pdf'), width: '210mm', height: '297mm', printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 }, preferCSSPageSize: true, scale: 1 });
  await p.screenshot({ path: path.resolve(__dirname, 'apercu.png'), fullPage: true });
  await b.close();
})();
