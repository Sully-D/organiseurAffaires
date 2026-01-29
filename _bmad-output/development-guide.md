# Organiseur d'Affaires - Guide de Développement

**Généré le:** 2026-01-27

---

## Prérequis

- **Python:** 3.8 ou supérieur
- **OS:** Linux, macOS, Windows
- **Git:** Pour cloner le dépôt
- **Environnement virtuel:** Recommandé

---

## Installation

### 1. Cloner le Dépôt

```bash
git clone <repository-url>
cd organiseurAffaires
```

### 2. Créer l'Environnement Virtuel

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les Dépendances

⚠️ **Note:** Aucun `requirements.txt` n'existe actuellement dans le projet.

**Dépendances connues (à installer manuellement):**

**Pour Desktop:**
```bash
pip install PySide6 sqlalchemy reportlab
```

**Pour Web (en plus):**
```bash
pip install django
```

**Recommandation:** Créer un `requirements.txt`:
```
PySide6>=6.0.0
SQLAlchemy>=1.4.0
reportlab>=3.6.0
Django>=4.0.0
```

Puis installer:
```bash
pip install -r requirements.txt
```

### 4. Initialiser la Base de Données

La base de données (`organiseur.db`) est créée automatiquement au premier lancement.

**Pour forcer l'initialisation (Desktop):**
```bash
python database/init_db.py
```

---

## Lancement

### Application Desktop

```bash
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows

python main.py
```

### Application Web Django

**Première fois - Créer superuser:**
```bash
python web/create_superuser.py
# OU
cd web
python manage.py createsuperuser
```

**Lancer le serveur:**
```bash
python web/manage.py runserver
```

**Accès:**
- Application: `http://127.0.0.1:8000`
- Admin Django: `http://127.0.0.1:8000/admin`
- Credentials par défaut: `admin`/`admin`

---

## Structure de Développement

### Desktop Application

**Point d'entrée:** `main.py`

**Architecture:**
```
main.py → UI Layer (ui/) → Business Logic → Data Layer (database/)
```

**Développement UI:**
- Les widgets Qt sont dans `ui/`
- Utilise PySide6 (Qt for Python)
- Styles et layouts définis en code Python

**Accès base de données:**
```python
from database.db import get_session
from database.models import Activity, Scelle

session = get_session()
activities = session.query(Activity).all()
```

### Web Application

**Point d'entrée:** `web/manage.py`

**Architecture Django MVT:**
```
URL → View (views.py) → Template (templates/) + Model (models.py)
```

**Commandes utiles:**
```bash
cd web

# Lancer serveur
python manage.py runserver

# Shell Django
python manage.py shell

# Créer superuser
python manage.py createsuperuser

# Collecter fichiers statiques (production)
python manage.py collectstatic
```

**Développement Frontend:**
- Templates: `web/kanban/templates/kanban/`
- Styles: `web/kanban/static/kanban/css/`
- JavaScript: `web/kanban/static/kanban/js/`

---

## Base de Données

### Schéma

Voir [data-models.md](./data-models.md) pour le schéma complet.

**Tables principales:**
- `kanban_columns` - Colonnes Kanban
- `activities` - Activités/Cartes
- `scelles` - Scellés
- `traitements` - Traitements
- `taches` - Tâches
- `tags` - Tags

### Migrations

