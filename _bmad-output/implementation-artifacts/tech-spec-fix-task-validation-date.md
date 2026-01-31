---
title: 'Corriger la date de validation des tâches dans le rapport journalier'
slug: 'fix-task-validation-date'
created: '2026-01-31T07:54:28+01:00'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4, 'adversarial-review-v1']
tech_stack: ['Django 4.x', 'Python 3.x', 'django.utils.timezone', 'Legacy DB (managed=False)']
files_to_modify: ['web/kanban/views.py']
files_to_create: ['web/kanban/management/commands/fix_task_dates.py', 'web/kanban/management/__init__.py', 'web/kanban/management/commands/__init__.py']
code_patterns: ['@require_POST decorator', 'user_passes_test(lambda u: u.is_superuser)', 'timezone.now().date() for timestamp', 'Django Command BaseCommand pattern']
test_patterns: ['Django TestCase', 'Manual testing via admin interface']
---

# Tech-Spec: Corriger la date de validation des tâches dans le rapport journalier

**Created:** 2026-01-31T07:54:28+01:00

## Overview

### Problem Statement

Lorsque l'utilisateur génère un rapport journalier via `/admin/kanban/activity/` → "EXPORTER RAPPORT HTML", la section "Tâches Validées" affiche toujours "Aucune tâche validée ce jour." même lorsque des tâches ont été validées pendant la période sélectionnée.

**Cause racine identifiée:** La vue `toggle_tache` (ligne 590 de `views.py`) ne met pas à jour le champ `done_at` lorsqu'une tâche est marquée comme complétée, contrairement à `toggle_traitement` qui le fait correctement. Le rapport filtre les tâches avec `done_at__range=(start_date, end_date)`, mais `done_at` reste toujours `None`.

### Solution

Corriger la vue `toggle_tache` pour qu'elle mette à jour le champ `done_at` de manière identique à `toggle_traitement`:
- Quand `done=True`: définir `done_at=timezone.now().date()`
- Quand `done=False`: réinitialiser `done_at=None`

De plus, corriger rétroactivement les tâches déjà validées qui ont `done=True` mais `done_at=None`.

### Scope

**In Scope:**
- Modifier la vue `toggle_tache` pour mettre à jour `done_at` lors du basculement
- Créer un script ou commande Django pour corriger les tâches existantes avec `done=True` et `done_at=None`
- Vérifier que le rapport journalier affiche correctement les tâches validées après le correctif

**Out of Scope:**
- Modifications du modèle de base de données (le champ `done_at` existe déjà)
- Modifications de l'interface utilisateur
- Modifications du template du rapport (il fonctionne correctement)

## Context for Development

### Codebase Patterns

**Pattern de toggle existant (Traitement):**
```python
# web/kanban/views.py, lignes 540-554
@require_POST
@user_passes_test(lambda u: u.is_superuser)
def toggle_traitement(request, traitement_id):
    try:
        from .models import Traitement
        t = Traitement.objects.get(id=traitement_id)
        t.done = not t.done
        if t.done:
            t.done_at = timezone.now().date()  # ← IMPORTANT
        else:
            t.done_at = None
        t.save()
        logger.info(...)
        return JsonResponse({'status': 'success', 'done': t.done})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
```

**Pattern actuel (Tâche) - À CORRIGER:**
```python
# web/kanban/views.py, lignes 588-599
@require_POST
@user_passes_test(lambda u: u.is_superuser)
def toggle_tache(request, tache_id):
    try:
        from .models import Tache
        t = Tache.objects.get(id=tache_id)
        t.done = not t.done
        # ← MANQUE: mise à jour de done_at
        t.save()
        logger.info(...)
        return JsonResponse({'status': 'success', 'done': t.done})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
```

**Utilisation de `done_at` dans le code:**
- `admin_export_report` (ligne 819): filtre avec `done_at__range`
- `activity_detail.html` (ligne 122): affiche la date de complétion si disponible
- `admin.py` (lignes 42, 47): affiche dans l'interface d'administration
- `views_snippet.py` (ligne 14): filtre par date exacte

### Files to Reference

| File | Purpose |
| ---- | ------- |
| `web/kanban/views.py` (MODIFY) | Contient `toggle_tache` (ligne 588-599, à corriger) et `toggle_traitement` (ligne 540-554, référence) |
| `web/kanban/models.py` (READ) | Définit le modèle `Tache` avec le champ `done_at` (ligne 105-118) |
| `web/kanban/templates/kanban/admin_export.html` (READ) | Template du rapport qui utilise la variable `taches` (ligne 106-128) |
| `web/kanban/management/commands/fix_task_dates.py` (CREATE) | Commande Django pour correction rétroactive des tâches existantes |
| `web/kanban/tests.py` (READ) | Fichier de tests existant (actuellement stub) |

