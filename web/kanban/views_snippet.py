
from django.contrib.auth.decorators import user_passes_test
from datetime import date, timedelta
from django.db.models import F, Q

@user_passes_test(lambda u: u.is_superuser)
def admin_export_report(request):
    today = date.today()
    
    # 1. Traitements Validated Today
    traitements = Traitement.objects.filter(done=True, done_at=today).select_related('scelle', 'scelle__activity')
    
    # 2. Tasks Validated Today
    taches = Tache.objects.filter(done=True, done_at=today).select_related('scelle', 'scelle__activity')
    
    # 3. Finished Cards (All time or just today? User said "les cartes terminées")
    # Let's list all currently in 'Terminé'.
    finished_cards = Activity.objects.filter(column__name='Terminé').order_by('-date')
    
    # 4. Urgent (Upcoming < 30 days) and Overdue
    # Exclude finished
    active_cards = Activity.objects.exclude(column__name='Terminé')
    
    urgent_cards = []
    overdue_cards = []
    
    limit_date = today + timedelta(days=30)
    
    for card in active_cards:
        if card.date:
            if card.date < today:
                card.days_overdue = (today - card.date).days
                overdue_cards.append(card)
            elif card.date <= limit_date:
                card.days_remaining = (card.date - today).days
                urgent_cards.append(card)
    
    # Sort lists
    overdue_cards.sort(key=lambda x: x.date) # Oldest due date first
    urgent_cards.sort(key=lambda x: x.date) # Sooner due date first
    
    context = {
        'today': today,
        'traitements': traitements,
        'taches': taches,
        'finished_cards': finished_cards,
        'urgent_cards': urgent_cards,
        'overdue_cards': overdue_cards,
    }
    
    return render(request, 'kanban/admin_export.html', context)
