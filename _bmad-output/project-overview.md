# Organiseur d'Affaires - Vue d'Ensemble du Projet

**Généré le:** 2026-01-27  
**Type de Projet:** Multi-part (Desktop + Web)  
**Langage Principal:** Python  
**Architecture:** Desktop Application + Web Application avec base de données partagée

---

## Résumé Exécutif

**Organiseur d'Affaires** est une application de gestion de tâches de type Kanban développée en Python. Le projet propose **deux interfaces distinctes** pour accéder aux mêmes données :

1. **Application Desktop** - Interface graphique PySide6 (Qt) pour utilisation locale
2. **Application Web** - Interface Django pour accès multi-utilisateurs via navigateur

Les deux applications partagent la même base de données SQLite (`organiseur.db`), permettant une utilisation transparente selon les besoins.

---

## Structure du Projet

### Type de Dépôt
**Multi-part** : Deux applications distinctes dans un seul dépôt

### Parties du Projet

#### Part 1: Application Desktop (racine/)
- **Type:** Desktop Application
- **Technologies:** Python 3.8+, PySide6, SQLAlchemy
- **Point d'entrée:** `main.py`
- **Répertoires critiques:**
  - `ui/` - Interface utilisateur Qt
  - `database/` - Modèles de données et migrations  
  - `export.py` - Génération de rapports PDF/HTML

#### Part 2: Application Web (web/)
- **Type:** Web Application (Backend + Frontend)
- **Technologies:** Django 4.x, SQLite
- **Point d'entrée:** `web/manage.py`
- **Répertoires critiques:**
  - `web/kanban/` - Application Django principale
  - `web/organiseur_web/` - Configuration Django

---

## Stack Technologique

### Desktop Application

| Catégorie | Technologie | Version | Justification |
|-----------|------------|---------|---------------|
| Framework UI | PySide6 | Latest | Interface graphique Qt moderne et performante |
| ORM | SQLAlchemy | Latest | Gestion robuste de la base de données |
| Export PDF | ReportLab | Latest | Génération de rapports PDF |
| Language | Python | 3.8+ | Compatible multi-plateforme |

### Web Application

| Catégorie | Technologie | Version | Justification |
|-----------|------------|---------|---------------|
| Framework Web | Django | 4.x | Framework web Python complet avec admin intégré |
| Base de Données | SQLite | 3.x | Base partagée avec l'app desktop |
| Frontend | Vanilla JS + CSS | - | Interface moderne "glassmorphism" |
| Auth | Django Auth | Intégré | Authentification utilisateur intégrée |

### Base de Données Partagée

| Catégorie | Technologie | Version | Justification |
|-----------|------------|---------|---------------|
| SGBD | SQLite | 3.x | Simple, portable, sans serveur - parfait pour usage local/petit équipe |
| Fichier | organiseur.db | - | Partagé entre Desktop et Web |

---

## Modèle de Données

Le schéma de base de données comprend **5 entités principales** :

1. **KanbanColumn** - Colonnes du tableau Kanban (À faire, En cours, Terminé, etc.)
2. **Activity** - Activités/Cartes Kanban 
3. **Scelle** - Scellés associés à une activité
4. **Traitement** - Traitements à effectuer sur un scellé
5. **Tache** - Tâches à effectuer sur un scellé
6. **Tag** - Tags pour catégoriser activités et scellés

---

## Architecture Pattern

### Desktop: **Layered Architecture**
- **UI Layer** (`ui/`) - Widgets et fenêtres Qt
- **Business Logic** (`export.py`, scripts) - Logique métier et exports  
- **Data Layer** (`database/`) - Modèles SQLAlchemy et accès DB

### Web: **Django MVT (Model-View-Template)**
- **Models** (`web/kanban/models.py`) - Modèles Django (managed=False pour compatibilité)
- **Views** (`web/kanban/views.py`) - Logique métier et APIs REST
- **Templates** (`web/kanban/templates/`) - Templates HTML

---

## Points d'Intégration

Les deux applications sont **indépendantes** mais partagent:
- **Base de données** : `organiseur.db` (SQLite)
- **Schéma** : Défini par SQLAlchemy (desktop), réutilisé par Django (managed=False)

⚠️ **Important:** Les deux applications ne doivent pas être utilisées **simultanément** sur la même base de données pour éviter les conflits de verrouillage SQLite.

---

## Documentation Générée

- [Architecture - Desktop](./architecture-desktop.md)
- [Architecture - Web](./architecture-web.md)
- [Modèles de Données](./data-models.md)  
- [API Contracts - Web](./api-contracts-web.md)
- [Arbre des Sources](./source-tree-analysis.md)
- [Guide de Développement](./development-guide.md)

---

## Documentation Existante

- [README.md](../README.md) - Documentation application desktop
- [README_DJANGO.md](../README_DJANGO.md) - Documentation application web Django

---

## Démarrage Rapide

### Application Desktop
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Application Web
```bash
source venv/bin/activate  
python web/manage.py runserver
# Accès: http://127.0.0.1:8000
# Admin: admin/admin
```

---

**Note:** Cette documentation a été générée automatiquement par le workflow BMad `document-project`.
