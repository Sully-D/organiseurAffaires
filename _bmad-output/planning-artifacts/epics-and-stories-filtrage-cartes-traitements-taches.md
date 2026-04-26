---
title: 'Epics and Stories - Filtrage des cartes par traitements et taches'
slug: 'epics-and-stories-filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'ready-for-implementation-readiness'
source_prd: '_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md'
source_ux: '_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md'
source_architecture: '_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md'
workflow: 'bmad-create-epics-and-stories'
agent: 'pm'
---

# Epics and Stories - Filtrage des cartes par traitements et taches

## 1. Objectif

Livrer le filtrage web Kanban par traitement et tache, avec distinction "Fait", "Restant a faire" et presence exacte, sans modifier le schema SQLite ni les endpoints existants.

La fonctionnalite doit respecter les documents sources :

- PRD : `_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md`
- UX : `_bmad-output/planning-artifacts/ux-design-filtrage-cartes-traitements-taches.md`
- Architecture : `_bmad-output/planning-artifacts/architecture-filtrage-cartes-traitements-taches.md`

## 2. Strategie de decoupage

Le decoupage separe les risques principaux :

1. donnees exactes disponibles dans le DOM ;
2. moteur de filtrage correct ;
3. controles UX et feedback utilisateur ;
4. integration avec les interactions existantes ;
5. verification fonctionnelle.

Chaque story doit pouvoir etre validee localement sur le tableau Django.

## Epic 1 - Donnees de filtrage exactes dans le rendu Kanban

### But

Permettre au navigateur de connaitre, pour chaque carte rendue, tous les traitements et toutes les taches associes a l'activite, faits et restants, avec leur libelle exact et leur etat `done`.

### Valeur utilisateur

L'utilisateur peut filtrer sur des elements faits ou restants sans faux positifs de texte.

### Stories

#### Story 1.1 - Alimenter les catalogues globaux faits et restants

**En tant que** utilisateur du tableau Kanban web,  
**je veux** voir les traitements et taches connus dans les champs de filtre, qu'ils soient faits ou restants,  
**afin de** pouvoir filtrer tous les cas demandes par le PRD.

**Portee technique**

- Modifier `web/kanban/views.py`, fonction `board()`.
- Remplacer les catalogues actuels limites a `done=False` par des listes distinctes de descriptions non vides.
- Conserver le tri alphabetique par `description`.
- Ne pas ajouter d'endpoint.

**Criteres d'acceptation**

- Les descriptions de traitements faits apparaissent dans `filter_traitements`.
- Les descriptions de traitements restants apparaissent dans `filter_traitements`.
- Les descriptions de taches faites apparaissent dans `filter_taches`.
- Les descriptions de taches restantes apparaissent dans `filter_taches`.
- Les descriptions vides sont exclues.
- Le comportement d'affichage des colonnes n'est pas modifie.

**Tests recommandes**

- Test Django de contexte `board()` avec un traitement fait, un traitement restant, une tache faite et une tache restante.
- Verification manuelle des options visibles dans le navigateur.

#### Story 1.2 - Exposer les traitements et taches de chaque carte en JSON echappe

**En tant que** navigateur executant le filtre,  
**je veux** recevoir des donnees structurees par carte,  
**afin de** matcher les libelles exacts et les etats sans analyser le texte visible.

**Portee technique**

- Modifier `web/kanban/templates/kanban/card_snippet.html`.
- Ajouter `data-traitements` et `data-taches` sur `.activity-card`.
- Le format cible est un tableau JSON d'objets `{ "description": "...", "done": true|false }`.
- Omettre les descriptions vides si possible.
- Conserver les attributs existants `data-pending-*` pour les tris et compatibilites actuelles.
- S'assurer que les snippets retournes par les appels AJAX reutilisent automatiquement ces attributs.

**Criteres d'acceptation**

- Chaque carte rendue contient `data-traitements`.
- Chaque carte rendue contient `data-taches`.
- Les donnees incluent les elements faits et restants.
- Les booleens JSON sont de vrais booleens, pas des chaines `"True"` ou `"False"`.
- Les libelles avec apostrophes, guillemets ou accents ne cassent pas le HTML.
- Les attributs existants de tri et compteurs restent presents.

**Tests recommandes**

- Test de rendu de template sur une activite avec plusieurs scelles, traitements et taches.
- Verification manuelle dans l'inspecteur DOM avec des libelles contenant caracteres speciaux.

## Epic 2 - Moteur de filtrage cote navigateur

### But

Creer une logique de filtrage centralisee, lisible et reutilisable par la recherche texte, les filtres metier et les interactions dynamiques du tableau.

### Valeur utilisateur

