# Organiseur d'Affaires - Index de Documentation

**Généré le:** 2026-01-27  
**Niveau de scan:** Deep Scan  
**Type de projet:** Multi-part (Desktop + Web)

---

## 📋 Vue d'Ensemble du Projet

**Organiseur d'Affaires** est une application de gestion de tâches Kanban avec deux interfaces:

- **Application Desktop** (PySide6/Qt) - Interface graphique locale
- **Application Web** (Django) - Interface web multi-utilisateurs

Les deux applications partagent la même base de données SQLite pour un accès transparent aux données.

---

## 🗂️ Structure du Projet

### Type
**Multi-part** avec 2 applications distinctes

### Parties

#### 📱 Desktop Application (racine/)
- **Type:** Desktop
- **Technologies:** Python, PySide6, SQLAlchemy  
- **Point d'entrée:** `main.py`
- **Répertoires:** `ui/`, `database/`, `export.py`

#### 🌐 Web Application (web/)
- **Type:** Web (Backend + Frontend)
- **Technologies:** Django, SQLite
- **Point d'entrée:** `web/manage.py`
- **Répertoires:** `web/kanban/`, `web/organiseur_web/`

---

## 🚀 Démarrage Rapide

### Desktop
```bash
python3 -m venv venv
source venv/bin/activate
pip install PySide6 sqlalchemy reportlab
python main.py
```

### Web
```bash
source venv/bin/activate
pip install django
python web/manage.py runserver
# Accès: http://127.0.0.1:8000
# Admin: admin/admin
```

---

## 📚 Documentation Générée

### Vue d'Ensemble et Architecture

