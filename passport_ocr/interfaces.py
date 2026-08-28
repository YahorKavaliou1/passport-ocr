from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class BaseImageLoader(ABC):
    # Contract for loading a passport image from disk.

    @abstractmethod
    def load(self, path: str) -> np.ndarray:
        # Read and return the image as a numpy array.
        raise NotImplementedError


class BaseQualityChecker(ABC):
    # Contract for assessing whether an image is fit for OCR.

    @abstractmethod
    def assert_acceptable(self, image: np.ndarray):
        # Reject the image if quality is too poor for recognition.
        raise NotImplementedError


class BaseImagePreprocessor(ABC):
    # Contract for preparing a raw image for OCR and MRZ parsing.

    @abstractmethod
    def process(self, image: np.ndarray):
        # Apply preprocessing and return images ready for downstream steps.
        raise NotImplementedError


class BaseMRZParser(ABC):
    # Contract for detecting and parsing passport MRZ data.

    @abstractmethod
    def parse(self, image: np.ndarray, ocr_engine, full_text: str | None = None):
        # Extract and validate MRZ fields from the image or OCR text.
        raise NotImplementedError


class BaseFieldExtractor(ABC):
    # Contract for merging OCR and MRZ data into passport fields.

    @abstractmethod
    def extract(self, full_text: str, mrz_result=None):
        # Build structured passport fields from visual OCR and MRZ results.
        raise NotImplementedError


class BaseResultValidator(ABC):
    # Contract for building the final API response with validation rules.

    @abstractmethod
    def build(self, data, ocr_result, mrz_result=None, extraction_warnings=None):
        # Validate extracted data and return a success or failure result.
        raise NotImplementedError
