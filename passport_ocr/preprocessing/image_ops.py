import numpy as np


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """TODO: cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)"""
    return image


def denoise(image: np.ndarray) -> np.ndarray:
    """TODO: cv2.fastNlMeansDenoising(image) или cv2.medianBlur(image, 3)"""
    return image


def binarize(image: np.ndarray) -> np.ndarray:
    """TODO: cv2.adaptiveThreshold(...)"""
    return image


def resize_for_ocr(image: np.ndarray, target_width: int = 1600) -> np.ndarray:
    """TODO: cv2.resize"""
    return image