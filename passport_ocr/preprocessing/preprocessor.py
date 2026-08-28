from dataclasses import dataclass

import numpy as np

from passport_ocr.interfaces import BaseImagePreprocessor
from passport_ocr.preprocessing import deskew, image_ops


@dataclass(frozen=True)
class PreprocessedImage:
    ocr_image: np.ndarray
    mrz_image: np.ndarray


class ImagePreprocessor(BaseImagePreprocessor):
    def process(self, image: np.ndarray) -> PreprocessedImage:
        gray = image_ops.to_grayscale(image)
        gray = image_ops.denoise(gray)
        gray = deskew.deskew(gray)
        gray = image_ops.enhance_contrast(gray)
        gray = image_ops.crop_data_page(gray)

        return PreprocessedImage(ocr_image=image_ops.resize_for_ocr(gray), mrz_image=gray)
