from passport_ocr.extraction.field_extractor import extract_fields
from passport_ocr.extraction.mrz_parser import parse_mrz
from passport_ocr.exceptions import (
    ImageLoadError, ImageQualityError, OCRFailureError, PassportOCRError
)
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
            image = image_ops.enhance_contrast(image)
            image = image_ops.crop_data_page(image)

            mrz_image = image

            ocr_image = image_ops.resize_for_ocr(image)
            ocr_result = self.ocr_engine.recognize(ocr_image)
            mrz_result = parse_mrz(
                mrz_image, self.ocr_engine, ocr_result.full_text
            )
            extraction = extract_fields(ocr_result.full_text, mrz_result)

            return build_result(
                extraction.data, ocr_result, mrz_result, extraction.warnings
            )

        except ImageLoadError as exc:
            return RecognitionResult(
                success=False,
                document_type="unknown",
                data=None,
                warnings=[str(exc)],
            )

        except ImageQualityError as exc:
            return RecognitionResult(
                success=False,
                document_type="unknown",
                data=None,
                warnings=[str(exc)],
            )

        except OCRFailureError:
            return RecognitionResult(
                success=False,
                document_type="unknown",
                data=None,
                warnings=["OCR could not recognize the text"],
            )

        except PassportOCRError as exc:
            return RecognitionResult(
                success=False,
                document_type="unknown",
                data=None,
                warnings=[str(exc)],
            )

        except Exception:
            return RecognitionResult(
                success=False,
                document_type="unknown",
                data=None,
                warnings=["The document could not be recognized"],
            )