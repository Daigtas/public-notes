from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list_view, name='note-list'),
    path('<int:pk>/', views.note_detail_view, name='note-detail'),
    path('create/', views.note_create_view, name='note-create'),
    path('<int:pk>/edit/', views.note_update_view, name='note-update'),
    path('<int:pk>/delete/', views.note_delete_view, name='note-delete'),
    path('mine/', views.my_notes_view, name='my-notes'),
]
