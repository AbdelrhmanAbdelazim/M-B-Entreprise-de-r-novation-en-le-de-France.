# REDESIGN premium : journal de travail

> **Pour l'agent suivant : commence par lire ce fichier en entier.**
> - Branche : `redesign-premium`, créée depuis `main` @ `8909697` le 23/10/2026.
> - Aucun merge dans `main` sans l'accord explicite du gérant.
> - Ce fichier est exclu de la publication du site (`_config.yml` → `exclude`).


## 🟪 Reprise par Claude (24/10) : seul outil sur le site

**Décision du gérant (23/10, soir) : un seul outil travaille sur le site, Claude.** Devin, Codex et Antigravity **arrêtent** tout travail sur ce dépôt.
Design voulu : **le dernier travail d'Antigravity**, pas `redesign-premium`, ni l'aperçu A-C seul. **Branche de travail : `antigravity/ac-final`.**

### Étape 0 : retrouver le travail d'Antigravity : FAIT, confirmé par le gérant
- Absent de GitHub (aucune branche, aucun commit, aucune PR Antigravity).
- Trouvé sur le Mac, **non commité**, dans le worktree Codex `~/MB-Renovation/codex-ac-menu-galleries` (52 fichiers modifiés, 34 nouveaux, dernières modifications le 23/10 à 23 h 48).
- Sauvegarde :
  - branche `antigravity/ac-final` @ 0c7fd2d ;
  - copie complète : `~/MB-Renovation/backups/antigravity-worktree-20261024/` ;
  - `_redesign/preview-site/` (28 Mo de build) non commité.
- Le worktree Codex a été détaché (HEAD détaché sur 0c7fd2d) pour libérer la branche. Rien n'y a été modifié.
- Le gérant a confirmé que c'est le bon design (24/10).
- Constat : les dernières modifications d'Antigravity mettent déjà son design en **production** : l'accueil `/` utilise `_includes/apercu/ac-content.html`, et l'en-tête, le menu complet et le pied de page sont unifiés sur toutes les pages. Son propre journal (plus bas) dit encore « aperçu seulement ».

### Étape 1 : WhatsApp et formulaire : FAIT (24/10, commit 4de5722)
- `index.html` : `sans_whatsapp` retiré.
- `ac-content.html` :
  - ligne **WhatsApp** dans « Contactez-nous » (« WhatsApp Direct », texte de main) ;
  - bouton « Contacter via WhatsApp » sous le formulaire.
- `js.html` :
  - à l'envoi : ouverture de WhatsApp avec la demande pré-remplie (comme sur main) **et** copie vers n8n ;
  - message de succès sans « équipe » : « Nous vous recontactons sous 24h ouvrées ».
