from django.urls import path
from . import views

app_name = 'kanban'

urlpatterns = [
    path('', views.board, name='board'),
    path('synthese/', views.synthese, name='synthese'),
    path('admin-export-form/', views.admin_export_form_view, name='admin_export_form'),
    path('admin-export/', views.admin_export_report, name='admin_export'),
    path('reorder-columns/', views.update_column_order, name='update_column_order'),
    path('move-activity/', views.move_activity, name='move_activity'),
    path('activity/<int:activity_id>/', views.get_activity_details, name='activity_detail'),
    path('api/activity/<int:activity_id>/update/', views.update_activity, name='update_activity'),
    path('api/activity/create/', views.create_activity, name='create_activity'),
    path('api/activity/<int:activity_id>/delete/', views.delete_activity, name='delete_activity'),
    path('api/activity/<int:activity_id>/toggle-tag/', views.toggle_activity_tag, name='toggle_activity_tag'),
    path('api/activity/<int:activity_id>/add-scelle/', views.add_scelle, name='add_scelle'),
    path('api/scelle/<int:scelle_id>/update/', views.update_scelle, name='update_scelle'),
    path('api/scelle/<int:scelle_id>/delete/', views.delete_scelle, name='delete_scelle'),
    path('api/tags/create/', views.create_tag, name='create_tag'),
    path('api/scelle/<int:scelle_id>/add-traitement/', views.add_traitement, name='add_traitement'),
    path('api/traitement/<int:traitement_id>/toggle/', views.toggle_traitement, name='toggle_traitement'),
    path('api/traitement/<int:traitement_id>/delete/', views.delete_traitement, name='delete_traitement'),
    path('api/scelle/<int:scelle_id>/add-tache/', views.add_tache, name='add_tache'),
    path('api/tache/<int:tache_id>/toggle/', views.toggle_tache, name='toggle_tache'),
    path('api/tache/<int:tache_id>/delete/', views.delete_tache, name='delete_tache'),
    path('api/activity/<int:activity_id>/columns/', views.get_activity_columns, name='get_activity_columns'),
    path('api/suggestions/traitements/', views.suggestion_traitements, name='suggestion_traitements'),
    path('api/suggestions/taches/', views.suggestion_taches, name='suggestion_taches'),
    path('archives/', views.archives, name='archives'),
    path('api/activity/<int:activity_id>/archive/', views.archive_activity, name='archive_activity'),
    path('api/activity/<int:activity_id>/unarchive/', views.unarchive_activity, name='unarchive_activity'),
]
