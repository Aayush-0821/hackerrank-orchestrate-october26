# HackerRank Orchestrate - October 2026

## Ghost Data Still Exists

An AI-powered deletion-audit agent that proves whether a user's personal data is truly gone across complex enterprise systems, secondary databases, support attachments, search indexes, analytics records, logs, exports, archives, and backups.

---

## Quick Start & Execution

1. Ensure Python 3.12+ is installed.
2. Run the audit agent to process all 518 cases from `dataset/` and generate `output.csv` at the repository root:

```bash
python3 code/main.py
```

3. Verify output generation:
- Exactly 518 data rows plus header.
- Sorted by `case_id` ascending.
- Valid JSON array serialization in `steps_json`.

---

## Deliverables Included

- `code/main.py`: Runnable audit engine entry point.
- `output.csv`: Complete predictions for all 518 evaluation requests.
- `code/evaluation/evaluation_report.md`: Case-level accuracy, step accuracy, sequence verification, custom evaluation cases, and failure analysis.
- `code/evaluation/usage_report.md`: Token usage, model calls, and cost analysis.
- `log.txt`: Complete session conversation transcript complying with `AGENTS.md`.
