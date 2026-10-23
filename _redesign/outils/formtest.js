// Formulaire devis : validation + envoi intercepté avec données synthétiques. Aucune requête ne quitte la machine.
const { chromium } = require('playwright');
const base = process.argv[2] || 'http://127.0.0.1:4001';
const path = process.argv[3] || '/';
const openSel = process.argv[4] || 'button.nav-btn';
(async () => {
  const browser = await chromium.launch();
  const res = {};
  for (const [w, h] of [[390, 844], [1366, 768]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    const captured = { webhook: [], whatsapp: [], otherExternal: 0 };
    await ctx.route(u => !u.href.startsWith(base), r => {
      const url = r.request().url();
      if (url.includes('hostingersite.com')) captured.webhook.push({ method: r.request().method(), body: r.request().postData() });
      else if (url.includes('wa.me') || url.includes('whatsapp')) captured.whatsapp.push(decodeURIComponent(url).slice(0, 300));
      else captured.otherExternal++;
      r.abort();
    });
    const page = await ctx.newPage();
    ctx.on('page', p => { captured.whatsapp.push('popup:' + decodeURIComponent(p.url()).slice(0, 300)); });
    await page.goto(base + path, { waitUntil: 'load' }); await page.waitForTimeout(1500);
    if (w < 800 && await page.locator('#hamburger, .hamburger, [data-menu-toggle]').first().isVisible().catch(() => false)) {
      await page.locator('#hamburger, .hamburger, [data-menu-toggle]').first().click(); await page.waitForTimeout(400);
      res[`menu@${w}`] = await page.evaluate(() => [...document.querySelectorAll('a,button')].filter(e => { const b = e.getBoundingClientRect(); return b.width && b.height && b.top >= 0 && b.top < innerHeight && getComputedStyle(e).visibility !== 'hidden'; }).map(e => e.innerText.trim()).filter(Boolean).slice(0, 14));
      await page.keyboard.press('Escape'); await page.locator('#hamburger, .hamburger, [data-menu-toggle]').first().click().catch(() => {}); await page.waitForTimeout(300);
    }
    const opener = page.locator(openSel).filter({ visible: true }).first();
    await opener.click(); await page.waitForTimeout(500);
    const form = page.locator('form').filter({ visible: true }).first();
    const labels = await form.evaluate(f => [...f.querySelectorAll('input,textarea')].map(i => ({ id: i.id, required: i.required, label: (f.querySelector(`label[for="${i.id}"]`) || {}).innerText || null })));
    await form.locator('[type=submit]').click();
    const invalid = await form.evaluate(f => [...f.querySelectorAll(':invalid')].map(i => i.id));
    await page.fill('#nom', 'Test Synthétique'); await page.fill('#tel', '0600000000'); await page.fill('#email', 'test@example.invalid'); await page.fill('#projet', 'Essai automatique sans envoi');
    await form.locator('[type=submit]').click(); await page.waitForTimeout(1500);
    res[`form@${w}`] = { labels, invalidOnEmptySubmit: invalid, captured };
    await ctx.close();
  }
  console.log(JSON.stringify(res, null, 1));
  await browser.close();
})();
