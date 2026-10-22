# Plan exact des corrections 2 à 6 (n8n)

Préparé le 22/10/2026 par Claude Code, à partir de `n8n/SYSTEME.md` et des exports du 19/10 (`automation/n8n/`).
**Mis à jour le 22/10/2026 vers 16 h** à partir des versions live (sauvegarde du 22/10 15:52, versions vérifiées identiques au live à 16 h).
**Statut au 22/10 (16 h 45) : corrections 3, 4, 5 et 6 appliquées** (voir journal de SYSTEME.md). **Correction 2 : à faire dans hPanel.** W3 reste désactivé jusqu'à la correction 2.
> ⚠️ La correction 4 appliquée diffère du texte ci-dessous : le test STOP porte sur le texte propre de l'expéditeur, pas sur `e.prompt` entier (qui contient le mot « stop » et notre e-mail cité).
- Chaque correction se fait l'une après l'autre, uniquement avec l'accord du gérant et en respectant les règles de SYSTEME.md (un seul agent à la fois, ligne « EN COURS » dans le journal).
- Aucune intervention sur n8n, le VPS ou le DNS sans cet accord.

## État live au 22/10 (contrôle en lecture seule)

- **17 workflows** : les 12 connus + 5 autres, absents de SYSTEME.md :
  - actifs : `M&B – ChatGPT Codex MCP`, `M&B – ChatGPT production ingress`, `M&B — AI Continuous Improvement` (1 e-mail envoyé en 48 h) ;
  - inactifs : `Gemini + Claude Automation Workflow`, `M&B campaign145 isolated temporary transport 20261020`.
- **10 des 12 workflows** ont une version ≠ manifest (modifiés surtout le 20/10 au soir), sans ligne dans le journal.
- **Nœuds visés par ce plan** (comparaison du code export 19/10 ↔ live) :

| Correction | Nœud | Live |
|---|---|---|
| 3 | W9 `À envoyer` | identique : correctif valable tel quel |
| 4 | W1 `Ajout blacklist ?` | identique : correctif valable tel quel |
| 5 | W3 et W4 `Sélection` | modifié : l'adresse de test a déjà été retirée, il reste 2 lignes inutiles |
| 5 | W7 `Requêtes` | modifié (BOAMP, preuves de source) : le bloc de test est toujours là |
| 6 | W5, My workflow | noms inchangés |

- **Incidents du 22/10** (heures de Paris) :
  - 05:01 et 06:00 : runner des nœuds Code indisponible (My workflow) ; même erreur le 21/10 à 16:00 et 16:15 (W9) ;
  - 06:10 : W7, échec de la source de recherche ;
  - 07:30 et 08:00 : erreurs DNS (Telegram et pages du site injoignables) → W8 et W5 en échec, et **W0 lui-même en échec** (11 erreurs en 48 h : les alertes Telegram ne partent pas) ;
  - 08:30 : W3 envoie 4 e-mails, puis échoue sur `Journal` (« Data table module is disabled ») → W3 désactivé par le gérant ;
  - 09:30 : **W4 ne s'est pas exécuté** (actif, jeudi : une exécution était attendue) ;
  - depuis au moins 15:30 : les Data tables fonctionnent de nouveau (W9, My workflow en succès).

## Préalable : un seul agent à la fois

- Les 3 workflows « ChatGPT / AI Continuous Improvement » actifs et les modifications du 20/10 montrent qu'un autre agent (Codex / ChatGPT) a travaillé sur n8n sans l'inscrire au journal.
- **Avant toute correction**, le gérant confirme que cet agent est arrêté, et décide du sort de ces 3 workflows (les garder actifs ou non). Aucune action de Claude Code sur ces workflows sans cette décision.

## Étape 0 : lecture seule (faite le 22/10)

1. **Hostinger** (via MCP) : état du serveur qui héberge `navajowhite-cormorant-668337.hostingersite.com`.
   - à vérifier : en ligne ou non, CPU, RAM, disque, redémarrages récents ;
   - consultation uniquement.
2. **n8n** : lancer `N8N_BASE_URL=https://navajowhite-cormorant-668337.hostingersite.com N8N_API_KEY="$(cat ~/.n8n_api_key)" python3 n8n/verifier_n8n.py` (la clé reste dans `~/.n8n_api_key`, hors dépôt).
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

