from typing import Optional

from pydantic import BaseModel, Field


class PassportData(BaseModel):
    # Structured passport fields extracted from OCR and MRZ.

    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[str] = None          # ISO-формат YYYY-MM-DD
    document_number: Optional[str] = None
    personal_number: Optional[str] = None
    issue_date: Optional[str] = None          # ISO-формат YYYY-MM-DD
    expiry_date: Optional[str] = None         # ISO-формат YYYY-MM-DD
    issued_by: Optional[str] = None
    nationality: Optional[str] = None
    sex: Optional[str] = None
    birth_place: Optional[str] = None
    citizenship: Optional[str] = None


class FieldConfidence(BaseModel):
    # Per-field OCR confidence metadata for a single extracted value.

    field_name: str
    raw_value: Optional[str] = None
    confidence: Optional[float] = None      # 0-100
    is_valid_format: bool = True


class RecognitionResult(BaseModel):
    # Final API response returned by the pipeline.

    success: bool
    document_type: str = "passport"
    data: Optional[PassportData] = None
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list, exclude=True)
