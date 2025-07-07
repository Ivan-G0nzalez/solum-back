from sqlalchemy.orm import Session, joinedload
from app.data_acess.models import Call, Evaluation
from app.repositories.repository import AbtractRepository
from app.utils.logger import logger
from app.domain.call_models import CallCreate, CallUpdate
from typing import List, Optional


class CallRepository(AbtractRepository):
    def __init__(self, session: Session) -> None:
        self.__session = session
    
    def list(self) -> List[Call]:
        logger.info("Fetching all calls from the database")
        try:
            calls = self.__session.query(Call)\
                .options(
                    joinedload(Call.evaluations),
                    joinedload(Call.clinic)  # Cargar también la clínica
                )\
                .all()
            return calls
        except Exception as e:
            logger.error(f"Failed to fetch all calls: {e}")
            raise
    
    def list_paginated(self, offset: int, limit: int) -> List[Call]:
        logger.info(f"Fetching paginated calls (offset={offset}, limit={limit})")
        try:
            return self.__session.query(Call)\
                .options(
                    joinedload(Call.evaluations),
                    joinedload(Call.clinic)
                )\
                .offset(offset)\
                .limit(limit)\
                .all()
        except Exception as e:
            logger.error(f"Failed to fetch paginated calls: {e}")
            raise
    
    def list_by_clinic(self, clinic_id: int) -> List[Call]:
        logger.info(f"Fetching all calls for clinic ID {clinic_id}")
        try:
            calls = self.__session.query(Call)\
                .options(
                    joinedload(Call.evaluations),
                    joinedload(Call.clinic)
                )\
                .filter(Call.clinic_id == clinic_id).all()
            return calls
        except Exception as e:
            logger.error(f"Failed to fetch calls for clinic {clinic_id}: {e}")
            raise
    
    def list_by_clinic_paginated(self, clinic_id: int, offset: int, limit: int) -> List[Call]:
        logger.info(f"Fetching paginated calls for clinic ID {clinic_id} (offset={offset}, limit={limit})")
        try:
            return self.__session.query(Call)\
                .options(
                    joinedload(Call.evaluations),
                    joinedload(Call.clinic)
                )\
                .filter(Call.clinic_id == clinic_id).offset(offset).limit(limit).all()
        except Exception as e:
            logger.error(f"Failed to fetch paginated calls for clinic {clinic_id}: {e}")
            raise

    def count(self) -> int:
        logger.info("Counting total calls")
        try:
            return self.__session.query(Call).count()
        except Exception as e:
            logger.error(f"Failed to count calls: {e}")
            raise

    
    def get(self, call_id: int) -> Optional[Call]:
        logger.info(f"Fetching call with ID {call_id}")
        try:
            call = self.__session.query(Call)\
                .options(joinedload(Call.evaluations),
                    joinedload(Call.clinic))\
                .filter(Call.id == call_id)\
                .first()
            return call
        except Exception as e:
            logger.error(f"Failed to fetch call {call_id}: {e}")
            raise

    def get_by_call_id(self, call_id: str) -> Optional[Call]:
        logger.info(f"Fetching call with call_id {call_id}")
        try:
            call = self.__session.query(Call)\
                .options(joinedload(Call.evaluations),
                    joinedload(Call.clinic))\
                .filter(Call.call_id == call_id)\
                .first()
            return call
        except Exception as e:
            logger.error(f"Failed to fetch call with call_id {call_id}: {e}")
            raise
    
    
    def add(self, call_create: CallCreate) -> Call:
        logger.info("Adding a new call to the database")
        try:
            # Convert Pydantic model to ORM model
            call_data = call_create.model_dump()
            call = Call(**call_data)

            self.__session.add(call)
            self.__session.commit()
            self.__session.refresh(call)
            
            logger.info(f"Call created successfully with ID {call.id}")
            return call
        except Exception as e:
            self.__session.rollback()
            logger.error(f"Failed to add call: {e}")
            raise

    def create(self, call_data: dict) -> Call:
        logger.info("Creating a new call from dictionary data")
        try:
            call = Call(**call_data)
            self.__session.add(call)
            self.__session.flush()  # Flush to get the ID
            self.__session.refresh(call)
            
            logger.info(f"Call created successfully with ID {call.id}")
            return call
        except Exception as e:
            logger.error(f"Failed to create call: {e}")
            raise

    def update(self, call_id: int, call_data: dict) -> Optional[Call]:
        logger.info(f"Updating call with ID {call_id}")
        try:
            call = self.get(call_id)
            if not call:
                return None
            for key, value in call_data.items():
                setattr(call, key, value)
            self.__session.commit()
            self.__session.refresh(call)
            return call
        except Exception as e:
            self.__session.rollback()
            logger.error(f"Failed to update call: {e}")
            raise

    def delete(self, call_id: int) -> bool:
        logger.info(f"Deleting call with ID {call_id}")
        try:
            call = self.get(call_id)
            if not call:
                logger.warning(f"Call with ID {call_id} not found for deletion")
                return False
            self.__session.delete(call)
            self.__session.commit()
            logger.info(f"Call with ID {call_id} deleted successfully")
            return True
        except Exception as e:
            self.__session.rollback()
            logger.error(f"Failed to delete call: {e}")
            raise
    
    def count_by_clinic(self, clinic_id: int) -> int:
        logger.info(f"Counting total calls for clinic ID {clinic_id}")
        try:
            return self.__session.query(Call).filter(Call.clinic_id == clinic_id).count()
        except Exception as e:
            logger.error(f"Failed to count calls for clinic {clinic_id}: {e}")
            raise

    def search_by_clinic_with_filters(
        self, 
        clinic_id: int, 
        search_term: str = None,
        call_type: str = None,
        sort_by: str = "created",
        sort_order: str = "desc",
        offset: int = 0,
        limit: int = 10
    ) -> List[Call]:
        """
        Search calls by clinic with filters, search, and sorting
        
        Args:
            clinic_id: ID of the clinic
            search_term: Search in call_id or customer_phone
            call_type: Filter by call type (inbound/outbound)
            sort_by: Field to sort by (created, call_start_time, duration, etc.)
            sort_order: asc or desc
            offset: Pagination offset
            limit: Pagination limit
        """
        logger.info(f"Searching calls for clinic {clinic_id} with filters: search={search_term}, type={call_type}, sort={sort_by} {sort_order}")
        
        try:
            query = self.__session.query(Call)\
                .options(
                    joinedload(Call.evaluations),
                    joinedload(Call.clinic)
                )\
                .filter(Call.clinic_id == clinic_id)
            
            # Apply search filter
            if search_term:
                query = query.filter(
                    (Call.call_id.ilike(f"%{search_term}%")) |
                    (Call.customer_phone.ilike(f"%{search_term}%"))
                )
            
            # Apply call type filter
            if call_type:
                query = query.filter(Call.call_type == call_type)
            
            # Apply sorting
            sort_field = getattr(Call, sort_by, Call.created)
            if sort_order.lower() == "desc":
                query = query.order_by(sort_field.desc())
            else:
                query = query.order_by(sort_field.asc())
            
            # Apply pagination
            query = query.offset(offset).limit(limit)
            
            calls = query.all()
            logger.info(f"Found {len(calls)} calls matching criteria")
            return calls
        except Exception as e:
            logger.error(f"Failed to search calls for clinic {clinic_id}: {e}")
            raise

    def count_by_clinic_with_filters(
        self, 
        clinic_id: int, 
        search_term: str = None,
        call_type: str = None
    ) -> int:
        """
        Count calls by clinic with filters (for pagination)
        """
        logger.info(f"Counting calls for clinic {clinic_id} with filters: search={search_term}, type={call_type}")
        
        try:
            query = self.__session.query(Call).filter(Call.clinic_id == clinic_id)
            
            # Apply search filter
            if search_term:
                query = query.filter(
                    (Call.call_id.ilike(f"%{search_term}%")) |
                    (Call.customer_phone.ilike(f"%{search_term}%"))
                )
            
            # Apply call type filter
            if call_type:
                query = query.filter(Call.call_type == call_type)
            
            count = query.count()
            logger.info(f"Found {count} calls matching criteria")
            return count
        except Exception as e:
            logger.error(f"Failed to count calls for clinic {clinic_id}: {e}")
            raise