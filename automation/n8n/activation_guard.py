"""Static acceptance of freshly read n8n definitions; no network or node execution."""
from collections import deque


def node(document, name):
    return next(n for n in document['nodes'] if n['name'] == name)


def target(document, source, branch=0, port='main'):
    groups = document['connections'].get(source, {}).get(port, [])
    return [edge['node'] for edge in groups[branch]] if len(groups) > branch else []


def reachable_without(document, blocked):
    starts = [n['name'] for n in document['nodes'] if ('Trigger' in n['type'] or n['type'].endswith('.webhook') or n['type'].endswith('.emailReadImap')) and not n.get('disabled')]
    seen = set()
    queue = deque(starts)
    while queue:
        name = queue.popleft()
        if name in seen or name == blocked:
            continue
        seen.add(name)
        for edges in document['connections'].get(name, {}).get('main', []):
            queue.extend(edge['node'] for edge in edges)
    return seen


def assert_chain(document, loop, providers, validators):
    assert target(document, loop, 1) == [providers[0]], 'Specialist primary differs'
    for i, (provider, validator) in enumerate(zip(providers, validators)):
        assert target(document, provider, 0) == [validator], 'Missing model contract validation'
        if i < 2:
            assert node(document, provider).get('onError') == 'continueErrorOutput'
            assert node(document, validator).get('onError') == 'continueErrorOutput'
            assert target(document, provider, 1) == [providers[i + 1]]
            assert target(document, validator, 1) == [providers[i + 1]]
        else:
            assert node(document, provider).get('onError', 'stopWorkflow') == 'stopWorkflow'
            assert node(document, validator).get('onError', 'stopWorkflow') == 'stopWorkflow'


def inspect(documents, tables):
    w0 = documents['W0']['id']
    assert not documents['W0']['settings'].get('errorWorkflow')
    assert any(n['type'].endswith('.errorTrigger') and not n.get('disabled') for n in documents['W0']['nodes'])
    assert set(target(documents['W0'], 'Formater')) == {'Telegram', 'Journal'}
    for name, d in documents.items():
        assert d['settings'].get('timezone') == 'Europe/Paris'
        if name != 'W0': assert d['settings'].get('errorWorkflow') == w0
    for name, guard in [('W2', 'Accusé ?'), ('W3', 'Garde commerciale'), ('W4', 'Garde commerciale'), ('W9', 'Chantier – garde')]:
        d = documents[name]
        bypass = reachable_without(d, guard)
        assert not any(n['name'] in bypass and n['type'].endswith('.emailSend') for n in d['nodes']), 'SMTP can bypass its guard'
    manager = documents['My workflow']
    assert node(manager, 'AI Agent')['parameters']['needsFallback'] is True
    assert target(manager, 'OpenAI principal', port='ai_languageModel') == ['AI Agent']
    assert target(manager, 'Gemini Flash (gratuit)', 0, 'ai_languageModel') == ['AI Agent']
    gemini_edge = manager['connections']['Gemini Flash (gratuit)']['ai_languageModel'][0][0]
    assert gemini_edge['index'] == 1
    assert target(manager, 'AI Agent', 1) == ['Restaurer message original']
    assert target(manager, 'Restaurer message original') == ['AI Agent — Claude dernier secours']
    for kind, providers in [('Ventes', ['OpenAI Ventes', 'Gemini Ventes', 'Claude Ventes']), ('Revue', ['Claude Revue', 'OpenAI Revue', 'Gemini Revue'])]:
        assert_chain(manager, 'Boucle résilience ' + kind, providers, ['Valider ' + p for p in providers])
    assert_chain(documents['W1'], 'Boucle résilience Claude classification', ['OpenAI Claude classification', 'Gemini secours', 'Claude principal'], ['Valider OpenAI Claude classification', 'Valider Gemini Claude classification', 'Valider Claude Claude classification'])
    assert_chain(documents['W7'], 'Boucle résilience Claude : concurrent ?', ['Gemini Claude : concurrent ?', 'OpenAI Claude : concurrent ?', 'Claude : concurrent ? (Claude secours)'], ['Valider Gemini Claude : concurrent ?', 'Valider OpenAI Claude : concurrent ?', 'Valider Claude Claude : concurrent ?'])
    assert_chain(documents['W8'], 'Boucle résilience SEO', ['Gemini SEO', 'OpenAI SEO', 'Claude SEO'], ['Valider Gemini SEO', 'Valider OpenAI SEO', 'Valider Claude SEO'])
    for kind, last in [('Analyse tendances', 'Analyse tendances (Claude secours)'), ('7 idées', 'Claude : 7 idées')]:
        assert_chain(documents['W10'], 'Boucle résilience ' + kind, ['Gemini ' + kind, 'OpenAI ' + kind, last], ['Valider Gemini ' + kind, 'Valider OpenAI ' + kind, 'Valider Claude ' + kind])
    schemas = {table['id']: {c['name']: c['type'] for c in table['columns']} for table in tables}
    required = ['task_key', 'type', 'priority', 'source', 'owner', 'status', 'created_at', 'last_action', 'next_action', 'due_at', 'payload']
    assert all(schemas['aqPFAT3TBwLGhlIj'].get(k) == 'string' for k in required)
    assert schemas['NE0QU8afBFipimhW'].get('email') == 'string'
    for name in ['W2', 'W3', 'W4', 'W6', 'W7', 'W9']:
        for n in documents[name]['nodes']:
            reference = n['parameters'].get('dataTableId')
            if reference: assert reference['value'] in schemas
    return {'watchdog_routing': 'confirmed_all_eleven_to_W0_no_self_reference',
            'manager_and_specialist_primary_fallbacks': 'confirmed_from_live_graph',
            'smtp_guard_bypass': 'none_reachable_from_triggers',
            'existing_table_schemas': 'confirmed_no_new_tables',
            'transactional_exactly_once': 'not_proven_read_then_upsert_is_not_atomic'}
