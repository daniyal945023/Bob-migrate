# BobMigrate — Autonomous Codebase Modernization Suite

> **An agentic refactoring workflow built inside IBM Bob IDE for automated Pydantic v1 to v2 migrations and Flask to FastAPI transformation — fully verified by a self-healing pytest loop.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.x-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![IBM Bob](https://img.shields.io/badge/IBM%20Bob-2.0-054ADA?style=flat-square&logo=ibm&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)

---

## Table of Contents

1. [Executive Summary](#executive-summary--problem-statement)
2. [IBM Bob 2.0 Core Features Demonstrated](#ibm-bob-20-hackathon-core-features-demonstrated)
3. [Architecture & Pipeline Diagram](#architecture--pipeline-diagram)
4. [Directory Structure](#directory-structure)
5. [Before vs. After Code Comparison](#before-vs-after-code-comparison)
6. [Quick Start & Local Verification](#quick-start--local-verification)
7. [Test Suite Output](#test-suite-output)
8. [Hackathon Acknowledgments](#hackathon-acknowledgments)

---

## Executive Summary & Problem Statement

### The Problem

Upgrading legacy Python codebases is a time-intensive, error-prone process. A typical Pydantic v1 → v2 migration requires an engineer to:

- **Read and internalize** 30+ pages of framework migration documentation
- **Locate every deprecated pattern** across dozens of model files (`@validator`, `.dict()`, `class Config`, `regex=`, `min_items=`, `orm_mode`, etc.)
- **Manually rewrite each occurrence** with the correct v2 equivalent — in the right order, with the right decorator stacking
- **Fix a broken Flask service layer** simultaneously, migrating routes, request parsing, error handling, and header injection to FastAPI conventions
- **Debug cascading test failures** introduced by subtle API differences until the suite is green again

This process routinely costs **multiple engineer-days** and introduces regressions. It is mechanical, repetitive, and entirely automatable — yet no tool has done it end-to-end until now.

### The Solution

**BobMigrate** is an autonomous modernization agent built natively inside **IBM Bob IDE**. It treats a legacy codebase as a structured transformation problem: ingest the migration specification, decompose the work across parallel subagents, apply changes atomically to disk, and close the loop via an agentic CLI test harness — all without human intervention.

The result: **3 source files, 28 migration rules, 1 syntax error corrected, 6/6 tests passing, 0 mypy errors — in a single orchestration pass.**

---

## IBM Bob 2.0 Hackathon Core Features Demonstrated

### 1. 📄 Document Understanding
BobMigrate begins by ingesting both migration guides as living specification documents:

```
@docs/pydantic_v1_to_v2_guide.md   →  Extract 13 Pydantic transformation rules
@docs/flask_to_fastapi_guide.md    →  Extract 9 Flask→FastAPI transformation rules
```

Rather than hard-coding migration logic, the agent **reads the documentation at runtime** and derives its transformation ruleset dynamically — exactly as a human engineer would, but in milliseconds.

---

### 2. ⚡ Parallel Subagents
Three independent subagents are spawned **simultaneously** in a single orchestration turn, each given an isolated, precisely-scoped task:

| Subagent | Target File | Responsibility |
|---|---|---|
| **Subagent 1** | `src/user_model.py` | 12 Pydantic v2 rules + syntax error correction |
| **Subagent 2** | `src/config_model.py` | 6 Pydantic v2 rules |
| **Subagent 3** | `src/api_service.py` | 9 Flask → FastAPI rules |

Each subagent writes its output directly to disk. The parent controller waits for all three to complete before proceeding — a **true fan-out/fan-in architecture** that reduces total refactoring time compared to sequential execution.

---

### 3. 🔁 Agent Mode & Self-Healing Loop
After subagent writes complete, BobMigrate enters **Agent Mode CLI** and executes a dual validation loop:

**Test Healing Loop:**
```
run pytest  →  if FAIL: inspect traceback → edit source on disk → re-run pytest
             →  if PASS: proceed ✅
```

**Type Healing Loop:**
```
run mypy src/ --ignore-missing-imports  →  if ERRORS: resolve annotations → re-run mypy
                                         →  if 0 ERRORS: proceed ✅
```

In this project, both loops resolved on the **first run** — a testament to the precision of the subagent transformation instructions.

---

### 4. 📊 Visual Reporting & Analytics
BobMigrate concludes by generating a complete audit trail:

| Artifact | Description |
|---|---|
| `MIGRATION_SUMMARY.md` | Full diff tables, applied rules, mypy report, benchmark results, pytest logs, git record |
| `MIGRATION_SUMMARY.html` | Interactive dark-mode developer dashboard with metric badges, red/green code diffs, and terminal output panels |
| `PULL_REQUEST.md` | Professional GitHub PR body with breaking changes, risk tier (🟢 LOW), verification steps, and reviewer sign-off checklist |

---

## Architecture & Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     LEGACY REPOSITORY INPUTS                        │
│                                                                     │
│  src/user_model.py    src/config_model.py    src/api_service.py    │
│  (Pydantic v1)        (Pydantic v1)          (Flask)               │
│                                                                     │
│  docs/pydantic_v1_to_v2_guide.md   docs/flask_to_fastapi_guide.md  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│               MASTER BOB CONTROLLER (Step 1)                        │
│                                                                     │
│  • Parse both migration guides                                      │
│  • Extract 13 Pydantic rules + 9 FastAPI rules                     │
│  • git checkout -b feature/bobmigrate-modernization                 │
└──────────┬──────────────────────────────────────────────────────────┘
           │
           │  Fan-out: 3 parallel subagents
           ▼
┌──────────────────────────────────────────────────────────────────┐
│                  PARALLEL SUBAGENTS (Step 2)                     │
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Subagent 1     │  │  Subagent 2     │  │  Subagent 3     │  │
│  │                 │  │                 │  │                 │  │
│  │  user_model.py  │  │ config_model.py │  │  api_service.py │  │
│  │  Pydantic v2    │  │  Pydantic v2    │  │  Flask→FastAPI  │  │
│  │  12 rules       │  │  6 rules        │  │  9 rules        │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           └───────────────────┬┘───────────────────┘            │
│                               │ Fan-in                           │
└───────────────────────────────┼──────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│              AGENT MODE CLI — DUAL HEALING LOOP (Step 3)            │
│                                                                     │
│  ┌──────────────┐         ┌─────────────┐                          │
│  │ python -m    │  PASS   │  python -m  │  0 ERRORS               │
│  │ pytest       ├────────►│  mypy src/  ├──────────►  CONTINUE    │
│  │              │         │             │                          │
│  │  6/6 GREEN ✅│         │  0 errors ✅│                          │
│  └──────────────┘         └─────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│              BENCHMARKS + GIT AUTOMATION (Steps 4–5)                │
│                                                                     │
│  python -m tests.benchmark  →  59,076 ops/sec @ 10,000 iterations  │
│  git add src/ docs/ tests/ requirements.txt                        │
│  git commit -m "refactor(core): automated Pydantic v2 & FastAPI    │
│                 modernization via BobMigrate"                       │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  GENERATED ARTIFACTS (Step 6)                       │
│                                                                     │
│  MIGRATION_SUMMARY.md    MIGRATION_SUMMARY.html    PULL_REQUEST.md  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
BobMigrate/
│
├── docs/
│   ├── pydantic_v1_to_v2_guide.md     # Migration spec: 13 Pydantic transformation rules
│   └── flask_to_fastapi_guide.md      # Migration spec: 9 Flask → FastAPI rules
│
├── src/
│   ├── __init__.py
│   ├── user_model.py                  # Address, UserProfile, UserModel (Pydantic v2)
│   ├── config_model.py                # SecuritySettings, AppConfig (Pydantic v2)
│   └── api_service.py                 # FastAPI app with 4 endpoints
│
├── tests/
│   ├── test_models.py                 # 3 model validation & serialization tests
│   ├── test_api.py                    # 3 FastAPI endpoint integration tests
│   └── benchmark.py                   # 10,000-iteration throughput benchmark
│
├── MIGRATION_SUMMARY.md               # Full audit trail (rules, mypy, benchmark, git)
├── MIGRATION_SUMMARY.html             # Interactive dark-mode developer dashboard
├── PULL_REQUEST.md                    # PR body with breaking changes & reviewer checklist
├── README.md                          # This file
└── requirements.txt                   # pydantic>=2.0.0, fastapi, pytest, mypy, httpx
```

---

## Before vs. After Code Comparison

### Model Configuration

**Before — Pydantic v1**
```python
class UserModel(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        str_strip_whitespace = True
        orm_mode = True          # ← deprecated key
        extra = 'forbid'
        allow_mutation = False   # ← deprecated key
```

**After — Pydantic v2**
```python
class UserModel(BaseModel):
    model_config = ConfigDict(   # ← top-level class variable
        str_strip_whitespace=True,
        from_attributes=True,    # ← orm_mode replacement
        extra='forbid',
        frozen=True,             # ← allow_mutation=False replacement
    )
    id: int
    username: str
    email: str
```

---

### Field Validators

**Before — Pydantic v1**
```python
from pydantic import validator, root_validator

@validator('username')
def validate_username(cls, v):
    if not v.isalnum():
        raise ValueError('Username must be alphanumeric')
    return v.lower()

@root_validator(pre=True)
def normalize_email(cls, values):
    values['email'] = values.get('email', '').strip().lower()
    return values
```

**After — Pydantic v2**
```python
from pydantic import field_validator, model_validator

@field_validator('username')   # ← @validator replaced
@classmethod                   # ← explicit classmethod required
def validate_username(cls, v):
    if not v.isalnum():
        raise ValueError('Username must be alphanumeric')
    return v.lower()

@model_validator(mode='before')  # ← @root_validator replaced
@classmethod
def normalize_email(cls, values):
    values['email'] = values.get('email', '').strip().lower()
    return values
```

---

### Serialization & Parsing

**Before — Pydantic v1**
```python
# Serialization
data = user.dict(exclude_unset=True)     # ← deprecated
clone = user.copy(update={"role": "admin"})  # ← deprecated

# Parsing
user = UserModel.parse_obj(raw_dict)     # ← deprecated
user = UserModel.parse_raw(json_string)  # ← deprecated
```

**After — Pydantic v2**
```python
# Serialization
data = user.model_dump(exclude_unset=True)        # ✅
clone = user.model_copy(update={"role": "admin"}) # ✅

# Parsing
user = UserModel.model_validate(raw_dict)         # ✅
user = UserModel.model_validate_json(json_string) # ✅
```

---

### Field Constraints

**Before — Pydantic v1**
```python
postal_code: str = Field(..., regex=r'^\d{5}(-\d{4})?$')  # ← deprecated kwarg
interests: List[str] = Field(default_factory=list, min_items=1)  # ← deprecated kwarg
```

**After — Pydantic v2**
```python
postal_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')   # ✅
interests: List[str] = Field(default_factory=list, min_length=1)  # ✅
```

---

### Web Framework (Flask → FastAPI)

**Before — Flask**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != "secret-api-token":
        return jsonify({"detail": "Unauthorized"}), 401

    raw_data = request.get_json()
    user = UserModel.parse_obj(raw_data)
    return jsonify({"user": user.dict()}), 201
```

**After — FastAPI**
```python
from fastapi import FastAPI, Header, HTTPException
from typing import Optional

app = FastAPI(title="Migrated Modern API")

@app.post('/api/v1/users', status_code=201)
def create_user(payload: UserModel, x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != "secret-api-token":
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"user": payload.model_dump()}
```

---

## Quick Start & Local Verification

### Prerequisites

- Python **3.11+**
- `git`

### 1. Clone the Repository

```bash
git clone https://github.com/daniyal945023/Bob-migrate.git
cd Bob-migrate
```

### 2. Create & Activate a Virtual Environment

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` installs:

| Package | Version | Purpose |
|---|---|---|
| `pydantic` | `>=2.0.0` | Core data validation framework |
| `fastapi` | `>=0.100.0` | Modern async web framework |
| `pytest` | `>=7.0.0` | Test runner |
| `httpx` | `>=0.24.0` | FastAPI `TestClient` transport |
| `mypy` | `>=1.5.0` | Static type checker |
| `flask` | `>=3.0.0` | Retained for legacy compatibility reference |

### 4. Run the Full Test Suite

```bash
pytest
```

Expected output:

```
============================= test session starts =============================
collected 6 items

tests/test_api.py::test_health_check                    PASSED    [ 16%]
tests/test_api.py::test_create_user_flow                PASSED    [ 33%]
tests/test_api.py::test_config_validation_endpoint      PASSED    [ 50%]
tests/test_models.py::test_user_model_legacy_features   PASSED    [ 66%]
tests/test_models.py::test_user_model_validation_failures PASSED  [ 83%]
tests/test_models.py::test_config_model_sanitization    PASSED    [100%]

============================== 6 passed in 1.48s ==============================
```

### 5. Run Static Type Checking

```bash
python -m mypy src/ --ignore-missing-imports
```

Expected output:

```
Success: no issues found in 4 source files
```

### 6. Run the Performance Benchmark

```bash
python -m tests.benchmark
```

Expected output:

```
--- BENCHMARK RESULTS ---
Total Iterations:      10,000
Total Execution Time:  0.1693 seconds
Throughput:            59,076.80 ops/sec
```

---

## Test Suite Output

| Test | File | Status |
|---|---|---|
| `test_health_check` | `tests/test_api.py` | ✅ PASSED |
| `test_create_user_flow` | `tests/test_api.py` | ✅ PASSED |
| `test_config_validation_endpoint` | `tests/test_api.py` | ✅ PASSED |
| `test_user_model_legacy_features` | `tests/test_models.py` | ✅ PASSED |
| `test_user_model_validation_failures` | `tests/test_models.py` | ✅ PASSED |
| `test_config_model_sanitization` | `tests/test_models.py` | ✅ PASSED |

**6/6 tests passing. 0 mypy errors. 59,076 ops/sec benchmark throughput.**

---

## Hackathon Acknowledgments

**BobMigrate** was designed and built for the **IBM Bob 2.0 Hackathon**, showcasing the full breadth of agentic capabilities available inside the **IBM Bob IDE**:

- **Document Understanding** — runtime ingestion of migration guides as dynamic rule sources
- **Parallel Subagents** — fan-out task decomposition for concurrent source file transformation
- **Agent Mode CLI** — self-healing feedback loops using live terminal execution
- **Visual Reporting** — auto-generated HTML dashboards and structured Markdown audit trails
- **Git Automation** — semantic commits and branch management executed programmatically

> _Built with ❤️ using **IBM Bob IDE** — the agentic development environment that turns migration specs into working code._

---

<p align="center">
  <sub>BobMigrate · IBM Bob 2.0 Hackathon · MIT License</sub>
</p>
