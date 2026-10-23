---
layout: page
title: "Nos services"
heading: "Nos services de rénovation"
seo_title: "Services de rénovation à Paris et en Île-de-France | M&B Rénovation"
description: "Les services de M&B Rénovation à Paris et en Île-de-France : électricité, plomberie, plâtrerie, carrelage, sols, peinture, menuiserie et rénovation complète."
permalink: /services/
---
{%- assign si_home = "/" -%}
{%- if site.apercu_sans_envoi -%}{%- assign si_home = "/apercu/ac/" -%}{%- endif -%}
**M&B Rénovation** intervient en rénovation intérieure tous corps d'état à {{ site.company.area }}. Découvrez chacun de nos métiers :

{% for s in site.services -%}
- [{{ s.title }}]({{ s.url }})
{% endfor %}

Pour un devis gratuit, écrivez-nous via notre formulaire [Contactez-nous]({{ si_home }}#contact), au [{{ site.company.phone }}](tel:{{ site.company.phone_raw }}) ou par e-mail à [{{ site.company.email }}](mailto:{{ site.company.email }}).
