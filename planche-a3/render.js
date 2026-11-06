// Rend planche.html en PDF A3 (planche-a3.pdf) et en aperçu PNG (apercu.png).
// Lancer : NODE_PATH=$(npm root -g) node render.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1123, height: 1587 }, deviceScaleFactor: 1.4 });
  p.on('pageerror', e => console.log('erreur:', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'planche.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const mesure = await p.evaluate(() => {
    const page = document.querySelector('.page');
    const rows = [...document.querySelectorAll('.page > *')].map(e => [e.className || e.tagName, Math.round(e.getBoundingClientRect().height / 3.7795)]);
    return { page: [page.scrollWidth, page.scrollHeight, page.clientWidth, page.clientHeight], rows,
      polices: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family) };
  });
  console.log(JSON.stringify(mesure));
  await p.screenshot({ path: 'apercu.png', clip: { x: 0, y: 0, width: 1123, height: 1587 } });
  await p.pdf({ path: 'planche-a3.pdf', width: '297mm', height: '420mm', printBackground: true, pageRanges: '1' });
  await b.close();
})();
