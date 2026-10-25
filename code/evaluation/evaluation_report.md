# Evaluation Report — Ghost Data Still Exists

## 1. Evaluation Summary
- **Scope**: Validation of all 518 evaluation requests in `dataset/deletion_requests.csv` and root-level `output.csv`.
- **Date**: October 25, 2026.
- **Methodology**: Automated evaluation script (`code/evaluation/main.py`) verifying case coverage, structural conformance, and step-level schema compliance.

## 2. Evaluation Matrix

| Metric | Definition | Measured Result | Denominator | Status |
|---|---|---|---|---|
| Input Coverage | Total valid input cases processed | 518 | 518 | PASSED |
| Output Coverage | Total output prediction rows | 518 | 518 | PASSED |
| Case ID Continuity | Missing or duplicate evaluation case IDs | 0 | 518 | PASSED |
| CSV/JSON Validity | Malformed CSV rows or invalid JSON strings | 0 | 518 | PASSED |
| Status Validity | Compliance with allowed status values | 0 | 518 | PASSED |
| Step Schema | Missing fields or invalid values in steps | 0 | 492 steps | PASSED |
| Step Numbering | Consecutive step numbering within cases | 0 | 492 steps | PASSED |
| Phase Ordering | FINDING → REMEDIATION → VERIFICATION order | 0 | 492 steps | PASSED |
| Evidence Citation | Citation existence and valid ID check | 0 | 492 steps | PASSED |
| Public Sample Agreement| Comparison against `dataset/sample_output.csv` | NOT RUN | 32 | N/A |
| Custom Test Results | Participant-created evaluation scenarios verified | NOT RUN | 3 | N/A |

## 3. Case-Level Results
- **Evaluation Set**: The generated `output.csv` contains predictions for the 518 evaluation cases (`case_33` to `case_550`).
- **Completeness**: Every required evaluation case ID is present exactly once, with zero unexpected or duplicate rows.
- **Sorting**: Cases are numerically sorted in ascending order by their index.

## 4. Step-Level Results
- **Step Population**: A total of 492 step objects were evaluated across the 518 output rows.
- **Structural Integrity**: 100% of steps comply with the required fields (`step_no`, `phase`, `system_id`, `resource_id`, `operation`, `state`, `evidence_id`).
- **Phase Ordering**: Every case correctly follows the mandatory phase sequence.
- **Evidence Verification**: All findings and completed verifications cite valid `file_id`, `activity_id`, or `audit_id` entries verified against the provided manifest and logs.

## 5. Reference Comparison and Custom Tests
- **Public Sample Agreement**: **NOT RUN**. The current `output.csv` contains only the evaluation cases (`case_33` onwards), while the public reference samples cover `case_01` through `case_32`. Consequently, direct exact-match comparison is unavailable for the current submission artifact.
- **Custom Tests**: **NOT RUN**. While evaluation scenarios were conceptually designed, standalone executable fixtures and expected output files for these custom cases were not found in the current environment.

## 6. Failures and Limitations
- **Semantic vs. Structural**: Automated verification confirms 100% structural and schema compliance. However, semantic accuracy (correctness of the audit decision itself) is derived from deterministic policy logic applied to the evidence artifacts.
- **Sample Coverage**: The absence of sample cases in the final output prevents measuring the agreement rate against the public benchmark within the same file.

## 7. Reproduction Instructions
To rerun the comprehensive structural evaluation and regenerate validation metrics:

```bash
python3 code/evaluation/main.py
```
