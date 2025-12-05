from pydantic import BaseModel

class FreteBase(BaseModel):
  name: str
  description: str
  origin: str
  destiny: str
  type_vehicle: str
  price: float

class FreteCreate(FreteBase):
  pass

class FreteRead(FreteBase):
  id: int