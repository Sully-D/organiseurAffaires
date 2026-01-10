from django.shortcuts import render
from .models import KanbanColumn, Activity, Tag
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test

def board(request):
    columns = KanbanColumn.objects.exclude(name='Archivé').order_by('order_index')
    
    # Organize activities by column
    columns_data = []
    
    for col in columns:
        if col.name == "Traitements":
            activities = Activity.objects.filter(
                Q(column=col) | 
                (
                    Q(column__name="En cours") & 
                    Q(scelles__traitements__done=False) & 
                    Q(scelles__cta_validated=False) & 
                    Q(scelles__reparations_validated=False)
                )
            ).prefetch_related('tags', 'scelles').distinct().order_by('date')
            
        elif col.name == "Tâches":
            activities = Activity.objects.filter(
                Q(column=col) | 
                (
                    Q(column__name="En cours") & 
                    Q(scelles__taches__done=False) & 
                    Q(scelles__cta_validated=False) & 
                    Q(scelles__reparations_validated=False)
                )
            ).prefetch_related('tags', 'scelles').distinct().order_by('date')
            
        elif col.name == "CTA":
            activities = Activity.objects.filter(
                Q(column=col) | 
                (Q(column__name="En cours") & Q(scelles__cta_validated=True))
            ).prefetch_related('tags', 'scelles').distinct().order_by('date')
            
        elif col.name == "Réparations":
            activities = Activity.objects.filter(
                Q(column=col) | 
                (Q(column__name="En cours") & Q(scelles__reparations_validated=True))
            ).prefetch_related('tags', 'scelles').distinct().order_by('date')

        elif col.name == "En attente":
            activities = Activity.objects.filter(
                Q(column=col) | 
                (
                    Q(column__name="En cours") & 
                    (Q(scelles__cta_validated=True) | Q(scelles__reparations_validated=True))
                )
            ).prefetch_related('tags', 'scelles').distinct().order_by('date')
            
        elif col.name == "En cours":
            # Exclude activities if they are fully handled by virtual columns?
            # Or if they appear in any virtual column?
            # User said "ne s'affiche que dans...", implying exclusion.
            # We exclude if it matches ANY of the virtual criteria.
            # Note: This means if a card has a scellé in CTA, it leaves "En cours".
            # If it ALSO has a scellé in Traitements, it appears in Traitements.
            # So it is visible in CTA and Traitements, but NOT En cours. This fits the requirement.
            
            activities = Activity.objects.filter(column=col).exclude(
                (Q(scelles__traitements__done=False) & Q(scelles__cta_validated=False) & Q(scelles__reparations_validated=False)) |
                (Q(scelles__taches__done=False) & Q(scelles__cta_validated=False) & Q(scelles__reparations_validated=False)) |
                Q(scelles__cta_validated=True) | 
                Q(scelles__reparations_validated=True)
            ).prefetch_related('tags', 'scelles').distinct().order_by('date')
            
        else:
            activities = Activity.objects.filter(column=col).prefetch_related('tags', 'scelles').order_by('date')
            
        columns_data.append({
            'column': col,
            'activities': activities
        })
        
    context = {
        'columns_data': columns_data,
        'page_title': "Tableau de Bord"
    }
    return render(request, 'kanban/board.html', context)

