from typing import List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

class SecuritySettings(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    secret_key: str = Field(..., min_length=16)
    token_ttl_minutes: int = 60
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]


class AppConfig(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, frozen=True, from_attributes=True)

    app_name: str
    environment: str = "development"
    debug: bool = False
    max_workers: int = Field(default=4, ge=1, le=32)
    security: SecuritySettings

    @field_validator('environment')
    @classmethod
    def validate_env(cls, v):
        valid_envs = ['development', 'staging', 'production', 'testing']
        if v.lower() not in valid_envs:
            raise ValueError(f'Environment must be in {valid_envs}')
        return v.lower()

    def export_sanitized_config(self) -> Dict[str, Any]:
        raw_dict = self.model_dump()
        if "security" in raw_dict and "secret_key" in raw_dict["security"]:
            raw_dict["security"]["secret_key"] = "********"
        return raw_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        return cls.model_validate(data)
