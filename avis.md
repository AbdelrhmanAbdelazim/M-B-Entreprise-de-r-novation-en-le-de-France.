---
layout: page
title: "Laissez-nous un avis"
heading: "Merci pour votre confiance"
description: "Vous avez confié vos travaux à M&B Rénovation ? Merci ! Partagez votre expérience en laissant un avis sur notre fiche Google."
permalink: /avis/
---
{%- assign avis_url = site.social.google_business -%}
Merci d'avoir confié vos travaux à **M&B Rénovation**. Votre avis compte beaucoup : il aide d'autres particuliers à nous faire confiance.

Vous allez être redirigé vers notre fiche Google dans quelques secondes. Cliquez sur « Avis » puis « Rédiger un avis ».

<p><a class="btn-cta" id="avis-lien" href="{{ avis_url }}" rel="noopener"><i class="fa-brands fa-google"></i>&nbsp; Donner mon avis sur Google</a></p>

Si la redirection ne se fait pas, utilisez le bouton ci-dessus.

<script>
    setTimeout(function () { window.location.href = document.getElementById('avis-lien').href; }, 4000);
</script>
