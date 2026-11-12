// Rend croquis.html (A4) et croquis-a3.html (A3) en PDF, et un aperçu PNG de chaque page A4.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  for (const [f, w, h] of [['croquis', 210, 297], ['croquis-a3', 297, 420]]) {
    const p = await b.newPage({ viewport: { width: Math.round(w * 3.78), height: Math.round(h * 3.78) }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.resolve(dir, f + '.html'));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    console.log(f, 'polices', JSON.stringify(await p.evaluate(() => [...document.fonts].filter(x => x.status === 'loaded').map(x => x.family))));
    await p.pdf({ path: path.resolve(dir, f + '.pdf'), width: w + 'mm', height: h + 'mm', printBackground: true });
    if (f === 'croquis') {
      const pages = await p.$$('.p');
      for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.resolve(dir, `apercu-${i + 1}.png`) });
    }
  }
  await b.close();
})();
