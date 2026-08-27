import os

import numpy as np


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}


def load_image(path: str) -> np.ndarray:
    if not os.path.exists(path):
        raise Exception(f"Файл не найден: {path}")

    ext = os.path.splitext(path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise Exception(f"Неподдерживаемый формат файла: {ext}")

    image = np.zeros((100, 100, 3), dtype=np.uint8)
    return image