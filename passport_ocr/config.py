MIN_SHARPNESS_SCORE = 50.0
MIN_BRIGHTNESS = 40
MAX_BRIGHTNESS = 220

OCR_CONFIDENCE_WARNING_THRESHOLD = 60

OCR_LANGUAGES = "rus+eng"

REQUIRED_FIELDS = ["last_name", "first_name", "birth_date", "document_number"]

FIELD_PATTERNS = {
    "last_name": r"Фамилия[:\s]+([А-ЯЁ\-]+)",
    "first_name": r"Имя[:\s]+([А-ЯЁ\-]+)",
    "middle_name": r"Отчество[:\s]+([А-ЯЁ\-]+)",
    "birth_date": r"Дата рождения[:\s]+(\d{2}\.\d{2}\.\d{4})",
    "document_number": r"(?:№|N)\s*([А-Я]{2}\d{7})",
    "issue_date": r"Дата выдачи[:\s]+(\d{2}\.\d{2}\.\d{4})",
    "issued_by": r"Выдан[:\s]+(.+)",
}