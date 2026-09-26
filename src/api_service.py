from typing import Dict, Any, Optional
from fastapi import FastAPI, Header, HTTPException, status
from src.user_model import UserModel
from src.config_model import AppConfig, SecuritySettings

app = FastAPI(title="Migrated Modern API")

# Mock database
USER_DATABASE: Dict[int, Dict[str, Any]] = {}

@app.get('/health')
def health_check():
    return {"status": "healthy", "service": "user-mgmt-service"}


@app.post('/api/v1/users', status_code=201)
def create_user(payload: UserModel, x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != "secret-api-token":
        raise HTTPException(status_code=401, detail="Unauthorized access")

    try:
        user = payload
        USER_DATABASE[user.id] = user.to_compact_dict()
        return {"message": "User created", "user": user.to_compact_dict()}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post('/api/v1/users/{user_id}/promote')
def promote_user(user_id: int):
    if user_id not in USER_DATABASE:
        raise HTTPException(status_code=404, detail="User not found")

    existing = UserModel.parse_from_dict_obj(USER_DATABASE[user_id])
    updated_user = existing.clone_with_role("manager")
    USER_DATABASE[user_id] = updated_user.to_compact_dict()

    return {"message": "User promoted", "user": updated_user.to_compact_dict()}


@app.post('/api/v1/config/validate')
def validate_config(payload: AppConfig):
    try:
        cfg = payload
        return {"valid": True, "sanitized": cfg.export_sanitized_config()}
    except ValueError as err:
        raise HTTPException(status_code=422, detail=str(err))
