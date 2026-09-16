from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from deps import require_roles, get_db
from helpers import paginate
from models import Author, Role
from schemas import AuthorOut, AuthorCreate, AuthorUpdate

router = APIRouter(prefix="/api/authors", tags=["authors"])


@router.post(
    "/",
    response_model=AuthorOut,
    dependencies= [Depends(require_roles(Role.admin))],
    status_code = status.HTTP_201_CREATED,
)
async def create_author(payload:AuthorCreate, db: Session = Depends(get_db)):
    if db.query(Author).filter_by(name=payload.name).first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists!")
    author = Author(name=payload.name.strip())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@router.get('/', response_model=dict, status_code=status.HTTP_200_OK)
async def list_authors(
        q: Optional[str] = Query(None),
        order: str = Query("name"),
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db),
):
    query = db.query(Author).options(joinedload(Author.books))
    if q:
        query = query.filter(Author.name.ilike(f"%{q}%"))
    allowed = {'name', 'id'}
    if order.lstrip('-') not in allowed:
        order = 'name'

    col = getattr(Author, order.lstrip('-'))
    if order.startswith('-'):
        col = col.desc()

    query = query.order_by(col)

    data = paginate(query, page=page, size=size)
    data["results"] = [AuthorOut.model_validate(a) for a in data["results"]]
    return data

@router.get('/{author_id}', response_model=AuthorOut, status_code=status.HTTP_200_OK)
async def get_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = db.query(Author).options(joinedload(Author.books)).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.patch(
    "/{author_id}",
    response_model=AuthorOut,
    dependencies=[Depends(require_roles(Role.admin))],
    status_code=status.HTTP_200_OK)
async def update_author(
        author_id: int,
        payload: AuthorUpdate,
        db: Session = Depends(get_db),
):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    author.name = payload.name.strip()
    db.commit()
    db.refresh(author)
    return author


@router.delete(
    "/{author_id}",
    dependencies=[Depends(require_roles(Role.admin))],
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
        author_id: int,
        db: Session = Depends(get_db),
):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return None
