MIN_SHARPNESS_SCORE = 50.0
MIN_BRIGHTNESS = 40
MAX_BRIGHTNESS = 220

OCR_CONFIDENCE_WARNING_THRESHOLD = 60
MIN_OCR_MEAN_CONFIDENCE = 30.0

OCR_LANGUAGES = "rus+eng"

TD3_LINE_LENGTH = 44
MRZ_CROP_RATIO = 0.20

REQUIRED_FIELDS = [
    "last_name",
    "first_name",
    "birth_date",
    "document_number",
]

ALL_PASSPORT_FIELDS = [
    "last_name",
    "first_name",
    "middle_name",
    "birth_date",
    "document_number",
    "personal_number",
    "issue_date",
    "expiry_date",
    "issued_by",
    "nationality",
    "sex",
    "birth_place",
    "citizenship",
]

DATE_FIELDS = {"birth_date", "issue_date", "expiry_date"}

MRZ_PRIORITY_FIELDS = {
    "last_name",
    "first_name",
    "birth_date",
    "document_number",
    "expiry_date",
    "nationality",
    "sex",
    "personal_number",
}

VISUAL_ONLY_FIELDS = {
    "middle_name",
    "issue_date",
    "issued_by",
    "birth_place",
    "citizenship",
}

FIELD_PATTERNS = {
    "last_name": r"Фамилия[:\s]+([А-ЯЁ\-]+)",
    "first_name": r"Имя[:\s]+([А-ЯЁ\-]+)",
    "middle_name": r"Отчество[:\s]+([А-ЯЁ\-]+)",
    "birth_date": r"Дата рождения[:\s]+(\d{2}\.\d{2}\.\d{4})",
    "document_number": r"(?:№|N)\s*([А-Я]{2}\d{7})",
    "personal_number": r"(?:Идентификационный номер|Идентиф\. номер)[:\s]+([\dA-Z]+)",
    "issue_date": r"Дата выдачи[:\s]+(\d{2}\.\d{2}\.\d{4})",
    "expiry_date": r"(?:Действителен до|Срок действия)[:\s]+(\d{2}\.\d{2}\.\d{4})",
    "issued_by": r"Выдан[:\s]+(.+)",
    "nationality": r"(?:Код государства|Nationality)[:\s]+([A-Z]{3})",
    "sex": r"Пол[:\s]+([МЖMF]|Муж\.?|Жен\.?|Male|Female)",
    "birth_place": r"Место рождения[:\s]+(.+)",
    "citizenship": r"Гражданство[:\s]+(.+)",
}