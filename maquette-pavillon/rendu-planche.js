// index.html#planche -> planche-a4.pdf (toutes les pièces sur une feuille A4, taille réelle) + aperçu PNG
// Lancer : NODE_PATH=$(npm root -g) node rendu-planche.js <dossier de l'aperçu>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2] || __dirname;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  p.on('pageerror', e => console.log('erreur:', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'index.html') + '#planche'); await p.waitForTimeout(800);
  await p.pdf({ path: path.resolve(__dirname, 'planche-a4.pdf'), width: '210mm', height: '297mm', printBackground: true, pageRanges: '1', margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await p.screenshot({ path: path.join(out, 'apercu-planche.png'), clip: { x: 0, y: 0, width: 794, height: 1123 } });
  await b.close();
})();
