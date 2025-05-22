from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from functools import wraps

from .models import Note
from .forms import NoteForm, UserSignUpForm

def owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, pk, *args, **kwargs):
        note = get_object_or_404(Note, pk=pk)
        if note.created_by != request.user:
            raise PermissionDenied
        return view_func(request, pk, *args, **kwargs)
    return _wrapped_view

def note_list_view(request):
    notes = Note.objects.all().order_by('-created_at')
    context = {
        'notes': notes
    }
    return render(request, 'notes/notes_list.html', context)

def note_detail_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    context = {
        'note': note
    }
    return render(request, 'notes/note_detail.html', context)

@login_required
def note_create_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            return redirect(reverse_lazy('notes:note-list'))
    else:
        form = NoteForm()
    context = {
        'form': form
    }
    return render(request, 'notes/note_form.html', context)

@login_required
@owner_required
def note_update_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('notes:note-list'))
    else:
        form = NoteForm(instance=note)
    context = {
        'form': form,
        'note': note
    }
    return render(request, 'notes/note_form.html', context)

@login_required
@owner_required
def note_delete_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect(reverse_lazy('notes:note-list'))
    context = {
        'note': note
    }
    return render(request, 'notes/note_confirm_delete.html', context)

@login_required
def my_notes_view(request):
    notes = Note.objects.filter(created_by=request.user).order_by('-created_at')
    context = {
        'notes': notes
    }
    return render(request, 'notes/notes_mine.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse_lazy('notes:note-list'))
    else:
        form = UserSignUpForm()
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)
