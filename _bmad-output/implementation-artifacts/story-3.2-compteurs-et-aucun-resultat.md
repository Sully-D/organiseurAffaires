---
title: 'Story 3.2 - Mettre a jour les compteurs et l''etat aucun resultat'
story_id: '3.2'
epic: 'Epic 3 - Interface de filtre et feedback utilisateur'
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
source_story_2_2: '_bmad-output/implementation-artifacts/story-2.2-combiner-filtre-metier-recherche-texte.md'
source_story_3_1: '_bmad-output/implementation-artifacts/story-3.1-ajouter-barre-filtres-metier.md'
---

# Story 3.2 - Mettre a jour les compteurs et l'etat aucun resultat

## Status

Done.

## Story

**En tant que** utilisateur,  
**je veux** voir combien de cartes restent visibles et etre informe quand aucune carte ne correspond,  
**afin de** comprendre l'effet de mes filtres.

## Scope

Cette story ajoute le feedback visuel minimal apres filtrage: compteurs de colonnes bases sur les cartes visibles et message global quand aucune carte n'est visible. Elle s'appuie sur la barre metier de Story 3.1 et sur le moteur centralise de Story 2.2.

### Included

- Ajouter le message global `Aucune carte ne correspond aux filtres` dans `board.html`.
- Donner au message `aria-live="polite"` et `hidden` par defaut.
- Recalculer chaque compteur `.count` apres `applyBoardFilters()`.
- Compter uniquement les `.activity-card` visibles dans chaque colonne.
- Afficher le message seulement si aucune carte visible ne reste sur tout le tableau.
- Masquer le message des qu'au moins une carte redevient visible.
- Conserver toutes les colonnes visibles, meme si leur compteur vaut `0`.
- Verifier que les compteurs recuperent leur valeur apres reset metier ou recherche vide.

### Excluded

- Styler finement le message ou les compteurs dans `style.css`.
- Changer la structure de la barre de filtres metier.
- Reappliquer les filtres apres mutations DOM, creation, suppression ou drag-and-drop.
- Changer le comportement de matching exact, de recherche texte ou du select global.
- Modifier `views.py`, le schema SQLite ou les endpoints.

## Acceptance Criteria

1. Chaque compteur de colonne reflète le nombre de `.activity-card` visibles dans sa colonne apres filtrage.
2. Les cartes masquees via `hidden` ne sont pas comptees.
3. Les compteurs baissent quand un filtre produit un resultat partiel.
4. Les compteurs reviennent quand les filtres metier sont reinitialises, sous reserve de la recherche texte / select global actifs.
5. Le message `Aucune carte ne correspond aux filtres` est present dans le DOM avec `id="noFilterResults"`.
6. Le message utilise `aria-live="polite"`.
7. Le message est cache par defaut avec `hidden`.
8. Le message apparait uniquement quand aucune carte visible ne reste dans tout le tableau.
9. Le message disparait des qu'au moins une carte redevient visible.
10. Les colonnes Kanban restent visibles meme quand leur compteur vaut `0`.
11. `applyBoardFilters()` met a jour les compteurs et le message apres avoir applique la visibilite des cartes.

## Tasks / Subtasks

- [x] Task 1 - Ajouter le message aucun resultat (AC: 5, 6, 7)
  - [x] Ajouter `<div id="noFilterResults" aria-live="polite" hidden>` dans `board.html`.
  - [x] Placer le message dans la zone du tableau, apres la barre de filtres et avant ou autour de `.board-container`.
  - [x] Utiliser le texte exact `Aucune carte ne correspond aux filtres`.
  - [x] Ne pas masquer ou supprimer les colonnes.

- [x] Task 2 - Ajouter le calcul des cartes visibles par colonne (AC: 1, 2, 3)
  - [x] Ajouter une fonction `isCardVisible(card)` ou equivalent.
  - [x] Ajouter une fonction `updateVisibleCounts()`.
  - [x] Pour chaque `.kanban-column`, compter les `.activity-card` qui ne sont pas `hidden`.
  - [x] Mettre a jour le `.count` de chaque colonne avec cette valeur.
  - [x] Retourner ou exposer le total visible global pour le message.

