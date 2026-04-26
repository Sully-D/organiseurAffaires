---
title: 'Story 5.1 - Ajouter une verification automatisee minimale'
story_id: '5.1'
epic: 'Epic 5 - Verification et documentation d''implementation'
feature: 'filtrage-cartes-traitements-taches'
created: '2026-04-26'
status: 'done'
workflow: 'bmad-create-story'
agent: 'sm'
source_sprint: '_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml'
source_epics: '_bmad-output/planning-artifacts/epics-and-stories-filtrage-cartes-traitements-taches.md'
source_prd: '_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
source_story_1_2: '_bmad-output/implementation-artifacts/story-1.2-donnees-json-par-carte.md'
source_story_2_1: '_bmad-output/implementation-artifacts/story-2.1-fonctions-correspondance-exactes.md'
source_story_4_2: '_bmad-output/implementation-artifacts/story-4.2-preserver-comportements-existants-non-lies-filtre.md'
---

# Story 5.1 - Ajouter une verification automatisee minimale

## Status

Done.

## Story

**En tant que** mainteneur,  
**je veux** des tests ciblant les donnees et les cas de filtrage critiques,  
**afin de** detecter les regressions les plus probables.

## Scope

Cette story consolide la verification automatisee minimale du filtrage traitements/taches. Une partie importante de la couverture existe deja dans `web/kanban/tests.py` depuis les stories 1.1, 1.2, 2.1, 2.2, 3.x et 4.2; le travail attendu est donc d'auditer cette couverture, de combler les manques strictement utiles, puis de documenter clairement les limites restantes, notamment l'absence de vrai runner JavaScript et les modeles Django `managed = False`.

### Included

- Auditer `web/kanban/tests.py` contre les exigences minimales de Story 5.1.
- Confirmer ou ajouter une couverture automatisee pour:
  - catalogues incluant descriptions faites et restantes;
  - rendu JSON par carte avec un traitement fait, un traitement restant, une tache faite et une tache restante;
  - exclusion des descriptions vides;
  - booleens JSON reels;
  - libelles avec caracteres speciaux;
  - matching exact structurel dans `matchesItemFilter`;
  - absence de dependance a `organiseur.db` de production.
- Garder les tests executables avec `SimpleTestCase` / mocks si possible, sans creation de tables legacy.
- Executer `venv/bin/python web/manage.py test kanban`.
- Executer `venv/bin/python web/manage.py check`.
- Documenter dans le Dev Agent Record ce qui est automatise et ce qui reste manuel pour Story 5.2.

### Excluded

- Ajouter Playwright, Cypress, npm, un bundler ou un runner JavaScript.
- Convertir les tests structurels JS en tests navigateur complets.
- Modifier le comportement de filtrage, le style, les templates, les endpoints ou le schema.
- Creer des migrations ou rendre les modeles unmanaged `managed=True`.
- Executer la matrice fonctionnelle complete AC-01 a AC-12; Story 5.2 la couvre.

## Acceptance Criteria

1. `web/kanban/tests.py` contient des tests executables qui couvrent les catalogues `filter_traitements` et `filter_taches` sans filtrer sur `done=False`.
2. Les tests verifient au moins un traitement fait et un traitement restant dans les donnees JSON de carte.
3. Les tests verifient au moins une tache faite et une tache restante dans les donnees JSON de carte.
4. Les tests verifient que les descriptions vides sont omises.
5. Les tests verifient que les valeurs `done` restent de vrais booleens JSON apres `json.loads`.
6. Les tests verifient que les attributs `data-traitements` et `data-taches` coexistent avec les attributs legacy `data-pending-*`.
7. Les tests verifient que le matching metier utilise des comparaisons exactes et n'utilise pas `.includes`, `innerText` ou une comparaison texte libre pour les libelles metier.
8. Les tests ne dependent pas de `organiseur.db` de production ni de tables legacy creees dans la base de test.
9. Si des limites restent dues a l'absence de runner JS/navigateur, elles sont documentees explicitement dans le Dev Agent Record.
10. `venv/bin/python web/manage.py test kanban` passe localement.
11. `venv/bin/python web/manage.py check` passe localement.
12. Aucun changement de schema, endpoint, modele ou comportement utilisateur n'est introduit.

## Tasks / Subtasks

- [x] Task 1 - Auditer la couverture existante (AC: 1-8)
  - [x] Lire `web/kanban/tests.py` et mapper les tests existants aux AC de cette story.
  - [x] Identifier les tests deja satisfaits par `BoardFilterCatalogQueryTests`, `CardFilterJsonTests` et `BoardBusinessFilterScriptTests`.
  - [x] Ne pas dupliquer un test existant qui couvre deja clairement un AC.
  - [x] Noter les manques reels avant toute modification.

