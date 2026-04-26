---
title: 'Story 4.2 - Preserver les comportements existants non lies au filtre'
story_id: '4.2'
epic: 'Epic 4 - Integration avec les interactions dynamiques du tableau'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-26'
status: 'done'
workflow: 'bmad-create-story'
agent: 'sm'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
source_prd: '_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
source_story_4_1: '_bmad-output/implementation-artifacts/story-4.1-reappliquer-filtre-apres-mutations-dom.md'
---

# Story 4.2 - Preserver les comportements existants non lies au filtre

## Status

Done.

## Story

**En tant que** utilisateur existant,  
**je veux** que le tri, les modales, le drag-and-drop et les colonnes virtuelles continuent de fonctionner,  
**afin que** le nouveau filtre n'introduise pas de regression.

## Scope

Cette story est une story de non-regression ciblee. Elle ne doit pas refondre le filtrage metier deja livre; elle doit verifier et corriger uniquement les comportements existants qui auraient ete fragilises par la centralisation de `applyBoardFilters()`, l'usage de `card.hidden`, la reapplication apres mutation DOM et les nouveaux attributs JSON par carte.

### Included

- Verifier et corriger si necessaire les tris de colonne par date, nom, traitements restants et taches restantes.
- Verifier et corriger si necessaire l'ouverture de modal au clic carte apres filtrage, creation, remplacement AJAX et tri.
- Verifier et corriger si necessaire le drag-and-drop superuser entre colonnes et le drag des colonnes.
- Verifier et corriger si necessaire le comportement non-superuser: drag des cartes/colonnes desactive et checkbox terminee desactivee.
- Verifier que les colonnes virtuelles affichent les memes activites quand aucun filtre metier, recherche texte ou filtre global n'est actif.
- Ajouter une verification automatisee structurelle dans `web/kanban/tests.py` pour les points non-regression testables sans navigateur.
- Documenter la passe manuelle minimale dans le record de story lors de l'implementation.

### Excluded

- Changer la logique serveur des colonnes virtuelles dans `board()` ou `get_activity_columns()`, sauf correction directe d'une regression prouvee.
- Changer les endpoints AJAX, leurs URLs ou leurs payloads.
- Modifier le schema SQLite, les modeles Django ou les migrations.
- Ajouter une nouvelle dependance JS, un framework de test navigateur ou un endpoint dedie.
- Refaire la barre de filtres, les regles de matching exact ou le style responsive.
- Executer la matrice complete AC-01 a AC-12 du PRD; Story 5.2 la couvre.

## Acceptance Criteria

1. Le tri par date ascendant et descendant fonctionne encore sur les cartes presentes dans une colonne.
2. Le tri par nom ascendant et descendant fonctionne encore et utilise `data-name` comme avant.
3. Le tri par traitements restants et taches restantes fonctionne encore avec `data-pending-traitements` et `data-pending-taches`.
4. Trier une colonne ne change pas l'etat des filtres actifs et ne reaffiche pas les cartes masquees.
5. Le clic sur une carte ouvre toujours la modal de detail via la delegation de `.board-container`.
6. Le clic sur le bouton supprimer ne declenche pas l'ouverture de modal.
7. Apres creation d'une carte, le clic automatique sur la nouvelle carte ouvre toujours la modal d'edition/detail.
8. Le drag-and-drop superuser entre colonnes appelle toujours `move_activity`, nettoie/rafraichit les instances et conserve l'etat de filtre courant.
9. Le drag des colonnes superuser appelle toujours `update_column_order`.
10. Pour un non-superuser, le drag des colonnes/cartes reste desactive et les checkbox `.done-checkbox` restent desactivees.
11. Sans filtre metier, sans recherche texte et avec le filtre global sur `all`, les colonnes virtuelles affichent les memes cartes qu'avant l'ajout du filtre.
12. Aucun endpoint, schema, modele ou contrat de payload n'est modifie.

