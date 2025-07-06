from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class CallBase(BaseModel):
    call_id: str = Field(..., min_length=3, max_length=100)
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
    pass

class CallUpdate(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)