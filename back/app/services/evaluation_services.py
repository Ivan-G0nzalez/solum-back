from typing import List, Optional
from app.domain.evaluation_models import EvaluationCreate, EvaluationUpdate, EvaluationRead
from app.repositories.unit_of_work import UnitOfWork
from app.utils.pagination import CustomPagination
from app.utils.logger import logger


class EvaluationService:
    def __init__(self, unit_of_work_factory=UnitOfWork) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def get_evaluations(self) -> List[EvaluationRead]:
        logger.info("Processing request for evaluations")
        try:
            with self._unit_of_work_factory() as uow:
                evaluation_models = uow.evaluations.list()
                evaluations = [EvaluationRead.model_validate(ev.model_dump()) for ev in evaluation_models]
                logger.info(f"Successfully retrieved {len(evaluations)} evaluations")
                return evaluations
        except Exception as e:
            logger.error(f"Error retrieving evaluations: {e}")
            raise

    def get_evaluations_paginated(self, pagination: CustomPagination):
        logger.info(f"Paginating evaluations: page={pagination.page}, items_per_page={pagination.items_per_page}")
        try:
            with self._unit_of_work_factory() as uow:
                total_count = uow.evaluations.count()
                paginated_models = uow.evaluations.list_paginated(
                    offset=pagination.offset,
                    limit=pagination.items_per_page
                )
                evaluations = [EvaluationRead.model_validate(ev.model_dump()) for ev in paginated_models]
                return pagination.paginate(evaluations, total_count)
        except Exception as e:
            logger.error(f"Error paginating evaluations: {e}")
            raise

    def get_evaluation(self, evaluation_id: int) -> Optional[EvaluationRead]:
        logger.info(f"Getting evaluation with ID {evaluation_id}")
        try:
            with self._unit_of_work_factory() as uow:
                ev_model = uow.evaluations.get(evaluation_id)
                if ev_model is None:
                    logger.warning(f"Evaluation with ID {evaluation_id} not found")
                    return None
                return EvaluationRead.model_validate(ev_model.model_dump())
        except Exception as e:
            logger.error(f"Error getting evaluation {evaluation_id}: {e}")
            raise

    def create_evaluation(self, evaluation_data: EvaluationCreate) -> EvaluationRead:
        logger.info("Creating a new evaluation")
        try:
            with self._unit_of_work_factory() as uow:
                evaluation_create = EvaluationCreate.model_validate(evaluation_data)
                created_model = uow.evaluations.add(evaluation_create)
                uow._UnitOfWork__session.commit()
                return EvaluationRead.model_validate(created_model)
        except Exception as e:
            logger.error(f"Error creating evaluation: {e}")
            raise

    def update_evaluation(self, evaluation_id: int, evaluation_data: EvaluationUpdate) -> Optional[EvaluationRead]:
        logger.info(f"Updating evaluation with ID {evaluation_id}")
        try:
            with self._unit_of_work_factory() as uow:
                update_data = evaluation_data.model_dump(exclude_unset=True)
                updated_model = uow.evaluations.update(evaluation_id, update_data)
                
                if updated_model is None:
                    logger.warning(f"Evaluation with ID {evaluation_id} not found for update")
                    return None
                
                uow._UnitOfWork__session.commit()
                
                return EvaluationRead.model_validate(updated_model)  # En lugar de updated_model.model_dump()
        except Exception as e:
            logger.error(f"Error updating evaluation {evaluation_id}: {e}")
            raise

    def delete_evaluation(self, evaluation_id: int) -> bool:
        logger.info(f"Deleting evaluation with ID {evaluation_id}")
        try:
            with self._unit_of_work_factory() as uow:
                success = uow.evaluations.delete(evaluation_id)
                if success:
                    uow._UnitOfWork__session.commit()
                    logger.info(f"Successfully deleted evaluation with ID {evaluation_id}")
                else:
                    logger.warning(f"Evaluation with ID {evaluation_id} not found for deletion")
                return success
        except Exception as e:
            logger.error(f"Error deleting evaluation {evaluation_id}: {e}")
            raise
