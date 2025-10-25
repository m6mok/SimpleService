check:
	uv run --no-group test ruff check -q src
	uv run --no-group test flake8 src
	uv run --no-group test black -q --check src
	uv run --no-group test mypy --no-error-summary src

fix:
	uv run --no-group test ruff format -q src
	uv run --no-group test black -q src
	uv run --no-group test isort -q src

test:
	uv run --no-dev --group test pytest -v --cov=src --cov-report=term-missing
