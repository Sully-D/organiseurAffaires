---
title: 'Story 2.2 - Combiner le filtre metier avec la recherche texte existante'
story_id: '2.2'
epic: 'Epic 2 - Moteur de filtrage cote navigateur'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'done'
workflow: 'bmad-dev-story'
agent: 'dev'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
source_prd: '_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
source_readiness: '_bmad-output/planning-artifacts/readiness-report-filtrage-cartes-traitements-taches.md'
---

# Story 2.2 - Combiner le filtre metier avec la recherche texte existante

## Status

Done.

## Story

**En tant que** utilisateur,  
**je veux** que la recherche texte et les filtres metier agissent ensemble,  
**afin de** reduire les cartes visibles selon toutes mes intentions.

## Scope

Cette story refactorise la recherche globale existante pour que la decision de visibilite des cartes soit centralisee avec le moteur de filtres metier ajoute en Story 2.1. Elle ne cree pas encore la nouvelle barre de filtres metier visible; cette UI reste reservee a Story 3.1.

### Included

- Identifier et remplacer la logique de masquage directe de `base.html`.
- Ajouter une fonction de matching pour la recherche texte existante.
- Ajouter une fonction de matching pour le select global existant.
- Faire appliquer `window.applyBoardFilters()` aux cartes selon recherche texte ET filtre global existant ET filtres metier.
- Conserver le comportement actuel de recherche quand aucun filtre metier n'est actif.
- Conserver l'independance entre recherche texte et futur reset des filtres metier.
- Exposer les fonctions utiles sur `window` pour les stories suivantes et les tests structurels.

### Excluded

- Ajouter la barre de filtres metier visible.
- Ajouter le message "aucun resultat" ou recalculer les compteurs visibles.
- Reappliquer les filtres apres mutations DOM.
- Modifier les donnees Django, le schema SQLite ou les endpoints.
- Supprimer les anciens attributs `data-pending-*`, encore utiles au select global historique.

## Acceptance Criteria

1. Sans filtre metier actif, la recherche texte existante conserve son comportement: elle matche le nom, la date ou le texte visible de la carte.
2. Sans filtre metier actif, le select global existant conserve son comportement pour `all`, `traitements_all` et `taches_all`.
3. Pour les options specifiques `traitement:<label>` et `tache:<label>`, le matching utilise les donnees structurees `data-traitements` / `data-taches` et la presence exacte du libelle.
4. La decision finale de visibilite est centralisee dans `window.applyBoardFilters()`.
5. Une carte est visible uniquement si elle satisfait la recherche texte, le select global existant et les filtres metier actifs.
6. L'ancien listener de `base.html` ne doit plus appliquer un `card.style.display` concurrent.
7. Modifier la recherche texte ne change pas `window.businessFilterState` ni les controles metier futurs.
8. Reinitialiser les filtres metier via `window.businessFilterState` ou un appel neutre a `applyBoardFilters()` ne vide pas `#global-search`.
9. Vider `#global-search` ne modifie pas l'etat metier courant.
10. La combinaison recherche + traitement + tache fonctionne en logique ET.

## Tasks / Subtasks

- [x] Task 1 - Refactoriser le filtre global de `base.html` (AC: 1, 2, 4, 6)
  - [x] Remplacer `filterCards()` par un delegue qui appelle `window.applyBoardFilters()` quand disponible.
  - [x] Supprimer le masquage direct `card.style.display = ...` du listener global.
  - [x] Conserver les listeners `input` sur `#global-search` et `change` sur `#global-filter`.
  - [x] Prevoir un fallback neutre si le tableau n'a pas encore expose `window.applyBoardFilters()`.

- [x] Task 2 - Ajouter le matching de recherche texte dans `board.html` (AC: 1, 5)
  - [x] Ajouter `getGlobalSearchState()` ou equivalent qui lit `#global-search` et `#global-filter`.
  - [x] Ajouter `matchesSearchText(card, query)` qui reproduit le comportement existant: `data-name`, `data-date`, puis texte visible.
  - [x] Normaliser la recherche en minuscules comme le comportement actuel.
  - [x] S'assurer qu'une recherche vide ne filtre aucune carte.

- [x] Task 3 - Integrer le select global existant avec le moteur commun (AC: 2, 3, 5)
  - [x] Ajouter `matchesLegacyGlobalFilter(card, filterValue)` ou equivalent.
  - [x] Conserver `all`, `traitements_all` et `taches_all` via `data-pending-traitements` / `data-pending-taches`.
  - [x] Pour `traitement:<label>`, utiliser `matchesItemFilter(parsed.traitements, label, false, false)`.
  - [x] Pour `tache:<label>`, utiliser `matchesItemFilter(parsed.taches, label, false, false)`.
  - [x] Ne pas utiliser `includes()` pour les libelles specifiques.

