# Ticket Reply Evaluation - LLM Based

This project evaluates AI-generated customer support replies using a local LLM (Mistral via Ollama).

---

## Project Structure

```
├── evaluation/
│   ├── io_utils.py          # Read and write CSV files
│   ├── llm_utils.py         # Evaluates replies via Ollama (Mistral)
│   ├── prompts.py           # Prompt builder for evaluation
│
├── tests/ # All the tests
│   └── test_io_utils_read_csv.py # Tests performed on io_utils read_csv
│   └── test_io_utils_save.py # Tests performed on io_utils save_csv
│   └── test_llm_utils.py # Tests performed on llm_utils
│   └── test_prompts.py # Tests performed on prompts
│
├── evaluate_tickets.ipynb  # Main notebook
├── run_tests.ipynb         # Test notebook
├── tickets.csv             # Input CSV
├── generated_tickets.csv   # AI Generated input CSV to used for testing
├── tickets_evaluated.csv   # Output CSV
├── requirements.txt        # Python dependencies
├── README.md               # This file
```

---

## How to Run

### 1. Install Ollama

Download and install from here https://ollama.com/download.

### 2. Start Ollama with Mistral
```bash
ollama run mistral
```

Ensure it runs at `http://localhost:11434`.

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the notebook
Open `notebook/evaluate_tickets.ipynb` and run all cells. It will:
- Load `tickets.csv`
- Call the LLM for each ticket+reply
- Output a new CSV: `tickets_evaluated.csv`

---

## CSV Input Format

Your `tickets.csv` should contain:
```csv
ticket,reply
"How do I reset my password?","To reset your password, follow these steps..."
...
```

---

## Output Format

The result `tickets_evaluated.csv` will include:
```csv
ticket,reply,content_score,content_explanation,format_score,format_explanation
...
```

---

## Requirements

Python 3.10.0 and packages specified in `requirements.txt`:
```
pandas
requests
tqdm
pytest
```

---