## Tasks / Subtasks

- [x] Task 1 - Verifier les tris existants (AC: 1, 2, 3, 4)
  - [x] Confirmer que les menus appellent encore `sortColumn(columnId, criteria, direction)` pour `date`, `name`, `pending-traitements`, `pending-taches`.
  - [x] Confirmer que `sortColumn()` lit encore les attributs `data-date`, `data-name`, `data-pending-traitements`, `data-pending-taches`.
  - [x] Confirmer que les tris numeriques restent numeriques pour traitements/taches et que les tris date/nom restent lexicographiques.
  - [x] Conserver l'appel a `reapplyBoardFiltersAfterMutation()` apres reattachement des cartes triees.
  - [x] Ajouter ou ajuster un test structurel qui protege les criteres de tri et l'appel post-tri.

- [x] Task 2 - Verifier les modales et les clics carte (AC: 5, 6, 7)
  - [x] Confirmer que la delegation de clic reste sur `.board-container` et cible `.activity-card`.
  - [x] Confirmer que `.delete-activity-btn` court-circuite l'ouverture de modal.
  - [x] Confirmer que `createActivity()` insere `newCard`, reapplique les filtres, puis execute encore `newCard.click()`.
  - [x] Verifier que les cartes remplacees par `refreshActivityColumns()` restent compatibles avec la delegation de clic.
  - [x] Ajouter ou ajuster un test structurel pour ces invariants.

- [x] Task 3 - Verifier drag-and-drop et permissions (AC: 8, 9, 10)
  - [x] Confirmer que `Sortable.create(board, { disabled: ... })` reste conditionne par `user.is_superuser`.
  - [x] Confirmer que chaque `.column-body` cree un Sortable avec `group: 'shared'`.
  - [x] Confirmer que le drop inter-colonnes appelle encore `{% url "kanban:move_activity" %}` avec `activity_id` et `column_id`.
  - [x] Confirmer que le succes appelle encore `cleanupDuplicates(activityId, itemEl)` puis `refreshActivityColumns(activityId)`.
  - [x] Confirmer que `card_snippet.html` garde `{% if not user.is_superuser %}disabled{% endif %}` sur `.done-checkbox`.
  - [x] Ajouter ou ajuster un test structurel pour les permissions et callbacks Sortable.

- [x] Task 4 - Verifier les colonnes virtuelles sans filtre actif (AC: 11, 12)
  - [x] Confirmer que `applyBoardFilters()` avec etat vide ne masque pas de carte: `matchesSearchText` true sans query, `matchesLegacyGlobalFilter` true avec `all`, `matchesBusinessFilters` true sans labels.
  - [x] Confirmer que `board()` conserve les requetes existantes des colonnes virtuelles "Traitements", "Taches", "CTA", "Reparations", "En attente" et "En cours".
  - [x] Ne pas modifier les endpoints ni `get_activity_columns()` sauf regression specifique prouvee.
  - [x] Ajouter ou ajuster un test structurel qui protege l'etat neutre `all` + filtres metier vides.

- [x] Task 5 - Executer la verification (AC: 1-12)
  - [x] Executer `venv/bin/python web/manage.py test kanban`.
  - [x] Executer `venv/bin/python web/manage.py check`.
  - [x] Documenter la limite de passe manuelle sans filtre actif si aucune session navigateur n'est disponible.
  - [x] Documenter dans le Dev Agent Record les commandes executees, les limites manuelles et tout ecart observe.

## Dev Notes

### Current Implementation Context

