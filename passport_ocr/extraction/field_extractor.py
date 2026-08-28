import re
from dataclasses import dataclass, field
from datetime import datetime

from passport_ocr.config import (
    DATE_FIELDS, FIELD_PATTERNS, MRZ_PRIORITY_FIELDS, VISUAL_ONLY_FIELDS
)
from passport_ocr.extraction.mrz_parser import MRZParseResult
from passport_ocr.models import PassportData


@dataclass
class FieldExtractionResult:
    data: PassportData
    warnings: list[str] = field(default_factory=list)


def extract_fields(
    full_text: str, mrz_result: MRZParseResult | None = None
) -> FieldExtractionResult:
    warnings: list[str] = []
    visual_fields = _extract_visual_fields(full_text, warnings)

    if mrz_result:
        warnings.extend(mrz_result.warnings)

    extracted: dict[str, str | None] = {
        field_name: None for field_name in PassportData.model_fields
    }

    for field_name in VISUAL_ONLY_FIELDS:
        extracted[field_name] = visual_fields.get(field_name)

    for field_name in MRZ_PRIORITY_FIELDS:
        mrz_value = _get_mrz_value(mrz_result, field_name)
        visual_value = visual_fields.get(field_name)

        if mrz_result and mrz_result.is_valid and mrz_value is not None:
            extracted[field_name] = mrz_value
            if visual_value and not _values_equal(mrz_value, visual_value, field_name):
                warnings.append(
                    f"Conflict between MRZ and visual text for '{field_name}'; MRZ value used"
                )
            continue

        if visual_value is not None:
            extracted[field_name] = visual_value
            continue

        if mrz_value is not None:
            extracted[field_name] = mrz_value
            if mrz_result and not mrz_result.is_valid:
                warnings.append(f"'{field_name}' taken from unvalidated MRZ")

    data = PassportData(**extracted)

    for field_name in PassportData.model_fields:
        if getattr(data, field_name) is None:
            warnings.append(f"Field '{field_name}' could not be extracted")

    return FieldExtractionResult(data=data, warnings=warnings)


def _extract_visual_fields(full_text: str, warnings: list[str]) -> dict[str, str]:
    results: dict[str, str] = {}

    for field_name, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, full_text, re.IGNORECASE | re.MULTILINE)
        if not match:
            continue

        raw_value = _clean_text(match.group(1))
        if not raw_value:
            continue

        if field_name in DATE_FIELDS:
            iso_date, warning = _parse_visual_date(raw_value)
            if warning:
                warnings.append(warning)
            if iso_date:
                results[field_name] = iso_date
            continue

        if field_name == "sex":
            normalized_sex = _normalize_sex(raw_value)
            if normalized_sex:
                results[field_name] = normalized_sex
            else:
                warnings.append(f"Invalid sex value: {raw_value}")
            continue

        results[field_name] = raw_value

    return results


def _get_mrz_value(
    mrz_result: MRZParseResult | None, field_name: str
) -> str | None:
    if mrz_result is None:
        return None
    return getattr(mrz_result, field_name, None)


def _parse_visual_date(raw_value: str) -> tuple[str | None, str | None]:
    try:
        parsed = datetime.strptime(raw_value.strip(), "%d.%m.%Y")
    except ValueError:
        return None, f"Invalid date format: {raw_value}"

    return parsed.strftime("%Y-%m-%d"), None


def _normalize_sex(raw_value: str) -> str | None:
    normalized = raw_value.strip().upper()

    if normalized in {"M", "М", "MALE", "МУЖ", "МУЖ."}:
        return "M"
    if normalized in {"F", "Ж", "FEMALE", "ЖЕН", "ЖЕН."}:
        return "F"

    return None


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _values_equal(left: str, right: str, field_name: str) -> bool:
    if field_name in {"last_name", "first_name", "middle_name", "issued_by", "birth_place", "citizenship"}:
        return _clean_text(left).upper() == _clean_text(right).upper()

    if field_name == "document_number":
        return left.replace(" ", "").upper() == right.replace(" ", "").upper()

    return left == right