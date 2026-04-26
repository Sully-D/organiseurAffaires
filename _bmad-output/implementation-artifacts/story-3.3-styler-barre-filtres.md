---
title: 'Story 3.3 - Styler la barre de filtres dans la grammaire visuelle existante'
story_id: '3.3'
epic: 'Epic 3 - Interface de filtre et feedback utilisateur'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'done'
workflow: 'bmad-dev-story'
agent: 'dev'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_story_3_1: '_bmad-output/implementation-artifacts/story-3.1-ajouter-barre-filtres-metier.md'
source_story_3_2: '_bmad-output/implementation-artifacts/story-3.2-compteurs-et-aucun-resultat.md'
---

# Story 3.3 - Styler la barre de filtres dans la grammaire visuelle existante

## Status

Done.

## Story

**En tant que** utilisateur,  
**je veux** une barre de filtres compacte et coherente avec le tableau,  
**afin de** l'utiliser sans perdre la lisibilite du Kanban.

## Scope

Cette story ajoute le style CSS de la barre de filtres metier, de ses controles et du message aucun resultat. Elle doit garder la densite et le scroll horizontal du tableau Kanban, tout en rendant la barre utilisable sur desktop et largeur reduite.

### Included

- Styler `#business-filter-bar` dans la grammaire visuelle sombre existante.
- Styler `.business-filter-group`, les labels, les `select`, les cases et le bouton reset.
- Donner aux controles une hauteur cible suffisante et stable.
- Eviter les chevauchements et debordements de texte.
- Faire passer la barre en pile sur largeur reduite.
- Styler `#noFilterResults` de facon visible mais non intrusive.
- Garder `.board-container` horizontalement scrollable.
- Ajouter ou ajuster des tests structurels CSS si pertinent.

### Excluded

- Modifier le markup de `board.html` sauf correction minimale necessaire a l'accessibilite ou aux hooks CSS.
- Modifier la logique de filtrage, les compteurs ou le message.
- Supprimer le select global historique dans l'en-tete.
- Changer le rendu des cartes ou des colonnes hors espace necessaire.
- Ajouter une dependance CSS/JS ou un framework.

## Acceptance Criteria

1. La barre de filtres ne chevauche pas le header, le tableau ou ses controles sur desktop.
2. La barre utilise le theme sombre existant: fond proche de `--bg-secondary`, bordure discrete et texte lisible.
3. Les controles ont une hauteur minimale d'au moins `36px`.
4. Les `select` ont une largeur stable et ne font pas deborder la barre.
5. Les libelles longs dans les selects sont tronques ou contenus sans casser le layout.
6. Les groupes Traitement et Tache restent lisibles et distincts.
7. Le bouton reset est visuellement identifiable et garde une hauteur coherente avec les autres controles.
8. A largeur reduite, la barre passe en pile ou en wrapping propre, sans chevauchement.
9. A largeur reduite, les controles peuvent occuper toute la largeur disponible.
10. Le tableau Kanban conserve son scroll horizontal.
11. Le message `#noFilterResults` est lisible, visible quand affiche, et ne masque pas les colonnes.
12. Aucun changement de comportement JavaScript n'est introduit.

## Tasks / Subtasks

- [x] Task 1 - Ajouter le style desktop de la barre (AC: 1, 2, 6)
  - [x] Ajouter une section CSS dediee aux filtres metier dans `web/kanban/static/kanban/css/style.css`.
  - [x] Styler `#business-filter-bar` avec flex, gap, fond sombre, bordure discrete et padding compact.
  - [x] Styler `.business-filter-group` pour aligner label, select et cases sans chevauchement.
  - [x] Utiliser les variables existantes `--bg-secondary`, `--text-primary`, `--text-secondary`, `--accent`, `--glass-border`.

- [x] Task 2 - Styler les controles (AC: 3, 4, 5, 7)
  - [x] Donner aux selects et au bouton une hauteur minimale stable.
  - [x] Definir largeur/min-width/max-width des selects.
  - [x] Gerer `text-overflow`, `white-space` et `overflow` pour les libelles longs.
  - [x] Styler les labels de checkbox avec une taille compacte et lisible.
  - [x] Ajouter des etats focus visibles pour clavier.
  - [x] Styler l'etat disabled des checkboxes sans les rendre invisibles.

- [x] Task 3 - Styler le message aucun resultat (AC: 11)
  - [x] Ajouter un style pour `#noFilterResults`.
  - [x] Le rendre visible sans occlure le tableau.
  - [x] Conserver `hidden` comme mecanisme d'affichage.

- [x] Task 4 - Ajouter le responsive (AC: 8, 9, 10)
  - [x] Ajouter une media query pour largeur reduite.
  - [x] Faire passer `#business-filter-bar` en pile ou wrapping vertical.
  - [x] Permettre aux groupes et selects de prendre toute la largeur disponible.
  - [x] Ne pas modifier le scroll horizontal de `.board-container`.

- [x] Task 5 - Ajouter ou ajuster la verification structurelle (AC: 1-12)
  - [x] Ajouter des assertions dans `web/kanban/tests.py` pour les selecteurs CSS principaux.
  - [x] Verifier qu'une media query existe pour la barre.
  - [x] Verifier que `.board-container` conserve `overflow-x: auto`.
  - [x] Verifier qu'aucune regle CSS ne masque `.kanban-column` pour les filtres.
  - [x] Executer `venv/bin/python web/manage.py test kanban`.
  - [x] Executer `venv/bin/python web/manage.py check`.

