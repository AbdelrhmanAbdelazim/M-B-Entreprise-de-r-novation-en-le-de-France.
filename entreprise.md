---
layout: page
title: "L'entreprise"
heading: "L'entreprise M&B Rénovation"
seo_title: "L'entreprise M&B Rénovation – Identité légale et engagements"
description: "Présentation de M&B Rénovation, entreprise de rénovation à Paris créée en 2023 : identité légale (EI, SIRET, RNE, TVA), démarche qualité et devis gratuit sur mesure."
permalink: /entreprise/
redirect_from:
  - /info/
image: /chantier-7.jpg
---
{%- assign c = site.company -%}

**{{ c.brand }}** est une entreprise de rénovation intérieure tous corps d'état, créée le {{ c.founding_date_fr }} à Paris. Nous intervenons à **{{ c.area }}** : électricité, plomberie, plâtrerie, carrelage, sols, peinture, menuiserie et rénovation complète.

Notre méthode : une visite technique offerte, un devis détaillé et transparent, un chantier protégé et nettoyé chaque jour, puis une livraison soignée avec contrôle des finitions.

{% include webp-img.html key="chantier-7.jpg" alt="Pièce rénovée par M&B Rénovation à Paris : parquet neuf, murs repeints et placard intégré" sizes="(min-width: 820px) 740px, 92vw" %}

## Nos services

{% for s in site.services -%}
- [{{ s.title }}]({{ s.url }})
{% endfor %}

## Identité légale

| Marque | {{ c.brand }} |
| Exploitant | {{ c.legal_name }} – {{ c.legal_form }} |
| SIRET | {{ c.siret }} |
| Immatriculation | {{ c.registry }} |
| Code APE | {{ c.ape }} |
| TVA intracommunautaire | {{ c.vat }} |
| Adresse | {{ c.street }}, {{ c.postal_code }} {{ c.city }} |
| Date de création | {{ c.founding_date_fr }} |
| Zone d'intervention | {{ c.area }} |
| Horaires | {{ c.hours }} |
| Téléphone | [{{ c.phone }}](tel:{{ c.phone_raw }}) |
| E-mail | [{{ c.email }}](mailto:{{ c.email }}) |

Ces informations sont vérifiables sur la fiche officielle de l'entreprise : [Annuaire des Entreprises (data.gouv.fr)]({{ c.annuaire_url }}).

[Voir notre fiche Google]({{ site.social.google_business }}){:target="_blank" rel="noopener"}

## Nos engagements

- **Visite technique préalable et devis détaillé**, sans engagement et transparent poste par poste.
- **Réalisation dans les règles de l'art** avec protection des lieux et propreté quotidienne du chantier.
- **Médiateur de la consommation** : {{ c.mediator_short }} (adhésion enregistrée, valable jusqu'au {{ c.mediator_valid_until }}).
{% if c.insurer and c.insurer != "" %}
- **Assurance {{ c.insurance }}** auprès de {{ c.insurer }}, contrat n° {{ c.insurance_contract }}, couverture {{ c.insurance_coverage }}.
{% endif %}

## Plaquette de présentation

Téléchargez notre plaquette de présentation au format PDF (environ 380 Ko) : [Plaquette M&B Rénovation (PDF)](/plaquette.pdf){:target="_blank" rel="noopener"}
