import cv2
import numpy as np

from passport_ocr.config import (
    DATA_PAGE_ASPECT_THRESHOLD,
    DATA_PAGE_CROP_RATIO,
    DATA_PAGE_MIN_HEIGHT,
)


def to_grayscale(image: np.ndarray) -> np.ndarray:
    # Convert a BGR color image to single-channel grayscale.
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def denoise(image: np.ndarray) -> np.ndarray:
    # Remove sensor noise while preserving text edges.
    return cv2.fastNlMeansDenoising(image, h=10)


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    # Boost local contrast with CLAHE to improve OCR readability.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)


def binarize(image: np.ndarray) -> np.ndarray:
    # Convert grayscale to black-and-white using adaptive thresholding.
    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )


def resize_for_ocr(image: np.ndarray, target_width: int = 1600) -> np.ndarray:
    # Upscale narrow images so Tesseract has enough resolution to read text.
    height, width = image.shape[:2]
    if width >= target_width:
        return image

    scale = target_width / width
    new_height = int(height * scale)
    return cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_CUBIC)


def crop_data_page(
    image: np.ndarray,
    top_ratio: float = DATA_PAGE_CROP_RATIO,
    aspect_threshold: float = DATA_PAGE_ASPECT_THRESHOLD,
    min_height: int = DATA_PAGE_MIN_HEIGHT,
) -> np.ndarray:
    # Crop the top cover page from two-page passport scans.
    height, width = image.shape[:2]
    if height < min_height or height / width < aspect_threshold:
        return image

    crop_start = int(height * top_ratio)
    return image[crop_start:, :]
