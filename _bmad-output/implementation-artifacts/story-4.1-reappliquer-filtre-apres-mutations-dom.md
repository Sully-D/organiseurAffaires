---
title: 'Story 4.1 - Reappliquer le filtre apres mutations DOM'
story_id: '4.1'
epic: 'Epic 4 - Integration avec les interactions dynamiques du tableau'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'done'
workflow: 'bmad-dev-story'
agent: 'dev'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
source_story_2_2: '_bmad-output/implementation-artifacts/story-2.2-combiner-filtre-metier-recherche-texte.md'
source_story_3_2: '_bmad-output/implementation-artifacts/story-3.2-compteurs-et-aucun-resultat.md'
---

# Story 4.1 - Reappliquer le filtre apres mutations DOM

## Status

Done.

## Story

**En tant que** utilisateur,  
**je veux** que mes filtres restent actifs apres une action sur une carte,  
**afin de** ne pas revoir des cartes qui ne correspondent pas.

## Scope

Cette story branche le moteur centralise `applyBoardFilters()` sur les callbacks existants qui ajoutent, suppriment, deplacent ou remplacent des cartes dans le DOM. Elle doit garantir que les cartes nouvellement inserees ou remplacees respectent immediatement la recherche texte, le select global et les filtres metier actifs.

### Included

- Appeler `applyBoardFilters()` apres creation d'activite.
- Appeler `applyBoardFilters()` apres suppression d'activite.
- Appeler `applyBoardFilters()` apres nettoyage de doublons.
- Appeler `applyBoardFilters()` apres `refreshActivityColumns(activityId)` quand les cartes ont ete ajoutees, remplacees ou supprimees.
- Appeler `applyBoardFilters()` apres deplacement reussi par checkbox ou drag-and-drop via les flux existants.
- Appeler `applyBoardFilters()` apres tri de colonne si necessaire pour conserver compteurs/message coherents.
- Laisser le cache `card._filterData` se reconstruire naturellement sur les nouveaux elements DOM.

### Excluded

- Changer les endpoints AJAX ou leurs payloads.
- Modifier la logique serveur des colonnes virtuelles.
- Ajouter un systeme MutationObserver.
- Changer les regles de matching, la barre de filtres ou le style.
- Refonte des compteurs manuels existants hors suppression des incoherences strictement necessaires.
- Verifier exhaustivement les comportements non lies au filtre; Story 4.2 le fera.

## Acceptance Criteria

1. Apres creation d'une carte, la nouvelle carte est visible ou masquee selon les filtres actifs.
2. Apres creation d'une carte, les compteurs visibles et le message aucun resultat sont recalcules.
3. Apres suppression d'une carte, les compteurs visibles et le message aucun resultat sont recalcules.
4. Apres `cleanupDuplicates()`, les instances restantes respectent les filtres actifs.
5. Apres `refreshActivityColumns(activityId)`, les cartes ajoutees ou remplacees sont soumises aux filtres actifs.
6. Apres un deplacement par checkbox vers ou hors "Termine", le resultat final respecte les filtres actifs.
7. Apres un drag-and-drop reussi entre colonnes, le resultat final respecte les filtres actifs.
8. Un tri de colonne ne reaffiche pas de carte hors filtre et ne laisse pas les compteurs/message incoherents.
9. Les appels a `applyBoardFilters()` interviennent apres les mutations DOM concernees, pas avant.
10. Aucun changement d'endpoint, schema ou modele n'est introduit.

## Tasks / Subtasks

- [x] Task 1 - Ajouter un point d'appel stable pour reappliquer les filtres (AC: 1-9)
  - [x] Ajouter une fonction utilitaire `reapplyBoardFiltersAfterMutation()` ou equivalent.
  - [x] Cette fonction appelle `window.applyBoardFilters()` si disponible, sinon `applyBoardFilters()`.
  - [x] Ne pas dupliquer la logique de matching ou de comptage.
  - [x] Utiliser ce helper dans les callbacks DOM pour rendre les tests structurels simples.

