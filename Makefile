PYTHON = python3
UV = UV_SKIP_WHEEL_FILENAME_CHECK=1 uv
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
ifdef VIRTUAL_ENV
	ACTIVE = --active
else
	ACTIVE =
endif

all: install run

install:
	$(UV) sync $(ACTIVE)

run:
	$(UV) run $(ACTIVE) $(PYTHON) -m src

debug:
	$(UV) run $(ACTIVE) $(PYTHON) -m src -m pdb

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".venv" -exec rm -rf {} +
	find . -type d -name ".vscode" -exec rm -rf {} +

lint:
	$(UV) $(ACTIVE) $(PYTHON) -m flake8 src/
	$(UV) $(ACTIVE) $(PYTHON) -m mypy $(MYPY_FLAGS) src/

lint-strict:
	$(UV) $(ACTIVE) $(PYTHON) -m flake8 src/
	$(UV) $(ACTIVE) $(PYTHON) -m mypy --strict src/

.PHONY: all install run debug clean lint lint-strict