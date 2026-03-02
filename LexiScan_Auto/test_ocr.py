import pytesseract
from PIL import Image

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Check version
print("✅ Tesseract version:", pytesseract.get_tesseract_version())
print("✅ OCR setup complete!")