Chaque changement de filtre s'applique immediatement et les resultats correspondent strictement aux criteres selectionnes.

### Stories

#### Story 2.1 - Implementer les fonctions de correspondance exactes

**En tant que** utilisateur,  
**je veux** que les filtres utilisent la presence exacte et l'etat des traitements/taches,  
**afin de** ne pas voir de cartes erronees quand des libelles se ressemblent.

**Portee technique**

- Modifier le script inline de `web/kanban/templates/kanban/board.html`.
- Ajouter des fonctions nommees pour :
  - parser les attributs JSON d'une carte ;
  - evaluer un axe de filtre ;
  - evaluer la combinaison traitement + tache ;
  - appliquer l'etat visible/masque a toutes les cartes.
- Utiliser `description === selectedLabel`.
- Implementer la regle de presence quand aucun etat ou deux etats sont coches.

**Criteres d'acceptation**

- Traitement "Fait" seul matche seulement `done === true`.
- Traitement "Restant a faire" seul matche seulement `done === false`.
- Tache "Fait" seul matche seulement `done === true`.
- Tache "Restant a faire" seul matche seulement `done === false`.
- Aucun etat coche matche la presence du libelle, quel que soit `done`.
- Deux etats coches matche la presence du libelle, quel que soit `done`.
- Un libelle `Controle` ne matche pas `Controle final`.
- Si traitement et tache sont selectionnes, la carte doit satisfaire les deux axes.

**Tests recommandes**

- Tests unitaires JavaScript si l'environnement le permet.
- A defaut, checklist manuelle avec libelles proches et combinaisons d'etats.

#### Story 2.2 - Combiner le filtre metier avec la recherche texte existante

**En tant que** utilisateur,  
**je veux** que la recherche texte et les filtres metier agissent ensemble,  
**afin de** reduire les cartes visibles selon toutes mes intentions.

**Portee technique**

- Identifier la recherche texte existante dans `base.html` ou `board.html`.
- Centraliser la decision finale dans `applyBoardFilters()`.
- Eviter deux mecanismes concurrents qui masqueraient/reafficheraient les cartes separement.
- Conserver le comportement de recherche existant quand aucun filtre metier n'est actif.

**Criteres d'acceptation**

- Sans filtre metier, la recherche texte conserve le comportement actuel.
- Avec un filtre metier actif, une carte est visible uniquement si elle respecte la recherche texte et le filtre metier.
- Reinitialiser les filtres metier ne modifie pas le texte de recherche.
- Vider la recherche texte ne modifie pas les filtres metier.

**Tests recommandes**

- Recherche seule.
- Filtre traitement seul.
- Recherche + filtre traitement.
- Recherche + filtre traitement + filtre tache.

## Epic 3 - Interface de filtre et feedback utilisateur

### But

Ajouter une barre de filtres accessible et responsive, avec compteurs visibles et message d'absence de resultats.

### Valeur utilisateur

L'utilisateur comprend quels filtres sont actifs, peut les ajuster au clavier, et voit immediatement le nombre de cartes restantes.

### Stories

#### Story 3.1 - Ajouter la barre de filtres metier

**En tant que** utilisateur du tableau Kanban,  
**je veux** selectionner un traitement, une tache et leurs etats directement au-dessus du tableau,  
**afin de** filtrer sans quitter ma vue de travail.

**Portee technique**

- Modifier `web/kanban/templates/kanban/board.html`.
- Ajouter la barre sous l'en-tete et avant `.board-container`.
- Utiliser des champs de selection simples ou `input list` avec les catalogues `filter_traitements` et `filter_taches`.
- Ajouter quatre cases d'etat : traitement fait, traitement restant, tache faite, tache restante.
- Desactiver les cases d'un axe quand son libelle est vide.
- Ajouter le bouton `Reinitialiser les filtres`.

**Criteres d'acceptation**

- Le controle Traitement affiche le catalogue des traitements.
- Le controle Tache affiche le catalogue des taches.
- Les cases d'etat sont atteignables au clavier.
- Les cases d'etat sans libelle actif sont desactivees avec l'attribut `disabled`.
- Chaque changement declenche immediatement le filtrage.
- Le bouton de reinitialisation efface les deux libelles et les quatre cases.

**Tests recommandes**

- Navigation clavier dans l'ordre : traitement, etats traitement, tache, etats tache, reinitialiser, tableau.
- Verification desktop et largeur reduite.

#### Story 3.2 - Mettre a jour les compteurs et l'etat aucun resultat

**En tant que** utilisateur,  
**je veux** voir combien de cartes restent visibles et etre informe quand aucune carte ne correspond,  
**afin de** comprendre l'effet de mes filtres.

**Portee technique**

