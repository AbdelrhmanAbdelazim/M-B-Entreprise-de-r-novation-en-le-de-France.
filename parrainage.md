---
layout: page
title: "Parrainage"
heading: "Parrainage : recommandez-nous à un proche"
seo_title: "Parrainage : une remise pour vous et pour votre proche | M&B Rénovation"
description: "Recommandez M&B Rénovation à un proche : vous bénéficiez d'une remise sur votre prochain chantier, et votre proche aussi sur le sien."
permalink: /parrainage/
---
{%- assign c = site.company -%}
{%- assign parr_home = "/" -%}
{%- if site.apercu_sans_envoi -%}{%- assign parr_home = "/apercu/ac/" -%}{%- endif -%}

Vous avez été satisfait de vos travaux avec **{{ c.brand }}** ? Recommandez-nous à un proche : vous êtes récompensé tous les deux.

{% include bloc-parrainage.html %}

## Comment ça marche

1. **Vous parlez de nous** à un proche qui a un projet de rénovation en Île-de-France.
2. **Votre proche nous contacte** en indiquant votre nom dès son premier message : « Bonjour, je viens de la part de … ».
3. **Nous réalisons ses travaux**, après visite et devis détaillé gratuit. Votre proche bénéficie d'**une remise sur son chantier**.
4. **Une fois ses travaux terminés et réglés**, vous bénéficiez d'**une remise sur votre prochain chantier**.

## Conditions

- Les remises s'appliquent **une fois les travaux de votre proche terminés et réglés**.
- Le montant de la remise est précisé sur le devis.
- Votre proche doit indiquer votre nom lors de sa première prise de contact.

## Votre proche a un projet ?

Il peut nous écrire directement via notre formulaire de contact ou par e-mail :

<p><a class="btn-cta" href="{{ parr_home }}#contact" data-contact-type="contact">Contactez-nous pour un parrainage</a></p>

Ou par e-mail à [{{ c.email }}](mailto:{{ c.email }}). Voir aussi [nos réalisations](/realisations/).
