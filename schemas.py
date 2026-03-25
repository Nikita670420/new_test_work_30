from typing import List

from pydantic import BaseModel, ConfigDict, Field


class RecipeList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    views_count: int = Field(description="Количество просмотров (популярности)")
    cooking_time: int = Field(description="Время готовки в минутах")


class RecipeDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(min_length=1, description="Название рецепта")
    cooking_time: int = Field(gt=0, description="Время готовки в минутах")
    ingredients: List[str]
    description: str = Field(min_length=10, description="Подробное описание")


class RecipeCreate(BaseModel):
    model_config = ConfigDict()

    name: str = Field(min_length=1, max_length=255, description="Название рецепта")
    cooking_time: int = Field(gt=0, le=1000, description="Время готовки в минутах")
    ingredients: List[str]  # ← УБРАЛ Field() полностью!
    description: str = Field(min_length=10, max_length=5000, description="Описание")
