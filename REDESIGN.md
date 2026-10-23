# REDESIGN premium : journal de travail

> **Pour l'agent suivant : commence par lire ce fichier en entier.**
> - Branche : `redesign-premium`, créée depuis `main` @ `8909697` le 23/10/2026.
> - Aucun merge dans `main` sans l'accord explicite du gérant.
> - Ce fichier est exclu de la publication du site (`_config.yml` → `exclude`).


## 🟦 Reprise Devin (23/10/2026) : étape 15, branche `devin/redesign-directions`

- Session : https://app.devin.ai/sessions/edaade99f0a54c9abeda9589798b669a
- Point de départ vérifié : `redesign-premium` @ `f893f03c79c96d44ced4f3bdfdb891993e6c1473`, main @ `8909697d920da75f140e97dec29e16bc04d244f3`.
- Règles : jamais main ni `redesign-premium`, pas de force-push, pas de merge, PR n° 24 non modifiée. Contenu = main épinglé uniquement. Aucun appel réel n8n / WhatsApp.
- Rappel : le design des étapes 0 à 13 est **REFUSÉ**. Les tableaux plus bas sont un historique, pas une approbation.

| Sous-étape | Statut | Détail |
|---|---|---|
| 15a Audit 14 confirmé et complété | **TESTÉ** | `_redesign/audit/AUDIT-15.md` |
| 15b Étude directe des 5 entreprises | **TESTÉ** (observation ; Craft via archive seulement) | `_redesign/concurrents/ETUDE-CONCURRENTS.md` |
| 15c Trois directions d'accueil (390 / 1366) | restant | |
| 15d Aperçus privés, captures, comparaison de contenu, tests CTA/menu/formulaire | restant | |
| 16 Choix du gérant | **EN ATTENTE D'ACCORD** (rien d'autre ne sera fait avant) | |

### Réalisé
- 15a : site publié = main (70/70 pages HTML identiques), 0 lien ni ancre cassé, formulaire testé en interception (aucun envoi réel), axe-core : contraste (18) et liens sans nom (4) sur l'accueil de main. Détails et limites : `_redesign/audit/AUDIT-15.md`.

- 15b : 4 sites visités en direct, Craft Paris injoignable (IPv6 seulement) donc vu via Wayback (10/02/2026). Principes retenus : CTA mobile toujours visible, formulaire court tôt, entrée « professionnels » visible, preuves d'exécution en haut. Aucune donnée de conversion.

### En cours
- 15c.

### Restant (dans l'ordre)
1. 15c trois directions de la page d'accueil uniquement.
2. 15d aperçus privés + captures + tests automatiques.
3. Rapport au gérant, puis **arrêt** en attente de son choix.

### Dernier SHA poussé
- (mis à jour à chaque étape)

## 🔶 Demande n° 3 du gérant (23/10, 3ᵉ message) : PRIORITAIRE

Le design de la branche (étapes 1 à 13) est **refusé : « pas assez fastueux »**.

**Pas de merge.** La PR n° 24 reste en brouillon.

### Positionnement imposé
- M&B est une **entreprise de rénovation haut de gamme qui exécute**. Ce n'est ni un architecte, ni un décorateur, ni un concepteur.
- Le site doit rassurer deux publics :
  - le particulier ;
  - l'architecte ou le décorateur qui cherche un exécutant respectueux des plans, des finitions et des délais.
- Les boutons « Demander un devis » et WhatsApp doivent être visibles sur chaque page. Le formulaire doit être simple.

### Références
- **Luxe visuel seulement** : Pierre Yovanovitch, Joseph Dirand, Gilles & Boissier, Sarah Lavoine, dai-creation-decorateur.fr.
- **Contenu et méthode** : 5 entreprises de rénovation haut de gamme à Paris.
- Interdit : copier un texte, une photo ou un design.

### Contenu
- Contenu identique à main : textes, données, photos.
- Seuls la forme et l'ordre d'affichage changent.
- Tout nouveau texte doit être **proposé au gérant d'abord**.

### Étapes
- 14 : audit.
- 15 : 3 directions pour l'accueil (mobile et ordinateur), en aperçu privé.
- 16 : attendre le choix du gérant avant de toucher aux autres pages.

### Étape 14 : audit (testé, 23/10)

