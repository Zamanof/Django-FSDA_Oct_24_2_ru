from flask import Flask, request, jsonify

app = Flask(__name__)

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

@app.get("/api/notes")
def get_notes():
    query = (request.args.get("q") or "").strip().lower()
    notes = list(_notes.values())
    if query:
        notes = [note for note in notes if query in note["title"].lower()]
    return jsonify([serialize_note(note) for note in notes])


@app.get("/api/notes/<int:note_id>")
def get_note(note_id: int):
    note = _notes.get(note_id)
    if note is None:
        return api_error(
            'Note not found',
            404,
            "not_found"
        )
    return jsonify(serialize_note(note))

@app.post("/api/notes")
def create_note():
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
def update_note(note_id: int):
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
def delete_note(note_id: int):
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
