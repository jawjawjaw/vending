from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security import get_password_hash
from app.db.sql.models import User
from app.schemas.requests import UserCreateRequest, UserUpdateRequest
from app.schemas.responses import UserResponse

router = APIRouter()


@router.get("", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(deps.get_current_user),
):
    """Get current user"""
    return UserResponse.model_validate(current_user)


@router.delete("", status_code=204)
async def delete_current_user(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Delete current user"""
    await session.execute(delete(User).where(User.id == current_user.id))
    await session.commit()


@router.patch("", status_code=201)
async def update_current_user(
    update_user_request: UserUpdateRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Update current user"""
    await session.execute(
        update(User)
        .where(User.id == current_user.id)
        .values(**update_user_request.model_dump())
    )
    await session.commit()


@router.post("", response_model=UserResponse)
async def register_new_user(
    new_user: UserCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Create new user"""
    result = await session.execute(
        select(User).where(User.username == new_user.username)
    )
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Cannot use this username")
    user = User(
        username=new_user.username,
        password=get_password_hash(new_user.password),
        role=new_user.role,
    )
    session.add(user)
    await session.commit()

    return UserResponse.model_validate(user)