- [x] Task 2 - Brancher creation et suppression (AC: 1, 2, 3, 9)
  - [x] Dans `createActivity()`, appeler le helper apres `column.appendChild(newCard)`.
  - [x] S'assurer que l'appel intervient apres insertion DOM et avant ou apres `newCard.click()` sans casser l'ouverture de modal.
  - [x] Dans `deleteActivity()`, appeler le helper apres suppression de toutes les instances.
  - [x] Eviter les increments/decrements de compteurs qui contredisent `updateVisibleCounts()` si le helper les remplace.

- [x] Task 3 - Brancher cleanup et refresh de colonnes (AC: 4, 5, 9)
  - [x] Dans `cleanupDuplicates()`, appeler le helper apres la boucle de suppression.
  - [x] Dans `refreshActivityColumns(activityId)`, appeler le helper apres la boucle qui ajoute/remplace/supprime les cartes.
  - [x] Verifier que les nouvelles cartes AJAX sont parsees via `parseCardFilterData()` lors du prochain filtrage.

- [x] Task 4 - Brancher les deplacements (AC: 6, 7, 9)
  - [x] Pour `toggleDone()`, s'assurer que le flux de succes aboutit a un helper apres mutation/refresh.
  - [x] Pour le drag-and-drop, s'assurer que le flux de succes aboutit a un helper apres cleanup et refresh.
  - [x] Ne pas appliquer le filtre avant que le DOM cible soit mis a jour.

- [x] Task 5 - Brancher ou verifier le tri (AC: 8)
  - [x] Apres `sortColumn()`, appeler le helper pour recalculer compteurs/message.
  - [x] Verifier que le tri reordonne toutes les cartes presentes mais ne reaffiche pas les cartes `hidden`.

- [x] Task 6 - Ajouter une verification automatisee structurelle (AC: 1-10)
  - [x] Ajouter des assertions dans `web/kanban/tests.py` pour l'existence du helper.
  - [x] Verifier que `createActivity`, `deleteActivity`, `cleanupDuplicates`, `refreshActivityColumns` et `sortColumn` appellent le helper.
  - [x] Verifier que les appels se situent apres `appendChild`, `remove`, `replaceChild` ou le tri selon le cas.
  - [x] Executer `venv/bin/python web/manage.py test kanban`.
  - [x] Executer `venv/bin/python web/manage.py check`.

## Dev Notes

### Current Implementation Context

- `applyBoardFilters()` applique la recherche texte, le select global, les filtres metier, puis met a jour compteurs et message aucun resultat.
- `createActivity()` insere `data.card_html` avec `column.appendChild(newCard)`.
- `deleteActivity()` supprime toutes les instances `.activity-card[data-id="..."]`.
- `cleanupDuplicates()` supprime les instances dupliquees apres deplacement.
- `refreshActivityColumns(activityId)` ajoute, remplace ou supprime des cartes selon les colonnes virtuelles retournees par l'endpoint.
- Les callbacks actuels font encore certains increments/decrements manuels de `.count`; apres cette story, `applyBoardFilters()` doit etre la source finale pour l'affichage des compteurs.

### Recommended Function Contract

Implementation recommandee:

```javascript
function reapplyBoardFiltersAfterMutation() {
    if (window.applyBoardFilters) {
        window.applyBoardFilters();
    } else {
        applyBoardFilters();
    }
}
```

Le helper doit etre appele apres la mutation DOM. Exemple:

```javascript
body.appendChild(newCard);
reapplyBoardFiltersAfterMutation();
```

### Non-Regression Guardrails

- Ne pas ajouter de MutationObserver dans cette story.
- Ne pas recharger la page pour reappliquer le filtre.
- Ne pas changer les endpoints AJAX.
- Ne pas supprimer l'ouverture de modal apres creation.
- Ne pas changer les permissions superuser/non-superuser.
- Ne pas modifier la logique de `matchesItemFilter()` ou `matchesBusinessFilters()`.
- Ne pas s'appuyer sur les compteurs manuels comme source finale apres filtrage.

### Testing Guidance

Le repo n'a pas de runner JavaScript configure. Tests structurels Django acceptables:

