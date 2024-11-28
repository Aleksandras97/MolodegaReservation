import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.user import User
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" # "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.post('/users/', json={"name": "test_name"})
    assert response.status_code == 201
    assert response.json()["name"] == "test_name"

@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        create_res = await ac.post('/users/', json={"name": "test_name"})
        user_id = create_res.json()["id"]
        response = await ac.get(f"/users/{user_id}")
        
    # async with AsyncClient(app=app, base_url='http://test') as ac:

    assert response.status_code == 200
    assert response.json()["name"] == "test_name"


@pytest.mark.asyncio
async def test_update_user():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        res = await ac.post('/users/', json={"name": "test_name"})
        user_id = res.json()["id"]
        response = await ac.put(f"/users/{user_id}", json={"name": "updated_user"})
    assert response.status_code == 200
    assert response.json()["name"] == "updated_user"

@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        res = await ac.post('/users/', json={"name": "test_name"})
        user_id = res.json()["id"]

        delete_response = await ac.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    async with AsyncClient(app=app, base_url='http://test') as ac:
        get_res = await ac.get(f"/users/{user_id}")
    assert get_res.status_code == 404