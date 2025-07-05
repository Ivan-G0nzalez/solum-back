from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy import JSON

class Clinic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    # calls: List["Call"] = Relationship(back_populates="clinic")

# class Call(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     call_id: str = Field(index=True, unique=True)
#     assistant: str
#     ended_reason: Optional[str] = None
#     customer_phone: Optional[str] = None
#     customer_name: Optional[str] = None
#     insurance: Optional[str] = None
#     dob: Optional[datetime] = None
#     call_reason: Optional[str] = None
#     call_start_time: Optional[datetime] = None
#     call_ended_time: Optional[datetime] = None
#     duration: Optional[float] = None
#     recording_url: Optional[str] = None
#     summary: Optional[str] = None
#     date: Optional[str] = None
#     call_metadata: Optional[dict] = Field(default=None, sa_column=JSON)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

#     clinic_id: int = Field(foreign_key="clinic.id")
#     clinic: Optional[Clinic] = Relationship(back_populates="calls")
#     evaluations: List["Evaluation"] = Relationship(back_populates="call")


# class Evaluation(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     call_id: int = Field(foreign_key="call.id")
#     evaluator_type: str  # "human" or "llm"
#     reviewer: Optional[str] = None
#     score: Optional[float] = None
#     check: Optional[str] = None
#     feedback: Optional[str] = None
#     status_feedback_engineer: Optional[str] = None
#     comments_engineer: Optional[str] = None
#     evaluation_metadata: Optional[dict] = Field(default=None, sa_column=JSON)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

#     call: Optional[Call] = Relationship(back_populates="evaluations")