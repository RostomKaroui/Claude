// croquis-jaune.html -> croquis-jaune-A4.pdf + apercu-jaune.png ; avec calque-jaune.html présent, aussi les captures du calque
// Lancer : NODE_PATH=$(npm root -g) node rendu.js [dossier des captures de calque]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(__dirname, 'croquis-jaune.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.pdf({ path: path.resolve(__dirname, 'croquis-jaune-A4.pdf'), width: '210mm', height: '297mm', printBackground: true });
  await (await p.$('.p')).screenshot({ path: path.resolve(__dirname, 'apercu-jaune.png') });
  const calque = path.resolve(__dirname, 'calque-jaune.html');
  if (fs.existsSync(calque) && process.argv[2]) {
    const q = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2.5 });
    await q.goto('file://' + calque); await q.waitForTimeout(300);
    const mm = 794 / 210;
    for (const [i, y0] of [[1, 30], [2, 150]])
      await q.screenshot({ path: path.join(process.argv[2], `calque-jaune-${i}.png`), clip: { x: 15 * mm, y: y0 * mm, width: 180 * mm, height: 120 * mm } });
  }
  await b.close();
})();
