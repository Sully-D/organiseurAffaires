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
