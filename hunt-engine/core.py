import json
import csv
import hashlib
import duckdb
from pathlib import Path

class HuntDatabase:
    """Safe DuckDB connection manager."""
    def __init__(self, db_path="clean.db"):
        self.db_path = db_path
    def __enter__(self):
        self.conn = duckdb.connect(self.db_path)
        self.conn.execute("PRAGMA memory_limit='4GB'")
        return self.conn
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'conn'): self.conn.close()

def process_ingestion(source_dir: str):
    """Verifies manifest row counts, streams logs, handles drift, and outputs quarantine."""
    source_path = Path(source_dir)
    metrics = {"total_raw": 0, "accepted": 0, "duplicates": 0, "quarantined": 0}
    seen_hashes = set()

    # 1. Read the Source Manifest for Expected Row Counts
    manifest_files = list(source_path.glob("*manifest*.csv"))
    if not manifest_files:
        print("[!] No manifest CSV found. Proceeding with caution.")
        return metrics
        
    expected_counts = {}
    with open(manifest_files[0], 'r', encoding='utf-8-sig') as m:
        for row in csv.reader(m):
            # Skip headers (like 'file', 'count', 'records', etc.)
            if not row or 'file' in row[0].lower() or not row[1].strip().isdigit(): 
                continue
            expected_counts[row[0].strip()] = int(row[1].strip())

    # 2. Open the exact requested quarantine file name
    with open("data-quality-register.csv", 'w', newline='', encoding='utf-8') as q_file:
        q_writer = csv.writer(q_file)
        q_writer.writerow(["reason_code", "source_file", "row_id", "raw_payload"])

        for filename, expected_count in expected_counts.items():
            filepath = source_path / filename
            if not filepath.exists() and (source_path / "source" / filename).exists():
                filepath = source_path / "source" / filename
                
            if not filepath.exists(): 
                continue

            print(f"[*] Ingesting {filename} (Expected rows: {expected_count})...")
            
            file_raw_count = 0
            
            # 3. Stream and clean data safely
            with open(filepath, 'r', encoding='utf-8') as raw_file:
                for line_num, line in enumerate(raw_file, start=1):
                    line = line.strip()
                    if not line: continue
                    
                    file_raw_count += 1
                    metrics["total_raw"] += 1

                    try:
                        parsed = json.loads(line)
                        if "timestamp" not in parsed or "log_id" not in parsed:
                            raise ValueError("SCHEMA_DRIFT_MISSING_ROUTING_FIELDS")
                        
                        row_hash = hashlib.sha256(json.dumps(parsed, sort_keys=True).encode()).hexdigest()
                        if row_hash in seen_hashes:
                            metrics["duplicates"] += 1
                            continue
                            
                        seen_hashes.add(row_hash)
                        metrics["accepted"] += 1
                        
                    except (json.JSONDecodeError, ValueError) as e:
                        metrics["quarantined"] += 1
                        q_writer.writerow([str(e), filename, line_num, line])
            
            # GATE: Unaccounted Source Row Check
            if file_raw_count != expected_count:
                raise ValueError(f"INTEGRITY ESCALATION: {filename} row count mismatch! Expected {expected_count}, Got {file_raw_count}")
            else:
                print(f"[+] {filename} verified: 100% of rows accounted for.")
                        
    return metrics