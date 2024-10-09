from typing import Union

from fastapi import FastAPI
from app.routers import user
from app.database import engine, Base

app = FastAPI()

# included the user router for user API calls
app.include_router(user.router)

Base.metadata.create_all(bind=engine)

@app.get('/')
def read_root():
    return {"message": "Mldg Reservation system"}