from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, List

from app.services.user_services import UserService
from app.domain.user_models import UserCreate, UserUpdate, UserResponse
from app.utils.pagination import get_pagination_params, PaginationResponse, CustomPagination
from app.utils.dependencies import get_user_service, get_current_user_dependency
from app.utils.logger import logger

router = APIRouter(prefix="/users", tags=["users"])



# Register
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    service = Depends(get_user_service)
):
    logger.info("Received request to register user")
    try:
        user = service.create_user(user_data)
        return UserResponse.model_validate(user.model_dump())
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get users paginated
@router.get("/", response_model=PaginationResponse[UserResponse])
async def get_users(
    pagination: CustomPagination = Depends(get_pagination_params),
    service = Depends(get_user_service)
):
    logger.info(f"Retrieving paginated users: page {pagination.page}")
    try:
        paginated_response = service.get_users_paginated(pagination)
        # Convert domain users to UserResponse models
        user_responses = [UserResponse.model_validate(user.model_dump()) for user in paginated_response.data]
        return PaginationResponse(
            data=user_responses,
            payload=paginated_response.payload
        )
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service = Depends(get_user_service)
):
    logger.info(f"Retrieving user by ID: {user_id}")
    try:
        user = service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user.model_dump())
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Update user
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_user_dependency)],
    service = Depends(get_user_service)
):
    logger.info(f"Updating user ID: {user_id}")
    try:
        user = service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user.model_dump())
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Delete user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user_dependency)],
    service = Depends(get_user_service)
):
    logger.info(f"Deleting user ID: {user_id}")
    try:
        success = service.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
