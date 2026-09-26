from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict


class Address(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    street: str
    city: str
    postal_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = "USA"


class UserProfile(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    interests: List[str] = Field(default_factory=list, min_length=1)


class UserModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True, extra='forbid')

    id: int
    username: str
    email: str
    is_active: bool = True
    role: str = "member"
    address: Optional[Address] = None
    profile: Optional[UserProfile] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed_roles = ['admin', 'member', 'guest', 'manager']
        if v.lower() not in allowed_roles:
            raise ValueError(f'Role must be one of {allowed_roles}')
        return v.lower()

    @model_validator(mode='before')
    @classmethod
    def normalize_and_check_email(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        email = values.get('email')
        if email:
            values['email'] = email.strip().lower()
            if not values['email'].endswith(('@example.com', '@company.org', '@test.com')):
                raise ValueError('Email domain not authorized')
        return values

    def to_compact_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_unset=True, exclude_none=True)

    def clone_with_role(self, new_role: str) -> "UserModel":
        return self.model_copy(update={"role": new_role})

    @classmethod
    def parse_from_json_str(cls, json_str: str) -> "UserModel":
        return cls.model_validate_json(json_str)

    @classmethod
    def parse_from_dict_obj(cls, obj: Any) -> "UserModel":
        return cls.model_validate(obj)
