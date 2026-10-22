# Plan exact des corrections 2 à 6 (n8n)

Préparé le 22/10/2026 par Claude Code, à partir de `n8n/SYSTEME.md` et des exports du 19/10 (`automation/n8n/`).
**Statut : rien n'est appliqué.**
- Chaque correction se fait l'une après l'autre, uniquement avec l'accord du gérant et en respectant les règles de SYSTEME.md (un seul agent à la fois, ligne « EN COURS » dans le journal).
- Aucune intervention sur n8n, le VPS ou le DNS sans cet accord.

## Étape 0 : lecture seule, dès que l'accès existe

1. **Hostinger** (via MCP) : état du serveur qui héberge `navajowhite-cormorant-668337.hostingersite.com`.
   - à vérifier : en ligne ou non, CPU, RAM, disque, redémarrages récents ;
   - consultation uniquement.
2. **n8n** : lancer `python3 n8n/verifier_n8n.py ~/MB-Renovation/.env.n8n`.
   - Le script ne fait que des requêtes GET.
   - Il donne la santé, la liste des workflows (actif, date de modification, version comparée au 19/10, doublons) et les exécutions des 48 dernières heures (erreurs et e-mails réellement envoyés).
3. **Si une version diffère du manifest**, quelqu'un a modifié le workflow depuis le 19/10.
   - Exporter la version live : `python3 automation/n8n/snapshot.py --out automation/n8n/private-live`, dossier non versionné.
   - Adapter les correctifs ci-dessous à cette version.
   - **Ne jamais importer** un export expurgé par-dessus la production.

## Méthode commune pour 3 à 6

- Modifier **le nœud indiqué uniquement**, dans l'interface n8n ou par l'API (`PUT /api/v1/workflows/{id}` construit à partir de l'export live du moment).
- Garder le même ID de workflow, puis publier.
- Ensuite :
  - relancer `verifier_n8n.py` ;
  - ajouter une ligne au journal de SYSTEME.md ;
  - commiter l'export expurgé mis à jour dans `automation/n8n/` ;
  - mettre à jour `manifest.json`.
- Aucun envoi de test vers un vrai client ou prospect.

## Correction 2 : santé du serveur (priorité haute)

Le 19/10, le serveur répondait 500 (W0) et 504 (table Queue).

- **Diagnostic, en lecture seule** : étape 0.
- **Causes à confirmer**, sans deviner : mémoire ou disque saturés, conteneur n8n arrêté, ou délai dépassé côté nginx.
- **Action selon la cause, proposée au gérant avant toute exécution** :
  - libérer de l'espace : purge des anciennes exécutions, avec `EXECUTIONS_DATA_PRUNE=true` et `EXECUTIONS_DATA_MAX_AGE=168` ;
  - ou redémarrer le service n8n ;
  - ou augmenter les ressources (offre Hostinger).
  - Le redémarrage et le changement d'offre demandent un « oui » explicite.
- **Vérification** : `/healthz` répond 200, et `verifier_n8n.py` liste les 12 workflows actifs, sans erreur depuis le correctif.

## Correction 3 : W9 n'envoie plus d'e-mails le week-end

- **Workflow** : `W9 – Après chantier (avis + parrainage)` (ID `9ttUYW3XcSztxwRu`).
- **Nœud** : `À envoyer` (Code). C'est le premier nœud de la chaîne d'envoi :
  - Clients → Chantier – Queue → **À envoyer** → … → Email client.
- **Modification** : ajouter juste après la ligne `const t = today();` :

```js
const dowW9 = new Date(t + 'T12:00:00Z').getUTCDay();
if (dowW9 === 0 || dowW9 === 6) return [];   // pas d'e-mail client le samedi ni le dimanche
```

- **Effet** : le samedi et le dimanche, rien n'est préparé. Le lundi, les remerciements en attente partent normalement, une seule fois, grâce à la garde existante.
- Les commandes Telegram de W9 ne passent pas par ce nœud et ne sont pas touchées.
- **Vérification** :
  - lecture du code ;
  - l'exécution suivante d'un samedi se termine sans aucun nœud « Email client » exécuté ;
  - `verifier_n8n.py` affiche e-mails envoyés = 0 pour W9 le week-end.

## Correction 4 : STOP détecté sans dépendre de l'IA (W1)

- **Workflow** : `W1 – Réponses emails`.
- **Nœud** : `Ajout blacklist ?` (Code).
- **Problème** :
  - l'ajout à la Blacklist n'a lieu que si l'IA classe le message en `stop` ;
  - si la réponse de l'IA est illisible, le message est ignoré (`return`).
- **Modification** :
  - ajouter en tête du nœud :

```js
const STOP_RX = /(^|[^a-z])stop([^a-z]|$)|d[ée]sinscri|d[ée]sabonn|unsubscribe|ne (plus|pas) (me )?(contacter|recevoir|[ée]crire)|retirez[- ]?moi|supprimez[- ]?moi/i;
```

  - et remplacer les 3 premières lignes du `forEach` par :

```js
  const raw = String(it.json.text || '');
  let r = {}; try { r = JSON.parse(raw.slice(raw.indexOf('{'), raw.lastIndexOf('}') + 1)); } catch (e) { r = {}; }
  const e = (src[i] || src[0]).json;
  const isBounce = r.categorie === 'rebond' || /mailer-daemon|postmaster/i.test(e.from);
  const isStop = r.categorie === 'stop' || STOP_RX.test(String(e.prompt || ''));
  if (!isStop && !isBounce) return;
```

  - Le reste du nœud ne change pas.
- **Effet** : un « STOP » ou une demande de désinscription est toujours mis en Blacklist, même si l'IA se trompe ou ne répond pas.
- **Vérification** : sur l'exécution suivante, avec un vrai message déjà reçu (pas d'envoi de test), contrôler la Blacklist. Sinon, relire le code avec 5 exemples de texte, sans exécuter le workflow.

## Correction 5 : retirer le code de test résiduel (W3, W4, W7)

Le nœud `Test (temporaire)` n'existe plus. Le code qui l'appelle ne fait rien, mais il contient une adresse personnelle et pourrait se réactiver par erreur.

| Workflow | Nœud | À supprimer |
|---|---|---|
| W3 – Envoi quotidien | `Sélection` | Le bloc depuis `let test = false; try { test = !!$('Test (temporaire)')…` jusqu'à la fin de `if (test) return [ … ];` |
| W4 – Relance unique | `Sélection` | Même bloc |
| W7 – Recherche de leads | `Requêtes` | La ligne `let test = null; try { test = $('Test (temporaire)').first().json.body; } catch (e) {}` et le bloc `if (test && test.test) { … return [ … ]; }`. Le reste ne change pas. |

**Vérification** : aucun texte `Test (temporaire)` ni l'adresse de test dans les 3 workflows. L'exécution planifiée suivante est un succès.

## Correction 6 : noms clairs (cosmétique)

| ID | Nom actuel | Nouveau nom |
|---|---|---|
| W5 | W5 – Rapport hebdomadaire | W5 – Rapports (08h / 18h + lundi) |
| My workflow | My workflow | Chat – Pilotage (Growth Queue) |

- Les liens entre workflows (`errorWorkflow`) passent par l'ID : renommer ne casse rien.
- Mettre à jour SYSTEME.md et le manifest.

## Ordre conseillé

2 → 3 → 4 → 5 → 6, une correction à la fois, avec vérification entre chaque.
Durée estimée une fois l'accès ouvert : environ 1 h, hors éventuelle intervention Hostinger.
