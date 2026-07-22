import pytest
import sys
import os
from pathlib import Path

# 1. Force Python to look inside the hyphenated folder
sys.path.insert(0, os.path.abspath('hunt-engine'))
from core import process_ingestion

def test_missing_input_and_schema_drift(tmp_path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    
    # 2. Updated the mock manifest to use row counts instead of hashes
    manifest = raw_dir / "manifest.csv"
    manifest.write_text("file,count\nauth.jsonl,0\n", encoding='utf-8')
    
    (raw_dir / "auth.jsonl").write_text("", encoding='utf-8') 
    
    metrics = process_ingestion(str(raw_dir))
    
    assert metrics["total_raw"] == 0
    assert metrics["quarantined"] == 0