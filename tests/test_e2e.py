from pathlib import Path

from passport_ocr.pipeline import PassportOCRPipeline

PASS3_IMAGE = Path(__file__).resolve().parent.parent / "examples" / "pass3.jpg"


def test_pass3_end_to_end():
    result = PassportOCRPipeline().run(str(PASS3_IMAGE))

    assert result.success is True
    assert result.document_type == "passport"
    assert result.data is not None
    assert isinstance(result.warnings, list)

    data = result.data

    assert data.last_name == "JOHNSON"
    assert data.first_name == "EMILY"
    assert data.birth_date == "1988-02-02"
    assert data.document_number == "KB1234567"
    assert data.expiry_date == "2008-02-01"
    assert data.nationality == "BLR"
    assert data.sex == "F"
    assert data.birth_place == "HOMIEL REGION"
