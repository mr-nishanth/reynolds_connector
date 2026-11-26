"""VIN validation rules: exactly 17 characters, alphanumeric, no I, O or Q."""

import re

VIN_LENGTH = 17
VIN_PATTERN = r"^[A-HJ-NPR-Z0-9]{17}$"
# Case-insensitive variant used for path validation; lowercase VINs are normalised.
VIN_PATTERN_CI = r"^[A-HJ-NPR-Za-hj-npr-z0-9]{17}$"

_VIN_RE = re.compile(VIN_PATTERN)


def normalise_vin(vin: str) -> str:
    """Return the VIN in upper case with surrounding whitespace removed."""
    return vin.strip().upper()


def is_valid_vin(vin: str) -> bool:
    """Return True when ``vin`` (after normalisation) satisfies the VIN rules."""
    return _VIN_RE.fullmatch(normalise_vin(vin)) is not None


def validate_vin(vin: str) -> str:
    """Return the normalised VIN or raise ValueError if it is invalid."""
    normalised = normalise_vin(vin)
    if not _VIN_RE.fullmatch(normalised):
        raise ValueError(
            "VIN must be 17 characters of letters (except I, O, Q) and digits"
        )
    return normalised
