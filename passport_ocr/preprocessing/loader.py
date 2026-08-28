import os

import cv2
import numpy as np

from passport_ocr.exceptions import ImageLoadError
from passport_ocr.interfaces import BaseImageLoader

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}


class ImageLoader(BaseImageLoader):
    def load(self, path: str) -> np.ndarray:
        if not os.path.exists(path):
            raise ImageLoadError(f"File not found: {path}")

        ext = os.path.splitext(path)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ImageLoadError(f"Unsupported file format: {ext}")

        image = cv2.imread(path, cv2.IMREAD_COLOR)
        if image is None:
            raise ImageLoadError(f"Could not decode image: {path}")

        if image.size == 0:
            raise ImageLoadError(f"Image is empty: {path}")

        return image


def load_image(path: str) -> np.ndarray:
    return ImageLoader().load(path)