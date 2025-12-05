from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine, Base
from .routers import fretes

app = FastAPI(title="Frete app api")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
  from .db import  Base, engine
  from .models import Frete
  
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

app.include_router(fretes.router)

@app.get("/")
def root():
  return {"message": "Frete API Online!"}