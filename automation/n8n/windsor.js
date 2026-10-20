// Read-only analytics boundary embedded unchanged in W5/W8/W10. No HTTP or publishing.
function windsorAnalytics(queue, timestamp) {
  const now = new Date(timestamp), today = now.toISOString().slice(0,10);
  const names = ['search_console','ga4','gbp','google_ads','meta_ads','instagram'];
  const metrics = {
    search_console:['clicks','impressions','position'], ga4:['sessions','users','key_events'],
    gbp:['impressions','website_clicks','calls','directions'], google_ads:['impressions','clicks','cost','conversions'],
    meta_ads:['impressions','clicks','cost','conversions'], instagram:['reach','impressions','engagements','profile_views'],
  };
  const website = value => {
    const s = String(value || '');
    if (!/^https:\/\/(?:www\.)?maison-mb\.fr(?:\/[^\s]*)?$/.test(s)) return null;
    return s.replace(/^https:\/\/(?:www\.)?maison-mb\.fr/, 'https://www.maison-mb.fr').split(/[?#]/)[0].replace(/\/$/, '') + (s.replace(/^https:\/\/(?:www\.)?maison-mb\.fr/, '').split(/[?#]/)[0].replace(/\/$/, '') ? '' : '/');
  };
  const numeric = value => typeof value === 'number' && Number.isFinite(value) && value >= 0;
  const secret = /(?:api[_-]?key|access[_-]?token|bearer\s|sk-(?:proj|ant)-|[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,})/i;
  const result = Object.fromEntries(names.map(channel => [channel,{channel,status:'missing',reason:'No validated Windsor snapshot in Growth Queue'}]));
  for (const row of queue) {
    if (row.type !== 'analytics_snapshot' || row.source !== 'Windsor.ai' || row.status !== 'done') continue;
    let p; try { p = JSON.parse(row.payload); } catch { continue; }
    if (!names.includes(p.channel)) continue;
    const candidate = {channel:p.channel,status:'invalid',reason:'Invalid analytics contract'};
    const date = x => { if (typeof x !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(x)) return false; const d = new Date(x+'T00:00:00Z'); return Number.isFinite(d.getTime()) && d.toISOString().slice(0,10) === x; };
    const captured = Date.parse(p.captured_at);
    const valid = p.schema === 'mb.windsor.v1' && typeof p.account === 'string' && p.account.length > 0 && p.account.length <= 120 && !secret.test(p.account)
      && Number.isFinite(captured) && captured <= now.getTime() && date(p.period_start) && date(p.period_end)
      && p.period_start <= p.period_end && p.period_end <= today && p.metrics && !Array.isArray(p.metrics)
      && Object.keys(p.metrics).length > 0 && Object.entries(p.metrics).every(([k,v]) => metrics[p.channel].includes(k) && numeric(v))
      && (!('cost' in p.metrics) || /^[A-Z]{3}$/.test(p.currency || ''));
    if (valid) {
      candidate.status = now.getTime()-captured <= 72*3600000 && now-new Date(p.period_end+'T00:00:00Z') <= 8*86400000 ? 'available' : 'stale';
      candidate.reason = candidate.status === 'available' ? '' : 'Snapshot older than freshness window';
      Object.assign(candidate,{account:p.account,captured_at:p.captured_at,period_start:p.period_start,period_end:p.period_end,metrics:p.metrics,currency:p.currency || null});
      candidate.pages = (Array.isArray(p.pages) ? p.pages : []).slice(0,100).filter(x => website(x.url) && ['clicks','impressions','position','sessions','key_events'].every(k => x[k] === undefined || numeric(x[k])))
        .map(x => ({url:website(x.url),...Object.fromEntries(['clicks','impressions','position','sessions','key_events'].filter(k => x[k] !== undefined).map(k => [k,x[k]]))}));
      candidate.posts = (Array.isArray(p.posts) ? p.posts : []).slice(0,30).filter(x => typeof x.title === 'string' && !secret.test(x.title) && ['reach','impressions','engagements','clicks'].every(k => x[k] === undefined || numeric(x[k])))
        .map(x => ({title:x.title.replace(/[<>\r\n]/g,' ').slice(0,160),...Object.fromEntries(['reach','impressions','engagements','clicks'].filter(k => x[k] !== undefined).map(k => [k,x[k]]))}));
    }
    const current = result[p.channel];
    // Invalid or newer empty rows never conceal a previously valid sample. Never sum overlapping periods/accounts.
    if ((valid && (!current.captured_at || captured > Date.parse(current.captured_at))) || (current.status === 'missing' && !valid)) result[p.channel] = candidate;
  }
  return result;
}

function windsorContext(queue, timestamp, channels) {
  const all = windsorAnalytics(queue,timestamp);
  return channels.map(channel => {
    const p = all[channel];
    if (p.status !== 'available') return {channel,status:p.status,reason:p.reason};
    return {channel,status:p.status,period_start:p.period_start,period_end:p.period_end,captured_at:p.captured_at,metrics:p.metrics,currency:p.currency,
      pages:p.pages.slice().sort((a,b)=>(b.impressions || b.sessions || 0)-(a.impressions || a.sessions || 0)).slice(0,8),
      posts:p.posts.slice().sort((a,b)=>(b.engagements || b.reach || 0)-(a.engagements || a.reach || 0)).slice(0,5)};
  });
}