- `base.html` delegue maintenant la recherche globale et le select `#global-filter` a `window.applyBoardFilters()`.
- `board.html` expose les helpers `parseCardFilterData`, `matchesItemFilter`, `matchesLegacyGlobalFilter`, `matchesBusinessFilters`, `updateVisibleCounts`, `applyBoardFilters` et `reapplyBoardFiltersAfterMutation`.
- Les cartes sont masquees via `card.hidden`, pas via `style.display`; les colonnes restent visibles et les compteurs sont recalcules depuis `.activity-card` non masquees.
- `sortColumn()` reattache les cartes dans `.column-body` puis appelle `reapplyBoardFiltersAfterMutation()`.
- `createActivity()`, `deleteActivity()`, `cleanupDuplicates()`, `refreshActivityColumns()` et `toggleDone()` appellent deja le helper apres mutation DOM depuis Story 4.1.
- `card_snippet.html` conserve les attributs historiques `data-pending-traitements`, `data-pending-taches`, `data-pending-traitement-names` et `data-pending-tache-names`, et ajoute `data-traitements` / `data-taches`.

### Files To Inspect Before Editing

- `web/kanban/templates/kanban/board.html`
  - Tri: menu `.sort-menu`, `sortColumn()`, attributs `data-*`.
  - Modal: delegation de clic sur `.board-container`, `openModal()`, fetch `/activity/${activityId}/`.
  - Mutations: `createActivity()`, `deleteActivity()`, `cleanupDuplicates()`, `refreshActivityColumns()`, `toggleDone()`.
  - Permissions JS: `Sortable.create(board, { disabled: {% if not user.is_superuser %}true{% else %}false{% endif %} })`.
- `web/kanban/templates/kanban/base.html`
  - Recherche globale et select global ne doivent pas reprendre une logique concurrente de masquage.
- `web/kanban/templates/kanban/card_snippet.html`
  - Les attributs de tri et la checkbox superuser/non-superuser doivent rester presents.
- `web/kanban/views.py`
  - Les requetes de colonnes virtuelles doivent rester stables; ne pas les refactorer dans cette story.
- `web/kanban/tests.py`
  - Ajouter des tests structurels dans `BoardBusinessFilterScriptTests`, en suivant les patterns existants.

### Non-Regression Guardrails

- Ne pas remplacer la delegation de clic par des listeners attaches carte par carte; les cartes AJAX doivent continuer de fonctionner sans rebinding.
- Ne pas retirer `data-pending-traitements` ou `data-pending-taches`; ils sont encore le contrat des tris numeriques.
- Ne pas faire dependre le tri des tableaux JSON `data-traitements` / `data-taches`.
- Ne pas utiliser `style.display` en parallele de `hidden`; cela recréerait deux sources de verite.
- Ne pas masquer `.kanban-column`; les colonnes virtuelles doivent rester visibles meme avec zero carte visible.
- Ne pas changer les URLs Django existantes: `move_activity`, `update_column_order`, `/api/activity/create/`, `/api/activity/<id>/delete/`, `/api/activity/<id>/columns/`, `/activity/<id>/`.
- Ne pas ajouter de migration ou de nouveau modele; le sprint exclut explicitement les changements de schema.

### Testing Guidance

Tests structurels recommandes dans `web/kanban/tests.py` :

- `sortColumn()` contient les criteres `pending-traitements` et `pending-taches`, lit `data-${criteria}`, utilise `parseFloat` pour les tris numeriques et appelle `reapplyBoardFiltersAfterMutation()` apres `appendChild`.
- La delegation modal reste attachee a `.board-container`, cherche `.activity-card`, ignore `.delete-activity-btn`, puis appelle `openModal()` et fetch `/activity/${activityId}/`.
- `createActivity()` appelle `column.appendChild(newCard)`, `reapplyBoardFiltersAfterMutation()` puis `newCard.click()`.
- Les callbacks Sortable gardent `disabled` conditionne par `user.is_superuser`, `group: 'shared'`, l'appel a `move_activity`, puis `cleanupDuplicates()` et `refreshActivityColumns()`.
- `card_snippet.html` garde `data-pending-traitements`, `data-pending-taches`, `.done-checkbox` et le `disabled` non-superuser.
- L'etat neutre de filtre reste vrai: `matchesLegacyGlobalFilter()` retourne true pour `all`, `matchesItemFilter()` retourne true sans label, et `getBusinessFilterState()` initialise les labels vides.

