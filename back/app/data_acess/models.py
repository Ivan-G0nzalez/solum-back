from typing import Optional, List, Literal
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy import JSON, TIMESTAMP, func, Column
from enum import Enum


class AgentEnvironment(str, Enum):
    production = "production"
    development = "development"

class CallType(str, Enum):
    inbound = "inbound"
    outbound = "outbound"

class EvaluatorType(str, Enum):
    HUMAN = "human"
    LLM = "llm"
    VAPI = "vapi"

class TimestampMixin:
    created: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now())
    )

class Clinic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    created: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now())
    )
    calls: List["Call"] = Relationship(back_populates="clinic")

class Call(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    call_id: str = Field(index=True, unique=True)
    call_type: CallType
    agent_environment: AgentEnvironment
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
    clinic_id: int = Field(foreign_key="clinic.id")
    clinic: Optional[Clinic] = Relationship(back_populates="calls")
    evaluations: List["Evaluation"] = Relationship(back_populates="call")
    created: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now())
    )


class Evaluation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    call_id: int = Field(foreign_key="call.id")
    evaluator_type: EvaluatorType

    reviewer: Optional[str] = None
    evaluation: Optional[str] = None
    check: Optional[str] = None
    feedback: Optional[str] = None
    score: Optional[float] = None

    status_feedback_engineer: Optional[str] = None
    comments_engineer: Optional[str] = None

    call: Optional["Call"] = Relationship(back_populates="evaluations")
    created: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now())
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    email: str = Field(index=True, unique=True, max_length=100)
    password: str = Field(max_length=255)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = None
    date_joined: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(TIMESTAMP, nullable=False, server_default=func.now())
    )
