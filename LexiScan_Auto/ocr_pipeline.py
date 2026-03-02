# PURPOSE: Convert PDF contracts into clean text using OCR

import pytesseract
from pdf2image import convert_from_path
import re
import os

# Explicit Tesseract path (Windows safety)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def pdf_to_text(pdf_path):
    """
    Converts PDF pages to raw OCR text
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    print(f"📄 Reading PDF: {pdf_path}")

    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ""

    for i, page in enumerate(pages):
        print(f"🔍 OCR on page {i + 1}")
        text = pytesseract.image_to_string(page, lang="eng")
        full_text += text + "\n"

    return full_text


def clean_text(text):
    """
    Cleans OCR output
    """
    text = re.sub(r"\s+", " ", text)          # remove extra spaces
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # remove weird chars
    return text.strip()


# =========================
# TEST THE OCR PIPELINE
# =========================
if __name__ == "__main__":
    sample_pdf = "data/sample_pdfs/Service1.pdf"

    raw_text = pdf_to_text(sample_pdf)
    cleaned_text = clean_text(raw_text)

    print("\n✅ OCR OUTPUT (First 500 characters):\n")
    print(cleaned_text[:500])