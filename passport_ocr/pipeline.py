from passport_ocr.extraction.field_extractor import extract_fields
from passport_ocr.models import RecognitionResult
from passport_ocr.ocr.tesseract_engine import TesseractOCREngine
from passport_ocr.preprocessing import deskew, image_ops
from passport_ocr.preprocessing.loader import load_image
from passport_ocr.preprocessing.quality_check import assert_acceptable_quality
from passport_ocr.validation.result_builder import build_result


class PassportOCRPipeline:
    def __init__(self) -> None:
        self.ocr_engine = TesseractOCREngine()

    def run(self, image_path: str) -> RecognitionResult:
        try:
            image = load_image(image_path)
            assert_acceptable_quality(image)

            image = image_ops.to_grayscale(image)
            image = image_ops.denoise(image)
            image = deskew.deskew(image)
            image = image_ops.binarize(image)
            image = image_ops.resize_for_ocr(image)

            ocr_result = self.ocr_engine.recognize(image)
            data = extract_fields(ocr_result.full_text)

            return build_result(data, ocr_result)

        except Exception:
            # TODO: make correct handling
            raise