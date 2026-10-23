---
layout: page
title: "Laissez-nous un avis"
heading: "Merci pour votre confiance"
description: "Vous avez confié vos travaux à M&B Rénovation ? Merci ! Partagez votre expérience en laissant un avis sur notre fiche Google."
permalink: /avis/
---
{%- assign avis_url = site.social.google_avis | default: site.social.google_business -%}
Merci d'avoir confié vos travaux à **M&B Rénovation**. Votre avis compte beaucoup : il aide d'autres particuliers à nous faire confiance.

Vous allez être redirigé vers notre fiche Google dans quelques secondes. Le formulaire d’avis Google s’ouvre directement.

<p><a class="btn-cta" id="avis-lien" href="{{ avis_url }}" rel="noopener"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.8 10.2h-9.6v3.8h5.5c-.4 2.1-2.2 3.6-5.5 3.6-3.4 0-6.2-2.8-6.2-6.2s2.8-6.2 6.2-6.2c1.6 0 3 .6 4.1 1.6l2.9-2.9C17.4 2.2 14.9 1.2 12.2 1.2 6.2 1.2 1.4 6 1.4 12s4.8 10.8 10.8 10.8c5.6 0 10.3-4 10.3-10.6 0-.7-.1-1.4-.2-2z"/></svg>&nbsp; Donner mon avis sur Google</a></p>

Si la redirection ne se fait pas, utilisez le bouton ci-dessus.

<script>
    setTimeout(function () { window.location.href = document.getElementById('avis-lien').href; }, 4000);
</script>
