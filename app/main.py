from typing import Union
from fastapi import FastAPI
from app.routers import user, telegram
from app.database import engine, Base
import uvicorn

app = FastAPI()

# included the user router for user API calls
app.include_router(user.router)
app.include_router(telegram.router)

Base.metadata.create_all(bind=engine)

@app.get('/')
def read_root():
    return {"message": "Mldg Reservation system"}

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0', port=8000)