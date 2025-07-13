from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Contact(BaseModel):
    name: Optional[str] = Field(None, description="Full Name if available")
    email: EmailStr
    source: Optional[str] = Field(None, description="Source of the contact information, e.g., 'email', 'database', 'website")