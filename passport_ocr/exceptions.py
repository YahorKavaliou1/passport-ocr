class PassportOCRError(Exception):
    # Base exception for all passport OCR pipeline errors.
    pass


class ImageLoadError(PassportOCRError):
    # Raised when the image file cannot be found or decoded.
    pass


class ImageQualityError(PassportOCRError):
    # Raised when the image is too blurry or poorly lit for OCR.
    pass


class OCRFailureError(PassportOCRError):
    # Raised when Tesseract fails to produce usable text.
    pass


class MRZValidationError(PassportOCRError):
    # Raised when MRZ check-digit or format validation fails.
    pass


class NonPassportDocumentError(PassportOCRError):
    # Raised when the document is not recognized as a passport.
    pass
