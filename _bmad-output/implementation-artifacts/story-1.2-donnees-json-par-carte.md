---
title: 'Story 1.2 - Exposer les traitements et taches de chaque carte en JSON echappe'
story_id: '1.2'
epic: 'Epic 1 - Donnees de filtrage exactes dans le rendu Kanban'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'done'
workflow: 'bmad-create-story'
agent: 'sm'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
source_prd: '_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
---

# Story 1.2 - Exposer les traitements et taches de chaque carte en JSON echappe

## Status

Done.

## Story

**En tant que** navigateur executant le filtre,  
**je veux** recevoir des donnees structurees par carte,  
**afin de** matcher les libelles exacts et les etats sans analyser le texte visible.

## Scope

Cette story ajoute les donnees structurees par carte necessaires aux stories suivantes. Elle ne modifie pas encore la logique JavaScript de filtrage, la recherche globale, les controles UX, le schema SQLite ni les endpoints.

### Included

- Ajouter `data-traitements` sur chaque `.activity-card`.
- Ajouter `data-taches` sur chaque `.activity-card`.
- Utiliser un tableau JSON d'objets `{ "description": "...", "done": true|false }`.
- Inclure les elements faits et restants.
- Omettre les descriptions vides.
- Echaper correctement le JSON pour un attribut HTML.
- Conserver les attributs existants `data-pending-*` et `data-pending-*-names`.
- S'assurer que les snippets retournes par AJAX reutilisent les memes attributs.

### Excluded

- Modifier le filtre global JavaScript dans `base.html`.
- Ajouter la barre de filtres metier.
- Parser ou exploiter `data-traitements` / `data-taches` cote navigateur.
- Modifier les regles des colonnes virtuelles.
- Modifier le schema SQLite.
- Ajouter un endpoint.

## Acceptance Criteria

1. Chaque carte rendue contient un attribut `data-traitements`.
2. Chaque carte rendue contient un attribut `data-taches`.
3. `data-traitements` inclut les traitements faits et restants de tous les scelles de l'activite.
4. `data-taches` inclut les taches faites et restantes de tous les scelles de l'activite.
5. Chaque item JSON contient `description` avec le libelle exact stocke en base.
6. Chaque item JSON contient `done` comme booleen JSON reel (`true` / `false`), pas comme chaine.
7. Les descriptions vides sont omises des tableaux JSON.
8. Les libelles contenant apostrophes, guillemets, accents, chevrons ou esperluettes ne cassent pas l'attribut HTML et restent parsables par `JSON.parse`.
9. Les attributs existants `data-id`, `data-name`, `data-date`, `data-pending-traitements`, `data-pending-taches`, `data-pending-traitement-names` et `data-pending-tache-names` restent presents.
10. Les snippets produits par `create_activity()` et `get_activity_columns()` contiennent aussi `data-traitements` et `data-taches`.
11. Aucun changement de schema, endpoint ou logique de visibilite des colonnes n'est introduit.

## Tasks / Subtasks

- [x] Task 1 - Ajouter une serialisation controlee des donnees de filtrage par carte (AC: 3, 4, 5, 6, 7, 8)
  - [x] Creer dans `web/kanban/views.py` une aide privee qui construit deux listes Python depuis `activity.scelles.all()`, `scelle.traitements.all()` et `scelle.taches.all()`.
  - [x] Pour chaque traitement/tache, ajouter `{ "description": description, "done": bool(done) }` uniquement si `description` n'est pas vide.
  - [x] Serialiser avec `json.dumps(..., ensure_ascii=False)` cote Python; ne pas construire du JSON par concatenation dans le template.
  - [x] Attacher les chaines JSON produites a chaque activite rendue, par exemple `activity.traitements_filter_json` et `activity.taches_filter_json`.

