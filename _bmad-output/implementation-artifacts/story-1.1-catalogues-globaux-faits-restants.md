---
title: 'Story 1.1 - Alimenter les catalogues globaux faits et restants'
story_id: '1.1'
epic: 'Epic 1 - Donnees de filtrage exactes dans le rendu Kanban'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'done'
workflow: 'bmad-create-story'
agent: 'sm'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
---

# Story 1.1 - Alimenter les catalogues globaux faits et restants

## User Story

**En tant que** utilisateur du tableau Kanban web,  
**je veux** voir les traitements et taches connus dans les champs de filtre, qu'ils soient faits ou restants,  
**afin de** pouvoir filtrer tous les cas demandes par le PRD.

## Status

Done.

## Scope

Cette story modifie uniquement les catalogues de filtre fournis au rendu du tableau Kanban. Elle ne modifie pas encore les attributs de donnees des cartes ni la logique JavaScript de filtrage.

### Included

- Mettre a jour `filter_traitements` dans `board()` pour inclure les descriptions de traitements faits et non faits.
- Mettre a jour `filter_taches` dans `board()` pour inclure les descriptions de taches faites et non faites.
- Exclure les descriptions vides.
- Conserver les valeurs distinctes et le tri alphabetique.

### Excluded

- Ajouter `data-traitements` ou `data-taches` sur les cartes.
- Modifier le filtre global JavaScript dans `base.html`.
- Ajouter la nouvelle barre de filtres metier.
- Modifier le schema SQLite.
- Ajouter un endpoint.
- Modifier les regles des colonnes virtuelles.

## Implementation Context

Fichier principal :

- `web/kanban/views.py`

Fonction concernee :

- `board(request)`

Code actuel a remplacer :

```python
'filter_traitements': Traitement.objects.filter(done=False).exclude(description="").values_list('description', flat=True).distinct().order_by('description'),
'filter_taches': Tache.objects.filter(done=False).exclude(description="").values_list('description', flat=True).distinct().order_by('description'),
```

Comportement attendu :

- retirer le filtre `done=False` ;
- exclure `description=""` ;
- idealement exclure aussi `description__isnull=True` si cela reste compatible avec les modeles actuels ;
- conserver `values_list('description', flat=True).distinct().order_by('description')`.

Exemple attendu :

```python
Traitement.objects.filter(description__isnull=False) \
    .exclude(description__exact="") \
    .values_list("description", flat=True) \
    .distinct() \
    .order_by("description")
```

## Acceptance Criteria

- `filter_traitements` contient les descriptions de traitements faits.
- `filter_traitements` contient les descriptions de traitements restants.
- `filter_taches` contient les descriptions de taches faites.
- `filter_taches` contient les descriptions de taches restantes.
- Les descriptions vides sont exclues.
- Les catalogues restent deduplices.
- Les catalogues restent tries par `description`.
- Le comportement d'affichage des colonnes Kanban est inchange.
- Aucun schema, endpoint ou template n'est requis pour cette story.

## Technical Notes

- `Traitement.description` est un `TextField`; `Tache.description` est un `CharField`.
- Le filtre existant dans `base.html` utilise encore ces catalogues pour les options "Traitements Specifiques" et "Taches Specifiques". Apres cette story, ces options pourront contenir des elements faits, meme si l'ancien filtre JavaScript ne saura pas encore les matcher correctement. Ce decalage est acceptable temporairement et sera corrige par Story 2.2.
- Ne pas refactorer la logique repetee de `board()` dans cette story. Le changement doit rester petit et focalise.
- Le fichier `web/kanban/tests.py` contient actuellement des tests vides et note la difficulte liee aux modeles `managed=False`. Ne pas surinvestir dans une infrastructure de test pour cette story si cela bloque l'avancement ; documenter le fallback manuel.

## Verification Plan

### Automated, if feasible

- Ajouter ou preparer un test de contexte `board()` qui cree :
  - un traitement `done=True` avec description non vide ;
  - un traitement `done=False` avec description non vide ;
  - une tache `done=True` avec description non vide ;
  - une tache `done=False` avec description non vide ;
  - un traitement ou une tache avec description vide.
- Verifier que les quatre descriptions non vides sont presentes et que la valeur vide est absente.

### Manual fallback

Si les tests Django sont bloques par les modeles `managed=False` :

1. Lancer le serveur Django.
2. Ouvrir le tableau Kanban.
3. Creer ou identifier au moins un traitement fait, un traitement restant, une tache faite et une tache restante.
4. Verifier dans les options du select global que les quatre libelles sont presents.
5. Verifier que les libelles vides ne sont pas affiches.

## Done Checklist

- [x] `web/kanban/views.py` mis a jour.
- [x] Les catalogues ne filtrent plus sur `done=False`.
- [x] Les descriptions vides restent exclues.
- [x] Aucun changement de schema ou endpoint.
- [x] Verification automatisee executee ou fallback manuel documente.
- [x] Sprint status mis a jour apres implementation.

## Dev Agent Record

### Debug Log

- 2026-04-25: `venv/bin/python web/manage.py test kanban` -> OK, 2 tests.
- 2026-04-25: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes

- Les catalogues `filter_traitements` et `filter_taches` du rendu Kanban incluent maintenant les descriptions faites et restantes, car le filtre `done=False` a ete retire.
- Les descriptions `NULL` et vides restent exclues, les valeurs restent distinctes et triees par `description`.
- La verification automatisee inspecte les `QuerySet` sans interroger les tables legacy `managed=False`.

### File List

- `web/kanban/views.py`
- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-1.1-catalogues-globaux-faits-restants.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-25: Implementation de la story 1.1 et ajout de tests de requete pour les catalogues de filtres.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-25: Clean review. Aucun finding decision-needed, patch ou defer.
- Les changements respectent le perimetre de la story: catalogues uniquement, sans modification de schema, endpoint, template ou logique de colonnes.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.

## Handoff to Dev

Implement this story with a minimal patch. Do not begin Story 1.2 in the same change unless explicitly requested. Preserve existing column queries and virtual-column behavior.
