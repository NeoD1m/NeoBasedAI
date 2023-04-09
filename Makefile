SYSTEM_PYTHON := $(shell which python3)
PYTHON        := venv/bin/python
PIP           := $(PYTHON) -m pip
PYTEST        := $(COVERAGE) run -m pytest

venv:
	$(SYSTEM_PYTHON) -m venv venv
	$(PIP) install --upgrade pip wheel

.PHONY: pip-install
pip-install: venv ## Install the project
	$(PIP) install -r requirements.txt

.PHONY: test
test:
	$(PYTEST) -v tests/

.PHONY: clean-venv
clean-venv: ## Reinstall dependencies
	rm -rf venv
	make venv
	make pip-install-dev

.PHONY: clean
clean: ## Remove __pycache__
	bash -c 'find src/ -type d -name __pycache__ -exec rm -rf {} +'

