from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.call_services import CallService
from app.utils.pagination import get_pagination_params, PaginationResponse
from app.domain.call_models import CallRead, CallCreate, CallUpdate
from app.utils.logger import logger

router = APIRouter(
    prefix="/calls",
    tags=["calls"],
    responses={404: {"description": "Not found"}},
)

def get_call_service() -> CallService:
    return CallService()

@router.get("/", response_model=PaginationResponse[CallRead], summary="Get all calls (paginated)")
async def get_calls(
    pagination = Depends(get_pagination_params),
    service: CallService = Depends(get_call_service)
):
    """
    Retrieve all calls from the database with pagination.
    
    Query Parameters:
        page (int): Page number (default: 1)
        items_per_page (int): Items per page (default: 10, max: 100)
    
    Returns:
        PaginationResponse[Call]: Paginated list of calls
    """
    try:
        calls = service.get_calls_paginated(pagination)
        return calls
    except Exception as e:
        logger.error(f"Error in get_calls endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

@router.get("/all", response_model=List[CallRead], summary="Get all calls (no pagination)")
async def get_all_calls(
    service: CallService = Depends(get_call_service)
):
    """
    Retrieve all calls from the database without pagination.
    
    Returns:
        List[Call]: List of all calls
    """
    try:
        calls = service.get_calls()
        return calls
    except Exception as e:
        logger.error(f"Error in get_all_calls endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
@router.get("/{call_id}", response_model=CallRead, summary="Get call by ID")
async def get_call(
    call_id: int,
    service: CallService = Depends(get_call_service)
):
    """
    Retrieve a specific call by its ID.
    
    Args:
        call_id (int): The ID of the call to retrieve
        
    Returns:
        Call: The call data
        
    Raises:
        HTTPException: If call not found
    """
    try:
        call = service.get_call(call_id)
        if call is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Call with ID {call_id} not found"
            )
        return call
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_call endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/", response_model=CallRead, status_code=status.HTTP_201_CREATED, summary="Create new call")
async def create_call(
    call_data: CallCreate,
    service: CallService = Depends(get_call_service)
):
    """
    Create a new call.
    
    Args:
        call_data (CallCreate): The call data to create
        
    Returns:
        Call: The created call
        
    Raises:
        HTTPException: If validation fails or creation error
    """
    try:
        call = service.create_call(call_data)
        return call
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in create_call endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{call_id}", response_model=CallRead, summary="Update call")
async def update_call(
    call_id: int,
    call_data: CallUpdate,
    service: CallService = Depends(get_call_service)
):
    """
    Update an existing call.
    
    Args:
        call_id (int): The ID of the call to update
        call_data (CallUpdate): The call data to update
        
    Returns:
        Call: The updated call
        
    Raises:
        HTTPException: If call not found or update error
    """
    try:
        call = service.update_call(call_id, call_data)
        if call is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Call with ID {call_id} not found"
            )
        return call
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in update_call endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    

@router.delete("/{call_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete call")
async def delete_call(
    call_id: int,
    service: CallService = Depends(get_call_service)
):
    """
    Delete a call by its ID.
    
    Args:
        call_id (int): The ID of the call to delete
        
    Raises:
        HTTPException: If call not found or deletion error
    """
    try:
        success = service.delete_call(call_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Call with ID {call_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_call endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/clinic/{clinic_id}", response_model=PaginationResponse[CallRead], summary="Get calls by clinic (paginated)")
async def get_calls_by_clinic(
    clinic_id: int,
    pagination = Depends(get_pagination_params),
    search: str = None,
    call_type: str = None,
    sort_by: str = "created",
    sort_order: str = "desc",
    service: CallService = Depends(get_call_service)
):
    """
    Retrieve all calls for a specific clinic with pagination, search, filters, and sorting.
    
    Args:
        clinic_id (int): The ID of the clinic to filter calls by
        
    Query Parameters:
        page (int): Page number (default: 1)
        items_per_page (int): Items per page (default: 10, max: 100)
        search (str, optional): Search term to filter by call_id or customer_phone (case-insensitive partial match)
        call_type (str, optional): Filter by call type - "inbound" or "outbound"
        sort_by (str, optional): Field to sort by - "created", "call_start_time", "duration", "call_id" (default: "created")
        sort_order (str, optional): Sort order - "asc" or "desc" (default: "desc")
    
    Returns:
        PaginationResponse[Call]: Paginated list of calls for the clinic
    """
    try:
        # Validate call_type if provided
        if call_type and call_type not in ["inbound", "outbound"]:
            raise HTTPException(
                status_code=400, 
                detail="call_type must be either 'inbound' or 'outbound'"
            )
        
        # Validate sort_order if provided
        if sort_order and sort_order.lower() not in ["asc", "desc"]:
            raise HTTPException(
                status_code=400, 
                detail="sort_order must be either 'asc' or 'desc'"
            )
        
        calls = service.get_calls_by_clinic_with_filters(
            clinic_id=clinic_id,
            pagination=pagination,
            search=search,
            call_type=call_type,
            sort_by=sort_by,
            sort_order=sort_order.lower()
        )
        return calls
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_calls_by_clinic endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")