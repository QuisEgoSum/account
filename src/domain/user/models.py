from sqlalchemy import Integer, String, extract
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from src.core.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    email: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(), nullable=False)
    created_at: Mapped[int] = mapped_column(Integer(), nullable=False, server_default=extract('epoch', now()))