- [x] Task 2 - Alimenter tous les chemins de rendu de `card_snippet.html` (AC: 1, 2, 10, 11)
  - [x] Dans `board()`, appliquer l'aide de serialisation aux activites de chaque colonne avant rendu.
  - [x] Dans `create_activity()`, fournir des tableaux JSON vides pour la nouvelle activite.
  - [x] Dans `get_activity_columns()`, prefetcher aussi `scelles__traitements` et `scelles__taches`, puis appliquer l'aide de serialisation avant `render_to_string`.
  - [x] Ne pas changer les requetes de selection des colonnes virtuelles hors prefetch necessaire.

- [x] Task 3 - Ajouter les attributs au template de carte (AC: 1, 2, 8, 9)
  - [x] Modifier uniquement l'ouverture de `.activity-card` dans `web/kanban/templates/kanban/card_snippet.html`.
  - [x] Ajouter `data-traitements="{{ activity.traitements_filter_json|escape }}"`.
  - [x] Ajouter `data-taches="{{ activity.taches_filter_json|escape }}"`.
  - [x] Conserver tous les attributs existants, y compris `data-pending-traitement-names` et `data-pending-tache-names`.

- [x] Task 4 - Verifier l'echappement et la compatibilite legacy (AC: 6, 7, 8, 9, 10, 11)
  - [x] Ajouter un test automatise ciblant la serialisation avec au moins un libelle contenant apostrophe, guillemets, accent, `<`, `>` et `&`.
  - [x] Verifier que `json.loads` recupere des booleens Python, pas des chaines.
  - [x] Verifier qu'une description vide est omise.
  - [x] Si un test de rendu template est faisable sans tables legacy, verifier que les attributs `data-traitements`, `data-taches` et `data-pending-*` coexistent dans le HTML.
  - [x] Executer `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check`.

## Dev Notes

### Current Implementation Context

- `web/kanban/templates/kanban/card_snippet.html` rend l'element `.activity-card`.
- Le template contient deja `data-pending-traitements`, `data-pending-taches`, `data-pending-traitement-names` et `data-pending-tache-names`.
- Les attributs `data-pending-*-names` ne couvrent actuellement que les elements `done=False` et utilisent un separateur texte `__SEP__`; ils doivent rester pour compatibilite mais ne sont pas le format cible.
- `board()` prefetch deja `tags`, `scelles__traitements` et `scelles__taches` pour les activites principales.
- `create_activity()` rend une carte via `render_to_string('kanban/card_snippet.html', {'activity': activity})`; cette carte n'a normalement aucun traitement ni tache.
- `get_activity_columns()` rend aussi `card_snippet.html`; il annote les compteurs et calcule les colonnes virtuelles. Ce chemin doit recevoir les nouveaux attributs sans changer la logique de colonnes.

### Required Data Contract

Chaque carte doit exposer :

```html
data-traitements='[{"description":"Controle final","done":true}]'
data-taches='[{"description":"Verification dossier","done":false}]'
```

Regles contractuelles :

- `description` est le libelle exact stocke en base.
- `done` est un booleen JSON.
- Les tableaux peuvent etre vides (`[]`).
- Les descriptions vides sont omises.
- Le filtre futur ne devra pas parser le texte visible ni les anciens attributs `data-pending-*-names`.

### Serialization Guardrails

- Ne pas assembler le JSON dans le template avec des boucles et des virgules manuelles.
- Ne pas utiliser `str(list)` ou des booleens Python `True` / `False` dans l'attribut.
- Utiliser `json.dumps` cote Python puis le filtre Django `escape` dans l'attribut HTML.
- Django 6.0.1 est installe localement. La documentation Django recommande `json_script` pour transmettre des objets JSON dans du HTML et indique que `escapejs` est limite aux chaines JavaScript; ici le contrat impose un attribut `data-*`, donc une serialisation Python + echappement HTML de l'attribut est le choix le plus direct.
- Source officielle Django consultee: https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#json-script et https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#escapejs.

### Project Structure Notes

- Fichiers attendus:
  - `web/kanban/views.py`
  - `web/kanban/templates/kanban/card_snippet.html`
  - `web/kanban/tests.py`
- Eviter de creer une nouvelle app, un endpoint, un fichier JS ou une migration pour cette story.
- Les modeles `Traitement` et `Tache` sont `managed=False`; privilegier des tests de helper/serialization et de rendu sans dependance aux tables de test.

