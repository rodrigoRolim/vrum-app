import asyncio
from sqlalchemy import select, func, delete
from app.db import AsyncSessionLocal, engine
from app.models import Base, Driver, Routes


async def seed():

  # Criar tabelas se ainda não existirem
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  async with AsyncSessionLocal() as session:

    await session.execute(delete(Driver))
    await session.commit()
    # Verifica se já existem motoristas cadastrados
    result = await session.execute(
      select(func.count()).select_from(Driver)
    )
    total = result.scalar()

    if total > 0:
      print("Seed already inserted")
      return

    # Motoristas e rotas iniciais
    driver1 = Driver(
      name="Carlos Silva",
      phone="98999990000",
      whatsapp="98999990000",
      city="Bacabal - MA",
      vehicle_type="Van",
      service_type="passenger",
      notes="Viagens diárias para São Luís",
      # file=None,
      routes=Routes(
        origin="Bacabal",
        destination="São Luís",
        days="segunda,quarta,sexta",
        time="06:00",
        price_per_seat=80.0,
        price_per_cargo=None,
      )
    )

    driver2 = Driver(
      name="Marcos Fretes",
      phone="98988887777",
      whatsapp="98988887777",
      city="Lago Verde - MA",
      vehicle_type="Caminhonete",
      service_type="cargo",
      notes="Fretes leves até 300kg",
      # file=None,
      routes = Routes(
        origin="Lago Verde",
        destination="Bacabal",
        days="todos",
        time=None,
        price_per_seat=None,
        price_per_cargo=50.0,
      )
    )

    session.add_all([driver1, driver2])
    await session.commit()

  print("Seed inserted successfully!")


if __name__ == "__main__":
  asyncio.run(seed())
