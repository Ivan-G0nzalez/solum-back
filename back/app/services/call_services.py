from app.repositories.unit_of_work import UnitOfWork
from app.data_acess.models import Call as CallModel
from app.domain.call_models import CallCreate, CallUpdate, CallRead
from app.utils.logger import logger
from app.utils.pagination import CustomPagination
from typing import List


class CallService:
    def __init__(self, unit_of_work=UnitOfWork()) -> None:
        self.__unit_of_work = unit_of_work

    def get_calls(self) -> List[CallRead]:
        logger.info("Processing request for calls")

        try:
            call_models = self.__unit_of_work.calls.list()
            calls = [CallRead.model_validate(call.model_dump()) for call in call_models]
            logger.info(f"Successfully retrieved {len(calls)} calls")
            return calls
        except Exception as e:
            logger.error(f"Error retrieving calls: {e}")
            raise
    
    def get_calls_by_clinic_paginated(self, clinic_id: int, pagination: CustomPagination):
        logger.info(f"Paginating calls for clinic {clinic_id}: page={pagination.page}, items_per_page={pagination.items_per_page}")

        try:
            total_count = self.__unit_of_work.calls.count_by_clinic(clinic_id)
            call_models = self.__unit_of_work.calls.list_by_clinic_paginated(
                clinic_id=clinic_id,
                offset=pagination.offset, 
                limit=pagination.items_per_page
            )
            calls = [CallRead.model_validate(call.model_dump()) for call in call_models]
            paginated_response = pagination.paginate(calls, total_count)
            return paginated_response
        except Exception as e:
            logger.error(f"Error paginating calls for clinic {clinic_id}: {e}")
            raise

    def get_calls_paginated(self, pagination: CustomPagination):
        logger.info(f"Paginating calls: page={pagination.page}, items_per_page={pagination.items_per_page}")

        try:
            total_count = self.__unit_of_work.calls.count()
            call_models = self.__unit_of_work.calls.list_paginated(
                offset=pagination.offset, 
                limit=pagination.items_per_page
            )
            calls = [CallRead.model_validate(call.model_dump()) for call in call_models]
            paginated_response = pagination.paginate(calls, total_count)
            return paginated_response
        except Exception as e:
            logger.error(f"Error paginating calls: {e}")
            raise

    def get_call(self, call_id: int) -> CallRead | None:
        logger.info(f"Getting call with ID {call_id}")

        try:
            call_model = self.__unit_of_work.calls.get(call_id)
            if call_model is None:
                logger.warning(f"Call with ID {call_id} not found")
                return None

            return CallRead.model_validate(call_model.model_dump())
        except Exception as e:
            logger.error(f"Error getting call {call_id}: {e}")
            raise

    def create_call(self, call_data: CallCreate) -> CallRead:
        logger.info("Creating a new call")

        try:
            call_create = CallCreate.model_validate(call_data)
            created_call = self.__unit_of_work.calls.add(call_create)
            self.__unit_of_work._UnitOfWork__session.commit()

            return CallRead.model_validate(created_call)
        except Exception as e:
            self.__unit_of_work._UnitOfWork__session.rollback()
            logger.error(f"Error creating call: {e}")
            raise

    def update_call(self, call_id: int, call_data: CallUpdate) -> CallRead | None:
        logger.info(f"Updating call with ID {call_id}")

        try:
            call_update = CallUpdate.model_validate(call_data)
            update_data = call_update.model_dump(exclude_unset=True)

            updated_call_model = self.__unit_of_work.calls.update(call_id, update_data)
            if updated_call_model is None:
                logger.warning(f"Call with ID {call_id} not found for update")
                return None

            self.__unit_of_work._UnitOfWork__session.commit()
            updated_call = CallRead.model_validate(updated_call_model)
            return updated_call
        except Exception as e:
            self.__unit_of_work._UnitOfWork__session.rollback()
            logger.error(f"Error updating call {call_id}: {e}")
            raise

    def delete_call(self, call_id: int) -> bool:
        logger.info(f"Deleting call with ID {call_id}")

        try:
            success = self.__unit_of_work.calls.delete(call_id)
            if success:
                self.__unit_of_work._UnitOfWork__session.commit()
                logger.info(f"Successfully deleted call with ID {call_id}")
            else:
                logger.warning(f"Call with ID {call_id} not found for deletion")
            return success
        except Exception as e:
            self.__unit_of_work._UnitOfWork__session.rollback()
            logger.error(f"Error deleting call {call_id}: {e}")
            raise