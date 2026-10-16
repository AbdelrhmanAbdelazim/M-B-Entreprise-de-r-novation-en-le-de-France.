---
layout: page
title: "Parrainage"
heading: "Parrainage : recommandez-nous à un proche"
seo_title: "Parrainage – 100 € pour vous, 50 € pour votre proche | M&B Rénovation"
description: "Recommandez M&B Rénovation à un proche : vous recevez 100 € et votre proche 50 € de remise sur son devis, pour des travaux à partir de 3 000 €."
permalink: /parrainage/
---
{%- assign c = site.company -%}
{%- capture wa_parrain -%}Bonjour, je viens de la part de … {%- endcapture -%}

Vous avez été satisfait de vos travaux avec **{{ c.brand }}** ? Recommandez-nous à un proche : vous êtes récompensé tous les deux.

{% include bloc-parrainage.html %}

## Comment ça marche

1. **Vous parlez de nous** à un proche qui a un projet de rénovation en Île-de-France.
2. **Votre proche nous contacte** sur WhatsApp en indiquant votre nom : « Bonjour, je viens de la part de … ».
3. **Nous réalisons ses travaux**, après visite et devis détaillé gratuit. Votre proche bénéficie de **50 € de remise sur son devis**.
4. **Une fois les travaux terminés et réglés**, vous recevez **100 €**, sous forme de remise sur vos prochains travaux ou de carte cadeau, au choix.

## Conditions

- Offre valable pour des travaux à partir de **3 000 €**.
- La récompense est versée **une fois les travaux terminés et réglés**.
- Votre proche doit indiquer votre nom lors de sa première prise de contact.

## Votre proche a un projet ?

Il peut nous écrire directement sur WhatsApp avec ce message prérempli :

<p><a class="btn-cta" href="https://wa.me/{{ c.phone_raw | remove: '+' }}?text={{ wa_parrain | uri_escape | replace: '&', '%26' }}" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp"></i>&nbsp; Bonjour, je viens de la part de …</a></p>

Ou par e-mail à [{{ c.email }}](mailto:{{ c.email }}). Voir aussi [nos réalisations](/realisations/).
