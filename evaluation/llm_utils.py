import json
import requests
from typing import Dict

from evaluation.prompts import build_evaluation_prompt

# Ollama API configuration
OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"

# Ollama model to use
# Ensure you have the model installed locally via Ollama CLI
OLLAMA_MODEL = "mistral"

# Call local Ollama server and parse the response
def evaluate_reply(ticket: str, reply: str) -> Dict:
    prompt = build_evaluation_prompt(ticket, reply)

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, json=body)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        data = json.loads(content)

        return {
            "content_score": data.get("content_score", 1),
            "content_explanation": data.get("content_explanation", ""),
            "format_score": data.get("format_score", 1),
            "format_explanation": data.get("format_explanation", "")
        }

    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error evaluating reply: {e}")
        return {
            "content_score": 1,
            "content_explanation": "Error during evaluation.",
            "format_score": 1,
            "format_explanation": "Error during evaluation."
        }