- [x] Task 2 - Completer la couverture des donnees de carte si necessaire (AC: 2, 3, 4, 5, 6, 8)
  - [x] Verifier que `CardFilterJsonTests.build_activity()` contient au moins un traitement fait, un traitement restant, une tache faite et une tache restante.
  - [x] Si absent, ajouter ces cas dans les fixtures de test existantes.
  - [x] Verifier que les descriptions vides sont presentes dans la fixture puis omises du JSON attendu.
  - [x] Verifier que le rendu `card_snippet.html` reste decodable apres `html.unescape` + `json.loads`.
  - [x] Eviter tout acces aux tables legacy; utiliser `SimpleNamespace`, `RelatedList`, `SimpleTestCase` et mocks existants.

- [x] Task 3 - Completer la couverture du matching exact si necessaire (AC: 7)
  - [x] Verifier que le test structurel de `matchesItemFilter` exige `item.description !== selectedLabel`.
  - [x] Verifier que le test interdit `.includes(`, `innerText` et `toLowerCase` dans le corps de `matchesItemFilter`.
  - [x] Verifier que les booleens stricts `item.done === true` et `item.done === false` sont proteges.
  - [x] Si un manque existe, ajouter une assertion structurelle ciblee plutot qu'un parseur JS fragile.

- [x] Task 4 - Verifier l'independance vis-a-vis de la base production (AC: 1, 8)
  - [x] Confirmer que les tests de catalogue inspectent les `QuerySet` et SQL genere sans evaluer les requetes.
  - [x] Confirmer que les tests de rendu utilisent des objets simples et ne creent pas de donnees en base.
  - [x] Ajouter un commentaire court uniquement si une intention de test non evidente doit etre expliquee.
  - [x] Ne pas introduire `TestCase` avec acces DB pour cette story.

- [x] Task 5 - Executer et documenter la verification (AC: 9, 10, 11, 12)
  - [x] Executer `venv/bin/python web/manage.py test kanban`.
  - [x] Executer `venv/bin/python web/manage.py check`.
  - [x] Documenter dans le Dev Agent Record les commandes et resultats.
  - [x] Documenter les limites restantes: pas de runner JS/navigateur dans cette story, matrice fonctionnelle complete reservee a Story 5.2.
  - [x] Mettre a jour la File List et le Change Log de cette story.

## Dev Notes

### Current Implementation Context

- `web/kanban/tests.py` est deja executable sans tables legacy et contient actuellement des tests structurels et de rendu.
- Les modeles Django du domaine sont `managed = False`; eviter les tests qui creent directement `Activity`, `Traitement`, `Tache`, `Scelle` en base de test.
- `BoardFilterCatalogQueryTests` mocke `KanbanColumn.objects.exclude` et inspecte les `QuerySet` des catalogues sans les evaluer.
- `CardFilterJsonTests` utilise `SimpleNamespace` et `RelatedList` pour verifier `_attach_card_filter_json()` et `card_snippet.html`.
- `BoardBusinessFilterScriptTests` lit `board.html`, `base.html`, `card_snippet.html`, `style.css` et `views.py` comme sources de contrats structurels.
- La story 4.2 a ajoute des tests de non-regression pour tri, modal, drag-and-drop, permissions, etat neutre et endpoints.

### Existing Coverage To Preserve

Les tests suivants sont directement pertinents pour Story 5.1 et doivent etre preserves ou renforces:

- `test_traitement_filter_catalog_includes_done_and_pending_non_empty_descriptions`
- `test_tache_filter_catalog_includes_done_and_pending_non_empty_descriptions`
- `test_card_filter_json_includes_done_pending_special_chars_and_omits_empty_descriptions`
- `test_card_snippet_renders_json_attributes_with_legacy_attributes`
- `test_matches_item_filter_uses_exact_labels_and_boolean_done_states`
- `test_legacy_global_specific_filters_use_structured_exact_matching`
- `test_apply_board_filters_centralizes_search_global_filter_and_business_filters`

### Non-Regression Guardrails

- Ne pas remplacer les tests structurels par des tests qui dependent d'un navigateur non configure.
- Ne pas ajouter une dependance de test lourde pour cette story.
- Ne pas faire de tests contre `organiseur.db`; les tests doivent etre reproductibles sans donnees locales utilisateur.
- Ne pas modifier `board.html`, `base.html`, `card_snippet.html` ou `views.py` sauf si l'audit revele une regression reelle.
- Ne pas supprimer les attributs legacy `data-pending-*`; ils restent necessaires pour les tris et compatibilites.
- Ne pas pretendre qu'une passe manuelle navigateur a ete executee si elle ne l'a pas ete.

### Recommended Implementation Strategy

