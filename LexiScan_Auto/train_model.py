# FILE: train_model.py
# PURPOSE: Train NER model on CUAD data using Hugging Face

import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    DataCollatorForTokenClassification
)
from torch.utils.data import Dataset
import numpy as np
import os

# ── Labels ──────────────────────────────────────────────
LABELS = ["O", "B-DATE", "I-DATE",
               "B-PARTY_NAME", "I-PARTY_NAME",
               "B-DOLLAR_AMOUNT", "I-DOLLAR_AMOUNT",
               "B-TERMINATION_CLAUSE", "I-TERMINATION_CLAUSE"]

label2id = {l: i for i, l in enumerate(LABELS)}
id2label = {i: l for i, l in enumerate(LABELS)}

# ── Load Data ────────────────────────────────────────────
print("Loading training data...")
with open("data/cuad_train.json", "r") as f:
    raw_data = json.load(f)

# Use 80% train, 20% eval
split = int(len(raw_data) * 0.8)
train_data = raw_data[:split]
eval_data  = raw_data[split:]
print(f"Train: {len(train_data)} | Eval: {len(eval_data)}")

# ── Tokenizer ────────────────────────────────────────────
MODEL_NAME = "distilbert-base-uncased"
tokenizer  = AutoTokenizer.from_pretrained(MODEL_NAME)

# ── Convert to Token Labels ───────────────────────────────
def encode_example(example):
    context  = example["context"][:512]   # limit length
    entities = example["entities"]

    encoding = tokenizer(
        context,
        truncation=True,
        max_length=512,
        return_offsets_mapping=True
    )

    offsets    = encoding["offset_mapping"]
    labels_ids = [label2id["O"]] * len(offsets)

    for ent in entities:
        start = ent["start"]
        end   = ent["end"]
        label = ent["label"]

        first = True
        for i, (tok_start, tok_end) in enumerate(offsets):
            if tok_end <= start or tok_start >= end:
                continue
            if first:
                labels_ids[i] = label2id[f"B-{label}"]
                first = False
            else:
                labels_ids[i] = label2id[f"I-{label}"]

    encoding["labels"] = labels_ids
    encoding.pop("offset_mapping")
    return encoding

# ── Dataset Class ─────────────────────────────────────────
class NERDataset(Dataset):
    def __init__(self, data):
        self.encodings = [encode_example(d) for d in data]

    def __len__(self):
        return len(self.encodings)

    def __getitem__(self, idx):
        return {k: torch.tensor(v) for k, v in self.encodings[idx].items()}

print("Encoding dataset (this may take 2-3 mins)...")
train_dataset = NERDataset(train_data)
eval_dataset  = NERDataset(eval_data)
print("✅ Dataset ready!")

# ── Model ─────────────────────────────────────────────────
model = AutoModelForTokenClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(LABELS),
    id2label=id2label,
    label2id=label2id
)

# ── Training Args ─────────────────────────────────────────
args = TrainingArguments(
    output_dir="models/",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    logging_steps=10,
)

# ── Trainer ───────────────────────────────────────────────
data_collator = DataCollatorForTokenClassification(tokenizer)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    processing_class=tokenizer,
    data_collator=data_collator
)

# ── Train ─────────────────────────────────────────────────
print("\n🚀 Starting training (30-60 mins)...")
trainer.train()

# ── Save ──────────────────────────────────────────────────
model.save_pretrained("models/model-best")
tokenizer.save_pretrained("models/model-best")
print("\n✅ Model saved → models/model-best")