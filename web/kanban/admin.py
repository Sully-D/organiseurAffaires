from django.contrib import admin
from .models import KanbanColumn, Tag, Activity, Scelle, Traitement, Tache

@admin.register(KanbanColumn)
class KanbanColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_index')
    ordering = ('order_index',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

class ScelleInline(admin.TabularInline):
    model = Scelle
    extra = 0

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    change_list_template = "kanban/admin_change_list.html"
    list_display = ('name', 'date', 'column')
    list_filter = ('column', 'date', 'tags')
    search_fields = ('name', 'description')
    inlines = [ScelleInline]

class TraitementInline(admin.TabularInline):
    model = Traitement
    extra = 0

class TacheInline(admin.TabularInline):
    model = Tache
    extra = 0

@admin.register(Scelle)
class ScelleAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity', 'cta_validated', 'reparations_validated')
    list_filter = ('cta_validated', 'reparations_validated', 'activity__column')
    search_fields = ('name', 'info')
    inlines = [TraitementInline, TacheInline]

@admin.register(Traitement)
class TraitementAdmin(admin.ModelAdmin):
    list_display = ('description', 'scelle', 'done', 'done_at')
    list_filter = ('done',)

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('description', 'scelle', 'done', 'done_at')
    list_filter = ('done',)
