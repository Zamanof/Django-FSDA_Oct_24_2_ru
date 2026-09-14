from pydantic import ValidationError

from schemas import BookCreate, AuthorCreate, UserRegister


def show(title, data, schema):
    print(f"\n=== {title} ===")
    try:
        obj = schema.model_validate(data)
        print("Ok", obj.model_dump())
    except ValidationError as e:
        print("ValidationError", e)


if __name__ == "__main__":
    show("Book ok", {"title": "War and Peace", 'pages':1223, "author_id": 1}, BookCreate)
    show("Book with 0 pages", {"title": "Bad", 'pages':0, "author_id": 1}, BookCreate)
    show("Author ok", {'name': "Leo Tolstoy"}, AuthorCreate)
    show("Empty author", {'name': ""}, AuthorCreate)
    show("Short password", {"email":"a@b.com", "password": "123"}, UserRegister)


