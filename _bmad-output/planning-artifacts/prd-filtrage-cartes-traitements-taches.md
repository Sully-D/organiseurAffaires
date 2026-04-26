# PRD - Filtrage des cartes par traitements et taches

**Projet :** Organiseur d'Affaires  
**Date :** 2026-04-25  
**Statut :** Draft PRD  
**Type :** Brownfield - amelioration fonctionnelle web Kanban  

## 1. Resume executif

L'application web Organiseur d'Affaires doit permettre a l'utilisateur de filtrer les cartes Kanban selon la presence et l'etat des traitements et des taches associes aux scelles. Le filtre actuel permet deja une recherche texte et un filtrage simple sur les traitements ou taches en attente, mais il ne permet pas de distinguer clairement les elements faits, restants a faire, ni de combiner un critere traitement avec un critere tache.

Cette version vise un filtrage plus precis et verifiable : l'utilisateur choisit au maximum un traitement et au maximum une tache, puis indique pour chaque axe si l'element doit etre fait, restant a faire, ou simplement present. Les criteres traitement et tache se combinent en logique ET.

## 2. Probleme a resoudre

Les utilisateurs doivent retrouver rapidement les cartes liees a un travail precis, par exemple les cartes ou un traitement donne reste a faire, les cartes ou une tache donnee est deja terminee, ou les cartes qui combinent un traitement et une tache specifiques. Aujourd'hui, l'utilisateur peut filtrer certains elements restants, mais pas couvrir les cas faits/restants/presence avec des regles explicites.

## 3. Objectifs

- Afficher uniquement les cartes correspondant aux criteres de traitement et/ou tache selectionnes.
- Distinguer les etats "Fait" et "Restant a faire" pour les traitements et les taches.
- Permettre une recherche par presence explicite quand aucun etat ou les deux etats sont coches.
- Combiner les criteres traitement et tache en logique ET stricte.
- Conserver le comportement par defaut : sans filtre, toutes les cartes restent visibles.
- Appliquer les filtres immediatement, sans bouton "Appliquer".
- Permettre une reinitialisation rapide.

## 4. Hors perimetre

- Filtrer plusieurs traitements ou plusieurs taches simultanement sur un meme axe.
- Modifier le modele de donnees SQLite.
- Changer les regles des colonnes virtuelles existantes "Traitements", "Taches", "CTA", "Reparations".
- Ajouter une persistance utilisateur des filtres entre sessions.
- Refondre l'interface globale du tableau Kanban.
- Implementer la meme interface dans l'application desktop PySide6 dans cette version.

## 5. Utilisateurs cibles

- Utilisateur principal du tableau Kanban web, qui suit des activites, scelles, traitements et taches.
- Administrateur/superutilisateur web, qui modifie les cartes et coche les traitements ou taches.

## 6. Parcours utilisateur

### Parcours 1 - Voir les cartes avec un traitement restant

1. L'utilisateur ouvre le tableau Kanban.
2. Il ouvre le panneau de filtres.
3. Il selectionne un traitement dans le catalogue.
4. Il coche "Restant a faire".
5. Le tableau masque les cartes qui ne contiennent pas ce traitement non coche.

### Parcours 2 - Voir les cartes ou une tache est faite

1. L'utilisateur selectionne une tache.
2. Il coche "Fait".
3. Le tableau affiche uniquement les cartes ou cette tache est explicitement presente et cochee.

### Parcours 3 - Combiner traitement et tache

1. L'utilisateur selectionne un traitement avec l'etat "Restant a faire".
2. Il selectionne une tache avec l'etat "Fait".
3. Le tableau affiche uniquement les cartes respectant les deux criteres simultanement.

### Parcours 4 - Revenir a la vue complete

1. L'utilisateur clique sur "Reinitialiser".
2. Les selections traitement/tache et les etats sont effaces.
3. Toutes les cartes visibles avant filtrage redeviennent affichees, sous reserve de la recherche texte courante si elle reste active.

## 7. Exigences fonctionnelles

### FR-01 - Catalogue global des traitements

Le filtre traitement doit proposer les descriptions de traitements connues par l'application, y compris les traitements faits et non faits, en excluant les descriptions vides.

### FR-02 - Catalogue global des taches

Le filtre tache doit proposer les descriptions de taches connues par l'application, y compris les taches faites et non faites, en excluant les descriptions vides.

### FR-03 - Selection simple par axe

L'utilisateur peut selectionner au maximum un traitement et au maximum une tache dans la version initiale.

### FR-04 - Etats par axe

Pour chaque axe selectionne, l'interface propose deux etats :

- Fait
- Restant a faire

### FR-05 - Correspondance traitement fait

Une carte correspond a un traitement "Fait" si au moins un scelle de la carte contient explicitement un traitement avec la description selectionnee et `done = true`.

### FR-06 - Correspondance traitement restant

Une carte correspond a un traitement "Restant a faire" si au moins un scelle de la carte contient explicitement un traitement avec la description selectionnee et `done = false`.

### FR-07 - Correspondance tache faite

Une carte correspond a une tache "Fait" si au moins un scelle de la carte contient explicitement une tache avec la description selectionnee et `done = true`.

### FR-08 - Correspondance tache restante

Une carte correspond a une tache "Restant a faire" si au moins un scelle de la carte contient explicitement une tache avec la description selectionnee et `done = false`.

### FR-09 - Presence explicite sans etat

Si un traitement ou une tache est selectionne sans etat coche, la carte correspond si l'element est explicitement present, quel que soit son etat.

### FR-10 - Presence explicite avec deux etats

