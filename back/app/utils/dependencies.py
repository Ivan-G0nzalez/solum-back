from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.services.user_services import UserService
from app.utils.auth import oauth2_scheme, verify_token
from app.domain.user_models import User as UserDomain

def get_user_service() -> UserService:
    return UserService()

async def get_current_user_dependency(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: UserService = Depends(get_user_service)
) -> UserDomain:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if not username:
        raise credentials_exception
    
    user = service.get_user_by_username(username)
    if not user:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user 