from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app import models, schemas

import os
import uuid

router = APIRouter(prefix="/drivers", tags=["drivers"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/create", response_model=schemas.DriverOut, status_code=201)
async def create_driver(
  driver_in: schemas.DriverCreate, 
  route_in: schemas.RouteIn, 
  db: AsyncSession = Depends(get_db)
):
  if not (driver_in.service_type):
    raise HTTPException(404, "Driver must offer passengers or cargo services")
  if not (route_in.price_per_cargo or route_in.price_per_seat):
    raise HTTPException(404, "At least one price must be provided: price_per_cargo or price_per_seat")
  
  # Create SQLAlchemy object
  # db_file = models.UploadedVehiclePhoto(
  #   filename=file.filename,
  #   filepath=file_path,
  #   content_type=file.content_type,
  # )

  driver = models.Driver(
    name=driver_in.name,
    phone=driver_in.phone,
    whatsapp=driver_in.whatsapp,
    city=driver_in.city,
    vehicle_type=driver_in.vehicle_type,
    service_type=driver_in.service_type,
    notes=driver_in.notes,
    # file=None,
  )

  route = models.Routes(
    origin=route_in.origin,
    destination=route_in.destination,
    days=",".join(route_in.days),
    time=route_in.time,
    price_per_cargo=route_in.price_per_cargo,
    price_per_seat=route_in.price_per_seat,
  )

  driver.routes = route
  db.add(driver)
  await db.commit()
  await db.refresh(driver)

  return driver

@router.post("/{driver_id}/vehicle_photo", response_model=schemas.UploadedPhoto)
async def upload_vehicle_photo(driver_id: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
  driver = await db.get(models.Driver, driver_id)
  if not driver:
    raise HTTPException(status_code=404, detail="Driver not found")
  
  # save file to disk
  # drivers photos will be saved as: uploads/{driver_id}.ext
  # drivers has none or many photos. Photo has only one driver associated
  # gera diretório por driver
  driver_dir = f"{UPLOAD_DIR}/vehicles/{driver_id}"
  os.makedirs(driver_dir, exist_ok=True)

  # nome único
  ext = os.path.splitext(file.filename)[1]
  unique_name = f"{uuid.uuid4()}{ext}"

  file_location = f"{driver_dir}/{unique_name}"

  # salva no disco
  with open(file_location, "wb") as f:
    f.write(await file.read())

  # salva no banco
  vehicle_photo = models.UploadedPhoto(
    filename=file.filename,
    filepath=file_location,
    category="vehicles",
    content_type=file.content_type,
    driver_id=driver_id,
  )
  db.add(vehicle_photo)
  await db.commit()
  await db.refresh(vehicle_photo)
  
  return vehicle_photo

@router.get("/list", response_model=list[schemas.DriverOut])
async def list_drivers(db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(models.Driver))
  drivers = result.scalars().unique().all()
  return drivers