### Technical Decisions

1. **Utiliser le même pattern que `toggle_traitement`** pour garantir la cohérence du code
2. **Import de `timezone`** déjà disponible en haut du fichier `views.py`
3. **Correction rétroactive** via une commande de gestion Django pour permettre une exécution contrôlée
4. **Logging** identique au pattern existant pour le traçage

## Implementation Plan

### Tasks

**Ordre d'exécution:** Les tâches sont ordonnées logiquement (dépendances d'abord).

- [ ] **Task 1: Corriger la vue `toggle_tache` pour mettre à jour `done_at`**
  - **File:** `web/kanban/views.py` (fonction `toggle_tache`)
  - **Action:** Modifier la fonction `toggle_tache` pour ajouter la logique de mise à jour du champ `done_at`
  - **Code modifié:**
    ```python
    @require_POST
    @user_passes_test(lambda u: u.is_superuser)
    def toggle_tache(request, tache_id):
        try:
            from .models import Tache
            t = Tache.objects.get(id=tache_id)
            t.done = not t.done
            # AJOUT: Mise à jour de done_at selon l'état
            if t.done:
                t.done_at = timezone.now().date()
            else:
                t.done_at = None
            t.save()
            logger.info(f"User {request.user.username} toggled tache {tache_id} ('{t.description[:50]}') on scelle '{t.scelle.name if t.scelle else '?'}' (done={t.done}).")
            return JsonResponse({'status': 'success', 'done': t.done})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    ```
  - **Changements spécifiques:**
    - Ajouter 4 lignes après `t.done = not t.done`
    - Message de log complet et précis (pas d'ellipses)
    - S'assurer que l'import `timezone` est présent en haut du fichier: `from django.utils import timezone`
  - **Pattern de référence:** `toggle_traitement` (même fichier)

- [ ] **Task 2: Créer la structure pour la commande de gestion Django**
  - **Directories \u0026 Files:**
    - Créer le répertoire: `web/kanban/management/`
    - Créer le répertoire: `web/kanban/management/commands/`
    - Créer le fichier: `web/kanban/management/__init__.py` (vide)
    - Créer le fichier: `web/kanban/management/commands/__init__.py` (vide)
  - **Action:** Créer la structure complète de répertoires nécessaire pour les commandes Django
  - **Commandes:**
    ```bash
    mkdir -p web/kanban/management/commands
    touch web/kanban/management/__init__.py
    touch web/kanban/management/commands/__init__.py
    ```
  - **Notes:** Ces fichiers doivent être vides pour que Django reconnaisse les répertoires comme des packages Python

- [ ] **Task 3: Créer la commande de correction rétroactive `fix_task_dates`**
  - **File:** `web/kanban/management/commands/fix_task_dates.py` (nouveau fichier)
  - **Action:** Créer une commande Django pour corriger les tâches existantes avec gestion de transaction
  - **Code complet:**
    ```python
    from django.core.management.base import BaseCommand
    from django.db import transaction
    from django.utils import timezone
    from kanban.models import Tache
    
    class Command(BaseCommand):
        help = 'Corrige les tâches validées (done=True) qui n\'ont pas de date de validation (done_at=NULL)'
        
        def add_arguments(self, parser):
            parser.add_argument(
                '--dry-run',
                action='store_true',
                help='Affiche les tâches qui seraient corrigées sans les modifier',
            )
        
        def handle(self, *args, **options):
            dry_run = options['dry_run']
            
            # Trouver les tâches à corriger
            tasks_to_fix = Tache.objects.filter(done=True, done_at__isnull=True)
            count = tasks_to_fix.count()
            
            if count == 0:
                self.stdout.write(self.style.SUCCESS('Aucune tâche à corriger.'))
                return
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(f'[DRY RUN] {count} tâche(s) seraient corrigée(s):')
                )
                for task in tasks_to_fix[:10]:  # Afficher max 10 exemples
                    self.stdout.write(f'  - Tâche #{task.id}: {task.description[:50]}')
                if count > 10:
                    self.stdout.write(f'  ... et {count - 10} autre(s)')
            else:
                # Utiliser une transaction atomique pour garantir la cohérence
                try:
                    with transaction.atomic():
                        correction_date = timezone.now().date()
                        updated = tasks_to_fix.update(done_at=correction_date)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ {updated} tâche(s) corrigée(s) avec la date {correction_date}'
                            )
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Erreur lors de la correction: {str(e)}')
                    )
                    raise
    ```
  - **Notes importantes:**
    - Utilise `@transaction.atomic` via context manager pour rollback automatique en cas d'erreur
    - L'option `--dry-run` permet de prévisualiser sans modifier
    - Affiche des exemples limités à 10 en mode dry-run pour éviter de surcharger la console
    - Message d'aide clair pour `python manage.py help fix_task_dates`

- [ ] **Task 4: Tester manuellement le correctif `toggle_tache`**
  - **Action:** Validation manuelle via l'interface admin
  - **Détails:** Voir "Testing Strategy" pour les étapes détaillées
  - **Vérification:** Confirmer que `done_at` est bien défini/réinitialisé lors du basculement

- [ ] **Task 5: Exécuter la commande de correction rétroactive**
  - **Command:** `python web/manage.py fix_task_dates`
  - **Action:** Corriger toutes les tâches historiques avec `done=True` mais `done_at=None`
  - **Vérification:** Vérifier le nombre de tâches corrigées affiché par la commande

- [ ] **Task 6: Valider le rapport journalier**
  - **Action:** Tester l'export du rapport HTML avec des tâches validées
  - **Détails:** Voir "Testing Strategy" → section "Validation du rapport journalier"
  - **Vérification:** La section "Tâches Validées" affiche maintenant les tâches validées pendant la période sélectionnée

### Acceptance Criteria

**Format:** Given/When/Then pour assurer la testabilité.

- [ ] **AC1: Validation d'une tâche définit la date de complétion**
  - **Given:** Une tâche non validée (`done=False`, `done_at=NULL`)
  - **When:** L'utilisateur clique sur la checkbox pour valider la tâche
  - **Then:** 
    - Le champ `done` passe à `True`
    - Le champ `done_at` est défini à la date actuelle
    - L'interface se met à jour visuellement

- [ ] **AC2: Dévalidation d'une tâche réinitialise la date**
  - **Given:** Une tâche validée (`done=True`, `done_at='2026-01-31'`)
  - **When:** L'utilisateur clique sur la checkbox pour dévalider la tâche
  - **Then:** 
    - Le champ `done` passe à `False`
    - Le champ `done_at` est réinitialisé à `NULL`
    - L'interface se met à jour visuellement

- [ ] **AC3: Le rapport journalier affiche les tâches validées pour la période sélectionnée**
  - **Given:** 
    - 3 tâches validées le 2026-01-31 (avec `done_at='2026-01-31'`)
    - 2 tâches validées le 2026-01-30
  - **When:** L'utilisateur exporte le rapport pour la période du 2026-01-31 au 2026-01-31
  - **Then:** 
    - La section "Tâches Validées" affiche exactement les 3 tâches du 31/01
    - Chaque tâche affiche: nom du scellé, activité, et description
    - Le message "Aucune tâche validée ce jour." n'apparaît PAS

- [ ] **AC4: La commande de correction traite uniquement les tâches concernées**
  - **Given:** 
    - 5 tâches avec `done=True` et `done_at=NULL` (à corriger)
    - 3 tâches avec `done=True` et `done_at` défini (déjà OK)
    - 2 tâches avec `done=False` (non validées)
  - **When:** L'utilisateur exécute `python web/manage.py fix_task_dates`
  - **Then:** 
    - Exactement 5 tâches sont mises à jour
    - La commande affiche "5 tâche(s) corrigée(s)"
    - Les 3 tâches déjà OK ne sont pas modifiées
    - Les 2 tâches non validées ne sont pas modifiées

- [ ] **AC5: La fonctionnalité des traitements n'est pas affectée (non-régression)**
  - **Given:** Le système existant avec des traitements validés
  - **When:** L'utilisateur valide/dévalide un traitement
  - **Then:** 
    - Le comportement de `toggle_traitement` reste identique
    - Le champ `done_at` du traitement est toujours mis à jour correctement
    - Le rapport affiche toujours les traitements validés

- [ ] **AC6: Gestion d'erreur robuste**
  - **Given:** Une tentative de toggle sur une tâche inexistante (ID invalide)
  - **When:** L'API reçoit une requête avec un `tache_id` invalide
  - **Then:** 
    - La vue retourne un JsonResponse avec `status='error'`
    - Un code HTTP 400 est retourné
    - Aucune exception non gérée ne remonte

- [ ] **AC7: Le rapport affiche le message par défaut quand aucune tâche n'est validée**
  - **Given:** Aucune tâche validée pour la période sélectionnée
  - **When:** L'utilisateur exporte le rapport pour cette période
  - **Then:** 
    - La section "Tâches Validées" affiche le message "Aucune tâche validée ce jour."
    - Aucune table vide n'est affichée
    - Le comportement est identique à celui des "Traitements Validés" dans le même cas

## Additional Context

### Dependencies

**Librairies/Modules:**
- `django.utils.timezone` (déjà importé dans `views.py`)
- `django.core.management.base.BaseCommand` (pour la commande)
- `django.contrib.auth.decorators.user_passes_test` (déjà utilisé)
- `django.views.decorators.http.require_POST` (déjà utilisé)

**Modèles:**
- `Tache` avec champ `done_at` (DateField, nullable) - ligne 105-118 de `models.py`

**Aucune dépendance externe:** Toutes les dépendances sont déjà présentes dans le projet Django existant.

### Testing Strategy

**Note:** Le projet utilise `managed=False` pour ses modèles (legacy DB), ce qui complique les tests unitaires automatisés car Django ne crée pas automatiquement les tables dans la base de test. Par conséquent, nous privilégions les tests manuels et la validation en environnement de développement.

**1. Tests Manuels (Prioritaire)**

a) **Validation du toggle_tache:**
   - Marquer une tâche comme "done" via l'interface
   - Vérifier en base de données que `done_at` est bien défini à la date actuelle
   - Décocher la tâche
   - Vérifier que `done_at` est bien remis à `NULL`

