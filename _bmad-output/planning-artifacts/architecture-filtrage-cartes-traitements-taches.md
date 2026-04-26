---
title: 'Architecture - Filtrage des cartes par traitements et taches'
slug: 'architecture-filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'ready-for-epics'
source_prd: '_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
workflow: 'bmad-create-architecture'
agent: 'architect'
---

# Architecture - Filtrage des cartes par traitements et taches

## 1. Resume

Cette architecture ajoute un filtrage metier cote navigateur au tableau Kanban Django. Elle conserve le rendu serveur existant, le schema SQLite partage et les colonnes virtuelles actuelles. Django continue de produire les colonnes et les cartes ; chaque carte expose seulement des donnees structurees supplementaires permettant au JavaScript de filtrer par libelle exact et par etat `done`.

Le changement est limite a l'application web :

- `web/kanban/views.py` alimente les catalogues de traitements et taches avec tous les libelles distincts non vides.
- `web/kanban/templates/kanban/board.html` ajoute la barre de filtres, le message "Aucune carte ne correspond aux filtres" et la logique JavaScript.
- `web/kanban/templates/kanban/card_snippet.html` expose les traitements et taches d'une carte sous forme JSON echappee.
- `web/kanban/static/kanban/css/style.css` ajoute le style responsive de la barre de filtres et du message vide.

## 2. Contexte existant

L'application est un projet brownfield multi-interface :

- Desktop PySide6/SQLAlchemy et Web Django partagent `organiseur.db`.
- Les modeles Django sont `managed = False`.
- Le tableau web est rendu par `board()` dans `web/kanban/views.py`.
- Les cartes sont rendues par `card_snippet.html`.
- Le JavaScript de tri, glisser-deposer, modal et rafraichissement des colonnes est actuellement inline dans `board.html`.
- Les colonnes "Traitements", "Taches", "CTA", "Reparations", "En attente" et "En cours" utilisent une logique de colonnes virtuelles cote serveur.

Les attributs actuels `data-pending-traitement-names` et `data-pending-tache-names` ne suffisent pas, car ils ne contiennent que les elements restants et utilisent une representation `__SEP__` adaptee a des correspondances simples.

## 3. Decisions architecturales

### AD-01 - Filtrage cote navigateur

Decision : appliquer le nouveau filtre en JavaScript sur les cartes deja rendues.

Raison :

- Le PRD demande une application immediate sans bouton.
- Le tableau charge deja les cartes et manipule le DOM pour tri, drag-and-drop et rafraichissement.
- Le volume courant vise une mise a jour sans latence perceptible.
- Aucun endpoint ni changement de navigation n'est necessaire.

Consequence :

- Le filtre ne reduit pas la charge SQL initiale.
- Les compteurs de colonnes doivent etre recalcules cote navigateur apres chaque filtrage.

### AD-02 - Donnees de carte en JSON structure

Decision : chaque instance `.activity-card` expose :

- `data-traitements='[{"description":"...","done":true}]'`
- `data-taches='[{"description":"...","done":false}]'`

Raison :

- Les exigences demandent des comparaisons exactes, pas des sous-chaines.
- Les etats "fait", "restant a faire" et "presence" doivent etre testables de facon isolee.
- JSON conserve une representation simple et locale au rendu Django.

Consequence :

- Le template doit echapper le JSON avec le filtre Django approprie pour attribut HTML.
- Les cartes rechargees via `refreshActivityColumns()` doivent recevoir les memes attributs, car elles reutilisent `card_snippet.html`.

### AD-03 - Catalogues globaux distincts

Decision : les listes `filter_traitements` et `filter_taches` viennent de toutes les descriptions distinctes non vides, sans filtre `done=False`.

Raison :

- Le filtre doit proposer les elements faits et non faits.
- Le catalogue est global au tableau, pas limite a une colonne.

Consequence :

- Le changement dans `board()` est simple : retirer `done=False`, exclure les libelles vides et ordonner.
- Les doublons exacts sont deduplices par `distinct()`.

### AD-04 - Aucun changement de schema ni d'API

Decision : ne pas modifier la base, les modeles ou les endpoints.

Raison :

- `Traitement.done` et `Tache.done` couvrent le besoin.
- Le PRD exclut les migrations.
- La base SQLite est partagee avec le desktop, donc tout changement de schema aurait un impact multi-interface.

Consequence :

- Toute logique d'affichage reste dans le rendu web.
- Les APIs existantes continuent de retourner des snippets compatibles si `card_snippet.html` est mis a jour.

