# Étape 15a : audit 14 confirmé et complété (23/10/2026, Devin)

Statut : **TESTÉ**. Preuves fraîches du 23/10/2026 ~15h40 UTC, distinctes des chiffres historiques de l'étape 14 (Claude).

## Sources
- main épinglé `8909697d920da75f140e97dec29e16bc04d244f3`, build local `github-pages` (bundle isolé hors dépôt).
- Branche source `redesign-premium` @ `f893f03c79c96d44ced4f3bdfdb891993e6c1473`, build local.
- **Nouveau** : le site publié https://www.maison-mb.fr est joignable depuis cette session (Claude ne l'avait pas). Lecture seule (GET), aucun envoi.

## Résultats frais
| Contrôle | Résultat | Écart avec l'étape 14 |
|---|---|---|
| Site publié = main | 70/70 pages HTML du sitemap publié identiques octet pour octet (espaces normalisés) au build local de main ; `plaquette.pdf` présent (binaire non comparé). Serveur GitHub Pages, `last-modified` 22/10 23:52 GMT. | Confirmé, désormais prouvé sur le live (avant : supposé) |
| Sitemap | 71 URL live = 71 URL build main | Confirmé |
| Liens internes (href/src) + ancres `#` | main : 71 pages, 2 139 liens, **0 cassé, 0 ancre cassée**. Branche : 98 pages, 0 cassé réel (96 faux positifs = commentaire JS « grande image »), 0 ancre cassée | Confirmé + ancres vérifiées |
| Icônes Font Awesome 6.5.1 | 19 classes distinctes utilisées sur main, toutes présentes dans la CSS cdnjs 6.5.1 | Confirmé (14 annonçait 22 ; méthode de comptage différente) |
| JS / débordement (Playwright, 390 et 1366 px ; accueil, plomberie, Versailles, réalisations, blog) | 0 erreur JS, 0 débordement, main et branche | Confirmé |
| Accessibilité (axe-core 4.10, WCAG 2 A/AA) | Accueil main : `color-contrast` 18 éléments, `link-name` 4 (icônes réseaux sans nom). Pages internes main : `color-contrast` 2, `link-in-text-block` 2 à 9. Lighthouse accessibilité accueil main : 90 | **Nouveau** (14 ne mesurait pas axe) |
| Titres | Accueil main : 3 sauts de niveau (h2→h4/h5) | Confirmé |
| Zones tactiles < 24 px (hors liens en ligne) | Accueil main : 4 ; pages internes : 1 à 4 | 14 annonçait 14 (méthode incluant les liens en ligne) ; à remesurer avec la même méthode avant décision |
| Bouton devis au 1er écran | Accueil main : oui. Plomberie, Versailles, réalisations, blog : **non** (main et branche). WhatsApp au 1er écran : non nulle part | Confirmé |
| Formulaire accueil main (390 et 1366) | 4 champs avec `<label for>` ; nom, tél., projet `required` ; envoi vide → 3 champs invalides, rien n'est envoyé. Envoi rempli (données **synthétiques**, réseau **intercepté et bloqué**) : 1 POST `x-www-form-urlencoded` vers le webhook n8n (champs nom, telephone, email, projet, source=site, page=/) + ouverture `wa.me/33753306559?text=…` | **Nouveau** : transport vérifié en interception. Le webhook live n'a **pas** été appelé (interdit) ; sa réception côté n8n reste **non testée** |
| Lighthouse 12.2.1 accueil main (externes bloqués, même méthode que 14) | Mobile : perf 97, a11y 90, bonnes pratiques 100, SEO 100, LCP 2,4 s, CLS 0, 204 Ko. Desktop : perf 99, LCP 0,6 s | Confirmé (14 : 96 / 99) |

## Limites
- Lighthouse en local avec CDN/polices/trackers bloqués : ce n'est pas la vitesse réelle vue par un visiteur (polices Google, Font Awesome, GTM non comptés).
- Aucune mesure de terrain (CrUX), aucune donnée de conversion : impossible d'affirmer quel design convertit mieux.
- Webhook n8n et WhatsApp : seulement le format de la requête est prouvé, pas la réception.
- axe ne détecte qu'une partie des problèmes d'accessibilité ; pas de test lecteur d'écran.

## Outils (versionnés dans `_redesign/outils/`)
`audit.js` (Playwright + axe), `formtest.js` (formulaire, réseau intercepté), `links.py` (liens + ancres), `competitors.js` (relevé concurrents).
