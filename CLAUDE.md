# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Virtual Environment

TODO: add path to venv used for project

## Project Overview

TODO: describe your project

## Template Cleanup

Once the first real code has been added, delete the example files that came from the template:
- `src/template/arithmetic.py`
- `tests/unit/test_arithmetic.py`
- `tests/functional/test_linear.py`

Then update `README.md`: replace the template tutorial ("How to use this template", example code references) with a project-specific description, installation instructions, and usage.

After all cleanup is done, remove this "Template Cleanup" section from both `CLAUDE.md` and `AGENTS.md`.

## Build and Development Commands

```bash
# Installation
pip install -e .                # Production install
pip install -e . --group dev    # Development install with linting/testing tools

# Formatting and linting
make format        # Format with ruff
make check-format  # Check formatting without modifying
make lint          # Lint with ruff + yamllint
make typecheck     # Run mypy type checking

# Testing
make test          # Run all tests
make coverage      # Run tests with coverage report
pytest tests/unit/path/to/test_file.py::test_name -v  # Run a single test

# Pre-commit
make pre-commit    # Run all pre-commit hooks

# Cleanup
make clean         # Remove build artifacts and caches
```

## Architecture

TODO: describe your package structure

```
src/
└── template/
    ├── __init__.py
    └── ...
```

## Code Style