- [x] Task 3 - Ajouter la gestion du message global (AC: 8, 9)
  - [x] Ajouter une fonction `updateNoFilterResults(totalVisible)` ou equivalent.
  - [x] Mettre `noFilterResults.hidden = totalVisible > 0`.
  - [x] Si aucune carte n'existe dans le DOM, garder le comportement coherent: message visible si total visible `0`.
  - [x] Ne pas afficher un message par colonne.

- [x] Task 4 - Integrer le feedback a `applyBoardFilters()` (AC: 4, 9, 11)
  - [x] Appeler `updateVisibleCounts()` a la fin de `applyBoardFilters()`.
  - [x] Appeler `updateNoFilterResults()` apres le recalcul des compteurs.
  - [x] Verifier que le reset de Story 3.1 declenche bien cette mise a jour via `applyBoardFilters()`.
  - [x] Ne pas ajouter de logique concurrente dans `base.html`.

- [x] Task 5 - Ajouter une verification automatisee structurelle (AC: 1-11)
  - [x] Ajouter des assertions dans `web/kanban/tests.py` pour `#noFilterResults`, `aria-live` et `hidden`.
  - [x] Verifier que `updateVisibleCounts()` existe et compte via `card.hidden`.
  - [x] Verifier que `applyBoardFilters()` appelle `updateVisibleCounts()` apres avoir affecte `card.hidden`.
  - [x] Verifier que les colonnes ne sont pas masquees par la logique du message.
  - [x] Executer `venv/bin/python web/manage.py test kanban`.
  - [x] Executer `venv/bin/python web/manage.py check`.

## Dev Notes

### Current Implementation Context

- `web/kanban/templates/kanban/board.html` contient deja:
  - `#business-filter-bar`;
  - `.board-container`;
  - `.kanban-column`;
  - `.column-header .count`;
  - `.column-body .activity-card`;
  - `applyBoardFilters()`, qui applique `card.hidden = !visible`.
- `base.html` delegue deja la recherche globale a `window.applyBoardFilters()`.
- Le reset metier de Story 3.1 appelle `updateBusinessFilterStateFromControls()`, qui appelle ensuite `window.applyBoardFilters()`.
- Les compteurs initiaux sont rendus serveur avec `{{ col_data.activities|length }}`; apres filtrage, ils doivent refleter le DOM visible.

### Recommended Function Contracts

Implementation recommandee:

```javascript
function isCardVisible(card) {
    return !card.hidden;
}

function updateVisibleCounts() {
    let totalVisible = 0;
    document.querySelectorAll('.kanban-column').forEach(column => {
        const visibleCount = Array.from(column.querySelectorAll('.activity-card'))
            .filter(isCardVisible).length;
        const countEl = column.querySelector('.count');
        if (countEl) countEl.innerText = visibleCount;
        totalVisible += visibleCount;
    });
    return totalVisible;
}

function updateNoFilterResults(totalVisible) {
    const noResults = document.getElementById('noFilterResults');
    if (noResults) noResults.hidden = totalVisible > 0;
}
```

Dans `applyBoardFilters()`, appeler:

```javascript
const totalVisible = updateVisibleCounts();
updateNoFilterResults(totalVisible);
```

apres la boucle qui met `card.hidden`.

### Non-Regression Guardrails

- Ne pas utiliser `style.display` pour les cartes ou les colonnes.
- Ne pas masquer `.kanban-column`; seul le message global change d'etat.
- Ne pas baser les compteurs sur les donnees serveur apres filtrage.
- Ne pas compter les cartes masquées avec `hidden`.
- Ne pas changer les fonctions de matching exact ni l'etat `window.businessFilterState`.
- Ne pas ajouter de recalcul apres mutations DOM; Story 4.1 couvrira la reappplication apres creation, suppression, drag-and-drop et refresh.

### Testing Guidance

Le repo n'a pas de runner JavaScript configure. Tests structurels Django acceptables:

