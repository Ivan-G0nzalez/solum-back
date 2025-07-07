from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from .evaluation_models import EvaluationRead
from .clinics_models import Clinic as ClinicDomain
from enum import Enum

class CallType(str, Enum):
    inbound = "inbound"
    outbound = "outbound"

class AgentEnvironment(str, Enum):
    production = "production"
    development = "development"

class CallBase(BaseModel):
    call_id: str = Field(..., min_length=3, max_length=100)
    call_type: CallType = CallType.inbound
    agent_environment: AgentEnvironment = AgentEnvironment.production
    assistant: str
    call_start_time: Optional[datetime] = None
    call_ended_time: Optional[datetime] = None
    customer_phone: Optional[str] = None
    customer_name: Optional[str] = None
    duration: Optional[float] = None
    summary: Optional[str] = None
    recording_url: Optional[str] = None
    ended_reason: Optional[str] = None
    call_reason: Optional[str] = None
    clinic_id: int

    model_config = ConfigDict(from_attributes=True) 

class CallCreate(CallBase):
    call_type: CallType = CallType.inbound
    agent_environment: AgentEnvironment = AgentEnvironment.production
    pass

class CallUpdate(BaseModel):
    call_type: Optional[CallType] = CallType.inbound
    agent_environment: Optional[AgentEnvironment] = AgentEnvironment.production
    assistant: Optional[str] = None
    call_start_time: Optional[datetime] = None
    call_ended_time: Optional[datetime] = None
    customer_phone: Optional[str] = None
    customer_name: Optional[str] = None
    duration: Optional[float] = None
    summary: Optional[str] = None
    recording_url: Optional[str] = None
    ended_reason: Optional[str] = None
    call_reason: Optional[str] = None
    clinic_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class CallRead(CallBase):
    id: int
    created: datetime
    evaluations: List[EvaluationRead] = []
    clinic: Optional[ClinicDomain] = None

    model_config = ConfigDict(from_attributes=True)