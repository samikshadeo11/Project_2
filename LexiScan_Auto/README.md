# Project Title
LexiScan Auto

# Project Summary
LexiScan Auto is an AI-based legal document analysis system that automatically extracts key information from contract PDFs. The system uses OCR technology to convert scanned documents into text and applies a DistilBERT-based Named Entity Recognition model to identify important legal entities such as parties, dates, and clauses. This approach reduces manual contract review effort and improves efficiency in legal document processing.

# Project Description
LexiScan Auto is an AI-powered legal document processing system designed to automatically extract important information from legal contracts and agreements. In many organizations, legal teams must manually review large volumes of PDF contracts to identify key details such as parties involved, agreement dates, obligations, and legal clauses. This manual process is time-consuming, inefficient, and prone to human errors.

The LexiScan Auto system automates this task by combining Optical Character Recognition (OCR) and Natural Language Processing (NLP) techniques. The system first converts PDF documents into images and uses Tesseract OCR to extract the textual content from each page. The extracted text is then processed using a pre-trained DistilBERT model fine-tuned for Named Entity Recognition (NER). This model identifies important legal entities such as organization names, dates, obligations, and contractual terms.

By automatically extracting structured information from unstructured legal documents, LexiScan Auto helps improve efficiency, reduce manual effort, and enable faster legal document analysis. This solution can be useful for legal firms, financial institutions, and enterprises that handle large volumes of contracts.

# Project Workflow
Legal Contract PDF
        ↓
PDF to Image Conversion (Poppler)
        ↓
Text Extraction using OCR (Tesseract)
        ↓
Text Cleaning & Preprocessing
        ↓
Named Entity Recognition using DistilBERT Model
        ↓
Extraction of Key Legal Entities
        ↓
Structured Output (Important Contract Information)

# Technologies Used

- Python
- PyTorch
- HuggingFace Transformers
- Tesseract OCR
- Poppler
- Pandas

# How to Run the Project

1. Install dependencies
pip install -r requirements.txt

2. Train the model
python train_model.py

3. Run OCR pipeline
python ocr_pipeline.py