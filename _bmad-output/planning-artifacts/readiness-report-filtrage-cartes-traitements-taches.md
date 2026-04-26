---
title: 'Implementation Readiness Report - Filtrage des cartes par traitements et taches'
slug: 'readiness-report-filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'ready-for-sprint-planning-with-concerns'
source_prd: '_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
workflow: 'bmad-check-implementation-readiness'
agent: 'architect'
verdict: 'GO_WITH_CONCERNS'
---

# Implementation Readiness Report - Filtrage des cartes par traitements et taches

## 1. Verdict

**GO WITH CONCERNS** : le projet est pret pour le sprint planning et l'implementation, a condition de traiter explicitement les points de vigilance ci-dessous pendant les stories.

Aucun blocage de fond n'a ete identifie. Le PRD, l'UX, l'architecture et les epics/stories sont alignes sur une solution brownfield limitee a l'application web, sans migration SQLite et sans nouvel endpoint.

## 2. Artifacts verifies

| Artifact | Statut | Observation |
| --- | --- | --- |
| PRD | Present | Couvre objectifs, hors perimetre, FR/NFR, AC et risques |
| UX Design | Present | Couvre structure UI, etats, compteurs, aucun resultat, accessibilite, responsive |
| Architecture | Present | Couvre decisions techniques, DOM contract, algorithme, integration, tests |
| Epics and Stories | Present | Couvre 5 epics, 11 stories, ordre recommande et matrice de couverture |

## 3. Synthese de readiness

| Axe | Evaluation | Commentaire |
| --- | --- | --- |
| Clarte produit | PASS | Le comportement attendu est explicite : un traitement max, une tache max, etats fait/restant/presence, logique ET |
| UX | PASS | Les controles, le feedback et les etats responsive sont suffisamment specifies |
| Architecture | PASS | La solution est coherente avec Django MVT, templates existants et filtrage navigateur |
| Couverture stories | PASS | Les stories couvrent donnees, moteur, UI, integration dynamique et verification |
| Testabilite | CONCERN | Les tests Django sont limites par `managed=False`; la strategie prevoit un fallback manuel documente |
| Risque regression | CONCERN | Le filtre global existant est dans `base.html` et utilise des correspondances partielles |
| Scope control | PASS | Aucun schema, endpoint ou refonte globale n'est demande |

## 4. Findings

### Concern 1 - Le filtre global existant doit etre refactorise, pas empile

Le code actuel dans `web/kanban/templates/kanban/base.html` contient un filtre global qui :

- lit `#global-search` et `#global-filter` ;
- masque les cartes via `card.style.display`;
- utilise `data-pending-traitement-names` et `data-pending-tache-names`;
- compare les libelles specifiques avec `includes()`.

Ce comportement est incompatible avec l'exigence de matching exact et avec les elements faits.

**Impact potentiel** : si une nouvelle barre de filtres est ajoutee sans centraliser la visibilite, un ancien listener peut reafficher ou masquer des cartes en contradiction avec le nouveau filtre.

**Mitigation obligatoire** : Story 2.2 doit refactoriser la recherche globale existante pour appeler un seul moteur de visibilite, par exemple `window.applyBoardFilters()`, ou deplacer la logique commune dans une fonction globale unique.

### Concern 2 - Echappement JSON dans les attributs HTML

Les nouveaux attributs `data-traitements` et `data-taches` doivent contenir du JSON valide pour des libelles metier libres.

**Impact potentiel** : apostrophes, guillemets, accents ou caracteres HTML peuvent casser l'attribut ou produire un parsing incorrect.

**Mitigation obligatoire** : implementer une serialisation controlee cote Python ou template et verifier au minimum un libelle contenant apostrophe et guillemets. Ne pas construire le JSON a la main avec une concatenation fragile dans le template.

### Concern 3 - Les tests automatises sont fragiles dans ce projet

`web/kanban/tests.py` indique deja que les modeles Django sont `managed=False`, ce qui peut empecher la creation simple des tables dans la base de test.

**Impact potentiel** : l'equipe peut croire disposer de tests Django alors qu'ils sont vides ou non executables.

**Mitigation obligatoire** : Story 5.1 doit soit rendre des tests minimaux executables avec setup de tables, soit documenter explicitement le blocage et executer la matrice manuelle AC-01 a AC-12.

### Concern 4 - Les mutations AJAX peuvent contourner le filtre courant

Le tableau remplace ou ajoute des cartes apres creation, suppression, drag-and-drop et `refreshActivityColumns(activityId)`.

**Impact potentiel** : une carte nouvellement rendue peut apparaitre alors qu'elle ne correspond pas au filtre courant, ou les compteurs peuvent redevenir faux.

**Mitigation obligatoire** : Story 4.1 doit appeler le moteur de filtrage apres chaque mutation DOM et recalculer les compteurs.

## 5. Traceability PRD vers stories

| Exigences | Couverture |
| --- | --- |
| Catalogues globaux faits/restants | Story 1.1 |
| Donnees structurees par carte | Story 1.2 |
| Selection simple par axe et etats | Story 3.1 |
| Correspondance fait/restant/presence | Story 2.1 |
| Combinaison traitement + tache en ET | Story 2.1 |
| Aucun filtre neutre | Story 2.1, Story 2.2 |
| Application immediate | Story 3.1 |
| Reinitialisation | Story 3.1 |
| Aucun resultat | Story 3.2 |
| Recherche texte combinee | Story 2.2 |
| Exactitude des libelles | Story 2.1 |
| Performance percue | Story 2.1, Story 4.1 |
| Accessibilite minimale | Story 3.1, Story 3.3 |
| Compatibilite brownfield | Story 1.1, Story 1.2, Story 4.2 |

Couverture : **complete** pour le perimetre du PRD.

## 6. Recommandations pour sprint planning

### Regroupement conseille

Sprint unique possible pour cette fonctionnalite, avec ordre strict :

1. Story 1.1 - Catalogues globaux.
2. Story 1.2 - Donnees JSON par carte.
3. Story 2.1 - Moteur de filtrage exact.
4. Story 2.2 - Refactor recherche globale existante.
5. Story 3.1 - Barre de filtres.
6. Story 3.2 - Compteurs et aucun resultat.
7. Story 3.3 - Style responsive.
8. Story 4.1 - Reapplication apres mutations DOM.
9. Story 4.2 - Non-regression interactions existantes.
10. Story 5.1 - Verification automatisee minimale ou fallback documente.
11. Story 5.2 - Matrice d'acceptation AC-01 a AC-12.

### Gate avant implementation

Avant d'ecrire le code, l'implementateur doit confirmer la strategie de serialisation JSON dans `card_snippet.html`. C'est le point technique le plus susceptible de creer une regression subtile.

### Gate avant livraison

Avant livraison, executer la matrice AC-01 a AC-12 avec au moins :

- un traitement fait ;
- un traitement restant ;
- une tache faite ;
- une tache restante ;
- deux libelles proches comme `Controle` et `Controle final` ;
- une carte presente dans plusieurs colonnes virtuelles.

## 7. Decision finale

Le dossier est **suffisamment pret** pour passer a `bmad-sprint-planning`.

Conditions a porter dans le sprint :

- centraliser la logique de visibilite avec la recherche existante ;
- traiter l'echappement JSON comme un point d'implementation critique ;
- ne pas compter sur les tests Django actuels sans les rendre executables ;
- verifier les mutations DOM avec filtre actif.
