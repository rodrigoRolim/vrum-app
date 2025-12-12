from enum import Enum

class PhotoCategory(str, Enum):
  VEHICLES = "vehicles"
  PROFILES = "profiles"

class ServiceType(str, Enum):
  PASSENGER = "passenger"
  CARGO = "cargo"
  BOTH = "both"

class VehicleType(str, Enum):
  VAN = "van" 
  CAR = "car"
  MOTORCYCLE = "motorcycle"
  PICKUP_TRUCK = "pickup_truck"
  TRUCK = "truck"