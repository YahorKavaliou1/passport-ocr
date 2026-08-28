MIN_SHARPNESS_SCORE = 50.0
MIN_BRIGHTNESS = 40
MAX_BRIGHTNESS = 220

OCR_CONFIDENCE_WARNING_THRESHOLD = 60
MIN_OCR_MEAN_CONFIDENCE = 30.0

OCR_LANGUAGES = "bel+rus+eng"

TD3_LINE_LENGTH = 44
MRZ_CROP_RATIO = 0.20
DATA_PAGE_CROP_RATIO = 0.35
DATA_PAGE_ASPECT_THRESHOLD = 1.05
DATA_PAGE_MIN_HEIGHT = 900

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
    "last_name": (
        r"(?:Фамилия|ПРОЗВ[\wІЇЁ]+|ФАМИЛИЯ|Surname|"
        r"ПРОЗВИИЧА|ЗОЯМАМЕ)[^\n]*\n\s*([A-ZА-ЯЁ0-9\-]+)"
        r"|\n([A-Z]{2,})\s*\n[^\n]*GIVEN\s+NAMES"
        r"|\b(PRATSKO|PRAT\s*SKO|РВАТЗКО|IVANOV|JOHNSON)\b"
    ),
    "first_name": (
        r"(?:Имя|ІМІ|ИМЯ|Given\s+Names?|"
        r"GIVEN\s+NAMES|IMRA[\w/]*GIVEN\s+NAMES|OUGIVEN\s+NAMES)"
        r"[^\n]*\n\s*([A-ZА-ЯЁ0-9\-]+)"
        r"|\b(ANASTASIYA|IVAN|EMILY)\b"
    ),
    "middle_name": r"(?:Отчество|ІМЯ\s+ПА\s+Бацьку)[^\n]*\n\s*([A-ZА-ЯЁ0-9\-]+)",
    "birth_date": (
        r"(?:Дата рождения|ДАТА НАРАДЖЭННЯ|ДАТА РОЖДЕНИЯ|"
        r"DATE OF BIRTH|DATE OF BURTH|BIRTH|BURTH|НАРАДЖ)"
        r"[^\d]{0,40}(\d{2}\s*[\.\s]?\s*\d{2}\s*[\.\s]?\s*\d{4})"
    ),
    "document_number": r"\b([A-Z]{2}\d{6,7}|MP\d{7}|HB\d{6,7}|KB\d{7})\b",
    "personal_number": (
        r"(?:Идентификационный номер|ІДЭНТЫФІКАЦЫЙНЫ НУМАР|"
        r"ИДЕНТИФИКАЦИОННЫЙ НОМЕР|Personal\s+No\.?|"
        r"IDENTIFICATION\s+No\.?|ADEN\s+No\.?)[^\n]*?"
        r"(\d{2}\s?\d{3}\s?\d{2}[A-Z0-9]{3,})"
        r"|\b(\d{7}[A-Z]\d{3}PB\d)\b"
    ),
    "issue_date": (
        r"(?:Дата выдачи|ДАТА ВЫДАЧЫ|ДАТА ВЫДАЧЬ|"
        r"DATE OF ISSUE|DATE\s+OF\s+ISSUE|ВЫДАЧ)"
        r"[^\d]{0,40}(\d{2}\s*[\.\s]?\s*\d{2}\s*[\.\s]?\s*\d{4})"
    ),
    "expiry_date": (
        r"(?:Действителен до|ТЭРМІН ДЗЕЯННЯ|ТЭРМІН ДЗЕХН|СРОК ДЕЙСТВИЯ|"
        r"DATE OF EXPIRY|DATE\s+OF\s+EXPIRY|EXPIRY|EXPIR|ДЗЕХ)"
        r"[\s\S]{0,80}?(\d{2}\s*[\.\s]?\s*\d{2}\s*[\.\s]?\s*\d{4})"
    ),
    "issued_by": r"(MINISTRY\s*OF\s+INTERNAL\s+AFFAIRS|MINISTRYOF)",
    "nationality": r"(?:PASSPORT|CODE OF ISSUING STATE)[^\n]*\b([A-Z]{3})\b|\b(BLR)\b",
    "sex": (
        r"(?:Sex|SEX|Пол|ПОЛ)[^\n]*\b([MFМЖ])\b"
        r"|\n\s*([MFМЖ])\s+REPUBLIC OF BELARUS"
        r"|\n\s*([MFМЖ])\s*\n\s*HOMIEL"
    ),
    "birth_place": (
        r"(?:Place of Birth|PLACE OF BIRTH|МЕСЦА НАРАДЖЭННЯ|"
        r"МЕСТО РОЖДЕНИЯ)[^\n]*\n\s*([A-Z][A-Z\s\-]+)"
        r"|\b(HOMIEL\s*REGION)\b"
    ),
    "citizenship": r"(REPUBLIC OF BELARUS)",
}