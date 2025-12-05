from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db import get_session
from ..models import Frete
from ..schemas import FreteCreate, FreteRead


router = APIRouter(prefix="/fretes", tags=["Fretes"])

@router.post("", response_model=FreteRead)
async def create_frete(data: FreteCreate, db: AsyncSession = Depends(get_session)):
  frete = Frete(**data.dict())
  db.add(frete)
  await db.commit()
  await db.refresh(frete)
  return frete

@router.get("", response_model=list[FreteRead])
async def list_fretes(
  origin: str | None = None,
  destiny: str | None = None,
  db: AsyncSession = Depends(get_session)
):
  query = select(Frete)

  if origin:
    query = query.where(Frete.origin.ilike(f"%{origin}%"))
  if destiny:
    query = query.where(Frete.destiny.ilike(f"%{destiny}%"))

  result = await db.execute(query)
  return result.scalars().all()