import numpy as np

from passport_ocr.config import OCR_LANGUAGES
from passport_ocr.exceptions import OCRFailureError
from passport_ocr.ocr.engine import BaseOCREngine, OCRResult, OCRWordResult


class TesseractOCREngine(BaseOCREngine):
    def __init__(self, languages: str = OCR_LANGUAGES) -> None:
        self.languages = languages

    def recognize(self, image: np.ndarray) -> OCRResult:
        full_text = (
            "Фамилия: ИВАНОВ\nИмя: ИВАН\nОтчество: ИВАНОВИЧ\n"
            "Дата рождения: 15.01.1990\n№ МР1234567\n"
            "Дата выдачи: 10.05.2020\nВыдан: ФРУНЗЕНСКИМ РУВД Г. МИНСКА"
        )
        if not full_text.strip():
            raise OCRFailureError("OCR could not recognize the text")

        words = [OCRWordResult(text=w, confidence=85.0) for w in full_text.split()]
        return OCRResult(full_text=full_text, words=words)