### AD-05 - Logique de filtre isolee dans des fonctions pures JavaScript

Decision : isoler les regles dans des fonctions nommees :

- `parseCardItems(card, datasetKey)`
- `matchesItemFilter(items, selectedLabel, wantDone, wantPending)`
- `matchesBusinessFilters(card, state)`
- `applyBoardFilters()`
- `updateVisibleCounts()`

Raison :

- Les regles FR-05 a FR-13 sont faciles a casser si elles sont dispersees.
- Les cas "aucun etat", "deux etats" et "presence" doivent etre lisibles.

Consequence :

- Le code reste dans `board.html` pour respecter le style actuel, mais il est structure pour une extraction future vers un fichier JS statique.

## 4. Flux de donnees

```text
SQLite organiseur.db
    |
    v
Django ORM managed=False
    |
    v
board() dans web/kanban/views.py
    |-- columns_data avec activites + prefetch scelles/traitements/taches
    |-- filter_traitements distincts
    |-- filter_taches distinctes
    v
board.html + card_snippet.html
    |-- barre de filtres
    |-- cartes avec data-traitements / data-taches
    v
JavaScript navigateur
    |-- recherche texte existante
    |-- filtre traitement
    |-- filtre tache
    |-- compteurs visibles
    |-- message aucun resultat
```

## 5. Contrat de donnees DOM

Chaque carte doit conserver les attributs existants :

- `data-id`
- `data-name`
- `data-date`
- `data-pending-traitements`
- `data-pending-taches`

Chaque carte doit ajouter :

```html
data-traitements='[{"description":"Controle final","done":true}]'
data-taches='[{"description":"Verification dossier","done":false}]'
```

Regles :

- `description` est le libelle exact stocke en base.
- `done` est un booleen JSON.
- Les descriptions vides ne sont pas utiles pour le filtrage et peuvent etre omises des tableaux JSON.
- Les attributs historiques `data-pending-*-names` peuvent rester temporairement pour compatibilite, mais le nouveau filtre ne doit pas les utiliser.

## 6. Algorithme de filtrage

Etat lu depuis l'interface :

```text
traitementLabel
traitementDoneChecked
traitementPendingChecked
tacheLabel
tacheDoneChecked
tachePendingChecked
searchText existant
```

Regle par axe :

- Aucun libelle selectionne : l'axe ne filtre pas.
- Libelle selectionne, aucun etat coche : presence exacte du libelle, peu importe `done`.
- Libelle selectionne, deux etats coches : presence exacte du libelle, peu importe `done`.
- Libelle selectionne, "Fait" seul : au moins un item avec `description === libelle` et `done === true`.
- Libelle selectionne, "Restant a faire" seul : au moins un item avec `description === libelle` et `done === false`.

Regle globale :

```text
visible = matchesSearchText(card)
       && matchesTraitementAxis(card)
       && matchesTacheAxis(card)
```

Les instances virtuelles d'une meme activite partagent les memes donnees de carte, donc elles doivent aboutir au meme resultat de visibilite.

## 7. Interface utilisateur

Ajouter une barre sous l'en-tete et avant `.board-container` :

- champ `input list` ou `select` pour Traitement ;
- cases "Fait" et "Restant a faire" pour l'axe Traitement ;
- champ `input list` ou `select` pour Tache ;
- cases "Fait" et "Restant a faire" pour l'axe Tache ;
- bouton `Reinitialiser les filtres`.

Les cases d'etat sont desactivees quand le champ correspondant est vide. Le bouton de reinitialisation efface uniquement les filtres metier ; il ne modifie pas la recherche texte existante.

Le message global :

```html
<div id="noFilterResults" aria-live="polite" hidden>
  Aucune carte ne correspond aux filtres
</div>
```

## 8. Integration avec les comportements existants

### Recherche texte

Si une recherche texte existe deja dans `base.html` ou `board.html`, `applyBoardFilters()` doit l'integrer au lieu de creer une logique concurrente. Si la recherche actuelle masque deja les cartes, elle doit etre refactorisee pour appeler le meme moteur de filtrage.

### Tri

Le tri continue d'ordonner toutes les cartes presentes dans une colonne. Les cartes masquees restent dans le DOM, donc un changement de tri ne doit pas reafficher les cartes masquees. Apres tri, `applyBoardFilters()` peut etre rappele si necessaire.

### Drag-and-drop et changement de colonne

Apres un deplacement ou un `refreshActivityColumns(activityId)`, les nouvelles instances de carte doivent etre soumises au filtre courant. Le point d'integration recommande est d'appeler `applyBoardFilters()` a la fin du traitement `refreshActivityColumns()`.

