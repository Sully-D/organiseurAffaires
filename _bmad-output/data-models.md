# Organiseur d'Affaires - Modèles de Données

**Généré le:** 2026-01-27  
**Base de Données:** SQLite (`organiseur.db`)  
**ORM:** SQLAlchemy (Desktop) / Django ORM (Web, managed=False)

---

## Vue d'Ensemble

La base de données `organiseur.db` est **partagée** entre l'application desktop (PySide6) et l'application web (Django). Le schéma est défini par SQLAlchemy dans `database/models.py` et réutilisé par Django avec `managed=False`.

---

## Schéma Relationnel

```
┌─────────────────┐         ┌─────────────────┐
│ KanbanColumn    │◄───┐    │      Tag        │
│                 │    │    │                 │
│ - id (PK)       │    │    │ - id (PK)       │
│ - name          │    │    │ - name          │
│ - order_index   │    │    │ - color         │
└─────────────────┘    │    └─────────────────┘
                       │            ▲
                       │            │ M:N
                       │            │
┌─────────────────────────┼────────┴──────────┐
│       Activity          │                   │
│                         │                   │
│ - id (PK)              │                   │
│ - name                 │          activity_tags
│ - date                 │
│ - description           │
│ - column_id (FK) ──────┘
└──────────┬──────────────┘
           │ 1:N
           │
           ▼
┌─────────────────────┐
│      Scelle         │──────────┐
│                     │          │ M:N
│ - id (PK)           │          │
│ - name              │     scelle_tags
│ - info              │          │
│ - cta_validated     │          ▼
│ -reparations_validated    <Tag>
│ - reparations_details
│ - important_info
│ - activity_id (FK)  │
└──────┬──────────────┘
       │ 1:N     1:N
       ├─────────┬────────┐
       ▼         ▼        │
┌─────────┐  ┌────────┐  │
│Traitement│  │ Tache  │  │
│          │  │        │  │
│ - id (PK)│  │ -id(PK)│  │
│ - description│ -description
│ - done   │  │ - done │  │
│ - done_at│  │-done_at│  │
│-scelle_id│  │-scelle_id
│   (FK)   │  │  (FK)  │  │
└──────────┘  └────────┘  │
```

---

## Tables

### 1. `kanban_columns`

Colonnes du tableau Kanban.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| **id** | INTEGER | PK, AUTO | Identifiant unique |
| **name** | STRING | UNIQUE, INDEX | Nom de la colonne (ex: "À faire", "En cours") |
| **order_index** | INTEGER | DEFAULT 0 | Ordre d'affichage |

**Relations:**
- 1:N avec `activities`

**Colonnes par défaut créées:**
1. À faire
2. En cours
3. Traitements (virtuelle pour le web)
4. Tâches (virtuelle pour le web)
5. CTA (virtuelle pour le web)
6. Réparations (virtuelle pour le web)
7. En attente
8. Terminé
9. Important
10. Archivé

---

### 2. `tags`

Tags pour catégoriser les activités et scellés.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| **id** | INTEGER | PK, AUTO | Identifiant unique |
| **name** | STRING | UNIQUE, INDEX | Nom du tag |
| **color** | STRING | DEFAULT "#CCCCCC" | Couleurdu tag (hex) |

**Relations:**
- M:N avec `activities` via `activity_tags`
- M:N avec `scelles` via `scelle_tags`

---

### 3. `activities`

Activités/Cartes Kanban principales.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| **id** | INTEGER | PK, AUTO | Identifiant unique |
| **name** | STRING | INDEX | Nom de l'activité |
| **date** | DATE | NOT NULL | Date de l'activité |
| **description** | TEXT | NULLABLE | Description détaillée |
| **column_id** | INTEGER | FK → kanban_columns.id | Colonne Kanban actuelle |

**Relations:**
- N:1 avec `kanban_columns` (column)
- 1:N avec `scelles`
- M:N avec `tags` via `activity_tags`

---

### 4. `scelles`

Scellés associés à une activité.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| **id** | INTEGER | PK, AUTO | Identifiant unique |
| **name** | STRING | INDEX | Nom du scellé |
| **info** | TEXT | NULLABLE | Informations générales |
| **cta_validated** | BOOLEAN | DEFAULT FALSE | Validation CTA effectuée |
| **reparations_validated** | BOOLEAN | DEFAULT FALSE | Validation Réparations effectuée |
| **reparations_details** | TEXT | NULLABLE | Détails des réparations |
| **important_info** | TEXT | NULLABLE | Infos importantes |
| **activity_id** | INTEGER | FK → activities.id | Activité parente |

