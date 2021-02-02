THIS_FILE := $(lastword $(MAKEFILE_LIST))
CURRENT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


.PHONY: dist
dist: ## generate distribution package
	$(MAKE) clean
	python3 setup.py sdist bdist_wheel

.PHONY: upload
upload: ## upload distribution package to PyPi
	$(MAKE) dist
	python3 -m twine upload dist/*

.PHONY: test-upload
test-upload: ## upload distribution package to PyPi test server
	$(MAKE) dist
	python3 -m twine upload --repository testpypi dist/*

.PHONY: upgrade-dist-tools
upgrade-dist-tools: ## upgrade packages necessary for testing, building, packaging and uploading to PyPi
	python3 -m pip install --upgrade pip setuptools wheel tqdm twine pytest mkdocs mkdocs

.PHONY: install-requirements
install-requirements: ## install requirements
	pip3 install -r requirements.txt

.PHONY: install
install: ## install from source
	pip3 install .

.PHONY: clean
clean: ## cleans the project directory
	@rm -rf dist/

.PHONY: run
run: ## install and run from source
	$(MAKE) clean
	$(MAKE) dist
	$(MAKE) install
	dsp-metadata

.PHONY: doc
doc: ## build and serve doc
	mkdocs build
	mkdocs serve

.PHONY: deploy-doc
deploy-doc: ## deploy doc to github pages
	mkdocs gh-deploy

