import re
from dataclasses import dataclass, field
from datetime import datetime

import cv2
import numpy as np
import pytesseract

from passport_ocr.ocr.engine import BaseOCREngine
from passport_ocr.ocr.tesseract_engine import MRZ_TESSERACT_CONFIG

TD3_LINE_LENGTH = 44
MRZ_CROP_RATIO = 0.20
MRZ_CHARSET = re.compile(r"^[A-Z0-9<]+$")

_AMBIGUOUS_SUBSTITUTIONS = {
    "O": "0",
    "0": "O",
    "I": "1",
    "1": "I",
    "L": "1",
    "B": "8",
    "8": "B",
}
_WEIGHTS = (7, 3, 1)


@dataclass
class MRZParseResult:
    is_valid: bool = False
    is_passport: bool = False
    lines: list[str] = field(default_factory=list)
    last_name: str | None = None
    first_name: str | None = None
    birth_date: str | None = None
    document_number: str | None = None
    nationality: str | None = None
    sex: str | None = None
    expiry_date: str | None = None
    personal_number: str | None = None
    warnings: list[str] = field(default_factory=list)


def parse_mrz(
    image: np.ndarray, ocr_engine: BaseOCREngine, full_text: str | None = None
) -> MRZParseResult:
    warnings: list[str] = []

    lines = detect_mrz_lines(image, ocr_engine)

    if len(lines) < 2 and full_text:
        text_lines = extract_mrz_from_text(full_text)
        if len(text_lines) >= 2:
            lines = text_lines[-2:]
            warnings.append("MRZ extracted from full-page OCR text")

    if len(lines) < 2:
        return MRZParseResult(
            is_valid=False, is_passport=False, warnings=[*warnings, "MRZ not detected"]
        )

    line1, line2 = normalize_mrz_line(lines[-2]), normalize_mrz_line(lines[-1])
    corrected_line1, corrected_line2, correction_warnings = correct_mrz_lines(line1, line2)
    warnings.extend(correction_warnings)

    return parse_td3(corrected_line1, corrected_line2, warnings)


