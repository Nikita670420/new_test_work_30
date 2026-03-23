from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_session, create_tables
from models import Recipe
from schemas import RecipeList, RecipeDetail, RecipeCreate
import json

app = FastAPI(
    title="Кулинарная книга API",
    description="Асинхронный сервис рецептов. GET /recipes — список с сортировкой по популярности (views_count DESC, cooking_time ASC). GET /recipes/{id} — детали. POST /recipes — создание.",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    await create_tables()


@app.get("/recipes", response_model=List[RecipeList])
async def get_recipes(session: AsyncSession = Depends(get_session)):
    """
    Получить список всех рецептов.
    Сортировка: по убыванию популярности (views_count), затем по времени готовки (ASC).
    Для фронтенда: используйте для таблицы с колонками name, views_count, cooking_time.
    """
    stmt = select(Recipe).order_by(desc(Recipe.views_count), Recipe.cooking_time)
    result = await session.execute(stmt)
    recipes = result.scalars().all()
    return recipes


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe_detail(recipe_id: int, session: AsyncSession = Depends(get_session)):
    """
    Получить детальную информацию о рецепте.
    Автоматически увеличивает views_count.
    Поля: name, cooking_time, ingredients (список), description.
    """
    stmt = select(Recipe).where(Recipe.id == recipe_id)
    result = await session.execute(stmt)
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    recipe.views_count += 1
    await session.commit()
    await session.refresh(recipe)

    ingredients = json.loads(recipe.ingredients) if recipe.ingredients else []
    return RecipeDetail(
        id=recipe.id,
        name=recipe.name,
        cooking_time=recipe.cooking_time,
        ingredients=ingredients,
        description=recipe.description
    )


@app.post("/recipes", response_model=RecipeDetail, status_code=201)
async def create_recipe(recipe_data: RecipeCreate, session: AsyncSession = Depends(get_session)):
    """
    Создать новый рецепт.
    Валидация: name (1-255 символов), cooking_time (>0), ingredients (>=1), description (>=10 символов).
    Ингредиенты сохраняются как JSON для простоты.
    """
    if len(recipe_data.ingredients) < 1:
        raise HTTPException(status_code=422, detail="ingredients: минимум 1 элемент")

    recipe = Recipe(
        name=recipe_data.name,
        cooking_time=recipe_data.cooking_time,
        description=recipe_data.description,
        ingredients=json.dumps(recipe_data.ingredients)
    )
    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)

    ingredients = recipe_data.ingredients
    return RecipeDetail(
        id=recipe.id,
        name=recipe.name,
        cooking_time=recipe.cooking_time,
        ingredients=ingredients,
        description=recipe.description
    )
