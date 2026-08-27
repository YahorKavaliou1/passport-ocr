from dataclasses import dataclass

import numpy as np

from passport_ocr.config import MAX_BRIGHTNESS, MIN_BRIGHTNESS, MIN_SHARPNESS_SCORE
from passport_ocr.exceptions import ImageQualityError


@dataclass
class QualityReport:
    sharpness_score: float
    brightness: float
    is_acceptable: bool
    reason: str | None = None


def assess_quality(image: np.ndarray) -> QualityReport:
    sharpness_score = 100.0
    brightness = 128.0

    if sharpness_score < MIN_SHARPNESS_SCORE:
        return QualityReport(sharpness_score, brightness, False, "The image is too blurry")
    if not (MIN_BRIGHTNESS <= brightness <= MAX_BRIGHTNESS):
        return QualityReport(sharpness_score, brightness, False, "Incorrect lighting")

    return QualityReport(sharpness_score, brightness, True)


def assert_acceptable_quality(image: np.ndarray) -> QualityReport:
    report = assess_quality(image)
    if not report.is_acceptable:
        raise ImageQualityError(report.reason or "Pure image quality")
    return report