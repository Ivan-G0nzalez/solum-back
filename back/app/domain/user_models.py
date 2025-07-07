from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, EmailStr
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"

class User(BaseModel):
    """Domain model for User with business logic"""
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="User email")
    first_name: str = Field(..., min_length=1, max_length=50, description="First name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Last name")
    is_active: bool = Field(default=True, description="User active status")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    date_joined: Optional[datetime] = Field(None, description="Registration timestamp")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError("Username cannot be empty")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v.strip().lower()
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v or not v.strip():
            raise ValueError("Email cannot be empty")
        # Basic email validation
        if '@' not in v or '.' not in v:
            raise ValueError("Invalid email format")
        return v.strip().lower()
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
    
    def get_full_name(self) -> str:
        """Business logic: get user's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_valid(self) -> bool:
        """Business rule: user is valid if it has required fields"""
        return bool(
            self.username and 
            self.email and 
            self.first_name and 
            self.last_name
        )
    
    def can_login(self) -> bool:
        """Business rule: user can login if active"""
        return self.is_active
    
    class Config:
        from_attributes = True

# Request/Response models for API
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="Password")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    is_active: bool = Field(default=True)

class UserUpdate(BaseModel):
    email: Optional[str] = Field(None, description="User email")
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    last_login: Optional[datetime] = None
    date_joined: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None 