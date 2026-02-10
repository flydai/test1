.PHONY: setup test run

setup:
	python -m pip install -r requirements.txt

test:
	pytest -q

run:
	python -m app.run --input-file examples/basic_intake.txt
