from brimo_sentiment.parsing import parse_llm_json


def test_parses_clean_json():
    result = parse_llm_json('{"Topic": "Errors/Bugs", "Sentiment": "Negative", "Explanation": "App crashes on login."}')
    assert result == {"Topic": "Errors/Bugs", "Sentiment": "Negative", "Explanation": "App crashes on login."}


def test_parses_json_wrapped_in_markdown_fence():
    text = 'Sure, here is the analysis:\n```json\n{"Topic": "User Experience", "Sentiment": "Positive", "Explanation": "Easy to use."}\n```'
    result = parse_llm_json(text)
    assert result == {"Topic": "User Experience", "Sentiment": "Positive", "Explanation": "Easy to use."}


def test_parses_json_wrapped_in_bare_fence_without_language_tag():
    text = '```\n{"Topic": "Banking System", "Sentiment": "Neutral", "Explanation": "Works as expected."}\n```'
    result = parse_llm_json(text)
    assert result["Topic"] == "Banking System"


def test_parses_json_embedded_in_surrounding_prose():
    text = (
        'Based on the review, here is my analysis: '
        '{"Topic": "Network or Connection", "Sentiment": "Negative", "Explanation": "Frequent timeouts."} '
        'Let me know if you need anything else.'
    )
    result = parse_llm_json(text)
    assert result["Topic"] == "Network or Connection"


def test_falls_back_to_none_dict_on_unparseable_text():
    result = parse_llm_json("I'm not able to analyze this review right now.")
    assert result == {"Topic": None, "Sentiment": None, "Explanation": None}


def test_falls_back_on_empty_string():
    assert parse_llm_json("") == {"Topic": None, "Sentiment": None, "Explanation": None}


def test_falls_back_on_malformed_json_inside_fence():
    text = '```json\n{"Topic": "Overall", "Sentiment": Positive}\n```'  # unquoted value, invalid JSON
    result = parse_llm_json(text)
    assert result == {"Topic": None, "Sentiment": None, "Explanation": None}
