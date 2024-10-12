from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post('/webhook')
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    if 'channel_post' in data:
        # A new message in the channel
        channel_post = data['channel_post']
        new_member = channel_post.get('new_chat_members')

        if new_member:
            users = []
            # Extract information about the new user
            for member in new_member:
                user_id = str(member['id'])
                username = member.get('username', 'NoUserName')

                crud.get_user_by_id(db, user_id)
                if user_id:
                    continue

                user = schemas.UserCreate(id=user_id, name=username)

                #register the user
                user = crud.create_user(db, user)
                users.append(user)
            
            return users

    return {"detail": "No Users found"}