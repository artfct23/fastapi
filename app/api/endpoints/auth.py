from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.db.user import User
from app.models.schemas.auth import UserCreate, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
        user_data: UserCreate,
        session: AsyncSession = Depends(db.get_db),
):
    result = await session.execute(
        select(User).where(User.username == user_data.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    access_token = create_access_token(user_id=new_user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login", response_model=Token)
async def login(
        username: str,
        password: str,
        session: AsyncSession = Depends(db.get_db),
):

    result = await session.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(user_id=user.id)
    return Token(access_token=access_token, token_type="bearer")