1. Executer d'abord `venv/bin/python web/manage.py test kanban` pour etablir l'etat actuel.
2. Lire les tests existants et mapper chaque AC.
3. Si tous les AC sont deja couverts, limiter le changement a la documentation de story et a une note claire dans le Dev Agent Record.
4. Si un AC n'est pas couvert, ajouter l'assertion la plus petite possible dans la classe de test existante appropriee.
5. Reexecuter `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check`.

### Testing Guidance

Les tests attendus doivent rester dans `web/kanban/tests.py`.

Patterns preferes:

- `SimpleTestCase` pour eviter la base de test.
- `SimpleNamespace` + `RelatedList` pour construire des activites/scelles/traitements/taches en memoire.
- `render_to_string("kanban/card_snippet.html", {"activity": activity})` pour verifier les attributs de carte.
- `html.unescape` + `json.loads` pour verifier que les attributs JSON rendus restent parsables.
- Lecture de `board.html` avec `Path.read_text` pour tester les fonctions JS inline tant qu'aucun runner JS n'est configure.

Patterns a eviter:

- `TestCase` avec creation de modeles unmanaged.
- Acces direct ou indirect a `organiseur.db`.
- Tests fondes sur l'ordre exact complet du template si une assertion de contrat suffit.
- Duplication de la logique JS en Python.

## Verification Plan

### Automated

- `venv/bin/python web/manage.py test kanban`
- `venv/bin/python web/manage.py check`

### Manual Fallback

Si un test automatise demande par cette story est bloque par l'environnement:

1. Documenter le blocage exact dans le Dev Agent Record.
2. Garder les tests automatises qui passent.
3. Ajouter une checklist manuelle courte pour Story 5.2 au lieu de gonfler cette story.

## Done Checklist

- [x] Couverture catalogue faits/restants auditee ou completee.
- [x] Couverture JSON carte faite/restante pour traitements et taches auditee ou completee.
- [x] Couverture descriptions vides et booleens JSON auditee ou completee.
- [x] Couverture matching exact auditee ou completee.
- [x] Tests independants de `organiseur.db` confirmes.
- [x] Limites JS/navigateur documentees.
- [x] `venv/bin/python web/manage.py test kanban` execute.
- [x] `venv/bin/python web/manage.py check` execute.
- [x] Aucun schema, endpoint, modele ou comportement utilisateur modifie.
- [x] Sprint status mis a jour apres implementation de story.

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- 2026-04-26: `venv/bin/python web/manage.py test kanban` avant modification -> OK, 24 tests.
- 2026-04-26: `venv/bin/python web/manage.py test kanban` apres ajout du garde-fou -> OK, 25 tests.
- 2026-04-26: `venv/bin/python web/manage.py check` -> OK, aucun probleme signale.

### Completion Notes List

- Audit effectue: les tests existants couvraient deja les catalogues faits/restants, JSON par carte, descriptions vides, booleens JSON, attributs legacy et matching exact structurel.
- Ajout du garde-fou `test_minimal_filter_tests_do_not_depend_on_production_database` pour proteger l'absence de `TestCase`, de creation ORM et de reference a `organiseur.db` dans la suite minimale.
- Correction pendant review: le garde-fou utilise maintenant `ast` pour detecter les imports/classes `TestCase` et une regex pour detecter les creations ORM meme avec espaces.
- Aucune modification fonctionnelle de template, vue, endpoint, modele ou schema.
- Limite documentee: pas de runner JS/navigateur ajoute; la matrice fonctionnelle complete reste reservee a Story 5.2.

### File List

- `web/kanban/tests.py`
- `_bmad-output/implementation-artifacts/story-5.1-ajouter-verification-automatisee-minimale.md`
- `_bmad-output/implementation-artifacts/sprint-status-filtrage-cartes-traitements-taches.yaml`
- `_bmad-output/bmm-workflow-status.yaml`

### Change Log

- 2026-04-26: Story 5.1 creee avec contexte d'audit et consolidation de la verification automatisee minimale.
- 2026-04-26: Story 5.1 implementee; audit de couverture effectue, garde-fou d'independance DB ajoute, validations Django executees.
- 2026-04-26: Code review approuvee; robustesse du garde-fou d'independance DB amelioree.

## Senior Developer Review (AI)

### Outcome

Approve.

### Review Notes

- 2026-04-26: Finding corrige pendant review: le test d'independance DB cherchait des chaines exactes et pouvait manquer `TestCase` importe dans une liste; il inspecte maintenant l'AST des imports et bases de classes.
- 2026-04-26: Finding corrige pendant review: la detection de creation ORM accepte maintenant les espaces via regex `\.objects\.create\s*\(`.
- La story consolide bien la verification minimale sans ajouter de dependance navigateur/JS et sans toucher au comportement applicatif.
- Les validations `venv/bin/python web/manage.py test kanban` et `venv/bin/python web/manage.py check` passent.
