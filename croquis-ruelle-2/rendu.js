// Rend croquis-A3.html (A3 portrait) et croquis-2xA4.html (2 A4 paysage) en PDF, avec un aperçu PNG de chaque page.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = process.argv[2] || __dirname;
  const b = await chromium.launch();
  for (const [f, w, h, apercu] of [['croquis-A3', 297, 420, 'apercu-A3'], ['croquis-2xA4', 297, 210, 'apercu-A4']]) {
    const p = await b.newPage({ viewport: { width: Math.round(w * 3.78), height: Math.round(h * 3.78) }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.resolve(dir, f + '.html'));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.pdf({ path: path.resolve(dir, f + '.pdf'), width: w + 'mm', height: h + 'mm', printBackground: true });
    const pages = await p.$$('.p');
    for (let i = 0; i < pages.length; i++)
      await pages[i].screenshot({ path: path.resolve(dir, pages.length > 1 ? `${apercu}-${i + 1}.png` : `${apercu}.png`) });
  }
  await b.close();
})();
