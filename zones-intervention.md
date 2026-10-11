---
layout: page
title: "Zones d'intervention"
heading: "Nos zones d'intervention en Île-de-France"
seo_title: "Zones d'intervention – Rénovation en Île-de-France | M&B Rénovation"
description: "Villes où M&B Rénovation intervient pour vos travaux de rénovation : Paris, Hauts-de-Seine, Val-de-Marne, Seine-Saint-Denis et toute l'Île-de-France."
permalink: /zones-intervention/
---
**M&B Rénovation** est basée à Paris 12e et intervient dans toute l'Île-de-France : Paris, Hauts-de-Seine, Seine-Saint-Denis, Val-de-Marne, Yvelines, Essonne, Seine-et-Marne et Val-d'Oise. Voici les villes pour lesquelles nous détaillons nos services.

{% assign groupes = site.villes | group_by: "departement" | sort: "name" %}
{% for g in groupes %}
## {{ g.name }}

{% assign villes = g.items | sort: "ville" %}
{% for v in villes -%}
- [Rénovation à {{ v.ville }} ({{ v.code_postal }})]({{ v.url }})
{% endfor %}
{% endfor %}

Votre ville n'apparaît pas dans la liste ? Nous intervenons aussi ailleurs en Île-de-France : écrivez-nous sur [WhatsApp](https://wa.me/33753306559) ou à [{{ site.company.email }}](mailto:{{ site.company.email }}).
