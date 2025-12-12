from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from typing import List, Optional
from app.db import Base
import uuid
from datetime import datetime

def generate_uuid():
  return str(uuid.uuid4())

class Vehicle(Base):
  __tablename__ = "vehicles"
  __mapper_args__ = {
    "polymorphic_identity": "vehicle",
    "polymorphic_on": "type"
  }

  id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
  type: Mapped[str] = mapped_column(String, nullable=False) # Discriminator column

  brand: Mapped[str] = mapped_column(String, nullable=False)
  model: Mapped[str] = mapped_column(String, nullable=False)
  year: Mapped[int] = mapped_column(String, nullable=False)

  license_plate: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  color: Mapped[Optional[str]] = mapped_column(String)

class Truck(Vehicle):
  __tablename__ = "trucks"
  __mapper_args__ = {
    "polymorphic_identity": "truck",
  }

  id: Mapped[str] = mapped_column( 
    String,
    ForeignKey("vehicles.id", ondelete="CASCADE"),
    primary_key=True
  )
  max_load_capacity: Mapped[int] = mapped_column(Integer, nullable=False) # in kg
  axles: Mapped[int] = mapped_column(Integer, nullable=False)

class Van(Vehicle):
  __tablename__ = "vans"
  __mapper_args__ = {
    "polymorphic_identity": "van",
  }

  id: Mapped[str] = mapped_column(
    String,
    ForeignKey("vehicles.id", ondelete="CASCADE"),
    primary_key=True
  )
  seating_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
  has_air_conditioning: Mapped[bool] = mapped_column(Boolean, default=False)
 
class Car(Vehicle):
  __tablename__ = "cars"
  __mapper_args__ = {
    "polymorphic_identity": "car"
  }

  id: Mapped[str] = mapped_column(
    String,
    ForeignKey("vehicles.id", ondelete="CASCADE"),
    primary_key=True
  )
  seating_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
  has_air_conditioning: Mapped[bool] = mapped_column(Boolean, default=False)

class Motorcycle(Vehicle):
  __tablename__ = "motorcycles"
  __mapper_args__ = {
    "polymorphic_identity": "motorcycle"
  }

  id: Mapped[str] = mapped_column(
    String,
    ForeignKey("vehicles.id", ondelete="CASCADE"),
    primary_key=True
  )

  engine_capacity: Mapped[int] = mapped_column(Integer, nullable=False) # in cc

class Driver(Base):
  __tablename__ = "drivers"

  # id
  # name
  # whatsapp
  # phone
  # city
  # uf
  # vehicle_type enum whit values 'carro', 'moto', 'caminhonete', 'van', 'caminhão'
  # service_type enum whit values 'passenger', 'cargo', 'both'
  # notes
  # cnh

  id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
  name: Mapped[str] = mapped_column(String, nullable=False)
  phone: Mapped[str] = mapped_column(String, nullable=False)
  whatsapp: Mapped[str] = mapped_column(String, nullable=False)
  city: Mapped[str] = mapped_column(String, nullable=False)
  vehicle_type: Mapped[Optional[str]] = mapped_column(String)
  service_type: Mapped[str] = mapped_column(String) # service: passengers, cargo or both
  notes: Mapped[Optional[str]] = mapped_column(String)

  routes: Mapped["Routes"] = relationship(
    back_populates="driver",
    cascade="all, delete-orphan",
    lazy="selectin"
  )
  photos: Mapped[List["UploadedPhoto"]] = relationship(
    "UploadedPhoto",
    back_populates="driver",
    cascade="all, delete-orphan",
    lazy="selectin"
  )

class UploadedPhoto(Base):
  __tablename__ = "uploaded_photos"

  id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
  filename: Mapped[str] = mapped_column(String, nullable=False)
  filepath: Mapped[str] = mapped_column(String, nullable=False)
  category: Mapped[str] = mapped_column(String, nullable=False)
  content_type: Mapped[str] = mapped_column(String, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
  driver_id: Mapped[str] = mapped_column(
    ForeignKey("drivers.id", ondelete="CASCADE"),
    nullable=False
  )

  driver: Mapped["Driver"] = relationship(
    "Driver", back_populates="photos",
  )

class Routes(Base):
  __tablename__ = "routes"

  id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
  driver_id: Mapped[str] = mapped_column(
    ForeignKey("drivers.id", ondelete="CASCADE"),
    nullable=False
  )

  origin: Mapped[str] = mapped_column(String, nullable=False)
  destination: Mapped[str] = mapped_column(String, nullable=False)
  days: Mapped[Optional[str]] = mapped_column(String)
  time: Mapped[Optional[str]] = mapped_column(String)
  price_per_seat: Mapped[Optional[float]] = mapped_column(Float)
  price_per_cargo: Mapped[Optional[float]] = mapped_column(Float)

  driver: Mapped["Driver"] = relationship(back_populates="routes")
