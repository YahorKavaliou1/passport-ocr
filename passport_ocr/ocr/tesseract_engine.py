import numpy as np
import pytesseract
from pytesseract import Output

from passport_ocr.config import MIN_OCR_MEAN_CONFIDENCE, OCR_LANGUAGES
from passport_ocr.exceptions import OCRFailureError
from passport_ocr.ocr.engine import BaseOCREngine, OCRResult, OCRWordResult

_MIN_MEAN_CONFIDENCE = MIN_OCR_MEAN_CONFIDENCE
_TESSERACT_CONFIG = "--psm 4"
MRZ_TESSERACT_CONFIG = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"

_OCR_STRATEGIES = (
    ("eng", "--psm 4"),
    (OCR_LANGUAGES, "--psm 6"),
)


class TesseractOCREngine(BaseOCREngine):
    def __init__(self, languages: str = OCR_LANGUAGES, config: str = _TESSERACT_CONFIG) -> None:
        self.languages = languages
        self.config = config

    def recognize(self, image: np.ndarray) -> OCRResult:
        if image is None or image.size == 0:
            raise OCRFailureError("OCR could not recognize the text")

        merged_text_parts: list[str] = []
        all_words: list[OCRWordResult] = []

        for languages, config in _OCR_STRATEGIES:
            text, words = self._run_ocr(image, languages, config)
            if text:
                merged_text_parts.append(text)
            all_words.extend(words)

        full_text = "\n".join(merged_text_parts).strip()
        if not full_text:
            raise OCRFailureError("OCR could not recognize the text")

        if all_words:
            mean_confidence = sum(word.confidence for word in all_words) / len(all_words)
            if mean_confidence < _MIN_MEAN_CONFIDENCE:
                raise OCRFailureError("OCR confidence is too low")

        return OCRResult(full_text=full_text, words=all_words)

    def _run_ocr(
        self, image: np.ndarray, languages: str, config: str
    ) -> tuple[str, list[OCRWordResult]]:
        full_text = pytesseract.image_to_string(
            image, lang=languages, config=config
        ).strip()

        data = pytesseract.image_to_data(
            image, lang=languages, config=config, output_type=Output.DICT
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

        return full_text, words
