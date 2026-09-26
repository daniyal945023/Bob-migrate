# IBM Bob 2.0 Master Execution Prompt
@workspace You are acting as BobMigrate, a Senior Principal Software Architect Agent. Your objective is to perform a complete end-to-end repository modernization: migrating Pydantic v1 to v2, Flask to FastAPI, enforcing strict type checking, running performance benchmarks, executing Git automation, and writing an audit trail.

Execute the following 6-step agentic pipeline:

STEP 1: DOCUMENT UNDERSTANDING & STATIC ANALYSIS
- Parse both @docs/pydantic_v1_to_v2_guide.md AND @docs/flask_to_fastapi_guide.md.
- Run terminal command: `git checkout -b feature/bobmigrate-modernization`

STEP 2: PARALLEL SUBAGENT REFACTORING
- Spawn 3 parallel subagents simultaneously:
  * Subagent 1: Modernize @src/user_model.py to Pydantic v2 (@field_validator, @model_validator, pattern, min_length, ConfigDict, model_dump, model_validate_json, model_copy).
  * Subagent 2: Modernize @src/config_model.py to Pydantic v2 (ConfigDict, model_dump, model_validate).
  * Subagent 3: Modernize @src/api_service.py to FastAPI (FastAPI app, status codes, Pydantic type signatures, Header parameters, HTTPException).

STEP 3: AGENT MODE CLI - DUAL TEST & TYPE HEALING LOOP
- Open Agent Mode terminal and run: `python -m pytest`
- If tests fail, inspect tracebacks, edit code on disk, and re-test until green.
- Run: `mypy src/ --ignore-missing-imports`
- If type errors occur, resolve missing or ambiguous annotations in @src/ files and re-run `mypy` until 0 errors are reported.

STEP 4: PERFORMANCE BENCHMARKING
- In Agent Mode terminal, execute: `python -m tests.benchmark`
- Capture the benchmark execution metrics (Execution Time & Throughput ops/sec).

STEP 5: GIT AUTOMATION & SEMANTIC COMMITS
- Execute in Agent Mode terminal:
  * `git add src/ docs/ tests/ requirements.txt`
  * `git commit -m "refactor(core): automated Pydantic v2 & FastAPI modernization via BobMigrate"`

STEP 6: GENERATE ENTERPRISE AUDIT & PR ARTIFACTS
- Create @MIGRATION_SUMMARY.md with file diff lists, applied rules, mypy report, benchmark throughput results, and pytest logs.
- Create @MIGRATION_SUMMARY.html featuring an interactive dark-mode dashboard with metric badges, side-by-side red/green code diffs, and terminal outputs.
- Create @PULL_REQUEST.md formatted as a professional GitHub PR body summarizing breaking changes, risk tier (Low), verification steps, and reviewer sign-off checklist.

Begin execution immediately with Step 1.