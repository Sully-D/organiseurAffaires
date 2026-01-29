# Organiseur d'Affaires - Analyse de l'Arborescence Source

**Généré le:** 2026-01-27  
**Type:** Multi-part (Desktop + Web)

---

## Structure Globale

```
organiseurAffaires/
├── 📁 ROOT (Desktop Application)
│   ├── main.py                    # 🔹 Point d'entrée application desktop
│   ├── export.py                  # Export PDF/HTML (16KB - logique complexe)
│   ├── fix_script.py              # Scripts de correction DB (27KB)
│   ├── fix_template.py
│   ├── verify_cols.py
│   ├── verify_fix.py
│   ├── organiseur.spec            # PyInstaller spec pour build Windows
│   ├── organiseur.db              # 🗄️  Base de données SQLite PARTAGÉE
│   ├── user_actions.log           # Logs actions utilisateur
│   │
│   ├── 📁 database/               # Couche de données (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── db.py                  # Configuration base de données
│   │   ├── models.py              # 🔑 Modèles SQLAlchemy (définition schéma)
│   │   ├── init_db.py             # Initialisation DB
│   │   ├── migrate_*.py           # Scripts de migration manuelle
│   │   └── __pycache__/
│   │
│   └── 📁 ui/                     # _(Non scanné en détail - PySide6 UI)_
│       └── (Widgets, Dialogs, Windows Qt)
│
├── 📁 web/                        # Application Web Django
│   ├── manage.py                  # 🔹 Point d'entrée Django
│   ├── create_superuser.py        # Utilitaire création admin
│   │
│   ├── 📁 organiseur_web/         # Configuration projet Django
│   │   ├── __init__.py
│   │   ├── settings.py            # Configuration Django
│   │   ├── urls.py                # Routing principal
│   │   ├── wsgi.py                # WSGI pour déploiement
│   │   └── asgi.py                # ASGI (async)
│   │
│   └── 📁 kanban/                 # Application Django principale
│       ├── __init__.py
│       ├── apps.py                # Configuration app
│       ├── admin.py               # Interface admin Django
│       ├── models.py              # 🔑 Modèles Django (managed=False)
│       ├── models_generated.py    # Modèles générés (backup?)
│       ├── views.py               # 🔹 Logique métier + API REST (34KB)
│       ├── views_snippet.py
│       ├── urls.py                # Routing Kanban (33 endpoints!)
│       ├── tests.py
│       ├── fix_syntax.py
│       │
│       ├── 📁 migrations/         # Migrations Django (vides car managed=False)
│       │   └── __init__.py
│       │
│       ├── 📁 static/             # Fichiers statiques
│       │   └── kanban/
│       │       ├── css/           # Styles glassmorphism
│       │       └── js/            # JavaScript frontend
│       │
│       └── 📁 templates/          # Templates Django
│           └── kanban/
│               ├── base.html      # Template de base
│               ├── board.html     # Tableau Kanban
│               ├── synthese.html  # Vue synthèse
│               ├── archives.html
│               ├── activity_detail.html
│               ├── card_snippet.html
│               ├── admin_export_form.html
│               └── admin_export_report.html
│
├── 📁 _bmad/                      # Infrastructure BMad (documentation/workflows)
├── 📁 _bmad-output/               # Sortie documentation générée
├── 📁 .agent/                     # Configuration agent
├── 📁 .git/                       # Git repository
├── 📁 venv/                       # Environnement virtuel Python
├── .gitignore
├── README.md                      # Doc application desktop
└── README_DJANGO.md               # Doc application web Django
```

---

## Répertoires Critiques

### Desktop Application (Racine)

#### `database/` - Couche de Données
**But:** Définition du schéma de base de données partagé via SQLAlchemy

