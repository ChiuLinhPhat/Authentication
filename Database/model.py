from sqlalchemy import (
    Boolean,
    Column,
    CursorResult,
    DateTime,
    ForeignKey,
    Identity,
    Insert,
    Integer,
    LargeBinary,
    MetaData,
    Select,
    String,
    Table,
    Update,
    func,
)
from sqlalchemy.dialects.mysql import UUID
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Query
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from typing import Optional, Type
from sqlalchemy.orm import sessionmaker
import jwt
from fastapi_login import LoginManager
from pydantic import BaseModel
from passlib.context import CryptContext
from Settings.config import DB_NAMING_CONVENTION, Settings
from typing import Any
Settings = Settings()
Base = declarative_base()
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

DATABASE_URL = str(Settings.DATABASE_URL)

engine = create_async_engine(DATABASE_URL)
auth_user = Table(
    "auth_user",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)

refresh_tokens = Table(
    "auth_refresh_token",
    metadata,
    Column("uuid", UUID(as_uuid=True), primary_key=True),
    Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
    Column("refresh_token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)


def to_json(self):
    return {
        "id": str(self.Userid),
        # "name": self.Usename,
        "email": self.email,
        "hash_passwords": self.hash_passwords,
        "createdAt": self.createdAt
    }


def to_info(self):
    return {
        "id": str(self.Userid),
        # "username": self.Usename,
        "email": self.email
    }

# Assuming create_db_client() function returns the engine
#
# engine = create_engine(url="mysql+mysqldb://root:@127.0.0.1/blog")
# Session = sessionmaker(bind=engine)
#
#
# class TokenManager:
#     jwt_token_prefix: str = "Token"
#     SECRET_KEY = "8470f8f48d4a2c9a11a1fe9af0e528a43aa70c4e5f69a5556875e6770283cbf8"  # Replace with a secure secret key
#     ALGORITHM = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES = 15
#
#
# manager = LoginManager(TokenManager.jwt_token_prefix, token_url="/Router/login", default_expiry=timedelta(minutes=30),
#                        use_cookie=True)
#
#
# @manager.user_loader()
# def get_user_by_email(username: str) -> Query[Type[Users]]:
#     session = Session()
#     user = session.query(Users).filter_by(username=username).first()
#     session.close()
#     return user
#
#
# async def get_user(username: str) -> Query[Type[Users]]:
#     session = Session()
#     user = session.query(Users).filter_by(username=username).first()
#     session.close()
#     return user
#
#
# class TokenData(BaseModel):
#     Username: str
#
#
# def create_access_token(username: str):
#     payload = {'iat': datetime.utcnow(),
#                'scope': 'access_token',
#                'sub': username}
#
#     return manager.create_access_token(data=payload)
#
#
# def create_refresh_token(username: str):
#     payload = {'iat': datetime.utcnow(),
#                'scope': 'token_refresh',
#                'sub': username}
#
#     return manager.create_access_token(data=payload)
#
# # Add other functions related to authentication if needed