## Dev Notes

### Current Implementation Context

- `web/kanban/static/kanban/css/style.css` contient deja:
  - variables CSS de theme sombre;
  - `.main-content { overflow: hidden; padding: 1rem; }`;
  - `.board-container { display: flex; gap: 1.5rem; height: 100%; overflow-x: auto; }`;
  - `.kanban-column` avec largeur fixe 300px et hauteur 100%.
- `board.html` contient deja:
  - `#business-filter-bar`;
  - `.business-filter-group`;
  - `.business-filter-select`;
  - `#business-filter-reset`;
  - `#noFilterResults`.
- Le style ne doit pas remettre en cause le scroll horizontal existant ni masquer les colonnes.

### Recommended CSS Direction

Approche recommandee:

```css
.business-filter-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}
```

Le select peut utiliser:

```css
.business-filter-select {
    min-height: 38px;
    max-width: 260px;
    text-overflow: ellipsis;
}
```

Le bouton reset doit rester un vrai bouton texte, pas une icone, car son action est destructive pour l'etat des filtres metier mais ne touche pas la recherche texte.

### Non-Regression Guardrails

- Ne pas changer `body` ou `.app-container` pour ajouter du scroll vertical global.
- Ne pas supprimer `overflow-x: auto` de `.board-container`.
- Ne pas modifier `min-width` / `max-width` des colonnes dans cette story.
- Ne pas utiliser de grandes ombres, gradients ou effets decoratifs qui dominent le tableau.
- Ne pas transformer la barre en card imbriquee dans une autre card; elle doit rester un outil compact.
- Ne pas ajouter de CSS qui cible `.activity-card[hidden]` pour les reafficher.

### Testing Guidance

Tests structurels Django acceptables:

- `style.css` contient `.business-filter-bar`, `.business-filter-group`, `.business-filter-select`, `#business-filter-reset`, `#noFilterResults`.
- `.business-filter-select` ou les controles ont `min-height`.
- Une media query cible une largeur reduite et ajuste la barre.
- `.board-container` conserve `overflow-x: auto`.
- Aucune regle CSS ne contient `.kanban-column { display: none` ni `.kanban-column[hidden]` dans le contexte des filtres.

Matrice manuelle minimale:

| Cas | Action | Resultat attendu |
| --- | --- | --- |
| Desktop | Ouvrir le tableau | Barre compacte, controles alignes, tableau visible |
| Libelle long | Choisir un long traitement/tache | Pas de debordement hors controle |
| Focus clavier | Tabuler dans la barre | Focus visible |
| Disabled | Aucun libelle choisi | Cases disabled visibles mais attenuees |
| Largeur reduite | Reduire la fenetre | Groupes empiles/wrappes proprement |
| Scroll Kanban | Largeur reduite avec plusieurs colonnes | Scroll horizontal conserve |
| Aucun resultat | Provoquer zero carte visible | Message lisible et colonnes non masquees |

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

### Manual Fallback

Si aucun test visuel automatise n'est disponible:

1. Ouvrir le tableau sur une largeur desktop.
2. Verifier que la barre ne chevauche ni le header ni les colonnes.
3. Tester un libelle long dans chaque select.
4. Tabuler dans les controles et verifier le focus.
5. Reduire la fenetre a une largeur mobile/tablette.
6. Verifier que la barre se replie proprement et que le tableau garde son scroll horizontal.
7. Provoquer un zero resultat et verifier que le message reste lisible.

## Done Checklist

- [x] Style desktop de la barre ajoute.
- [x] Controles compacts, lisibles et avec hauteur suffisante.
- [x] Responsive largeur reduite ajoute.
- [x] Message aucun resultat style sans occlusion.
- [x] Scroll horizontal du Kanban preserve.
- [x] Aucun changement JS ou backend introduit.
- [x] Verification automatisee executee ou fallback manuel documente.
- [x] Sprint status mis a jour apres implementation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-25: `venv/bin/python web/manage.py test kanban` -> OK, 16 tests.
- 2026-04-25: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- Ajout d'une section CSS Business Filters dans `style.css`.
- `#business-filter-bar` utilise un layout flex wrap, fond sombre, bordure discrete et padding compact.
- Les selects, cases et bouton reset ont une hauteur minimale coherente, des etats focus visibles et une gestion des libelles longs.
- `#noFilterResults` est style sans occlure les colonnes et conserve le mecanisme `hidden`.
- Une media query `max-width: 760px` empile la barre et donne toute la largeur aux selects et au reset.
- Le scroll horizontal de `.board-container` reste `overflow-x: auto`.
- Verification structurelle CSS ajoutee dans `web/kanban/tests.py`.

### File List

- `web/kanban/static/kanban/css/style.css`
- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-3.3-styler-barre-filtres.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-25: Story 3.3 creee avec contexte d'implementation pour styler la barre de filtres, les controles et le message aucun resultat.
- 2026-04-25: Story 3.3 implementee; style responsive de la barre, controles et message ajoute.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-25: Clean review. Aucun finding decision-needed, patch ou defer.
- Les styles ajoutés sont bornes a la barre metier, aux controles, au reset et au message aucun resultat.
- `.board-container` conserve `overflow-x: auto`, et aucune regle ne masque `.kanban-column` ou ne reaffiche `.activity-card[hidden]`.
- La media query `max-width: 760px` replie la barre sans toucher aux dimensions des colonnes Kanban.
- Les controles ont une hauteur minimale stable, des etats focus visibles, et les libelles longs sont contenus.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
