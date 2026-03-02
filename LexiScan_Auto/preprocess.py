# FILE: preprocess.py
# PURPOSE: Convert CUAD JSON → Hugging Face training format

import json

print("Loading CUAD_v1.json...")
with open("data/CUAD_v1.json", "r") as f:
    cuad = json.load(f)

ENTITY_MAP = {
    "DATE": ["Effective Date", "Agreement Date", "Expiration Date"],
    "PARTY_NAME": ["Parties", "Document Name"],
    "DOLLAR_AMOUNT": ["Minimum Commitment", "Cap On Liability",
                      "Revenue", "Price", "Liquidated Damages"],
    "TERMINATION_CLAUSE": ["Termination For Convenience",
                           "Termination For Cause"]
}

def get_label(question):
    for label, keywords in ENTITY_MAP.items():
        for kw in keywords:
            if kw.lower() in question.lower():
                return label
    return None

# Extract training data
training_data = []
count = 0

for contract in cuad["data"]:
    for para in contract["paragraphs"]:
        context = para["context"]
        ents = []

        for qa in para["qas"]:
            label = get_label(qa["question"])
            if not label:
                continue
            if qa["is_impossible"]:
                continue

            for ans in qa["answers"]:
                start = ans["answer_start"]
                end   = start + len(ans["text"])
                ents.append({
                    "start": start,
                    "end": end,
                    "label": label,
                    "text": ans["text"]
                })

        if not ents:
            continue

        training_data.append({
            "context": context,
            "entities": ents
        })
        count += 1

# Save as JSON
with open("data/cuad_train.json", "w") as f:
    json.dump(training_data, f, indent=2)

print(f"✅ Done! Saved {count} training documents → data/cuad_train.json")