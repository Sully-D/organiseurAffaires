---
title: 'Story 2.1 - Implementer les fonctions de correspondance exactes'
story_id: '2.1'
epic: 'Epic 2 - Moteur de filtrage cote navigateur'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'done'
workflow: 'bmad-create-story'
agent: 'sm'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
---

# Story 2.1 - Implementer les fonctions de correspondance exactes

## Status

Done.

## Story

**En tant que** utilisateur,  
**je veux** que les filtres utilisent la presence exacte et l'etat des traitements/taches,  
**afin de** ne pas voir de cartes erronees quand des libelles se ressemblent.

## Scope

Cette story ajoute le moteur JavaScript de matching exact dans `board.html`. Elle ne cree pas encore la barre de filtres metier visible et ne refactorise pas encore la recherche globale existante dans `base.html`; cette integration est reservee a Story 2.2 / 3.1.

### Included

- Parser les attributs `data-traitements` et `data-taches` ajoutes en Story 1.2.
- Ajouter des fonctions nommees pour evaluer un axe de filtre et la combinaison traitement + tache.
- Comparer les libelles avec `description === selectedLabel`.
- Gerer les etats `done === true` et `done === false`.
- Gerer la regle de presence quand aucun etat ou les deux etats sont coches.
- Exposer les fonctions utiles sur `window` pour les stories suivantes.
- Fournir une fonction `window.applyBoardFilters()` non destructive qui ne change rien quand aucun filtre metier n'est actif.

### Excluded

- Ajouter les controles UI de filtre metier.
- Modifier la recherche globale de `base.html`.
- Modifier les compteurs visibles ou le message aucun resultat.
- Reappliquer le filtre apres mutations DOM.
- Modifier `card_snippet.html`, `views.py`, le schema SQLite ou les endpoints.

## Acceptance Criteria

1. Traitement avec etat "Fait" seul matche uniquement les cartes dont `data-traitements` contient `{ description: selectedLabel, done: true }`.
2. Traitement avec etat "Restant a faire" seul matche uniquement les cartes dont `data-traitements` contient `{ description: selectedLabel, done: false }`.
3. Tache avec etat "Fait" seul matche uniquement les cartes dont `data-taches` contient `{ description: selectedLabel, done: true }`.
4. Tache avec etat "Restant a faire" seul matche uniquement les cartes dont `data-taches` contient `{ description: selectedLabel, done: false }`.
5. Un libelle selectionne sans etat coche matche la presence exacte du libelle, quel que soit `done`.
6. Un libelle selectionne avec les deux etats coches matche la presence exacte du libelle, quel que soit `done`.
7. Le libelle `Controle` ne matche pas `Controle final`.
8. Si un traitement et une tache sont selectionnes, la carte doit satisfaire les deux axes avec une logique ET.
9. Une carte avec JSON absent, vide ou invalide ne provoque pas d'exception et ne matche pas un axe actif.
10. Sans filtre metier actif, `window.applyBoardFilters()` conserve l'affichage actuel des cartes.

## Tasks / Subtasks

- [x] Task 1 - Ajouter les fonctions de parsing des donnees de carte (AC: 9, 10)
  - [x] Dans le script inline de `web/kanban/templates/kanban/board.html`, ajouter `parseCardFilterData(card)`.
  - [x] Lire `data-traitements` et `data-taches`.
  - [x] Utiliser `JSON.parse` avec `try/catch`.
  - [x] Normaliser les resultats en tableaux; en cas d'absence ou JSON invalide, retourner des tableaux vides.
  - [x] Mettre en cache les donnees parsees sur la carte, par exemple `card._filterData`.

- [x] Task 2 - Ajouter les fonctions de matching exact par axe (AC: 1, 2, 3, 4, 5, 6, 7)
  - [x] Ajouter `matchesItemFilter(items, selectedLabel, doneChecked, pendingChecked)`.
  - [x] Si `selectedLabel` est vide, retourner `true`.
  - [x] Si aucun etat ou deux etats sont coches, matcher `item.description === selectedLabel`.
  - [x] Si "Fait" seul est coche, matcher `item.description === selectedLabel && item.done === true`.
  - [x] Si "Restant a faire" seul est coche, matcher `item.description === selectedLabel && item.done === false`.
  - [x] Ne jamais utiliser `includes`, `innerText` ou une comparaison insensible a la casse pour les libelles metier.

