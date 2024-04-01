from sqlmodel import Session

from basic_auth.src.apis.utils.security import verify_password
from basic_auth.src.crud.user import get_user
from basic_auth.src.models.user import User


async def authenticate(username: str, password: str, db: Session) -> User | None:
    user = await get_user(username=username, db=db)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
