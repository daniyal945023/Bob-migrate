# Comprehensive Pydantic v1 to v2 Migration Guide

### 1. Field Validators
- Replace `@validator('field1', 'field2', pre=True)` with `@field_validator('field1', 'field2', mode='before')`.
- Replace `@validator('field', always=True)` with `@field_validator('field', mode='after')`.
- **CRITICAL**: All `@field_validator` functions MUST be decorated with `@classmethod` as the top decorator.

### 2. Root Validators
- Replace `@root_validator(pre=True)` with `@model_validator(mode='before')`.
- Replace `@root_validator()` (or `pre=False`) with `@model_validator(mode='after')`.

### 3. Serialization & Parsing
- Replace `.dict()` with `.model_dump()`. Pass parameters like `exclude_unset=True` or `exclude_none=True` as-is.
- Replace `.json()` with `.model_dump_json()`.
- Replace `Model.parse_raw(data)` with `Model.model_validate_json(data)`.
- Replace `Model.parse_obj(data)` with `Model.model_validate(data)`.
- Replace `model.copy(update={...})` with `model.model_copy(update={...})`.

### 4. Field Definitions & Constraints
- Replace `Field(..., regex=r'...')` with `Field(..., pattern=r'...')`.
- Replace `Field(..., min_items=N)` with `Field(..., min_length=N)`.

### 5. Model Configuration (`ConfigDict`)
- Remove inner `class Config:`.
- Add `model_config = ConfigDict(...)` at the class top level. Import `ConfigDict` from `pydantic`.
- Key Mappings:
  - `allow_mutation = False` $\rightarrow$ `frozen=True`
  - `orm_mode = True` $\rightarrow$ `from_attributes=True`
  - `str_strip_whitespace = True` $\rightarrow$ `str_strip_whitespace=True`
  - `extra = 'forbid'` $\rightarrow$ `extra='forbid'`