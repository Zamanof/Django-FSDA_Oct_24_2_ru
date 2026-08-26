from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import escape

from . import data


# CSRF -> Cross-Site Request Forgery

def _csrf_field(request):
    token = get_token(request)
    return f"""
        <input
            type="hidden"
            name="csrfmiddlewaretoken"
            value="{escape(token)}"
        >
    """


def _html_page(title: str, content: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{escape(title)}</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                color: #2d3436;
            }}

            .container {{
                max-width: 800px;
                margin: 50px auto;
                padding: 30px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            }}

            h1 {{
                margin-top: 0;
                color: #2c3e50;
            }}

            a {{
                color: #3498db;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}

            .notes {{
                list-style: none;
                padding: 0;
            }}

            .notes li {{
                margin-bottom: 10px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #3498db;
            }}

            .notes li:hover {{
                background: #eef5fb;
            }}

            label {{
                font-weight: bold;
            }}

            input,
            textarea {{
                width: 100%;
                padding: 10px;
                margin-top: 6px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }}

            input:focus,
            textarea:focus {{
                outline: none;
                border-color: #3498db;
            }}

            button,
            .button {{
                display: inline-block;
                padding: 10px 18px;
                background: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                text-decoration: none;
            }}

            button:hover,
            .button:hover {{
                background: #2980b9;
                text-decoration: none;
            }}

            .error {{
                padding: 10px;
                background: #ffe5e5;
                color: #c0392b;
                border-radius: 6px;
                margin-bottom: 15px;
            }}

            .actions {{
                margin-top: 25px;
            }}

            .note-body {{
                line-height: 1.6;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """


def home(request: HttpRequest) -> HttpResponse:
    content = f"""
        <h1>📚 Knowledge Hub</h1>

        <p>
            Welcome to Knowledge Hub.
            Here you can create and manage your notes.
        </p>

        <div class="actions">
            <a class="button" href="{escape(reverse('notes_list'))}">
                View Notes
            </a>

            <a class="button" href="{escape(reverse('note_create'))}">
                Create Note
            </a>
        </div>
    """

    return HttpResponse(
        _html_page("Knowledge Hub", content)
    )


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

    items: list[str] = []

    for note in notes:
        url = reverse(
            "note_detail",
            kwargs={"note_id": note["id"]}
        )

        items.append(
            f"""
            <li>
                <a href="{escape(url)}">
                    <strong>{escape(note["title"])}</strong>
                </a>

                <br>

                <small>
                    Tag: {escape(note["tag"])}
                    |
                    Category: {escape(note["category"])}
                </small>
            </li>
            """
        )

    if items:
        notes_html = f"""
            <ul class="notes">
                {"".join(items)}
            </ul>
        """
    else:
        notes_html = """
            <p>No notes found.</p>
        """

    content = f"""
        <h1>📝 Knowledge Hub Notes</h1>

        <div class="actions">
            <a class="button"
               href="{escape(reverse('note_create'))}">
                + Create Note
            </a>
        </div>

        {notes_html}

        <div class="actions">
            <a href="{escape(reverse('home'))}">
                ← Return to Home
            </a>
        </div>
    """

    return HttpResponse(
        _html_page("Notes", content)
    )


def note_detail(
    request: HttpRequest,
    note_id: int
) -> HttpResponse:

    note = data.get_note(note_id)

    if note is None:
        content = f"""
            <h1>❌ Note not found</h1>

            <p>
                Note with ID {note_id} does not exist.
            </p>

            <a href="{escape(reverse('notes_list'))}">
                ← Return to Notes
            </a>
        """

        return HttpResponse(
            _html_page("Note not found", content),
            status=404
        )

    content = f"""
        <h1>{escape(note["title"])}</h1>

        <div class="note-body">
            {escape(note["body"])}
        </div>

        <p>
            <strong>Tag:</strong>
            {escape(note["tag"])}
        </p>

        <p>
            <strong>Category:</strong>
            {escape(note["category"])}
        </p>

        <div class="actions">
            <a href="{escape(reverse('notes_list'))}">
                ← Return to Notes
            </a>
        </div>
    """

    return HttpResponse(
        _html_page(note["title"], content)
    )


def note_create(request: HttpRequest) -> HttpResponse:
    err = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        if not title.strip():
            err = """
                <div class="error">
                    Title cannot be empty.
                </div>
            """

        else:
            data.create_note(
                title=title.strip(),
                body=body.strip(),
                tag=tag.strip() or "misc",
                category=category.strip() or "general"
            )

            # PRG -> Post / Redirect / Get
            return redirect("notes_list")

    else:
        title = ""
        body = ""
        tag = ""
        category = ""

    action = escape(reverse("note_create"))

    form = f"""
        <h1>✏️ Create Note</h1>

        <p>
            Add a new note to your Knowledge Hub.
        </p>

        {err}

        <form method="post" action="{action}">

            {_csrf_field(request)}

            <p>
                <label>Title</label>
                <input
                    type="text"
                    name="title"
                    value="{escape(title)}"
                    placeholder="Enter note title"
                    required
                >
            </p>

            <p>
                <label>Text</label>
                <textarea
                    name="body"
                    rows="6"
                    placeholder="Write your note..."
                >{escape(body)}</textarea>
            </p>

            <p>
                <label>Tag</label>
                <input
                    type="text"
                    name="tag"
                    value="{escape(tag)}"
                    placeholder="Example: django"
                >
            </p>

            <p>
                <label>Category</label>
                <input
                    type="text"
                    name="category"
                    value="{escape(category)}"
                    placeholder="Example: backend"
                >
            </p>

            <p>
                <button type="submit">
                    Save Note
                </button>
            </p>

        </form>

        <div class="actions">
            <a href="{escape(reverse('notes_list'))}">
                ← Cancel and return to Notes
            </a>
        </div>
    """

    return HttpResponse(
        _html_page("Create Note", form)
    )


def note_delete(request: HttpRequest, note_id:int) -> HttpResponse:
    pass


def note_edit(request: HttpRequest, note_id:int) -> HttpResponse:
    pass