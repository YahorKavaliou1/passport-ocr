from passport_ocr.config import OCR_CONFIDENCE_WARNING_THRESHOLD, REQUIRED_FIELDS
from passport_ocr.extraction.mrz_parser import MRZParseResult
from passport_ocr.models import PassportData, RecognitionResult
from passport_ocr.ocr.engine import OCRResult


def build_result(
    data: PassportData,
    ocr_result: OCRResult,
    mrz_result: MRZParseResult | None,
    extraction_warnings: list[str] | None = None,
) -> RecognitionResult:
    warnings = _dedupe_warnings(list(extraction_warnings or []))

    warnings.extend(_check_ocr_confidence(ocr_result))
    warnings.extend(_check_mrz(mrz_result))
    warnings.extend(_check_required_fields(data))
    warnings = _dedupe_warnings(warnings)

    is_passport = _is_passport_document(mrz_result, data)

    if not is_passport:
        return RecognitionResult(
            success=False,
            document_type="unknown",
            data=None,
            warnings=_dedupe_warnings(
                [*warnings, "The document could not be recognized as a passport"]
            ),
        )

    missing_required = [
        field_name
        for field_name in REQUIRED_FIELDS
        if getattr(data, field_name) is None
    ]
    success = len(missing_required) == 0

    return RecognitionResult(
        success=success,
        document_type="passport",
        data=data if success else None,
        warnings=warnings,
    )


def _check_ocr_confidence(ocr_result: OCRResult) -> list[str]:
    if not ocr_result.words:
        return []

    mean_confidence = sum(word.confidence for word in ocr_result.words) / len(
        ocr_result.words
    )
    if mean_confidence < OCR_CONFIDENCE_WARNING_THRESHOLD:
        return [f"Low OCR confidence: {mean_confidence:.1f}%"]

    return []


def _check_mrz(mrz_result: MRZParseResult | None) -> list[str]:
    if mrz_result is None:
        return []

    warnings: list[str] = []

    if not mrz_result.lines:
        return warnings

    if not mrz_result.is_passport:
        warnings.append("Document is not a passport")

    return warnings


def _check_required_fields(data: PassportData) -> list[str]:
    warnings: list[str] = []

    for field_name in REQUIRED_FIELDS:
        if getattr(data, field_name) is None:
            warnings.append(f"Required field '{field_name}' is missing")

    return warnings


def _is_passport_document(
    mrz_result: MRZParseResult | None,
    data: PassportData,
) -> bool:
    if mrz_result and mrz_result.lines:
        return mrz_result.is_passport

    passport_indicators = sum(
        value is not None
        for value in (
            data.last_name,
            data.first_name,
            data.document_number,
            data.birth_date,
        )
    )
    return passport_indicators >= 2


def _dedupe_warnings(warnings: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_warnings: list[str] = []

    for warning in warnings:
        if warning in seen:
            continue
        seen.add(warning)
        unique_warnings.append(warning)

    return unique_warnings