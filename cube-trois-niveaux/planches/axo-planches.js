// Dessins des planches A3 : axonométries 30°/60° et faces du cube, en traits (parties cachées enlevées).
// S'exécute dans index.html (qui définit MAQUETTES et THREE). Chaque face reçoit un numéro de plan ;
// un trait est dessiné là où le numéro change (contour fort contre le vide, arêtes fines ailleurs).
window.PLANCHES = (function () {
  const rad = d => d * Math.PI / 180;

  // ---------------------------------------------------------------- triangles + numéros de surface
  function collecter(M, garder) {
    const pos = [], ids = [];
    let nId = 1; const plans = new Map();
    const idPlan = (n, a) => { const k = n.map(v => Math.round(v * 1000)).join(",") + "|" + Math.round(a * 200); if (!plans.has(k)) plans.set(k, nId++); return plans.get(k); };
    const tri = (a, b, c, id) => { pos.push(a, b, c); ids.push(id); };
    function planDe(a, b, c) {
      const u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
      let n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
      const l = Math.hypot(...n) || 1; n = n.map(x => x / l);
      if (n[0] < -1e-9 || (Math.abs(n[0]) < 1e-9 && (n[1] < -1e-9 || (Math.abs(n[1]) < 1e-9 && n[2] < 0)))) n = n.map(x => -x);
      return [n, n[0] * a[0] + n[1] * a[1] + n[2] * a[2]];
    }
    const plat = (a, b, c) => { const [n, d] = planDe(a, b, c); return idPlan(n, d); };
    const A = {
      plaque(id, contour, trous, o, du, dv, dn, t) {
        if (!garder(id)) return;
        const W = (u, v, w) => [o[0] + u * du[0] + v * dv[0] + w * dn[0], o[1] + u * du[1] + v * dv[1] + w * dn[1], o[2] + u * du[2] + v * dv[2] + w * dn[2]];
        const v2 = l => l.map(([u, v]) => new THREE.Vector2(u, v));
        const faces = THREE.ShapeUtils.triangulateShape(v2(contour), trous.map(v2)), tous = contour.concat(...trous);
        for (const w of [0, t]) for (const f of faces) { const [a, b, c] = f.map(i => W(tous[i][0], tous[i][1], w)); tri(a, b, c, plat(a, b, c)); }
        for (const poly of [contour, ...trous]) {           // côtés : les segments presque alignés forment une seule surface (trou rond)
          const n = poly.length, dir = i => { const a = poly[i], b = poly[(i + 1) % n]; return Math.atan2(b[1] - a[1], b[0] - a[0]); };
          const lisse = i => { let d = Math.abs(dir(i) - dir((i + n - 1) % n)); d = Math.min(d, 2 * Math.PI - d); return d < rad(25); };
          let chaine = 0;
          for (let i = 0; i < n; i++) {
            const a = poly[i], b = poly[(i + 1) % n]; if (Math.hypot(b[0] - a[0], b[1] - a[1]) < 1e-6) continue;
            const q = [W(a[0], a[1], 0), W(b[0], b[1], 0), W(b[0], b[1], t), W(a[0], a[1], t)];
            let idc; if (lisse(i) || lisse((i + 1) % n)) { if (!lisse(i) || !chaine) chaine = nId++; idc = chaine; } else { chaine = 0; idc = plat(q[0], q[1], q[2]); }
            tri(q[0], q[1], q[2], idc); tri(q[0], q[2], q[3], idc);
          }
        }
      },
      boite(id, x, y, z, sx, sy, sz) {
        if (!garder(id)) return;
        const P = (i, j, k) => [x + i * sx, y + j * sy, z + k * sz];
        for (const f of [[[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], [[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]],
          [[0, 1, 0], [1, 1, 0], [1, 1, 1], [0, 1, 1]], [[0, 0, 0], [0, 1, 0], [0, 1, 1], [0, 0, 1]], [[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 0, 1]]]) {
          const q = f.map(p => P(...p)), idf = plat(q[0], q[1], q[2]); tri(q[0], q[1], q[2], idf); tri(q[0], q[2], q[3], idf);
        }
      },
      cylindre(id, x, y, z0, z1, r) {
        if (!garder(id)) return;
        const n = 24, flanc = nId++, pts = Array.from({ length: n }, (_, i) => [x + r * Math.cos(2 * Math.PI * i / n), y + r * Math.sin(2 * Math.PI * i / n)]);
        for (let i = 0; i < n; i++) { const a = pts[i], b = pts[(i + 1) % n];
          tri([a[0], a[1], z0], [b[0], b[1], z0], [b[0], b[1], z1], flanc); tri([a[0], a[1], z0], [b[0], b[1], z1], [a[0], a[1], z1], flanc);
          for (const z of [z0, z1]) { const c = [x, y, z], p = [a[0], a[1], z], q = [b[0], b[1], z]; tri(c, p, q, plat(c, p, q)); } }
      },
    };
    M.construire(A);
    return { pos, ids };
  }

  // ---------------------------------------------------------------- vues : axonométrie 30°/60° et faces (u, v, profondeur)
    function axo(C, e1, e2, gauche = 30) {   // C : coin le plus bas ; e1 part à gauche (30° ou 60°), e2 à droite (l'angle complémentaire)
    const cg = Math.cos(rad(gauche)), sg = Math.sin(rad(gauche)), cd = Math.cos(rad(90 - gauche)), sd = Math.sin(rad(90 - gauche));
    return p => { const dx = p[0] - C[0], dy = p[1] - C[1], a = dx * e1[0] + dy * e1[1], b = dx * e2[0] + dy * e2[1], vp = sg * a + sd * b;
      return [-cg * a + cd * b, vp + p[2], vp - p[2]]; };
  }
  const VUES = {
    dessus: p => [p[0], p[1], -p[2]], dessous: p => [p[0], -p[1], p[2]],
    devant: p => [p[0], p[2], p[1]], arriere: p => [-p[0], p[2], -p[1]],
    droite: p => [p[1], p[2], -p[0]], gauche: p => [-p[1], p[2], p[0]],
  };

  // ---------------------------------------------------------------- rendu (numéros) -> traits
  let renderer = null;
  function dessiner(geo, proj, k, epFort, epFin, cadre) {
    // k : mm sur la feuille par cm de maquette ; rendu à 12 pixels par mm
    const PX = 12, { pos, ids } = geo, P = pos.map(proj);
    let [u0, u1, v0, v1] = cadre || [1e9, -1e9, 1e9, -1e9];
    if (!cadre) for (const [u, v] of P) { u0 = Math.min(u0, u); u1 = Math.max(u1, u); v0 = Math.min(v0, v); v1 = Math.max(v1, v); }
    const marge = 0.25; u0 -= marge; u1 += marge; v0 -= marge; v1 += marge;
    const Wmm = (u1 - u0) * k, Hmm = (v1 - v0) * k, W = Math.ceil(Wmm * PX), H = Math.ceil(Hmm * PX);
    let dmin = 1e9, dmax = -1e9; for (const p of P) { dmin = Math.min(dmin, p[2]); dmax = Math.max(dmax, p[2]); }
    const xyz = new Float32Array(P.length * 3), col = new Float32Array(P.length * 3);
    P.forEach((p, i) => { xyz[3 * i] = (p[0] - u0) / (u1 - u0) * 2 - 1; xyz[3 * i + 1] = (p[1] - v0) / (v1 - v0) * 2 - 1; xyz[3 * i + 2] = ((p[2] - dmin) / (dmax - dmin + 1e-9)) * 1.8 - 0.9;
      const id = ids[Math.floor(i / 3)]; col[3 * i] = (id & 255) / 255; col[3 * i + 1] = ((id >> 8) & 255) / 255; col[3 * i + 2] = ((id >> 16) & 255) / 255; });
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(xyz, 3)); g.setAttribute("couleur", new THREE.BufferAttribute(col, 3));
    const mat = new THREE.ShaderMaterial({ side: THREE.DoubleSide, vertexShader: "attribute vec3 couleur; varying vec3 c; void main(){ c = couleur; gl_Position = vec4(position, 1.0); }", fragmentShader: "varying vec3 c; void main(){ gl_FragColor = vec4(c, 1.0); }" });
    const scene = new THREE.Scene(); scene.add(new THREE.Mesh(g, mat)); scene.background = new THREE.Color(0, 0, 0);
    if (!renderer) renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
    const cible = new THREE.WebGLRenderTarget(W, H, { minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
    renderer.setRenderTarget(cible); renderer.render(scene, new THREE.Camera());
    const buf = new Uint8Array(W * H * 4); renderer.readRenderTargetPixels(cible, 0, 0, W, H, buf); renderer.setRenderTarget(null); cible.dispose(); g.dispose(); mat.dispose();
    const idA = (x, y) => { const q = (y * W + x) * 4; return buf[q] | (buf[q + 1] << 8) | (buf[q + 2] << 16); };
    const fort = new Uint8Array(W * H), fin = new Uint8Array(W * H);
    for (let y = 0; y < H - 1; y++) for (let x = 0; x < W - 1; x++) { const a = idA(x, y);
      for (const b of [idA(x + 1, y), idA(x, y + 1)]) if (b !== a) ((a === 0 || b === 0) ? fort : fin)[y * W + x] = 1; }
    // enlève les points isolés (faces confondues qui se disputent le même pixel)
    for (const m of [fort, fin]) { const garde = new Uint8Array(W * H);
      for (let y = 2; y < H - 2; y++) for (let x = 2; x < W - 2; x++) if (m[y * W + x]) { let n = 0;
        for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) n += m[(y + dy) * W + x + dx];
        if (n >= 4) garde[y * W + x] = 1; }
      m.set(garde); }
    const cv = document.createElement("canvas"); cv.width = W; cv.height = H; const c2 = cv.getContext("2d");
    const img = c2.createImageData(W, H); for (let i = 0; i < W * H; i++) { img.data[4 * i + 3] = 0; }
    const peindre = (m, r) => { const off = []; for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) if (dx * dx + dy * dy <= r * r + 0.5) off.push([dx, dy]);
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (m[y * W + x]) for (const [dx, dy] of off) { const X = x + dx, Y = H - 1 - (y + dy);
        if (X >= 0 && X < W && Y >= 0 && Y < H) { const q = (Y * W + X) * 4; img.data[q] = img.data[q + 1] = img.data[q + 2] = 22; img.data[q + 3] = 255; } } };
    peindre(fin, Math.max(1, Math.round(epFin * PX / 2))); peindre(fort, Math.max(1, Math.round(epFort * PX / 2)));
    c2.putImageData(img, 0, 0);
    return { url: cv.toDataURL("image/png"), w: Wmm, h: Hmm };
  }

  // ---------------------------------------------------------------- ce que chaque planche montre
  const VUE_AXO = {
    projectif: axo([10, 0], [-1, 0], [0, 1]),
    metrique: axo([10, 10], [0, -1], [-1, 0]),
    topologique: axo([10, 0], [-1, 0], [0, 1]),        // vu de l'avant droit : l'ouverture à droite et le panneau pivoté
  };
  const ETAPES = {
    projectif: [["socle", "pique"], ["socle", "pique", "poteaux", "c0", "c1"], ["socle", "pique", "poteaux", "c0", "c1", "c2", "c3"]],
    metrique: [["B0", "B1", "B2", "B3", "B4"], ["B0", "B1", "B2", "B3", "B4", "A0", "A1"], null],
    topologique: [["sol", "gauche"], ["sol", "gauche", "arriere", "toit"], null],
  };
  function planche(id) {
    const M = MAQUETTES[id], tout = () => true, geo = collecter(M, tout);
    const out = { axo: dessiner(geo, VUE_AXO[id], 10, 0.55, 0.25), faces: {}, etapes: [] };
    for (const [nom, f] of Object.entries(VUES)) out.faces[nom] = dessiner(geo, f, 5, 0.4, 0.18, null);
    // cadre commun pour les vignettes : celui de la maquette entière
    const P = geo.pos.map(VUE_AXO[id]); let c = [1e9, -1e9, 1e9, -1e9];
    for (const [u, v] of P) { c = [Math.min(c[0], u), Math.max(c[1], u), Math.min(c[2], v), Math.max(c[3], v)]; }
    for (const ids of ETAPES[id]) { const g = ids ? collecter(M, k => ids.includes(k)) : geo; out.etapes.push(dessiner(g, VUE_AXO[id], 2.5, 0.35, 0.15, c)); }
    return out;
  }
  return { planche };
})();
