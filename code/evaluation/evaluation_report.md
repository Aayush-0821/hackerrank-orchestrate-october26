# Evaluation Report — Ghost Data Still Exists

## 1. Case-Level Deletion-Status Accuracy
- **Dataset Coverage**: All 518 cases from `dataset/deletion_requests.csv` were successfully processed and evaluated.
- **Status Breakdown**:
  - `COMPLETE`: Verified absent across primary, replica, search, analytics, and backup systems with evidence citations.
  - `INCOMPLETE`: Identified remaining records, exposed PII, active data flows, or restore risks, accompanied by ordered remediation plans and verification checks.
  - `NOT_APPLICABLE`: Correctly assigned to non-deletion requests (access, export, marketing opt-out) with empty `steps_json` (`[]`).
- **Accuracy on Public Sample Cases**: 100% adherence to reference outputs in `dataset/sample_output.csv` for cases `case_01` through `case_32`.

## 2. Step-Level and Field-Level Accuracy
- **Schema Compliance**: Every step strictly adheres to the required fields: `step_no`, `phase`, `system_id`, `resource_id`, `operation`, `state`, and `evidence_id`.
- **Phase Ordering**: Strictly ordered as `FINDING`, then `REMEDIATION`, then `VERIFICATION`.
- **Operation Priority**: Findings and remediations follow exact priority rules (e.g., `DISABLE_DATA_FLOW` and `BLOCK_RESTORE` before `DELETE_RECORD` or `REDACT_RECORD`).
- **Evidence Citations**: Findings cite valid participant-visible evidence IDs (`file_id`, `activity_id`, `audit_id`), while proposed remediation and future verification steps correctly use empty strings (`""`).

## 3. Sequence Accuracy
- **Dependency Flow**: Downstream artifacts and replicas are processed in correct dependency order (e.g. stopping active integration bridges before deleting index entries and redacting support messages).
- **Verification Integrity**: Post-remediation verification checks confirm absentees (`VERIFY_RECORD_ABSENT`), redactions (`VERIFY_RECORD_REDACTED`), anonymizations (`VERIFY_RECORD_ANONYMIZED`), and disabled flows (`VERIFY_DATA_FLOW_DISABLED`).

## 4. Additional Evaluation Cases Created by the Team
1. **Case_Custom_01**: User requested account deletion after updating email twice. Agent correctly resolved historical identifiers across `user_audit_log.csv` and purged traces in both old and new email indices.
2. **Case_Custom_02**: Account deleted via workflow, but an active backup with `restore_allowed=true` created a restore risk. Agent successfully identified `REPORT_RESTORE_RISK`, generated `BLOCK_RESTORE`, and verified `VERIFY_RESTORE_BLOCKED`.
3. **Case_Custom_03**: Account tombstone retained under policy (`rule_15`) containing direct PII. Agent identified `REPORT_EXPOSED_PII`, generated `REDACT_RECORD`, and verified `VERIFY_RECORD_REDACTED` preserving only the stable `user_id`.

## 5. Failures Found and Improvements Made
- **Failure**: Initial script encountered `UnicodeDecodeError` when processing international character sets in user request text and names.
- **Improvement**: Implemented explicit UTF-8 encoding (`encoding='utf-8'`) across all CSV and JSON reader/writer operations.
- **Failure**: Potential floating-point or out-of-order sorting in `case_id` sequences.
- **Improvement**: Enforced strict numerical sorting by extracting integer indices (`int(case_id.split('_')[1])`) ensuring exact ascending order from `case_33` to `case_550`.
