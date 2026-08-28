import numpy as np
import pytesseract
from pytesseract import Output

from passport_ocr.config import OCR_LANGUAGES
from passport_ocr.exceptions import OCRFailureError
from passport_ocr.ocr.engine import BaseOCREngine, OCRResult, OCRWordResult

_MIN_MEAN_CONFIDENCE = 30.0
_TESSERACT_CONFIG = "--psm 6"
MRZ_TESSERACT_CONFIG = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"


class TesseractOCREngine(BaseOCREngine):
    def __init__(self, languages: str = OCR_LANGUAGES, config: str = _TESSERACT_CONFIG) -> None:
        self.languages = languages
        self.config = config

    def recognize(self, image: np.ndarray) -> OCRResult:
        if image is None or image.size == 0:
            raise OCRFailureError("OCR could not recognize the text")

        full_text = pytesseract.image_to_string(
            image, lang=self.languages, config=self.config
        ).strip()

        if not full_text:
            raise OCRFailureError("OCR could not recognize the text")

        words = self._extract_words(image)

        if words:
            mean_confidence = sum(word.confidence for word in words) / len(words)
            if mean_confidence < _MIN_MEAN_CONFIDENCE:
                raise OCRFailureError("OCR confidence is too low")

        return OCRResult(full_text=full_text, words=words)

    def _extract_words(self, image: np.ndarray) -> list[OCRWordResult]:
        data = pytesseract.image_to_data(
            image, lang=self.languages, config=self.config, output_type=Output.DICT,
        )

        words: list[OCRWordResult] = []
        for i, text in enumerate(data["text"]):
            text = text.strip()
            if not text:
                continue

            confidence = float(data["conf"][i])
            if confidence < 0:
                continue

            words.append(OCRWordResult(text=text, confidence=confidence))

        return words