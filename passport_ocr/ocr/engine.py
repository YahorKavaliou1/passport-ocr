from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np


@dataclass
class OCRWordResult:
    text: str
    confidence: float


@dataclass
class OCRResult:
    full_text: str
    words: list[OCRWordResult] = field(default_factory=list)


class BaseOCREngine(ABC):

    @abstractmethod
    def recognize(self, image: np.ndarray) -> OCRResult:
        raise NotImplementedError