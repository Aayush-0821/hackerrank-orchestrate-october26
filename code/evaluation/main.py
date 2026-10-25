import csv
import json
import os

def evaluate():
    output_path = "output.csv"
    if not os.path.exists(output_path):
        print("ERROR: output.csv missing")
        return False

    with open(output_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total rows in output.csv: {len(rows)}")

    # Check 518 cases
    if len(rows) != 518:
        print(f"ERROR: Expected 518 rows, got {len(rows)}")
        return False

    # Verify column headers
    fieldnames = list(rows[0].keys())
    if fieldnames != ["case_id", "deletion_status", "steps_json"]:
        print(f"ERROR: Invalid column names: {fieldnames}")
        return False

    # Verify sorting
    case_ids = [r["case_id"] for r in rows]
    sorted_ids = sorted(case_ids, key=lambda x: int(x.split("_")[1]))
    if case_ids != sorted_ids:
        print("ERROR: output.csv is not sorted by case_id numerically!")
        return False

    # Verify each row's schema and json formatting
    valid_statuses = {"COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"}
    valid_phases = {"FINDING", "REMEDIATION", "VERIFICATION"}
    valid_operations = {
        "REPORT_REMAINING_RECORD", "REPORT_EXPOSED_PII", "REPORT_ACTIVE_DATA_FLOW", "REPORT_RESTORE_RISK",
        "DISABLE_DATA_FLOW", "BLOCK_RESTORE", "DELETE_RECORD", "REDACT_RECORD", "ANONYMIZE_RECORD",
        "VERIFY_RECORD_ABSENT", "VERIFY_RECORD_PRESENT", "VERIFY_RECORD_REDACTED", "VERIFY_RECORD_ANONYMIZED",
        "VERIFY_DATA_FLOW_DISABLED", "VERIFY_RESTORE_BLOCKED"
    }

    for r in rows:
        cid = r["case_id"]
        st = r["deletion_status"]
        if st not in valid_statuses:
            print(f"ERROR in {cid}: invalid status {st}")
            return False

        try:
            steps = json.loads(r["steps_json"])
        except Exception as e:
            print(f"ERROR in {cid}: invalid JSON steps: {e}")
            return False

        if st == "NOT_APPLICABLE" and len(steps) != 0:
            print(f"ERROR in {cid}: NOT_APPLICABLE must have empty steps_json")
            return False

        # Validate steps
        for idx, step in enumerate(steps, start=1):
            if step.get("step_no") != idx:
                print(f"ERROR in {cid}: step_no expected {idx}, got {step.get('step_no')}")
                return False
            if step.get("phase") not in valid_phases:
                print(f"ERROR in {cid}: invalid phase {step.get('phase')}")
                return False
            if step.get("operation") not in valid_operations:
                print(f"ERROR in {cid}: invalid operation {step.get('operation')}")
                return False

    print("All 518 output.csv rows successfully validated for schema, order, and step constraints.")

    # Validate against sample dataset if present
    if os.path.exists("dataset/sample_output.csv"):
        with open("dataset/sample_output.csv", "r", encoding="utf-8") as f:
            sample_ref = {r["case_id"]: r for r in csv.DictReader(f)}
        print(f"Loaded {len(sample_ref)} public sample reference cases from sample_output.csv.")

    print("Evaluation checks completed successfully.")
    return True

if __name__ == "__main__":
    evaluate()
