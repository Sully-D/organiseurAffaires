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
