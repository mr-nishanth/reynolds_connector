# Reynolds Connector

## Overview

The `reynolds-connector` repository contains the vendor-specific integration responsible for extracting dealership data from the Reynolds & Reynolds DMS and preparing it for migration into Tekion ARC.

This connector owns its Reynolds-specific authentication, navigation, extraction workflows, data handling, transformation and migration behaviour.

Reynolds workflows must be treated independently from all other vendor connectors.

## Responsibilities

- Connect to the authorized Reynolds DMS environment.
- Authenticate using the existing supported authentication mechanism.
- Navigate Reynolds-specific workflows.
- Extract supported dealership data.
- Handle Reynolds-specific extraction failures.
- Transform extracted data into the required ARC-compatible format.
- Preserve migration data integrity.
- Report extraction and processing errors.

## Vendor Identity

| Property | Value |
|---|---|
| Vendor | REYNOLDS |
| Repository | reynolds-connector |
| Target platform | Tekion ARC |
| Connector type | Vendor-specific DMS connector |

## Architecture

Document the actual implementation here:

- Authentication mechanism: To be documented
- Navigation mechanism: To be documented
- Extraction workflow: To be documented
- Supported data entities: To be documented
- Transformation and mapping: To be documented
- Error-handling strategy: To be documented

## Vendor-Specific Workflow

Document the actual Reynolds extraction sequence.

| Workflow | Extraction steps | Status |
|---|---|---|
| Customer data | To be documented | Pending |
| Vehicle data | To be documented | Pending |
| Deal data | To be documented | Pending |
| Service data | To be documented | Pending |

Do not assume Reynolds extraction steps correspond to steps in Automate, AutoSoft or CDK.

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

## AI Migration Agent Integration

This repository is registered under the logical vendor identifier `REYNOLDS`.

The central repository registry must resolve `REYNOLDS` to `reynolds-connector`.

The AI Migration Agent may:

- Investigate Reynolds-specific workflow failures.
- Analyze relevant source files and dependencies.
- Use Graphify to identify code relationships.
- Identify the probable root cause.
- Prepare a targeted implementation plan.
- Modify relevant source files in an isolated Docker workspace.
- Execute available tests.
- Produce a Git diff for deterministic validation.

Repository selection and access authorization remain backend responsibilities.

## Testing and Validation

Before creating a pull request:

- Run relevant unit tests.
- Run relevant integration tests where available.
- Execute configured lint and type checks.
- Inspect the complete Git diff.
- Confirm changes are limited to the intended connector.
- Check for unintended extraction and mapping regressions.

Document actual commands after repository inspection.

## Security

- Never commit dealership credentials, passwords, cookies or API tokens.
- Redact sensitive information from logs.
- Use approved secure credential handling.
- Preserve existing authentication and authorization controls.

## Documentation Maintenance

Update this README when Reynolds extraction workflows, supported entities, architecture or test procedures change.

**Note:** Actual Reynolds implementation details must be verified against the source code before treating this documentation as complete.
