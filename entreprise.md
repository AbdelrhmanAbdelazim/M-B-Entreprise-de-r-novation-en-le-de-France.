---
layout: page
title: "L'entreprise"
heading: "L'entreprise M&B Rénovation"
seo_title: "L'entreprise M&B Rénovation – Identité légale et garanties"
description: "Présentation de M&B Rénovation, entreprise de rénovation à Paris créée en 2023 : identité légale (EI, SIRET, RNE, TVA), assurance RC Pro et décennale Entoria / Fidelidade."
permalink: /entreprise/
redirect_from:
  - /info/
image: /chantier-7.jpg
---
{%- assign c = site.company -%}

**{{ c.brand }}** est une entreprise de rénovation intérieure tous corps d'état, créée le {{ c.founding_date_fr }} à Paris. Nous intervenons à **{{ c.area }}** : électricité, plomberie, plâtrerie, carrelage, sols, peinture, menuiserie et rénovation complète.

Notre méthode : une visite technique offerte, un devis détaillé et transparent, un chantier protégé et nettoyé chaque jour, puis une livraison accompagnée de l'attestation d'assurance décennale.

<img src="/chantier-7.jpg" alt="Pièce rénovée par M&B Rénovation à Paris : parquet neuf, murs repeints et placard intégré" width="1200" height="1600" loading="lazy" decoding="async" style="width:100%;max-height:520px;object-fit:cover;">

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

## Nos garanties

- **Assurance {{ c.insurance }}** auprès de {{ c.insurer }}, contrat n° {{ c.insurance_contract }}, couverture {{ c.insurance_coverage }}.
- **Garantie décennale** : les ouvrages réalisés sont couverts pendant 10 ans après réception des travaux. L'attestation est remise avec le devis et à la livraison.
- **Devis gratuit et détaillé**, sans engagement.
