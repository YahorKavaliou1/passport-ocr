from passport_ocr.extraction.field_extractor import FieldExtractor
from passport_ocr.extraction.mrz_parser import MRZParser
from passport_ocr.interfaces import (
    BaseFieldExtractor,
    BaseImageLoader,
    BaseImagePreprocessor,
    BaseMRZParser,
    BaseQualityChecker,
    BaseResultValidator,
)
from passport_ocr.models import RecognitionResult
from passport_ocr.ocr.engine import BaseOCREngine
from passport_ocr.ocr.tesseract_engine import TesseractOCREngine
from passport_ocr.preprocessing.loader import ImageLoader
from passport_ocr.preprocessing.preprocessor import ImagePreprocessor
from passport_ocr.preprocessing.quality_check import QualityChecker
from passport_ocr.validation.error_mapper import PipelineErrorMapper
from passport_ocr.validation.result_builder import ResultValidator


class PassportOCRPipeline:
    def __init__(
        self,
        loader: BaseImageLoader | None = None,
        quality_checker: BaseQualityChecker | None = None,
        preprocessor: BaseImagePreprocessor | None = None,
        ocr_engine: BaseOCREngine | None = None,
        mrz_parser: BaseMRZParser | None = None,
        field_extractor: BaseFieldExtractor | None = None,
        result_validator: BaseResultValidator | None = None,
        error_mapper: PipelineErrorMapper | None = None,
    ) -> None:
        self._loader = loader or ImageLoader()
        self._quality_checker = quality_checker or QualityChecker()
        self._preprocessor = preprocessor or ImagePreprocessor()
        self._ocr_engine = ocr_engine or TesseractOCREngine()
        self._mrz_parser = mrz_parser or MRZParser()
        self._field_extractor = field_extractor or FieldExtractor()
        self._result_validator = result_validator or ResultValidator()
        self._error_mapper = error_mapper or PipelineErrorMapper()

    def run(self, image_path: str) -> RecognitionResult:
        try:
            image = self._loader.load(image_path)
            self._quality_checker.assert_acceptable(image)

            preprocessed = self._preprocessor.process(image)
            ocr_result = self._ocr_engine.recognize(preprocessed.ocr_image)
            mrz_result = self._mrz_parser.parse(
                preprocessed.mrz_image, self._ocr_engine, ocr_result.full_text
            )
            extraction = self._field_extractor.extract(ocr_result.full_text, mrz_result)

            return self._result_validator.build(
                extraction.data, ocr_result, mrz_result, extraction.warnings
            )

        except Exception as exc:
            return self._error_mapper.to_result(exc)
