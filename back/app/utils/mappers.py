from app.data_acess.models import Clinic as ClinicModel, Call as CallModel, Evaluation as EvaluationModel
from app.domain.models import Clinic as ClinicDomain, Call as CallDomain, Evaluation as EvaluationDomain
from utils.logger import logger

class ClinicMapper:
    @staticmethod
    def to_domain(clinic_model: ClinicModel) -> ClinicDomain:
        """Convert SQLModel to Domain model using Pydantic"""
        try:
            return ClinicDomain.model_validate(clinic_model)
        except Exception as e:
            logger.error(f"Error mapping clinic to domain: {e}")
            raise ValueError(f"Failed to map clinic to domain: {e}")
    
    @staticmethod
    def to_model(clinic_domain: ClinicDomain) -> ClinicModel:
        """Convert Domain model to SQLModel"""
        try:
            return ClinicModel(
                id=clinic_domain.id,
                name=clinic_domain.name
            )
        except Exception as e:
            logger.error(f"Error mapping clinic to model: {e}")
            raise ValueError(f"Failed to map clinic to model: {e}")

    

class CallMapper:
    @staticmethod
    def to_domain(call_model: CallModel) -> CallDomain:
        """Convert SQLModel to Domain model using Pydantic"""
        return CallDomain.model_validate(call_model)
    
    @staticmethod
    def to_model(call_domain: CallDomain) -> CallModel:
        """Convert Domain model to SQLModel"""
        return CallModel(
            id=call_domain.id,
            call_id=call_domain.call_id,
            assistant=call_domain.assistant,
            clinic_id=call_domain.clinic_id,
            customer_phone=call_domain.customer_phone,
            customer_name=call_domain.customer_name,
            insurance=call_domain.insurance,
            dob=call_domain.dob,
            call_reason=call_domain.call_reason,
            call_start_time=call_domain.call_start_time,
            call_ended_time=call_domain.call_ended_time,
            duration=call_domain.duration,
            recording_url=call_domain.recording_url,
            summary=call_domain.summary,
            ended_reason=call_domain.ended_reason,
            created_at=call_domain.created_at
        ) 