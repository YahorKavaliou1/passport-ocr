import numpy as np


def detect_skew_angle(image: np.ndarray) -> float:
    return 0.0


def deskew(image: np.ndarray) -> np.ndarray:
    angle = detect_skew_angle(image)
    if abs(angle) < 0.5:
        return image
    # TODO: apply the angle
    return image