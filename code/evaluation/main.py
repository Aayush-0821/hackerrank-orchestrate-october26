import csv
import json
import os

def run_evaluation():
    print("=" * 60)
    print("GHOST DATA STILL EXISTS — COMPREHENSIVE EVALUATION RUNNER")
    print("=" * 60)

    # Paths
    input_cases_path = "dataset/deletion_requests.csv"
    output_path = "output.csv"
    sample_ref_path = "dataset/sample_output.csv"
    evidence_manifest_path = "dataset/evidence_files.csv"
    system_activity_path = "dataset/system_activity.csv"
    user_audit_log_path = "dataset/user_audit_log.csv"

    # Load evidence IDs
    valid_evidence_ids = set()
    if os.path.exists(evidence_manifest_path):
        with open(evidence_manifest_path, "r", encoding="utf-8") as f:
            valid_evidence_ids.update(r["file_id"] for r in csv.DictReader(f))
    if os.path.exists(system_activity_path):
        with open(system_activity_path, "r", encoding="utf-8") as f:
            valid_evidence_ids.update(r["activity_id"] for r in csv.DictReader(f))
    if os.path.exists(user_audit_log_path):
        with open(user_audit_log_path, "r", encoding="utf-8") as f:
            valid_evidence_ids.update(r["audit_id"] for r in csv.DictReader(f))

    # 1. Input coverage
    input_ids = []
    if os.path.exists(input_cases_path):
        with open(input_cases_path, "r", encoding="utf-8") as f:
            input_requests = list(csv.DictReader(f))
            input_ids = [r["case_id"] for r in input_requests]
    input_count = len(input_ids)

    # 2. Output coverage
    output_rows = []
    malformed_csv_rows = 0
    missing_columns = 0
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            try:
                reader = csv.DictReader(f)
                expected_fields = ["case_id", "deletion_status", "steps_json"]
                if not reader.fieldnames or not all(f in reader.fieldnames for f in expected_fields):
                    missing_columns += 1
                for row in reader:
                    output_rows.append(row)
            except Exception:
                malformed_csv_rows += 1
    output_count = len(output_rows)

    # 3. Case ID checks
    output_ids = [r.get("case_id") for r in output_rows if r.get("case_id")]
    missing_ids = set(input_ids) - set(output_ids)
    unexpected_ids = set(output_ids) - set(input_ids)
    duplicate_ids = [cid for cid in set(output_ids) if output_ids.count(cid) > 1]

    # 4. Status and Step validation
    valid_statuses = {"COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"}
    valid_phases = {"FINDING", "REMEDIATION", "VERIFICATION"}
    valid_operations = {
        "REPORT_REMAINING_RECORD", "REPORT_EXPOSED_PII", "REPORT_ACTIVE_DATA_FLOW", "REPORT_RESTORE_RISK",
        "DISABLE_DATA_FLOW", "BLOCK_RESTORE", "DELETE_RECORD", "REDACT_RECORD", "ANONYMIZE_RECORD",
        "VERIFY_RECORD_ABSENT", "VERIFY_RECORD_PRESENT", "VERIFY_RECORD_REDACTED", "VERIFY_RECORD_ANONYMIZED",
        "VERIFY_DATA_FLOW_DISABLED", "VERIFY_RESTORE_BLOCKED"
    }

    invalid_statuses = 0
    invalid_json_rows = 0
    step_schema_violations = 0
    step_numbering_failures = 0
    phase_order_failures = 0
    not_applicable_compliance_failures = 0
    evidence_compliance_failures = 0
    invalid_evidence_citations = 0
    total_steps = 0

    for r in output_rows:
        cid = r.get("case_id", "unknown")
        st = r.get("deletion_status")
        if st not in valid_statuses:
            invalid_statuses += 1

        try:
            steps = json.loads(r.get("steps_json", "[]"))
        except Exception:
            invalid_json_rows += 1
            continue

        if st == "NOT_APPLICABLE" and len(steps) != 0:
            not_applicable_compliance_failures += 1

        total_steps += len(steps)
        last_phase_rank = 0
        phase_map = {"FINDING": 1, "REMEDIATION": 2, "VERIFICATION": 3}

        for idx, step in enumerate(steps, start=1):
            if step.get("step_no") != idx:
                step_numbering_failures += 1

            if not all(f in step for f in ["step_no", "phase", "system_id", "resource_id", "operation", "state", "evidence_id"]):
                step_schema_violations += 1

            ph = step.get("phase")
            if ph not in valid_phases:
                step_schema_violations += 1

            if step.get("operation") not in valid_operations:
                step_schema_violations += 1

            if ph in phase_map:
                rank = phase_map[ph]
                if rank < last_phase_rank:
                    phase_order_failures += 1
                last_phase_rank = rank

            ev_id = step.get("evidence_id")
            if ph == "FINDING" or (ph == "VERIFICATION" and st == "COMPLETE"):
                if not ev_id or ev_id == "":
                    evidence_compliance_failures += 1
                elif ev_id not in valid_evidence_ids:
                    invalid_evidence_citations += 1
            else:
                if ev_id != "":
                    evidence_compliance_failures += 1

    # 5. Public sample comparison (Only if in output.csv)
    sample_matches = 0
    sample_compared = 0
    if os.path.exists(sample_ref_path):
        with open(sample_ref_path, "r", encoding="utf-8") as f:
            sample_ref = {r["case_id"]: r for r in csv.DictReader(f)}

        output_dict = {r["case_id"]: r for r in output_rows}
        for cid, ref_row in sample_ref.items():
            if cid in output_dict:
                sample_compared += 1
                pred_row = output_dict[cid]
                if pred_row["deletion_status"] == ref_row["deletion_status"]:
                    try:
                        if json.loads(pred_row["steps_json"]) == json.loads(ref_row["steps_json"]):
                            sample_matches += 1
                    except:
                        pass

    # Print Summary
    print(f"1. Input coverage: {input_count} cases")
    print(f"2. Output coverage: {output_count} rows")
    print(f"3. Public sample matches: {sample_matches} / {sample_compared} compared (Ref total: {len(sample_ref) if os.path.exists(sample_ref_path) else 0})")
    print(f"4. Total step objects evaluated: {total_steps}")
    print(f"5. Structural failures:")
    print(f"   - Malformed CSV/JSON: {malformed_csv_rows + invalid_json_rows}")
    print(f"   - Schema violations: {step_schema_violations + invalid_statuses}")
    print(f"   - Numbering/Ordering: {step_numbering_failures + phase_order_failures}")
    print(f"   - Policy/Evidence compliance: {not_applicable_compliance_failures + evidence_compliance_failures + invalid_evidence_citations}")

    # Save detailed JSON report
    report_data = {
        "summary": {
            "input_cases": input_count,
            "output_rows": output_count,
            "total_steps": total_steps,
            "sample_matches": sample_matches,
            "sample_compared": sample_compared
        },
        "failures": {
            "missing_case_ids": len(missing_ids),
            "duplicate_case_ids": len(duplicate_ids),
            "invalid_statuses": invalid_statuses,
            "step_schema_violations": step_schema_violations,
            "step_numbering_failures": step_numbering_failures,
            "phase_order_failures": phase_order_failures,
            "evidence_compliance_failures": evidence_compliance_failures,
            "invalid_evidence_citations": invalid_evidence_citations
        }
    }

    report_json_path = "code/evaluation/evaluation_metrics.json"
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
    print(f"Metrics saved to {report_json_path}")

if __name__ == "__main__":
    run_evaluation()
