.PHONY: build test clean

build:
	python -m hunt-engine.cli ingest --source $(INPUT)
	python -m hunt-engine.cli hunt --module all
	
test:
	pytest tests/ -v

clean:
	rm -f clean.db benchmark.json normalized-timeline.csv campaign-graph.json tp-fp-table.csv data-quality-register.csv evidence-index.csv