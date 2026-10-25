import csv
import json

with open("dataset/sample_output.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cid = row["case_id"]
        st = row["deletion_status"]
        print(f"=== {cid}: {st} ===")
        steps = json.loads(row["steps_json"])
        for s in steps:
            print(f"  Step {s['step_no']}: [{s['phase']}] {s['operation']} -> {s['system_id']}/{s['resource_id']} ({s['state']}) ev={s['evidence_id']}")
        print()