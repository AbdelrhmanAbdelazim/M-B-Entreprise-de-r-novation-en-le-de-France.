import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import vm from 'node:vm';
import { execFileSync } from 'node:child_process';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const baseline = process.env.N8N_TEST_BASELINE === '1';
const doc = name => {
  const d = baseline ? JSON.parse(execFileSync('git', ['show', '883e99b9a859fef687f5ffe997e999328c43e384:automation/n8n/' + name + '.json'], { cwd: join(root, '..', '..'), encoding: 'utf8' })) : JSON.parse(readFileSync(join(root, name + '.json')));
  if (!baseline) {
    const p = JSON.parse(readFileSync(join(root, 'pending', name + '.patch.json')));
    if (d.versionId === p.base_version_id) {
      for (const change of p.node_changes) Object.assign(d.nodes.find(n => n.id === change.node_id).parameters, change.parameters);
      for (const n of p.add_nodes || []) d.nodes.push(n);
    } else {
      for (const change of p.node_changes) assert.equal(d.nodes.find(n => n.id === change.node_id).parameters.jsCode, change.parameters.jsCode, 'Published code drift requires a new review');
    }
  }
  return d;
};
const item = json => ({ json });
const fixed = new Date('2026-10-19T08:00:00Z');
class Clock extends Date { constructor(...args) { super(...(args.length ? args : [fixed.getTime()])); } static now() { return fixed.getTime(); } }
function run(name, nodeName, rows = {}, input = []) {
  const code = doc(name).nodes.find(n => n.name === nodeName).parameters.jsCode;
  const sandbox = { Date: Clock, $runIndex: 0, $execution: { id: 'synthetic-execution' }, $json: input[0] || {},
    $input: { all: () => input.map(item), first: () => item(input[0] || {}) },
    $: name => { if (!(name in rows)) throw new Error('Unavailable fixture node: ' + name); const values = rows[name].map(item); return { all: () => values, first: () => values[0], item: values[0] }; },
  };
  return vm.runInNewContext(`(() => {${code}\n})()`, sandbox, { timeout: 1000 });
}
const lead = { id: 41, email: 'contact@synthetic.invalid', site: 'synthetic.invalid', statut: 'nouveau' };
const approval = { task_key: 'prospect:synthetic.invalid', status: 'approved', priority: 'WARM' };
function guard(name, queue, override = {}) {
  const current = { ...lead, ...(name === 'W4' ? { statut: 'envoye', date_envoi: '2026-10-01' } : {}), ...override };
  return run(name, 'Garde commerciale', { 'Un par un': [current], 'Avant envoi – Leads': [current], 'Avant envoi – Blacklist': [] }, queue)[0].json;
}
function search(responses) { return run('W7', 'URLs', { Leads: [], Blacklist: [], 'Requêtes': [{ type: 'syndic', departement: '75' }, { type: 'agence', departement: '92' }] }, responses); }
test('W7 search transport failure must reach W0 instead of closing an empty successful cycle', () => {
  assert.throws(() => search([{ error: { message: 'synthetic timeout' } }, { error: 'synthetic timeout' }]), /W7_SEARCH_SOURCE_FAILED/);
});
test('W7 rejects HTTP errors and malformed successful response shapes', () => {
  for (const response of [{ statusCode: 429, body: { data: [] } }, { statusCode: 200, body: { error: 'quota' } }, { statusCode: 200, body: {} }])
    assert.throws(() => search([response, { body: { data: [] } }]), /W7_SEARCH_SOURCE_FAILED/);
});
test('W7 does not silently accept a missing query response or a partially failed batch', () => {
  assert.throws(() => search([{ body: { data: [] } }]), /W7_SEARCH_SOURCE_FAILED/);
  assert.throws(() => search([{ body: { data: [{ url: 'https://synthetic.invalid/' }] } }, { error: 'timeout' }]), /W7_SEARCH_SOURCE_FAILED/);
});
test('W7 genuine empty search responses stay a legitimate empty cycle', () => {
  assert.equal(search([{ body: { data: [] } }, { body: { data: [] } }]).length, 0);
});
test('W3 must reject unknown or missing grade even when approved', () => {
  for (const priority of ['', 'INVALID', undefined]) assert.equal(guard('W3', [{ ...approval, priority }]).allowed, false);
});
test('W3 conflicting duplicate approvals must fail closed', () => {
  assert.equal(guard('W3', [approval, { ...approval, status: 'rejected' }]).allowed, false);
});
test('W3 must block previous ambiguous delivery matched by recipient even under a different company key', () => {
  assert.equal(guard('W3', [approval, { task_key: 'send:outreach:old-alias.invalid', type: 'action', status: 'uncertain', payload: JSON.stringify({ email: lead.email, kind: 'outreach' }) }]).allowed, false);
});
test('W3 must block a pending followup for the same company', () => {
  assert.equal(guard('W3', [approval, { task_key: 'send:followup:synthetic.invalid', type: 'action', status: 'reserved' }]).allowed, false);
});
test('W4 requires an approved HOT/WARM prospect at the last send gate', () => {
  assert.equal(guard('W4', []).allowed, false);
  assert.equal(guard('W4', [{ ...approval, priority: 'COLD' }]).allowed, false);
  assert.equal(guard('W4', [{ ...approval, status: 'rejected' }]).allowed, false);
});
test('W4 blocks an uncertain original outreach even if lead status claims sent', () => {
  assert.equal(guard('W4', [approval, { task_key: 'send:outreach:synthetic.invalid', type: 'action', status: 'uncertain' }]).allowed, false);
});
test('W4 blocks a pending followup under a recipient alias', () => {
  assert.equal(guard('W4', [approval, { task_key: 'send:followup:alias.invalid', type: 'action', status: 'reserved', payload: JSON.stringify({ lead: { email: lead.email }, kind: 'followup' }) }]).allowed, false);
});
test('W3 ranks HOT prospects first within the existing quota', () => {
  const coldOrder = [{ ...lead, id: 1 }, { ...lead, id: 2, email: 'contact@hot.invalid', site: 'hot.invalid' }];
  const result = run('W3', 'Sélection', { Leads: coldOrder, Blacklist: [], 'Commercial – Queue': [approval, { task_key: 'prospect:hot.invalid', status: 'approved', priority: 'HOT' }] });
  assert.equal(result[0].json.id, 2);
});
function after(blacklist, changed = {}) {
  const action = { id: 41, kind: 'merci', to: lead.email };
  return run('W9', 'Chantier – garde', { 'Chantier – un par un': [action], 'Chantier – Clients frais': [{ id: 41, email: lead.email, statut: 'termine', ...changed }], 'Chantier – Blacklist fraîche': blacklist }, [])[0].json;
}
test('W9 respects freshly read blacklist and opt-outs before the review request', () => {
  assert.equal(after([{ email: lead.email }]).allowed, false);
});
test('W9 rejects a stale email recipient after a client record changes', () => {
  assert.equal(after([], { email: 'updated@synthetic.invalid' }).allowed, false);
});
test('W7 persists location and opportunity metadata in central prospect payload', () => {
  const rows = run('W7', 'Radar – tâches prospects', { Final: [{ rows: [{ ...lead, entreprise: 'Synthetic', type: 'syndic', ville: 'Paris', departement: '75', source: 'oxylabs' }] }], Emails: [{ email: lead.email, prompt: '' }], 'Radar – Queue': [], Requêtes: [{}, {}] });
  const p = JSON.parse(rows[0].json.payload);
  assert.equal(p.location, 'Paris (75)'); assert.equal(p.opportunity_type, 'syndic'); assert.ok(p.discovered_at);
});
test('Changed W3/W4 gates still allow qualified synthetic contacts without conflicting history', () => {
  for (const name of ['W3', 'W4']) for (const priority of ['HOT', 'WARM'])
    assert.equal(guard(name, [{ ...approval, priority }]).allowed, true);
});
test('Changed W9 gate still allows a completed synthetic project with no opt-out', () => {
  assert.equal(after([]).allowed, true);
});
test('W7 preserves a successful source result and deduplicates repeated companies in its batch', () => {
  const result = search([{ body: { data: [{ url: 'https://synthetic.invalid/' }] } }, { body: { data: [{ url: 'https://synthetic.invalid/contact' }] } }]);
  assert.equal(result.length, 1); assert.equal(result[0].json.host, 'synthetic.invalid');
});
test('W2 respects an existing opt-out before acknowledging a website request', () => {
  const rows = { Normaliser: [{ nom: 'Synthetic', email: lead.email }], 'Site – Blacklist fraîche': [{ email: lead.email }] };
  assert.equal(run('W2', 'Accusé ?', rows).length, 0);
  rows['Site – Blacklist fraîche'] = [];
  assert.equal(run('W2', 'Accusé ?', rows)[0].json.to, lead.email);
});
test('W6 cannot notify again after reserving the same Paris day, even with uncertain delivery', () => {
  const rows = { Journal: [], 'Rappels – Queue': [{ task_key: 'reminder:2026-10-19', status: 'uncertain' }] };
  assert.equal(run('W6', 'Vérifier échéances', rows).length, 0);
});
test('W6 retains due reminders and creates a reservation for first delivery', () => {
  const output = run('W6', 'Vérifier échéances', { Journal: [], 'Rappels – Queue': [] })[0].json;
  assert.ok(output.message); assert.equal(output._reservation.task_key, 'reminder:2026-10-19');
  assert.equal(output._reservation.status, 'reserved');
});
test('Legacy temporary W3/W4 test mode cannot select real email recipients', () => {
  for (const name of ['W3', 'W4'])
    assert.equal(run(name, 'Sélection', { 'Test (temporaire)': [{ body: { test: true } }] }).length, 0);
});
