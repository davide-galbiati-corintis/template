.PHONY: format check-format lint typecheck test coverage pre-commit clean

format:
	ruff format .

check-format:
	ruff format --check .

lint:
	ruff check .
	yamllint --strict -c=.yamllint .

typecheck:
	mypy src/

test:
	pytest tests/

coverage:
	pytest --cov=src --cov-branch --cov-report=term-missing tests/

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf .mypy_cache .pytest_cache *.egg-info dist build .coverage coverage.xml htmlcov
