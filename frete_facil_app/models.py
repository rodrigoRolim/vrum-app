from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from .db import Base

class Frete(Base):
  __tablename__ = "fretes"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String, index=True)
  description: Mapped[str | None] = mapped_column(String, nullable=True)
  origin: Mapped[str] = mapped_column(String(100))
  destiny: Mapped[str] = mapped_column(String(100))
  type_vehicle: Mapped[str] = mapped_column(String(50))
  price: Mapped[float] = mapped_column(Float)