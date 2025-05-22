from django.contrib import admin
from .models import Note

# Register your models here.

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at']
    list_filter = ['created_by', 'created_at'] # Added for better filtering
    search_fields = ['title', 'content'] # Added for searching
