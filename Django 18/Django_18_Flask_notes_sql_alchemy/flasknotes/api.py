from flask import Flask, request, jsonify, redirect, url_for, render_template, flash, Blueprint

from flasknotes import db
from flasknotes.demo import get_demo_user
from flasknotes.models import Note

bp = Blueprint('api', __name__)

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

@bp.get("/api/notes")
def api_get_notes():
    query = (request.args.get("q") or "").strip().lower()
    stmt = db.select(Note).order_by(Note.created_at.desc())
    notes = db.session.execute(stmt).scalars().all()
    if query:
        notes = [note for note in notes if query in note["title"].lower()]
    return jsonify([serialize_note(note) for note in notes])


@bp.get("/api/notes/<int:note_id>")
def api_get_note(note_id: int):
    note = db.session.get(Note, note_id)
    if note is None:
        return api_error(
            'Note not found',
            404,
            "not_found"
        )
    return jsonify(serialize_note(note))

@bp.post("/api/notes")
def api_create_note():
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

    note = Note(title=title, content=content, author=get_demo_user())

    try:
        db.session.add(note)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return jsonify(serialize_note(note)), 201


@bp.patch("/api/notes/<int:note_id>")
def api_update_note(note_id: int):
    note = db.session.get(Note, note_id)
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
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return jsonify(serialize_note(note))


@bp.delete("/api/notes/<int:note_id>")
def api_delete_note(note_id: int):
    note = db.session.get(Note, note_id)
    if note is None:
        return api_error(
            'Note not found',
            404,
            "not_found"
        )
    try:
        db.session.delete(note)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return ('', 204)