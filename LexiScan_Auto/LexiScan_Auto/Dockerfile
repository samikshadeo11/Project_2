FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install torch transformers flask pytesseract pdf2image pillow

CMD ["python", "api_service.py"]