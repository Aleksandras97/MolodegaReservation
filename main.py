from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

users = []

class User(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


@app.post("/users/", response_model=User)
def create_user(user: User):
    user.id = uuid4()
    users.append(user)
    return user

@app.get("/users/", response_model=List[User])
def read_users():
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: UUID):
    for user in users:
        if user.id == user_id:
            return user
        
    raise HTTPException(status_code=404, detail="user not found") 


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user_update: User):
    for key, user in enumerate(users):
        if user.id == user_id:
            user_update = user.copy(update=user_update.dict(exclude_unset=True))
            users[key] = user_update
            return user_update
        
    raise HTTPException(status_code=404, detail="user not found") 

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: UUID):
    for key, user in enumerate(users):
        if user.id == user_id:
            return users.pop(key)

    raise HTTPException(status_code=404, detail="user not found") 


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}