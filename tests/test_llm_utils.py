import json
from unittest.mock import patch, Mock
from evaluation.llm_utils import evaluate_reply
from evaluation.io_utils import read_tickets_csv
from requests.exceptions import RequestException

def test_evaluate_reply_mock():
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "content_score": 4,
                        "content_explanation": "Relevant and mostly complete.",
                        "format_score": 5,
                        "format_explanation": "Very clear and well-written."
                    })
                }
            }
        ]
    }

    with patch("evaluation.llm_utils.requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = mock_response

        result = evaluate_reply("Sample ticket", "Sample reply")

        assert result["content_score"] == 4
        assert result["format_score"] == 5
        assert "Relevant" in result["content_explanation"]
        assert "clear" in result["format_explanation"].lower()


def test_bulk_evaluation():
    file_path = "generated_tickets.csv"
    df = read_tickets_csv(file_path)

    total = len(df)
    successful = 0

    for _, row in df.iterrows():
        result = evaluate_reply(row["ticket"], row["reply"])

        if not (
            result["content_score"] == 1
            and result["format_score"] == 1
            and "Error during evaluation." in result["content_explanation"]
            and "Error during evaluation." in result["format_explanation"]
        ):
            successful += 1

    print(f"✅ {successful}/{total} replies evaluated successfully.")
    assert successful > 0, "All evaluations failed."

def test_evaluate_reply_request_exception():
    with patch("evaluation.llm_utils.requests.post", side_effect=RequestException("Network error")):
        result = evaluate_reply("Ticket?", "Reply.")
        assert result["content_score"] == 1
        assert result["format_score"] == 1
        assert result["content_explanation"] == "Error during evaluation."
        assert result["format_explanation"] == "Error during evaluation."


def test_evaluate_reply_json_decode_error():
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = {
        "choices": [
            {"message": {"content": "not a valid json string"}}
        ]
    }
    with patch("evaluation.llm_utils.requests.post", return_value=mock_response):
        with patch("json.loads", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            result = evaluate_reply("Ticket?", "Reply.")
            assert result["content_score"] == 1
            assert result["format_score"] == 1
            assert result["content_explanation"] == "Error during evaluation."
            assert result["format_explanation"] == "Error during evaluation."


def test_evaluate_reply_key_error():
    # Simulate missing 'choices' key in the response
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = {}

    with patch("evaluation.llm_utils.requests.post", return_value=mock_response):
        result = evaluate_reply("Ticket?", "Reply.")
        assert result["content_score"] == 1
        assert result["format_score"] == 1
        assert result["content_explanation"] == "Error during evaluation."
        assert result["format_explanation"] == "Error during evaluation."