- `reapplyBoardFiltersAfterMutation()` existe et appelle `applyBoardFilters`.
- `createActivity()` contient `appendChild(newCard)` puis `reapplyBoardFiltersAfterMutation()`.
- `deleteActivity()` contient `card.remove()` puis `reapplyBoardFiltersAfterMutation()`.
- `cleanupDuplicates()` contient `card.remove()` puis `reapplyBoardFiltersAfterMutation()`.
- `refreshActivityColumns()` contient `replaceChild`, `appendChild` et `remove`, puis `reapplyBoardFiltersAfterMutation()`.
- `sortColumn()` appelle le helper apres avoir re-attache les cartes.

Matrice manuelle minimale:

| Cas | Action | Resultat attendu |
| --- | --- | --- |
| Creation sous filtre actif | Creer une carte | La carte respecte immediatement le filtre courant |
| Suppression sous filtre actif | Supprimer une carte visible | Compteurs/message recalcules |
| Drag-and-drop sous filtre actif | Deplacer une carte | Aucune carte hors filtre ne reapparait |
| Checkbox Termine | Cocher/decocher une carte | Colonnes rafraichies puis filtre reapplique |
| Refresh modal | Modifier un item si refresh declenche | Carte remplacee soumise au filtre courant |
| Tri | Trier une colonne filtree | Cartes masquees restent masquees, compteurs stables |

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

### Manual Fallback

Si aucun test navigateur n'est disponible:

1. Ouvrir le tableau Kanban.
2. Appliquer un filtre metier qui masque certaines cartes.
3. Creer une carte, puis verifier sa visibilite et les compteurs.
4. Supprimer une carte visible, puis verifier les compteurs et le message.
5. Deplacer une carte par drag-and-drop et verifier qu'aucune carte hors filtre ne reapparait.
6. Cocher/decocher une carte vers "Termine" si autorise.
7. Trier une colonne et verifier que les cartes masquees restent masquees.

## Done Checklist

- [x] Helper de reapplication ajoute.
- [x] Creation, suppression, cleanup, refresh et tri appellent le helper apres mutation DOM.
- [x] Les deplacements checkbox et drag-and-drop aboutissent a une reapplication apres mutation/refresh.
- [x] Les compteurs et le message aucun resultat restent coherents apres mutations.
- [x] Aucun endpoint, schema, permission ou matching modifie.
- [x] Verification automatisee executee ou fallback manuel documente.
- [x] Sprint status mis a jour apres implementation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-25: `venv/bin/python web/manage.py test kanban` -> OK, 19 tests.
- 2026-04-25: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- Ajout de `reapplyBoardFiltersAfterMutation()` pour deleguer a `window.applyBoardFilters()` ou `applyBoardFilters()`.
- `sortColumn()` reapplique les filtres apres reattachement des cartes triees.
- `toggleDone()`, `createActivity()`, `deleteActivity()`, `cleanupDuplicates()` et `refreshActivityColumns()` reappliquent les filtres apres mutation DOM.
- Les increments/decrements manuels de compteurs dans les callbacks dynamiques ont ete retires au profit de `applyBoardFilters()` / `updateVisibleCounts()`.
- Aucun endpoint, schema, permission ou matching n'a ete modifie.
- Verification structurelle ajoutee dans `web/kanban/tests.py`.

### File List

- `web/kanban/templates/kanban/board.html`
- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-4.1-reappliquer-filtre-apres-mutations-dom.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-25: Story 4.1 creee avec contexte d'implementation pour reappliquer le filtre centralise apres mutations DOM.
- 2026-04-25: Story 4.1 implementee; helper de reapplication branche apres les mutations DOM.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-25: Clean review. Aucun finding decision-needed, patch ou defer.
- `reapplyBoardFiltersAfterMutation()` delegue correctement au moteur centralise sans dupliquer le matching ou le comptage.
- Les appels sont places apres les mutations DOM ciblees: tri, creation, suppression, cleanup de doublons, refresh de colonnes et flux de deplacement.
- Les increments/decrements manuels de compteurs dans les callbacks dynamiques ont ete retires au profit de `applyBoardFilters()` / `updateVisibleCounts()`.
- Aucun endpoint, schema, permission ou logique de matching n'a ete modifie.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
