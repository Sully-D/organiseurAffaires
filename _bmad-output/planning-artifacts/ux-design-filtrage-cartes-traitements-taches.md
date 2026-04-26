---
title: 'UX Design - Filtrage des cartes par traitements et taches'
slug: 'ux-design-filtrage-cartes-traitements-taches'
created: '2026-04-25'
status: 'ready-for-architecture'
source_prd: '_bmad-output/planning-artifacts/prd-filtrage-cartes-traitements-taches.md'
workflow: 'bmad-create-ux-design'
agent: 'ux-designer'
---

# UX Design - Filtrage des cartes par traitements et taches

## 1. Objectif UX

Permettre a l'utilisateur de retrouver rapidement les cartes Kanban qui contiennent un traitement ou une tache specifique, en distinguant clairement les elements faits, les elements restants a faire, et la simple presence d'un element.

La solution doit rester compatible avec l'interface existante : tableau horizontal, recherche globale dans l'en-tete, cartes compactes, tri par colonne et modale de detail.

## 2. Principes de conception

- Le filtre doit etre visible au moment ou l'utilisateur lit le tableau, sans ouvrir une page dediee.
- Les controles doivent parler le langage metier : "Traitement", "Tache", "Fait", "Restant a faire".
- Le comportement par defaut doit rester neutre : aucun critere metier ne masque de carte.
- Chaque changement doit s'appliquer immediatement.
- La recherche texte et les filtres metier doivent etre percus comme deux couches complementaires.
- L'etat "presence" ne doit pas etre un troisieme bouton : il decoule naturellement de l'absence d'etat coche ou des deux etats coches.

## 3. Structure recommandee

Ajouter une barre de filtres metier sous l'en-tete principal et au-dessus du tableau Kanban.

Disposition desktop :

```text
[Recherche existante dans l'en-tete]

[Traitement: select/search] [Fait] [Restant a faire]   [Tache: select/search] [Fait] [Restant a faire]   [Reinitialiser]

[Colonnes Kanban]
```

Disposition mobile ou largeur reduite :

```text
[Traitement: select/search]
[Fait] [Restant a faire]
[Tache: select/search]
[Fait] [Restant a faire]
[Reinitialiser]
[Colonnes Kanban scrollables]
```

La barre doit utiliser la meme grammaire visuelle que l'application : fond sombre, bordure discrete, controles compacts, boutons d'etat lisibles, sans changer la densite du tableau.

## 4. Controles

### Traitement

Controle principal : un champ de selection avec recherche ou un `select` enrichi par une `datalist`.

Etat vide :

- Placeholder : `Traitement`
- Aucun critere traitement applique.

Etat selectionne :

- Le libelle exact est affiche.
- Les cases "Fait" et "Restant a faire" deviennent le modificateur d'etat pour ce traitement.

### Tache

Controle symetrique au controle Traitement.

Etat vide :

- Placeholder : `Tache`
- Aucun critere tache applique.

Etat selectionne :

- Le libelle exact est affiche.
- Les cases "Fait" et "Restant a faire" deviennent le modificateur d'etat pour cette tache.

### Etats

Utiliser des cases a cocher ou des toggles accessibles, pas une liste deroulante.

- Aucun etat coche : presence explicite, quel que soit l'etat.
- "Fait" seul : element explicitement present et coche.
- "Restant a faire" seul : element explicitement present et non coche.
- Les deux etats coches : presence explicite, quel que soit l'etat.

Les controles d'etat doivent rester disponibles meme si aucun libelle n'est selectionne, mais inactifs visuellement ou sans effet. Pour eviter l'ambiguite, recommandation UX : les desactiver tant que l'axe correspondant n'a pas de selection.

### Reinitialiser

Commande secondaire, a droite sur desktop, sous les champs sur mobile.

Comportement :

- Efface le traitement selectionne.
- Efface la tache selectionnee.
- Decoche les quatre etats.
- Ne modifie pas la recherche texte existante.

Libelle recommande : `Reinitialiser les filtres`.

## 5. Feedback utilisateur

### Compteurs de colonnes

Les compteurs de colonnes doivent refleter le nombre de cartes actuellement visibles dans chaque colonne apres filtrage. Si l'implementation conserve le total d'origine, l'utilisateur risque de croire que le filtre ne fonctionne pas.

Recommandation :

- compteur normal : cartes visibles dans la colonne ;
- titre ou `aria-label` optionnel : nombre total avant filtre si utile plus tard.

### Aucun resultat

Afficher un message global dans la zone du tableau quand aucune carte visible ne reste :

`Aucune carte ne correspond aux filtres`

Le message doit apparaitre seulement apres evaluation combinee de la recherche texte et des filtres metier.

Position :

- centree dans la zone de contenu ;
- sous la barre de filtres ;
- sans masquer les colonnes si elles restent necessaires pour l'orientation.

### Etat actif

Quand au moins un axe metier est actif, la barre doit rendre cet etat visible.

Exemples de feedback discret :

- bouton Reinitialiser visible et actif ;
- bordure ou accent sur la barre ;
- texte court possible : `Filtres actifs`, si l'espace le permet.

Eviter les badges redondants si les selections sont deja visibles dans les champs.

## 6. Regles d'interaction

### Logique de filtre

L'interface applique une logique ET stricte entre :

- la recherche texte existante ;
- le critere traitement, s'il existe ;
- le critere tache, s'il existe.

