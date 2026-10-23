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
| 1 | Photos : WebP (3 tailles), bandeaux texte retirés, avant/après séparés, données des projets | testé |
| 2 | Feuille de style commune + gabarit `page.html` (toutes les pages) + en-tête, pied de page, fenêtre devis et lightbox communs | testé |
| 3 | Pages projets (collection `_projets`) + nouvelle page /realisations/ en cartes | testé |
| 4 | Nouvel accueil court | testé |
| 5 | Contrôles : build, liens, SEO identique à main, mots interdits, captures mobile/ordinateur, vitesse après | testé |
| 6 | PR vers `main` (sans merge) + captures envoyées au gérant | en attente d'accord |

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

- **Palette** :
  - noir `#121110` ;
  - crème `#F5F0E6` (fond) et `#FBF8F2` (cartes) ;
  - or `#B8924A` pour les filets ;
  - or foncé `#7E6127` pour les petits textes sur crème (contraste suffisant) ;
  - or clair `#D2B272` sur fond noir.
  - Raison : demande « noir, blanc crème, touche dorée ». L'or du logo `#C9A84C` est trop pâle pour du texte sur crème.
- **Polices** : Cormorant Garamond (titres serif) et Jost (texte), déjà utilisées par le site. Graisses réduites à 400/500 + italique (Cormorant) et 300/400/500 (Jost), pour charger moins.
- **Icônes** : SVG en ligne dans les nouveaux gabarits. Font Awesome est chargé sans bloquer l'affichage (`media="print"` puis `all`), car des pages existantes (services, villes, articles) l'utilisent encore.
- **Fenêtre devis sur toutes les pages** : avant, elle n'existait que sur l'accueil. Les champs, le message WhatsApp et la copie vers le webhook n8n sont identiques. Tous les boutons `data-devis` l'ouvrent.
- **Chiffres retirés** : bloc paiement et note de la fenêtre devis (« projets à partir de 3 000 €, main-d'œuvre en 3 fois » devient « projets éligibles, en plusieurs fois »). Raison : règle « pas de prix ni de chiffres ».
  - Gardés : « 24h ouvrées » dans la fenêtre devis (texte du gérant du 23/10), « 48h » et « 14 clients 5/5 » (demandés).
  - Gardés aussi : les identifiants légaux et de contact (SIRET, téléphone, codes postaux, n° d'assurance), obligatoires.
- **Description du site** (`_config.yml` → `description`, utilisée dans le JSON-LD et par défaut) : « menuiserie » devient « pose de placards ». Raison : règle « pas de menuiserie ».
- **`_data/realisations.yml`** n'est plus utilisé par /realisations/. Il est gardé, non supprimé, en attendant l'accord du gérant.
- **Accueil sans faux avis** : aucune citation inventée. On affiche la note réelle confirmée par le gérant (14 clients, 5/5) et un lien vers la fiche Google. Pour afficher 2 ou 3 vrais avis, le gérant doit fournir les textes, avec l'accord des clients.
- **Retirés de l'accueil** :
  - galerie et « L'Envers du Décor » (remplacés par 3 projets + la page Réalisations) ;
  - écran de chargement, curseur personnalisé, barre de progression, parallaxe (lenteur) ;
  - bandeau de chiffres « 10 ans / 24h / 100 % sur mesure » (chiffres et « sur mesure ») ;
  - blocs paiement et parrainage (remplacés par un lien Parrainage) ;
  - liste « Nos actualités » : les articles restent sur /blog/ et dans le sitemap.
- **« Menuiserie » dans `site.services`** : le libellé devient « Pose de placards ». L'URL `/services/menuiserie/` ne change pas.
- **Pas d'animation d'apparition au défilement** : elle laissait le contenu invisible pour les outils qui ne font pas défiler la page (captures, certains robots).
- **6ᵉ point « Assuré en décennale »** dans Pourquoi M&B : fait déjà présent sur le site (assureur dans `_config.yml`). À retirer si le gérant préfère seulement les 5 points demandés.
- **Photos sans texte** : les projets utilisent les originaux propres (`chantier-N.jpg`) quand ils existent ; sinon le montage, découpé sous le bandeau. Raison : un rendu « cabinet d'architecture » et la suppression des légendes contenant « sur mesure ».
- **Une seule source pour les projets** : `_data/projets.yml`. Pour ajouter un projet, ajouter une entrée puis lancer `python3 _scripts/projets.py`. Le dossier `_scripts` n'est pas publié (préfixe `_`).
- **Collections** : les photos isolées ne sont pas présentées comme un même chantier. Elles sont regroupées par thème et la carte précise « Plusieurs chantiers ». Raison : ne pas inventer de projet.
- **Photo écartée** : la vue « APRÈS » du montage carrelage, trop petite une fois la pastille retirée ; `chantier-2.jpg` montre déjà le résultat.

- **Ville des projets** : aucune ville précise n'est connue. Les cartes affichent « Paris · Île-de-France », comme sur les montages d'origine. Le champ `ville` de chaque projet est prêt pour la vraie commune, à confirmer par le gérant (voir « Restant »).

## Fait

- Étape 0 : mesure de départ, inventaire des photos, ce fichier.
- Étape 1 (testé) :
  - `_data/projets.yml` : 12 projets, dont 4 « collections » qui regroupent plusieurs chantiers du même thème.
  - `_scripts/projets.py` génère :
    - les images : `images/projets/<slug>/<n>-480|960|1600.webp` + `og.jpg`, soit 30 photos et 4,6 Mo pour toutes les tailles ;
    - les pages : `_projets/<slug>.md` ;
    - les dimensions : `_data/projets_media.yml`.
  - Les bandeaux texte (marque, légende avec « sur mesure », téléphone) et les pastilles « AVANT / APRÈS » incrustées sont retirés par découpe.
  - Les bandes noires des captures de téléphone sont rognées.
  - Vérifié à l'œil sur planches contact : plus aucun texte incrusté, aucun visage.

- Étape 2 (testé : build OK ; captures de /services/plomberie/ et /renovation/versailles/ en 390 px et 1366 px ; 0 erreur JS ; pas de débordement) :
  - `assets/css/site.css` : palette, typographie, boutons, en-tête, pied de page, contenu éditorial, cartes, projets, lightbox, fenêtre devis, barre d'action mobile.
  - `_layouts/page.html` :
    - nouveau gabarit, avec la même balise facebook-domain-verification en dur, plus consent-head et seo ;
    - option `full_width: true` pour les pages composées (accueil, réalisations, projets).
  - Nouveaux includes :
    - `site-header.html` : menu desktop, menu mobile, bouton devis ;
    - `site-footer.html` : contact, navigation, footer légal, barre « WhatsApp / Demander un devis » en bas sur mobile ;
    - `devis-modal.html` : même formulaire et mêmes champs ;
    - `site-js.html` : même envoi WhatsApp + copie n8n W2, menu, lightbox avec balayage tactile, apparition au défilement ;
    - `icon.html` : icônes SVG en ligne.
  - `bloc-paiement.html` et `bloc-parrainage.html` passent au nouveau style ; le bloc paiement n'a plus de montant ni de chiffre.

- Étape 3 (testé : build OK ; captures mobile et desktop de /realisations/ et de 2 projets ; 0 erreur JS ; pas de débordement ; test automatique lightbox ouvrir / suivant / Échap OK ; fenêtre devis ouverte depuis la barre mobile, envoi qui ouvre WhatsApp) :
  - `_config.yml` : collection `projets` (URL /realisations/<slug>/, gabarit `projet`).
  - `_layouts/projet.html` :
    - en-tête avec Travaux, Lieu et « Plusieurs chantiers » pour les collections ;
    - avant / après côte à côte ;
    - autres photos ;
    - lightbox ;
    - encart « Demander un devis » ;
    - liens précédent / suivant.
  - `_includes/projet-img.html` : `<img>` WebP avec srcset et sizes, largeur et hauteur fixées (pas de décalage de mise en page), chargement différé sauf la première image.
  - `realisations.html` : réécrit en cartes (photo, type de travaux, titre, lieu). Même URL et même title. Description sans « menuiserie sur mesure ».
  - Bug corrigé : sur mobile, la légende de la lightbox recouvrait les boutons précédent / suivant.

- Étape 4 (testé : captures mobile et desktop, 0 erreur JS, pas de débordement) — `index.html` réécrit (1 630 → environ 140 lignes), avec `layout: page` et `full_width`. Même seo_title, même description, même H1 (« Entreprise de rénovation · Paris & Île-de-France »). Sections :
  1. grande photo + une phrase (« L'exigence d'un atelier, la simplicité d'un seul interlocuteur. ») + Demander un devis / Voir nos réalisations ;
  2. Services : 6 cartes simples vers les pages services, puis Sols, Pose de placards et Tous les services ;
  3. Pourquoi M&B (fond noir) : un seul interlocuteur, devis détaillé en 48h, durée écrite, chantier propre, 14 clients ont noté 5/5 (lien vers la fiche Google), assuré en décennale ;
  4. 3 projets choisis + lien vers Réalisations ;
  5. Avis : « 14 clients ont noté M&B Rénovation 5/5 sur Google » + Lire les avis sur Google / Laisser un avis ;
  6. 4 étapes ;
  7. Demander un devis + WhatsApp, puis liens Sous-traitance et Parrainage.

- Étape 5 (testé) :
  - **SEO** :
    - les 71 pages de main existent toujours, avec les mêmes URL ;
    - titles et H1 identiques (sauf le H1 de /realisations/, « Nos réalisations ») ;
    - descriptions identiques (sauf /realisations/, sans « menuiserie sur mesure ») ;
    - 0 lien cassé, 0 doublon de title ou de description ;
    - sitemap : 83 URL (71 + 12 projets) ;
    - JSON-LD inchangé (description du site sans « menuiserie »).
  - **Navigateur (Playwright, 82 pages × 390 px et 1366 px)** :
    - 0 erreur JS, 0 débordement horizontal ;
    - menu mobile, fenêtre devis (depuis le menu, l'en-tête et la barre mobile), validation des champs et labels OK ;
    - l'envoi ouvre WhatsApp ;
    - lightbox OK.
    - Liens du pied de page agrandis pour le doigt.
  - **Mots interdits (texte visible de toutes les pages construites)** : corrigés.
    - `entreprise.md`, `services/renovation-complete.md` : « menuiserie (sur mesure) » devient « pose de placards » ; « placard sur mesure » devient « placard intégré » dans un texte alternatif.
    - Article plâtrerie/peinture : « garantit » devient « assure ».
    - Article erreurs salle de bain : « étanches à 100% » devient « totalement étanches » ; « sur-mesure » devient « personnalisé ».
    - Article appartement ancien : « menuiserie(s) » devient « pose de placards (et portes) ».
    - Évry : « menuiseries intérieures à remplacer » devient « portes intérieures à remplacer ».
  - **Photos des pages villes** :
    - les anciens montages (bandeau, légendes « sur mesure », téléphone) sont remplacés par les WebP propres via `_data/photos_remplacement.yml` ;
    - les photos exclues (visage, meubles fabriqués, reflet) ne s'affichent plus ;
    - les 34 fichiers villes ne sont pas modifiés.
  - **Photo avec reflet d'une personne** (`chantier-7.jpg`) remplacée par `chantier-13.jpg` sur /entreprise/ et /services/renovation-complete/.

## Vitesse avant / après (Lighthouse, même méthode)

| Page | Avant mobile | Après mobile | Avant ordinateur | Après ordinateur |
|---|---|---|---|---|
| / | 96, LCP 2,4 s, 204 Ko | **99, LCP 1,5 s, 91 Ko** | 99, LCP 0,6 s | **100, LCP 0,4 s** |
| /realisations/ | 100, LCP 1,5 s, 1 328 Ko | 98, LCP 2,2 s, **207 Ko** | 100, 3 230 Ko | 100, **237 Ko** |
| /services/plomberie/ | 99, LCP 2,0 s, 108 Ko | 99, LCP 2,0 s, 138 Ko | 100 | 100 |

- Étape 6 : PR brouillon n° 24 ouverte vers main, **non mergée**. Captures mobile et ordinateur envoyées au gérant.

## En cours

- Rien. **En attente de l'accord du gérant** avant tout merge.

## Restant (dans l'ordre, pour l'agent suivant)

1. Lire les réponses du gérant aux « Questions » ci-dessous et appliquer seulement ce qu'il accepte, sur `redesign-premium`, avec un commit par point.
2. Relancer les contrôles de l'étape 5 :
   - build github-pages (bundle isolé) ;
   - liens et SEO comparés à main ;
   - scan des mots interdits ;
   - Playwright mobile et ordinateur ;
   - Lighthouse.
3. Merger la PR n° 24 **uniquement** après un « oui » explicite du gérant, puis vérifier le déploiement GitHub Pages.


## Questions pour le gérant (ne bloquent pas le travail)

1. **Ville de chaque projet** : la ville réelle, s'il veut l'afficher à la place de « Paris · Île-de-France ». Modifier `ville` dans `_data/projets.yml`.
2. **Page `/services/menuiserie/`** : le title, le H1 et le texte contiennent encore « menuiserie intérieure ».
   - Proposition : renommer en « Pose de placards et portes intérieures », en gardant l'URL pour ne pas perdre le référencement.
   - Pas fait sans accord : cela change le title et le H1 d'une page indexée.
3. **« menuiseries » au sens d'éléments existants du logement** : laissé tel quel, ce n'est pas une prestation proposée. Pages concernées :
   - « protégeons les sols, les menuiseries » (Peinture) ;
   - « menuiseries extérieures » (Yvelines) ;
   - « parquets, menuiseries » (Hauts-de-Seine).
   - À remplacer si le gérant préfère.
4. **Vrais avis à afficher** : 2 ou 3 textes d'avis Google, avec prénom, pour enrichir la section Avis.
5. **6ᵉ point « Assuré en décennale »** dans Pourquoi M&B : le garder ou non.
6. **`_data/realisations.yml` et les montages `images/realisations/*.jpg`** ne sont plus utilisés par les pages. Les supprimer plus tard ? Rien n'est supprimé sans accord.

## Dernier commit

1f53ee2 (étape 5) puis le commit de cette mise à jour ; PR brouillon : https://github.com/AbdelrhmanAbdelazim/M-B-Entreprise-de-r-novation-en-le-de-France./pull/24
