---
title: 'Story 3.1 - Ajouter la barre de filtres metier'
story_id: '3.1'
epic: 'Epic 3 - Interface de filtre et feedback utilisateur'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'done'
workflow: 'bmad-dev-story'
agent: 'dev'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
source_story_2_1: '_bmad-output/implementation-artifacts/story-2.1-fonctions-correspondance-exactes.md'
source_story_2_2: '_bmad-output/implementation-artifacts/story-2.2-combiner-filtre-metier-recherche-texte.md'
---

# Story 3.1 - Ajouter la barre de filtres metier

## Status

Done.

## Story

**En tant que** utilisateur du tableau Kanban,  
**je veux** selectionner un traitement, une tache et leurs etats directement au-dessus du tableau,  
**afin de** filtrer sans quitter ma vue de travail.

## Scope

Cette story ajoute la barre de filtres metier dans `board.html` et la branche sur le moteur de filtrage centralise. Elle rend les controles utilisables et immediats, mais laisse le recalcul des compteurs et le message "aucun resultat" a Story 3.2, et le polissage CSS complet a Story 3.3.

### Included

- Ajouter une barre de filtres metier sous l'en-tete de page et avant `.board-container`.
- Ajouter un controle Traitement alimente par `filter_traitements`.
- Ajouter un controle Tache alimente par `filter_taches`.
- Ajouter les cases d'etat "Fait" et "Restant a faire" pour chaque axe.
- Desactiver les cases d'etat d'un axe quand son libelle est vide.
- Ajouter un bouton de reinitialisation des filtres metier.
- Mettre a jour `window.businessFilterState` depuis les controles.
- Appeler `window.applyBoardFilters()` a chaque changement.
- Conserver la recherche texte existante independante.

### Excluded

- Recalculer les compteurs de colonne selon les cartes visibles.
- Ajouter ou afficher le message global "aucun resultat".
- Ajouter le style final responsive dans `style.css`.
- Supprimer ou remplacer le select global historique dans l'en-tete.
- Reappliquer automatiquement les filtres apres mutations DOM.
- Modifier `views.py`, le schema SQLite ou les endpoints.

## Acceptance Criteria

1. Le controle Traitement affiche les options issues de `filter_traitements`.
2. Le controle Tache affiche les options issues de `filter_taches`.
3. Les cases d'etat Traitement "Fait" et "Restant a faire" sont atteignables au clavier.
4. Les cases d'etat Tache "Fait" et "Restant a faire" sont atteignables au clavier.
5. Les cases d'etat Traitement sont desactivees avec `disabled` quand aucun traitement n'est selectionne.
6. Les cases d'etat Tache sont desactivees avec `disabled` quand aucune tache n'est selectionnee.
7. Selectionner ou vider un traitement applique immediatement les filtres.
8. Selectionner ou vider une tache applique immediatement les filtres.
9. Cocher ou decocher une case d'etat applique immediatement les filtres.
10. Le bouton de reinitialisation efface les deux libelles et les quatre cases d'etat.
11. Le bouton de reinitialisation applique immediatement les filtres apres remise a zero.
12. Le bouton de reinitialisation ne vide pas `#global-search` et ne modifie pas `#global-filter`.
13. Sans libelle metier selectionne, la barre est neutre et ne masque aucune carte au-dela de la recherche texte / select global existants.

## Tasks / Subtasks

- [x] Task 1 - Ajouter le markup de la barre dans `board.html` (AC: 1, 2, 3, 4)
  - [x] Inserer la barre avant `.board-container`.
  - [x] Ajouter un groupe Traitement avec `label`, controle de selection et deux cases d'etat.
  - [x] Ajouter un groupe Tache avec `label`, controle de selection et deux cases d'etat.
  - [x] Ajouter le bouton `Reinitialiser les filtres`.
  - [x] Utiliser des ids stables pour les hooks JS et les tests.

- [x] Task 2 - Alimenter les controles avec les catalogues existants (AC: 1, 2)
  - [x] Utiliser `filter_traitements` pour les options du controle Traitement.
  - [x] Utiliser `filter_taches` pour les options du controle Tache.
  - [x] Conserver une option vide neutre au debut de chaque controle.
  - [x] Ne pas ajouter de requete AJAX ou endpoint.

