.PHONY: build test clean

build:
	mkdir -p raw_data/
	unzip -o $(INPUT) -d raw_data/
	python hunt-engine/cli.py ingest --source raw_data/
	python hunt-engine/cli.py hunt --module all
	
test:
	pytest tests/ -v

clean:
	rm -f clean.db benchmark.json normalized-timeline.csv campaign-graph.json tp-fp-table.csv data-quality-register.csv evidence-index.csv
	rm -rf raw_data/