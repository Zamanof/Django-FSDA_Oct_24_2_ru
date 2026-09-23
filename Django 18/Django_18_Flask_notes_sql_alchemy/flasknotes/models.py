from datetime import datetime

from sqlalchemy import String, Text, func, DateTime, ForeignKey, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flasknotes.extensions import db


class User(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    notes: Mapped[list["Note"]] = relationship(back_populates='author')


class Note(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship(back_populates='notes')