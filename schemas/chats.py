from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class AllChatsBase(BaseModel):
    id: int
    chat_user: int

class ChatBase(BaseModel):
    id: int
    user_input: str
    response_text: str
    timestamp: datetime
    chat_user: int