- Le template contient `id="noFilterResults"`, `aria-live="polite"` et `hidden`.
- Le texte exact `Aucune carte ne correspond aux filtres` est present.
- `isCardVisible()` ou `updateVisibleCounts()` utilise `!card.hidden`.
- `updateVisibleCounts()` parcourt `.kanban-column` et met a jour `.count`.
- `updateNoFilterResults()` pilote seulement `noResults.hidden`.
- `applyBoardFilters()` appelle `updateVisibleCounts()` et `updateNoFilterResults()` apres `card.hidden = !visible`.

Matrice manuelle minimale:

| Cas | Action | Resultat attendu |
| --- | --- | --- |
| Etat initial | Charger le tableau | Compteurs egaux aux cartes visibles initiales, message cache |
| Resultat partiel | Appliquer un filtre qui masque certaines cartes | Compteurs diminuent par colonne |
| Colonne vide | Appliquer un filtre qui vide une colonne | Colonne reste visible, compteur `0` |
| Zero global | Appliquer un filtre sans resultat | Tous compteurs `0`, message visible |
| Recuperation | Changer le filtre pour retrouver des cartes | Message cache, compteurs mis a jour |
| Reset metier | Cliquer reset apres zero resultat | Message cache si des cartes restent selon recherche/select global |
| Recherche active | Recherche texte active puis reset metier | Compteurs refletent encore la recherche active |

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

### Manual Fallback

Si aucun test navigateur n'est disponible:

1. Ouvrir le tableau Kanban.
2. Noter les compteurs initiaux.
3. Choisir un traitement ou une tache avec resultats partiels.
4. Verifier que les compteurs correspondent aux cartes visibles par colonne.
5. Choisir une combinaison sans resultat.
6. Verifier que le message global apparait et que les colonnes restent visibles.
7. Cliquer `Reinitialiser les filtres`.
8. Verifier que le message disparait et que les compteurs se recalculent.

## Done Checklist

- [x] Message aucun resultat ajoute avec `aria-live="polite"` et `hidden`.
- [x] Compteurs recalcules depuis les cartes visibles apres filtrage.
- [x] Message affiche uniquement quand le total visible global vaut `0`.
- [x] Colonnes conservees visibles meme avec compteur `0`.
- [x] Reset metier et recherche globale declenchent le recalcul via `applyBoardFilters()`.
- [x] Aucun changement de matching, schema, endpoint ou style final.
- [x] Verification automatisee executee ou fallback manuel documente.
- [x] Sprint status mis a jour apres implementation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-25: `venv/bin/python web/manage.py test kanban` -> OK, 14 tests.
- 2026-04-25: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- Ajout de `#noFilterResults` avec `aria-live="polite"`, `hidden` et le texte exact attendu.
- Ajout de `isCardVisible()`, `updateVisibleCounts()` et `updateNoFilterResults()`.
- `applyBoardFilters()` met maintenant a jour les compteurs et le message apres avoir applique `card.hidden`.
- Les compteurs sont recalcules par colonne depuis les cartes non masquees.
- Le message global est affiche uniquement quand le total visible vaut `0`.
- Les colonnes ne sont pas masquees par cette story.
- Verification automatisee structurelle ajoutee dans `web/kanban/tests.py`.

### File List

- `web/kanban/templates/kanban/board.html`
- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-3.2-compteurs-et-aucun-resultat.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-25: Story 3.2 creee avec contexte d'implementation pour recalculer les compteurs visibles et afficher le message aucun resultat.
- 2026-04-25: Story 3.2 implementee; compteurs visibles et message aucun resultat branches sur `applyBoardFilters()`.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-25: Clean review. Aucun finding decision-needed, patch ou defer.
- `#noFilterResults` est present avant `.board-container`, cache par defaut et annonce via `aria-live="polite"`.
- `applyBoardFilters()` applique d'abord `card.hidden`, puis recalcule les compteurs visibles et l'etat du message global.
- Les compteurs utilisent les cartes non masquees par colonne et ne masquent jamais les colonnes elles-memes.
- Le message global est pilote uniquement par le total visible global, pas par colonne.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
