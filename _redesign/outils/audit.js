// Audit navigateur : JS, débordement, zones tactiles, axe, CTA 1er écran, formulaire intercepté (aucun envoi réel)
const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;
const base = process.argv[2] || 'http://127.0.0.1:4001';
const pages = (process.argv[3] || '/,/services/plomberie/,/renovation/versailles/,/realisations/,/blog/').split(',');
(async () => {
  const browser = await chromium.launch();
  const out = {};
  for (const p of pages) for (const [w, h] of [[390, 844], [1366, 768]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    const page = await ctx.newPage();
    const errors = []; const external = [];
    page.on('pageerror', e => errors.push(String(e).slice(0, 120)));
    // Tout trafic externe bloqué : n8n, WhatsApp, trackers, CDN (mesure du code du site seul)
    await page.route(u => !u.href.startsWith(base), r => { external.push(r.request().url().slice(0, 80)); r.abort(); });
    await page.goto(base + p, { waitUntil: 'load' }); await page.waitForTimeout(1500);
    const r = await page.evaluate(() => {
      const vis = e => { const b = e.getBoundingClientRect(); const s = getComputedStyle(e); return b.width > 0 && b.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0'; };
      const overflow = document.documentElement.scrollWidth > innerWidth + 1;
      const small = [...document.querySelectorAll('a,button,input,textarea')].filter(vis).filter(e => { const b = e.getBoundingClientRect(); return (b.height < 24 || b.width < 24) && getComputedStyle(e).display !== 'inline'; }).length;
      const inFold = e => { const b = e.getBoundingClientRect(); return vis(e) && b.top < innerHeight && b.bottom > 0; };
      const ctas = [...document.querySelectorAll('a,button')].filter(inFold).map(e => (e.innerText || e.getAttribute('aria-label') || '').trim());
      const devis = ctas.some(t => /devis|étude de projet/i.test(t)); const wa = [...document.querySelectorAll('a[href*="wa.me"]')].some(inFold);
      const heads = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e => +e.tagName[1]); let jumps = 0; for (let i = 1; i < heads.length; i++) if (heads[i] - heads[i - 1] > 1) jumps++;
      return { overflow, small, devisFold: devis, waFold: wa, h1: document.querySelectorAll('h1').length, headingJumps: jumps };
    });
    let axe = null;
    try { const a = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze(); axe = a.violations.map(v => `${v.id}(${v.nodes.length})`); } catch (e) { axe = ['axe err ' + String(e).slice(0, 60)]; }
    out[`${p} @${w}`] = { ...r, jsErrors: errors, axe, externalBlocked: external.length };
    await ctx.close();
  }
  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})();
