class PassportOCRError(Exception):
    pass


class ImageLoadError(PassportOCRError):
    pass


class ImageQualityError(PassportOCRError):
    pass


class OCRFailureError(PassportOCRError):
    pass