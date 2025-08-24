# Domain Jargon Simplification (Non‑Neural)

Translate jargon-heavy sentences from medicine, law, and technology into clear, plain English using a rule-based + statistical pipeline. No neural networks.

## Structure
```
domain_simplification/
├── data/
│   ├── dataset.csv
│   └── test.csv
├── output/
│   └── submission.csv
├── src/
│   ├── preprocessing.py
│   ├── jargon_detect.py
│   ├── simplifier.py
│   ├── reconstruct.py
│   ├── evaluate.py
│   └── utils.py
├── notebooks/
│   └── exploration.ipynb
├── report/
│   └── approach.pdf (later)
├── requirements.txt
├── workflow.txt
└── main.py
```

## Quickstart

```bash
# 1) Create venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) First run (simplify test set)
python main.py --input data/test.csv --output output/submission.csv

# 4) Evaluate on mini dataset
python main.py --evaluate --input data/dataset.csv
```

## Notes
- First run may download NLTK data automatically.
- Grammar correction uses LanguageTool if Java is available; otherwise it skips gracefully.
