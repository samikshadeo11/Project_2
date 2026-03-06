from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

# ADD TESSERACT PATH HERE
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def pdf_to_text(pdf_path):

    pages = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=r"C:\poppler-25.12.0\Library\bin"
    )

    text = ""

    for i, page in enumerate(pages):
        print(f"🔍 OCR on page {i+1}")
        page_text = pytesseract.image_to_string(page, lang="eng")
        text += page_text

    return text


# Sample PDF path
sample_pdf = r"data\sample_pdfs\Service1.pdf"

# Run OCR
raw_text = pdf_to_text(sample_pdf)

print("\nExtracted Text:\n")
print(raw_text)