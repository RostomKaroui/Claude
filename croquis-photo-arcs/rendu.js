// Rend construction.html en PNG (taille réelle) et PDF.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = process.argv[2] || __dirname;
  const b = await chromium.launch();
  for (const f of ['construction']) {
    const p = await b.newPage({ viewport: { width: 800, height: 800 }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.resolve(dir, f + '.html'));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    const svg = await p.$('svg');
    await svg.screenshot({ path: path.resolve(dir, f + '.png') });
    const box = await svg.boundingBox();
    await p.pdf({ path: path.resolve(dir, f + '.pdf'), width: box.width + 'px', height: box.height + 'px', printBackground: true, pageRanges: '1' });
  }
  await b.close();
})();
