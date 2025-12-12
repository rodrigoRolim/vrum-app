from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Optional
from datetime import datetime

class RouteIn(BaseModel):
  origin: str
  destination: str
  days: List[str] = []
  time: Optional[str] = None
  price_per_cargo: Optional[float] = None # turn to only price, cause the type of transportation is implicit on Driver Model (service_cargo or service_passengers)
  price_per_seat: Optional[float] = None # remove
  # it might have the service category (cargo or passengers) and then this category might be removed from driver's schema and model

  @field_validator("days", mode="before")
  def slipt_days(cls, v):
    if isinstance(v, str):
      return v.split(",")
    return v

class RouteOut(RouteIn):
  id: str
  class Config:
    from_attributes = True

class UploadedPhoto(BaseModel):
  id: str
  filename: str
  filepath: str
  category: str
  content_type: str
  created_at: datetime

  class Config:
    from_attributes = True

class DriverCreate(BaseModel):
  name: str
  phone: str
  whatsapp: str
  city: str
  vehicle_type: Optional[str] = None
  service_type: Optional[str] = None
  notes: Optional[str] = None
  file: Optional[str] = None # id to UploadedVehiclePhoto table

class DriverOut(DriverCreate):
  id: str
  routes: RouteOut
  photos: List[UploadedPhoto] = []

  class Config:
    from_attributes = True

class DriverListRoute(BaseModel):
  id: str
  origin: str
  destination: str
  time: str | None = None
  price: float

  class Config:
    from_attributes = True

class DriverListOut(BaseModel):
  id: str
  name: str
  city: str
  vehicle_type: str | None
  service_type: Optional[str] = None
  photo: Optional[HttpUrl] = None
  # for now, it is the first route but will be the searched route
  route: DriverListRoute | None

  class Config:
    from_attributes = True