- [x] Task 3 - Ajouter les fonctions de combinaison et d'application (AC: 8, 10)
  - [x] Ajouter `matchesBusinessFilters(card, filterState)`.
  - [x] Combiner axe traitement et axe tache avec `&&`.
  - [x] Ajouter `getBusinessFilterState()` qui retourne un etat neutre tant que la barre UI n'existe pas.
  - [x] Ajouter `applyBoardFilters()` qui applique le moteur aux `.activity-card`.
  - [x] Quand l'etat metier est neutre, `applyBoardFilters()` ne doit pas modifier `style.display`, `hidden` ou les classes des cartes.
  - [x] Exposer au minimum `window.parseCardFilterData`, `window.matchesItemFilter`, `window.matchesBusinessFilters` et `window.applyBoardFilters`.

- [x] Task 4 - Verifier les combinaisons critiques (AC: 1-10)
  - [x] Ajouter des tests automatises si faisable sans nouveau framework lourd.
  - [x] A minima, documenter une matrice manuelle dans le Dev Agent Record avec: Fait, Restant, presence, deux etats, libelles proches, traitement+tache.
  - [x] Executer `venv/bin/python web/manage.py test kanban`.
  - [x] Executer `venv/bin/python web/manage.py check`.

## Dev Notes

### Current Implementation Context

- `web/kanban/templates/kanban/board.html` contient deja le script inline du tableau: tri, modal, creation, suppression, drag-and-drop et `refreshActivityColumns()`.
- `web/kanban/templates/kanban/base.html` contient actuellement la recherche globale et un select `#global-filter` qui utilise encore `data-pending-*` et des comparaisons `includes`.
- Story 2.1 ne doit pas modifier `base.html`. Story 2.2 refactorisera la recherche globale pour appeler le moteur commun.
- Story 1.2 a ajoute sur chaque `.activity-card`:
  - `data-traitements`
  - `data-taches`
  - JSON sous forme de tableaux d'objets `{ "description": "...", "done": true|false }`.
- `card_snippet.html` conserve aussi les anciens attributs `data-pending-*`; ne pas les supprimer.

### Recommended Function Contracts

Implementation recommandee dans `board.html` :

```javascript
function parseCardFilterData(card) {
    if (card._filterData) return card._filterData;
    const traitements = parseJsonArrayAttribute(card, 'data-traitements');
    const taches = parseJsonArrayAttribute(card, 'data-taches');
    card._filterData = { traitements, taches };
    return card._filterData;
}

function matchesItemFilter(items, selectedLabel, doneChecked, pendingChecked) {
    if (!selectedLabel) return true;
    const matchPresence = !doneChecked || !pendingChecked;
    return items.some(item => {
        if (item.description !== selectedLabel) return false;
        if (matchPresence) return true;
        if (doneChecked) return item.done === true;
        return item.done === false;
    });
}
```

Attention: l'exemple ci-dessus illustre le contrat, mais l'implementation doit corriger la logique de presence ainsi:

- presence si `!doneChecked && !pendingChecked`;
- presence si `doneChecked && pendingChecked`;
- fait seul si `doneChecked && !pendingChecked`;
- restant seul si `!doneChecked && pendingChecked`.

### Filter State Shape

Utiliser une forme simple et stable pour les stories suivantes :

```javascript
{
    traitementLabel: '',
    traitementDone: false,
    traitementPending: false,
    tacheLabel: '',
    tacheDone: false,
    tachePending: false
}
```

Tant que les controles UI n'existent pas, `getBusinessFilterState()` peut retourner cet etat neutre.

### Non-Regression Guardrails

- Ne pas brancher ce moteur sur `#global-search` ou `#global-filter` dans cette story.
- Ne pas changer `sortColumn()` sauf si l'ajout d'un appel neutre a `applyBoardFilters()` est strictement necessaire.
- Ne pas modifier `refreshActivityColumns()` dans cette story; l'integration apres mutation est reservee a Story 4.1.
- Ne pas ajouter de dependance npm, bundler, endpoint ou fichier JS separe.
- Sans filtre metier actif, aucune carte ne doit etre masquee par ce nouveau code.
- Si une carte est remplacee par AJAX, le cache `card._filterData` disparait naturellement avec l'ancien element DOM.

### Testing Guidance

Le repo n'a pas de runner JavaScript configure. Options acceptables :

- Test Django qui lit le contenu de `board.html` et verifie la presence des fonctions nommees et l'absence de `.includes(` dans `matchesItemFilter`.
- Petit test Python ciblant une fonction JS extraite n'est pas recommande si cela force une duplication de logique.
- Fallback manuel documente si aucun test JS executable n'est raisonnable.

