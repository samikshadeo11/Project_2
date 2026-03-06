# PURPOSE: Full pipeline API (OCR + NER + Postprocessing)

from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

from ocr_pipeline import pdf_to_text, clean_text
from postprocess import validate_entities

app = Flask(__name__)

MODEL_PATH = "models/model-best"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH)

LABELS = model.config.id2label


def extract_entities(text):

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

    outputs = model(**inputs)

    preds = torch.argmax(outputs.logits, dim=2)

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    entities = []

    for token, pred in zip(tokens, preds[0]):
        label = LABELS[pred.item()]

        if label != "O":
            entities.append({
                "token": token,
                "label": label
            })

    return entities


@app.route("/extract", methods=["POST"])
def extract():

    file = request.files["file"]

    pdf_path = "temp.pdf"
    file.save(pdf_path)

    text = pdf_to_text(pdf_path)
    text = clean_text(text)

    raw_entities = extract_entities(text)

    validated = validate_entities(raw_entities)

    return jsonify({
        "entities": validated
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)