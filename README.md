# brimo-sentiment

[![CI](https://github.com/apricitea/brimo-sentiment/actions/workflows/ci.yml/badge.svg)](https://github.com/apricitea/brimo-sentiment/actions/workflows/ci.yml)

Sentiment analysis on public Google Play Store reviews for BRImo (BRI's
mobile banking app), scored by a local LLM instead of manual labeling or a
paid API.

## Pipeline

1. **Review collection** (`brimo_sentiment/sentiment-analysis-brimo.ipynb`) —
   pulls reviews via `google-play-scraper` (package `id.co.bri.brimo`,
   Indonesian locale).
2. **LLM sentiment scoring** — each review is sent to a local Ollama
   (`llama3`) model, constrained to JSON output (`format: "json"`), that
   extracts topic, sentiment, and a short explanation. Runs entirely
   offline, no per-request API cost. Response parsing (`brimo_sentiment/parsing.py`)
   handles the common case of the model still wrapping its answer in prose
   or a markdown code fence despite the JSON constraint — unit tested in
   `tests/test_parsing.py`.
3. **Twitter scraping** (`brimo_sentiment/scrape-twitter.ipynb`) — a
   Playwright-based scraper for tweet threads, as a secondary text source
   beyond Play Store reviews.

`brimo_sentiment/openai-api.ipynb` is a standalone scratch notebook testing
the OpenAI API directly (as a comparison point against the local LLM) — it
requires `OPENAI_API_KEY` in a `.env` file and isn't part of the main
pipeline.

## Why local LLM over an API

Running the labeling model locally (Ollama) removes per-review API cost and
rate limits entirely, which matters at review-corpus scale — the tradeoff is
lower classification quality than a frontier model, worth it here since the
task is coarse sentiment/topic extraction, not high-stakes classification.

## Stack

Python · google-play-scraper · Playwright · Ollama (llama3) · pandas

## Setup

```bash
poetry install
playwright install
cp .env.example .env  # only needed for the OpenAI comparison notebook
```

## Tests

```bash
poetry run pytest
```

Covers the LLM-response parsing logic (`brimo_sentiment/parsing.py`) — the
rest of the pipeline is notebook-driven and depends on live services
(Ollama, Google Play, Twitter), so it isn't exercised in CI.
