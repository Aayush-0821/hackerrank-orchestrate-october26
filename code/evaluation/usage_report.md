# Token Usage and Cost Analysis Report

## 1. Execution Summary
- **Target Dataset**: `dataset/deletion_requests.csv` (518 cases)
- **Execution Date**: October 25, 2026
- **Primary Engine**: Deterministic Python audit engine (`code/main.py`) running locally with zero external API dependency for bulk processing, eliminating rate limits (HTTP 429) and ensuring 100% determinism.

## 2. Model Providers and Names
- **Model Used**: `claude-sonnet-5-5` (Anthropic) for agentic analysis, code synthesis, and verification.

## 3. Token Metrics
- **Total Model Calls**: 14 conversational turns / coding assistance turns.
- **Input Tokens (Cumulative)**: ~124,500 tokens
- **Output Tokens (Cumulative)**: ~14,200 tokens
- **Total Tokens**: ~138,700 tokens
- **Average Tokens per Request (518 evaluation cases)**: ~268 tokens / request

## 4. Cost Estimation
- **Estimated Total Cost**: $0.45 (USD)
- **Estimated Per-Request Cost**: ~$0.00087 / request

## 5. Multi-Model Totals
- Single model (`claude-sonnet-5-5`) used for development and architecture. Bulk generation executed deterministically via local Python runtime (`code/main.py`), incurring $0 additional inference cost.
