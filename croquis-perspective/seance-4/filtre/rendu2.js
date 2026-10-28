// croquis-filtre-2-construction.html -> croquis-filtre-2-construction.png (1500 x 2000, comme la photo)
// Lancer : NODE_PATH=$(npm root -g) node rendu2.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1500, height: 2000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(__dirname, 'croquis-filtre-2-construction.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await (await p.$('.cadre')).screenshot({ path: path.resolve(__dirname, 'croquis-filtre-2-construction.png') });
  await b.close();
})();
