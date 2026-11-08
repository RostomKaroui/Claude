// Rend a3.html (A3 paysage) et a4x2.html (2 A4 portrait) en PDF + aperçus PNG.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = process.argv[2] || __dirname;
  const b = await chromium.launch();
  for (const [f, w, h, out, ap] of [['a3', 420, 297, 'croquis-A3', 'apercu-A3'], ['a4x2', 210, 297, 'croquis-2xA4', 'apercu-A4']]) {
    const p = await b.newPage({ viewport: { width: Math.round(w * 3.78), height: Math.round(h * 3.78) }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.resolve(dir, f + '.html'));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
    await p.pdf({ path: path.resolve(dir, out + '.pdf'), width: w + 'mm', height: h + 'mm', printBackground: true });
    const pages = await p.$$('.p');
    for (let i = 0; i < pages.length; i++)
      await pages[i].screenshot({ path: path.resolve(dir, pages.length > 1 ? `${ap}-${i + 1}.png` : `${ap}.png`) });
  }
  await b.close();
})();
