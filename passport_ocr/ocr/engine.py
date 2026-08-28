from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np


@dataclass
class OCRWordResult:
    # A single word recognized by OCR with its confidence score.

    text: str
    confidence: float


@dataclass
class OCRResult:
    # Full OCR output: combined text and per-word confidence data.

    full_text: str
    words: list[OCRWordResult] = field(default_factory=list)


class BaseOCREngine(ABC):
    # Contract for running OCR on a preprocessed image.

    @abstractmethod
    def recognize(self, image: np.ndarray) -> OCRResult:
        # Extract text and word-level confidence from the image.
        raise NotImplementedError
