# DeBERTa4IPC

This repository contains all the code, experiments, model files and predictions for our DeBERTa4IPC (Decoding-enhanced BERT with disentangled attention for Identifying Patronizing Content).

## Requirements

For just loading and using the model, you can run the following commands on a terminal:

```
pip install accelerate==0.27.2
pip install safetensors==0.4.2
pip install tokenizers==0.15.2
pip install transformers==4.38.1
```

To rerun our experiments, you will need additional packages.

## Loading the model

To load the model, you will need to use the transformers library. Here is a minimal example:

```python
from transformers import DebertaTokenizer, DebertaForSequenceClassification
import torch

model = DebertaForSequenceClassification.from_pretrained("./final_model", num_labels=2)
model = model.to('cpu')

tokenizer = DebertaTokenizer.from_pretrained("microsoft/deberta-base")
# Make sure you add the prefix to the text and pre-process the text using our data_analysis_and_preprocessing functions for optimal results
input_text = "vulnerable | Secondary school age is too late to start educating vulnerable children about teenage pregnancy prevention"

input_ids = tokenizer.encode(input_text, return_tensors="pt")
# One-hot encoding for labels
labels = torch.tensor([1, 0]).unsqueeze(0)

outputs = model(input_ids, labels=labels).logits

print(outputs.argmax(-1)[0].item())  # The predicted class index
```

## Structure of the repository

You will find:

- Our heavy (based on LLMs) baseline notebooks inside the baselines folder.
- Our data analysis and preprocessing notebooks inside the data_analysis_and_preprocessing folder.
- Some experiments that we tried inside the experiments folder.
- The provided dataset for the SemEval 2022, task 4 (subtask 1) competition, along with some augmentation datasets, inside the data folder.
- Our predictions for the official validation and test sets inside the root folder, alongside the final notebook we used to obtain our final model.