- Modifier `web/kanban/templates/kanban/board.html`.
- Ajouter le message global `Aucune carte ne correspond aux filtres` avec `aria-live="polite"`.
- Recalculer chaque `.count` a partir des cartes visibles dans la colonne.
- Afficher le message seulement quand aucune carte n'est visible sur tout le tableau.

**Criteres d'acceptation**

- Les compteurs de colonnes baissent quand des cartes sont masquees.
- Les compteurs reviennent apres reinitialisation.
- Le message aucun resultat apparait quand aucune carte visible ne reste.
- Le message disparait des qu'au moins une carte redevient visible.
- Les colonnes restent visibles pour conserver l'orientation.

**Tests recommandes**

- Filtre produisant un resultat partiel.
- Filtre produisant zero resultat.
- Reinitialisation apres zero resultat.

#### Story 3.3 - Styler la barre de filtres dans la grammaire visuelle existante

**En tant que** utilisateur,  
**je veux** une barre de filtres compacte et coherente avec le tableau,  
**afin de** l'utiliser sans perdre la lisibilite du Kanban.

**Portee technique**

- Modifier `web/kanban/static/kanban/css/style.css`.
- Ajouter les styles de la barre, des groupes, champs, cases et bouton.
- Respecter le theme sombre actuel.
- Ajouter une disposition responsive : horizontal desktop, groupes empiles en largeur reduite.
- Ne pas modifier la structure globale du tableau au-dela de l'espace necessaire a la barre.

**Criteres d'acceptation**

- La barre tient sur desktop sans chevauchement.
- La barre passe proprement en pile sur mobile ou largeur reduite.
- Les controles ont une hauteur tactile suffisante.
- Les textes ne debordent pas de leurs controles.
- Le tableau conserve son scroll horizontal.

**Tests recommandes**

- Verification visuelle desktop.
- Verification visuelle largeur reduite.
- Controle du contraste texte/fond.

## Epic 4 - Integration avec les interactions dynamiques du tableau

### But

Garantir que le filtre reste coherent apres tri, creation, suppression, drag-and-drop et rafraichissement AJAX de cartes.

### Valeur utilisateur

Le tableau ne perd pas l'etat des filtres pendant les operations courantes.

### Stories

#### Story 4.1 - Reappliquer le filtre apres mutations DOM

**En tant que** utilisateur,  
**je veux** que mes filtres restent actifs apres une action sur une carte,  
**afin de** ne pas revoir des cartes qui ne correspondent pas.

**Portee technique**

- Modifier les callbacks existants dans `board.html`.
- Appeler `applyBoardFilters()` apres :
  - tri manuel de colonne si necessaire ;
  - creation d'activite ;
  - suppression d'activite ;
  - `refreshActivityColumns(activityId)`;
  - deplacement drag-and-drop reussi.
- S'assurer que les cartes remplacees par AJAX sont reparses naturellement.

**Criteres d'acceptation**

- Apres creation d'une carte, elle est visible ou masquee selon le filtre courant.
- Apres suppression d'une carte, les compteurs et le message aucun resultat sont corrects.
- Apres drag-and-drop, les instances restantes respectent le filtre courant.
- Apres `refreshActivityColumns()`, aucune carte hors filtre n'est reaffichee.

**Tests recommandes**

- Appliquer un filtre puis deplacer une carte.
- Appliquer un filtre puis creer une carte.
- Appliquer un filtre puis supprimer une carte.
- Cocher/decocher des elements dans la modal si le refresh de colonnes est declenche par l'action.

#### Story 4.2 - Preserver les comportements existants non lies au filtre

**En tant que** utilisateur existant,  
**je veux** que le tri, les modales, le drag-and-drop et les colonnes virtuelles continuent de fonctionner,  
**afin que** le nouveau filtre n'introduise pas de regression.

**Portee technique**

- Verifier les interactions existantes dans `board.html`.
- Ne pas changer la logique serveur des colonnes virtuelles.
- Ne pas modifier les endpoints.
- Ne pas modifier le schema ou les modeles.

**Criteres d'acceptation**

- Le tri par date, nom, traitements et taches fonctionne encore.
- L'ouverture de modal par clic carte fonctionne encore.
- Le drag-and-drop superuser fonctionne encore.
- Les colonnes virtuelles continuent d'afficher les memes activites sans filtre actif.
- Les actions non-superuser restent limitees comme avant.

**Tests recommandes**

- Parcours manuel des interactions existantes avant/apres filtre.
- Verification sans filtre actif pour confirmer la non-regression de base.

## Epic 5 - Verification et documentation d'implementation

### But

Valider que la fonctionnalite couvre les criteres d'acceptation et documenter les points utiles pour maintenance.

### Valeur utilisateur

