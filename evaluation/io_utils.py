import pandas as pd
from pathlib import Path
from typing import Union

# Read and validate the input CSV
def read_tickets_csv(file_path: Union[str, Path]) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError("CSV file is empty.")
    if not {'ticket', 'reply'}.issubset(df.columns):
        raise ValueError("CSV must contain 'ticket' and 'reply' columns.")
    df = df[['ticket', 'reply']].dropna().reset_index(drop=True)
    return df

# Save the evaluated DataFrame to CSV
def save_evaluated_tickets(df: pd.DataFrame, output_path: Union[str, Path]) -> None:
    df.to_csv(output_path, index=False)
    print(f"[i] Results saved to {output_path}")