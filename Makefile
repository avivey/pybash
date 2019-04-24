
default: test

.venv:
	virtualenv -p python3 .venv
	.venv/bin/pip install -r requirements_dev.txt

lint:
	.venv/bin/black -t py37 pybash/ tests/
	.venv/bin/mypy pybash/

test:
	.venv/bin/pytest tests/
