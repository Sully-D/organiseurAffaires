# Organiseur d'Affaires - Contrats API (Application Web)

**Généré le:** 2026-01-27  
**Application:** Web (Django)  
**Base URL:** `http://127.0.0.1:8000`  
**Authentification:** Django Session Auth + Superuser Required

---

## Vue d'Ensemble

L'application web Django expose **33 endpoints** REST pour gérer les activités Kanban, les scellés, les traitements et les tâches. Tous les endpoints API (préfixés `/api/`) nécessitent une authentification **superuser**.

---

## Authentification

**Type:** Django Session Authentication  
**Décorateur:** `@user_passes_test(lambda u: u.is_superuser)`

**Login:** Utiliser l'interface Admin Django ou session  
**Admin:** `http://127.0.0.1:8000/admin`  
**Credentials par défaut:** `admin`/`admin`

---

## Groupes d'Endpoints

### 1. Vues de Rendu (HTML)
### 2. Gestion Colonnes
### 3. Gestion Activités (CRUD)
### 4. Gestion Scellés (CRUD)
### 5. Gestion Traitements (CRUD)
### 6. Gestion Tâches (CRUD)
### 7. Tags
### 8. Archives
### 9. Suggestions/Autocomplete
### 10. Exports

---

## 1. Vues de Rendu (HTML)

### GET `/`
**Description:** Page principale - Tableau Kanban  
**Auth:** Non requis  
**Response:** HTML (board.html)

**Logique:**
- Affiche toutes les colonnes (sauf "Archivé")
- Applique logique colonnes virtuelles (Traitements, Tâches, CTA, Réparations)
- Annotate: pending_traitements, pending_taches, has_cta, has_reparations

---

### GET `/synthese/`
**Description:** Vue synthèse/dashboard  
**Auth:** Non requis  
**Response:** HTML (synthese.html)

**Données:**
- Total activités (hors archivées)
- Terminées
- CTA validées
- Réparations validées  
- En attente
- En cours réel (remaining)

---

### GET `/archives/`
**Description:** Page archives  
**Auth:** Non requis  
**Response:** HTML (archives.html)

**Données:**
- Activités dans colonne "Archivé"
- Tri par date décroissante

---

### GET `/activity/<activity_id>/`
**Description:** Modal détails activité  
**Auth:** Non requis  
**Response:** HTML (activity_detail.html)

**Données:**
- Activité complète
- Scellés + traitements + tâches
- Tags associés

---

### GET `/admin-export-form/`
**Description:** Formulaire génération rapport  
**Auth:** Superuser required  
**Response:** HTML (admin_export_form.html)

---

### GET `/admin-export/`
**Description:** Génération rapport période  
**Auth:** Superuser required  
**Query Params:**
- `start_date` (YYYY-MM-DD)
- `end_date` (YYYY-MM-DD)

**Response:** HTML (admin_export_report.html)

**Données:**
- Traitements validés dans la période
- Tâches validées dans la période
- Cartes terminées
- Cartes CTA
- Cartes Réparations
- Cartes urgentes/en retard

---

## 2. Gestion Colonnes

### POST `/reorder-columns/`
**Description:** Réorganiser l'ordre des colonnes  
**Auth:** Superuser required

**Request Body:**
```json
{
  "order": [3, 1, 2, 5, 4]  // IDs des colonnes dans le nouvel ordre
}
```

**Response:**
```json
{
  "status": "success"
}
```

---

## 3. Gestion Activités (CRUD)

### POST `/api/activity/create/`
**Description:** Créer nouvelle activité  
**Auth:** Superuser required

**Request Body:**
```json
{
  "column_id": 1
}
```

**Response:**
```json
{
  "status": "success",
  "activity_id": 42,
  "card_html": "<div class='activity-card'>...</div>"
}
```

**Defaults:** name="Nouvelle Activité", date=today, description=""

---

### POST `/api/activity/<activity_id>/update/`
**Description:** Modifier activité  
**Auth:** Superuser required

**Request Body:**
```json
{
  "name": "Activité mise à jour",
  "date": "2026-01-30",
  "description": "Nouvelle description"
}
```

**Response:**
```json
{
  "status": "success"
}
```

---

### POST `/api/activity/<activity_id>/delete/`
**Description:** Supprimer activité (+ cascades manuelles)  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success"
}
```

**Side effects:**
- Supprime tous les scellés associés
- Supprime traitements + tâches (via scellés)
- Clear tags M:N

---

### POST `/move-activity/`
**Description:** Déplacer activité vers une colonne  
**Auth:** Superuser required

**Request Body:**
```json
{
  "activity_id": 42,
  "column_id": 3
}
```

**Response:**
```json
{
  "status": "success"
}
```

---

### POST `/api/activity/<activity_id>/toggle-tag/`
**Description:** Ajouter/retirer tag d'une activité  
**Auth:** Superuser required

**Request Body:**
```json
{
  "tag_id": 5
}
```

**Response:**
```json
{
  "status": "success",
  "action": "added" | "removed"
}
```

---

### POST `/api/activity/<activity_id>/columns/`
**Description:** Calculer colonnes virtuelles pour une activité  
**Auth:** Non requis (mais POST?!)

**Response:**
```json
{
  "status": "success",
  "columns": [1, 3, 7],  // IDs colonnes où l'activité doit apparaître
  "card_html": "<div>...</div>"
}
```

**Logique:** Calcule colonnes physiques + virtuelles (Traitements, Tâches, CTA, etc.)

---

### POST `/api/activity/<activity_id>/archive/`
**Description:** Archiver activité  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success"
}
```

**Side effect:** Move to column "Archivé"

---