We follow [PEP 8](https://peps.python.org/pep-0008/) to the extent possible.

- Python 3.14, line length 120 characters
- Formatting: `ruff format`, type hints required (mypy enforced)
- **Minimize inline comments.** Code should be self-explanatory through clear names and well-structured logic. If you feel the need to explain *what* the code does, instead: rename variables/functions to be more descriptive, extract complex logic into a well-named helper, or move the explanation into the docstring. Inline comments are acceptable only in rare cases to explain *why* a non-obvious workaround is necessary. Be particularly vigilant about removing verbose AI-generated comments that narrate each step.
- **Remove dead code, commented-out code, debug prints, and unused parameters/functions/imports.** Don't add speculative abstractions or single-use wrappers until a concrete use exists ([YAGNI](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it)).
- **Replace magic numbers with named constants** that document their rationale (iteration caps, tolerances, conversion factors). Don't hardcode values that should be tunable -- expose them via config/CLI or name them. Group constants in a dedicated `constants` module placed in the (sub)package matching their scope of use.
- Use `Path` for filesystem paths; accept `str | Path` at boundaries, keep values as `Path` until the last moment, and convert to string with `.as_posix()`. Prefer `Path` methods (`.unlink()`, `/`, `.suffix`) over `os.path` calls.
- All imports must be at the top of the file, never inside functions or methods. The only sanctioned exception is deferring a heavy/slow import into a function body (e.g. inside a CLI command) so that importing the module doesn't pull in the whole framework.
- Route output through the standard `logging` framework (or the project logger), not `print`. Keep default verbosity low; reserve high-visibility levels for messages users genuinely need.
- Narrow lint suppressions to the specific rule and document why (`# noqa: D102`, not a bare `# noqa`). Keep diffs minimal -- don't reformat unrelated lines.
- Every package/subpackage directory containing `.py` files must contain an `__init__.py` (even if empty). Do not rely on [PEP 420](https://peps.python.org/pep-0420/) implicit namespace packages -- they are silently skipped by `pkgutil.iter_modules` and require extra configuration for mypy and import-linter. Only add re-exports to `__init__.py` if the package has a curated public API.
- For exhaustive dispatch on enums (or other closed `Literal` / tagged unions), use `match`/`case` with a trailing `case _: assert_never(x)` from `typing`. This gives compile-time exhaustiveness checking (mypy errors if a new enum member is added without updating the match), a runtime guard, and satisfies Ruff's `RET503`. Prefer this over `if`/`elif` chains ending in an unchecked fall-through or a plain `raise ValueError(...)`.
- When the same string literals appear in more than one place (dict keys plus function returns, parameter discriminators, repeated comparisons, etc.), define them as a `StrEnum` instead of using raw strings. The same applies to repeated integer constants -- use `IntEnum`. This prevents typos, gives mypy a closed value set to check against, and makes the set of valid values discoverable via the type.

### Naming

- `snake_case` for functions and variables (e.g. `my_nice_function`); `CamelCase` reserved for class names (e.g. `MySuperClass`); constants in `UPPER_CASE`.
- Use descriptive, intention-revealing names; spell out the concept rather than cryptic abbreviations (`three_dimensional` not `three_dim`, not `QQ`/`pp`/`t_t`). Short single-letter names are tolerated only inside well-established mathematical notation (e.g. a variational form or equation that mirrors a paper).
- Prefixes: `create_*` for object creation, `get_*` for access, `n_*` for counts (e.g. `n_channels`, not `nchannels`), `is_*`/`has_*` for booleans.
- Use one canonical term per concept and keep it consistent across code, tests, and docs (don't mix `edge`/`side` or `optimisation`/`optimization` -- pick one, American spelling preferred).
- Name things for what they actually are/do, and rename when behavior diverges (a normalized vector isn't `*_norm`; a method returning "should continue" isn't `check_converged`). Update names after refactors.
- Don't shadow builtins (`row_count`, not `len`) or stdlib module names (`app_logging.py`, not `logging.py`). Never leave placeholder names (`foo`, `tmp`, `claude`) in committed code.
- Encode units and coordinate frames in names when not SI (`max_flow_rate_lpm`, `fin_width_mm`, `position_local`) so a reader can't confuse unit systems or frames.

### Docstrings

- Google style (`Args:`, `Returns:`, `Raises:`). All public functions (those imported outside the module in which they are defined) must have a docstring written so any new developer can understand them. Private functions need only the documentation necessary to explain their functionality. Test functions do not need docstrings.
- **Do not repeat type information in docstrings** -- type hints are the single source of truth (and docstring types drift out of date). Keep the docstring in sync with the signature: remove params that no longer exist, update outdated descriptions.
- Write complete docstrings; never commit placeholder stubs like `_description_` / `_type_` or an empty `Raises:` line.
- Define acronyms and domain jargon on first use (e.g. "Singular Value Decomposition (SVD)"). Cite a reference for non-obvious math/physics so the next reader can follow it.

## API and Function Design

- **Functions returning multiple values must return an attrs class, not a tuple or dict.** Named immutable fields make call sites self-documenting and prevent positional-unpacking errors.
- **Pass only the minimal data a function needs.** Never thread whole aggregate/"god" objects (a global config, a manager holding everything) through a call just to read one field -- accept that field (or a small focused object). Narrow parameters lower coupling and make dependencies explicit.
- **Keep functions small and single-responsibility**, named after what they do. Split functions that mix concerns (compute-from-IO, check-from-enforce, oversized orchestration) into focused pieces.
- **Prefer pure functions:** return new objects rather than mutating arguments. A function should either mutate in place and return `None`, or return a new value -- never both. Side-effect-free functions are predictable, thread-safe, and easier to debug.
- **Avoid hidden side effects and global-state mutation.** A predicate must not mutate state; everything a function does should be reflected in its name. Confine process-wide side effects (changing global config, `matplotlib` rcParams, thread counts) to the entry-point/CLI layer, not reusable library functions.
- **Reuse existing helpers, constructors, and abstractions** instead of duplicating logic. Duplicated formulas and parallel classes drift apart -- consolidate into one shared helper or extend the existing domain type.
- **Place code in the module/package that owns its concern.** Generic helpers go in shared utils; domain logic stays with its domain. Respect the layered package hierarchy.
- **Make a symbol private (leading underscore) only when it is internal to its module**; make it public when it is imported across modules. Don't import another module's private symbols.
- **Avoid runtime `isinstance`/type dispatch.** It duplicates what the type checker should enforce and an `if/elif` chain lets a new subtype silently fall into the wrong `else`. Prefer precise types, polymorphism, or an ABC `@abstractmethod` that forces every subclass to implement the behavior.
- **Use `Optional` / `X | None` only for values that are genuinely absent at runtime.** Model invariants in the type instead: build data structures whose members are all valid, so downstream code never has to check for existence. Scattered `None`-guards signal a missing dedicated class.
- **Don't make mandatory parameters optional**, and don't pass redundant arguments that are derivable from another argument (e.g. passing both a mesh and a function space that already contains it).
- **Don't introduce inheritance that violates the Liskov Substitution Principle:** a specialized variant must not subclass a general case the parent can't stand in for. Use a never-instantiated base class or a `Protocol` instead; only leaf classes get instantiated.
- Provide `create_*` / `from_*` factory classmethods that take exactly the dependencies they need (so tests don't have to build heavy config), and return `Self` / `type(self)(...)` so subtype results stay correctly typed.

## Input Serialization / Deserialization

Do not read files (`.json`, etc.) directly throughout the code. Instead, define a Python object that represents the file's structure and validation rules in one central location, and reuse that same logic for all reads and writes. This keeps file-format changes localized and gives built-in validation.

- Use [`attrs`](https://www.attrs.org/) to define the data structures and [`cattrs`](https://cattrs.readthedocs.io/en/stable/) to serialize/deserialize. Usage of stdlib `dataclasses` (and `NamedTuple` / bare dicts for structured data) is discouraged.
- Prefer `@frozen` over `@define` -- everything should be immutable by default unless mutability is explicitly needed. Use `field(factory=...)` for mutable defaults (never a shared mutable default), and set defaults via `default=`, keeping validators for validation only.
- **Validate input as early as possible -- at the attrs/cattrs layer**, using `validators.instance_of` / `validators.in_` and `__attrs_post_init__`, and a shared cattrs converter configured with `forbid_extra_keys=True`. Don't re-validate the same invariant deep in the stack; downstream code should be able to assume clean values.
- **Keep a single source of truth** for every value, default, and schema read. Don't duplicate a default across the attrs class and a loader, pin a version in multiple files, or read the same config in several places -- one writer, many readers.
- Keep manipulation of raw input files (e.g. editing JSON before it is loaded) outside the core library to the extent possible.
- Don't introduce default `./` / current-working-directory output paths; require explicit output directories so the tool never scatters files in users' working directories.

## Typing

We use `mypy` for static type checking.

- All functions (including tests) must have type annotations on every parameter and the return value. Avoid `Any`.

  ```python
  # Correct
  def create_layer_coefficients(
      mesh: LabeledMesh,
      factory: ThermalLayerFactory,
  ) -> list[CoefficientsWithRegion]: ...

  # Wrong -- no annotations
  def create_layer_coefficients(mesh, factory): ...
  ```

- Use modern typing syntax: builtin generics (`list[int]`, `dict[str, float]` per [PEP 585](https://peps.python.org/pep-0585/)) and `X | None` (PEP 604) instead of `Optional[X]`. `int` is a subtype of `float`, so `int | float` is redundant -- just use `float`.
- **Prefer duck typing / Protocols over concrete types.** If a function needs to know a lot of implementation detail about its argument (e.g. branching on `isinstance`), that signals tight coupling. Type against the minimal interface (e.g. `Iterable[float]`) rather than a concrete class.
- **Interface segregation.** Type against a small set of expected functionalities using `Protocol`s and ABCs. Don't force callers/subclasses to depend on or implement methods they do not need; split fat protocols into narrow ones.
- **Use domain-specific type aliases** (`MeshMarkerId: TypeAlias = int`, `GmshTag`, `BodyLabel`) instead of passing bare `int`/`str` around. An alias documents intent, stops unrelated values of the same base type from being confused, and lets the underlying type change in one place.
- **Use small custom classes** when you want stronger guarantees than an alias provides -- a dedicated class prevents passing an unrelated value of the same base type and lets you validate invariants in `__init__`.

## Error Handling

- **Raise explicit, specific exceptions for invalid user input** -- a project-defined error type (e.g. `InvalidUserInputError`) with an actionable message that names the offending value. **Never use `assert` for validation in production code**: assertions are stripped under `python -O`. Reserve `assert` for tests and internal logic checks. Rule of thumb: *raises are for users of the software (bad inputs); asserts are for programmers checking the logic.*
- **Fail fast and loudly on unsupported/invalid configurations.** Don't warn-and-continue or silently fall back to a default -- a warning is easy to miss and produces silently wrong results. Reserve warnings for genuinely actionable, uncommon conditions so users don't become desensitized.
- **Guard against division by zero / near-zero / non-finite denominators** before dividing. A tiny or zero denominator silently explodes results or produces `NaN`/`inf` -- check and raise a clear error first.
- **Don't catch broad `Exception` and swallow it** or downgrade it to a warning. Catch the narrowest type that applies, use `raise NewError(...) from original` to preserve the traceback, and put cleanup in `finally` (not only in `except`).
- **Don't validate at import/class scope** -- raising at module or class body explodes on import. Move guards into `__init__` or the function that needs them.
- **Use `is None` checks, not truthiness, for optional numeric/integer values that can legitimately be `0`.** `if x:` and `any([...])` treat `0` (a region tagged `0`, a zero pressure drop) as absent.
- **Don't use sentinel magic values (`-1`, `0`, `1e50`) to mean "absent"** -- use `None` and check `is None`. Sentinels conflate magic numbers with domain logic and break when a real value collides with the sentinel.

## Defensive Programming

Defensive programming means writing code that anticipates and handles unexpected internal states. Use `if` statements with `raise` to verify internal invariants and assumptions during development.

**Key principle:** if a defensive check fails, it indicates a *bug in our code*, not invalid user input. User-input errors should be handled gracefully with informative, specific exceptions (see Error Handling above).

**Use defensive programming to:**
- Verify invariants that should always hold if the code is correct
- Catch logic errors during development
- Document assumptions about internal state

**Do NOT use defensive programming to:**
- Validate user input -- handle that at system boundaries via serialization/deserialization and raise specific, descriptive exceptions
- Check types at runtime -- rely on proper data structures (`attrs` classes), type hints, and mypy instead
- Handle expected error conditions -- use proper error handling

```python
# Good: verify an internal invariant
def compute_average_temperature(temperatures: list[float]) -> float:
    if len(temperatures) == 0:
        raise ValueError("temperatures list should never be empty at this point")
    return sum(temperatures) / len(temperatures)

# Bad: using if/raise for type checking -- use a typed data structure instead
def process_data(data):
    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")

# Bad: silently swallowing an error / returning None
def load_config(filepath: Path) -> Config | None:
    if not filepath.exists():
        print(f"Error: file {filepath} not found")
        return None

# Bad: raising a generic exception without context
def load_config(filepath: Path) -> Config:
    if not filepath.exists():
        raise Exception("File not found")

# Good: specific exception with a descriptive message
def load_config(filepath: Path) -> Config:
    if not filepath.exists():
        raise FileNotFoundError(f"Config file not found: {filepath}")
```

## Units and Physical Quantities

For scientific/engineering code that handles physical quantities:

- **Keep quantities in SI internally**; encode any user-facing non-SI unit in the name (`value_lpm`, `fin_width_mm`) and convert at the load/display boundary only.
- **Centralize conversions** through a single shared unit registry (e.g. [Pint](https://pint.readthedocs.io/)) or named conversion constants; never sprinkle hardcoded factors like `* 1e6` or `* 1e3` through the code -- they silently introduce errors.
- **Do `is_nondimensional` / rescaling once, at the boundary** (load or print), not scattered deep in the stack. Document sign and unit-system conventions.
- **Don't attach units to integer identifiers** (region markers, ids) -- reserve units for genuine physical quantities.
- Verify dimensional consistency: a limit and the value it bounds must share units.

## Performance

- **Hoist invariant work out of loops:** compute scale factors, forms, solvers, and file reads once and reuse them; don't recompute or re-read inside a loop.
- **Avoid deeply nested Python loops over large data.** Vectorize with numpy (meshgrid, boolean masks, `np.clip`, `np.nonzero`) instead of element-wise Python loops over millions of items. Note `list.pop(0)` is O(n) -- use `collections.deque` for FIFO.
- **Defer heavy framework imports** into the function body that needs them, so importing a module (or starting an unrelated CLI command) stays fast.
- **Be mindful of memory for large dense structures.** A dense matrix with many DOFs can be gigabytes; choose a data structure matching the object's nature (a list of vectors instead of reallocating a growing matrix; sparse structures for diagonal/structured data).

## Testing Conventions

Structure the test suite following the test pyramid: many fast unit tests at the base, fewer integration/functional tests in the middle, and a small number of expensive end-to-end / verification tests at the top.

### Test placement and coverage

- **Unit tests** (`tests/unit/`): test individual functions and classes in isolation. Construct inputs directly (e.g. hand-crafted data, attrs objects) rather than calling other production functions to build them. Every public function and class should have at least one unit test. These are the tests used to compute coverage. A good unit test also clearly shows a new developer the intended use of the function.
- **Functional tests** (`tests/functional/`): test composed behavior and end-to-end workflows where multiple functions work together. This includes CLI commands, file I/O round-trips, and integration with external libraries. Don't over-rely on slow end-to-end tests just to raise coverage -- pin behavior with fast unit tests.
- **Verification tests** (`tests/verification/`, where applicable): computationally expensive tests that check correctness against a reference solution using realistic parameters. Run only on merges to main branches, not on every push.
- Every new module must have corresponding tests in both `tests/unit/` and `tests/functional/` where applicable. Do not put all tests in one category.

### Test quality

- **Assertions must be meaningful: check exact/expected values, not truthiness.** Loose checks (file exists, `size > 0`, `is not None` on a never-`None` return) pass even when output is wrong. Assert against golden references or known computed values -- e.g. if a function computes `sin(a * y) + c * cos(a * x)`, assert the numeric result for a known input.
- **Compare floating-point values with `np.isclose` / `np.allclose`, never `==`.** Use an explicit absolute tolerance when comparing against zero, and don't inflate tolerances to the point where they hide regressions.
- Test boundary conditions and edge cases (zero inputs, empty collections, minimum/maximum values, off-by-one) and cover every error branch, not just the happy path.
- **Add a regression test for every bug fix** -- one that fails before the fix and passes after. A demo or manual check is not a regression test; without it the bug can silently re-emerge.
- **Don't test private functions, schema-level guarantees, or tautologies.** That a field is frozen/optional is part of the schema, not behavior; testing type-checker-guaranteed conditions inflates the suite without catching bugs. Test through the public API.
- Apply the same standards (typing, clear structure) to test code, and **don't reimplement the function under test step-for-step** -- a shared bug would then slip through. Assert against independently hand-computed expected values.
- Parametrized tests should include a `test_description` parameter explaining the purpose of each case; prefer `@pytest.mark.parametrize` over loops or duplicated test functions (it isolates failures per case):

  ```python
  @pytest.mark.parametrize(
      "is_split_flow,has_symmetry,expected_multiplier,test_description",
      [
          (False, False, 1.0, "No split flow, no symmetry"),
          (True, False, 2.0, "Split flow, no symmetry"),
          (True, True, 4.0, "Split flow, with symmetry"),
      ],
  )
  def test_compute_multiplier(is_split_flow, has_symmetry, expected_multiplier, test_description): ...
  ```

- **Avoid mocking.** Prefer real but quick runs -- mocks drift out of date and keep passing while the real code breaks. Reserve mocks for genuinely expensive externals (databases, slow services).

### Fixtures and temporary files

- Use the `tmp_path` fixture for temporary files; never use `tempfile` or manual cleanup (the fixture is auto-cleaned). Document and file a follow-up for any deviation.
- Compose small, focused, reusable fixtures (e.g. separate `mesh`, `boundary_markers`, `problem_data`) rather than one fat fixture. Place fixtures shared across multiple files in `tests/conftest.py`; place helper functions reused across files in `tests/helpers.py`.
- Avoid module-level global test variables -- one test can corrupt another's state. Don't prefix non-test helpers with `test_`/`Test` or pytest will mis-collect them.

### CLI testing

- Keep CLI entry points as thin wrappers that parse input and delegate to a framework-free function containing the actual logic. Test that logic directly (without spawning a process) for end-to-end coverage. Decorated CLI functions can't be called from Python, so the logic must live in a plain function.
- Use the CLI runner only to test the CLI plumbing itself, not full end-to-end flows (it spawns new processes).
- When invoking a command with a CLI runner, always set `catch_exceptions=False` (so real failures surface instead of being swallowed) and assert on `exit_code` (printing `result.output` on failure).

### Matplotlib outputs and golden images

Figures depend on the environment (OS, FreeType, Matplotlib version, backend, DPI), so comparing generated PNGs against a committed baseline produces false failures on CI. Split responsibilities instead:

1. **Data layer** -- a pure function mapping inputs to a stable in-memory structure (arrays, attrs classes). No Matplotlib calls.
2. **Plotting layer** -- functions that take that structure, apply style, and call `savefig`.

Then: write **strong** tests on the data layer (explicit expected arrays / grouping / ordering -- this is where correctness is enforced), and **weak** smoke tests on the plotting layer (assert the output file exists after `savefig`, exercise boolean flag branches). Reserve pixel-identical golden-image comparison for a workflow where the entire render stack is pinned (e.g. a dedicated Docker image).

For headless CI, set a non-interactive backend with `matplotlib.use("Agg")` **before** importing `pyplot` -- configuring it afterward has no effect.

### Design for testability

- Keep entry points (scripts, CLI commands, etc.) as thin wrappers that parse input and delegate to a function containing the actual logic. This allows unit-testing the logic without invoking the entry point.

## Packaging and Dependencies

- **Declare every direct dependency** in `pyproject.toml` as soon as you import it directly -- don't rely on it arriving transitively.
- **Pin dependencies to exact versions** (`==`) for reproducible builds and let a tool like Dependabot bump them deliberately; a `>=` range can silently pull a breaking release. Pin third-party GitHub Actions to immutable commit SHAs for supply-chain safety. Keep tool config in sync across files.
- **Ship runtime resource files in package data.** Anything resolved via `Path(package.__file__).parent` must be declared as package data, or it works in editable installs but fails under `pip install`.
- **Keep packages independent and avoid circular dependencies.** A foundational package (logger, config) must not import from higher-level ones; sibling packages shouldn't depend on each other -- cross-cutting code gets its own package.

## Developer Tools

### Pre-commit hooks

We use [pre-commit](https://pre-commit.com/) to run automated checks before each commit (configured in `.pre-commit-config.yaml`).

```bash
pre-commit install              # one-time setup per clone
pre-commit run --all-files      # run all hooks manually (or: make pre-commit)
pre-commit run ruff --all-files # run a single hook
```

If a check fails, the commit is aborted -- fix and recommit. Use `git commit --no-verify` only sparingly (e.g. WIP commits); CI enforces the same checks regardless.

### Ruff (lint + format)

We use [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting (configured in `pyproject.toml`). Enabled rule sets include flake8-builtins, flake8-bugbear, flake8-comprehensions, pydocstyle, pycodestyle, pyflakes, pep8-naming, NumPy rules, flake8-bandit, isort, pyupgrade, and flake8-type-checking.

```bash
ruff format .        # format
ruff check --fix .   # lint and auto-fix
```

### Mypy

Static type checking, configured in `pyproject.toml`. Key settings: `disallow_untyped_defs` (annotations required on all functions), `check_untyped_defs`, and `ignore_missing_imports` (tolerate untyped third-party packages). Run with `make typecheck`.

### Pytest

[pytest](https://docs.pytest.org/) is the test framework. Common plugins: `pytest-xdist` (parallel local runs, e.g. `-n 8`), `pytest-cov` (coverage), `pytest-timeout` (prevent hangs), and `pytest-split` (parallelize the suite across CI machines). Mark tests that are unsafe to run in parallel (e.g. those spawning a new process) so they run serially.

## Pull Requests and Workflow

- **Keep PRs focused on a single idea**; defer unrelated cleanups to their own PR or a tracking issue. Multi-concern PRs are hard to review and risk regressions.
- PR titles follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `chore:` (add `!` for breaking changes). One type per PR, formatted `<type>: <description>`.
- **Record user-facing changes in the CHANGELOG** -- new features, output/interface/JSON changes -- under the right section and the latest version, with the PR number. Keep entries concise and user-facing (no internal class names or math). Never edit historical CHANGELOG entries. Breaking changes (`!`) signal that users may need to update their workflows.
- **Track deferred work and known hacks** in an issue or tech-debt list, not silently in a code comment, so they stay visible and schedulable.
- Engage with reviewer and automated suggestions before merging -- apply each or explain why not.
