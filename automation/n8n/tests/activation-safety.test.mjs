// Acceptance checks against private candidates assembled from the freshly read live versions.
// No n8n node engine, SMTP, HTTP, model or Telegram transport is available in this VM.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import vm from 'node:vm';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
const directory = process.env.N8N_ACTIVATION_FIXTURE_DIR;
assert.ok(directory, 'Provide the private staged live-candidate directory');
const source = name => JSON.parse(readFileSync(join(directory, name + '.json')));
const item = json => ({ json });
const now = new Date('2026-10-19T08:00:00Z');
class Clock extends Date { constructor(...args) { super(...(args.length ? args : [now.getTime()])); } static now() { return now.getTime(); } }
function run(name, node, rows, input = [], clock = Clock) {
  const code = source(name).nodes.find(n => n.name === node).parameters.jsCode;
  return vm.runInNewContext(`(() => {${code}\n})()`, { Date: clock, $runIndex: 0, $execution: { id: 'isolated-activation' }, $json: input[0] || {},
    $input: { all: () => input.map(item), first: () => item(input[0] || {}) },
    $: key => { if (!(key in rows)) throw Error('Missing synthetic node: ' + key); const values = rows[key].map(item); return { all: () => values, first: () => values[0], item: values[0] }; },
  }, { timeout: 1000 });
}
const person = { id: 7301, email: 'contact@activation.invalid', site: 'activation.invalid', statut: 'nouveau' };
const approved = { task_key: 'prospect:activation.invalid', status: 'approved', priority: 'HOT' };
function gate(name, { lead = {}, blacklist = [], queue = [approved], clock = Clock } = {}) {
  const current = { ...person, ...(name === 'W4' ? { statut: 'envoye', date_envoi: '2026-10-01' } : {}), ...lead };
  return run(name, 'Garde commerciale', { 'Un par un': [current], 'Avant envoi – Leads': [current], 'Avant envoi – Blacklist': blacklist }, queue, clock)[0].json.allowed;
}
for (const name of ['W3', 'W4']) {
  test(`${name}: only approved HOT/WARM can pass the fresh live send gate`, () => {
    for (const priority of ['HOT', 'WARM']) assert.equal(gate(name, { queue: [{ ...approved, priority }] }), true);
    for (const priority of ['COLD', 'UNKNOWN', '']) assert.equal(gate(name, { queue: [{ ...approved, priority }] }), false);
    for (const status of ['needs_review', 'rejected', 'deferred']) assert.equal(gate(name, { queue: [{ ...approved, status }] }), false);
  });
  test(`${name}: reply/rejection/STOP cancels a pending send`, () => {
    assert.equal(gate(name, { lead: { date_reponse: '2026-10-19' } }), false);
    for (const statut of ['stop', 'pas_interesse', 'interesse', 'erreur']) assert.equal(gate(name, { lead: { statut } }), false);
  });
  test(`${name}: blacklist and same-company suppression are effective`, () => {
    assert.equal(gate(name, { blacklist: [{ email: person.email }] }), false);
    assert.equal(gate(name, { blacklist: [{ email: 'other@activation.invalid' }] }), false);
    assert.equal(gate(name, { blacklist: [{ email: 'unrelated@elsewhere.invalid' }] }), true);
  });
  test(`${name}: existing reservation/uncertain/completed action blocks repeat delivery`, () => {
    const kind = name === 'W3' ? 'outreach' : 'followup';
    for (const status of ['reserved', 'uncertain', 'done', 'needs_attention']) {
      assert.equal(gate(name, { queue: [approved, { task_key: `send:${kind}:activation.invalid`, type: 'action', status }] }), false);
      assert.equal(gate(name, { queue: [approved, { task_key: `send:${kind}:old-alias.invalid`, type: 'action', status, payload: JSON.stringify({ email: person.email, kind }) }] }), false);
    }
  });
  test(`${name}: conflicting approvals fail closed`, () => {
    assert.equal(gate(name, { queue: [approved, { ...approved, status: 'rejected' }] }), false);
  });
  test(`${name}: no delivery outside the business window`, () => {
    class Evening extends Clock { constructor(...args) { super(...(args.length ? args : ['2026-10-19T19:00:00Z'])); } }
    assert.equal(gate(name, { clock: Evening }), false);
  });
  test(`${name}: legacy temporary test trigger selects no real recipient`, () => {
    assert.equal(run(name, 'Sélection', { 'Test (temporaire)': [{ body: { test: true } }] }).length, 0);
  });
}
test('W4: already-followed-up and not-yet-due prospects are suppressed', () => {
  assert.equal(gate('W4', { lead: { date_relance: '2026-10-18' } }), false);
  assert.equal(gate('W4', { lead: { date_envoi: '2026-10-18' } }), false);
  assert.equal(gate('W4', { queue: [approved, { task_key: 'send:outreach:activation.invalid', type: 'action', status: 'uncertain' }] }), false);
});
test('W1: explicit unsubscribe is converted to the existing blacklist contract', () => {
  const result = run('W1', 'Ajout blacklist ?', { 'Claude classification': [{ text: JSON.stringify({ categorie: 'stop' }) }], 'Filtre expéditeurs': [{ from: person.email }], 'Leads – lecture': [person], 'Blacklist – lecture': [] });
  assert.equal(result[0].json.email, person.email); assert.equal(result[0].json.raison, 'stop');
});
test('W2: website acknowledgement respects an existing unsubscribe without changing the intake', () => {
  const rows = { Normaliser: [{ nom: 'Synthetic', email: person.email }], 'Site – Blacklist fraîche': [{ email: person.email }] };
  assert.equal(run('W2', 'Accusé ?', rows).length, 0);
  rows['Site – Blacklist fraîche'] = []; assert.equal(run('W2', 'Accusé ?', rows)[0].json.to, person.email);
});
test('W6: reserved or uncertain reminder cannot be delivered a second time that Paris day', () => {
  for (const status of ['reserved', 'uncertain', 'done', 'needs_attention'])
    assert.equal(run('W6', 'Vérifier échéances', { Journal: [], 'Rappels – Queue': [{ task_key: 'reminder:2026-10-19', status }] }).length, 0);
});
test('W7: source failure reaches the error route rather than successful zero-lead completion', () => {
  const rows = { Requêtes: [{}, {}], Leads: [], Blacklist: [] };
  assert.throws(() => run('W7', 'URLs', rows, [{ error: 'synthetic timeout' }, { body: { data: [] } }]), /W7_SEARCH_SOURCE_FAILED/);
  assert.equal(run('W7', 'URLs', rows, [{ body: { data: [] } }, { body: { data: [] } }]).length, 0);
});
test('W9: completed project, current recipient and fresh blacklist are required', () => {
  const rows = { 'Chantier – un par un': [{ id: person.id, kind: 'merci', to: person.email }], 'Chantier – Clients frais': [{ id: person.id, email: person.email, statut: 'termine' }], 'Chantier – Blacklist fraîche': [] };
  const allowed = () => run('W9', 'Chantier – garde', rows)[0].json.allowed;
  assert.equal(allowed(), true); rows['Chantier – Blacklist fraîche'] = [{ email: person.email }]; assert.equal(allowed(), false);
  rows['Chantier – Blacklist fraîche'] = []; rows['Chantier – Clients frais'][0].statut = 'en_cours'; assert.equal(allowed(), false);
  rows['Chantier – Clients frais'][0].statut = 'termine'; rows['Chantier – Clients frais'][0].email = 'changed@activation.invalid'; assert.equal(allowed(), false);
});
