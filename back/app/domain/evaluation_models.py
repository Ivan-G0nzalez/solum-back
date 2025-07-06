from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EvaluationBase(BaseModel):
    call_id: int
    evaluator_type: Literal["human", "llm", "vapi"]
    reviewer: Optional[str] = None
    evaluation: Optional[str] = None
    check: Optional[str] = None
    feedback: Optional[str] = None
    score: Optional[float] = None
    status_feedback_engineer: Optional[str] = None
    comments_engineer: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) 

class EvaluationCreate(EvaluationBase):
    pass

class EvaluationUpdate(BaseModel):
    evaluation: Optional[str] = None
    feedback: Optional[str] = None
    score: Optional[float] = None
    status_feedback_engineer: Optional[str] = None
    comments_engineer: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class EvaluationRead(EvaluationBase):
    id: int
    created: datetime

    model_config = ConfigDict(from_attributes=True)
