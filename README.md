# HackerRank Orchestrate — October 2026

## Ghost Data Still Exists

An AI-powered deletion-audit agent that evaluates whether a user's personal data has been deleted across interconnected enterprise systems, including secondary databases, support attachments, search indexes, analytics records, logs, exports, archives, and backups.

## Quick Start & Execution

### Prerequisites
- Python 3.12 or later
- The input datasets and configuration files required by the audit engine

### Run the audit agent

From the repository root, execute:

```bash
python3 code/main.py
```

The audit engine processes the evaluation requests available in `dataset/` and generates `output.csv` in the repository root.

### Validate the output

Confirm that `output.csv` contains:

- Exactly 518 data rows, plus the CSV header.
- One row per evaluation case, with no missing or duplicate `case_id` values.
- Cases sorted in ascending order by `case_id`.
- Valid JSON-array serialization in `steps_json`.
- Only permitted deletion-status values and schema-compliant steps.

For structural evaluation, run:

```bash
python3 code/evaluation/main.py
```

Review the evaluation report for the metrics actually verified by the evaluator. Public sample comparisons and custom test results should be treated as unverified unless those tests have been executed successfully.

## Deliverables

- `code/main.py` — Audit engine entry point.
- `output.csv` — Predictions for the 518 evaluation requests.
- `code/evaluation/evaluation_report.md` — Evaluation methodology, verified structural metrics, limitations, and failure analysis.
- `code/evaluation/usage_report.md` — Recorded model/API usage, token counts, and cost estimates, where applicable.
- `log.txt` — Session log maintained according to the applicable `AGENTS.md` requirements.
- `code.zip` — Submission archive containing the required runnable code, documentation, and evaluation reports.

## Notes

- Evaluation metrics reflect only checks that were actually executed.
- Structural validity does not, by itself, establish semantic correctness for every deletion decision.
- Usage statistics and cost estimates should be based on recorded execution data rather than assumptions.
