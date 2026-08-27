import os

import numpy as np

from passport_ocr.exceptions import ImageLoadError

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}


def load_image(path: str) -> np.ndarray:
    if not os.path.exists(path):
        raise ImageLoadError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ImageLoadError(f"Unsupported file format: {ext}")

    image = np.zeros((100, 100, 3), dtype=np.uint8)
    return image