from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404

from .forms import NoteForm
from .models import Note

def home(request: HttpRequest) -> HttpResponse:
    return render(request, "notes/home.html")


def about(request: HttpRequest):
    context = {
        'project_name': "Knowledge Hub",
        'author_name': "Nadir Zamanov",
    }
    return render(request, "notes/about.html", context)

def notes_list(request: HttpRequest) -> HttpResponse:
    notes = Note.objects.select_related('author', 'category').prefetch_related('tags').all()

    return render(request, "notes/note_list.html", {'notes': notes})


def note_detail(
    request: HttpRequest,
    note_id: int
) -> HttpResponse:

    note = get_object_or_404(
        Note.objects.select_related('author', 'category').prefetch_related('tags'), pk=note_id)

    return render(request, "notes/note_detail.html", {'note': note})

@login_required
def note_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            form.save_m2m()
            messages.success(request, "Note created")
            return redirect("notes:note_detail", note_id=note.pk)
    else:
        form = NoteForm()
    return render(request, "notes/note_create.html", {'form': form})

@login_required
def note_delete(request: HttpRequest, note_id:int) -> HttpResponse:
    note = get_object_or_404(Note, pk=note_id)
    if note.author_id != request.user.id:
        return HttpResponseForbidden("Udalit mojet tolko avtor zametki")
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted")
        return redirect("notes:notes_list")
    return render(request, "notes/note_delete.html", {'note': note})

@login_required
def note_edit(request: HttpRequest, note_id:int) -> HttpResponse:
    note = get_object_or_404(Note, pk=note_id)

    if note.author_id != request.user.id:
        return  HttpResponseForbidden("Redaktirovat mojet tolko avtor zametki")

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated")
            return redirect("notes:note_detail", note_id=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/note_edit.html", {
        'note': note,
        'form': form,
    })