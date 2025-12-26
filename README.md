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

## Création d'exécutable (Windows)

L'application inclut des scripts pour générer un fichier `.exe` autonome.
1.  Copiez tout le dossier du projet sur une machine Windows.
2.  Double-cliquez sur le fichier `build_windows.bat`.
3.  L'exécutable sera généré dans le dossier `dist/OrganiseurAffaires`.

## Structure du Projet
*   `main.py` : Point d'entrée.
*   `ui/` : Interface utilisateur (Fenêtres, Dialogues, Widgets).
*   `database/` : Modèles de données (SQLAlchemy) et gestion DB.
*   `export.py` : Logique de génération des rapports PDF et HTML.