### POST `/api/activity/<activity_id>/unarchive/`
**Description:** Désarchiver activité  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success"
}
```

**Side effect:** Move to column "En attente"

---

## 4. Gestion Scellés (CRUD)

### POST `/api/activity/<activity_id>/add-scelle/`
**Description:** Ajouter scellé à une activité  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success",
  "scelle_id": 15
}
```

**Defaults:** name="Nouveau Scellé", info=""

---

### POST `/api/scelle/<scelle_id>/update/`
**Description:** Modifier scellé  
**Auth:** Superuser required

**Request Body:**
```json
{
  "name": "Scellé XYZ",
  "info": "Informations détaillées",
  "cta_validated": true,
  "reparations_validated": false
}
```

**Response:**
```json
{
  "status": "success"
}
```

---

### POST `/api/scelle/<scelle_id>/delete/`
**Description:** Supprimer scellé  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success"
}
```

**Side effects:** Cascade delete traitements + tâches

---

## 5. Gestion Traitements (CRUD)

### POST `/api/scelle/<scelle_id>/add-traitement/`
**Description:** Ajouter traitement à un scellé  
**Auth:** Superuser required

**Request Body:**
```json
{
  "description": "Vérification complète"
}
```

**Response:**
```json
{
  "status": "success",
  "traitement_id": 23
}
```

---

### POST `/api/traitement/<traitement_id>/toggle/`
**Description:** Marquer traitement comme done/undone  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success",
  "done": true
}
```

**Side effect:** Si done=true, set done_at=now()

---

### POST `/api/traitement/<traitement_id>/delete/`
**Description:** Supprimer traitement  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success"
}
```

---

## 6. Gestion Tâches (CRUD)

### POST `/api/scelle/<scelle_id>/add-tache/`
**Description:** Ajouter tâche à un scellé  
**Auth:** Superuser required

**Request Body:**
```json
{
  "description": "Nettoyer surface"
}
```

**Response:**
```json
{
  "status": "success",
  "tache_id": 18
}
```

---

### POST `/api/tache/<tache_id>/toggle/`
**Description:** Marquer tâche comme done/undone  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success",
  "done": false
}
```

---

### POST `/api/tache/<tache_id>/delete/`
**Description:** Supprimer tâche  
**Auth:** Superuser required

**Response:**
```json
{
  "status": "success"
}
```

---

## 7. Tags

### POST `/api/tags/create/`
**Description:** Créer nouveau tag  
**Auth:** Superuser required

**Request Body:**
```json
{
  "name": "Urgent",
  "color": "#ff0000"
}
```

**Response:**
```json
{
  "status": "success",
  "tag": {
    "id": 7,
    "name": "Urgent",
    "color": "#ff0000"
  }
}
```

**Note:** get_or_create logic - retourne tag existant si nom déjà pris

---

## 8. Suggestions/Autocomplete

### GET `/api/suggestions/traitements/`
**Description:** Liste descriptions de traitements pour autocomplete  
**Auth:** Non requis

**Response:**
```json
{
  "status": "success",
  "suggestions": [
    "Vérification complète",
    "Test d'étanchéité",
    "Contrôle visuel"
  ]
}
```

---

### GET `/api/suggestions/taches/`
**Description:** Liste descriptions de tâches pour autocomplete  
**Auth:** Non requis

**Response:**
```json
{
  "status": "success",
  "suggestions": [
    "Nettoyer surface",
    "Préparer outillage",
    "Rédiger rapport"
  ]
}
```

---

## Codes d'Erreur

### Standard Responses

**Success:**
```json
{
  "status": "success",
  // ... data ...
}
```

**Error:**
```json
{
  "status": "error",
  "message": "Description de l'erreur"
}
```

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (données invalides)
- `404` - Not Found (ressource inexistante)
- `403` - Forbidden (pas superuser)

---

## Logging

Toutes les actions API (superuser) sont loggées dans `user_actions.log`:

```
INFO - User admin updated activity 42 ('Activité Test').
INFO - User admin added traitement 23 ('Vérification') to scelle 15 ('Scellé XYZ').
INFO - User admin deleted activity 99 ('Old Activity').
```

---

## Notes Techniques

### Colonnes Virtuelles (Logique Complexe)

Certaines colonnes sont **virtuelles** - les activités y apparaissent sans y être physiquement déplacées:

- **Traitements** : Activités "En cours" avec traitements non terminés (et sans CTA/Rep validé)
- **Tâches** : Activités "En cours" avec tâches non terminées (et sans CTA/Rep validé)
- **CTA** : Activités "En cours" avec scellé.cta_validated=True
- **Réparations** : Activités "En cours" avec scellé.reparations_validated=True
- **En attente** : Activités "En cours" avec CTA OU Réparations validées

Cette logique est implémentée dans:
- `views.board()` - Pour rendu tableau
- `views.get_activity_columns()` - Pour calcul colonnes après modification

### Optimisations Django

- **prefetch_related()** pour éviter N+1 queries
- **annotate()** pour calculs en DB (Count, Exists)
- **select_related()** pour FK
- Pas de sérializers (Django REST Framework non utilisé)

---

## Exemple Flux AJAX

Création d'une activité depuis le frontend:

```javascript
fetch('/api/activity/create/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
  body: JSON.stringify({column_id: 1})
})
.then(res => res.json())
.then(data => {
  if(data.status === 'success') {
    // Injecter data.card_html dans le DOM
    document.querySelector(`#column-${1} .activities`).innerHTML += data.card_html;
  }
});
```

---

**Note:** Cette documentation reflète l'API au 2026-01-27. Tous les endpoints POST nécessitent un token CSRF Django.
