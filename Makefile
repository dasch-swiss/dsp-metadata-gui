THIS_FILE := $(lastword $(MAKEFILE_LIST))
CURRENT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


.PHONY: dist
dist: ## generate distribution package
	$(MAKE) clean
	python setup.py sdist bdist_wheel

.PHONY: upload
upload: ## upload distribution package to PyPi
	$(MAKE) dist
	python -m twine upload dist/*

.PHONY: prepare-release
prepare-release: ## prepare everythign for relaese
	pipenv requirements > requirements.txt

.PHONY: install
install: ## install from source
	pip install . -e

.PHONY: clean
clean: ## cleans the project directory
	@rm -rf dist/
	@rm -rf build/

.PHONY: install-and-run
install-and-run: ## install and run from source
	$(MAKE) clean
	$(MAKE) dist
	$(MAKE) install
	dsp-metadata

.PHONY: doc
doc: ## build and serve doc
	mkdocs build
	mkdocs serve

.PHONY: help
help: ## this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help