Matrice manuelle minimale :

| Cas | Donnees carte | Filtre | Resultat attendu |
| --- | --- | --- | --- |
| Traitement fait | `Controle`, `done:true` | traitement `Controle`, fait | visible |
| Traitement restant | `Controle`, `done:false` | traitement `Controle`, restant | visible |
| Tache faite | `Verification`, `done:true` | tache `Verification`, fait | visible |
| Tache restante | `Verification`, `done:false` | tache `Verification`, restant | visible |
| Presence | `Controle`, deux etats ou aucun | traitement `Controle` | visible |
| Libelles proches | `Controle final` | traitement `Controle` | masque |
| ET traitement+tache | traitement OK, tache KO | deux axes actifs | masque |
| JSON invalide | attribut invalide | axe actif | masque sans exception |

### Source References

- `_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md`, section "Story 2.1 - Implementer les fonctions de correspondance exactes".
- `_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md`, sections "Algorithme de filtrage", "Integration avec les comportements existants", "Performance", "Strategie de test".
- `_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md`, sections "Impacts sur l'interface existante" et "Criteres UX d'acceptation".
- `_bmad-output/implementation-artifacts/story-1.2-donnees-json-par-carte.md`, contrat `data-traitements` / `data-taches`.

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

Si un test structurel est ajoute dans `web/kanban/tests.py`, verifier :

- `parseCardFilterData` existe.
- `matchesItemFilter` existe.
- `matchesBusinessFilters` existe.
- `applyBoardFilters` existe et est expose sur `window`.
- Le template contient une comparaison stricte `item.description === selectedLabel`.

### Manual Fallback

Si aucun test JS executable n'est ajoute :

1. Ouvrir le tableau Kanban.
2. Dans la console, appeler directement `window.matchesItemFilter(...)` avec des tableaux d'objets.
3. Verifier les cas Fait, Restant, presence sans etat, presence avec deux etats.
4. Verifier que `Controle` ne matche pas `Controle final`.
5. Verifier que `window.applyBoardFilters()` appelee sans UI active ne change pas l'affichage actuel.

## Done Checklist

- [x] `board.html` contient les fonctions nommees de parsing et matching.
- [x] Les comparaisons de libelles utilisent `===`.
- [x] Les etats fait/restant/presence respectent les AC.
- [x] Traitement et tache se combinent en ET.
- [x] JSON invalide ou absent ne casse pas le tableau.
- [x] Sans filtre metier actif, aucune carte n'est masquee par le nouveau moteur.
- [x] Aucun changement de schema, endpoint, recherche globale ou UI de filtre.
- [x] Verification automatisee executee ou fallback manuel documente.
- [x] Sprint status mis a jour apres creation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-25: `venv/bin/python web/manage.py test kanban` -> OK, 7 tests.
- 2026-04-25: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- Ajout dans `board.html` des fonctions `parseCardFilterData`, `matchesItemFilter`, `matchesBusinessFilters` et `applyBoardFilters`.
- `matchesItemFilter` utilise uniquement `item.description === selectedLabel` et les booleens stricts `item.done === true/false`.
- `applyBoardFilters()` retourne immediatement si aucun libelle metier n'est actif, ce qui preserve l'affichage actuel jusqu'a l'ajout de l'UI.
- Les fonctions sont exposees sur `window` pour les stories suivantes.
- Verification automatisee structurelle ajoutee dans `web/kanban/tests.py`.
- Matrice manuelle a reprendre si execution navigateur: fait, restant, presence sans etat, presence deux etats, libelles proches, traitement+tache, JSON invalide.

### File List

- `web/kanban/templates/kanban/board.html`
- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-2.1-fonctions-correspondance-exactes.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-25: Story 2.1 creee avec contexte d'implementation du moteur JS de matching exact.
- 2026-04-25: Implementation du moteur JS de matching exact et ajout de tests structurels.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-25: Clean review. Aucun finding decision-needed, patch ou defer.
- Le moteur JS respecte le perimetre de Story 2.1: fonctions de parsing/matching exposees sur `window`, sans ajout d'UI ni modification de la recherche globale.
- Le matching utilise une comparaison exacte `item.description === selectedLabel` et des booleens stricts `item.done === true/false`.
- `applyBoardFilters()` est neutre sans filtre metier actif, ce qui preserve le comportement existant en attendant Story 2.2/3.1.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
