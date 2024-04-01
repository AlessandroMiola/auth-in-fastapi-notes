from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from basic_auth.src.apis.utils.authenticate import authenticate
from basic_auth.src.crud.user import create_user
from basic_auth.src.db.session import get_session
from basic_auth.src.models.user import UserCreate, UserResponse

router = APIRouter()
security = HTTPBasic()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    user: UserCreate,
    db: Annotated[Session, Depends(get_session)],
) -> UserResponse | None:
    try:
        new_user = await create_user(user=user, db=db)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user.username} already exists.",
        ) from exc
    return new_user


@router.post("/login", response_model=UserResponse)
async def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_session)],
) -> UserResponse | None:
    user = await authenticate(username=credentials.username, password=credentials.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