Si "Fait" et "Restant a faire" sont tous les deux coches pour un axe, la carte correspond si l'element est explicitement present, quel que soit son etat.

### FR-11 - Combinaison ET

Si un traitement et une tache sont selectionnes, une carte doit respecter les deux criteres pour rester affichee.

### FR-12 - Filtrage partiel

Si seul un traitement est selectionne, les taches ne sont pas prises en compte. Si seule une tache est selectionnee, les traitements ne sont pas pris en compte.

### FR-13 - Aucun filtre

Sans traitement ni tache selectionne, le filtre metier ne masque aucune carte.

### FR-14 - Application immediate

Le filtrage s'applique immediatement a chaque changement de selection ou d'etat.

### FR-15 - Reinitialisation

Un bouton reinitialise les selections traitement/tache et les cases d'etat. La recherche texte existante peut rester independante, sauf decision UX contraire.

### FR-16 - Aucun resultat

Si aucune carte ne correspond aux criteres, l'interface affiche un message explicite : "Aucune carte ne correspond aux filtres".

### FR-17 - Compatibilite avec la recherche texte

Le nouveau filtre doit se combiner avec la recherche texte existante. Une carte reste visible uniquement si elle correspond a la recherche texte et aux criteres metier selectionnes.

### FR-18 - Exactitude des libelles

Les comparaisons de descriptions doivent eviter les faux positifs dus a des correspondances partielles. Par exemple, "Controle" ne doit pas matcher "Controle final" sauf si c'est exactement le libelle selectionne.

## 8. Exigences non fonctionnelles

### NFR-01 - Performance percue

Sur le volume courant du tableau, chaque changement de filtre doit mettre a jour l'affichage sans latence perceptible.

### NFR-02 - Robustesse des donnees

Le filtre ne doit pas modifier les cartes, scelles, traitements ou taches. Il agit uniquement sur l'affichage.

### NFR-03 - Accessibilite minimale

Les controles doivent avoir des libelles visibles ou accessibles et rester utilisables au clavier.

### NFR-04 - Maintenabilite

La logique de filtrage doit etre lisible et testable. Les regles "fait", "restant" et "presence" doivent etre isolees plutot que dispersees dans des comparaisons ad hoc.

### NFR-05 - Compatibilite brownfield

La solution doit respecter l'architecture existante : Django rend le tableau, les cartes utilisent des attributs de donnees, et le filtrage actuel s'execute cote navigateur.

## 9. Contraintes et dependances

- Le schema de donnees actuel contient `Traitement.done` et `Tache.done`, suffisants pour cette version.
- Le tableau web expose deja des listes de suggestions et des donnees de cartes, mais seulement pour les elements en attente. Il faudra etendre ces donnees aux elements faits et non faits.
- Les colonnes virtuelles existantes peuvent afficher la meme activite dans plusieurs colonnes ; le filtre doit traiter chaque carte rendue de facon coherente.
- Les donnees Desktop et Web partagent `organiseur.db`; aucune migration n'est attendue pour cette fonctionnalite.

## 10. Criteres d'acceptation

- AC-01 : Avec aucun filtre selectionne, le tableau affiche les memes cartes qu'avant la fonctionnalite.
- AC-02 : En selectionnant un traitement et "Restant a faire", seules les cartes contenant ce traitement non coche restent visibles.
- AC-03 : En selectionnant un traitement et "Fait", seules les cartes contenant ce traitement coche restent visibles.
- AC-04 : En selectionnant une tache et "Restant a faire", seules les cartes contenant cette tache non cochee restent visibles.
- AC-05 : En selectionnant une tache et "Fait", seules les cartes contenant cette tache cochee restent visibles.
- AC-06 : En selectionnant un traitement sans etat, toutes les cartes contenant explicitement ce traitement restent visibles, quel que soit l'etat.
- AC-07 : En cochant "Fait" et "Restant a faire" pour un axe, le resultat est identique au filtrage par presence de cet element.
- AC-08 : En combinant un traitement et une tache, seules les cartes satisfaisant les deux criteres restent visibles.
- AC-09 : Une carte dont le texte contient un libelle proche mais sans element explicite correspondant n'est pas affichee.
- AC-10 : Le bouton de reinitialisation remet le filtre metier a zero.
- AC-11 : Quand aucun resultat ne correspond, le message "Aucune carte ne correspond aux filtres" est visible.
- AC-12 : La recherche texte existante continue de fonctionner et se combine avec les filtres.

## 11. Risques

- Les attributs HTML actuels stockent seulement les noms d'elements en attente, ce qui ne couvre pas les elements faits.
- Les comparaisons actuelles par `includes` peuvent produire des faux positifs si deux libelles se ressemblent.
- Les cartes dupliquees dans plusieurs colonnes virtuelles peuvent rendre l'effet du filtre plus difficile a percevoir si le message "aucun resultat" n'est pas gere globalement.

## 12. Mesures de succes

- L'utilisateur peut identifier une carte par traitement ou tache specifique sans ouvrir manuellement chaque carte.
- Les cas faits/restants/presence sont compris sans clarification externe.
- Les faux positifs de correspondance de libelle sont elimines.
- La fonctionnalite ne degrade pas la recherche globale ni l'affichage Kanban existant.

## 13. Notes d'implementation pour la suite

- Preferer des attributs de donnees structures par carte pour les traitements et taches faits/restants, ou une representation JSON echappee correctement.
- Alimenter les catalogues depuis toutes les descriptions distinctes, pas seulement `done = false`.
- Conserver les endpoints existants pour les suggestions, sauf si une API dediee devient necessaire.
- Ajouter des tests de logique de filtrage pour les combinaisons principales et les libelles proches.
