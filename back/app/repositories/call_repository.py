from sqlalchemy.orm import Session
from app.data_acess.models import Call
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
            calls = self.__session.query(Call).all()
            return calls
        except Exception as e:
            logger.error(f"Failed to fetch all calls: {e}")
            raise
    
    def list_paginated(self, offset: int, limit: int) -> List[Call]:
        logger.info(f"Fetching paginated calls (offset={offset}, limit={limit})")
        try:
            return self.__session.query(Call).offset(offset).limit(limit).all()
        except Exception as e:
            logger.error(f"Failed to fetch paginated calls: {e}")
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
        call = self.__session.query(Call).filter(Call.id == call_id).first()
        if not call:
            logger.warning(f"Call with ID {call_id} not found")
        return call
    
    
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

    def update(self, call_id: int, call_update: CallUpdate) -> Optional[Call]:
        logger.info(f"Updating call with ID {call_id}")
        try:
            call = self.get(call_id)
            if not call:
                return None
            for key, value in call_update.dict(exclude_unset=True).items():
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