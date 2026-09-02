from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.html import escape

from . import data
from .forms import NoteForm

def home(request: HttpRequest) -> HttpResponse:
    return render(request, "notes/home.html")


def about(request: HttpRequest):
    context = {
        'project_name': "Knowledge Hub",
        'author_name': "Nadir Zamanov",
    }
    return render(request, "notes/about.html", context)

def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get("tag")
    raw_category = request.GET.get("category")

    notes = data.list_notes()

    if raw_tag:
        raw_tag = raw_tag.strip().lower()
        notes = [
            n for n in notes
            if n["tag"].lower() == raw_tag
        ]

    if raw_category:
        raw_category = raw_category.strip().lower()
        notes = [
            n for n in notes
            if n["category"].lower() == raw_category
        ]



    return render(request, "notes/note_list.html", {'notes': notes})


def note_detail(
    request: HttpRequest,
    note_id: int
) -> HttpResponse:

    note = data.get_note(note_id)
    return render(request, "notes/note_detail.html", {'note_id':note_id, 'note': note})


def note_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            notes = request.session.get("notes", [])
            notes.append(
                {
                    'title': form.cleaned_data["title"],
                    'content': form.cleaned_data["content"],
                    'tags': form.cleaned_data["tags"],
                    'category': form.cleaned_data["category"],
                }
            )
            request.session["notes"] = notes
            data.create_note(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
            tags=form.cleaned_data["tags"].split(),
            category=form.cleaned_data["category"],)
            return redirect("notes_list")
    else:
        form = NoteForm()

    return render(request, "notes/note_create.html", {'form': form})


def note_delete(request: HttpRequest, note_id:int) -> HttpResponse:
    note = data.get_note(note_id)
    if request.method == "POST":
        data.delete_note(note_id)
        return redirect("notes_list")
    return render(request, "notes/note_delete.html", {'note': note})


def note_edit(request: HttpRequest, note_id:int) -> HttpResponse:
    note = data.get_note(note_id)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            tags = form.cleaned_data["tags"]
            category = form.cleaned_data["category"]
            data.edit_note(
                note_id,
                title=title,
                content=content,
                tags=tags.split(),
                category=category)
            return redirect("notes_list")
    else:
        form = NoteForm(initial=
                        {
                            'title': note["title"],
                            'content': note["content"],
                            'tags': ' '.join(note["tags"]),
                            'category': note["category"]
                        })
    return render(request, "notes/note_edit.html", {
        "note":note,
        "note_id":note_id,
        'form': form})