from dataclasses import dataclass

import cv2
import numpy as np

from passport_ocr.config import MAX_BRIGHTNESS, MIN_BRIGHTNESS, MIN_SHARPNESS_SCORE
from passport_ocr.exceptions import ImageQualityError
from passport_ocr.interfaces import BaseQualityChecker


@dataclass
class QualityReport:
    # Outcome of an image sharpness and brightness assessment.

    sharpness_score: float
    brightness: float
    is_acceptable: bool
    reason: str | None = None


class QualityChecker(BaseQualityChecker):
    # Checks whether an image is sharp and lit well enough for OCR.

    def assess(self, image: np.ndarray) -> QualityReport:
        # Measure sharpness and brightness without raising an error.
        gray = self._to_grayscale(image)

        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness_score = float(laplacian.var())
        brightness = float(np.mean(gray))

        if sharpness_score < MIN_SHARPNESS_SCORE:
            return QualityReport(
                sharpness_score, brightness, False, "The image is too blurry"
            )

        if not (MIN_BRIGHTNESS <= brightness <= MAX_BRIGHTNESS):
            return QualityReport(
                sharpness_score, brightness, False, "Incorrect lighting"
            )

        return QualityReport(sharpness_score, brightness, True)

    def assert_acceptable(self, image: np.ndarray) -> QualityReport:
        # Reject the image when quality falls below configured thresholds.
        report = self.assess(image)
        if not report.is_acceptable:
            raise ImageQualityError(report.reason or "Poor image quality")
        return report

    def _to_grayscale(self, image: np.ndarray) -> np.ndarray:
        if image.ndim == 2:
            return image
        if image.ndim == 3 and image.shape[2] == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        raise ImageQualityError("Unsupported image format for quality assessment")


def assess_quality(image: np.ndarray) -> QualityReport:
    # Convenience wrapper around QualityChecker.assess.
    return QualityChecker().assess(image)


def assert_acceptable_quality(image: np.ndarray) -> QualityReport:
    # Convenience wrapper around QualityChecker.assert_acceptable.
    return QualityChecker().assert_acceptable(image)
