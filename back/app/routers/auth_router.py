from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.utils.auth import create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.dependencies import get_user_service, get_current_user_dependency
from app.domain.user_models import UserResponse
from app.utils.logger import logger

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service = Depends(get_user_service)
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logger.info(f"Login attempt for user: {form_data.username}")
    
    user_model = service.authenticate_user(form_data.username, form_data.password)
    if not user_model:
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_model.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"Successful login for user: {user_model.username}")
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_user_dependency)]
) -> UserResponse:
    """
    Get current user information
    """
    logger.info(f"Retrieving info for user: {current_user.username}")
    return UserResponse.model_validate(current_user.model_dump())

 