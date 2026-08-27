"""Схемы данных: структура извлечённых полей и итогового результата."""
from typing import Optional

from pydantic import BaseModel, Field


class PassportData(BaseModel):
    """Извлечённые поля паспорта. Все опциональны — отсутствие не ломает сериализацию."""

    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[str] = None       # ISO-формат YYYY-MM-DD
    document_number: Optional[str] = None
    personal_number: Optional[str] = None
    issue_date: Optional[str] = None
    issued_by: Optional[str] = None


class FieldConfidence(BaseModel):
    """Служебная информация об уверенности распознавания конкретного поля."""

    field_name: str
    raw_value: Optional[str] = None
    confidence: Optional[float] = None      # 0-100
    is_valid_format: bool = True


class RecognitionResult(BaseModel):
    """Итоговый результат работы пайплайна — то, что сериализуется в JSON."""

    success: bool
    document_type: str = "passport"
    data: PassportData = Field(default_factory=PassportData)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)