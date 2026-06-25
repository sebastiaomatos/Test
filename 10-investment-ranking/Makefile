.PHONY: run refresh test clean install

install:
	pip install -r requirements.txt

run:
	CURL_CA_BUNDLE=/root/.ccr/ca-bundle.crt python run.py

refresh:
	CURL_CA_BUNDLE=/root/.ccr/ca-bundle.crt python run.py --refresh

test:
	CURL_CA_BUNDLE=/root/.ccr/ca-bundle.crt python -m pytest tests/ -v

clean:
	rm -rf data/raw/*.parquet outputs/*.png outputs/*.xlsx outputs/*.csv

lint:
	python -m py_compile src/sources/yahoo.py src/sources/bcb.py src/fx.py \
	    src/loader.py src/metrics.py src/validate.py src/report.py run.py
	@echo "Sintaxe OK"
