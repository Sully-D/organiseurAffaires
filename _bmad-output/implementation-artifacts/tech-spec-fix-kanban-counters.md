---
title: 'Corriger les compteurs de traitements et tâches dans le Kanban Django'
slug: 'fix-kanban-counters'
created: '2026-01-29T19:58:46+01:00'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['Django 4.x', 'Python 3.8+', 'SQLite 3', 'Django ORM', 'Subquery', 'Coalesce']
files_to_modify: ['web/kanban/views.py']
code_patterns: ['Django Subquery', 'OuterRef', 'Count aggregation', 'Coalesce for NULL handling']
test_patterns: ['Manual testing via browser', 'Django runserver']
---

# Tech-Spec: Corriger les compteurs de traitements et tâches dans le Kanban Django

**Created:** 2026-01-29T19:58:46+01:00

## Overview

### Problem Statement

Les compteurs de traitements et tâches affichés sur les cartes Kanban de la page principale (`http://127.0.0.1:8000/`) sont **complètement incorrects**. 

**Cause racine :** L'utilisation de `Count('scelles__traitements', filter=Q(scelles__traitements__done=False))` et `Count('scelles__taches', filter=Q(scelles__taches__done=False))` dans les annotations Django, combinée avec des filtres complexes et `.distinct()` sur les activités, provoque des comptages erronés.

**Mécanisme du bug :** Les relations en cascade `Activity → Scelle → Traitement/Tache` créent des JOINs multiples. Quand Django applique `.distinct()` sur l'Activity, les annotations Count() ne sont pas correctement déduplicées, résultant en des comptages multipliés ou incorrects.

### Solution

Remplacer les annotations `Count()` problématiques par des **sous-requêtes `Subquery`** qui calculent indépendamment le nombre de traitements et tâches non terminés pour chaque activité, sans être affectées par les JOINs de la requête principale.

**Approche technique :**
- Utiliser `Subquery` avec `Count` pour isoler le comptage dans une requête séparée
- Annoter les résultats sur le queryset principal via `OuterRef`
- Garantir que les comptages restent précis même avec des filtres complexes et `.distinct()`

### Scope

**In Scope:**
- Correction de la fonction `board()` dans `web/kanban/views.py` (lignes 17-164)
- Correction de la fonction `get_activity_columns()` dans `web/kanban/views.py` (lignes 560-645)
- Les annotations `pending_traitements` et `pending_taches` doivent afficher le nombre exact de traitements/tâches avec `done=False`
- Le compteur de scellés (`activity.scelles.count`) fonctionne correctement et ne doit pas être modifié

