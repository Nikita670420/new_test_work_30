from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from typing import List

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    cooking_time: Mapped[int] = mapped_column(Integer)
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(Text)
    ingredients: Mapped[List[str]] = mapped_column(Text)
