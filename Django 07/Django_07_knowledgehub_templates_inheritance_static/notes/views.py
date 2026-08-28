from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
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
    print(note)
    return render(request, "notes/note_detail.html", {'note': note})


def note_create(request: HttpRequest) -> HttpResponse:
    err = ""

    if request.method == "POST":

        title = request.POST.get("title", "")
        content = request.POST.get("body", "")
        tags = request.POST.get("tags", "")
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
                content=content.strip(),
                tags= tags.split() or "misc",
                category=category.strip() or "general"
            )
            return redirect("notes_list")

    else:
        title = ""
        body = ""
        tag = ""
        category = ""

    return render(request, "notes/note_create.html")


def note_delete(request: HttpRequest, note_id:int) -> HttpResponse:
    pass


def note_edit(request: HttpRequest, note_id:int) -> HttpResponse:
    pass