Une carte reste visible uniquement si elle satisfait toutes les couches actives.

### Exactitude des libelles

La selection doit matcher des valeurs structurees, pas du texte de carte ni une sous-chaine.

Exemples :

- `Controle` ne matche pas `Controle final`.
- `Controle final` ne matche pas `Controle`.
- Les accents et espaces doivent suivre le libelle stocke, avec normalisation seulement si elle est explicite et coherente dans tout le catalogue.

### Cartes dupliquees dans les colonnes virtuelles

Une meme activite peut etre rendue dans plusieurs colonnes virtuelles. Le filtrage doit traiter chaque instance de carte de facon coherente.

Regle UX :

- si l'activite correspond au filtre, toutes ses instances rendues dans les colonnes applicables restent visibles ;
- si elle ne correspond pas, toutes ses instances sont masquees ;
- le message "aucun resultat" regarde l'ensemble du tableau, pas colonne par colonne.

## 7. Accessibilite

- Chaque champ de selection doit avoir un libelle accessible.
- Les cases d'etat doivent etre atteignables au clavier.
- L'ordre de tabulation doit suivre : traitement, etats traitement, tache, etats tache, reinitialiser, tableau.
- Le message aucun resultat doit etre annonce via une region `aria-live="polite"` si possible.
- Les controles desactives doivent exposer `disabled`, pas seulement une opacite CSS.
- Le contraste doit rester au niveau de l'interface existante : texte clair sur fond sombre, accent reserve aux elements actifs ou interactifs.

## 8. Responsive

Desktop :

- Barre horizontale en une ligne si l'espace le permet.
- Largeurs minimales stables pour les champs afin d'eviter les sauts de mise en page.
- Le tableau conserve son scroll horizontal.

Tablette :

- Deux groupes flexibles : Traitement et Tache.
- Le bouton Reinitialiser peut passer a la ligne.

Mobile :

- Barre en pile verticale.
- Groupes d'etats sous chaque champ.
- Cibles tactiles suffisantes, minimum 36 px de hauteur.

## 9. Etats visuels attendus

### Aucun filtre actif

- Champs vides.
- Etats desactives ou non accentues.
- Bouton Reinitialiser inactif ou discret.
- Toutes les cartes visibles selon le comportement actuel.

### Filtre traitement actif

- Champ Traitement rempli.
- Etats Traitement actifs.
- Axe Tache neutre si vide.
- Les cartes visibles respectent le critere traitement et la recherche texte.

### Filtre tache actif

- Champ Tache rempli.
- Etats Tache actifs.
- Axe Traitement neutre si vide.
- Les cartes visibles respectent le critere tache et la recherche texte.

### Filtre combine

- Les deux champs sont remplis.
- Les cartes visibles respectent les deux criteres en logique ET.

### Aucun resultat

- Aucune carte visible.
- Message global affiche.
- Reinitialiser reste disponible.
- Les selections restent visibles pour que l'utilisateur comprenne la cause.

## 10. Donnees necessaires a l'interface

Pour supporter ce design, chaque carte doit exposer des donnees structurees couvrant faits et restants.

Representation recommandee :

- `data-traitements` : JSON encode contenant les libelles exacts et leur etat.
- `data-taches` : JSON encode contenant les libelles exacts et leur etat.

Exemple conceptuel :

```json
[
  {"description": "Controle final", "done": true},
  {"description": "Photographie", "done": false}
]
```

Le catalogue des selections doit venir de toutes les descriptions distinctes non vides, pas seulement des elements en attente.

## 11. Impacts sur l'interface existante

Fichiers concernes probables :

- `web/kanban/templates/kanban/base.html` : emplacement actuel de la recherche globale et du filtre simple.
- `web/kanban/templates/kanban/board.html` : emplacement adapte pour une barre de filtres metier au-dessus du tableau.
- `web/kanban/templates/kanban/card_snippet.html` : donnees structurees par carte.
- `web/kanban/static/kanban/css/style.css` : style de la barre, controles, responsive, et message aucun resultat.
- `web/kanban/views.py` : alimentation des catalogues complets traitements/taches.

Le filtre simple actuel dans l'en-tete peut etre conserve pendant la transition, mais le design cible recommande de remplacer les options "Traitements Specifiques" et "Taches Specifiques" par la nouvelle barre metier pour eviter deux systemes concurrents.

## 12. Criteres UX d'acceptation

- L'utilisateur identifie en moins d'un regard ou selectionner un traitement et une tache.
- Les etats "Fait" et "Restant a faire" sont visibles sans ouvrir de menu.
- La presence explicite est comprehensible : selectionner un libelle sans cocher d'etat affiche tous les cas de ce libelle.
- Le bouton de reinitialisation remet le filtre metier a zero sans effacer la recherche texte.
- Les compteurs et le message aucun resultat correspondent a ce qui est visible.
- Le filtrage ne depend jamais d'une correspondance partielle de texte.
- La barre reste utilisable au clavier et sur petit ecran.

## 13. Decision UX pour la suite

Le design retenu est une barre de filtres metier compacte, placee au-dessus du tableau, avec deux axes symetriques :

- Traitement + etats.
- Tache + etats.

Cette solution couvre le PRD sans refondre l'interface globale et donne a l'architecture suivante des contraintes claires : donnees structurees par carte, catalogue complet, logique de matching exacte, feedback global aucun resultat et compteurs recalcules.