### Creation/suppression

- Apres creation d'une carte, appeler `applyBoardFilters()` pour respecter l'etat courant.
- Apres suppression, appeler `updateVisibleCounts()` et mettre a jour le message aucun resultat.

## 9. Accessibilite et responsive

- Les champs ont des labels visibles ou `aria-label`.
- Les cases sont des inputs natifs atteignables au clavier.
- L'ordre de tabulation suit : traitement, etats traitement, tache, etats tache, reinitialiser, tableau.
- Le message aucun resultat utilise `aria-live="polite"`.
- La barre est horizontale sur desktop et passe en pile sur mobile.
- Les controles gardent des tailles stables pour eviter les sauts de layout.

## 10. Performance

Le filtrage parcourt les cartes rendues et parse les donnees JSON. Pour eviter de reparses a chaque changement :

- parser une fois par carte et stocker le resultat sur une propriete JS non persistante, par exemple `card._filterData`;
- invalider naturellement cette cache quand une carte est remplacee par `refreshActivityColumns()`.

Sur le volume courant, un parcours DOM complet a chaque changement est acceptable. Si le volume augmente fortement, l'etape suivante serait un index JS par `activityId`, pas un filtrage serveur premature.

## 11. Strategie de test

### Tests manuels obligatoires

- Aucun filtre : les cartes visibles correspondent au comportement actuel.
- Traitement + "Restant a faire" : seules les cartes contenant ce traitement non fait restent visibles.
- Traitement + "Fait" : seules les cartes contenant ce traitement fait restent visibles.
- Tache + "Restant a faire" : seules les cartes contenant cette tache non faite restent visibles.
- Tache + "Fait" : seules les cartes contenant cette tache faite restent visibles.
- Libelle selectionne sans etat : presence exacte, peu importe `done`.
- Deux etats coches : meme resultat que presence.
- Traitement + tache : logique ET.
- Libelles proches : `Controle` ne matche pas `Controle final`.
- Aucun resultat : message visible et compteurs a zero.
- Reinitialiser : filtres metier effaces, recherche texte conservee.
- Drag-and-drop ou edition de carte : filtre courant toujours applique apres refresh.

### Tests automatises recommandes

- Test Django de contexte `board()` : catalogues contiennent descriptions faites et non faites.
- Test de rendu `card_snippet.html` : les attributs JSON contiennent les libelles exacts et les booleens.
- Test JavaScript unitaire ou Playwright pour `matchesItemFilter()` sur les combinaisons d'etat.

## 12. Risques et mitigations

| Risque | Impact | Mitigation |
| --- | --- | --- |
| JSON mal echappe dans un attribut HTML | Filtre casse ou HTML invalide | Utiliser `json_script` ou `escapejs`/echappement adapte, verifier avec libelles contenant apostrophes et guillemets |
| Recherche texte et filtre metier se contredisent | Cartes reaffichees a tort | Centraliser la decision de visibilite dans `applyBoardFilters()` |
| Compteurs restent sur le total initial | Confusion utilisateur | Recalculer les `.count` depuis `.activity-card:not([hidden])` |
| Cartes remplacees par AJAX sans filtre | Etat courant perdu visuellement | Appeler `applyBoardFilters()` apres ajout/remplacement de carte |
| Matching par sous-chaine conserve par erreur | Faux positifs | Ne comparer que `item.description === selectedLabel` |

## 13. Ordre d'implementation recommande

1. Modifier `board()` pour alimenter les catalogues globaux faits/restants.
2. Ajouter une petite aide de serialisation cote Python ou template pour produire les tableaux JSON par carte.
3. Ajouter les attributs `data-traitements` et `data-taches` dans `card_snippet.html`.
4. Ajouter la barre de filtres et le message aucun resultat dans `board.html`.
5. Ajouter les fonctions JavaScript de filtrage et les brancher sur `input/change/reset`.
6. Appeler le filtrage apres tri, creation, suppression et `refreshActivityColumns()`.
7. Ajouter le CSS responsive.
8. Verifier les criteres d'acceptation du PRD.

## 14. Definition of done architecture

- Le schema de donnees reste inchange.
- Les endpoints restent inchanges.
- Le filtre utilise des donnees structurees, pas du texte visible.
- Les criteres traitement et tache sont combines en ET.
- Les compteurs et le message aucun resultat refletent l'etat filtre.
- Les prochaines stories peuvent etre derivees sans decisions techniques ouvertes majeures.
