---
layout: page
title: "Mentions légales"
seo_title: "Mentions légales | M&B Rénovation"
description: "Mentions légales du site maison-mb.fr : éditeur M&B Rénovation (EI, SIRET 923 102 412 00015), directeur de publication, hébergeur GitHub Inc. et assurance décennale."
permalink: /mentions-legales/
---
{%- assign c = site.company -%}

## Éditeur du site

| Marque | {{ c.brand }} |
| Exploitant | {{ c.legal_name }} – {{ c.legal_form }} |
| SIRET | {{ c.siret }} |
| Immatriculation | {{ c.registry }} |
| Code APE | {{ c.ape }} |
| TVA intracommunautaire | {{ c.vat }} |
| Adresse | {{ c.street }}, {{ c.postal_code }} {{ c.city }} |
| Téléphone | [{{ c.phone }}](tel:{{ c.phone_raw }}) |
| E-mail | [{{ c.email }}](mailto:{{ c.email }}) |
| Date de création | {{ c.founding_date_fr }} |

**Directeur de la publication :** {{ c.publication_director }}.

## Hébergeur

Le site est hébergé par **GitHub Inc.** (service GitHub Pages), 88 Colin P Kelly Jr St, San Francisco, CA 94107, USA – [github.com](https://github.com).

## Assurance professionnelle

{{ c.brand }} est assurée en **{{ c.insurance }}** auprès de **{{ c.insurer }}**, contrat n° **{{ c.insurance_contract }}**, couverture géographique : {{ c.insurance_coverage }}.

## Médiateur de la consommation

Conformément aux articles L.611-1 et suivants du Code de la consommation, en cas de litige non résolu avec {{ c.brand }}, le client consommateur peut recourir gratuitement au médiateur suivant : **{{ c.mediator }}**, {{ c.mediator_address }} – [{{ c.mediator_url }}]({{ c.mediator_url }}). Le client doit d'abord avoir adressé une réclamation écrite à {{ c.brand }} ([{{ c.email }}](mailto:{{ c.email }})).

## Propriété intellectuelle

L'ensemble des contenus de ce site (textes, photographies de chantiers, logo et éléments graphiques) est la propriété de {{ c.brand }}, sauf mention contraire. Toute reproduction, représentation ou diffusion, totale ou partielle, sans autorisation écrite préalable est interdite.

## Données personnelles

Le traitement des données personnelles est décrit dans notre [politique de confidentialité](/confidentialite/).
