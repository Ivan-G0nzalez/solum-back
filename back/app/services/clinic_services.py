from app.repositories.unit_of_work import UnitOfWork
from app.data_acess.models import Clinic as ClinicModel
from app.domain.clinics_models import Clinic as ClinicDomain, ClinicCreate, ClinicUpdate
from app.utils.logger import logger
from app.utils.pagination import CustomPagination


class ClinicService:
    def __init__(self, unit_of_work=UnitOfWork()) -> None:
        self.__unit_of_work = unit_of_work
    
    def get_clinics(self):
        logger.info("Processing request clinics")

        try:
            clinic_models = self.__unit_of_work.clinics.list()
            # Convert to domain models
            clinics = [ClinicDomain.model_validate(clinic) for clinic in clinic_models]
            logger.info(f"Successfully retrieved {len(clinics)} clinics")
            return clinics
        except Exception as e:
            logger.error(f"Error retrieving clinics: {e}")
            raise

    def search_clinics(self, search_term: str):
        """Search clinics by name using case-insensitive partial match"""
        logger.info(f"Processing search request for clinics with term: {search_term}")

        try:
            clinic_models = self.__unit_of_work.clinics.search_by_name(search_term)
            # Convert to domain models
            clinics = [ClinicDomain.model_validate(clinic) for clinic in clinic_models]
            logger.info(f"Successfully found {len(clinics)} clinics matching '{search_term}'")
            return clinics
        except Exception as e:
            logger.error(f"Error searching clinics: {e}")
            raise

    def get_clinics_paginated(self, pagination: CustomPagination):
        """Get paginated clinics"""
        logger.info(f"Processing request for paginated clinics: page={pagination.page}, items_per_page={pagination.items_per_page}")

        try:
            # Get total count
            total_count = self.__unit_of_work.clinics.count()
            
            # Get paginated data
            clinic_models = self.__unit_of_work.clinics.list_paginated(
                offset=pagination.offset, 
                limit=pagination.items_per_page
            )
            
            # Convert to domain models
            clinics = [ClinicDomain.model_validate(clinic) for clinic in clinic_models]
            
            # Create paginated response
            paginated_response = pagination.paginate(clinics, total_count)
            
            logger.info(f"Successfully retrieved {len(clinics)} clinics (page {pagination.page} of {paginated_response.payload['pagination']['last_page']})")
            return paginated_response
        except Exception as e:
            logger.error(f"Error retrieving paginated clinics: {e}")
            raise

    def get_clinic(self, clinic_id: int):
        logger.info(f"Processing request for clinic ID: {clinic_id}")
        
        try:
            clinic_model = self.__unit_of_work.clinics.get(clinic_id)
            if clinic_model is None:
                logger.warning(f"Clinic with ID {clinic_id} not found")
                return None
            
            # Convert to domain model
            clinic = ClinicDomain.model_validate(clinic_model)
            logger.info(f"Successfully retrieved clinic: {clinic.name}")
            return clinic
        except Exception as e:
            logger.error(f"Error retrieving clinic {clinic_id}: {e}")
            raise

    def create_clinic(self, clinic_data: ClinicCreate):
        logger.info("Processing request to create new clinic")
        
        try:
            # Validate with Pydantic
            clinic_create = ClinicCreate.model_validate(clinic_data)
            
            # Create SQLModel instance
            clinic_model = ClinicModel(name=clinic_create.name)
            created_clinic_model = self.__unit_of_work.clinics.add(clinic_model)
            
            # Commit the transaction
            self.__unit_of_work._UnitOfWork__session.commit()
            
            # Convert to domain model
            created_clinic = ClinicDomain.model_validate(created_clinic_model)
            logger.info(f"Successfully created clinic: {created_clinic.name}")
            return created_clinic
        except Exception as e:
            # Rollback on error
            self.__unit_of_work._UnitOfWork__session.rollback()
            logger.error(f"Error creating clinic: {e}")
            raise

    def update_clinic(self, clinic_id: int, clinic_data: ClinicUpdate):
        logger.info(f"Processing request to update clinic ID: {clinic_id}")
        
        try:
            # Validate with Pydantic
            clinic_update = ClinicUpdate.model_validate(clinic_data)
            
            # Convert to dict, removing None values
            update_data = clinic_update.model_dump(exclude_unset=True)
            
            updated_clinic_model = self.__unit_of_work.clinics.update(clinic_id, update_data)
            if updated_clinic_model is None:
                logger.warning(f"Clinic with ID {clinic_id} not found for update")
                return None
            
            # Commit the transaction
            self.__unit_of_work._UnitOfWork__session.commit()
            
            # Convert to domain model
            updated_clinic = ClinicDomain.model_validate(updated_clinic_model)
            logger.info(f"Successfully updated clinic: {updated_clinic.name}")
            return updated_clinic
        except Exception as e:
            # Rollback on error
            self.__unit_of_work._UnitOfWork__session.rollback()
            logger.error(f"Error updating clinic {clinic_id}: {e}")
            raise

    def delete_clinic(self, clinic_id: int):
        logger.info(f"Processing request to delete clinic ID: {clinic_id}")
        
        try:
            success = self.__unit_of_work.clinics.delete(clinic_id)
            if success:
                # Commit the transaction
                self.__unit_of_work._UnitOfWork__session.commit()
                logger.info(f"Successfully deleted clinic with ID: {clinic_id}")
            else:
                logger.warning(f"Clinic with ID {clinic_id} not found for deletion")
            return success
        except Exception as e:
            # Rollback on error
            self.__unit_of_work._UnitOfWork__session.rollback()
            logger.error(f"Error deleting clinic {clinic_id}: {e}")
            raise