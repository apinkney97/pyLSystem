.phony: test fmt lint

test:
	pytest tests/

fmt:
	isort .
	black .

lint:
	pylint lsystem/