### Previous Story Intelligence

- Story 1.1 a retire `done=False` des catalogues globaux et a ajoute des tests executables avec `SimpleTestCase`.
- Les tests existants evitent la creation de tables legacy en inspectant le contexte et les `QuerySet`.
- La review de Story 1.1 est approuvee; la story est `done`.
- Ne pas revenir sur les requetes `filter_traitements` / `filter_taches` sauf necessite directe.

### Source References

- Story 1.2 source: `_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md`, section "Story 1.2 - Exposer les traitements et taches de chaque carte en JSON echappe".
- PRD: `_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md`, sections "Risques", "Mesures de succes" et "Notes d'implementation pour la suite".
- Architecture: `_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md`, sections "AD-02 - Donnees de carte en JSON structure", "Format de carte", "Strategie de test" et "Risques et mitigations".
- UX: `_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md`, section "Donnees necessaires a l'interface".
- Readiness: `_bmad-output/planning-artifacts/readiness-report-filtrage-cartes-traitements-taches.md`, section "Concern 2 - Echappement JSON dans les attributs HTML".

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

Tests attendus :

- Helper de serialisation:
  - inclut un traitement fait et un traitement restant;
  - inclut une tache faite et une tache restante;
  - conserve les caracteres speciaux apres `json.loads`;
  - produit des booleens JSON;
  - omet les descriptions vides.
- Rendu template si faisable:
  - `data-traitements` et `data-taches` existent;
  - `data-pending-*` existent encore;
  - le HTML rendu contient un attribut echappe et parsable apres lecture DOM ou decodage HTML.

### Manual Fallback

Si le test de rendu template est bloque par les modeles legacy :

1. Lancer le serveur Django.
2. Ouvrir le tableau Kanban.
3. Inspecter une carte avec au moins un traitement fait, un traitement restant, une tache faite et une tache restante.
4. Verifier dans le DOM `data-traitements` et `data-taches`.
5. Copier la valeur des attributs et verifier que `JSON.parse(...)` fonctionne dans la console.
6. Verifier avec des libelles contenant apostrophes, guillemets et accents.

## Done Checklist

- [x] `web/kanban/views.py` prepare les donnees JSON par activite.
- [x] `card_snippet.html` expose `data-traitements` et `data-taches`.
- [x] Les booleens JSON sont de vrais booleens.
- [x] Les descriptions vides sont exclues.
- [x] Les attributs legacy `data-pending-*` sont conserves.
- [x] Les chemins AJAX retournent les nouveaux attributs.
- [x] Aucun schema, endpoint ou moteur JS de filtrage n'est modifie.
- [x] Verification automatisee executee ou fallback manuel documente.
- [x] Sprint status mis a jour apres creation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-25: `venv/bin/python web/manage.py test kanban` -> OK, 4 tests.
- 2026-04-25: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- Ajout de helpers prives dans `web/kanban/views.py` pour serialiser les traitements et taches de chaque activite en JSON structure.
- Ajout des attributs `data-traitements` et `data-taches` dans `card_snippet.html` avec echappement HTML.
- Couverture des chemins `board()`, `create_activity()` et `get_activity_columns()`; les attributs legacy `data-pending-*` restent inchanges.
- Ajout de tests executables sans tables legacy pour la serialisation, les caracteres speciaux, les booleens JSON et le rendu template.

### File List

- `web/kanban/views.py`
- `web/kanban/templates/kanban/card_snippet.html`
- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-1.2-donnees-json-par-carte.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-25: Story 1.2 creee avec contexte d'implementation et guardrails JSON.
- 2026-04-25: Implementation de la story 1.2 et ajout des tests de serialisation/rendu.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-25: Clean review. Aucun finding decision-needed, patch ou defer.
- Les attributs `data-traitements` et `data-taches` respectent le contrat JSON attendu et conservent les attributs legacy.
- Les chemins `board()`, `create_activity()` et `get_activity_columns()` sont couverts sans modification de schema, endpoint ou logique JavaScript.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