Sources de l'audit :
- **main** = le site en ligne. Commit 8909697, publié par GitHub Pages le 22/10 avec succès.
- **Branche** : 208e3a6.
- maison-mb.fr n'est pas joignable depuis la session (proxy). L'audit porte donc sur le build local de main, qui est identique au site publié.

#### Liens et SEO
- **Liens** :
  - 0 lien cassé sur main (71 pages) ;
  - 0 lien cassé sur la branche (98 pages).
- **Balises** :
  - canonical présent partout ;
  - JSON-LD présent partout ;
  - aucun title ni description en double.
- **Sitemap** :
  - 71 URL sur main, 98 sur la branche ;
  - robots.txt OK.
- **Titles trop longs** : environ 40 pages dépassent 60 caractères (jusqu'à 95), donc ils sont tronqués dans Google. C'est du contenu : on ne le change pas sans accord.
- **Accueil de main** : saut de niveaux de titres (h2 puis h4 ou h5). C'est mineur.

#### Navigateur (Playwright, 390 px et 1366 px)
- 0 erreur JS et 0 débordement horizontal, sur main comme sur la branche.

#### Formulaire (accueil seulement, dans une fenêtre)
- Fonctionnement : 4 champs avec labels, validation OK, envoi vers le webhook n8n, puis ouverture de WhatsApp.
- Le webhook (hostingersite.com) n'est pas joignable depuis la session. Il n'est donc pas testé ici.
- **Problème** : il n'y a **aucun formulaire ni aucune fenêtre devis** hors de l'accueil.

#### Boutons devis / WhatsApp
- **Problème** : sur les pages services, villes et blog (main et branche), **aucun bouton devis ni WhatsApp** n'est visible sur le 1ᵉʳ écran mobile, et il n'y a pas de bouton flottant. On trouve seulement un lien WhatsApp plus bas dans la page.
- Sur l'accueil de main : « Devis Gratuit », « Demander un devis » et le bouton flottant.

#### Icônes
- Font Awesome 6.5.1 (cdnjs) : les 22 icônes utilisées existent.
- Elles chargent environ 100 Ko de CSS et de polices pour 22 icônes. Des icônes en SVG intégré seraient plus légères.

#### Photos
- 0 image sans alt.
- Aucune image de plus de 400 Ko.
- Lazy loading : 148 images sur 161.
- short-mb.mp4 fait 2,9 Mo (non affiché sur l'accueil).

#### Mobile
- **Main, accueil** : 14 zones tactiles de moins de 24 px (liens des services, téléphone, e-mail, « Comment ça marche »).
- **Main** : écran de chargement (« loader ») masqué 1,2 s après le chargement complet. Le contenu est donc caché plus longtemps que nécessaire.
- **Main** : curseur personnalisé et parallax en JS sur l'accueil.

#### Vitesse (Lighthouse mobile, mesurée à l'étape 12, code inchangé depuis)

| Page | main | branche |
|---|---|---|
| / | 96 | 99 |
| /realisations/ | 100 | 94 |
| /services/plomberie/ | 99 | 99 |

#### Textes de main qui présentent M&B comme concepteur
Signalés au gérant, **non modifiés** :
- Accueil, grand titre : « L'Art de Sublimer Votre Intérieur ».
- Accueil, sous-titre : « … Une signature unique pour votre habitat. »
- Accueil, Méthodologie 01 : « Nous écoutons avant de concevoir. »
- Accueil, pied de page : « Nous créons des espaces qui vous ressemblent. »
- Légende de galerie : « Salles de Bains – Design & Bien-être ».

Les mentions « architectes » de main vont dans le bon sens : M&B réalise les lots de projets conçus par des architectes (Yvelines, Saint-Germain-en-Laye, sous-traitance).

#### Recherche : 5 entreprises de rénovation haut de gamme à Paris
- Entreprises étudiées : Craft Paris, Belmard Bâtiment, Costaud Rénovation, Avoltis Rénovation, Erema Bat.
- Méthode : résultats de recherche seulement, car les sites ne sont pas joignables depuis la session.
- Ce qui revient chez toutes :
  1. **Entreprise générale tous corps d'état, interlocuteur unique**, coordination des métiers et du planning.
  2. **Travail avec architectes et décorateurs**, dit clairement : exécution des plans, respect des détails et des délais.
  3. **Savoir-faire de l'ancien** : moulures, staff, parquet point de Hongrie, cheminées, immeubles haussmanniens.
  4. **Fiches projet factuelles** : lieu, surface, durée, travaux réalisés.
  5. **Preuves** : décennale, années d'expérience, avis notés, devis sous 48 h, conducteur de travaux dédié.

#### Ce que les sites de décorateurs apportent au visuel
- Grandes photos plein cadre et beaucoup de vide.
- Peu de texte, navigation discrète en petites capitales.
- Une ou deux polices maximum.
- Palette sobre, pas d'icônes ni de badges.
- Rythme lent : une idée par écran.

## ⚠️ Correction demandée par le gérant (23/10, 2ᵉ message) : PRIORITAIRE

Le gérant a demandé **uniquement le design, pas le contenu**. Règles à partir de maintenant :

1. **Tout le contenu redevient exactement celui de `main`** :
   - textes, titres et descriptions (y compris /realisations/, le bloc de paiement en plusieurs fois et ses montants) ;
   - noms de services et de pages (« Menuiserie », « sur mesure ») ;
   - textes de l'accueil d'origine, placés dans le nouveau design ;
   - choix des photos des pages villes et de /entreprise/.
2. **Ce qui reste de notre travail** :
   - le design (couleurs, polices, espacements, ordre des sections, cartes, mobile) ;
   - le déplacement des galeries photo de l'accueil vers /realisations/ et les pages projets ;
   - la lightbox ;
   - le WebP.
3. **Aperçu** : un lien temporaire en noindex (Netlify ou autre) pour voir le site sur mobile ; à défaut, des captures mobiles.
4. **Aucun merge sans accord.**

Les règles « pas de prix ni de chiffres, pas de menuiserie, pas de sur mesure » du 1ᵉʳ message s'appliquaient au nouveau contenu. Le gérant ne veut pas qu'on modifie le contenu existant. Elles ne justifient donc aucune modification de texte.

### Contenu modifié par rapport à `main` (branche `redesign-premium` @ c269b7b)

Comparaison automatique du texte visible, des textes alternatifs des images, des meta et du JSON-LD, sur les 71 pages de `main`.
**Statut : tout ce qui suit sera remis exactement comme sur `main`.**

#### A. Sur toutes les pages (en-tête, pied de page, fenêtre devis)

1. **Menu** :
   - ajout de « Professionnels », « Zones », « Accueil » (mobile) et « Demander un devis » ;
   - retrait de « Retour au site ».
2. **Pied de page** :
   - ajout d'une phrase (« Rénovation intérieure à Paris et en Île-de-France. Un seul interlocuteur… »), de « Contact / Navigation », « Avis clients », « Parrainage » et « WhatsApp » ;
   - retrait de « © 2026 M&B Rénovation. L'excellence n'est pas un acte, c'est une habitude. »
3. **Barre mobile** « WhatsApp / Demander un devis » ajoutée sur toutes les pages.
4. **Fenêtre devis** : ajoutée sur toutes les pages (avant : accueil seulement), avec des textes modifiés.
   - « Consultation Privée », « Étude de Projet », « Expertise gratuite… Aucun engagement. » deviennent « Étude de projet offerte », « Demander un devis », « … Sans engagement. » ;
   - « Nom & Prénom » devient « Nom et prénom » ; « Votre Projet » devient « Votre projet » ;
   - « Envoyer la Demande » devient « Envoyer la demande » ;
   - « Contacter via WhatsApp » devient « Écrire sur WhatsApp » ;
   - le texte de paiement « à partir de 3 000 €… en 3 fois » est remplacé par « projets éligibles, en plusieurs fois » ;
   - les placeholders (Jean Dupont, 06 00 00 00 00…) sont retirés.
5. **JSON-LD (données Google, toutes les pages)** : dans la description du site, « menuiserie » devient « pose de placards ».

#### B. Bloc « Paiement en plusieurs fois sans frais » (accueil et 8 pages services)

« Pour les projets à partir de 3 000 €, matériaux réglés à la signature, main-d'œuvre en 3 fois sans frais. » devient « Pour les projets éligibles : … en plusieurs fois sans frais. »

#### C. Nom de service « Menuiserie »

Remplacé par « Pose de placards » dans les listes de services (8 pages services, /services/, /entreprise/).

#### D. Textes de pages

- **/entreprise/** : « … peinture, menuiserie et rénovation complète » devient « … pose de placards … ». Photo `chantier-7.jpg` remplacée par `chantier-13.jpg` (page et image de partage).
- **/services/renovation-complete/** :
  - « Menuiserie intérieure sur mesure » devient « Pose de placards et de portes intérieures » ;
  - texte alternatif « placard sur mesure » devient « placard intégré » ;
  - image de partage `chantier-7.jpg` remplacée par `chantier-13.jpg`.
- **Article « Rénover un appartement ancien… »** : « Menuiseries » devient « Pose de placards et portes » ; « … peinture et menuiserie » devient « … pose de placards ».
- **Article « Plâtrerie et peinture… »** : « Cela garantit » devient « Cela assure ».
- **Article « 3 erreurs salle de bain »** : « étanches à 100% » devient « totalement étanches » ; « sur-mesure » devient « personnalisé ».
- **/renovation/evry-courcouronnes/** : « menuiseries intérieures à remplacer » devient « portes intérieures à remplacer ».
- **/parrainage/** : la flèche du lien « Comment ça marche → » est retirée.

#### E. Photos des 34 pages villes

Les photos choisies ont été remplacées par d'autres, avec d'autres textes alternatifs. Des photos ont aussi été retirées sur Neuilly, Vincennes, Paris 12, Saint-Mandé, Savigny-le-Temple, Savigny-sur-Orge, Versailles et Asnières.

#### F. /realisations/

- Description et og:description sans « menuiserie sur mesure ».
- H1 « Nos réalisations – M&B Rénovation Paris » devient « Nos réalisations ».
- Phrase d'intro réécrite.
- Sections « Avant / Après » et « Sur le chantier », avec leurs 27 photos et textes alternatifs, remplacées par 12 cartes de projets à titres et textes nouveaux.
- Photos retirées : visage, reflet, meubles « sur mesure ».
- Lien « Demander un devis » (WhatsApp) remplacé par un bouton qui ouvre la fenêtre devis.

#### G. Accueil

- **Retiré** :
  - « L'Art de Sublimer Votre Intérieur » et le sous-titre ;
  - les chiffres (10 / 24h / 100 % Projets Sur Mesure) ;
  - « Nos Compétences / Expertise Globale » et les 4 cartes avec leurs listes (Bains & Eau, Lumière & Tech, Matières & Couleurs, Sols & Structure, dont « Pose de menuiseries ») ;
  - « Découvrir nos services en détail » ;
  - Portfolio « Pièces Rénovées » ;
  - « L'Envers du Décor » ;
  - « Avant / Après – Nos réalisations » ;
  - « Méthodologie – Votre Sérénité, Étape par Étape » (Rencontre / Chiffrage / Réalisation / Garantie) ;
  - « Avantages clients » (paiement + parrainage) ;
  - « Commençons Ensemble – Votre Projet Mérite L'Excellence » ;
  - le pied de page de l'accueil (phrase, réseaux, « Contact Privé », SIRET, assurance, citation) ;
  - « Nos Actualités » (9 articles) ;
  - le menu de l'accueil (Portfolio, L'Envers du Décor, Processus, Le Blog, Devis Gratuit, téléphone).
- **Ajouté** :
  - « L'exigence d'un atelier, la simplicité d'un seul interlocuteur » ;
  - 6 cartes de services réécrites ;
  - « Pourquoi M&B » (6 points, dont « Assuré en décennale ») ;
  - « Projets choisis » ;
  - section avis « 14 clients… » ;
  - « Quatre étapes » réécrites ;
  - « Parlons de votre rénovation ».

#### H. Ajouté (nouvelles URL, pas dans `main`)

12 pages `/realisations/<projet>/`, avec des titres et descriptions écrits par moi. Elles seront gardées, mais remplies avec les textes existants (légendes des photos du gérant et textes alternatifs de `_data/realisations.yml`).

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
- **WebP des montages** (`images/realisations/webp/<nom>-480|1080.webp`, 3,8 Mo contre 7,6 Mo en JPG) : même image, sans recadrage. Raison : vitesse, sans changer le choix des photos.
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

- Étape 7 : liste des contenus modifiés envoyée au gérant (testé : comparaison automatique du texte des 71 pages, script `textdiff.py` dans le scratchpad).
- Étape 8 (testé : comparaison du texte de toutes les pages avec main → identique hors en-tête, pied de page et fenêtre devis ; JSON-LD identique sur toutes les pages) :
  - remis depuis main : `_posts`, `entreprise.md`, `services/`, `_villes`, `_departements`, avis, parrainage, sous-traitance, zones, mentions, confidentialité, blog, `_data/realisations.yml`, ainsi que `legal-footer`, `cookie-banner`, `seo` et `consent-head` ;
  - `_config.yml` : description du site et libellé « Menuiserie » remis ;
  - blocs paiement et parrainage : texte de main mot pour mot (montants et icônes compris), seul le style change ;
  - pages villes : mêmes photos et mêmes textes alternatifs que main, servies en WebP via `<picture>`, avec le JPG d'origine en secours ;
  - `_data/photos_remplacement.yml` supprimé (fichier créé par nous).
- Étape 9 (testé : texte identique à main sur 69 des 71 pages ; restent l'accueil et /realisations/) :
  - `site-header.html` : sur l'accueil (`home: true`), en-tête de main (logo, téléphone, « Devis Gratuit », menu mobile d'origine, bouton flottant) ; sur les autres pages, en-tête simple de main (Services, Réalisations, Blog, « Retour au site ») ;
  - `site-footer.html` : sur l'accueil, pied de page complet de main (réseaux, Navigation, Contact Privé, citation, « Nos Actualités ») ; ailleurs, pied simple de main ;
  - `devis-modal.html` : textes de main mot pour mot. La fenêtre n'existe que sur l'accueil, comme dans main ;
  - barre mobile « WhatsApp / Demander un devis » retirée ; mention « M&B Rénovation » retirée au-dessus des titres ;
  - lightbox seulement sur les pages qui ont `lightbox: true` ;
  - les liens Portfolio et L'Envers du Décor (menu et pied de l'accueil) pointent vers `/realisations/#portfolio` et `/realisations/#chantiers`, où ces galeries sont déplacées. Le texte des liens ne change pas.
- Étape 10 (testé : la comparaison du texte avec main ne montre que le retrait des légendes et des textes alternatifs des 3 galeries déplacées ; aucun texte ajouté) :
  - `index.html` : tous les textes de main, dans l'ordre de main ;
  - sections reprises : hero, chiffres, Nos Compétences (4 cartes), Avant / Après, Méthodologie, Avantages clients, Commençons Ensemble, puis le pied de page complet et Nos Actualités ;
  - photo du haut : même photo (`chantier-10.jpg`) en WebP, même texte alternatif ;
  - **déplacé vers /realisations/** : la galerie Portfolio « Pièces Rénovées » (3 photos et légendes) et « L'Envers du Décor – La Rigueur de la Préparation » (10 photos et légendes) ;
  - les 6 vignettes de la section Avant / Après sont retirées de l'accueil (elles sont toutes sur /realisations/). Le titre, la phrase et le bouton « Voir toutes nos réalisations » de cette section restent.
- Étape 11 (testé : comparaison du texte de toutes les pages avec main. Seuls l'accueil et /realisations/ diffèrent, et uniquement par le déplacement des galeries. 0 lien cassé, sitemap à 98 URL, soit 71 + 27 pages photo) :
  - `realisations.html` : front matter, titre, intro, sections et textes alternatifs de `_data/realisations.yml`, bouton « Demander un devis » ; tout identique à main ;
    - chaque photo (le montage d'origine, en WebP) est une carte qui ouvre `/realisations/<nom-du-fichier>/` ;
    - en bas : sections `#portfolio` (Portfolio – Pièces Rénovées) et `#chantiers` (L'Envers du Décor), déplacées depuis l'accueil avec leurs légendes exactes, dans une lightbox.
  - **27 pages photo** (`_projets/`, générées par `_scripts/projets.py`) :
    - titre et description = texte alternatif de main ; intertitre = nom de la section ;
    - photos : le montage d'origine, puis les moitiés avant / après découpées sous le bandeau, et les photos brutes quand elles existent (`DECOUPES` dans le script) ;
    - textes réutilisés de main : « Cliquez sur une photo pour l'agrandir. » et « Demander un devis » ;
    - liens précédent / suivant = titres des autres pages photo.
  - Les 12 pages projets à textes inventés (étape 3) sont supprimées. Elles n'ont jamais été publiées.
  - **Photos** :
    - `equipe-sur-le-chantier.jpg` (visage) et `chantier-7.jpg` (reflet) sont remises, car elles sont sur main ;
    - le gérant a demandé d'abord « pas de visages », puis « le même contenu que main ». **Question posée au gérant.**
  - WebP : photos brutes dans `images/webp/` (1,5 Mo), montages dans `images/realisations/webp/` (3,8 Mo), pages photo dans `images/projets/` (5,4 Mo).
- Étape 12 (testé) :
  - **Playwright** sur 97 pages × 390 px et 1366 px : 0 erreur JS, 0 débordement.
  - **Accueil** : menu mobile, fenêtre devis, validation et labels OK ; l'envoi ouvre WhatsApp.
  - **/realisations/** : lightbox (ouvrir, suivant, Échap) OK.
  - **Photos de /realisations/** : 2 colonnes dès le mobile et préchargement de la 1ʳᵉ image. Raison : avec une seule colonne, le mobile tombait à 79.
  - **Vitesse (Lighthouse, même méthode qu'avant)** :

| Page | main mobile | branche mobile | main ordinateur | branche ordinateur |
|---|---|---|---|---|
| / | 96, LCP 2,4 s, 204 Ko | **99, LCP 1,5 s, 96 Ko** | 99, LCP 0,6 s | **100, LCP 0,4 s** |
| /realisations/ | 100, LCP 1,5 s, 1 328 Ko | 94, LCP 2,9 s, **483 Ko** | 100, 3 230 Ko | 100, **461 Ko** |
| /services/plomberie/ | 99, LCP 2,0 s, 108 Ko | 99, LCP 2,1 s, 137 Ko | 100 | 100 |

  Sur /realisations/ en mobile, main affichait d'abord le texte (photos chargées plus tard), alors que la branche affiche une photo en haut. D'où un LCP un peu plus long, mais un poids divisé par 2,7.
- Étape 13 (testé) : aperçu.
  - Netlify impossible : le proxy de la session bloque api.netlify.com (« fetch failed »).
  - **Décision** : aperçu privé claude.ai (Artifact) à la place, visible seulement par le gérant : https://claude.ai/artifact/NoH6PyMMDxYb8kxARWDqLy
    - 4 pages : accueil, /realisations/, une page photo, une page service ;
    - `noindex, nofollow` ; suivi (GTM, Pixel) et webhook n8n désactivés ;
    - les icônes Font Awesome ne s'affichent pas dans l'aperçu (CDN bloqué), mais elles s'afficheront sur le vrai site.
  - Captures mobiles (390 px) des 4 pages envoyées au gérant.
  - **Statut : en attente de l'accord du gérant. Rien n'est mergé.**

## Statut actuel

| Élément | Statut |
|---|---|
| Design (couleurs, polices, espacements, cartes, mobile) | testé, **en attente d'accord** |
| Contenu | identique à main, sauf l'emplacement des galeries photo (testé) |
| Galeries déplacées vers /realisations/ + 27 pages photo | testé, **en attente d'accord** |
| Lightbox, WebP | testé, **en attente d'accord** |
| PR n° 24 (brouillon) | **non mergée** |

## Restant (dans l'ordre, pour l'agent suivant)

1. Attendre les réponses du gérant (aperçu, captures, questions ci-dessous). Appliquer seulement ce qu'il accepte, sur `redesign-premium`, avec un commit par point.
2. Après chaque modification, relancer les contrôles :
   - build github-pages (bundle isolé) ;
   - `textdiff.py` (texte identique à main) ;
   - liens et SEO ;
   - Playwright mobile et ordinateur ;
   - Lighthouse.
3. Merger la PR n° 24 **uniquement** après un « oui » explicite du gérant, puis vérifier le déploiement GitHub Pages.

## Questions pour le gérant

1. **Photos avec une personne** : `equipe-sur-le-chantier.jpg` (visage) et `chantier-7.jpg` (reflet dans un miroir).
   - Elles sont remises, car elles sont sur main.
   - Le 1ᵉʳ message demandait « pas de visages ». Les garder ou les retirer ?
2. **Vitesse /realisations/ en mobile** : 94 au lieu de 100, mais une page 2,7 fois plus légère. Acceptable ?
3. **`_data/realisations.yml`** : reste la source de /realisations/ et des 27 pages photo. Rien n'est supprimé.

## Dernier commit

Voir `git log -1` sur `redesign-premium` (commit « étape 13 »). Étape précédente : dff681b. PR brouillon : https://github.com/AbdelrhmanAbdelazim/M-B-Entreprise-de-r-novation-en-le-de-France./pull/24
