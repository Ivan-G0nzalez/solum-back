from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class CallStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class EvaluationType(str, Enum):
    HUMAN = "human"
    LLM = "llm"

class Clinic(BaseModel):
    """Domain model for Clinic with business logic"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100, description="Clinic name")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Clinic name cannot be empty")
        return v.strip()
    
    def is_valid(self) -> bool:
        """Business rule: clinic is valid if it has a name"""
        return bool(self.name and self.name.strip())
    
    class Config:
        from_attributes = True

class Call(BaseModel):
    """Domain model for Call with business logic"""
    id: Optional[int] = None
    call_id: str = Field(..., description="Unique call identifier")
    assistant: str = Field(..., description="Assistant name")
    clinic_id: int = Field(..., description="Clinic ID")
    customer_phone: Optional[str] = Field(None, description="Customer phone number")
    customer_name: Optional[str] = Field(None, description="Customer name")
    insurance: Optional[str] = Field(None, description="Insurance provider")
    dob: Optional[datetime] = Field(None, description="Date of birth")
    call_reason: Optional[str] = Field(None, description="Reason for the call")
    call_start_time: Optional[datetime] = Field(None, description="Call start time")
    call_ended_time: Optional[datetime] = Field(None, description="Call end time")
    duration: Optional[float] = Field(None, description="Call duration in seconds")
    recording_url: Optional[str] = Field(None, description="Recording URL")
    summary: Optional[str] = Field(None, description="Call summary")
    ended_reason: Optional[str] = Field(None, description="Reason call ended")
    status: CallStatus = Field(CallStatus.IN_PROGRESS, description="Call status")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    
    @field_validator('call_id')
    @classmethod
    def validate_call_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Call ID is required")
        return v.strip()
    
    @field_validator('assistant')
    @classmethod
    def validate_assistant(cls, v):
        if not v or not v.strip():
            raise ValueError("Assistant is required")
        return v.strip()
    
    def calculate_duration(self) -> Optional[float]:
        """Business logic: calculate call duration"""
        if self.call_start_time and self.call_ended_time:
            return (self.call_ended_time - self.call_start_time).total_seconds()
        return None
    
    def is_completed(self) -> bool:
        """Business rule: call is completed if it has end time"""
        return self.call_ended_time is not None
    
    def can_be_evaluated(self) -> bool:
        """Business rule: call can be evaluated if completed and has recording"""
        return self.is_completed() and bool(self.recording_url)
    
    class Config:
        from_attributes = True

class Evaluation(BaseModel):
    """Domain model for Evaluation with business logic"""
    id: Optional[int] = None
    call_id: int = Field(..., description="Call ID")
    evaluator_type: EvaluationType = Field(..., description="Type of evaluator")
    reviewer: Optional[str] = Field(None, description="Reviewer name")
    score: Optional[float] = Field(None, ge=0, le=10, description="Evaluation score (0-10)")
    check: Optional[str] = Field(None, description="Check details")
    feedback: Optional[str] = Field(None, description="Evaluation feedback")
    status_feedback_engineer: Optional[str] = Field(None, description="Engineer feedback status")
    comments_engineer: Optional[str] = Field(None, description="Engineer comments")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    
    @field_validator('score')
    @classmethod
    def validate_score(cls, v):
        if v is not None and not (0 <= v <= 10):
            raise ValueError("Score must be between 0 and 10")
        return v
    
    def is_complete(self) -> bool:
        """Business rule: evaluation is complete if it has score and feedback"""
        return self.score is not None and bool(self.feedback)
    
    def get_quality_level(self) -> str:
        """Business logic: determine quality level based on score"""
        if self.score is None:
            return "Not evaluated"
        elif self.score >= 9:
            return "Excellent"
        elif self.score >= 7:
            return "Good"
        elif self.score >= 5:
            return "Average"
        else:
            return "Poor"
    
    class Config:
        from_attributes = True

# Request/Response models for API
class ClinicCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class ClinicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class CallCreate(BaseModel):
    call_id: str
    assistant: str
    clinic_id: int
    customer_phone: Optional[str] = None
    customer_name: Optional[str] = None
    insurance: Optional[str] = None
    call_reason: Optional[str] = None
    recording_url: Optional[str] = None

class CallUpdate(BaseModel):
    call_ended_time: Optional[datetime] = None
    duration: Optional[float] = None
    summary: Optional[str] = None
    ended_reason: Optional[str] = None
    status: Optional[CallStatus] = None 