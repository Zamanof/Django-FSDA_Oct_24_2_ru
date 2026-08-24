from typing import Any

from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import escape

from . import data



def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Knowledge Hub home page")


def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get("tag")
    raw_category = request.GET.get("category")

    notes = data.list_notes()

    if raw_tag:
        raw_tag = raw_tag.strip().lower()
        notes = [n for n in notes if n['tag'].lower() == raw_tag]
    if raw_category:
        raw_category = raw_category.strip().lower()
        notes = [n for n in notes if n['category'].lower() == raw_category]

    items:list[str] = []
    for note in notes:
        url = reverse("note_detail", kwargs={"note_id": note["id"]})
        items.append(f"""
        <li>
            <a href="{escape(url)}">{escape(note["title"])}</a>
        </li>
""")

    body = (
        f"""
            <h1>Knowledge Hub Notes</h1>
            <ul>
                {"".join(items)}
            </ul>
            <p>
                <a href={escape(reverse("home"))}>Return to home page</a>
            </p>
        """
    )
    return HttpResponse(body)

def note_detail(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse("Note not found")

    body = (f"""
    <h1>{escape((note['title']))}</h1>
    <p>{escape((note['body']))}</p>
    <p>
       <a href={escape(reverse("notes_list"))}>Return to note lists</a>
    </p>
    
    """)
    return HttpResponse(body)