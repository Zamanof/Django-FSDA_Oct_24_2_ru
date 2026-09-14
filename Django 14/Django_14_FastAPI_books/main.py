from fastapi import FastAPI
import models

from database import Base, engine
from routers import authors_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Book API")

app.include_router(authors_router)