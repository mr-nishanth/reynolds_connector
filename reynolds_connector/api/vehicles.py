"""Vehicle lookup endpoint and repository.

The repository is an in-memory placeholder seeded with fixture data. No Reynolds
DMS extraction client exists in this repository yet; replace ``VehicleStore`` with
the real data source when extraction is wired in.
"""

from typing import Mapping

from fastapi import APIRouter, HTTPException, Path

from reynolds_connector.api.schemas import ErrorResponse, VehicleRecord
from reynolds_connector.api.vin import VIN_PATTERN_CI, normalise_vin

# Deterministic fixture data. These are NOT production dealership records.
FIXTURE_VEHICLES: Mapping[str, VehicleRecord] = {
    record.vin: record
    for record in (
        VehicleRecord(
            vin="1HGCM82633A004352", make="Honda", model="Accord", year=2003
        ),
        VehicleRecord(
            vin="5YJSA1E26HF000337", make="Tesla", model="Model S", year=2017
        ),
        VehicleRecord(
            vin="WBAPH5C55BA441234", make="BMW", model="5 Series", year=2011
        ),
    )
}


class VehicleStore:
    """Lookup of vehicles by VIN."""

    def __init__(self, records: Mapping[str, VehicleRecord]) -> None:
        self._records = dict(records)

    def get(self, vin: str) -> VehicleRecord | None:
        return self._records.get(normalise_vin(vin))


default_store = VehicleStore(FIXTURE_VEHICLES)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get(
    "/{vin}",
    response_model=VehicleRecord,
    responses={
        404: {"model": ErrorResponse, "description": "Unknown VIN"},
        422: {"description": "Invalid VIN format"},
    },
)
def get_vehicle(
    vin: str = Path(pattern=VIN_PATTERN_CI, min_length=17, max_length=17),
) -> VehicleRecord:
    record = default_store.get(vin)
    if record is None:
        vin_normalised = normalise_vin(vin)
        raise HTTPException(
            status_code=404, detail=f"Vehicle not found: {vin_normalised}"
        )
    return record
