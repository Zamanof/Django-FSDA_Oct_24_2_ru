from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from deps import require_roles, get_db
from models import Author, Role
from schemas import AuthorOut, AuthorCreate

router = APIRouter(prefix="/api/authors", tags=["authors"])


@router.post(
    "/",
    response_model=AuthorOut,
    dependencies= [Depends(require_roles(Role.admin))],
    status_code = status.HTTP_201_CREATED,
)
def create_author(payload:AuthorCreate, db: Session = Depends(get_db)):
    if db.query(Author).filter_by(name=payload.name).first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists!")
    author = Author(name=payload.name.strip())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author