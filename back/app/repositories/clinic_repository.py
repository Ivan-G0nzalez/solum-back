from app.data_acess.models import Clinic
from app.repositories.repository import AbtractRepository
from app.utils.logger import logger

class ClinicRepository(AbtractRepository):
    def __init__(self, session):
        self.__session = session
    
    def list(self):
        logger.info("Start getting the clinic from database")
        try:
            clinic = self.__session.query(Clinic).all()
            logger.info("Successful operation to get all clinic")
            return clinic
        except Exception as e:
            logger.error(
                f'Failed Operation to get all clinic name'
            )
            raise

    def list_paginated(self, offset: int, limit: int):
        """Get paginated list of clinics"""
        logger.info(f"Start getting paginated clinics: offset={offset}, limit={limit}")
        try:
            clinics = self.__session.query(Clinic).offset(offset).limit(limit).all()
            logger.info(f"Successful operation to get paginated clinics: {len(clinics)} items")
            return clinics
        except Exception as e:
            logger.error(f'Failed Operation to get paginated clinics: {e}')
            raise

    def count(self) -> int:
        """Get total count of clinics"""
        logger.info("Start counting clinics")
        try:
            count = self.__session.query(Clinic).count()
            logger.info(f"Successful count operation: {count} clinics")
            return count
        except Exception as e:
            logger.error(f'Failed Operation to count clinics: {e}')
            raise
    
    def get(self, clinic_id):
        logger.info("Starting to get a clinic from  data base")
        clinic = self.__session.query(Clinic).filter(Clinic.id == clinic_id).first()

        if clinic is None:
            logger.info(f'Clinic not founded')
            return None
        
        logger.info(f'Found the clinic: {clinic.id} name: {clinic.name}')
        return clinic

    def add(self, clinic: Clinic):
        logger.info("Starting to add a clinic to database")
        try:
            self.__session.add(clinic)
            self.__session.flush()  # Flush to get the ID
            self.__session.refresh(clinic)
            logger.info(f"Successfully added clinic: {clinic.name}")
            return clinic
        except Exception as e:
            logger.error(f"Failed to add clinic: {e}")
            raise

    def update(self, clinic_id: int, clinic_data: dict):
        logger.info(f"Starting to update clinic with id: {clinic_id}")
        try:
            clinic = self.get(clinic_id)
            if clinic is None:
                logger.error(f"Clinic with id {clinic_id} not found")
                return None
            
            for key, value in clinic_data.items():
                setattr(clinic, key, value)
            
            self.__session.flush()
            self.__session.refresh(clinic)
            logger.info(f"Successfully updated clinic: {clinic.name}")
            return clinic
        except Exception as e:
            logger.error(f"Failed to update clinic: {e}")
            raise

    def delete(self, clinic_id: int):
        logger.info(f"Starting to delete clinic with id: {clinic_id}")
        try:
            clinic = self.get(clinic_id)
            if clinic is None:
                logger.error(f"Clinic with id {clinic_id} not found")
                return False
            
            self.__session.delete(clinic)
            self.__session.flush()
            logger.info(f"Successfully deleted clinic: {clinic.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete clinic: {e}")
            raise