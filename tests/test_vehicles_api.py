"""Tests for GET /vehicles/{vin} and the VIN validation rules."""

import pytest
from fastapi.testclient import TestClient

from reynolds_connector.api.app import app
from reynolds_connector.api.vin import is_valid_vin, validate_vin

client = TestClient(app)

KNOWN_VIN = "1HGCM82633A004352"


def test_get_known_vehicle_returns_vehicle_record():
    response = client.get(f"/vehicles/{KNOWN_VIN}")
    assert response.status_code == 200
    assert response.json() == {
        "vin": KNOWN_VIN,
        "make": "Honda",
        "model": "Accord",
        "year": 2003,
    }
    assert isinstance(response.json()["year"], int)


def test_unknown_vin_returns_404():
    response = client.get("/vehicles/ZZZZZ0000000000ZZ")
    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}


def test_wrong_length_vin_returns_422():
    assert client.get("/vehicles/1HGCM8263").status_code == 422
    assert client.get("/vehicles/1HGCM82633A0043521").status_code == 422


def test_vin_with_I_O_Q_returns_422():
    for bad in ("1HGCM82633A00435I", "1HGCM82633A00435O", "1HGCM82633A00435Q"):
        assert client.get(f"/vehicles/{bad}").status_code == 422


def test_non_alphanumeric_vin_returns_422():
    assert client.get("/vehicles/1HGCM82633A00435-").status_code == 422
    assert client.get("/vehicles/1HGCM82633A00435%20").status_code == 422


def test_lowercase_vin_is_normalised():
    response = client.get(f"/vehicles/{KNOWN_VIN.lower()}")
    assert response.status_code == 200
    assert response.json()["vin"] == KNOWN_VIN


@pytest.mark.parametrize(
    "vin, expected",
    [
        (KNOWN_VIN, True),
        (KNOWN_VIN.lower(), True),
        ("1HGCM82633A00435I", False),
        ("1HGCM82633A00435O", False),
        ("1HGCM82633A00435Q", False),
        ("1HGCM8263", False),
        ("", False),
        ("1HGCM82633A00435-", False),
    ],
)
def test_vin_validator_accepts_valid_and_rejects_invalid(vin, expected):
    assert is_valid_vin(vin) is expected


def test_validate_vin_returns_normalised_value():
    assert validate_vin(f" {KNOWN_VIN.lower()} ") == KNOWN_VIN


def test_validate_vin_raises_for_invalid():
    with pytest.raises(ValueError):
        validate_vin("1HGCM82633A00435I")
