import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pytest
import pandas as pd
from evaluation.prompts import build_evaluation_prompt

# Dummy data for tests
dummy_ticket = "How do I change my email address?"
dummy_reply = "You can change your email by going to settings > profile."

def test_prompt_structure():
    prompt = build_evaluation_prompt(dummy_ticket, dummy_reply)
    assert "content_score" in prompt
    assert "Ticket:" in prompt
    assert "Reply:" in prompt
