from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    photo = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, server_default=false(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    is_admin = Column(Boolean, server_default=false(), nullable=False)

    chats = relationship(
        "ChatHistory",
        back_populates="chat_user"  # Link to ChatHistory.chat_user
    )


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now()) 

    chat_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    chat_user = relationship(
        "User",
        back_populates="chats"
    )