# Système n8n M&B Rénovation : référence commune Claude Code / Codex

> **Règle n° 1 : un seul agent modifie le système à la fois.**
> Avant toute modification, dans n8n comme dans ce dépôt, l'agent (Claude Code ou Codex) lit ce fichier en entier.
> Il ajoute ensuite une ligne « EN COURS » au journal ci-dessous, et la remplace par le compte rendu une fois le travail terminé.
> Si une ligne « EN COURS » d'un autre agent existe, il ne touche à rien et prévient le gérant.
> Aucune correction n'est appliquée sans l'accord explicite du gérant.

## Où se trouvent les exports

- **Exports JSON des workflows** : `automation/n8n/` (W0 à W10, `My workflow.json`).
  - Ce sont des exports réels, sans clés ni identifiants de credentials, déposés par Codex le 19/10/2026.
  - L'historique Git permet de revenir en arrière.
  - `manifest.json` donne, pour chaque workflow, l'ID, la versionId et l'empreinte.
- **Nouvel export** : uniquement avec `python3 automation/n8n/snapshot.py`, qui ne fait que lire n8n. On ne réimporte jamais un export expurgé par-dessus la production.
- **Interdit dans Git** : une clé API, un mot de passe, un ID de chat Telegram, le chemin d'un webhook ou une ligne de client.

## Les workflows (dernier état connu : publiés et actifs le 19/10/2026)

Heures en Europe/Paris. Toutes les erreurs remontent à W0.

| ID | Nom n8n | Rôle | Déclencheur | Envoie des e-mails ? |
|---|---|---|---|---|
| W0 | W0 – Erreurs (Telegram + journal) | Erreurs de tous les workflows → Telegram + Journal | Error Trigger | Non |
| W1 | W1 – Réponses emails | Lit la boîte de réception, classe les réponses (intéressé / STOP / rebond), met à jour Leads et Blacklist, prépare un brouillon | IMAP | Non (brouillons seulement) |
| W2 | W2 – Demandes du site web | Formulaire du site → Clients + Telegram + accusé de réception | Webhook | Oui : accusé de réception au demandeur |
| W3 | W3 – Envoi quotidien | Premier e-mail de prospection aux leads approuvés HOT/WARM | lun.–jeu. 08:30 | Oui |
| W4 | W4 – Relance unique | Une seule relance, 7 jours après le premier e-mail, sans réponse | lun.–jeu. 09:30 | Oui |
| W5 | W5 – Rapport hebdomadaire | Rapport Telegram : chaque jour à 08:00 et 18:00, plus large le lundi | 08:00 et 18:00 | Non |
| W6 | W6 – Rappels échéances | Rappels d'échéances sur Telegram | chaque jour 09:00 | Non |
| W7 | W7 – Recherche de leads | Recherche Oxylabs + classement HOT/WARM/COLD | 06:10, 10:10, 14:10, 18:10 | Non |
| W8 | W8 – Notifications pages SEO | Contrôle SEO de 5 pages au maximum, sans modifier le site | 07:30 + webhook | Non |
| W9 | W9 – Après chantier (avis + parrainage) | Remerciement + demande d'avis + parrainage (chantier terminé) ; commandes Telegram | toutes les 15 min, 08–20 h + Telegram | Oui : aux clients |
| W10 | W10 – Idées de contenu (vidéos) | Jusqu'à 7 brouillons de contenu à valider (rien n'est publié) | chaque jour 04:30 | Non |
| Chat | My workflow | Chat de pilotage + coordination chaque heure (Growth Queue) | Chat + chaque heure | Non |

Tables n8n : Leads, Clients, Blacklist, Journal, Growth Queue (IDs dans `automation/n8n/data-tables.json`).

## Règles métier (à respecter dans chaque texte, prompt et e-mail)

1. **Activités autorisées** :
   - plâtrerie, cloisons et faux plafonds ;
   - électricité, plomberie, carrelage, peinture ;
   - parquet et sols ;
   - pose de placards et de portes ;
   - VMC ;
   - rénovation complète.
2. **Jamais** : maçonnerie, démolition (lourde), gros œuvre, fabrication de menuiserie, toiture, façade.
3. **Aucune promesse** de prix, de montant, de délai ou de date. Seuls engagements réels : « réponse sous 24 h » et « devis sous 48 h ».
4. Aucun faux avis, aucun chiffre inventé, aucun nom de client. Pas de notion d'« équipe » : un seul interlocuteur, le gérant.
5. **Prospection (W3 + W4)** :
   - 30 e-mails par jour au maximum, dont 20 relances au maximum ;
   - du lundi au jeudi, entre 08 h et 18 h ;
   - jamais le week-end ;
   - pause de 2 à 5 minutes entre deux envois ;
   - une seule relance.
6. **Arrêt des envois** : jamais d'envoi à une adresse de la Blacklist ni à son domaine (sauf domaines de messagerie gratuite), ni à un lead qui a répondu. « STOP » ou un rebond → ajout à la Blacklist.
7. **Validation humaine** : aucun envoi ni aucune publication décidés seuls par une IA. Une campagne ou un contenu n'avance qu'avec l'approbation du gérant.
8. **Parrainage** : 100 € pour le parrain, 50 € pour le proche, travaux à partir de 3 000 €. Ces montants doivent rester identiques à `/parrainage/`.

## Accès

- Hôte : variable `N8N_BASE_URL`. Clé : variable `N8N_API_KEY`, en lecture seule si possible.
- Les deux se configurent dans les paramètres de l'environnement, jamais dans Git ni dans la conversation.
- Les sessions cloud doivent avoir l'hôte n8n autorisé dans l'accès réseau.

## Journal des modifications

Format : `AAAA-MM-JJ | agent | workflows ou fichiers | ce qui a changé | vérification faite`

| Date | Agent | Portée | Changement | Vérification |
|---|---|---|---|---|
| 2026-10-19 | Codex | W0–W10, My workflow, Growth Queue | Extension du système : Growth Queue, réservations anti-doublon, IA avec secours (OpenAI / Gemini / Claude), W7 4 fois par jour, W8 quotidien, W9 toutes les 15 min, W10 brouillons. Exports dans `automation/n8n/`. | D'après `automation/n8n/STATUS.md` ; serveur en erreur 500/504 lors de l'export |
| 2026-10-22 | Claude Code | `n8n/SYSTEME.md`, `_config.yml` | Création de ce fichier ; dossier `n8n/` exclu de la publication du site. Audit en lecture seule des exports : aucune modification dans n8n. | Audit statique des 12 exports ; accès direct à n8n impossible (proxy + clé absente) |
| 2026-10-22 | Claude Code | `_config.yml` | Accord du gérant : `automation/` et `AGENTS.md` exclus de la publication (ils étaient visibles sur www.maison-mb.fr et dans le sitemap). Fichiers conservés dans Git. | Build github-pages OK ; sitemap 74 → 71 URL ; toutes les autres pages identiques |