La fonctionnalite peut etre livree avec une confiance raisonnable et des regles compréhensibles pour les futures evolutions.

### Stories

#### Story 5.1 - Ajouter une verification automatisee minimale

**En tant que** mainteneur,  
**je veux** des tests ciblant les donnees et les cas de filtrage critiques,  
**afin de** detecter les regressions les plus probables.

**Portee technique**

- Ajouter ou etendre des tests Django dans `web/kanban/tests.py`, si l'environnement de test local le permet.
- Couvrir au minimum :
  - catalogues incluant faits/restants ;
  - rendu des attributs JSON de carte ;
  - absence de libelles vides.
- Si les tests JS ne sont pas pratiques dans ce repo, documenter la checklist manuelle dans l'artifact ou le compte rendu de story.

**Criteres d'acceptation**

- Les tests automatises passent localement ou les limites d'environnement sont documentees.
- Les tests couvrent au moins une valeur faite et une valeur restante pour traitement et tache.
- Les tests ne dependent pas de la base `organiseur.db` de production.

**Tests recommandes**

- `python web/manage.py test kanban` si compatible avec le schema unmanaged.
- Si le schema unmanaged bloque les tests, documenter le blocage et executer une verification manuelle structuree.

#### Story 5.2 - Executer la matrice d'acceptation fonctionnelle

**En tant que** responsable de livraison,  
**je veux** une verification explicite des AC du PRD,  
**afin de** savoir que la fonctionnalite est terminee.

**Portee technique**

- Executer une checklist manuelle ou automatisee couvrant AC-01 a AC-12.
- Inclure les cas de libelles proches et de combinaison ET.
- Verifier au moins une interaction dynamique avec filtre actif.

**Criteres d'acceptation**

- AC-01 a AC-12 sont marques passes ou documentes avec ecart.
- Aucun ecart bloquant connu ne reste ouvert.
- Les fichiers modifies sont listes dans le compte rendu d'implementation.

**Tests recommandes**

- Demarrer le serveur Django localement.
- Verifier la fonctionnalite dans le navigateur avec donnees de test representatives.

## 3. Ordre d'implementation recommande

1. Story 1.1 - Catalogues globaux.
2. Story 1.2 - Donnees JSON par carte.
3. Story 2.1 - Moteur de correspondance metier.
4. Story 3.1 - Barre de filtres.
5. Story 2.2 - Combinaison avec recherche texte.
6. Story 3.2 - Compteurs et aucun resultat.
7. Story 3.3 - Styles responsive.
8. Story 4.1 - Reapplication apres mutations DOM.
9. Story 4.2 - Non-regression interactions existantes.
10. Story 5.1 - Tests automatises minimaux.
11. Story 5.2 - Matrice d'acceptation.

## 4. Matrice de couverture PRD

| PRD | Stories |
| --- | --- |
| FR-01 | 1.1 |
| FR-02 | 1.1 |
| FR-03 | 3.1 |
| FR-04 | 3.1 |
| FR-05 | 1.2, 2.1 |
| FR-06 | 1.2, 2.1 |
| FR-07 | 1.2, 2.1 |
| FR-08 | 1.2, 2.1 |
| FR-09 | 2.1 |
| FR-10 | 2.1 |
| FR-11 | 2.1 |
| FR-12 | 2.1 |
| FR-13 | 2.1, 2.2 |
| FR-14 | 3.1 |
| FR-15 | 3.1, 2.2 |
| FR-16 | 3.2 |
| FR-17 | 2.2 |
| FR-18 | 2.1 |
| NFR-01 | 2.1, 4.1 |
| NFR-02 | 1.2, 2.1 |
| NFR-03 | 3.1, 3.3 |
| NFR-04 | 2.1, 5.1 |
| NFR-05 | 1.1, 1.2, 4.2 |

## 5. Definition of ready pour implementation

- Les trois artifacts sources existent et sont references dans ce document.
- Les stories indiquent les fichiers probables a modifier.
- Aucune story ne demande de migration de schema.
- Aucune story ne demande de nouvel endpoint.
- Les criteres d'acceptation couvrent les cas faits, restants, presence, combinaison ET, recherche texte, aucun resultat et libelles proches.

## 6. Definition of done globale

- Les catalogues affichent faits et restants.
- Les cartes exposent des donnees structurees exactes.
- Le filtre applique les regles du PRD en logique ET avec la recherche texte.
- Les compteurs et l'etat aucun resultat refletent les cartes visibles.
- Les operations dynamiques du tableau ne reaffichent pas les cartes hors filtre.
- Les interactions existantes restent fonctionnelles sans filtre actif.
- Les tests ou la matrice d'acceptation couvrent AC-01 a AC-12.
