from sqlalchemy.orm import Session
from app.data_acess.models import Evaluation
from app.repositories.repository import AbtractRepository
from app.utils.logger import logger
from app.domain.evaluation_models import EvaluationCreate, EvaluationUpdate
from typing import List

class EvaluationRepository(AbtractRepository):
    def __init__(self, session: Session):
        self.__session = session

    def list(self):
        logger.info("Getting all evaluations from the database")
        try:
            return self.__session.query(Evaluation).all()
        except Exception as e:
            logger.error(f"Error listing evaluations: {e}")
            raise   
    
    def count(self) -> int:
        logger.info("Counting total Evaluations")
        try:
            return self.__session.query(Evaluation).count()
        except Exception as e:
            logger.error(f"Failed to count Evaluations: {e}")
            raise

    def list_paginated(self, offset: int, limit: int) -> List[Evaluation]:
        logger.info(f"Getting paginated evaluations (offset={offset}, limit={limit})")
        try:
            return self.__session.query(Evaluation).offset(offset).limit(limit).all()
        except Exception as e:
            logger.error(f"Error paginating evaluations: {e}")
            raise

    def get(self, evaluation_id: int):
        logger.info(f"Getting evaluation with ID: {evaluation_id}")
        try:
            return self.__session.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        except Exception as e:
            logger.error(f"Error retrieving evaluation {evaluation_id}: {e}")
            raise

    def add(self, evaluation_create: EvaluationCreate) -> Evaluation:
        logger.info("Adding a new evaluation")
        try:
            evaluation_data = evaluation_create.model_dump()
            evaluation = Evaluation(**evaluation_data)            

            self.__session.add(evaluation)
            self.__session.commit()
            self.__session.refresh(evaluation)
            logger.info(f"Evaluation created successfully with ID {evaluation.id}")
            return evaluation
        except Exception as e:
            self.__session.rollback()
            logger.error(f"Error creating evaluation: {e}")
            raise

    def update(self, evaluation_id: int, data: EvaluationUpdate):
        logger.info(f"Updating evaluation with ID {evaluation_id}")
        try:
            evaluation = self.get(evaluation_id)
            if not evaluation:
                logger.warning(f"Evaluation with ID {evaluation_id} not found")
                return None
            for key, value in data.items():
                setattr(evaluation, key, value)
            self.__session.commit()
            self.__session.refresh(evaluation)
            logger.info(f"Evaluation with ID {evaluation_id} updated successfully")
            return evaluation
        except Exception as e:
            self.__session.rollback()
            logger.error(f"Error updating evaluation {evaluation_id}: {e}")
            raise

    def delete(self, evaluation_id: int):
        logger.info(f"Deleting evaluation with ID {evaluation_id}")
        try:
            evaluation = self.get(evaluation_id)
            if evaluation:
                self.__session.delete(evaluation)
                self.__session.commit()
                logger.info(f"Evaluation with ID {evaluation_id} deleted successfully")
                return True
            else:
                logger.warning(f"Evaluation with ID {evaluation_id} not found for deletion")
                return False
        except Exception as e:
            self.__session.rollback()
            logger.error(f"Error deleting evaluation {evaluation_id}: {e}")
            raise