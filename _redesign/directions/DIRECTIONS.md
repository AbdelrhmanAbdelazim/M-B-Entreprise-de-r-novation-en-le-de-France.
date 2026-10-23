# Étapes 15c/15d : trois directions pour la PAGE D'ACCUEIL uniquement (23/10/2026, Devin)

Statut : **TESTÉ** puis **EN ATTENTE D'ACCORD** du gérant (aucune n'est choisie, aucune autre page touchée).

## Principe technique (n'affecte pas le site publié)
- Contenu : un seul inventaire `_data/apercu_accueil.yml`, copié mot pour mot de l'accueil de main (8909697) : textes, alt, liens. Les 3 directions lisent ce même fichier ; seules la forme et l'ordre changent.
- Pages : `_apercu/a.html`, `b.html`, `c.html` (+ `_layouts/apercu.html`, `_includes/apercu/`). Le dossier commence par `_` : **GitHub Pages ne le publie pas**. Il n'est construit qu'avec `jekyll build --config _config.yml,_config.apercu.yml`.
- Preuve : build de production avec et sans ces fichiers → sortie identique (seuls diffèrent les horodatages `site.css?v=` et `lastmod` du sitemap).
- Aperçu : pas de `consent-head` (aucun tracker GTM / Google Ads / Meta), `noindex, nofollow`, formulaire **sans envoi** (ni n8n ni WhatsApp) : message « Aperçu : envoi désactivé, aucune donnée transmise. » En production le code d'envoi serait celui de main.

## Les 3 directions
| | A · Immersive noir et or | B · Éditoriale ivoire et noir | C · Structurée, preuves d'exécution |
|---|---|---|---|
| Idée | Le luxe par la photo plein écran et l'or, proche de l'actuel mais plus calme | Magazine de décoration : fond ivoire, très grands titres, beaucoup de vide, photos encadrées | Parcours de conversion : formulaire visible dès le 1er écran, preuves et entrée « professionnels » en haut |
| 1er écran desktop | Photo plein écran, titre, 2 boutons, chiffres 10 / 24h / 100% en bas | Texte à gauche, photo verticale à droite | Texte + bloc « Professionnels du bâtiment » à gauche, formulaire à droite |
| 1er écran mobile | Photo plein écran + titre + boutons | Photo d'abord, titre ensuite | Texte, boutons, ligne pro ; formulaire juste après |
| Ordre des sections | Portfolio → Services → Envers du décor (bande défilante) → Avant/après → Méthode → Avantages → Appel final sur photo | Chiffres → Services (liste numérotée) → Portfolio (double page) → Envers du décor (mosaïque légendée) → Méthode (fond noir) → Avant/après → Avantages → Appel final | Bande de preuves (10 ans, 24h, 100%, assurance, SIRET) → Méthode → Envers du décor (grille de preuves 5×2) → Avant/après → Portfolio → Services → Avantages → Appel final |
| Pour qui en priorité | Particuliers sensibles à l'image | Particuliers + architectes/décorateurs (ton éditorial) | Architectes/décorateurs et clients qui veulent agir vite |
| Risque | Plus sombre, texte clair sur photo | Moins « coup de poing », CTA moins voyant | Moins luxueux, plus « entreprise » |

Commun aux 3 : logo M&B noir et or existant (`/logo.png`), barre fixe mobile « Demander un devis » + « WhatsApp Direct » (libellés existants de main), téléphone + WhatsApp + « Devis Gratuit » dans l'en-tête desktop, formulaire de 4 champs avec libellés, titres h1→h2→h3 sans saut.

## Écarts avec main (formes, pas de contenu nouveau) — à valider
- Ajouts d'accessibilité : lien « Aller au contenu », `aria-label` « Fermer » sur la croix, noms des icônes réseaux (Facebook, Instagram, Google, Pinterest, déjà présents sur main en `title`).
- Libellés existants répétés à d'autres endroits : « Demander un devis », « WhatsApp Direct » (barre mobile) ; en C, assurance et SIRET aussi dans la bande de preuves et la phrase « Professionnels du bâtiment… » en haut.
- Retirés car purement décoratifs : écran de chargement, curseur personnalisé, barre de progression.
- Photos servies en WebP (mêmes photos, mêmes alt).

## Contradictions de positionnement signalées (NON modifiées, le gérant décide)
- « Nous écoutons avant de concevoir » (Méthode, étape 01) : « concevoir » évoque la conception.
- « Nous créons des espaces qui vous ressemblent » (pied de page) : évoque la décoration/conception.
- « Création salles de bains luxe », « Design & Bien-être » (légende portfolio) : même remarque.
- Aucune mention d'architecte n'existe sur l'accueil de main ; rien n'a été retiré.

## Tests exécutés (fichier `directions-tests.json`, outils `_redesign/outils/`)
- Comparaison automatique avec l'accueil de main (textes du DOM, alt, liens, title, description, JSON-LD) : **0 texte de main absent, 0 alt absent, 0 lien absent, JSON-LD identique** pour A, B et C. En plus seulement : « Aller au contenu », alt du logo « M&B Rénovation », ancres `#contenu` / `#stats`. Différences d'en-tête attendues : canonical `/apercu/x/` et `noindex`.
- 390 × 844 et 1366 × 768 : 0 débordement horizontal, 0 erreur JS, 1 seul h1, 0 saut de titre.
- 1er écran : « Demander un devis » et WhatsApp visibles dans les 3 directions aux 2 largeurs ; téléphone visible sur desktop.
- Menu mobile : ouverture (aria-expanded=true) et fermeture par Échap : OK ×3.
- Formulaire : focus sur « Nom & Prénom » à l'ouverture ; envoi vide → nom, tél., projet signalés invalides ; envoi avec données synthétiques → message d'aperçu, **0 requête externe, 0 ouverture WhatsApp** (réseau intercepté).
- axe-core WCAG 2 A/AA : **0 violation** sur A, B, C aux 2 largeurs (après correction du contraste et du soulignement du lien téléphone du pied légal dans l'aperçu).
- Lighthouse : voir REDESIGN.md (même méthode que l'audit 15a).

## Limites
- Aucune donnée de conversion : aucune direction n'est garantie plus rentable.
- Lighthouse local avec polices/CDN bloqués.
- L'aperçu n'est accessible que pendant que la machine de la session Devin est active.