Matrice manuelle minimale :

| Cas | Action | Resultat attendu |
| --- | --- | --- |
| Vue neutre | Ouvrir le board avec recherche vide et global `Tous` | Les colonnes virtuelles affichent les cartes attendues |
| Tri date | Trier date asc/desc | Ordre change, cartes masquees restent masquees |
| Tri nom | Trier nom asc/desc | Ordre change selon `data-name` |
| Tri compteurs | Trier traitements/taches croissant/decroissant | Ordre numerique selon compteurs restants |
| Modal | Cliquer une carte | Modal charge `/activity/<id>/` |
| Supprimer | Cliquer la corbeille puis annuler | Pas d'ouverture de modal |
| Creation | Creer une carte superuser | Carte ajoutee, filtre reapplique, modal ouverte |
| Drag carte | Deplacer une carte superuser | Endpoint move appele, colonnes virtuelles rafraichies |
| Non-superuser | Ouvrir avec utilisateur non-superuser | Drag/checkbox restent desactives |

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

### Manual Fallback

Si aucune session navigateur superuser/non-superuser n'est disponible pendant l'implementation, documenter explicitement cette limite dans le Dev Agent Record et executer au minimum les tests structurels ci-dessus. La validation fonctionnelle complete sera reprise dans Story 5.2.

## Done Checklist

- [x] Tris date, nom, traitements et taches proteges par verification.
- [x] Modal carte, suppression et creation proteges par verification.
- [x] Drag-and-drop et permissions superuser/non-superuser proteges par verification.
- [x] Vue neutre sans filtre preservee.
- [x] Aucun endpoint, schema, modele ou payload modifie.
- [x] Verification automatisee executee ou limite documentee.
- [x] Sprint status mis a jour apres implementation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-26: `venv/bin/python web/manage.py test kanban` -> OK, 24 tests.
- 2026-04-26: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- Ajout de tests structurels pour proteger les contrats de tri `date`, `name`, `pending-traitements` et `pending-taches`.
- Ajout de tests structurels pour la delegation de modal, l'exclusion du bouton supprimer et le clic automatique apres creation.
- Ajout de tests structurels pour les callbacks Sortable, les permissions superuser/non-superuser et la checkbox terminee.
- Ajout de tests structurels pour l'etat neutre du filtrage et la presence des colonnes virtuelles/endpoints existants.
- Aucune modification fonctionnelle de `board.html`, `base.html`, `card_snippet.html`, `views.py`, endpoints, modeles ou schema.
- Passe manuelle navigateur non executee dans cette session; la verification est couverte par tests structurels et sera reprise fonctionnellement en Story 5.2.

### File List

- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-4.2-preserver-comportements-existants-non-lies-filtre.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-26: Story 4.2 creee avec contexte de non-regression pour tris, modales, drag-and-drop, permissions et colonnes virtuelles.
- 2026-04-26: Story 4.2 implementee; tests de garde non-regression ajoutes et validations Django executees.
- 2026-04-26: Code review approuvee; corrections d'artefact appliquees pour aligner le statut frontmatter et la limite de verification manuelle.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-26: Correction appliquee pendant review: le frontmatter de la story est aligne sur le statut final `done`.
- 2026-04-26: Correction appliquee pendant review: la sous-tache de verification manuelle indique maintenant la limite documentee, au lieu de pretendre qu'une passe navigateur a ete executee.
- Les tests ajoutes ciblent les contrats de non-regression demandes par Story 4.2: tri, delegation modal, creation, callbacks Sortable, permissions, etat neutre du filtre, colonnes virtuelles et endpoints existants.
- Aucun changement fonctionnel de `board.html`, `base.html`, `card_snippet.html`, `views.py`, endpoint, modele ou schema n'a ete introduit par cette story.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
