from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.db import get_session
from app.goods.models.goods import Goods, GoodsCreate, GoodsUpdate
from app.utils.logger import log_success, log_error, log_info

router = APIRouter(
    prefix="/goods",
    tags=["goods"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Goods, status_code=status.HTTP_201_CREATED)
async def create_goods(
    goods: GoodsCreate, session: AsyncSession = Depends(get_session)
):
    db_goods = Goods(**goods.model_dump())
    session.add(db_goods)
    await session.commit()
    await session.refresh(db_goods)
    log_success(f"Создан товар с ID {db_goods.id}")
    return db_goods


@router.get("/", response_model=List[Goods])
async def read_goods(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    query = select(Goods).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{goods_id}", response_model=Goods)
async def read_goods_by_id(goods_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Goods).where(Goods.id == goods_id)
    result = await session.execute(query)
    goods = result.scalar_one_or_none()
    if goods is None:
        log_error(f"Товар с ID {goods_id} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goods not found"
        )
    log_success(f"Товар с ID {goods_id} успешно получен")
    return goods


@router.put("/{goods_id}", response_model=Goods)
async def update_goods(
    goods_id: int, goods: GoodsUpdate, session: AsyncSession = Depends(get_session)
):
    log_info(f"Запрос на обновление товара с ID {goods_id}")

    query = select(Goods).where(Goods.id == goods_id)
    result = await session.execute(query)
    db_goods = result.scalar_one_or_none()

    if db_goods is None:
        log_error(f"Товар с ID {goods_id} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goods not found"
        )

    goods_data = goods.model_dump(exclude_unset=True)
    for key, value in goods_data.items():
        setattr(db_goods, key, value)
        log_info(f"Обновлено поле `{key}` → {value}")

    await session.commit()
    await session.refresh(db_goods)

    log_success(f"Товар с ID {goods_id} успешно обновлён")
    return db_goods


@router.delete("/{goods_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goods(goods_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Goods).where(Goods.id == goods_id)
    result = await session.execute(query)
    db_goods = result.scalar_one_or_none()
    if db_goods is None:
        log_error(f"Ошибка при удалении товара с ID {goods_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goods not found"
        )

    await session.delete(db_goods)
    await session.commit()
    log_success(f"Товар с ID {goods_id} успешно удалён")
    return None