def detect_mrz_lines(image: np.ndarray, ocr_engine: BaseOCREngine) -> list[str]:
    height = image.shape[0]
    crop_start = int(height * (1 - MRZ_CROP_RATIO))
    mrz_region = image[crop_start:, :]

    if mrz_region.ndim == 3:
        mrz_region = cv2.cvtColor(mrz_region, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(mrz_region, lang="eng", config=MRZ_TESSERACT_CONFIG)
    return extract_mrz_from_text(text)


def extract_mrz_from_text(text: str) -> list[str]:
    lines: list[str] = []

    for raw_line in text.upper().splitlines():
        line = re.sub(r"[^A-Z0-9<]", "", raw_line)
        if len(line) == TD3_LINE_LENGTH and MRZ_CHARSET.match(line):
            lines.append(line)
            continue

        if len(line) > TD3_LINE_LENGTH:
            for start in range(len(line) - TD3_LINE_LENGTH + 1):
                candidate = line[start : start + TD3_LINE_LENGTH]
                if MRZ_CHARSET.match(candidate):
                    lines.append(candidate)

    return lines


def normalize_mrz_line(line: str) -> str:
    normalized = re.sub(r"[^A-Z0-9<]", "", line.upper())
    if len(normalized) < TD3_LINE_LENGTH:
        normalized = normalized.ljust(TD3_LINE_LENGTH, "<")
    return normalized[:TD3_LINE_LENGTH]


def correct_mrz_lines(line1: str, line2: str) -> tuple[str, str, list[str]]:
    warnings: list[str] = []

    if _validate_td3_lines(line1, line2):
        return line1, line2, warnings

    corrected = _apply_ocr_corrections(line1, line2)
    if corrected != (line1, line2):
        warnings.append("MRZ OCR corrections applied")
        line1, line2 = corrected

    if not _validate_td3_lines(line1, line2):
        warnings.append("MRZ check-digit validation failed")

    return line1, line2, warnings


def parse_td3(line1: str, line2: str, warnings: list[str] | None = None) -> MRZParseResult:
    result_warnings = list(warnings or [])
    is_passport = line1.startswith("P")
    is_valid = _validate_td3_lines(line1, line2)

    last_name, first_name = _parse_mrz_name(line1[5:44])

    document_number = line2[0:9].replace("<", "").strip() or None
    nationality = line2[10:13].replace("<", "").strip() or None
    birth_date = _yymmdd_to_iso(line2[13:19], is_expiry=False)
    sex = line2[20] if line2[20] in {"M", "F", "<"} else None
    if sex == "<":
        sex = None
    expiry_date = _yymmdd_to_iso(line2[21:27], is_expiry=True)

    personal_number_raw = line2[28:42].replace("<", "").strip()
    personal_number = personal_number_raw or None

    return MRZParseResult(
        is_valid=is_valid,
        is_passport=is_passport,
        lines=[line1, line2],
        last_name=last_name,
        first_name=first_name,
        birth_date=birth_date,
        document_number=document_number,
        nationality=nationality,
        sex=sex,
        expiry_date=expiry_date,
        personal_number=personal_number,
        warnings=result_warnings,
    )


def _validate_td3_lines(line1: str, line2: str) -> bool:
    if len(line1) != TD3_LINE_LENGTH or len(line2) != TD3_LINE_LENGTH:
        return False
    if not line1.startswith("P"):
        return False

    if not validate_check_digit(line2[0:9], line2[9]):
        return False
    if not validate_check_digit(line2[13:19], line2[19]):
        return False
    if not validate_check_digit(line2[21:27], line2[27]):
        return False
    if not validate_check_digit(line2[28:42], line2[42]):
        return False

    composite_data = line2[0:10] + line2[13:20] + line2[21:28] + line2[28:43]
    return validate_check_digit(composite_data, line2[43])


def validate_check_digit(data: str, check: str) -> bool:
    if check == "<":
        return True
    if not check.isdigit():
        return False
    return compute_check_digit(data) == check


def compute_check_digit(data: str) -> str:
    total = sum(_char_value(char) * _WEIGHTS[index % 3] for index, char in enumerate(data))
    return str(total % 10)


def _char_value(char: str) -> int:
    if char == "<":
        return 0
    if char.isdigit():
        return int(char)
    if "A" <= char <= "Z":
        return ord(char) - ord("A") + 10
    return 0


def _parse_mrz_name(name_field: str) -> tuple[str | None, str | None]:
    surname, _, given_names = name_field.partition("<<")
    last_name = surname.replace("<", " ").strip() or None
    first_name = given_names.replace("<", " ").strip() or None
    return last_name, first_name


def _yymmdd_to_iso(value: str, is_expiry: bool) -> str | None:
    if len(value) != 6 or not value.isdigit():
        return None

    yy = int(value[0:2])
    mm = int(value[2:4])
    dd = int(value[4:6])

    if not (1 <= mm <= 12 and 1 <= dd <= 31):
        return None

    if is_expiry:
        year = 2000 + yy
    else:
        current_yy = datetime.now().year % 100
        year = 1900 + yy if yy > current_yy else 2000 + yy

    return f"{year:04d}-{mm:02d}-{dd:02d}"


def _apply_ocr_corrections(line1: str, line2: str) -> tuple[str, str]:
    candidates = [(line1, line2)]

    for line_index, line in enumerate((line1, line2)):
        for position, char in enumerate(line):
            replacement = _AMBIGUOUS_SUBSTITUTIONS.get(char)
            if replacement is None:
                continue

            current_line1, current_line2 = candidates[0]
            target_line = current_line1 if line_index == 0 else current_line2
            corrected_line = (
                target_line[:position] + replacement + target_line[position + 1 :]
            )

            if line_index == 0:
                candidate = (corrected_line, current_line2)
            else:
                candidate = (current_line1, corrected_line)

            if candidate not in candidates:
                candidates.append(candidate)

    for candidate_line1, candidate_line2 in candidates:
        if _validate_td3_lines(candidate_line1, candidate_line2):
            return candidate_line1, candidate_line2

    return line1, line2