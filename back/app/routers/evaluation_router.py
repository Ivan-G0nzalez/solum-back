
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.evaluation_services import EvaluationService
from app.domain.evaluation_models import EvaluationRead, EvaluationCreate, EvaluationUpdate
from app.utils.pagination import get_pagination_params, PaginationResponse
from app.utils.logger import logger

router = APIRouter(
    prefix="/evaluations",
    tags=["evaluations"],
    responses={404: {"description": "Not found"}},
)

def get_evaluation_service() -> EvaluationService:
    return EvaluationService()

@router.get("/", response_model=PaginationResponse[EvaluationRead], summary="Get all evaluations (paginated)")
async def get_evaluations(
    pagination = Depends(get_pagination_params),
    service: EvaluationService = Depends(get_evaluation_service)
):
    """
    Retrieve all evaluations from the database with pagination.
    
    Query Parameters:
        page (int): Page number (default: 1)
        items_per_page (int): Items per page (default: 10, max: 100)

    Returns:
        PaginationResponse[Evaluation]: Paginated list of evaluations
    """
    try:
        evaluations = service.get_evaluations_paginated(pagination)
        return evaluations
    except Exception as e:
        logger.error(f"Error in get_evaluations endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/all", response_model=List[EvaluationRead], summary="Get all evaluations (no pagination)")
async def get_all_evaluations(
    service: EvaluationService = Depends(get_evaluation_service)
):
    """
    Retrieve all evaluations from the database without pagination.
    
    Returns:
        List[Evaluation]: List of all evaluations
    """
    try:
        evaluations = service.get_evaluations()
        return evaluations
    except Exception as e:
        logger.error(f"Error in get_all_evaluations endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{evaluation_id}", response_model=EvaluationRead, summary="Get evaluation by ID")
async def get_evaluation(
    evaluation_id: int,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """
    Retrieve a specific evaluation by its ID.

    Args:
        evaluation_id (int): The ID of the evaluation to retrieve

    Returns:
        Evaluation: The evaluation data

    Raises:
        HTTPException: If evaluation not found
    """
    try:
        evaluation = service.get_evaluation(evaluation_id)
        if evaluation is None:
            raise HTTPException(status_code=404, detail=f"Evaluation with ID {evaluation_id} not found")
        return evaluation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_evaluation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=EvaluationRead, status_code=201, summary="Create new evaluation")
async def create_evaluation(
    evaluation_data: EvaluationCreate,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """
    Create a new evaluation.

    Args:
        evaluation_data (EvaluationCreate): The evaluation data to create

    Returns:
        Evaluation: The created evaluation

    Raises:
        HTTPException: If validation fails or creation error
    """
    try:
        evaluation = service.create_evaluation(evaluation_data)
        return evaluation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in create_evaluation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{evaluation_id}", response_model=EvaluationRead, summary="Update evaluation")
async def update_evaluation(
    evaluation_id: int,
    evaluation_data: EvaluationUpdate,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """
    Update an existing evaluation.

    Args:
        evaluation_id (int): The ID of the evaluation to update
        evaluation_data (EvaluationUpdate): The evaluation data to update

    Returns:
        Evaluation: The updated evaluation

    Raises:
        HTTPException: If evaluation not found or update error
    """
    try:
        evaluation = service.update_evaluation(evaluation_id, evaluation_data)
        if evaluation is None:
            raise HTTPException(status_code=404, detail=f"Evaluation with ID {evaluation_id} not found")
        return evaluation
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in update_evaluation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

@router.delete("/{evaluation_id}", status_code=204, summary="Delete evaluation")
async def delete_evaluation(
    evaluation_id: int,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """
    Delete an evaluation by its ID.

    Args:
        evaluation_id (int): The ID of the evaluation to delete

    Raises:
        HTTPException: If evaluation not found or deletion error
    """
    try:
        success = service.delete_evaluation(evaluation_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Evaluation with ID {evaluation_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_evaluation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")