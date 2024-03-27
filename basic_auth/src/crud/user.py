from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from basic_auth.src.apis.utils.security import get_password_hash
from basic_auth.src.models.user import User, UserCreate


async def create_user(user: UserCreate, db: Session) -> User:
    hashed_password = get_password_hash(user.password)
    user_obj = User(**user.model_dump(), hashed_password=hashed_password)
    db.add(user_obj)
    await db.commit()
    await db.refresh(user_obj)
    return user_obj


async def get_user(username: str, db: Session) -> User | None:
    return db.get(entity=User, ident=username)