b) **Validation du rapport journalier:**
   - Créer/valider quelques tâches aujourd'hui
   - Aller sur `/admin/kanban/activity/`
   - Cliquer sur "EXPORTER RAPPORT HTML"
   - Sélectionner la période (aujourd'hui)
   - Vérifier que la section "Tâches Validées" affiche bien les tâches validées aujourd'hui

c) **Validation de la commande de correction:**
   - Identifier des tâches avec `done=True` et `done_at=NULL` en base
   - Exécuter la commande: `python web/manage.py fix_task_dates`
   - Vérifier que les tâches ont été corrigées (afficher le compte des mises à jour)
   - Re-vérifier en base de données

**2. Tests de Non-Régression**

- Vérifier que `toggle_traitement` continue de fonctionner normalement
- Vérifier que les autres sections du rapport (Traitements Validés, Cartes Terminées, etc.) fonctionnent toujours
- Vérifier que l'affichage de `done_at` dans `activity_detail.html` fonctionne correctement

**3. Validation SQL (Optionnel)**

Requêtes SQL pour vérifier l'état avant/après:

```sql
-- Tâches validées sans date (avant correction)
SELECT COUNT(*) FROM taches WHERE done = 1 AND done_at IS NULL;

-- Tâches validées avec date (après correction)
SELECT COUNT(*) FROM taches WHERE done = 1 AND done_at IS NOT NULL;

-- Détail des tâches validées aujourd'hui
SELECT * FROM taches WHERE done = 1 AND done_at = date('now');
```

