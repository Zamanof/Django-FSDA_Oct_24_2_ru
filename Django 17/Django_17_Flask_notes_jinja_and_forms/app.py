from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
from forms import NoteForm
import os

load_dotenv()
app = Flask(__name__)

secret = os.environ.get("SECRET_KEY")
if not secret:
    raise RuntimeError("Missing SECRET_KEY")
app.config["SECRET_KEY"] = secret

csrf = CSRFProtect(app)


_notes: dict[int, dict] = {}
_next_id: int = 1

def api_error(message: str, status:int, error:str='error'):
    return jsonify({'error': error, 'message':message}), status

def parse_json_object()-> tuple[dict|None, tuple|None]:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, api_error(
            'Invalid JSON object',
            400, ""
                 "invalid_json")
    return data, None


def serialize_note(note: dict) -> dict:
    return {
        "id": note['id'],
        "title": note['title'],
        "content": note['content'],
    }


def parse_title(data:dict)->tuple[str|None, tuple|None]:
    raw_title = data.get('title')
    if not isinstance(raw_title, str) or not raw_title.strip():
        return None, api_error(
            'Title cannot be empty',
            400,
            "validation_error"
        )
    return raw_title.strip(), None

@app.get('/')
def home():
    return redirect(url_for("get_notes"))


@app.get("/notes")
def get_notes():
    notes = list(_notes.values())
    return render_template("notes/list.html", notes=notes)

@app.get("/notes/<int:note_id>")
def note_detail(note_id: int):
    note = _notes.get(note_id)
    if note is None:
        flash("Note not found", "error")
        return redirect(url_for("get_notes"))
    return render_template("notes/detail.html", note=note)


@app.route("/notes/create", methods=["GET","POST"])
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        global _next_id
        note = {
            "id": _next_id,
            "title": form.title.data.strip(),
            "content": form.content.data.strip()
        }
        _notes[_next_id] = note
        _next_id += 1
        flash("Note created", "success")
        return redirect(url_for("note_detail", note_id=note["id"]))
    return render_template("notes/form.html", form=form, mode='create')





@app.get("/api/notes")
def api_get_notes():
    query = (request.args.get("q") or "").strip().lower()
    notes = list(_notes.values())
    if query:
        notes = [note for note in notes if query in note["title"].lower()]
    return jsonify([serialize_note(note) for note in notes])


@app.get("/api/notes/<int:note_id>")
def api_get_note(note_id: int):
    note = _notes.get(note_id)
    if note is None:
        return api_error(
            'Note not found',
            404,
            "not_found"
        )
    return jsonify(serialize_note(note))

@app.post("/api/notes")
def api_create_note():
    global _next_id
    data, error = parse_json_object()

    if error:
        return error

    title, error = parse_title(data)

    if error:
        return error

    content = data.get('content', '')
    if content is None:
        content = ''

    if not isinstance(content, str):
        return api_error(
            'Content must be a string',
            400,
            "validation_error"
        )

    note = {
        "id": _next_id,
        "title": title,
        "content": content
    }
    _notes[_next_id] = note
    _next_id += 1
    return jsonify(serialize_note(note)), 201


@app.patch("/api/notes/<int:note_id>")
def api_update_note(note_id: int):
    note = _notes.get(note_id)
    if note is None:
        return api_error(
            'Note not found',
            404,
            "not_found"
        )
    data, error = parse_json_object()
    if "title" in data:
        title, _error = parse_title(data)
        if error:
            return error
    note['title'] = title
    if "content" in data:
        content = data["content"]
        if content is None:
            content = ''
        if not isinstance(content, str):
            return api_error(
                'Content must be a string',
                400,
                "validation_error"
            )
        note["content"] = content
    return jsonify(serialize_note(note))


@app.delete("/api/notes/<int:note_id>")
def api_delete_note(note_id: int):
    if note_id not in _notes:
        return api_error(
            'Note not found',
            404,
            "not_found"
        )
    del _notes[note_id]
    return ('', 204)

if __name__ == '__main__':
    app.run()
