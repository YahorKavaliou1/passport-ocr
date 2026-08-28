from passport_ocr.extraction.field_extractor import FieldExtractor
from passport_ocr.extraction.mrz_parser import MRZParser
from passport_ocr.ocr.tesseract_engine import TesseractOCREngine
from passport_ocr.pipeline import PassportOCRPipeline
from passport_ocr.preprocessing.loader import ImageLoader
from passport_ocr.preprocessing.preprocessor import ImagePreprocessor
from passport_ocr.preprocessing.quality_check import QualityChecker
from passport_ocr.validation.error_mapper import PipelineErrorMapper
from passport_ocr.validation.result_builder import ResultValidator


def create_pipeline() -> PassportOCRPipeline:
    # Build a pipeline with the default production dependencies.
    return PassportOCRPipeline(
        loader=ImageLoader(),
        quality_checker=QualityChecker(),
        preprocessor=ImagePreprocessor(),
        ocr_engine=TesseractOCREngine(),
        mrz_parser=MRZParser(),
        field_extractor=FieldExtractor(),
        result_validator=ResultValidator(),
        error_mapper=PipelineErrorMapper(),
    )