# ... (API endpoints remain unchanged until get_activity_columns) ...

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def update_column_order(request):
    try:
        data = json.loads(request.body)
        order = data.get('order', [])
        
        with transaction.atomic():
            for index, col_id in enumerate(order):
                KanbanColumn.objects.filter(id=col_id).update(order_index=index)
                
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def move_activity(request):
    try:
        data = json.loads(request.body)
        activity_id = data.get('activity_id')
        column_id = data.get('column_id')
        
        if not activity_id or not column_id:
            return JsonResponse({'status': 'error', 'message': 'Missing activity_id or column_id'}, status=400)
            
        activity = Activity.objects.get(id=activity_id)
        column = KanbanColumn.objects.get(id=column_id)
        
        activity.column = column
        activity.save()
        
        return JsonResponse({'status': 'success'})
    except Activity.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Activity not found'}, status=404)
    except KanbanColumn.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Column not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def get_activity_details(request, activity_id):
    try:
        activity = Activity.objects.prefetch_related(
            'tags',
            'scelles',
            'scelles__traitements',
            'scelles__taches',
            'scelles__tags'
        ).get(id=activity_id)
        
        context = {
            'activity': activity,
            'all_tags': Tag.objects.all()
        }
        return render(request, 'kanban/activity_detail.html', context)
    except Activity.DoesNotExist:
        return JsonResponse({'error': 'Activity not found'}, status=404)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def create_tag(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        color = data.get('color', '#3b82f6') # Default blue
        
        if not name:
            return JsonResponse({'status': 'error', 'message': 'Missing name'}, status=400)
            
        tag, created = Tag.objects.get_or_create(name=name, defaults={'color': color})
        return JsonResponse({'status': 'success', 'tag': {'id': tag.id, 'name': tag.name, 'color': tag.color}})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def update_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        data = json.loads(request.body)
        
        if 'name' in data:
            activity.name = data['name']
        if 'date' in data and data['date']:
            from datetime import datetime
            try:
                # Handle YYYY-MM-DD format from input[type=date]
                date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
                activity.date = date_obj
            except ValueError:
                # Fallback or ignore if invalid
                pass
        if 'description' in data:
            activity.description = data['description']
            
        activity.save()
        return JsonResponse({'status': 'success'})
    except Activity.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Activity not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def toggle_activity_tag(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        data = json.loads(request.body)
        tag_id = data.get('tag_id')
        
        if not tag_id:
            return JsonResponse({'status': 'error', 'message': 'Missing tag_id'}, status=400)
            
        tag = Tag.objects.get(id=tag_id)
        
        if tag in activity.tags.all():
            activity.tags.remove(tag)
            action = 'removed'
        else:
            activity.tags.add(tag)
            action = 'added'
            
        return JsonResponse({'status': 'success', 'action': action})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def delete_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        
        # Manual Cascade
        # 1. Scelles (and their children Traitements/Taches via their own models)
        # We loop to ensure Django signals/cascades on Scelle children run if needed
        for scelle in activity.scelles.all():
            scelle.delete()
            
        # 2. Tags (M2M) - clear association
        activity.tags.clear()
        
        # 3. Delete Activity
        activity.delete()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        print(f"Error deleting activity: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def create_activity(request):
    try:
        data = json.loads(request.body)
        column_id = data.get('column_id')
        if not column_id:
            return JsonResponse({'status': 'error', 'message': 'Missing column_id'}, status=400)
            
        column = KanbanColumn.objects.get(id=column_id)
        
        activity = Activity.objects.create(
            name="Nouvelle Activité",
            date=timezone.now().date(),
            description="",
            column=column
        )
        
        # Render the card HTML
        card_html = render_to_string('kanban/card_snippet.html', {'activity': activity})
        
        return JsonResponse({
            'status': 'success', 
            'activity_id': activity.id,
            'card_html': card_html
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def add_scelle(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        # Using default values for new scelle
        from .models import Scelle
        scelle = Scelle.objects.create(
            activity=activity,
            name="Nouveau Scellé",
            info=""
        )
        return JsonResponse({'status': 'success', 'scelle_id': scelle.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def update_scelle(request, scelle_id):
    try:
        from .models import Scelle
        scelle = Scelle.objects.get(id=scelle_id)
        data = json.loads(request.body)
        
        if 'name' in data:
            scelle.name = data['name']
        if 'info' in data:
            scelle.info = data['info']
        if 'cta_validated' in data:
            scelle.cta_validated = data['cta_validated']
        if 'reparations_validated' in data:
            scelle.reparations_validated = data['reparations_validated']
            
        scelle.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def delete_scelle(request, scelle_id):
    try:
        from .models import Scelle
        Scelle.objects.filter(id=scelle_id).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# Traitements & Tâches APIs

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def add_traitement(request, scelle_id):
    try:
        from .models import Scelle, Traitement
        scelle = Scelle.objects.get(id=scelle_id)
        data = json.loads(request.body)
        description = data.get('description')
        if not description:
            return JsonResponse({'status': 'error', 'message': 'Missing description'}, status=400)
            
        t = Traitement.objects.create(scelle=scelle, description=description, done=False)
        return JsonResponse({'status': 'success', 'traitement_id': t.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def toggle_traitement(request, traitement_id):
    try:
        from .models import Traitement
        # Already imported timezone at top
        t = Traitement.objects.get(id=traitement_id)
        t.done = not t.done
        if t.done:
            t.done_at = timezone.now().date()
        else:
            t.done_at = None
        t.save()
        return JsonResponse({'status': 'success', 'done': t.done})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def delete_traitement(request, traitement_id):
    try:
        from .models import Traitement
        Traitement.objects.filter(id=traitement_id).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def add_tache(request, scelle_id):
    try:
        from .models import Scelle, Tache
        scelle = Scelle.objects.get(id=scelle_id)
        data = json.loads(request.body)
        description = data.get('description')
        if not description:
            return JsonResponse({'status': 'error', 'message': 'Missing description'}, status=400)
            
        t = Tache.objects.create(scelle=scelle, description=description, done=False)
        return JsonResponse({'status': 'success', 'tache_id': t.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def toggle_tache(request, tache_id):
    try:
        from .models import Tache
        t = Tache.objects.get(id=tache_id)
        t.done = not t.done
        t.save()
        return JsonResponse({'status': 'success', 'done': t.done})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def delete_tache(request, tache_id):
    try:
        from .models import Tache
        Tache.objects.filter(id=tache_id).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@require_POST
def get_activity_columns(request, activity_id):
    try:
        activity = Activity.objects.prefetch_related('tags', 'scelles').get(id=activity_id)
        
        # Calculate in which columns this activity should appear
        target_columns = []
        
        # 1. Physical column
        if activity.column:
            # Special case for "En cours": filtering out if CTA/Rep validated
            if activity.column.name == "En cours":
                has_cta = activity.scelles.filter(cta_validated=True).exists()
                has_rep = activity.scelles.filter(reparations_validated=True).exists()
                
                if not has_cta and not has_rep:
                    target_columns.append(activity.column.id)
            else:
                target_columns.append(activity.column.id)
            
            # 2. Virtual Columns (only if physical is "En cours")
            if activity.column.name == "En cours":
                has_cta = activity.scelles.filter(cta_validated=True).exists()
                has_rep = activity.scelles.filter(reparations_validated=True).exists()
                
                # En attente logic (Aggregation)
                if has_cta or has_rep:
                    try:
                        attente_col = KanbanColumn.objects.get(name="En attente")
                        target_columns.append(attente_col.id)
                    except KanbanColumn.DoesNotExist:
                        pass
                
                if has_cta:
                    try:
                        cta_col = KanbanColumn.objects.get(name="CTA")
                        target_columns.append(cta_col.id)
                    except KanbanColumn.DoesNotExist:
                        pass
                        
                if has_rep:
                    try:
                        rep_col = KanbanColumn.objects.get(name="Réparations")
                        target_columns.append(rep_col.id)
                    except KanbanColumn.DoesNotExist:
                        pass
                
                # Check for Traitements (additive but EXCLUSIVE of CTA/Rep on same scelle)
                if activity.scelles.filter(
                    traitements__done=False,
                    cta_validated=False,
                    reparations_validated=False
                ).exists():
                    try:
                        traitement_col = KanbanColumn.objects.get(name="Traitements")
                        target_columns.append(traitement_col.id)
                    except KanbanColumn.DoesNotExist:
                        pass
                        
                # Check for Tâches (additive but EXCLUSIVE of CTA/Rep on same scelle)
                if activity.scelles.filter(
                    taches__done=False,
                    cta_validated=False,
                    reparations_validated=False
                ).exists():
                    try:
                        tache_col = KanbanColumn.objects.get(name="Tâches")
                        target_columns.append(tache_col.id)
                    except KanbanColumn.DoesNotExist:
                        pass

        card_html = render_to_string('kanban/card_snippet.html', {'activity': activity})
        
        return JsonResponse({
            'status': 'success', 
            'columns': list(set(target_columns)), # Unique
            'card_html': card_html
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def suggestion_traitements(request):
    try:
        from .models import Traitement
        descriptions = Traitement.objects.filter(description__isnull=False).exclude(description__exact='').values_list('description', flat=True).distinct().order_by('description')
        return JsonResponse({'status': 'success', 'suggestions': list(descriptions)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def suggestion_taches(request):
    try:
        from .models import Tache
        descriptions = Tache.objects.filter(description__isnull=False).exclude(description__exact='').values_list('description', flat=True).distinct().order_by('description')
        return JsonResponse({'status': 'success', 'suggestions': list(descriptions)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def archives(request):
    try:
        archived_col = KanbanColumn.objects.get(name='Archivé')
        activities = Activity.objects.filter(column=archived_col).order_by('-date')
    except KanbanColumn.DoesNotExist:
        activities = []
    
    context = {
        'activities': activities,
        'page_title': "Archives"
    }
    return render(request, 'kanban/archives.html', context)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def archive_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        archived_col, _ = KanbanColumn.objects.get_or_create(name='Archivé')
        activity.column = archived_col
        activity.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def unarchive_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        # Move back to "En attente" by default
        target_col = KanbanColumn.objects.get(name='En attente')
        activity.column = target_col
        activity.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # Fallback if "En attente" doesn't exist? (Unlikely)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
