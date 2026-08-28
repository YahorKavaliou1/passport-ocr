from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class BaseImageLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> np.ndarray:
        raise NotImplementedError


class BaseQualityChecker(ABC):
    @abstractmethod
    def assert_acceptable(self, image: np.ndarray):
        raise NotImplementedError


class BaseImagePreprocessor(ABC):
    @abstractmethod
    def process(self, image: np.ndarray):
        raise NotImplementedError


class BaseMRZParser(ABC):
    @abstractmethod
    def parse(self, image: np.ndarray, ocr_engine, full_text: str | None = None):
        raise NotImplementedError


class BaseFieldExtractor(ABC):
    @abstractmethod
    def extract(self, full_text: str, mrz_result=None):
        raise NotImplementedError


class BaseResultValidator(ABC):
    @abstractmethod
    def build(self, data, ocr_result, mrz_result=None, extraction_warnings=None):
        raise NotImplementedError