⚠️ **Important:** Pas de système de migration automatisé (pas d'Alembic, Django managed=False)

**Process actuel:**
1. Modifier `database/models.py` (SQLAlchemy)
2. Créer script de migration dans `database/migrate_*.py`
3. Exécuter le script manuellement
4. Mettre à jour `web/kanban/models.py` (Django) en conséquence

**Exemple de migration:**
```python
# database/migrate_example.py
from database.db import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE scelles ADD COLUMN new_field TEXT"))
    conn.commit()
```

**Recommandation:** Migrer vers Alembic pour automatiser les migrations.

### Accès Concurrent

⚠️ **SQLite Limitation:** Ne pas utiliser Desktop et Web simultanément!

SQLite ne supporte pas les écritures concurrentes. Si besoin:
1. Utiliser PostgreSQL ou MySQL
2. Modifier `database/db.py` et `web/organiseur_web/settings.py`

---

## Tests

### Desktop

**Aucun test automatisé détecté.**

**Recommandation:** Ajouter tests avec `pytest`:
```bash
pip install pytest pytest-qt
```

Exemple test:
```python
# tests/test_models.py
from database.models import Activity, KanbanColumn
from database.db import get_session

def test_create_activity():
    session = get_session()
    col = session.query(KanbanColumn).first()
    activity = Activity(name="Test", date=date.today(), column=col)
    session.add(activity)
    session.commit()
    assert activity.id is not None
```

### Web

**Tests Django:**
```bash
cd web
python manage.py test kanban
```

**Fichier:** `web/kanban/tests.py` (1KB - tests basiques)

---

## Build et Déploiement

### Desktop - Build Exécutable Windows

**Fichier:** `organiseur.spec` (PyInstaller)

**Process:**
1. Copier le projet sur machine Windows
2. Double-cliquer `build_windows.bat`
3. Exécutable généré dans `dist/OrganiseurAffaires/`

**Ou manuellement:**
```bash
pip install pyinstaller
pyinstaller organiseur.spec
```

### Web - Déploiement Production

**Checklist:**
1. Désactiver DEBUG dans `web/organiseur_web/settings.py`
2. Définir SECRET_KEY sécurisée
3. Configurer ALLOWED_HOSTS
4. Utiliser PostgreSQL/MySQL au lieu de SQLite
5. Collecter fichiers statiques:
   ```bash
   python web/manage.py collectstatic
   ```
6. Utiliser Gunicorn ou uWSGI:
   ```bash
   pip install gunicorn
   gunicorn organiseur_web.wsgi:application
   ```
7. Reverse proxy (Nginx)

---

## Workflow de Développement

### Ajouter une Nouvelle Fonctionnalité

#### Desktop

1. Créer/modifier modèle dans `database/models.py` si nécessaire
2. Créer migration si schéma modifié
3. Développer UI dans `ui/`
4. Tester localement
5. Mettre à jour README.md

#### Web

1. Si schéma modifié, voir section Migrations ci-dessus
2. Ajouter route dans `web/kanban/urls.py`
3. Créer view dans `web/kanban/views.py`
4. Créer template dans `web/kanban/templates/kanban/`
5. Ajouter styles/JS si nécessaire
6. Tester avec `python manage.py runserver`
7. Mettre à jour README_DJANGO.md

---

## Debugging

### Desktop

**PySide6 Debug:**
```bash
export QT_DEBUG_PLUGINS=1  # Linux/macOS
set QT_DEBUG_PLUGINS=1     # Windows
python main.py
```

**SQLAlchemy Debug (logs SQL):**
```python
# database/db.py
engine = create_engine('sqlite:///organiseur.db', echo=True)
```

### Web

**Django Debug Toolbar:**
```bash
pip install django-debug-toolbar
```

Puis ajouter dans `settings.py` et `urls.py`.

**Logs Django:**
```bash
python web/manage.py runserver --verbosity 2
```

**Shell IPython:**
```bash
pip install ipython
python web/manage.py shell
```

---

## Conventions de Code

### Python
- **Style:** PEP 8
- **Formatter:** Black (recommandé)
- **Linter:** Flake8 ou Pylint

**Installation:**
```bash
pip install black flake8
black .
flake8 .
```

### Django
- **Apps:** snake_case (ex: `kanban`)
- **Models:** PascalCase (ex: `Activity`)
- **Views:** snake_case (ex: `get_activity_details`)
- **Templates:** kebab-case (ex: `activity-detail.html`)

---

## Logs

### Desktop
Pas de système de logging structuré détecté.

**Recommandation:** Ajouter logging Python:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Web

**Fichier de log:** `user_actions.log` (racine du projet)

**Configuration:** Dans `web/kanban/views.py`:
```python
import logging
logger = logging.getLogger('user_actions')
logger.info(f"User {user} performed action")
```

---

## Résolution de Problèmes Courants

### "Module not found"
```bash
# Vérifier environnement virtuel activé
which python  # Doit pointer vers venv/bin/python

# Réinstaller dépendances
pip install --force-reinstall <package>
```

### Base de données verrouillée (SQLite)
- Vérifier qu'aucune autre instance Desktop/Web ne tourne
- Supprimer le fichier `organiseur.db-journal` si présent
- En dernier recours : copier les données et recréer la DB

### Erreurs Django Admin
```bash
# Migrations Django (même si managed=False pour certaines tables)
cd web
python manage.py makemigrations
python manage.py migrate
```

---

## Ressources Utiles

### Documentation
- **PySide6:** https://doc.qt.io/qtforpython/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Django:** https://docs.djangoproject.com/

### Outils de Développement
- **Qt Designer:** Pour créer UI graphiquement
- **DB Browser for SQLite:** Visualiser/éditer organiseur.db

---

**Note:** Ce guide reflète l'état du projet au 2026-01-27. Pour questions ou contributions, consulter le README principal.
