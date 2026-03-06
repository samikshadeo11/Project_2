# PURPOSE: Validate and clean NER outputs

import re

def validate_date(text):
    pattern = r"\b\d{4}-\d{2}-\d{2}\b"
    match = re.search(pattern, text)
    return match.group() if match else None


def validate_amount(text):
    pattern = r"\$[0-9,]+(\.[0-9]{2})?"
    match = re.search(pattern, text)
    return match.group() if match else None


def validate_party(text):
    if len(text) < 3:
        return None
    return text.strip()


def validate_entities(entities):

    validated = []

    for ent in entities:

        label = ent["label"]
        text  = ent["text"]

        if label == "DATE":
            value = validate_date(text)

        elif label == "DOLLAR_AMOUNT":
            value = validate_amount(text)

        elif label == "PARTY_NAME":
            value = validate_party(text)

        else:
            value = text

        if value:
            validated.append({
                "label": label,
                "value": value
            })

    return validated