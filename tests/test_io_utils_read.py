import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pytest
import pandas as pd
from evaluation.io_utils import read_tickets_csv

def test_read_csv_valid(tmp_path):
    csv_file = tmp_path / "valid.csv"
    df = pd.DataFrame({
        "ticket": ["Test ticket"],
        "reply": ["Test reply"],
        "extra": ["extra"]
    })
    df.to_csv(csv_file, index=False)
    loaded_df = read_tickets_csv(csv_file)
    assert set(["ticket", "reply"]).issubset(loaded_df.columns)
    assert set(loaded_df.columns) == {"ticket", "reply"}
    assert len(loaded_df) == 1

def test_read_csv_missing_column(tmp_path):
    csv_file = tmp_path / "missing_column.csv"
    df = pd.DataFrame({"ticket": ["Only ticket"]})
    df.to_csv(csv_file, index=False)
    with pytest.raises(ValueError):
        read_tickets_csv(csv_file)

def test_read_csv_empty_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    with pytest.raises(ValueError):
        read_tickets_csv(csv_file)

def test_read_csv_invalid_content(tmp_path):
    csv_file = tmp_path / "garbage.csv"
    csv_file.write_text("random$$$garbage&&&data")
    with pytest.raises(ValueError):
        read_tickets_csv(csv_file)