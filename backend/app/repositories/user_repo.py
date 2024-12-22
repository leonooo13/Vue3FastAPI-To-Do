import secrets
import string
from datetime import datetime, timezone

from sqlmodel import Session, select, or_
from typing import Optional
from app.models import User
from app.schemas import UserCreate
from app.utils import get_hashed_password, verify_hashed_password

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username_or_email(username)
        if not user:
            return None
        if not verify_hashed_password(plain_password=password, hashed_password=user.password):
            return None
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db_session.get(User, user_id)

    def get_user_by_username_or_email(self, username: str) -> Optional[User]:
        result = self.db_session.exec(
            select(User).where(or_(User.username == username, User.email == username)),
        )
        return result.one_or_none()

    def get_user_by_username(self, username: str) -> Optional[User]:
        result = self.db_session.exec(
            select(User).where(User.username == username)
        )
        return result.one_or_none()

    def get_user_by_email(self, email: str) -> Optional[User]:
        result = self.db_session.exec(select(User).where(User.email == email))
        return result.one_or_none()

    def create_user(self, user_schema: UserCreate) -> User:
        hashed_password = get_hashed_password(user_schema.password)
        user = User(
            email=user_schema.email,
            name=user_schema.name,
            username=user_schema.username,
            password=hashed_password,
        )
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def delete_user_by_id(self, user_id: int) -> bool:
        user = self.db_session.get(User, user_id)
        if not user:
            return False
        self.db_session.delete(user)
        self.db_session.commit()
        return True

    def update_user_last_login(self, user: User) -> None:
        user.last_login = datetime.now(timezone.utc)
        self.db_session.commit()