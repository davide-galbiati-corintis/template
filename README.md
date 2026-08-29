# Code Project Template

A Python project template pre-configured with linting, formatting, type checking, testing, and CI.
Based on the conventions and tooling used in the glaciercore repository.

## How to use this template

1. **Create your repo** from this template using the "Use this template" button on GitHub.
   Choose the repo name carefully -- it will be used as the Python package name automatically
   (e.g., repo `cool-code` becomes package `cool_code`).

2. **Fill in the TODOs**:
   - `pyproject.toml` -- project description.
   - `CLAUDE.md` / `AGENTS.md` -- virtual environment path, project overview, architecture.
   - `src/template/__init__.py` -- package docstring.

3. **Start prompting**: begin writing code with your AI agents. The `CLAUDE.md` and `AGENTS.md`
   files instruct agents to write clean, well-structured code with type hints, docstrings, and accompanying unit and functional tests. They will also automatically delete
   the template example files (`arithmetic.py`, `test_arithmetic.py`, `test_linear.py`) once
   real code is added, and update this README with project-specific content.

## Quickstart

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode (includes linting, testing, formatting tools)
pip install -e . --group dev

# Set up pre-commit hooks
pre-commit install

# Verify everything works
make test
```

To install only production dependencies (no dev tools):

```bash
pip install -e .
```

> **Note:** `--group` requires pip 25.1 or newer. Run `pip install --upgrade pip` if needed.

## Makefile targets

| Target         | Description                                      |
|----------------|--------------------------------------------------|
| `make format`       | Format code with ruff                       |
| `make check-format` | Check formatting without modifying files    |
| `make lint`         | Lint code with ruff + yamllint              |
| `make typecheck`    | Run mypy type checking                      |
| `make test`         | Run all tests with pytest                   |
| `make coverage`     | Run tests with coverage report              |
| `make pre-commit`   | Run all pre-commit hooks                    |
| `make clean`        | Remove build artifacts and caches           |

## Project structure

```
├── src/
│   └── template/        # Your package source code (src-layout)
│       ├── __init__.py
│       └── ...
├── tests/
│   ├── unit/                 # Unit tests
│   ├── functional/           # Functional / integration tests
│   └── conftest.py           # Shared test fixtures
├── .github/workflows/
│   ├── ci.yml                # CI pipeline (format, lint, typecheck, test)
│   └── lint-pr-title.yml     # Enforce Conventional Commit PR titles
├── .pre-commit-config.yaml   # Pre-commit hook configuration
├── .editorconfig             # Editor defaults (indentation, line endings)
├── CLAUDE.md                 # AI agent guidance (Claude)
├── AGENTS.md                 # AI agent guidance (generic)
├── makefile                  # Development task runner
└── pyproject.toml            # Project metadata and tool configuration
```

## Coding conventions

See `CLAUDE.md` or `AGENTS.md` for the full coding style guide. Key points:

- Python 3.14, 120-character line length
- Type hints on all functions (mypy enforced)
- Google-style docstrings
