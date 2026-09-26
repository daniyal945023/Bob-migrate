# Flask to FastAPI Migration Guide

1. **App Initialization**:
   - Replace `from flask import Flask, request, jsonify, Header` with `from fastapi import FastAPI, Header, HTTPException, status`.
   - Replace `app = Flask(__name__)` with `app = FastAPI(title="Migrated Modern API")`.

2. **Routes & Decorators**:
   - `@app.route('/path', methods=['GET'])` $\rightarrow$ `@app.get('/path')`
   - `@app.route('/path', methods=['POST'])` $\rightarrow$ `@app.post('/path', status_code=201)`

3. **Request Payload & Query Injection**:
   - Remove `request.get_json()`. Inject Pydantic models directly as body arguments: `def endpoint(payload: UserModel):`.
   - Path/Query params are inferred from function signature arguments.

4. **Headers & Security**:
   - Replace `request.headers.get('X-API-Key')` with type-annotated parameters: `x_api_key: Optional[str] = Header(None)`.

5. **Responses & Error Handling**:
   - Return raw dicts or Pydantic instances directly (remove `jsonify()`).
   - Replace `return jsonify({'error': 'msg'}), 400` with `raise HTTPException(status_code=400, detail='msg')`.