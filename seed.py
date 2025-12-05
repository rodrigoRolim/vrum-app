import asyncio
from frete_facil_app.db import AsyncSessionLocal, Base, engine
from frete_facil_app.models import Frete
from sqlalchemy import select

async def seed():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  

  async with AsyncSessionLocal() as session:
    exists = await session.execute(
      select(Frete)
    )
    
    if exists.scalars().first():
      print("Seed already inserted")
      return
    
    fretes = [
      Frete(name="Lin Fretes", description="Fretes para todo o maranhão", origin="Lago verde, MA", destiny="Bacabal, MA", type_vehicle="carreta", price=200),
      Frete(name="Fretisa", description="Fretes no nordeste", origin="São luis, MA", destiny="Salvador, BA", type_vehicle="van", price=1200),
    ]

    session.add_all(fretes)
    await session.commit()
  print("Seed inserted")

if __name__ == "__main__":
  asyncio.run(seed())