- `_data/apercu_accueil.yml` : sous-titre du formulaire remis comme sur main (Antigravity l'avait changé).
- n8n, côté mb-operations :
  - W2 envoie aussi un **email au gérant** ;
  - accusé client « sous 24h ouvrées » ;
  - W1 ignore les emails venant de @maison-mb.fr.
- **Test réel depuis le formulaire du nouveau site** (build local) :
  - W2 exécution 922 success : Telegram OK, email gérant accepté, accusé client accepté ;
  - WhatsApp ouvert avec nom, téléphone, email, objet et projet (2ᵉ essai, sans envoi réseau) ;
  - CORS du webhook autorisé pour https://www.maison-mb.fr ;
  - lignes de test supprimées (Clients n° 1, Queue n° 276, Journal n° 113) ; Blacklist inchangée.
- Build local : Jekyll 3.9.5 de Codex (`~/Documents/Codex/.../mb-site-build-gems`), commande `JEKYLL_NO_BUNDLER_REQUIRE=true GEM_HOME=… jekyll build`.

### Étape 2 : contenu remis comme main (24/10)
Comparaison automatique du texte visible, des textes alternatifs et des meta, sur les 71 pages, entre le build de main (8909697) et celui de la branche.
- **Antigravity avait modifié le contenu, pas seulement le design** :
  - mentions de la décennale et de l'assurance supprimées (assureur vidé dans `_config.yml`) ;
  - « Écrivez-nous sur WhatsApp » remplacé par « formulaire » ;
  - descriptions SEO des services modifiées ;
  - statistiques et étape « Garantie » de l'accueil modifiées ;
  - section « Nos garanties » de /entreprise/ réécrite ;
  - page sous-traitance cassée (« Assurance auprès de , contrat n° . ») ;
  - horaires sans « Réponse sous 24h ouvrées ».
- **Remis comme main** :
  - fichiers repris tels quels : `_config.yml` (assureur, horaires, description), services (×9), articles (×7), saint-mande, sous-traitance, zones, parrainage, confidentialité, mentions légales ;
  - fichiers où seul le texte change, design conservé : `entreprise.md` (image WebP conservée), CTA WhatsApp des gabarits service, ville, département, article et projet, `_data/apercu_accueil.yml` (copie mot pour mot de main), meta de l'accueil, phrase parrainage.
- **Écarts conservés** :
  - voulus par le gérant : le bloc « Paiement en plusieurs fois sans frais / 3 000 € » remplacé par « Paiements selon l'avancement des travaux » (décision du gérant, `_redesign/COMMERCIAL-OFFERS-REVIEW-AR.md`) ;
  - liés au design : galeries de l'accueil déplacées vers /realisations/, libellés d'en-tête, légendes visibles sur /realisations/ (= textes alternatifs de main), « Lire l'article → », lien d'évitement ;
  - **nouveaux textes d'Antigravity sur l'accueil, à valider par le gérant** : section « Pourquoi choisir M&B Rénovation ? » et « Trois entrées selon la nature de votre projet ».
- Résultat : hors accueil, plus aucune différence de contenu avec main, sauf ces écarts.

### Étape 3 : contrôle du design sur toutes les pages (24/10)
- Build de production (98 pages) :
  - **0 lien, 0 image et 0 ancre cassés** (9 062 références locales) ;
  - à 375 px : **0 débordement**, en-tête et pied A-C présents sur les **96 pages** du sitemap (hors PDF), 0 image cassée ;
  - lien WhatsApp sur 91 pages.
- Correctif /realisations/ sur mobile : les légendes couvraient la moitié des photos et leurs étiquettes « Avant / Après » ; elles sont maintenant **sous la photo**, en plus petit (`site.css`, max-width 699px).

### Étape 4 : propositions pour les phrases « concepteur » : EN ATTENTE DU GÉRANT (rien n'est modifié)
| Où | Texte actuel (main) | Proposition (exécutant) |
|---|---|---|
| Accueil, grand titre | L'Art de Sublimer / Votre Intérieur | A : « Rénover avec exigence / Livrer avec précision » · B : « L'exécution / au millimètre » |
| Accueil, sous-titre | … Une signature unique pour votre habitat. | … Un seul interlocuteur, du devis à la réception. |
| Accueil, méthode 01 | Nous écoutons avant de concevoir. | Nous visitons avant de chiffrer. |
| Pied de page | … Nous créons des espaces qui vous ressemblent. | … Nous exécutons vos travaux dans les règles de l'art, de la visite à la réception. |
| Accueil, carte services | Création salles de bains luxe | Rénovation de salles de bains haut de gamme |
| /realisations/ (légende) | Salles de Bains – Design & Bien-être | Salles de Bains – Exécution & Finitions |

**Nouveaux textes d'Antigravity sur l'accueil (absents de main), à valider** : section « Pourquoi choisir M&B Rénovation ? » (4 cartes) et « Trois entrées selon la nature de votre projet » (3 formules). Attention : le sur-titre « Votre projet sur mesure » contient « sur mesure ».

### Restant (ordre du gérant)
1. ~~Comparer le texte de toutes les pages avec main~~ (fait). et remettre le contenu de main, sauf ce que le gérant a fait retirer.
2. Vérifier et terminer le design sur toutes les pages (services, villes, départements, blog, Réalisations, pages projets, entreprise…).
3. Propositions pour les phrases « concepteur » (sans les modifier).
4. Aperçu mobile au gérant : accueil, une page service, Réalisations.
5. Après accord : contrôle complet, tag `site-avant-redesign` sur main 8909697, merge, vérification en ligne (retour au tag si gros problème).

### Reprise Antigravity demandée par le gérant — 23/10/2026
- Branche propriétaire : `codex/ac-menu-galleries` ; base et dernier commit vérifié : `5c7f2def1f2d8dcb50ab798ad7c1465e905b466a` (`main` épinglé à `8909697d920da75f140e97dec29e16bc04d244f3`).
- État : **TESTÉ EN NAVIGATEUR (WebKit natif macOS 320 / 390 / 1366 px) / EN ATTENTE D’ACCORD DU GÉRANT**, aucune fusion ni publication.
- Devin a reçu la demande mais s’est arrêté pour quota gratuit épuisé. Codex a préparé une ébauche locale puis le gérant a demandé Antigravity ; Antigravity a repris, consolidé et testé la variante `A-C`.
- Décision : conserver le hero d’inspiration (`Visuel d'inspiration`) et la palette ivoire/charbon/champagne (`A-C`), remplacer les galeries de l’accueil par deux entrées éditoriales vers les pages existantes (`/realisations/#portfolio` et `/realisations/#chantiers`) + bouton `/realisations/`, et proposer un menu complet (`<dialog id="mobileMenu">`) ivoire/charbon/champagne sur mobile et desktop sans logo ni téléphone en en-tête et sans WhatsApp. Raison : demande explicite du gérant, accès aux photos uniquement à la demande dans leurs pages dédiées.
- Fichiers et contrat de reprise : `_redesign/ANTIGRAVITY-HANDOFF-AR.md` ; référence visuelle `_redesign/references/owner-menu-reference.jpg`.
- Réalisé et consolidé par Antigravity :
  - `_apercu/ac.html` : retrait des grilles de photos d’accueil (portfolio, coulisses, avant/après) ; 1 seule balise `<img>` sur `/apercu/ac/` (le hero d’inspiration avec mention visible `Visuel d'inspiration`) ; deux cartes d’entrée éditoriales (`#portfolio` → `/realisations/#portfolio`, `#chantiers` → `/realisations/#chantiers`) et bouton `Voir toutes nos réalisations` (`/realisations/`) ;
    - **Suppression intégrale de « Contact Privé »** sur `/apercu/ac/` et les composants d’aperçu (`0` occurrence dans le DOM), tout en préservant les aperçus archivés `A / B / C` (`_data/apercu_accueil.yml` intact) et le build de production ;
    - **Unification de tous les contacts et demandes dans `#contact` (`Contactez-nous`)** : téléphone (`tel:`), e-mail (`mailto:`), réseaux sociaux (`Facebook`, `Instagram`, `Google`, `Pinterest`) et formulaire unique (`#contactForm` avec sélecteur d’objet `#c-type` et pastilles rapides `[data-type-pill]`) regroupés uniquement dans `#contact` ; suppression de la modale parallèle `#devisModal` sur `A-C` (`form_inline: true`) ; tous les CTA `Demander un devis` (`[data-devis]`), `Contactez-nous` (`[data-contact-type="contact"]`) et les boutons des formules (`[data-formule]`) ferment le menu s’il est ouvert, défilent vers `#contact`, pré-sélectionnent l’objet correspondant (`devis`, `contact`, `formule-rafraichissement`, `formule-salle-de-bains`, `formule-renovation-complete`) et placent le focus dans le formulaire ;
    - **Ajout de la section `Pourquoi choisir M&B Rénovation ?` (`#pourquoi`)** : 4 cartes éditoriales avec icônes `<svg>` intégrées (`Un interlocuteur unique`, `Devis détaillé, poste par poste`, `Protection & préparation du chantier`, `Chantiers & réalisations consultables`), sans chiffres de succès, sans notes ni témoignages, sans promesse de délai nouvelle ni revendication d’architecte, avec liens directs vers `/realisations/`, `/realisations/#chantiers` et `#processus` ;
    - **Ajout de la section d’entrées de projets (`#formules` — `Trois entrées selon la nature de votre projet`)** : décision finale du gérant (« الباقات والأقساط التحديد بعد المعاينة » / « تمام اعمل كده ») : 3 cartes d’entrées de projets (et non des forfaits à prix ou périmètre figés) fondées exclusivement sur les services réels :
      1. `Rafraîchissement intérieur` (`Peinture, finitions et sols selon les besoins`),
      2. `Rénovation de salle de bains` (`Périmètre défini après examen des lieux`),
      3. `Rénovation complète` (`Coordination et réalisation des étapes de rénovation`),
      chacune avec une phrase « Pour qui », la liste des travaux possibles dans les services existants, et le bouton `Parlons de votre projet` orientant vers `#contact` en pré-sélectionnant le projet correspondant sans envoi ;
    - **Harmonisation de `#avantages` (`Paiement par étapes & parrainage`) et de la note du formulaire `#contactForm`** selon la décision finale du gérant :
      - Formule de référence unifiée : *« Le périmètre des travaux, le prix et l’échéancier des paiements par étapes sont définis après la visite technique et précisés dans votre devis détaillé. »* ;
      - Utilisation de `Paiement par étapes` / `Paiements selon l’avancement des travaux` (aucun pourcentage, aucun montant minimum, aucun nombre fixe d’échéances, retrait total de `3 000 € / 3 fois / sans frais` sur `A-C` tout en gardant `_data/apercu_accueil.yml` intact pour `A / B / C`) ;
      - Remise fondée uniquement sur le programme existant `Parrainage` avec ses conditions d’origine (`/parrainage/` : montant précisé sur le devis et appliqué une fois les travaux du proche terminés et réglés, sans remise en pourcentage ni offre inventée). Décision documentée dans `_redesign/COMMERCIAL-OFFERS-REVIEW-AR.md`.
  - `_includes/apercu/ac-menu.html` : `<dialog class="full-menu" id="mobileMenu">` avec tous les vrais liens du site (Accueil, Pourquoi M&B `#pourquoi`, Nos formules `#formules`, Portfolio, L’Envers du Décor, Processus, Réalisations, Le Blog, `<details>` Nos Services avec les 8 services réels, `<details>` Zones d’intervention avec Paris & Île-de-France + les 8 départements `75` à `95`, L’entreprise, Sous-traitance, Donner mon avis, Parrainage, Modalités de paiement `#avantages`, lien dédié `Contactez-nous` vers `/apercu/ac/#contact`, bouton champagne `Demander un devis` orientant vers `#contact` en mode `devis`, Mentions légales, Confidentialité, Voir notre fiche Google), sans bloc `Contact Privé` ni répétition de téléphone/e-mail/réseaux dans le menu.
  - `_includes/apercu/social.html`, `_includes/site-footer.html` & `_includes/legal-footer.html` : restauration des 4 profils sociaux authentiques (`Facebook`, `Instagram`, `Google`, `Pinterest`) avec icônes `<svg>` intégrées uniquement dans `#contact` sur `A-C` ; dans `_includes/site-footer.html` et `_includes/legal-footer.html`, les changements d’aperçu (retrait de `Contact Privé` et redirection vers `/apercu/ac/#contact` tout en conservant l’adresse, le SIRET et l’assurance) sont strictement isolés derrière `site.apercu_sans_envoi` (et `page.direction != "a"/"b"/"c"`) afin que le build de production et les aperçus `A/B/C` restent 100 % identiques à l’origine.
  - `realisations.html` & `_includes/site-header.html` : strictement isolés derrière `{%- if site.apercu_sans_envoi %}` (`assets/css/site.css`, `_includes/webp-img.html` et `_includes/site-js.html` sont laissés 100 % intacts à l’état d’origine, y compris `<img alt="">` de `#lightbox`). En mode aperçu (`site.apercu_sans_envoi`), ajout de la barre de filtres rapides (`.real-filter-nav`) vers les 5 sections (`#avant-apres`, `#realisations-terminees`, `#sur-le-chantier`, `#portfolio`, `#chantiers`), des légendes visibles sur les 27 cartes de projets, du chargement `eager` des 40 vraies photos de projets/chantiers, et d’un en-tête compact sans débordement à `320px` (`0px` overflow) : **40/40 vraies photos de projets chargées (`complete && naturalWidth > 0`) + 1 image `#lightbox img` chargée au clic (41 balises `<img>` au total)**.
  - `_includes/apercu/ac.css` : centrage exact du glyphe `×` dans `.full-menu-close` ; styles de la section `#contact` (`.contact-sec`, `.contact-grid`, `.contact-card`) et des blocs sociaux du menu (`.full-menu-socials`) ; règle responsive `@media (max-width: 360px)` garantissant `0px` de débordement horizontal à `320px` tout en conservant des cibles tactiles `>= 44px`.
  - `_includes/apercu/js.html` : isolation complète via `{% if page.detailed_menu %}` (les aperçus `A`, `B`, `C` restent intacts) ; gestion de `body.no-scroll` + attribut `inert` (`syncInert()`) ; piège de focus clavier `Tab` / `Shift+Tab` dynamique dans `#mobileMenu` ; restauration fiable du focus vers `#menuBtn` ; prise en charge du formulaire `#contactForm` (désactivé en aperçu sans aucun envoi réseau).
  - `_redesign/outils/check-ac-menu.py` : script de vérification structurelle enrichi (contrôle des 40 vraies photos de projets/galeries sur disque + 1 balise `#lightbox img` = 41 `<img>`, de `#contact`, de `Contactez-nous`, et des 4 réseaux sociaux).
- Vérifications et tests exécutés (en sandbox strict `BypassSandbox: false`) :
  1. **Builds isolés hors dépôt** (via Ruby 2.6 stdlib compatible Liquid/Kramdown/YAML sans modifier macOS) :
     - Build d’aperçu (`_config.yml,_config.apercu.yml`, `apercu_sans_envoi: true`) dans `/tmp/mb-preview-build` (102 pages HTML).
     - Build de production (`_config.yml`) dans `/tmp/mb-prod-build` (97 pages HTML) : **0 fichier** issu de `apercu`, `_apercu`, `_redesign` ou `REDESIGN.md`, et **`diff -rq` = 0 différence octet par octet** par rapport au build de production de référence avant nos modifications.
  2. **Contrôle automatisé `python3 _redesign/outils/check-ac-menu.py`** : **OK** (`homepage_images: 1`, `local_links_and_anchors_checked: 79`, `gallery_total_img_tags: 41`, `gallery_real_project_photos_verified_on_disk: 40`, `lightbox_placeholder_img: 1`, `original_previews_preserved: ["a", "b", "c"]`, `preview_form: "disabled"`, `0` référence WhatsApp dans `/apercu/ac/`).
  3. **Contrôle global des liens et ancres `python3 _redesign/outils/links.py`** : **0 lien cassé (`0 []`), 0 ancre cassée (`0 []`)** sur le build d’aperçu et le build de production (et note de vérification Codex reçue : build Jekyll 3.9.5 réel validé sur snapshot isolé avant les correctifs Contact/Social/Gallery avec 103 pages preview / 98 pages prod, 3906 et 3398 références `srcset` incluses vérifiées sans lien ni ancre cassés dans `/Users/abdo/Documents/Codex/2026-10-22/macbook-pro-15-2015-intel-i7/outputs/mb-site-verification/` ; un build final Jekyll 3.9.5 sera relancé après livraison des correctifs Contact/Social/Gallery).
  4. **Validation syntaxique JS (`node --check`) et tests DOM / clavier / formulaire** :
     - `0` erreur de syntaxe sur les `<script>` rendus de `ac`, `a`, `b`, `c`.
     - Ouverture du menu (`showModal`), `aria-expanded="true"`, `body.no-scroll`, `inert` sur l’arrière-plan, cycle `Tab` / `Shift+Tab` sur 16 contrôles (details fermés) puis 34 contrôles (details Services + Zones ouverts), fermeture par `Escape` et restauration du focus sur `#menuBtn`.
     - Transition `Menu` → `Demander un devis` (`#devisModal`) : fermeture du menu, ouverture de la modale avec maintien de `body.no-scroll` et `inert`, focus sur `#d-nom`, refus des champs vides, soumission synthétique avec `test@example.invalid` / `0600000000` affichant `Aperçu : envoi désactivé (aucune donnée transmise).`, `0` appel réseau (`fetch`), `0` `window.open`, fermeture par `Escape` restaurant le focus sur `#menuBtn`.
  5. **Tests navigateur réels (WebKit natif macOS `320x568`, `390x844`, `1366x768`) et captures** :
     - `0px` de débordement horizontal sur l’accueil et dans le menu ouvert à `320px`, `390px` et `1366px`.
     - En-tête : `0` logo, `0` téléphone ; `#menuBtn` (`>= 89×44 px`) et `.head-devis` (`>= 151×44 px`, fond champagne `rgb(201, 178, 124)`, texte charbon `rgb(28, 30, 34)`) visibles sur mobile et desktop.
     - Cibles tactiles : `0` cible `< 24px` sur la page, `0` cible `< 44px` dans le menu ouvert ; défilement complet du menu vérifié (`scrollHeight: 1928px` sur mobile, `1524px` sur desktop).
     - Captures enregistrées dans `_redesign/directions/ac/captures/apercu_ac-{320,390,1366}-{accueil,realisations,menu,menu-details}.jpg`.
- Limites connues à communiquer au gérant :
  1. **Périmètre `A-C` uniquement** : les pages de destination ouvertes depuis le menu (`/realisations/`, pages services, zones, entreprise, blog, etc.) conservent leur habillage actuel tant que le gérant n’a pas validé l’application globale de la direction `A-C`.
  2. **aperçu local (`noindex` ≠ privé)** : les fichiers locaux ou un serveur `localhost` ne sont accessibles que sur ce Mac.
  3. **Commit / push Git depuis le sandbox** : ce dossier est un worktree Git dont les métadonnées résident dans `/Users/abdo/MB-Renovation/site/.git/worktrees/codex-ac-menu-galleries` (hors du périmètre d’écriture du sandbox strict `/Users/abdo/MB-Renovation/codex-ac-menu-galleries`). Les fichiers sont prêts et vérifiés dans l’arbre de travail ; la commande `git commit` / `git push origin codex/ac-menu-galleries` doit être exécutée dans le terminal du Mac par le gérant (ou après ouverture des droits sur `/Users/abdo/MB-Renovation/site/.git`).
- Restant dans l’ordre : exécuter le commit/push sur `codex/ac-menu-galleries`, recueillir l’avis du gérant sur `A-C`, puis seulement après validation explicite, décliner sur les autres pages.

## 🟦 Reprise Devin (23/10/2026) : étape 15, branche `devin/redesign-directions`

- Session : https://app.devin.ai/sessions/edaade99f0a54c9abeda9589798b669a
- Point de départ vérifié : `redesign-premium` @ `f893f03c79c96d44ced4f3bdfdb891993e6c1473`, main @ `8909697d920da75f140e97dec29e16bc04d244f3`.
- Règles : jamais main ni `redesign-premium`, pas de force-push, pas de merge, PR n° 24 non modifiée. Contenu = main épinglé uniquement. Aucun appel réel n8n / WhatsApp.
- Rappel : le design des étapes 0 à 13 est **REFUSÉ**. Les tableaux plus bas sont un historique, pas une approbation.

| Sous-étape | Statut | Détail |
|---|---|---|
| 15a Audit 14 confirmé et complété | **TESTÉ** | `_redesign/audit/AUDIT-15.md` |
| 15b Étude directe des 5 entreprises | **TESTÉ** (observation ; Craft via archive seulement) | `_redesign/concurrents/ETUDE-CONCURRENTS.md` |
| 15c Trois directions d'accueil (390 / 1366) | **TESTÉ** | `_redesign/directions/DIRECTIONS.md`, captures v1 conservées dans `_redesign/directions/v1/captures/` |
| 15d Aperçus privés, captures, comparaison de contenu, tests CTA/menu/formulaire | **TESTÉ** | `_redesign/directions/v1/directions-tests.json` |
| 16 Choix du gérant | **CHOIX REÇU** (23/10) : composition A + couleurs C, sans WhatsApp, image d'inspiration en hero | voir 17 |
| 17a Variante A-C (aperçu seulement), retrait WhatsApp, palette ivoire/charbon/or retenu | **TESTÉ** (hero provisoire sans image) | `_apercu/ac.html`, `_includes/apercu/ac.css`, `_redesign/directions/ac-tests.json`, captures `_redesign/directions/ac/captures-attente/` |
| 17b Image d'inspiration en hero | **TESTÉ** | `_redesign/inspiration/PROVENANCE.md`, captures finales `_redesign/directions/ac/captures/`, tests `_redesign/directions/ac-tests.json` |
| 17c Choix final sur la variante A-C | **EN ATTENTE D'ACCORD** | |

### Réalisé
- 15a : site publié = main (70/70 pages HTML identiques), 0 lien ni ancre cassé, formulaire testé en interception (aucun envoi réel), axe-core : contraste (18) et liens sans nom (4) sur l'accueil de main. Détails et limites : `_redesign/audit/AUDIT-15.md`.

- 15b : 4 sites visités en direct, Craft Paris injoignable (IPv6 seulement) donc vu via Wayback (10/02/2026). Principes retenus : CTA mobile toujours visible, formulaire court tôt, entrée « professionnels » visible, preuves d'exécution en haut. Aucune donnée de conversion.

- 15c/15d : directions A (immersive noir et or), B (éditoriale ivoire et noir), C (structurée, preuves d'exécution), accueil seulement, dans `_apercu/` (non publié par GitHub Pages ; build de production prouvé identique). Contenu = `_data/apercu_accueil.yml` copié de main : 0 texte, 0 alt, 0 lien de main absent, JSON-LD identique. axe : 0 violation. Formulaire : 0 requête externe.
- Lighthouse 12.2.1 (local, polices/CDN bloqués) : A, B, C mobile perf 99, a11y 100, bonnes pratiques 100, LCP 1,7 s, CLS 0 (153 / 103 / 106 Ko) ; desktop perf 100, LCP 0,5 s. SEO 69 = effet voulu du `noindex` de l'aperçu (main : 100).
- Aperçu privé : port local 4100 de la machine Devin exposé par l'aperçu Devin (connexion + droit d'écriture sur la session exigés) ; disponible seulement quand la machine est active. Captures permanentes dans le dépôt.
- Contradictions signalées, non modifiées : « Nous écoutons avant de concevoir », « Nous créons des espaces qui vous ressemblent », « Création salles de bains luxe », « Design & Bien-être ».

- 17a (décision du gérant, 23/10, prioritaire sur le perfectionnement de A/B/C) :
  - Périmètre autorisé : **nouvelle preview seulement** `/apercu/ac/`. Pas de merge, pas d'accueil réel, pas de main, pas de n8n, pas de publication.
  - A, B, C historiques conservés tels quels (le perfectionnement v2 commencé a été abandonné, non commité). Captures v1 déplacées dans `_redesign/directions/v1/`.
  - Composition A (plein cadre, texte en bas à gauche, chiffres en pied de hero, portfolio, bande de chantiers, réalisations, processus, avantages, CTA) ; couleurs C : blanc / pierre #F4F1EB / ivoire #F7F4EE / charbon #1C1E22, or retenu #A88A4E (texte #7A5E26). Plus de boutons dorés : boutons charbon ou ivoire. Voile du hero limité à la moitié gauche (plus de voile noir plein).
  - **WhatsApp retiré de cette variante uniquement** (drapeau de page `sans_whatsapp`) : en-tête, barre mobile (devis seul), CTA final, lien sous le formulaire, ouverture `wa.me` après soumission. A/B/C inchangés.
  - « Demander un devis » et formulaire conservés, en mode aperçu sans envoi.
  - Photo hero actuelle (chantier-10 + son alt) supprimée de cette variante, à la demande du gérant. La photo décorative du CTA final de A est aussi retirée (fond charbon uni).
  - Image hero : emplacement prêt (`hero_inspiration` dans l'en-tête de `_apercu/ac.html`). Elle portera la mention « Image d'inspiration » et n'ira jamais dans le portfolio ou les chantiers.
- Tests 17a (390 et 1366, réseau externe bloqué) : 0 débordement, 0 erreur JS, 1 h1, 0 saut de titre, menu ouvert puis fermé par Échap, focus sur « nom » à l'ouverture du devis, champs vides refusés (nom, tel, projet), envoi synthétique : statut « envoi désactivé », 0 requête externe, 0 `window.open`, 0 popup ; 0 lien wa.me, 0 icône WhatsApp ; axe-core wcag2a/aa : 0 violation (ce n'est pas une conformité globale).
- Écarts de contenu avec main, **voulus par la décision du gérant** : absents « Contacter via WhatsApp », « WhatsApp Direct », lien `https://wa.me/33753306559`, alt de la photo hero chantier-10. JSON-LD identique.
- À valider par le gérant (non modifié, contenu de main) : le sous-titre du formulaire dit encore « Réponse écrite sous 24h ouvrées (WhatsApp ou e-mail) ». Nouveau texte ajouté pour la seule image d'inspiration : « Image d'inspiration ».

- 17b (23/10) : visuel d'inspiration généré fourni par Codex intégré au hero A-C (`<picture>` AVIF + WebP, 640 à 1672 px, mention « Visuel d'inspiration », alt descriptif sans attribution à M&B). Portfolio réel intact. Desktop : image plein cadre, voile charbon limité à la moitié gauche et au pied. Mobile : image 16/10 au-dessus du texte (sujet non coupé, titre jamais sur la photo). Provenance : `_redesign/inspiration/PROVENANCE.md`.
  - Sous-titre de la fenêtre devis, **dans A-C seulement** : « (WhatsApp ou e-mail) » retiré pour respecter « 0 texte WhatsApp visible » ; aucun mot ajouté. Réversible, à confirmer par le gérant.
  - Tests refaits après intégration (390 et 1366, réseau externe bloqué) : 0 débordement, 0 erreur JS, 1 h1, 0 saut de titre ; menu ouvert/fermé par Échap ; clavier : lien d'évitement puis navigation, focus sur « nom » à l'ouverture du devis ; reduced-motion : défilement `auto`, transitions 0 s ; champs vides refusés ; envoi synthétique « envoi désactivé », 0 requête externe, 0 `window.open`, 0 popup ; **0 `wa.me` / `fa-whatsapp` dans le HTML rendu, 0 texte WhatsApp visible (fenêtre devis ouverte incluse)** ; axe wcag2a/aa : 0 violation (pas une conformité globale).
  - Lighthouse 12 (local) : mobile perf 98, a11y 100, BP 100, LCP 2,0 s, CLS 0,017, 563 Ko ; desktop perf 99, LCP 0,8 s. SEO 69 = `noindex` voulu de l'aperçu.
  - Écarts de contenu avec main (voulus) : textes WhatsApp, lien wa.me, alt hero chantier-10, sous-titre devis sans « (WhatsApp ou e-mail) » ; ajouts « Visuel d'inspiration » et son alt. JSON-LD identique.
  - Comparaison avec v1 au même viewport : `_redesign/directions/ac/captures/comparaison-v1A-vs-AC-{390,1366}.jpg`.