- [x] Task 4 - Centraliser la decision finale (AC: 4, 5, 10)
  - [x] Modifier `applyBoardFilters()` pour evaluer recherche texte, select global et filtres metier.
  - [x] Retirer le retour immediat qui rend `applyBoardFilters()` neutre sans filtre metier actif, car la recherche texte doit maintenant passer par elle.
  - [x] Appliquer un seul mecanisme de masquage aux cartes, de preference `card.hidden = !visible`.
  - [x] Garantir que tous les criteres se combinent avec `&&`.

- [x] Task 5 - Verifier l'independance des etats (AC: 7, 8, 9)
  - [x] Verifier que les listeners de recherche ne modifient pas `window.businessFilterState`.
  - [x] Verifier qu'un appel avec etat metier neutre ne vide pas `#global-search`.
  - [x] Documenter dans le Dev Agent Record la matrice: recherche seule, filtre global seul, filtre metier seul, recherche + traitement, recherche + traitement + tache.

- [x] Task 6 - Ajouter ou ajuster les tests structurels (AC: 3, 4, 6, 10)
  - [x] Ajouter des assertions dans `web/kanban/tests.py` pour les fonctions de recherche globale.
  - [x] Verifier que `base.html` n'a plus de `card.style.display` dans la logique de filtre.
  - [x] Verifier que le matching specifique ne repose plus sur `data-pending-*-names.includes(target)`.
  - [x] Executer `venv/bin/python web/manage.py test kanban`.
  - [x] Executer `venv/bin/python web/manage.py check`.

## Dev Notes

### Current Implementation Context

- `web/kanban/templates/kanban/base.html` contient actuellement la recherche globale:
  - lit `#global-search` et `#global-filter`;
  - parcourt `.activity-card`;
  - masque directement avec `card.style.display`;
  - utilise `includes()` sur `data-pending-traitement-names` et `data-pending-tache-names` pour les options specifiques.
- `web/kanban/templates/kanban/board.html` expose deja:
  - `parseCardFilterData(card)`;
  - `matchesItemFilter(items, selectedLabel, doneChecked, pendingChecked)`;
  - `matchesBusinessFilters(card, filterState)`;
  - `applyBoardFilters(filterState = getBusinessFilterState())`.
- Story 2.1 a rendu `applyBoardFilters()` neutre sans filtre metier actif. Story 2.2 doit changer ce contrat: la fonction devient le point unique pour recherche texte, select global et filtres metier.
- Les futures stories 3.1 et 4.1 dependront de cette centralisation pour eviter que plusieurs listeners reaffichent ou masquent des cartes de facon contradictoire.

### Recommended Function Contracts

Etat global recommande:

```javascript
function getGlobalFilterState() {
    const searchInput = document.getElementById('global-search');
    const filterSelect = document.getElementById('global-filter');
    return {
        query: (searchInput?.value || '').toLowerCase(),
        filterValue: filterSelect?.value || 'all'
    };
}
```

Decision finale recommandee:

```javascript
const visible = matchesSearchText(card, globalState.query)
    && matchesLegacyGlobalFilter(card, globalState.filterValue)
    && matchesBusinessFilters(card, filterState);
```

Pour les options specifiques du select global, utiliser la presence exacte:

```javascript
const data = parseCardFilterData(card);
return matchesItemFilter(data.traitements, target, false, false);
```

### Non-Regression Guardrails

- Ne pas supprimer les options actuelles de `#global-filter`.
- Ne pas vider ou modifier `#global-search` depuis le reset metier.
- Ne pas ajouter de nouveau select ou barre de filtres dans cette story.
- Ne pas utiliser `includes()` pour les libelles metier specifiques; `includes()` reste acceptable pour la recherche texte libre.
- Ne pas melanger `style.display` et `hidden` sur les memes cartes pour le filtrage courant.
- Si `base.html` est charge sur une page sans tableau, le listener doit rester sans erreur.

### Testing Guidance

Le repo n'a pas de runner JavaScript configure. Tests structurels Django acceptables:

- `base.html` appelle `window.applyBoardFilters()` dans les listeners de recherche.
- La logique de filtrage de `base.html` ne contient plus `card.style.display`.
- `board.html` expose `matchesSearchText`, `matchesLegacyGlobalFilter` et `getGlobalFilterState`.
- `matchesLegacyGlobalFilter` utilise `parseCardFilterData` et `matchesItemFilter` pour `traitement:` / `tache:`.
- `applyBoardFilters` combine les criteres avec `&&`.