Le 19/10, le serveur répondait 500 (W0) et 504 (table Queue). Le 22/10 : runner Code indisponible, erreurs DNS sortantes, module Data table désactivé pendant un moment, exécution planifiée de W4 manquée (voir « État live »). Tout cela pointe vers l'hébergement, pas vers les workflows.

- **Hébergement** : offre Hostinger « AI automation apps » (pas un VPS). L'API Hostinger ne donne ni CPU, ni RAM, ni redémarrage, ni snapshot pour cette offre.
  - Le gérant regarde dans **hPanel** : utilisation CPU / RAM / disque, redémarrages récents, sauvegardes disponibles.
  - `/healthz` n'est pas exposé sur cet hôte (il renvoie la page de l'interface) : la santé se vérifie avec `verifier_n8n.py` (l'API répond).
- **Causes à confirmer**, sans deviner : ressources saturées (le runner Code et le DNS lâchent ensemble), redémarrage du service, ou panne côté Hostinger.
- **Action selon la cause, proposée au gérant avant toute exécution** :
  - purger les anciennes exécutions (`EXECUTIONS_DATA_PRUNE=true`, `EXECUTIONS_DATA_MAX_AGE=168`), si l'offre permet de régler ces variables ;
  - ou redémarrer n8n depuis hPanel ;
  - ou passer à une offre plus grande ;
  - ou ouvrir un ticket Hostinger avec les heures des incidents ci-dessus.
  - Le redémarrage et le changement d'offre demandent un « oui » explicite.
- **Après correction** :
  - vérifier les 4 e-mails W3 du 22/10 à 08:30 : présents dans Leads (statut mis à jour) malgré l'échec du `Journal` ? Sinon, les marquer à la main **avant** de réactiver W3, pour éviter un second envoi ;
  - réactiver W3 avec l'accord du gérant ;
  - surveiller la prochaine exécution de W4 (lundi 26/10 09:30) ;
  - W0 : vérifier qu'une alerte Telegram arrive bien.
- **Vérification** : `verifier_n8n.py` sans nouvelle erreur runner, DNS ou Data table pendant 48 h ; W3 et W4 exécutés à l'heure prévue.

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

**Mise à jour live** : dans W3 et W4, l'adresse de test a déjà été retirée (le bloc renvoie maintenant `[]`). Il ne reste que 2 lignes sans effet. Dans W7, le bloc de test est toujours présent.

| Workflow | Nœud | À supprimer (version live) |
|---|---|---|
| W3 – Envoi quotidien | `Sélection` | Les 2 lignes 20–21 : `let test = false; try { test = !!$('Test (temporaire)').first().json.body.test; } catch (e) {}` et `if (test) return []; // Test mode never produces real email recipients.` |
| W4 – Relance unique | `Sélection` | Les mêmes 2 lignes (20–21) |
| W7 – Recherche de leads | `Requêtes` | La ligne 77 `let test = null; try { test = $('Test (temporaire)').first().json.body; } catch (e) {}` et le bloc qui commence ligne 89 `if (test && test.test) { … return [ … ]; }`. Le reste ne change pas (dont les nouvelles fonctions BOAMP / `si…`). |

- Ne pas toucher à la nouvelle ligne `if(Number(l.id)===79)continue;` de W3 et W4 : c'est une protection anti-renvoi.
- W3 est désactivé : le modifier ne le réactive pas. La réactivation suit la correction 2.

**Vérification** : aucun texte `Test (temporaire)` dans les 3 workflows. L'exécution planifiée suivante de W4 et W7 est un succès.

## Correction 6 : noms clairs (cosmétique)

| ID | Nom actuel | Nouveau nom |
|---|---|---|
| W5 | W5 – Rapport hebdomadaire | W5 – Rapports (08h / 18h + lundi) |
| My workflow | My workflow | Chat – Pilotage (Growth Queue) |

- Les liens entre workflows (`errorWorkflow`) passent par l'ID : renommer ne casse rien.
- Mettre à jour SYSTEME.md et le manifest.

## Ordre conseillé

Préalable (autre agent arrêté) → 2 → 3 → 4 → 5 → 6, une correction à la fois, avec vérification entre chaque.
- Chaque modification part de la version live du moment (refaire `snapshot.py` juste avant, si une version a changé depuis le 22/10 15:52).
- Durée estimée : environ 1 h, hors intervention Hostinger.