- [x] Task 3 - Brancher les controles sur l'etat metier (AC: 7, 8, 9, 13)
  - [x] Ajouter une fonction `updateBusinessFilterStateFromControls()`.
  - [x] Renseigner `window.businessFilterState` avec la forme attendue par Story 2.1 / 2.2.
  - [x] Appeler `window.applyBoardFilters()` apres chaque mise a jour.
  - [x] Ne pas modifier `#global-search` ni `#global-filter`.

- [x] Task 4 - Gerer les cases d'etat actives/desactivees (AC: 5, 6)
  - [x] Ajouter une fonction `syncBusinessFilterControlState()` ou equivalent.
  - [x] Desactiver et decocher les cases Traitement si le controle Traitement est vide.
  - [x] Desactiver et decocher les cases Tache si le controle Tache est vide.
  - [x] S'assurer que l'etat disabled est present dans le DOM, pas seulement visuel.

- [x] Task 5 - Ajouter le reset metier (AC: 10, 11, 12, 13)
  - [x] Vider les controles Traitement et Tache.
  - [x] Decocher les quatre cases d'etat.
  - [x] Desactiver les cases d'etat apres reset.
  - [x] Appeler `applyBoardFilters()` apres reset.
  - [x] Verifier que `#global-search` et `#global-filter` conservent leurs valeurs.

- [x] Task 6 - Ajouter une verification automatisee structurelle (AC: 1-13)
  - [x] Ajouter des assertions dans `web/kanban/tests.py` pour le markup de la barre.
  - [x] Verifier que les controles utilisent `filter_traitements` et `filter_taches`.
  - [x] Verifier que les fonctions JS de branchement existent.
  - [x] Verifier que le reset ne reference pas `global-search.value = ''` ni `global-filter.value`.
  - [x] Executer `venv/bin/python web/manage.py test kanban`.
  - [x] Executer `venv/bin/python web/manage.py check`.

## Dev Notes

### Current Implementation Context

- `web/kanban/templates/kanban/board.html` commence actuellement par `.board-container`; la barre doit etre inseree avant ce conteneur.
- `base.html` conserve la recherche texte et le select global historique dans l'en-tete.
- Story 2.2 a centralise la visibilite dans `window.applyBoardFilters()`.
- `getBusinessFilterState()` lit `window.businessFilterState` avec la forme:

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

- `applyBoardFilters()` relit aussi `#global-search` et `#global-filter`, donc la barre metier doit uniquement mettre a jour l'etat metier et appeler cette fonction.

### Recommended Markup Contract

Ids recommandes:

- `business-filter-bar`
- `business-filter-traitement`
- `business-filter-traitement-done`
- `business-filter-traitement-pending`
- `business-filter-tache`
- `business-filter-tache-done`
- `business-filter-tache-pending`
- `business-filter-reset`

Un `select` simple est suffisant pour cette story. Exemple attendu:

```html
<select id="business-filter-traitement">
  <option value="">Traitement</option>
  {% for t in filter_traitements %}
  <option value="{{ t }}">{{ t }}</option>
  {% endfor %}
</select>
```

### Recommended JS Contract

Implementation recommandee:

```javascript
function updateBusinessFilterStateFromControls() {
    syncBusinessFilterControlState();
    window.businessFilterState = {
        traitementLabel: traitementSelect.value,
        traitementDone: traitementDoneCheckbox.checked,
        traitementPending: traitementPendingCheckbox.checked,
        tacheLabel: tacheSelect.value,
        tacheDone: tacheDoneCheckbox.checked,
        tachePending: tachePendingCheckbox.checked
    };
    window.applyBoardFilters();
}
```

Lorsque le libelle d'un axe devient vide, decocher puis desactiver les cases de cet axe avant de reconstruire l'etat.

### Non-Regression Guardrails

- Ne pas changer le comportement du select global dans `base.html`.
- Ne pas vider la recherche texte existante lors du reset metier.
- Ne pas modifier la logique de matching exact de `matchesItemFilter()`.
- Ne pas utiliser une comparaison texte libre ou `includes()` pour les libelles metier.
- Ne pas ajouter de CSS final dans cette story sauf un minimum strictement necessaire au layout; Story 3.3 porte le style.
- Ne pas introduire de dependance JS, bundler ou fichier JS separe.

### Testing Guidance

Le repo n'a pas de runner JavaScript configure. Tests structurels Django acceptables:

