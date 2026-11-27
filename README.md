# Reynolds Connector

## Project Overview

`reynolds-connector` is the vendor-specific integration for the Reynolds & Reynolds DMS. Its intended purpose is to extract dealership data from Reynolds and prepare it for migration into Tekion ARC.

This repository currently contains a small FastAPI service (the first step of the connector). The HTTP API is a sample surface with in-memory data; it does **not** yet implement any Reynolds DMS authentication, navigation or extraction behaviour.

| Property | Value |
|---|---|
| Vendor | REYNOLDS |
| Repository | reynolds-connector |
| Target platform | Tekion ARC |
| Connector type | Vendor-specific DMS connector |

## Prerequisites

- Python 3.11 or newer
- `pip` and the `venv` module (or another virtual environment tool)

## Project Structure

```
reynolds-connector/
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # This document
├── app/
│   ├── __init__.py       # Package marker; exposes `app`
│   ├── main.py           # FastAPI application entry point, GET / and GET /health
│   ├── schemas.py        # Pydantic request/response models
│   ├── store.py          # In-memory item store (sample data)
│   └── api/
│       ├── __init__.py
│       └── items.py      # /api/v1/items router
└── tests/
    ├── conftest.py       # Shared TestClient fixture and store reset
    ├── test_root_health.py
    └── test_items.py
```

## Environment and Dependency Setup

Dependencies are declared in `pyproject.toml`:

- Runtime: `fastapi`, `pydantic`, `uvicorn`
- Development (optional extra `dev`): `pytest`, `httpx` (required by FastAPI's `TestClient`)

Create and activate a virtual environment from the repository root:

```bash
python3.11 -m venv .venv          # any Python >= 3.11
source .venv/bin/activate         # Windows: .venv\Scripts\activate
```

## Installation

Install the project in editable mode with development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Running the FastAPI Server

From the repository root, with the virtual environment active:

```bash
uvicorn app.main:app --reload
```

The server listens on http://127.0.0.1:8000 by default.

## Running Automated Tests

```bash
python -m pytest -q
```

Tests use FastAPI's `TestClient` and reset the in-memory store before each test; no running server is needed.

## API Endpoints

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| GET | `/` | Welcome message | 200 | – |
| GET | `/health` | Health status (`{"status": "ok"}`) | 200 | – |
| GET | `/api/v1/items` | List sample items | 200 | – |
| GET | `/api/v1/items/{item_id}` | Get an item by integer ID (≥ 1) | 200 | 404 unknown ID, 422 invalid ID |
| POST | `/api/v1/items` | Create an item | 201 | 422 invalid payload |

### Item Model

Create request body (`POST /api/v1/items`):

```json
{
  "name": "Example",
  "description": "Optional text",
  "price": 10.5
}
```

- `name`: required, string, 1–100 characters.
- `description`: optional string, up to 500 characters.
- `price`: required number, must be `>= 0`.
- Unknown extra fields are rejected with 422.

Responses include the assigned `id` (integer):

```json
{
  "id": 4,
  "name": "Example",
  "description": "Optional text",
  "price": 10.5
}
```

### Example Requests

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/items
curl http://127.0.0.1:8000/api/v1/items/1
curl -X POST http://127.0.0.1:8000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Example", "price": 10.5}'
```

### Data Storage Limitation

Items are stored in memory. Data is seeded with three sample items on start-up, is not persisted, and resets when the process restarts.

## Swagger and API Documentation

With the server running:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

## Development Workflow

1. Create a branch for the change.
2. Set up the environment and install with `python -m pip install -e ".[dev]"`.
3. Make focused changes; keep routers in `app/api/`, models in `app/schemas.py`, and data access in `app/store.py`.
4. Add or update tests in `tests/` for every behaviour change.
5. Run `python -m pytest -q` and confirm all tests pass.
6. Start the server with `uvicorn app.main:app --reload` and check `/docs` for manual verification.
7. Inspect the complete `git diff` before opening a pull request. Confirm changes are limited to this connector.

Note: no `.gitignore`, lint or type-check configuration is present in this repository yet.

## Published API Contract: Vehicle Lookup

This repository exposes a FastAPI backend. Dependent repositories (for example `automate-connector`) must use exactly this contract.

### Endpoint

`GET /vehicles/{vin}`

- Path parameter `vin`: string, exactly 17 characters, letters and digits only, excluding `I`, `O` and `Q`. Lowercase input is accepted and normalised to uppercase before lookup.
- No request body, no authentication headers required by this endpoint.

### Response schema: `VehicleRecord`

| Field | Type | Description |
|---|---|---|
| `vin` | string | 17-character upper-case VIN |
| `make` | string | Vehicle make |
| `model` | string | Vehicle model |
| `year` | integer | Model year |

Example `200` body:

```json
{"vin": "1HGCM82633A004352", "make": "Honda", "model": "Accord", "year": 2003}
```

### Status codes

| Status | Meaning | Body |
|---|---|---|
| `200` | VIN found | `VehicleRecord` JSON |
| `404` | Well-formed VIN not in the store | `{"detail": "Vehicle not found"}` |
| `422` | VIN invalid (wrong length, contains `I`/`O`/`Q`, or non-alphanumeric) | FastAPI validation error body (`{"detail": [...]}`) |

### Data source limitation

The current lookup is an in-memory placeholder seeded with fixture VINs (`1HGCM82633A004352`, `5YJSA1E26HF000337`, `WBAPH5C55BA441234`). It is not backed by Reynolds DMS extraction yet and must not be treated as production data. Replace `VehicleStore` in `reynolds_connector/api/vehicles.py` when real extraction is wired in.

### Running the tests

```
python -m pytest -q
```

Tests run offline using FastAPI `TestClient`.

## Repository Development Guidelines

1. Preserve existing Reynolds extraction behaviour.
2. Investigate the relevant workflow and source code before making changes.
3. Keep modifications focused on the Jira Story.
4. Follow existing repository conventions.
5. Add or update relevant tests.
6. Avoid unrelated refactoring.
7. Do not modify other vendor repositories.

## Reynolds Connector Documentation Status

The Reynolds-specific sections below remain to be documented against the source code. Do not treat them as complete.

| Area | Status |
|---|---|
| Authentication mechanism | To be documented |
| Navigation mechanism | To be documented |
| Extraction workflow | To be documented |
| Supported data entities | To be documented |
| Transformation and mapping | To be documented |
| Error-handling strategy | To be documented |

| Reynolds workflow | Status |
|---|---|
| Customer data | Pending |
| Vehicle data | Pending |
| Deal data | Pending |
| Service data | Pending |

Do not assume Reynolds extraction steps correspond to steps in Automate, AutoSoft or CDK.

## AI Migration Agent Integration

This repository is registered under the logical vendor identifier `REYNOLDS`. The central repository registry must resolve `REYNOLDS` to `reynolds-connector`. Repository selection and access authorization remain backend responsibilities.

## Security

- Never commit dealership credentials, passwords, cookies or API tokens.
- Redact sensitive information from logs.
- Use approved secure credential handling.
- Preserve existing authentication and authorization controls.
