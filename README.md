# Stage 5 Advanced Assessment: SOC Production Hunt Engine
**Evidence Marker:** UBI-A5-3A20CEDE0A6A

## Execution Instructions
This pipeline uses Python 3.11+ and DuckDB. To execute a clean build:

`make build INPUT=project/raw/evidence`

**What this command does:**
- Verifies integrity against the source manifest.
- Executes streaming ingestion, deduplication, and schema drift quarantine to `data-quality-register.csv`.
- Benchmarks RAM and execution time to `benchmark.json`.
- Executes behavioral queries from the `queries/` directory.
- Exports scored tables (`evidence-index.csv`, `tp-fp-table.csv`).

## Automated Tests
To verify schema drift handling, aliases, and empty inputs:
`make test`