**Fichiers clés:**
- `models.py` (3.2KB) - **SOURCE DE VÉRITÉ** pour le schéma DB
- `db.py` - Configuration SQLAlchemy et session
- `init_db.py` - Création initiale de la DB et colonnes par défaut
- `migrate_*.py` - Scripts de migration manuelle (pas d'Alembic)

**Pattern:** Layered Data Access avec ORM

#### `ui/` - Interface Graphique
**But:** Widgets et fenêtres PySide6/Qt

_(Non scanné en détail dans ce rapport)_

**Contenu attendu:**
- Widgets Kanban
- Dialogues (ajout activité, scellé, etc.)
- Fenêtre principale
- Exports PDF/HTML UI

---

### Web Application (`web/`)

#### `organiseur_web/` - Configuration Django
**But:** Configuration du projet Django

**Fichiers clés:**
- `settings.py` - Configuration complète Django (DB, auth, apps, middleware)
- `urls.py` - Routing racine (inclut `kanban.urls`)
- `wsgi.py` / `asgi.py` - Points d'entrée serveur

#### `kanban/` - Application Kanban
**But:** Logique métier complète de l'application Kanban

**Fichiers clés:**
- `models.py` (3.8KB) - Modèles Django avec `managed = False` ⚠️
- `views.py` (34KB!) - **GROS FICHIER** avec toute la logique:
  - Vues de rendu (board, synthese, archives, exports)
  - 33 endpoints API REST (CRUD complet)
  - Logique Kanban complexe (colonnes virtuelles)
  - Gestion permissions (superuser required)
- `urls.py` (2.5KB) - Routing détaillé (33 routes)
- `admin.py` - Configuration Django Admin

#### `kanban/templates/` - Templates Django
**But:** Rendu HTML de l'interface Kanban

**Fichiers clés:**
- `base.html` - Layout de base (navbar, styles)
- `board.html` - Tableau Kanban principal
- `synthese.html` - Vue synthèse/dashboard
- `activity_detail.html` - Modal détails activité
- `card_snippet.html` - Template carte Kanban (réutilisable AJAX)
- `admin_export_*.html` - Interface génération rapports

#### `kanban/static/` - Assets Frontend
**But:** CSS et JavaScript pour l'interface moderne

**Structure:**
- `kanban/css/` - Styles glassmorphism
- `kanban/js/` - Interactions frontend (AJAX, drag & drop logique)

---

## Points d'Entrée

### Desktop Application
```python
# main.py
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # ... Initialisation UI Qt ...
```

### Web Application
```python
# web/manage.py
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organiseur_web.settings')
    execute_from_command_line(sys.argv)
```

Commande typique: `python web/manage.py runserver`

---

## Base de Données Partagée

### `organiseur.db`
**Localisation:** Racine du projet  
**Type:** SQLite 3  
**Taille:** ~208 KB (données utilisateur)

**Gestion du schéma:**
1. **Desktop (SQLAlchemy)** - Propriétaire du schéma
   - Crée et modifie la structure
   - Fichier source: `database/models.py`
   
2. **Web (Django)** - Consommateur du schéma
   - Lit la structure existante
   - `managed = False` → Django ne touche PAS au schéma
   - Fichier: `web/kanban/models.py`

⚠️ **Attention:** Migrations uniquement via desktop (SQLAlchemy)

---

## Fichiers de Configuration

### Desktop
- `organiseur.spec` - Configuration PyInstaller pour build Windows .exe

### Web
- `web/organiseur_web/settings.py` - Configuration Django complète

**Aucun fichier de dépendances Python** détecté! (requirements.txt manquant)

---

## Patterns Architecturaux Détectés

### Desktop
**Pattern:** Layered Architecture (3-tier)
- **UI Layer** - `ui/` (PySide6)
- **Business Logic** - `export.py`, scripts de traitement
- **Data Layer** - `database/` (SQLAlchemy ORM)

### Web
**Pattern:** Django MVT (Model-View-Template)
- **Model** - `kanban/models.py`
- **View** - `kanban/views.py` (logique + API)
- **Template** - `kanban/templates/`

**API REST** - Architecture RESTful partielle (endpoints CRUD mais pas totalement REST)

---

## Intégration Multi-Part

### Communication
**Type:** Base de données partagée (SQLite)

**Flux de données:**
```
Desktop App (PySide6)
      │
      ├─────► organiseur.db ◄─────┤
      │                            │
Web App (Django)                   │
                                   │
   (Pas de communication directe entre les apps)
```

**⚠️ Limitations:**
- SQLite ne supporte pas les accès concurrents en écriture
- Les deux apps ne doivent PAS fonctionner simultanément
- Pas de synchronisation temps réel

---

## Fichiers Importants Non-Standard

### Scripts de Maintenance
- `fix_script.py` (27 KB!) - Corrections/migrations de données
- `fix_template.py` - Corrections templates
- `verify_cols.py` - Vérification cohérence colonnes
- `verify_fix.py` - Vérification post-migration

### Logs
- `user_actions.log` (5KB) - Historique actions utilisateur Django

---

## Observations

### Points Positifs
✅ Séparation claire Desktop / Web  
✅ Base de données partagée bien documentée  
✅ Code web volumineux mais structuré (`views.py` bien commenté)

### Points d'Attention
⚠️ Pas de `requirements.txt` détecté  
⚠️ Migrations manuelles (risque d'erreur)  
⚠️ Fichier `views.py` très volumineux (34KB - pourrait être refactoré)  
⚠️ Utilisation simultanée Desktop+Web non supportée

### Recommandations
1. Créer un `requirements.txt` pour les dépendances
2. Migrer vers Alembic pour migrations SQLAlchemy automatisées
3. Refactorer `views.py` en modules séparés (views, serializers, services)
4. Ajouter un système de locking si usage simultané souhaité
5. Documenter davantage le processus de migration DB

---

**Note:** Cette analyse reflète la structure au 2026-01-27. Les chemins sont relatifs à la racine du projet.