**Out of Scope:**
- Modification du template `card_snippet.html` (l'affichage est déjà correct)
- Modification des modèles Django dans `models.py`
- Autres vues ou fonctions qui n'utilisent pas ces annotations spécifiques
- Modification de la logique métier de filtrage des colonnes (Traitements, Tâches, CTA, etc.)

## Context for Development

### Codebase Patterns

**Architecture :** Application Django multi-part (Desktop PySide6 + Web Django) partageant une base SQLite.

**Modèle de données :**
- `Activity` (1) → `Scelle` (N) → `Traitement/Tache` (N)
- Relations : `activity.scelles.all()` → `scelle.traitements.all()` / `scelle.taches.all()`
- Tous les modèles Django ont `managed = False` (schéma géré par SQLAlchemy côté Desktop)
- Relations définies dans `web/kanban/models.py` :
  - `Scelle.activity` (ForeignKey vers Activity, related_name='scelles')
  - `Traitement.scelle` (ForeignKey vers Scelle, related_name='traitements')
  - `Tache.scelle` (ForeignKey vers Scelle, related_name='taches')

**Imports Django ORM actuels (ligne 4 de views.py) :**
```python
from django.db.models import Q, F, Count, Exists, OuterRef
```

**Imports requis après correction :**
```python
from django.db.models import Q, F, Count, Exists, OuterRef, Subquery, Value, IntegerField
from django.db.models.functions import Coalesce
```

**Pattern actuel (problématique) - 8 occurrences identiques :**

Localisations exactes dans `views.py` :
- Ligne 39-40 : Colonne "Traitements"
- Ligne 59-60 : Colonne "Tâches"
- Ligne 74-75 : Colonne "CTA"
- Ligne 89-90 : Colonne "Réparations"
- Ligne 108-109 : Colonne "En attente"
- Ligne 135-136 : Colonne "En cours"
- Ligne 147-148 : Else case (autres colonnes)
- Ligne 563-564 : Fonction `get_activity_columns()`

```python
activities = Activity.objects.filter(...).prefetch_related(
    'tags', 'scelles__traitements', 'scelles__taches'
).distinct().annotate(
    pending_traitements=Count('scelles__traitements', filter=Q(scelles__traitements__done=False)),
    pending_taches=Count('scelles__taches', filter=Q(scelles__taches__done=False)),
    has_cta=Exists(Scelle.objects.filter(activity=OuterRef('pk'), cta_validated=True)),
    has_reparations=Exists(Scelle.objects.filter(activity=OuterRef('pk'), reparations_validated=True))
).order_by('date')
```

**Problème :** Le `.distinct()` combiné avec des filtres complexes (Q() objects) sur les relations many-to-many crée des JOINs multiples. Le `Count()` compte les lignes du résultat JOIN plutôt que les objets uniques.

**Pattern attendu (solution CORRIGÉE) :**

Créer des subqueries réutilisables en début de fonction `board()` :

```python
from django.db.models import Subquery, OuterRef, Count, Value, IntegerField
from django.db.models.functions import Coalesce

# Créer les subqueries une seule fois au début de la fonction
# Compte directement les Traitements à travers la relation scelle__activity
pending_traitements_subquery = Traitement.objects.filter(
    scelle__activity=OuterRef('pk'),
    done=False
).values('scelle__activity').annotate(
    total=Count('id')
).values('total')

pending_taches_subquery = Tache.objects.filter(
    scelle__activity=OuterRef('pk'),
    done=False
).values('scelle__activity').annotate(
    total=Count('id')
).values('total')

# Puis utiliser dans toutes les annotations avec Coalesce pour gérer NULL:
activities = Activity.objects.filter(...).prefetch_related(
    'tags', 'scelles__traitements', 'scelles__taches'
).distinct().annotate(
    pending_traitements=Coalesce(
        Subquery(pending_traitements_subquery, output_field=IntegerField()),
        Value(0)
    ),
    pending_taches=Coalesce(
        Subquery(pending_taches_subquery, output_field=IntegerField()),
        Value(0)
    ),
    has_cta=Exists(Scelle.objects.filter(activity=OuterRef('pk'), cta_validated=True)),
    has_reparations=Exists(Scelle.objects.filter(activity=OuterRef('pk'), reparations_validated=True))
).order_by('date')
```

**Avantagesde cette approche :**
1. Les subqueries sont isolées du queryset principal → pas d'interférence avec `.distinct()`
2. Réutilisables pour les 7 occurrences dans `board()`
3. Performance similaire ou meilleure (Django optimise les subqueries)
4. `Coalesce` garantit qu'on retourne 0 au lieu de NULL pour les activités sans traitements/tâches
5. Compte directement les objets Traitement/Tache via la relation, plus simple et plus clair

### Files to Reference

| File | Purpose |
| ---- | ------- |
| [web/kanban/views.py](file:///home/sdl-eos/Programmation/organiseurAffaires/web/kanban/views.py) | Contient les fonctions `board()` et `get_activity_columns()` à corriger |
| [web/kanban/models.py](file:///home/sdl-eos/Programmation/organiseurAffaires/web/kanban/models.py) | Définitions des modèles Activity, Scelle, Traitement, Tache |
| [web/kanban/templates/kanban/card_snippet.html](file:///home/sdl-eos/Programmation/organiseurAffaires/web/kanban/templates/kanban/card_snippet.html) | Template utilisant les compteurs (lignes 33-38) |

### Technical Decisions

**Décision 1 : Utiliser des Subquery au lieu de Count direct**
- **Raison :** Isoler le comptage dans une requête indépendante évite les problèmes de duplication causés par les JOINs multiples
- **Alternative rejetée :** Calcul dans le template (Option B) - moins performant, nécessiterait des itérations supplémentaires

**Décision 2 : Corriger aussi `get_activity_columns()`**
- **Raison :** Cette fonction est appelée après chaque modification d'activité pour rafraîchir l'affichage. Elle a exactement le même bug.
- **Impact :** Garantit la cohérence des compteurs après les modifications AJAX

**Décision 3 : Conserver le pattern `Exists()` pour `has_cta` et `has_reparations`**
- **Raison :** Les `Exists()` fonctionnent correctement (booléens, pas de comptages)
- **Impact :** Pas besoin de les modifier

## Implementation Plan

### Tasks

Les tâches sont ordonnées par dépendances (modifications de base d'abord, puis applications spécifiques).

- [ ] **Task 1: Ajouter les imports manquants pour Subquery et Coalesce**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Modifier les imports en haut du fichier (actuellement ligne 4)
  - **Changement exact:**
    ```python
    # Avant:
    from django.db.models import Q, F, Count, Exists, OuterRef
    
    # Après:
    from django.db.models import Q, F, Count, Exists, OuterRef, Subquery, Value, IntegerField
    from django.db.models.functions import Coalesce
    ```
  - **Notes:** Imports requis pour utiliser les subqueries avec gestion NULL dans les étapes suivantes

- [ ] **Task 2: Créer les subqueries réutilisables dans la fonction board()**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Ajouter les subqueries au début de la fonction `board()`, après la ligne de déclaration des colonnes (`columns = KanbanColumn.objects.exclude(name='Archivé').order_by('order_index')`)
  - **Code à insérer:**
    ```python
    
    # Create reusable subqueries for accurate pending counts
    pending_traitements_subquery = Traitement.objects.filter(
        scelle__activity=OuterRef('pk'),
        done=False
    ).values('scelle__activity').annotate(
        total=Count('id')
    ).values('total')
    
    pending_taches_subquery = Tache.objects.filter(
        scelle__activity=OuterRef('pk'),
        done=False
    ).values('scelle__activity').annotate(
        total=Count('id')
    ).values('total')
    ```
  - **Notes:** Ces subqueries comptent directement les Traitement/Tache objets via la relation `scelle__activity`, évitant la double agrégation problématique. Elles sont isolées du queryset principal et ne sont pas affectées par `.distinct()`.


- [ ] **Task 3: Remplacer l'annotation pour la colonne "Traitements"**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Remplacer les annotations `Count()` par les `Subquery` avec `Coalesce`
  - **Localisation:** Dans le bloc `if col.name == "Traitements":`, trouver les lignes `.annotate(pending_traitements=Count(...), pending_taches=Count(...))`
  - **Changement:**
    ```python
    # Avant:
    pending_traitements=Count('scelles__traitements', filter=Q(scelles__traitements__done=False)),
    pending_taches=Count('scelles__taches', filter=Q(scelles__taches__done=False)),
    
    # Après:
    pending_traitements=Coalesce(
        Subquery(pending_traitements_subquery, output_field=IntegerField()),
        Value(0)
    ),
    pending_taches=Coalesce(
        Subquery(pending_taches_subquery, output_field=IntegerField()),
        Value(0)
    ),
    ```

- [ ] **Task 4: Remplacer l'annotation pour la colonne "Tâches"**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Même remplacement que Task 3
  - **Localisation:** Dans le bloc `elif col.name == "Tâches":`, annotations pending_traitements/pending_taches

- [ ] **Task 5: Remplacer l'annotation pour la colonne "CTA"**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Même remplacement que Task 3
  - **Localisation:** Dans le bloc `elif col.name == "CTA":`, annotations pending_traitements/pending_taches

- [ ] **Task 6: Remplacer l'annotation pour la colonne "Réparations"**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Même remplacement que Task 3
  - **Localisation:** Dans le bloc `elif col.name == "Réparations":`, annotations pending_traitements/pending_taches

- [ ] **Task 7: Remplacer l'annotation pour la colonne "En attente"**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Même remplacement que Task 3
  - **Localisation:** Dans le bloc `elif col.name == "En attente":`, annotations pending_traitements/pending_taches

- [ ] **Task 8: Remplacer l'annotation pour la colonne "En cours"**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Même remplacement que Task 3
  - **Localisation:** Dans le bloc `elif col.name == "En cours":`, annotations pending_traitements/pending_taches

- [ ] **Task 9: Remplacer l'annotation pour le else case (autres colonnes)**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Même remplacement que Task 3
  - **Localisation:** Dans le bloc `else:` (après tous les `elif`), annotations pending_traitements/pending_taches


- [ ] **Task 10: Corriger la fonction get_activity_columns()**
  - **Fichier:** `web/kanban/views.py`
  - **Action:** Créer les mêmes subqueries localement dans cette fonction et remplacer les annotations
  - **Localisation:** Dans la fonction `get_activity_columns(request, activity_id)`, avant le `.annotate()` de l'objet `activity`, insérer les subqueries
  - **Code à insérer avant l'annotation:**
    ```python
    # Create subqueries for accurate counts
    pending_traitements_subquery = Traitement.objects.filter(
        scelle__activity=OuterRef('pk'),
        done=False
    ).values('scelle__activity').annotate(
        total=Count('id')
    ).values('total')
    
    pending_taches_subquery = Tache.objects.filter(
        scelle__activity=OuterRef('pk'),
        done=False
    ).values('scelle__activity').annotate(
        total=Count('id')
    ).values('total')
    ```
  - **Puis remplacer les lignes d'annotation par:**
    ```python
    pending_traitements=Coalesce(
        Subquery(pending_traitements_subquery, output_field=IntegerField()),
        Value(0)
    ),
    pending_taches=Coalesce(
        Subquery(pending_taches_subquery, output_field=IntegerField()),
        Value(0)
    ),
    ```
  - **Notes:** Cette fonction ne peut pas réutiliser les subqueries de `board()` car elle est appelée séparément via AJAX. Le code est dupliqué (voir Finding F9) mais accepté pour simplicité.


### Acceptance Criteria

- [ ] **AC1: Compteurs corrects pour activités avec un seul scellé**
  - **Given** une activité avec 1 scellé ayant 2 traitements non faits et 3 tâches non faites
  - **When** j'affiche la page Kanban principale
  - **Then** la carte affiche "2" pour traitements et "3" pour tâches

- [ ] **AC2: Compteurs corrects pour activités avec plusieurs scellés**
  - **Given** une activité avec 3 scellés :
    - Scellé 1: 2 traitements non faits, 1 tâche non faite
    - Scellé 2: 1 traitement non fait, 2 tâches non faites
    - Scellé 3: 0 traitements, 0 tâches
  - **When** j'affiche la page Kanban
  - **Then** la carte affiche "3" pour traitements (2+1+0) et "3" pour tâches (1+2+0)

- [ ] **AC3: Compteurs ignorent les traitements/tâches terminés**
  - **Given** une activité avec 1 scellé ayant :
    - 2 traitements avec done=True
    - 1 traitement avec done=False
    - 3 tâches avec done=True
    - 2 tâches avec done=False
  - **When** j'affiche la page Kanban
  - **Then** la carte affiche "1" pour traitements et "2" pour tâches

- [ ] **AC4: Compteurs corrects sur toutes les colonnes spéciales**
  - **Given** des activités dans les colonnes Traitements, Tâches, CTA, Réparations, En attente, En cours
  - **When** j'affiche la page Kanban
  - **Then** toutes les cartes affichent des compteurs corrects selon leur contenu réel

- [ ] **AC5: Compteurs corrects après modification AJAX**
  - **Given** une activité visible sur le Kanban
  - **When** j'ajoute un traitement via l'interface AJAX
  - **Then** la carte se rafraîchit et affiche le nouveau compteur correct

- [ ] **AC6: Compteur de scellés non affecté**
  - **Given** une activité avec 3 scellés
  - **When** j'affiche la page Kanban
  - **Then** le compteur de scellés affiche toujours "3" (pas de régression)

- [ ] **AC7: Performance acceptable**
  - **Given** le tableau Kanban avec 50+ activités
  - **When** je charge la page principale
  - **Then** le temps de chargement est similaire ou meilleur qu'avant le fix

- [ ] **AC8: Pas d'erreur SQL ou Django**
  - **Given** le serveur Django en mode debug
  - **When** j'utilise toutes les fonctionnalités du Kanban (affichage, modification, filtres)
  - **Then** aucune erreur SQL ou Django n'apparaît dans les logs

- [ ] **AC9: Compteurs corrects pour activité sans scellés (cas limite)**
  - **Given** une activité qui n'a **aucun scellé** attaché
  - **When** j'affiche la page Kanban
  - **Then** la carte affiche "0" pour traitements et "0" pour tâches (grâce à Coalesce)

## Additional Context

### Dependencies

**Dépendances existantes (déjà installées) :**
- Django 4.x - Framework web principal
- Django ORM - Pour les annotations et subqueries
- SQLite 3 - Base de données partagée

**Nouvelles dépendances requises :**
- Aucune - Toutes les fonctionnalités nécessaires (`Subquery`, `Sum`, `OuterRef`) sont natives de Django ORM

**Dépendances internes :**
- Les modèles `Activity`, `Scelle`, `Traitement`, `Tache` dans `web/kanban/models.py` doivent rester inchangés
- Le template `card_snippet.html` utilise les attributs `pending_traitements` et `pending_taches` - la compatibilité est maintenue

### Testing Strategy

**Tests manuels (REQUIS avant de considérer le fix complet) :**

1. **Test de base - Vérifier les compteurs visuellement :**
   - Pré-requis : Serveur Django en cours (`python web/manage.py runserver`)
   - Étapes :
     1. Ouvrir `http://127.0.0.1:8000/` dans le navigateur
     2. Pour chaque carte visible, noter les compteurs affichés (traitements et tâches)
     3. Cliquer sur une carte pour voir les détails
     4. Compter manuellement les traitements avec ☐ (non faits) et les tâches avec ☐ (non faites)
     5. Vérifier que les compteurs de la carte correspondent aux nombres réels
   - Critère de succès : Les compteurs affichés = compte manuel pour au moins 5 cartes différentes

2. **Test AJAX - Vérifier le rafraîchissement :**
   - Pré-requis : Une carte ouverte en modal
   - Étapes :
     1. Noter le compteur de traitements actuel sur une carte
     2. Ouvrir la carte (clic)
     3. Ajouter un nouveau traitement via le formulaire AJAX
     4. Fermer le modal
     5. Observer si la carte se rafraîchit automatiquement
   - Critère de succès : Le compteur de la carte s'incrémente de 1

3. **Test de régression - Compteur de scellés :**
   - Étapes :
     1. Ouvrir une carte qui a 3 scellés (visible dans les détails)
     2. Vérifier que le compteur de scellés affiche bien "3"
   - Critère de succès : Les compteurs de scellés restent corrects

4. **Test de performance :**
   - Pré-requis : Base de données avec au moins 30 activités
   - Étapes :
     1. Ouvrir les DevTools du navigateur (F12)
     2. Onglet Network
     3. Recharger la page `http://127.0.0.1:8000/`
     4. Noter le temps de chargement de la requête principale
   - Critère de succès : Temps similaire ou meilleur qu'avant le fix (baseline à établir avant modification)

**Tests automatisés :**
- Aucun test Django existant identifié pour `views.py`
- Recommandation : Ajouter des tests unitaires Django dans un futur sprint (hors scope)

**Vérification des logs :**
- Surveiller la console du serveur Django pendant les tests
- Aucune erreur SQL ou exception Django ne doit apparaître
- Vérifier qu'il n'y a pas de warnings sur les annotations

### Notes

**Points critiques (Pre-mortem) :**

1. **~~Risque : Subquery retournant NULL au lieu de 0~~** **[RÉSOLU]**
   - **Solution implémentée :** Utilisation de `Coalesce(Subquery(...), Value(0))` dans toutes les annotations
   - **Garantie :** Les compteurs retournent toujours 0 pour les activités sans traitements/tâches au lieu de NULL

2. **Risque : Performance avec de nombreuses activités**
   - **Impact :** Les subqueries génèrent potentiellement une requête supplémentaire par activité (N+1 queries possible)
   - **Observation :** Django optimise généralement les subqueries en les intégrant au SQL principal, mais à surveiller
   - **Monitoring :** Utiliser `django-debug-toolbar` ou surveiller le nombre de requêtes SQL avec `connection.queries`
   - **Baseline recommandée :** Mesurer le temps de chargement et le nombre de requêtes AVANT le fix pour comparaison
   - **Solution de secours :** Si trop lent (>2x plus lent), envisager prefetch_related avec annotations Python côté code

3. **Risque : Duplication de code entre board() et get_activity_columns()**
   - **Impact :** Maintenance - deux endroits à modifier si la logique change
   - **Mitigation actuelle :** Accepté pour ce fix (simplicité + rapidité)
   - **Amélioration future :** Créer une fonction helper `_get_pending_counts_annotations()` qui retourne les annotations Coalesce+Subquery réutilisables

**Limitations connues :**
- Cette correction ne change pas la logique métier des colonnes virtuelles (Traitements, Tâches, CTA, etc.)
- La correction suppose que les relations `scelles`, `traitements`, `taches` sont bien définies dans les modèles
- Le fix ne gère pas les cas où les modèles auraient été modifiés côté Desktop (peu probable car `managed=False`)

**Considérations futures (hors scope) :**
- Ajouter des tests automatisés Django pour `board()` et `get_activity_columns()`
- Refactoriser `views.py` (34KB) en modules séparés (views, serializers, services)
- Créer une fonction helper pour les annotations de compteurs réutilisables
- Surveiller la performance avec django-debug-toolbar après déploiement
