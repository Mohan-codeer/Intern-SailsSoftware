# THIS IS NOT MY CODE I FOLLOWED A TUTORIAL

from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification, TrainingArguments, Trainer
import evaluate
import numpy as np

dataset_name = "ag_news"
dataset = load_dataset(dataset_name)
print(dataset)

train_dataset = dataset["train"]
eval_dataset = dataset["test"]

model_checkpoint = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

text = "The stock market saw record gains today."

inputs = tokenizer(text, return_tensors="pt")

print("Tokenized input:")
for k, v in inputs.items():
    print(f"{k}: {v.shape} -> {v}")


def preprocess_function(examples):
  return tokenizer(examples["text"], truncation=True, padding="max_length")

train_dataset = train_dataset.map(preprocess_function, batched=True)
eval_dataset = eval_dataset.map(preprocess_function, batched=True)


num_labels = dataset["train"].features["label"].num_classes
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=num_labels)

# Freeze the entire base model (DistilBERT)
for param in model.base_model.parameters():
  param.requires_grad = False

# The classification head will be trainable by default.



def count_parameters(model):
  total_params = sum(p.numel() for p in model.parameters())
  trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
  return {
      "Total": total_params,
      "Trainable": trainable_params,
      "Frozen": total_params - trainable_params
  }


param_counts = count_parameters(model)
print("Model Paramenter Counts:")
for k, v in param_counts.items():
  print(f"{k}: {v:,}")



outputs = model(**inputs)
print(outputs)

import evaluate
import numpy as np

accuracy_metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
  logits, labels = eval_pred
  predictions = np.argmax(logits, axis=-1)
  return accuracy_metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    logging_steps=10,
    learning_rate=5e-5,
    per_device_train_batch_size=64,
    per_device_eval_batch_size=64,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    report_to="none",
    fp16=True,
    dataloader_num_workers=2
)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)
trainer.train()

final_scores = trainer.evaluate()
print("Final Scores:")
for k, v in final_scores.items():
  print(f"{k}: {v:.4f}")


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()


final_scores = trainer.evaluate()
print("Final Scores:")
for k, v in final_scores.items():
  print(f"{k}: {v:.4f}")


trainer.train()

final_scores = trainer.evaluate()
print("Final Scores:")
for k, v in final_scores.items():
  print(f"{k}: {v:.4f}")
