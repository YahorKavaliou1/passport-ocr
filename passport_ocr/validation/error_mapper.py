from passport_ocr.exceptions import (
    ImageLoadError,
    ImageQualityError,
    OCRFailureError,
    PassportOCRError,
)
from passport_ocr.models import RecognitionResult


class PipelineErrorMapper:
    def to_result(self, exc: Exception) -> RecognitionResult:
        if isinstance(exc, ImageLoadError):
            return self._failure(str(exc))
        if isinstance(exc, ImageQualityError):
            return self._failure(str(exc))
        if isinstance(exc, OCRFailureError):
            return self._failure("OCR could not recognize the text")
        if isinstance(exc, PassportOCRError):
            return self._failure(str(exc))
        return self._failure("The document could not be recognized")

    def _failure(self, message: str) -> RecognitionResult:
        return RecognitionResult(
            success=False, document_type="unknown", data=None, warnings=[message]
        )