**Relations:**
- N:1 avec `activities`  
- 1:N avec `traitements` (CASCADE DELETE)
- 1:N avec `taches` (CASCADE DELETE)
- M:N avec `tags` via `scelle_tags`

**Logique Métier:**
- Un scellé validé CTA ou Réparations fait passer l'activité dans des colonnes virtuelles (Web uniquement)
- Les validations sont exclusives des traitements/tâches en cours

---

### 5. `traitements`

Traitements à effectuer sur un scellé.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| **id** | INTEGER | PK, AUTO | Identifiant unique |
| **description** | TEXT | NOT NULL | Description du traitement |
| **done** | BOOLEAN | DEFAULT FALSE | Traitement terminé |
| **done_at** | DATE | NULLABLE | Date de complétion |
| **scelle_id** | INTEGER | FK → scelles.id | Scellé parent |

**Relations:**
- N:1 avec `scelles`

---

### 6. `taches`

Tâches à effectuer sur un scellé.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| **id** | INTEGER | PK, AUTO | Identifiant unique  
| **description** | STRING | NOT NULL | Description de la tâche |
| **done** | BOOLEAN | DEFAULT FALSE | Tâche terminée |
| **done_at** | DATE | NULLABLE | Date de complétion |
| **scelle_id** | INTEGER | FK → scelles.id | Scellé parent |

**Relations:**
- N:1 avec `scelles`

---

## Tables d'Association (M:N)

### `activity_tags`

| Colonne  | Type | Contraintes |
|------------ |------|-------------|
| **activity_id** | INTEGER | FK → activities.id |
| **tag_id** | INTEGER | FK → tags.id |

### `scelle_tags`

| Colonne | Type | Contraintes  |
|---------|------|-------------|
| **scelle_id** | INTEGER | FK → scelles.id |
| **tag_id** | INTEGER | FK → tags.id |

---

## Différences Desktop vs Web

### Desktop (SQLAlchemy)
- ORM complet avec cascades définies
- Gestion explicite des relations
- Fichier: `database/models.py`

### Web (Django)
- `managed = False` dans Meta - Django ne crée PAS les tables
- Réutilise le schéma existant de l'app desktop
- Fichier: `web/kanban/models.py`

⚠️ **Important:** Toute migration de schéma doit être effectuée via SQLAlchemy (desktop), puis Django doit être mis à jour en conséquence.

---

## Stratégie de Migration

Actuellement, pas de système de migration automatisé. Les migrations sont gérées via:
- Scripts manuels dans `database/migrate_*.py`
- Outil `database/init_db.py` pour initialisation

**Fichiers de migration existants:**
- `database/migrate_done_at.py` - Ajout du champ `done_at`
- `database/migrate_scelle.py` - Migration structure scellés
- `database/migrate_traitement.py` - Migration traitements

---

## Indexes et Performance

**Indexes définis:**
- `activities.name` (INDEX)
- `activities.column_id` (FK inherent)
- `scelles.name` (INDEX)
- `tags.name` (UNIQUE INDEX)
- `kanban_columns.name` (UNIQUE INDEX)

**Optimisations Django:**
- Utilisation de `prefetch_related()` pour réduire les requêtes N+1
- Annotations pour calculs agrégés (pending_traitements, pending_taches)
- Exists() pour vérifications booléennes performantes

---

## Règles de Cascade

### SQLAlchemy (Desktop)
```python
# Activity → Scelles
scelles = relationship("Scelle", cascade="all, delete-orphan")

# Scelle → Traitements/Taches
traitements = relationship("Traitement", cascade="all, delete-orphan")
taches = relationship("Tache", cascade="all, delete-orphan")
```

### Django (Web)
Les cascades ne sont PAS gérées by Django (managed=False), mais implémentées manuellement dans `views.py`:
```python
def delete_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    for scelle in activity.scelles.all():
        scelle.delete()  # Supprime aussi traitements/taches
    activity.tags.clear()
    activity.delete()
```

---

**Note:** Cette documentation reflète l'état actuel du schéma de base de données partagé entre les applications Desktop et Web.
