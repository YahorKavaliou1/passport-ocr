# Passport OCR

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng
sudo apt-get install -y build-essential python3-dev libgl1 libglib2.0-0

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -c "import cv2, pytesseract, pydantic, numpy, PIL; print('Все зависимости импортированы успешно')"
python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
```
