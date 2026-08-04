"""Parsing helpers for the local-LLM sentiment pipeline.

Extracted out of sentiment-analysis-brimo.ipynb so the JSON-parsing logic
is unit-testable independent of a running Ollama instance.
"""

import json
import re

_FALLBACK = {"Topic": None, "Sentiment": None, "Explanation": None}

# Matches a ```json ... ``` or bare ``` ... ``` fenced block
_CODE_FENCE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)
# Matches the first {...} block anywhere in the text, as a last-resort fallback
_FIRST_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


def parse_llm_json(text: str) -> dict:
    """Parse a JSON object out of an LLM response.

    llama3 (run without an explicit JSON output constraint) frequently wraps
    its answer in prose or a markdown code fence rather than returning bare
    JSON, so a plain `json.loads(text)` fails far more often than it
    succeeds in practice. This tries, in order: the raw text, a fenced code
    block if present, and the first `{...}` span in the text. Falls back to
    a dict of Nones (matching the pipeline's existing failure shape) if
    nothing parses.
    """
    if not text:
        return dict(_FALLBACK)

    candidates = [text.strip()]

    fence_match = _CODE_FENCE.search(text)
    if fence_match:
        candidates.append(fence_match.group(1).strip())

    object_match = _FIRST_OBJECT.search(text)
    if object_match:
        candidates.append(object_match.group(0).strip())

    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    return dict(_FALLBACK)
