from fastapi import FastAPI
from app.routers import user, telegram, book, reservation
from app.database import engine, Base
import uvicorn
from app.bot import create_bot_app

Base.metadata.create_all(bind=engine)

bot_app = create_bot_app()

app = FastAPI()
app.include_router(user.router)
app.include_router(telegram.router)
app.include_router(book.router)
app.include_router(reservation.router, prefix="/reservations", tags=["reservations"])

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0', port=8000)