Matrice manuelle minimale:

| Cas | Recherche | Select global | Filtre metier | Resultat attendu |
| --- | --- | --- | --- | --- |
| Recherche seule | nom existant | all | neutre | cartes correspondantes visibles |
| Select global seul | vide | traitements_all | neutre | cartes avec traitement restant visibles |
| Specifique exact | vide | traitement `Controle` | neutre | `Controle` visible, `Controle final` masque |
| Recherche + specifique | texte OK | traitement OK | neutre | visible |
| Recherche + specifique | texte KO | traitement OK | neutre | masque |
| Recherche + metier | texte OK | all | traitement OK | visible |
| Recherche + traitement + tache | texte OK | all | deux axes OK | visible |
| Recherche + traitement + tache | texte OK | all | un axe KO | masque |
| Vider recherche | vide | all | metier actif | filtre metier conserve |
| Reset metier | texte conserve | all | neutre | recherche texte conservee |

### Source References

- `_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md`, section "Story 2.2 - Combiner le filtre metier avec la recherche texte existante".
- `_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md`, sections "Algorithme de filtrage" et "Integration avec les comportements existants".
- `_bmad-output/planning-artifacts/readiness-report-filtrage-cartes-traitements-taches.md`, "Concern 1 - Le filtre global existant doit etre refactorise, pas empile".
- `_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md`, FR-17 et AC-12.
- `_bmad-output/implementation-artifacts/story-2.1-fonctions-correspondance-exactes.md`, contrats du moteur de matching exact.

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

### Manual Fallback

Si aucun test navigateur n'est disponible:

1. Ouvrir le tableau Kanban.
2. Verifier une recherche texte seule avec `#global-filter = all`.
3. Verifier `traitements_all` et `taches_all`.
4. Verifier une option specifique avec deux libelles proches.
5. Depuis la console, definir `window.businessFilterState` avec un traitement et une tache, puis appeler `window.applyBoardFilters()`.
6. Verifier que vider `#global-search` conserve l'etat metier, et qu'un etat metier neutre conserve la recherche texte.

## Done Checklist

- [x] `base.html` ne masque plus les cartes via un mecanisme concurrent.
- [x] `applyBoardFilters()` est le point unique de decision de visibilite.
- [x] Recherche texte, select global et filtres metier se combinent en ET.
- [x] Les options specifiques du select global utilisent les donnees JSON structurees et un matching exact.
- [x] `#global-search` et l'etat metier restent independants.
- [x] Aucun nouveau schema, endpoint, bundler ou framework JS n'est ajoute.
- [x] Verification automatisee executee ou fallback manuel documente.
- [x] Sprint status mis a jour apres implementation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-25: `venv/bin/python web/manage.py test kanban` -> OK, 9 tests.
- 2026-04-25: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- `base.html` ne masque plus directement les cartes; les listeners de recherche deleguent a `window.applyBoardFilters()`.
- `board.html` ajoute `getGlobalFilterState`, `matchesSearchText` et `matchesLegacyGlobalFilter`.
- Les options specifiques du select global utilisent `data-traitements` / `data-taches` avec `matchesItemFilter(..., false, false)` pour une presence exacte.
- `applyBoardFilters()` combine recherche texte, select global et filtres metier en logique ET, puis applique uniquement `card.hidden`.
- La recherche texte et `window.businessFilterState` restent independants: aucun listener de recherche ne modifie l'etat metier.
- Matrice manuelle a reprendre si execution navigateur: recherche seule, filtre global seul, specifique exact, recherche + specifique, recherche + filtre metier, recherche + traitement + tache, vider recherche, reset metier.

### File List

- `web/kanban/templates/kanban/base.html`
- `web/kanban/templates/kanban/board.html`
- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-2.2-combiner-filtre-metier-recherche-texte.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-25: Story 2.2 creee avec contexte d'implementation pour centraliser recherche texte, select global et filtre metier.
- 2026-04-25: Story 2.2 implementee; filtrage global centralise dans `applyBoardFilters()` et tests structurels ajoutes.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-25: Clean review. Aucun finding decision-needed, patch ou defer.
- Le masquage concurrent dans `base.html` a bien ete retire au profit de `window.applyBoardFilters()`.
- `applyBoardFilters()` combine recherche texte, select global existant et filtres metier avec une logique ET.
- Les options specifiques `traitement:` et `tache:` utilisent les donnees JSON structurees avec matching exact au lieu des anciens `data-pending-*-names.includes(...)`.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
