from copy import deepcopy
from typing import Any

_NOTES: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Django Views",
        "body": "View принимает request и возвращает response",
        "tag": "django",
        "category": "backend",
    },
    {
        "id": 2,
        "title": "Django URLs",
        "body": "URL-маршруты связывают адреса страниц с соответствующими views",
        "tag": "django",
        "category": "backend",
    },
    {
        "id": 3,
        "title": "Django Models",
        "body": "Models используются для описания структуры данных и работы с базой данных",
        "tag": "django",
        "category": "database",
    },
    {
        "id": 4,
        "title": "Python Functions",
        "body": "Функции позволяют группировать код и повторно использовать его",
        "tag": "python",
        "category": "programming",
    },
    {
        "id": 5,
        "title": "Python Generators",
        "body": "Генераторы используют yield для последовательного возврата значений",
        "tag": "python",
        "category": "programming",
    },
    {
        "id": 6,
        "title": "HTML Forms",
        "body": "HTML-формы используются для отправки пользовательских данных на сервер",
        "tag": "html",
        "category": "frontend",
    },
    {
        "id": 7,
        "title": "CSS Flexbox",
        "body": "Flexbox позволяет удобно располагать элементы внутри контейнера",
        "tag": "css",
        "category": "frontend",
    },
    {
        "id": 8,
        "title": "JavaScript Events",
        "body": "События позволяют выполнять JavaScript-код в ответ на действия пользователя",
        "tag": "javascript",
        "category": "frontend",
    },
    {
        "id": 9,
        "title": "SQL SELECT",
        "body": "Команда SELECT используется для получения данных из таблицы",
        "tag": "sql",
        "category": "database",
    },
    {
        "id": 10,
        "title": "REST API",
        "body": "REST API позволяет клиенту и серверу обмениваться данными через HTTP",
        "tag": "api",
        "category": "backend",
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

def create_note(*, title:str, body:str, tag:str, category:str) -> dict[str: Any]:
    global _next_id
    note = {
        "id": _next_id,
        "title": title.strip(),
        "body": body.strip(),
        "tag": tag.strip(),
        "category": category.strip(),
    }

    _NOTES.append(note)
    _next_id += 1
    return deepcopy(note)


def delete_note(note_id: int) -> bool:
    pass


def edit_note(
        note_id: int,
        *,
        title:str,
        body:str,
        tag:str, category:str) -> bool:
    pass