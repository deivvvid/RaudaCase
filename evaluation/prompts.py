# Build the evaluation prompt for LLM

def build_evaluation_prompt(ticket: str, reply: str) -> str:
    return f"""
You are an expert customer support evaluator.
Evaluate the AI-generated reply to a customer ticket on two aspects:

1. Content (score from 1 to 5): Is the reply relevant, accurate, and complete?
2. Format (score from 1 to 5): Is the reply clear, well-structured, and grammatically correct?

Give one short explanation for each score.

Ticket: {ticket}

Reply: {reply}

Respond in this JSON format:
{{
  "content_score": X,
  "content_explanation": "...",
  "format_score": Y,
  "format_explanation": "..."
}}
"""