### Notes

**Informations importantes:**
- Le modèle possède déjà le champ `done_at` (DateField, nullable, ligne 109 de `models.py`)
- Le template `admin_export.html` fonctionne correctement et n'a pas besoin de modification
- Les traitements fonctionnent déjà correctement car `toggle_traitement` met à jour `done_at`

**Analyse de risque (Pré-mortem):**

1. **Risque faible:** Base de données legacy avec `managed=False` pourrait avoir des contraintes non documentées
   - **Mitigation:** Tester d'abord en environnement de dev, vérifier les contraintes DB avant déploiement

2. **Risque faible:** Les tâches corrigées rétroactivement auront toutes la même date (date d'exécution de la commande)
   - **Impact:** Acceptable car l'historique précis n'existe pas actuellement
   - **Note:** Documenter ce comportement dans les logs de la commande

3. **Risque très faible:** Possibilité de race condition si plusieurs utilisateurs valident la même tâche simultanément
   - **Impact:** Négligeable car le système est utilisé en solo selon les informations fournies

**Limitations connues:**
- Les tâches corrigées rétroactivement n'auront pas leur date historique réelle de validation
- Pas de tests unitaires automatisés (complexité due à `managed=False`)

**Stratégie de rollback en cas d'erreur:**
Si la commande `fix_task_dates` a été exécutée par erreur, il est possible de revenir en arrière:
1. **Avant correction:** Faire une sauvegarde de la base de données (recommandé)
2. **Si correction erronée:** Restaurer la sauvegarde OU exécuter:
   ```sql
   UPDATE taches SET done_at = NULL WHERE done = 1 AND done_at = '[date_de_correction]';
   ```
3. **Meilleure pratique:** Toujours utiliser `--dry-run` d'abord pour vérifier

**Considérations futures (hors scope):**
- Ajouter un champ `updated_at` pour tracker toutes les modifications
- Créer des tests d'intégration avec une base de test dédiée
- Envisager une migration vers `managed=True` pour faciliter les tests