- 17c (ajustement du gérant, 23/10, **en-tête A-C uniquement**) :
  - Logo supprimé de l'en-tête (pas remplacé par un texte) ; numéro de téléphone supprimé de l'en-tête. Footer inchangé (logo texte, téléphone, coordonnées légales conservés).
  - Bouton d'en-tête : libellé « Devis Gratuit » remplacé par le libellé existant de main « Demander un devis » (`hero.btn`) ; couleur champagne retenue #C9B27C, texte charbon #1C1E22 (contraste 8,06:1), bordure #A88A4E ; survol #D8C59A (9,83:1) ; focus : contour charbon 2 px ; hauteur 44 px (390 et 1366).
  - Rééquilibrage : desktop, navigation alignée à gauche (48 px) et bouton à droite ; mobile, hamburger à gauche (44 × 44) et bouton devis à droite, donc plus de trou. La barre mobile fixe est masquée sur A-C, car l'en-tête fixe porte déjà le bouton devis (évite trois boutons identiques). Le bouton « Devis Gratuit » du menu plein écran mobile (include commun) n'est pas modifié.
  - Tests (390 et 1366) : 0 logo, 0 lien tel, 0 numéro dans l'en-tête ; navigation et hamburger accessibles ; Entrée sur le bouton ouvre la fenêtre devis, focus sur « nom », Échap la ferme et rend le focus au bouton ; tabulation : lien d'évitement, navigation, bouton devis ; 0 débordement, 0 erreur JS, axe 0 violation ; WhatsApp : 0 lien, 0 icône, 0 texte visible, 0 `window.open` ; formulaire : envoi désactivé, 0 requête externe. Résultats : `_redesign/directions/ac-tests.json`, `ac-header-tests.json`.
  - Captures : `ac/captures/apercu_ac-{390,1366}-*.jpg`, comparaison avant/après de l'en-tête `ac/captures/comparaison-entete-avant-apres-{390,1366}.jpg`, comparaison avec v1 A `comparaison-v1A-vs-AC-{390,1366}.jpg`.

### En cours
- 17d : **EN ATTENTE DE REVUE** du gérant sur la variante A-C. Rien d'autre (pas de merge, pas d'accueil réel, pas de publication).

### Restant (dans l'ordre)
1. Accord du gérant sur A-C ; décisions sur les phrases signalées et sur le sous-titre devis sans « WhatsApp ou e-mail ».
2. Seulement ensuite : appliquer la direction choisie à l'accueil réel, puis aux autres pages, avec son accord.

### Dernier SHA poussé
- 15a 444ed67, 15b 2e6b04d, 15c/15d 465e1a6d7afea219179669d32aecd63db4a66a85, 15 final 62e9a4d, 17a 8972214, 17b 81ec82c00b9f28540c67e13e0e740de64c3dbd40, 17c : voir `git log -1` (commit « Étape 17c »)

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
