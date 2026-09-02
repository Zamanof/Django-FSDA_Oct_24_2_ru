from copy import deepcopy
from datetime import datetime
from typing import Any

from datetime import datetime
from typing import Any


from datetime import datetime
from typing import Any


_NOTES: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Django Views",
        "content": "View принимает request и возвращает response",
        "tags": ["python", "django", "views", "web"],
        "category": "backend",
        "created_at": datetime(2026, 8, 26),
    },
    {
        "id": 2,
        "title": "Django URLs",
        "content": "URL-маршруты связывают адреса страниц с соответствующими views",
        "tags": ["django"],
        "category": "backend",
        "created_at": datetime(2026, 8, 24),
    },
    {
        "id": 3,
        "title": "Django Models",
        "content": "Models используются для описания структуры данных и работы с базой данных",
        "tags": ["django", "python", "database", "models", "orm", "sql"],
        "category": "database",
        "created_at": datetime(2026, 8, 21),
    },
    {
        "id": 4,
        "title": "Python Functions",
        "content": "Функции позволяют группировать код и повторно использовать его",
        "tags": ["python", "functions"],
        "category": "programming",
        "created_at": datetime(2026, 8, 19),
    },
    {
        "id": 5,
        "title": "Python Generators",
        "content": "Генераторы используют yield для последовательного возврата значений",
        "tags": ["python", "generators", "yield", "iterator", "programming"],
        "category": "programming",
        "created_at": datetime(2026, 8, 16),
    },
    {
        "id": 6,
        "title": "HTML Forms",
        "content": "HTML-формы используются для отправки пользовательских данных на сервер",
        "tags": ["html", "forms", "frontend"],
        "category": "frontend",
        "created_at": datetime(2026, 8, 14),
    },
    {
        "id": 7,
        "title": "CSS Flexbox",
        "content": "Flexbox позволяет удобно располагать элементы внутри контейнера",
        "tags": ["css", "flexbox"],
        "category": "frontend",
        "created_at": datetime(2026, 8, 11),
    },
    {
        "id": 8,
        "title": "JavaScript Events",
        "content": "События позволяют выполнять JavaScript-код в ответ на действия пользователя",
        "tags": ["javascript", "events", "dom", "browser", "frontend", "web"],
        "category": "frontend",
        "created_at": datetime(2026, 8, 7),
    },
    {
        "id": 9,
        "title": "SQL SELECT",
        "content": "Команда SELECT используется для получения данных из таблицы",
        "tags": ["sql", "database", "query"],
        "category": "database",
        "created_at": datetime(2026, 8, 3),
    },
    {
        "id": 10,
        "title": "REST API",
        "content": "REST API позволяет клиенту и серверу обмениваться данными через HTTP",
        "tags": ["api", "rest", "http", "backend", "web"],
        "category": "backend",
        "created_at": datetime(2026, 7, 29),
    },
]

_next_id: int = 11

def list_notes()->list[dict[str: Any]]:
    return deepcopy(_NOTES)


def get_note(note_id: int) -> dict[str: Any]|None:
    for note in _NOTES:
        if note["id"] == note_id:
            return deepcopy(note)
    return None

def create_note(*, title:str, content:str, tags:list[str], category:str) -> dict[str: Any]:
    global _next_id
    note = {
        "id": _next_id,
        "title": title.strip(),
        "content": content.strip(),
        "tags": tags,
        "category": category.strip(),
        "created_at": datetime.now()
    }

    _NOTES.append(note)
    _next_id += 1
    return deepcopy(note)


def delete_note(note_id: int) -> bool:
    global _NOTES
    before = len(_NOTES)
    _NOTES = [n for n in _NOTES if n["id"] != note_id]
    return len(_NOTES) != before


def edit_note(
        note_id: int,
        *,
        title:str,
        content:str,
        tags:list['str'],
        category:str) -> dict[str: Any]|None:
    for note in _NOTES:
        if note["id"] == note_id:
            note["title"] = title.strip()
            note["content"] = content.strip()
            note["tags"] = ' '.join(tags)
            note["category"] = category.strip()
            return deepcopy(note)
    return None

