import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pytest
import pandas as pd
from evaluation.io_utils import save_evaluated_tickets

def test_save_csv(tmp_path):
    output_file = tmp_path / "output.csv"
    df = pd.DataFrame({
        "ticket": ["T"],
        "reply": ["R"],
        "content_score": [5],
        "format_score": [4],
        "content_explanation": ["Good"],
        "format_explanation": ["Clear"]
    })
    save_evaluated_tickets(df, output_file)
    assert output_file.exists()
    reloaded = pd.read_csv(output_file)
    assert reloaded.shape == (1, 6)