- Le template contient la barre et les ids stables.
- Les options de select sont generees depuis `filter_traitements` et `filter_taches`.
- Les checkboxes ont `type="checkbox"` et des labels associes.
- Les checkboxes sont initialisees `disabled`.
- Le JS ajoute des listeners `change` aux six controles.
- Le reset remet les controles metier a zero sans reference a `global-search` ni `global-filter`.

Matrice manuelle minimale:

| Cas | Action | Resultat attendu |
| --- | --- | --- |
| Etat initial | Charger le tableau | Cases d'etat desactivees, aucun filtre metier actif |
| Traitement seul | Choisir un traitement | Filtre presence applique, cases traitement actives |
| Traitement fait | Cocher Fait | Cartes avec traitement fait visibles |
| Traitement restant | Cocher Restant a faire seul | Cartes avec traitement restant visibles |
| Tache seule | Choisir une tache | Filtre presence applique, cases tache actives |
| Traitement + tache | Choisir les deux axes | Logique ET appliquee |
| Vider libelle | Vider traitement | Cases traitement desactivees et decochees |
| Reset | Cliquer reset | Deux libelles vides, quatre cases decochees/desactivees |
| Reset + recherche | Recherche texte active puis reset | Recherche texte conservee |
| Clavier | Tabuler tous controles | Ordre: traitement, etats, tache, etats, reset, tableau |

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

### Manual Fallback

Si aucun test navigateur n'est disponible:

1. Ouvrir le tableau Kanban.
2. Tabuler de la recherche globale vers la barre metier et le tableau.
3. Selectionner un traitement puis verifier que les cases Traitement deviennent actives.
4. Cocher/decocher Fait et Restant a faire, verifier que les cartes changent immediatement.
5. Selectionner une tache et verifier la combinaison ET avec le traitement.
6. Cliquer `Reinitialiser les filtres` et verifier que la recherche texte reste en place.
7. Reduire la largeur de la fenetre et verifier que les controles restent utilisables, meme sans polissage CSS final.

## Done Checklist

- [x] Barre de filtres metier ajoutee avant `.board-container`.
- [x] Controles Traitement et Tache alimentes par les catalogues existants.
- [x] Cases Fait/Restant accessibles et desactivees sans libelle.
- [x] Chaque changement met a jour `window.businessFilterState` et appelle `applyBoardFilters()`.
- [x] Reset metier efface uniquement les controles metier.
- [x] Recherche texte et select global restent independants.
- [x] Aucun compteur, message aucun resultat, schema ou endpoint ajoute.
- [x] Verification automatisee executee ou fallback manuel documente.
- [x] Sprint status mis a jour apres implementation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-25: `venv/bin/python web/manage.py test kanban` -> OK, 12 tests.
- 2026-04-25: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- Ajout de `#business-filter-bar` avant `.board-container`.
- Ajout de deux `select` alimentes par `filter_traitements` et `filter_taches`.
- Ajout des quatre cases Fait / Restant a faire, initialisees avec `disabled`.
- Ajout de `syncBusinessFilterControlState()`, `updateBusinessFilterStateFromControls()` et `resetBusinessFilters()`.
- Chaque changement de controle met a jour `window.businessFilterState` et appelle `window.applyBoardFilters()`.
- Le reset vide uniquement les controles metier et ne reference pas `#global-search` ni `#global-filter`.
- Verification automatisee structurelle ajoutee dans `web/kanban/tests.py`.

### File List

- `web/kanban/templates/kanban/board.html`
- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-3.1-ajouter-barre-filtres-metier.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-25: Story 3.1 creee avec contexte d'implementation pour ajouter la barre de filtres metier et la brancher sur le moteur centralise.
- 2026-04-25: Story 3.1 implementee; barre metier ajoutee et branchee sur `window.businessFilterState` / `applyBoardFilters()`.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-25: Clean review. Aucun finding decision-needed, patch ou defer.
- La barre metier est inseree avant `.board-container` et utilise les catalogues `filter_traitements` / `filter_taches`.
- Les quatre cases d'etat sont initialisees `disabled`, deviennent actives uniquement avec un libelle, et sont decochees quand l'axe redevient vide.
- `window.businessFilterState` est reconstruit depuis les controles et applique via `window.applyBoardFilters()` sans modifier `#global-search` ni `#global-filter`.
- Le reset vide uniquement les controles metier puis reapplique le filtre centralise.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
