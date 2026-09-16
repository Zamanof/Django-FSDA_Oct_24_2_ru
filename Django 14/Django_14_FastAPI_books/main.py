from fastapi import FastAPI
import models

from database import Base, engine
from routers import authors_router, books_router, auth_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Book API")

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(auth_router)