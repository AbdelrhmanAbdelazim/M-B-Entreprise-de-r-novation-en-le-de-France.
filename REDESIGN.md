# REDESIGN premium : journal de travail

> **Pour l'agent suivant : commence par lire ce fichier en entier.**
> - Branche : `redesign-premium`, créée depuis `main` @ `8909697` le 23/10/2026.
> - Aucun merge dans `main` sans l'accord explicite du gérant.
> - Ce fichier est exclu de la publication du site (`_config.yml` → `exclude`).

## Statuts utilisés

`brouillon` → `testé` → `en attente d'accord` → `mergé`

## Demande du gérant (résumé fidèle)

- **A. Photos** :
  - retirer la galerie de l'accueil ;
  - page Réalisations en cartes (couverture + type de travaux + ville), chaque carte mène à une page projet (toutes les photos + avant/après) ;
  - lightbox ; WebP ; chargement différé ;
  - aucun visage, plaque ni adresse visible.
- **B. Design « maison d'architecture d'intérieur »** :
  - noir, blanc crème, touche dorée ;
  - titres serif, texte sans-serif ;
  - beaucoup d'espace ; une grande photo en haut.
  - **Accueil court** :
    - hero + une phrase ;
    - services (cartes simples) ;
    - « Pourquoi M&B » (un seul interlocuteur, devis détaillé sous 48h, durée écrite, chantier propre, 14 clients ont noté 5/5) ;
    - 3 projets → Réalisations ;
    - avis ;
    - étapes ;
    - bouton « Demander un devis ».
  - Mobile d'abord.
- **C. Ne rien casser** :
  - SEO (titles, descriptions, anciennes URL, JSON-LD) ;
  - 0 lien cassé ;
  - vitesse mesurée avant et après.
- **Interdits sur les pages publiques** :
  - prix et chiffres ;
  - « pas cher / moins cher / imbattable / promo / garantir » ;
  - menuiserie, « sur mesure ».
  - Exceptions autorisées par la demande elle-même : « 48h » et « 14 clients ont noté 5/5 ».

## Plan (dans l'ordre)

| # | Étape | Statut |
|---|---|---|
| 0 | Mesure de départ + ce fichier | testé |
| 1 | Photos : WebP (3 tailles), bandeaux texte retirés, avant/après séparés, données des projets | à faire |
| 2 | Pages projets (collection `_projets`) + nouvelle page /realisations/ en cartes + lightbox | à faire |
| 3 | Nouvelle feuille de style commune (palette, polices) + nouvel accueil court | à faire |
| 4 | Gabarit `page.html` (toutes les autres pages) aligné sur le nouveau style | à faire |
| 5 | Contrôles : build, liens, SEO identique à main, mots interdits, captures mobile/ordinateur, vitesse après | à faire |
| 6 | PR vers `main` (sans merge) + captures envoyées au gérant | à faire |

## Mesure de départ (Lighthouse 12.2.1, performance, site construit localement)

Les ressources externes (Google Fonts, cdnjs, GTM, Facebook) sont bloquées pendant la mesure, avant comme après, pour comparer seulement le code du site.

| Page | Mobile | Ordinateur |
|---|---|---|
| / | 96, LCP 2,4 s, CLS 0, 204 Ko | 99, LCP 0,6 s, 204 Ko |
| /realisations/ | 100, LCP 1,5 s, 1 328 Ko | 100, LCP 0,4 s, 3 230 Ko |
| /services/plomberie/ | 99, LCP 2,0 s, 108 Ko | 100, LCP 0,5 s, 108 Ko |

Script : `lh/run.sh` dans le scratchpad (non versionné). Pour le relancer :
- `npm i lighthouse@12.2.1` dans un dossier temporaire ;
- servir `_site` en local ;
- lancer Lighthouse avec `--blocked-url-patterns` sur `*fonts.googleapis.com*`, `*fonts.gstatic.com*`, `*cdnjs.cloudflare.com*`, `*googletagmanager*` et `*facebook*`.

## Inventaire des photos (fait le 23/10)

- Les 27 photos de `images/realisations/` sont des montages : bandeau « M&B RÉNOVATION » en haut, légende + téléphone en bas. Plusieurs légendes contiennent « sur mesure ».
- Les photos `chantier-1…13.jpg` à la racine sont les originaux propres de plusieurs montages :
  - 1 + 2 → carrelage salle de bain ;
  - 9 + 10 → chambre ;
  - 5 + 6 → salle de bain ;
  - 12 + 13 → séjour ;
  - 4 → pièce en pierre ;
  - 8 → plafond fissuré ;
  - 3 → électricité ;
  - 11 → cuisine.
- Aucune donnée EXIF ni GPS dans les photos.
- **Exclues** des nouvelles pages :
  - `equipe-sur-le-chantier.jpg` : visage ;
  - `chantier-7.jpg` : reflet d'une personne dans le miroir ;
  - `chantier-agencement-sur-mesure.jpg`, `realisation-bibliotheques-sur-mesure.jpg`, `chantier-tete-de-lit.jpg` : meubles fabriqués, donc menuiserie ;
  - `IMG_4803.jpeg`, `ad-carte.jpg` : cartes de visite.
- **Aucun fichier existant n'est supprimé ni renommé.** Les nouvelles images WebP sont créées à côté, dans `images/projets/`.

## Décisions

- **Ville des projets** : aucune ville précise n'est connue. Les cartes affichent « Paris · Île-de-France », comme sur les montages d'origine. Le champ `ville` de chaque projet est prêt pour la vraie commune, à confirmer par le gérant (voir « Restant »).

## Fait

- Étape 0 : mesure de départ, inventaire des photos, ce fichier.

## En cours

- Étape 1.

## Restant (dans l'ordre)

Étapes 1 à 6 du plan ci-dessus.

## Questions pour le gérant (ne bloquent pas le travail)

1. La ville réelle de chaque projet, s'il veut l'afficher à la place de « Paris · Île-de-France ».

## Dernier commit

(mis à jour à chaque étape)
