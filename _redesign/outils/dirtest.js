const { chromium } = require('playwright');
const axe = require('axe-core');
const fs = require('fs');
const MAIN = 'http://127.0.0.1:4101/', AP = 'http://127.0.0.1:4100';
const norm = s => s.replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim();
async function inventory(page) {
  return page.evaluate(() => {
    const n = s => s.replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim();
    const texts = [];
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) { const t = w.currentNode; const p = t.parentElement;
      if (!p || p.closest('script,style,noscript,[data-apercu]')) continue;
      const v = n(t.textContent); if (v && /[A-Za-zÀ-ÿ0-9]/.test(v)) texts.push(v); }
    const alts = [...document.querySelectorAll('img')].map(i => n(i.alt)).filter(Boolean);
    const links = [...document.querySelectorAll('a[href]')].filter(a => !a.closest('[data-apercu]')).map(a => a.getAttribute('href'));
    const q = s => { const e = document.querySelector(s); return e ? (e.content || e.href || e.textContent) : null; };
    const head = { title: document.title, description: q('meta[name=description]'), canonical: q('link[rel=canonical]'), og_title: q('meta[property="og:title"]'), og_image: q('meta[property="og:image"]'), robots: [...document.querySelectorAll('meta[name=robots]')].map(m => m.content).join(' | ') };
    const jsonld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent.replace(/\s+/g, ' ').trim());
    return { texts, alts, links, head, jsonld };
  });
}
const diff = (a, b) => [...new Set(a)].filter(x => !new Set(b).has(x));
(async () => {
  const b = await chromium.launch();
  const report = {};
  const ctx0 = await b.newContext(); const p0 = await ctx0.newPage();
  await p0.route(u => !u.href.startsWith(MAIN), r => r.abort());
  await p0.goto(MAIN, { waitUntil: 'load' });
  const main = await inventory(p0); await ctx0.close();
  for (const dir of ['a', 'b', 'c']) {
    const R = report[dir] = {};
    for (const [W, H] of [[390, 844], [1366, 768]]) {
      const ctx = await b.newContext({ viewport: { width: W, height: H } });
      const page = await ctx.newPage();
      const ext = [], errs = [], popups = [];
      page.on('pageerror', e => errs.push(String(e)));
      ctx.on('page', p => popups.push(p.url()));
      await page.route(u => !u.href.startsWith(AP), r => { const url = r.request().url(); if (!/fonts\.(googleapis|gstatic)|cdnjs\.cloudflare/.test(url)) ext.push(url.slice(0, 90)); r.abort(); });
      await page.addInitScript(() => { window.__opened = []; window.open = (u) => { window.__opened.push(u); return null; }; });
      await page.goto(`${AP}/apercu/${dir}/`, { waitUntil: 'load' });
      await page.evaluate(() => { const c = document.getElementById('mbCookie'); if (c) c.classList.remove('is-open'); });
      const r = R[W] = {};
      if (W === 1366) {
        const inv = await inventory(page);
        R.contenu = {
          textes_main_absents: diff(main.texts, inv.texts), textes_en_plus: diff(inv.texts, main.texts),
          alts_main_absents: diff(main.alts, inv.alts), alts_en_plus: diff(inv.alts, main.alts),
          liens_main_absents: diff(main.links, inv.links), liens_en_plus: diff(inv.links, main.links),
          head_differences: Object.fromEntries(Object.keys(main.head).filter(k => main.head[k] !== inv.head[k]).map(k => [k, [main.head[k], inv.head[k]]])),
          jsonld_identique: JSON.stringify(main.jsonld.map(j => j.replaceAll('/apercu/' + dir + '/', '/'))) === JSON.stringify(inv.jsonld.map(j => j.replaceAll('/apercu/' + dir + '/', '/'))),
          jsonld_brut_identique: JSON.stringify(main.jsonld) === JSON.stringify(inv.jsonld),
        };
      }
      r.premier_ecran = await page.evaluate(() => {
        const vis = e => { const b = e.getBoundingClientRect(), s = getComputedStyle(e); return b.width > 0 && b.height > 0 && b.top < innerHeight && b.bottom > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
        return { devis: [...document.querySelectorAll('[data-devis]')].filter(vis).map(e => e.textContent.trim()),
                 whatsapp: [...document.querySelectorAll('a[href*="wa.me"]')].filter(vis).map(e => e.textContent.trim() || e.getAttribute('aria-label')),
                 tel: [...document.querySelectorAll('a[href^="tel:"]')].filter(vis).length };
      });
      r.debordement = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      r.h1 = await page.locator('h1').count();
      r.sauts_titres = await page.evaluate(() => { let prev = 0, j = 0; document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => { const l = +h.tagName[1]; if (prev && l > prev + 1) j++; prev = l; }); return j; });
      r.cibles_lt24 = await page.evaluate(() => [...document.querySelectorAll('a,button,input,textarea')].filter(e => { const b = e.getBoundingClientRect(); const inline = e.tagName === 'A' && getComputedStyle(e).display === 'inline' && e.closest('p,li'); return b.width && (b.height < 24 || b.width < 24) && !inline && !e.classList.contains('skip'); }).map(e => (e.textContent.trim() || e.getAttribute('aria-label') || e.tagName).slice(0, 30)));
      if (W === 390) {
        await page.click('#menuBtn');
        const opened = await page.evaluate(() => !document.getElementById('mobileMenu').hidden && document.getElementById('menuBtn').getAttribute('aria-expanded'));
        await page.keyboard.press('Escape');
        const closed = await page.evaluate(() => document.getElementById('mobileMenu').hidden);
        r.menu = { ouvert: opened, ferme_par_echap: closed };
      }
      // formulaire
      await page.locator('[data-devis]:visible').first().click();
      await page.waitForTimeout(600);
      r.focus_apres_devis = await page.evaluate(() => document.activeElement && document.activeElement.id);
      await page.click('#leadForm .form-submit');
      r.vide_invalides = await page.evaluate(() => [...document.querySelectorAll('#leadForm [aria-invalid=true]')].map(e => e.id));
      await page.fill('#nom', 'Test Synthétique'); await page.fill('#tel', '0600000000'); await page.fill('#email', 'test@example.invalid'); await page.fill('#projet', 'Essai automatique sans envoi');
      await page.click('#leadForm .form-submit');
      await page.waitForTimeout(500);
      r.statut = await page.textContent('#leadForm .form-status');
      r.window_open = await page.evaluate(() => window.__opened);
      r.requetes_externes_bloquees = ext; r.popups = popups; r.erreurs_js = errs;
      if (W === 390) { await page.keyboard.press('Escape'); }
      await page.evaluate(() => { const m = document.getElementById('devisModal'); if (m) m.hidden = true; document.body.classList.remove('no-scroll'); });
      await page.addScriptTag({ content: axe.source });
      const ax = await page.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa'] })).violations.map(v => `${v.id} (${v.nodes.length}) ${v.nodes.map(n => n.target.join(" ")).slice(0,3).join(" ; ")}`));
      r.axe = ax;
      await ctx.close();
    }
  }
  fs.writeFileSync('/home/ubuntu/audit/directions-tests.json', JSON.stringify({ main_counts: { texts: main.texts.length, alts: main.alts.length, links: main.links.length }, report }, null, 1));
  console.log(JSON.stringify(report, null, 1).slice(0, 9000));
  await b.close();
})();