- **[📄 Vue d'Ensemble du Projet](./project-overview.md)**  
  Résumé exécutif, type de dépôt, stack technologique, architecture patterns

- **[🗂️ Arbre des Sources](./source-tree-analysis.md)**  
  Structure détaillée des répertoires, points d'entrée, patterns architecturaux, intégration multi-part

### Données et API

- **[🗄️ Modèles de Données](./data-models.md)**  
  Schéma complet de la base de données (6 tables), relations, indexes, migrations, différences Desktop vs Web

- **[🔌 Contrats API - Web](./api-contracts-web.md)**  
  Documentation complète des 33 endpoints REST Django, authentification, requêtes/réponses, logging

### Développement

- **[👨 💻 Guide de Développement](./development-guide.md)**  
  Installation, configuration, workflows, tests, build, déploiement, debugging, troubleshooting

---

## 📄 Documentation Existante

### Documentation Utilisateur
- **[README.md](../README.md)**  
  Documentation application desktop - Fonctionnalités, installation, configuration initiale

- **[README_DJANGO.md](../README_DJANGO.md)**  
  Documentation application web Django - Installation, lancement, fonctionnalités, structure

---

## 🛠️ Technologies Utilisées

### Desktop

| Catégorie | Technologie | Justification |
|-----------|-------------|---------------|
| UI Framework | PySide6 | Interface Qt moderne |
| ORM | SQLAlchemy | Gestion robuste DB |
| Export | ReportLab | Génération PDF |

### Web

| Catégorie | Technologie | Justification |
|-----------|-------------|---------------|
| Framework | Django 4.x | Framework complet |
| Base de Données | SQLite | Partagée avec Desktop |
| Frontend | Vanilla JS/CSS | Interface glassmorphism |

---

## 🗂️ Base de Données

### Tables Principales

1. **kanban_columns** - Colonnes du tableau Kanban
2. **activities** - Activités/Cartes Kanban
3. **scelles** - Scellés associés aux activités
4. **traitements** - Traitements à effectuer
5. **taches** - Tâches à effectuer
6. **tags** - Tags pour catégorisation

**Fichier:** `organiseur.db` (SQLite 3, ~208 KB)

**Emplacement:** Racine du projet

⚠️ **Important:** Base partagée - ne pas utiliser Desktop et Web simultanément!

---

## 🔗 Intégration Multi-Part

### Type d'Intégration
**Base de données partagée** (SQLite)

### Schéma de Propriété
- **Desktop (SQLAlchemy)** : Propriétaire du schéma, gère les migrations
- **Web (Django)** : `managed=False` - Consomme le schéma existant

### Flux de Données
```
┌──────────────────┐
│  Desktop App     │───┐
│  (PySide6)       │   │
└──────────────────┘   │
                       ▼
                ┌──────────────┐
                │organiseur.db │
                │  (SQLite)    │
                └──────────────┘
                       ▲
┌──────────────────┐   │
│   Web App        │───┘
│   (Django)       │
└──────────────────┘
```

---

## 📊 Statistiques du Projet

### Lignes de Code Principales

- `web/kanban/views.py` - **34 KB** (806 lignes) - Logique métier + 33 APIs
- `database/models.py` - **3.2 KB** (86 lignes) - Schéma SQLAlchemy
- `web/kanban/models.py` - **3.8 KB** - Modèles Django
- `export.py` - **16 KB** (424 lignes) - Génération PDF/HTML
- `fix_script.py` - **27 KB** - Scripts maintenance/migration

### Endpoints API Web
**33 endpoints REST** dans l'application Django

### Modèles de Données
**6 tables principales** + 2 tables d'association (M:N)

---

## ⚠️ Points d'Attention

### Limitations Actuelles

1. **Pas de `requirements.txt`** - Dépendances non documentées formellement
2. **Migrations manuelles** - Pas d'Alembic, scripts manuels dans `database/migrate_*.py`
3. **Accès concurrent interdit** - SQLite ne supporte pas écritures simultanées Desktop+Web
4. **`views.py` volumineux** - 34KB, pourrait être refactoré en modules

### Recommandations

✅ Créer `requirements.txt` avec toutes les dépendances  
✅ Migrer vers Alembic pour migrations automatisées  
✅ Refactorer `views.py` en modules (views, serializers, services)  
✅ Ajouter tests automatisés (pytest pour Desktop, Django tests pour Web)  
✅ Documenter le process de migration de schéma  

---

## 🎯 Cas d'Usage

### Application Desktop
- Utilisation **locale** par un seul utilisateur
- Exports PDF avancés (4 pages statistiques)
- Interface graphique riche Qt
- Idéal pour: Travail individuel, offline, exports formels

### Application Web
- Utilisation **multi-utilisateurs** via navigateur
- Interface moderne glassmorphism
- Admin Django intégré
- Idéal pour: Équipe, accès distant, collaboration

---

## 📞 Support et Contribution

### Structure de Développement

**Desktop:**
```
main.py → UI (ui/) → Business Logic → Data (database/)
```

**Web:**
```
URLs → Views (views.py) → Templates + Models (models.py)
```

### Commandes Essentielles

**Desktop:**
```bash
python main.py                   # Lancer l'app
python database/init_db.py       # Initialiser DB
```

**Web:**
```bash
python web/manage.py runserver   # Lancer serveur
python web/manage.py shell       # Shell Django
python web/manage.py test        # Lancer tests
```

---

## 📝 Notes

### Méthode de Scan
**Deep Scan** - Lecture sélective des fichiers dans les répertoires critiques selon le type de projet détecté.

### Fichiers Analysés
- Tous les modèles de données (Desktop + Web)
- Tous les endpoints API (Web)
- Structure complète des répertoires
- Documentation existante (README files)
- Scripts de migration et maintenance

### Fichiers Non Analysés
- `ui/` (interface PySide6) - Scan limité
- `venv/` - Exclu
- `_bmad/` - Infrastructure de documentation

---

## 🔄 Mise à Jour de cette Documentation

Cette documentation a été générée automatiquement par le workflow BMad **document-project** en mode **deep scan**.

Pour régénérer:
```bash
# Charger l'agent bmad-master
@bmad-master → document-project
```

---

**Dernière mise à jour:** 2026-01-27  
**Version du workflow:** 1.2.0  
**Mode de scan:** Deep  
**Durée d'analyse:** ~5-10 minutes
