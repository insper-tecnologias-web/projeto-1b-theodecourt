from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/<int:tag_id>/', views.notes_by_tag, name='notes_by_tag'),
    path('api/notes/<int:note_id>/', views.api_note),
    path('api/notes/', views.api_note2),
]