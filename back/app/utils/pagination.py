# app/utils/pagination.py - ESTILO DJANGO REST FRAMEWORK
import math
from typing import Generic, TypeVar, List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fastapi import Query, Request

T = TypeVar('T')

class PaginationLinks(BaseModel):
    label: str
    page: Optional[int] = None

class PaginationPayload(BaseModel):
    """Payload de paginación idéntico a Django REST"""
    total: int
    page: int
    from_: int = Field(alias="from")  # 'from' es palabra reservada en Python
    last_page: int
    links: List[PaginationLinks]

class PaginationResponse(BaseModel, Generic[T]):
    data: List[T]
    payload: dict

class CustomPagination:
    """Paginación personalizada estilo Django REST Framework"""
    
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        items_per_page: int = Query(10, ge=1, le=100, description="Items per page")
    ):
        self.page = page
        self.items_per_page = min(items_per_page, 100)  # max_page_size = 100
        self.offset = (page - 1) * self.items_per_page

    def paginate(self, data: List[T], total_count: int) -> PaginationResponse[T]:
        """
        Paginate the data and return the response in the format expected by your frontend.
        """
        # Calculate pagination info
        last_page = math.ceil(total_count / self.items_per_page)
        
        # Determine previous and next pages
        previous_page = self.page - 1 if self.page > 1 else None
        next_page = self.page + 1 if self.page < last_page else None
        
        # Build pagination links
        paginador = []
        
        # Previous link
        paginador.append({
            "label": "&laquo; Previous",
            "page": previous_page
        })
        
        # Page numbers
        for pagina in range(1, last_page + 1):
            paginador.append({
                "label": pagina,
                "page": pagina
            })
        
        # Next link
        paginador.append({
            "label": "Next &raquo;",
            "page": next_page
        })
        
        # Build response
        return PaginationResponse(
            data=data,
            payload={
                "pagination": {
                    "total": total_count,
                    "page": self.page,
                    "from": 1,
                    "last_page": last_page,
                    "links": paginador
                }
            }
        )

def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    items_per_page: int = Query(10, ge=1, le=100, description="Items per page")
) -> CustomPagination:
    """
    Dependency to get pagination parameters from query string.
    """
    return CustomPagination(page=page, items_per_page=items_per_page)

