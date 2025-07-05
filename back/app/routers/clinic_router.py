from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.clinic_services import ClinicService
from app.domain.models import Clinic, ClinicCreate, ClinicUpdate
from app.utils.logger import logger
from app.utils.pagination import get_pagination_params, PaginationResponse

# Create router with prefix and tags
router = APIRouter(
    prefix="/clinics",
    tags=["clinics"],
    responses={404: {"description": "Not found"}},
)

# Dependency injection for service
def get_clinic_service() -> ClinicService:
    return ClinicService()

@router.get("/", response_model=PaginationResponse[Clinic], summary="Get all clinics (paginated)")
async def get_clinics(
    pagination = Depends(get_pagination_params),
    service: ClinicService = Depends(get_clinic_service)
):
    """
    Retrieve all clinics from the database with pagination.
    
    Query Parameters:
        page (int): Page number (default: 1)
        items_per_page (int): Items per page (default: 10, max: 100)
    
    Returns:
        PaginationResponse[Clinic]: Paginated list of clinics
    """
    try:
        clinics = service.get_clinics_paginated(pagination)
        return clinics
    except Exception as e:
        logger.error(f"Error in get_clinics endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/all", response_model=List[Clinic], summary="Get all clinics (no pagination)")
async def get_all_clinics(
    service: ClinicService = Depends(get_clinic_service)
):
    """
    Retrieve all clinics from the database without pagination.
    
    Returns:
        List[Clinic]: List of all clinics
    """
    try:
        clinics = service.get_clinics()
        return clinics
    except Exception as e:
        logger.error(f"Error in get_all_clinics endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{clinic_id}", response_model=Clinic, summary="Get clinic by ID")
async def get_clinic(
    clinic_id: int,
    service: ClinicService = Depends(get_clinic_service)
):
    """
    Retrieve a specific clinic by its ID.
    
    Args:
        clinic_id (int): The ID of the clinic to retrieve
        
    Returns:
        Clinic: The clinic data
        
    Raises:
        HTTPException: If clinic not found
    """
    try:
        clinic = service.get_clinic(clinic_id)
        if clinic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clinic with ID {clinic_id} not found"
            )
        return clinic
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_clinic endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/", response_model=Clinic, status_code=status.HTTP_201_CREATED, summary="Create new clinic")
async def create_clinic(
    clinic_data: ClinicCreate,
    service: ClinicService = Depends(get_clinic_service)
):
    """
    Create a new clinic.
    
    Args:
        clinic_data (ClinicCreate): The clinic data to create
        
    Returns:
        Clinic: The created clinic
        
    Raises:
        HTTPException: If validation fails or creation error
    """
    try:
        clinic = service.create_clinic(clinic_data)
        return clinic
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in create_clinic endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{clinic_id}", response_model=Clinic, summary="Update clinic")
async def update_clinic(
    clinic_id: int,
    clinic_data: ClinicUpdate,
    service: ClinicService = Depends(get_clinic_service)
):
    """
    Update an existing clinic.
    
    Args:
        clinic_id (int): The ID of the clinic to update
        clinic_data (ClinicUpdate): The clinic data to update
        
    Returns:
        Clinic: The updated clinic
        
    Raises:
        HTTPException: If clinic not found or update error
    """
    try:
        clinic = service.update_clinic(clinic_id, clinic_data)
        if clinic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clinic with ID {clinic_id} not found"
            )
        return clinic
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in update_clinic endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete("/{clinic_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete clinic")
async def delete_clinic(
    clinic_id: int,
    service: ClinicService = Depends(get_clinic_service)
):
    """
    Delete a clinic by its ID.
    
    Args:
        clinic_id (int): The ID of the clinic to delete
        
    Raises:
        HTTPException: If clinic not found or deletion error
    """
    try:
        success = service.delete_clinic(clinic_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clinic with ID {clinic_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_clinic endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 