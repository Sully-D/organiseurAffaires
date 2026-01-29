# Organiseur d'Affaires

Application de gestion de tâches style Kanban, développée en Python avec PySide6 (Qt). Permet de suivre des activités, des scellés, des traitements et des tâches avec une interface visuelle et des fonctionnalités d'export avancées.

## Fonctionnalités Principales

*   **Tableau Kanban Visuel** : Gestion des activités par colonnes (glisser-déposer non implémenté, gestion via menu).
*   **Détails Complets** : Suivi des Scellés, Traitements et Tâches pour chaque activité.
*   **Validations** : Suivi des validations CTA et Réparations.
*   **Exports** :
    *   **PDF Complet (4 pages)** : Résumé global, vue du programme, graphiques statistiques, résumé du jour.
    *   **HTML Journalier** : Résumé léger des activités et validations du jour.
*   **Recherche & Filtres** : Recherche par texte/tags et tri par date/nom.

## Installation et Lancement

### Prérequis
*   Python 3.8 ou supérieur
*   Environnement virtuel recommandé

### Installation (Linux/Mac)
```bash
# 1. Créer un environnement virtuel
python3 -m venv venv

# 2. Activer l'environnement
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

### Installation (Windows)
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Lancement
```bash
python main.py
```

## Configuration Initiale

Lors du premier lancement, la base de données `organiseur.db` sera créée automatiquement.

### Colonnes Recommandées
Les colonnes par défaut créées automatiquement sont :
1.  **À faire**
2.  **En cours**
3.  **Traitements**
4.  **Tâches**
5.  **CTA**
6.  **Réparations**
7.  **Terminé**
8.  **Important**

Vous pouvez ajouter ou modifier ces colonnes via le menu **Outils > Gérer Colonnes**.
Pour un flux de travail optimal, nous recommandons la structure suivante :
*   **À faire** : Nouvelles activités
*   **En cours** : Activités démarrées
*   **En attente** : Blocage (attente pièce, validation...)
*   **Terminé** : Activités clôturées

# Nouvelle Interface Django

Ce projet dispose maintenant d'une interface web basée sur Django, en plus de l'interface graphique existante PySide6.

## Installation

Si vous ne l'avez pas déjà fait, installez Django (automatiquement fait si vous utilisez le même venv) :

```bash
pip install django
```

## Lancement

1.  Assurez-vous d'être dans le dossier racine du projet.
2.  Activez votre environnement virtuel.
3.  Lancez le serveur de développement :

```bash
python web/manage.py runserver
```

4.  Ouvrez votre navigateur à l'adresse : [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Fonctionnalités

*   **Tableau Kanban** : Visualisation des activités par colonnes.
*   **Interface Moderne** : Design "Glassmorphism" sombre.
*   **Administration** : Gestion complète des données (Activités, Scellés, etc.) via l'interface d'administration Django.
    *   Accès : [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
    *   Compte par défaut : `admin` / `admin`

## Structure

Le projet Django se trouve dans le dossier `web/`. Il utilise la même base de données `organiseur.db` que l'application de bureau, ce qui permet de passer de l'un à l'autre sans perte de données.
Les modèles (`web/kanban/models.py`) sont définis avec `managed = False` pour respecter le schéma existant.
