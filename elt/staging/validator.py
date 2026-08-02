"""
elt/staging/validator.py

Validation layer for the NIVAAS staging pipeline.

Responsible for inspecting raw JSONB payloads coming from raw.raw_listing
and determining whether a record is eligible for transformation and
persistence into staging.staging_listing.

Validation rules (per project spec):
    - rent must be present and > 0
    - area_sqft must be present and > 0
    - bhk must be present and > 0
    - locality must be present (non-empty string)
    - property_type must be present (non-empty string)

This module performs NO mutation of the payload. It only inspects values
and reports structured validation issues. Numeric coercion helpers are
exposed here so transformer.py can reuse identical parsing semantics.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from uuid import UUID


class ValidationErrorCode(str, Enum):
    MISSING_FIELD = "MISSING_FIELD"
    INVALID_TYPE = "INVALID_TYPE"
    NON_POSITIVE_VALUE = "NON_POSITIVE_VALUE"
    EMPTY_STRING = "EMPTY_STRING"
    OUT_OF_RANGE = "OUT_OF_RANGE"


@dataclass(frozen=True)
class ValidationIssue:
    field_name: str
    code: ValidationErrorCode
    message: str


@dataclass
class ValidationResult:
    raw_listing_id: UUID
    is_valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)

    def add_issue(self, field_name: str, code: ValidationErrorCode, message: str) -> None:
        self.issues.append(ValidationIssue(field_name=field_name, code=code, message=message))
        self.is_valid = False

    def issues_as_dicts(self) -> list[dict[str, str]]:
        return [
            {
                "field": issue.field_name,
                "code": issue.code.value,
                "message": issue.message,
            }
            for issue in self.issues
        ]


def safe_str(value: Any) -> Optional[str]:
    """Coerce a raw payload value into a trimmed string, or None if unusable."""
    if value is None:
        return None
    if isinstance(value, str):
        trimmed = value.strip()
        return trimmed if trimmed else None
    if isinstance(value, (int, float)):
        return str(value).strip()
    return None


def safe_float(value: Any) -> Optional[float]:
    """Coerce a raw payload value into a float, or None if unusable/non-finite."""
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        result = float(value)
        if math.isnan(result) or math.isinf(result):
            return None
        return result
    if isinstance(value, str):
        stripped = value.strip().replace(",", "")
        if not stripped:
            return None
        try:
            result = float(stripped)
        except ValueError:
            return None
        if math.isnan(result) or math.isinf(result):
            return None
        return result
    return None


def safe_int(value: Any) -> Optional[int]:
    """Coerce a raw payload value into an int, or None if unusable."""
    as_float = safe_float(value)
    if as_float is None:
        return None
    if not as_float.is_integer():
        return int(round(as_float))
    return int(as_float)


class RawListingValidator:
    """Validates a single raw_listing payload against NIVAAS staging rules."""

    REQUIRED_STRING_FIELDS: tuple[str, ...] = ("locality", "property_type")
    REQUIRED_POSITIVE_NUMERIC_FIELDS: tuple[str, ...] = ( "price","area","bedroom")
    @classmethod
    def validate(cls, raw_listing_id: UUID, payload: dict[str, Any]) -> ValidationResult:
        result = ValidationResult(raw_listing_id=raw_listing_id, is_valid=True)

        if not isinstance(payload, dict):
            result.add_issue(
                field_name="__payload__",
                code=ValidationErrorCode.INVALID_TYPE,
                message="Payload is not a JSON object.",
            )
            return result

        cls._validate_required_strings(payload, result)
        cls._validate_required_positive_numerics(payload, result)
        cls._validate_optional_geo(payload, result)

        return result

    @classmethod
    def _validate_required_strings(cls, payload: dict[str, Any], result: ValidationResult) -> None:
        for field_name in cls.REQUIRED_STRING_FIELDS:
            raw_value = payload.get(field_name)
            value = safe_str(raw_value)
            if raw_value is None:
                result.add_issue(
                    field_name=field_name,
                    code=ValidationErrorCode.MISSING_FIELD,
                    message=f"'{field_name}' is missing.",
                )
            elif value is None:
                result.add_issue(
                    field_name=field_name,
                    code=ValidationErrorCode.EMPTY_STRING,
                    message=f"'{field_name}' is present but empty or blank.",
                )

    @classmethod
    def _validate_required_positive_numerics(
        cls, payload: dict[str, Any], result: ValidationResult
    ) -> None:
        for field_name in cls.REQUIRED_POSITIVE_NUMERIC_FIELDS:
            raw_value = payload.get(field_name)
            if raw_value is None:
                result.add_issue(
                    field_name=field_name,
                    code=ValidationErrorCode.MISSING_FIELD,
                    message=f"'{field_name}' is missing.",
                )
                continue

            numeric_value = safe_float(raw_value)
            if numeric_value is None:
                result.add_issue(
                    field_name=field_name,
                    code=ValidationErrorCode.INVALID_TYPE,
                    message=f"'{field_name}' could not be parsed as a number.",
                )
                continue

            if numeric_value <= 0:
                result.add_issue(
                    field_name=field_name,
                    code=ValidationErrorCode.NON_POSITIVE_VALUE,
                    message=f"'{field_name}' must be greater than 0, got {numeric_value}.",
                )

    @classmethod
    def _validate_optional_geo(cls, payload: dict[str, Any], result: ValidationResult) -> None:
        latitude_raw = payload.get("latitude")
        longitude_raw = payload.get("longitude")

        if latitude_raw is None and longitude_raw is None:
            return

        latitude = safe_float(latitude_raw)
        longitude = safe_float(longitude_raw)

        if latitude_raw is not None and latitude is None:
            result.add_issue(
                field_name="latitude",
                code=ValidationErrorCode.INVALID_TYPE,
                message="'latitude' could not be parsed as a number.",
            )
        elif latitude is not None and not (-90.0 <= latitude <= 90.0):
            result.add_issue(
                field_name="latitude",
                code=ValidationErrorCode.OUT_OF_RANGE,
                message=f"'latitude' out of valid range [-90, 90], got {latitude}.",
            )

        if longitude_raw is not None and longitude is None:
            result.add_issue(
                field_name="longitude",
                code=ValidationErrorCode.INVALID_TYPE,
                message="'longitude' could not be parsed as a number.",
            )
        elif longitude is not None and not (-180.0 <= longitude <= 180.0):
            result.add_issue(
                field_name="longitude",
                code=ValidationErrorCode.OUT_OF_RANGE,
                message=f"'longitude' out of valid range [-180, 180], got {longitude}.",
            )
