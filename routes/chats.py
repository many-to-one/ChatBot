from fastapi import APIRouter, status, Depends, Response, HTTPException

from models.models import ChatHistory
from orm.orm import OrmService
from schemas.chats import AllChatsBase, ChatBase
from schemas.users import UserBase
from db.db import get_db
from settings.security import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["Chats"], prefix="/chats")

@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[AllChatsBase])
async def chats(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    
    __orm = OrmService(db)

    try:
        chats = await __orm.all(ChatHistory, 'chats')
        return chats
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'{e}',
            )
    

@router.get("/get", status_code=status.HTTP_200_OK, response_model=ChatBase)
async def chat(
        id: int,
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    
    __orm = OrmService(db)

    try:
        chat = await __orm.get(id, ChatHistory, 'chat')
        return chat
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'{e}',
            )