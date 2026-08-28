# Passport OCR

Extract structured data from passport images using preprocessing, OCR, MRZ parsing, and field validation.

## Requirements

- Python 3.10+
- Tesseract OCR with Belarusian, Russian, and English language packs

## Installation

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-bel tesseract-ocr-rus tesseract-ocr-eng
sudo apt-get install -y build-essential python3-dev libgl1 libglib2.0-0

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

```bash
python main.py --input /path/to/passport.jpg
python main.py --input /path/to/passport.jpg --output result.json
```

Supported image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`

## Output

On success:

```json
{
  "success": true,
  "document_type": "passport",
  "data": {
    "last_name": "IVANOV",
    "first_name": "IVAN",
    "birth_date": "1990-01-15",
    "document_number": "MP1234567"
  },
  "warnings": []
}
```

On failure:

```json
{
  "success": false,
  "document_type": "unknown",
  "data": null,
  "warnings": ["The document could not be recognized"]
}
```

Missing fields are returned as `null` with warnings — values are never guessed. Dates use `YYYY-MM-DD`.

## Pipeline

```
Passport image → preprocessing → OCR → MRZ parsing → field extraction → validation → JSON
```

| Stage | Purpose |
|-------|---------|
| Preprocessing | Grayscale, denoise, deskew, contrast, crop data page, upscale |
| OCR | Reads printed text (labels and values) from the passport page |
| MRZ parsing | Reads and validates the machine-readable zone at the bottom |
| Field extraction | Merges OCR + MRZ into 13 passport fields |
| Validation | Checks required fields, OCR confidence, document type |

## OCR and MRZ

Both are used because they cover different fields:

- **MRZ** — core identity data with check-digit validation (`last_name`, `first_name`, `birth_date`, `document_number`, `expiry_date`, `nationality`, `sex`, `personal_number`)
- **OCR** — visual-zone fields not in MRZ (`middle_name`, `issue_date`, `issued_by`, `birth_place`, `citizenship`) and fallback when MRZ is missing or unreliable

MRZ takes priority when valid; OCR fills gaps and visual-only fields.
