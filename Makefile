# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

include default.mk

define mk-venv-link
	@if [ -n "$(WORKON_HOME)" ] ; then \
		echo $(ROOT_DIR) > $(VENV_ROOT)/.project; \
		if [ ! -d $(WORKON_HOME)/$(PKG_NAME) -a ! -L $(WORKON_HOME)/$(PKG_NAME) ]; \
		then \
			ln -s $(ROOT_DIR)/$(VENV_ROOT) $(WORKON_HOME)/$(PKG_NAME); \
			echo ; \
			echo Since you use virtualenvwrapper, we created a symlink; \
			echo "so you can also use \"workon $(PKG_NAME)\" to activate the venv."; \
			echo ; \
		fi; \
	fi
endef

define rm-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		if [ -L "$(WORKON_HOME)/$(PKG_NAME)" -a -f "$(WORKON_HOME)/$(PKG_NAME)" ]; \
		then \
			$(RM) $(WORKON_HOME)/$(PKG_NAME); \
		fi; \
	fi
endef

requirements/%.txt: requirements/%.in $(VENV_BIN)
	$(VENV_BIN)/pip-compile --allow-unsafe --strip-extras --generate-hashes --output-file=$@ $<

## Public targets

$(VENV_PYTHON): $(VENV_ROOT)
	@echo

$(VENV_ROOT):
	@echo $(CS)Creating a Python environment $(VENV_ROOT)$(CE)
	$(VIRTUALENV) --prompt $(PKG_NAME) $(VENV_ROOT)
	@echo
	@echo Done.
	@echo
	@echo To active it manually, run:
	@echo
	@echo "    source $(VENV_BIN)/activate"
	@echo
	@echo See https://docs.python.org/3/library/venv.html for more.
	@echo
	$(call mk-venv-link)

.PHONY: init
init: $(VENV_PYTHON)
	@echo $(CS)Set up virtualenv$(CE)
	$(VENV_PIP) install --progress-bar=off --upgrade pip pip-tools setuptools wheel
	@echo

.PHONY: install
install: $(REQUIREMENTS)
	@echo $(CS)Installing $(PKG_NAME) and all its dependencies$(CE)
	$(VENV_BIN)/pip-sync $^
	$(VENV_PIP) install --progress-bar=off -e .
	@echo

.PHONY: uninstall
uninstall:
	@echo $(CS)Uninstalling $(PKG_NAME)$(CE)
	- $(VENV_PIP) uninstall --yes $(PKG_NAME) &2>/dev/null

	@echo Verifying...
	cd .. && ! $(VENV_PYTHON) -m $(PKG_NAME) --version &2>/dev/null

	@echo Done.
	@echo

.PHONY: clean
clean:
	@echo $(CS)Remove build and tests artefacts and directories$(CE)
	$(call rm-venv-link)
	find ./ -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r ./build ./dist ./*.egg-info
	$(RM) -r ./.cache ./.pytest_cache
	$(RM) -r ./htmlcov
	$(RM) ./coverage.*
	@echo

.PHONY: maintainer-clean
maintainer-clean: clean
	@echo $(CS)Performing full clean$(CE)
	-$(RM) -r $(VENV_ROOT)
	$(call rm-venv-link)
	$(RM) requirements/*.txt
	@echo

.PHONY: lint
lint: $(VENV_PYTHON)
	@echo $(CS)Running linters$(CE)
	-$(VENV_BIN)/flake8 $(FLAKE8_FLAGS) ./
	$(VENV_BIN)/pylint $(PYLINT_FLAGS) ./$(PKG_NAME)
	@echo

.PHONY: typecheck
typecheck: $(VENV_PYTHON)
	@echo $(CS)Type check with mypy$(CE)
	$(VENV_BIN)/mypy $(MYPY_FLAGS) ./$(PKG_NAME)
	@echo

.PHONY: test
test: $(VENV_PYTHON)
	@echo $(CS)Running tests$(CE)
	$(VENV_BIN)/coverage erase
	$(VENV_BIN)/coverage run -m pytest $(PYTEST_FLAGS) ./$(PKG_NAME) ./tests
	@echo

.PHONY: ccov
ccov: $(VENV_PYTHON)
	@echo $(CS)Combine coverage reports$(CE)
	$(VENV_BIN)/coverage combine
	$(VENV_BIN)/coverage report
	$(VENV_BIN)/coverage html
	$(VENV_BIN)/coverage xml
	@echo

.PHONY: manifest
manifest:
	@echo $(CS)Check MANIFEST.in for completeness$(CE)
	$(VENV_BIN)/check-manifest -v
	@echo

.PHONY: build
build: manifest sdist wheel

.PHONY: check-dist
check-dist: $(VENV_PYTHON)
	@echo $(CS)Check distribution files$(CE)
	$(VENV_PIP) install twine check-wheel-contents
	$(VENV_BIN)/twine check ./dist/*
	$(VENV_BIN)/check-wheel-contents ./dist/*.whl
	@echo

.PHONY: test-all
test-all: uninstall clean install test test-dist lint typecheck

.PHONY: test-dist
test-dist: test-sdist test-wheel

.PHONY: sdist
sdist:
	@echo $(CS)Creating source distribution$(CE)
	$(VENV_PYTHON) -m build --sdist
	@echo

.PHONY: test-sdist
test-sdist: $(VENV_PYTHON) sdist
	@echo $(CS)Testing source distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.gz
	@echo
	$(VENV_BIN)/$(PKG_NAME) --version
	@echo

.PHONY: wheel
wheel: $(VENV_PYTHON)
	@echo $(CS)Creating wheel distribution$(CE)
	$(VENV_PYTHON) -m build --wheel
	@echo

.PHONY: test-wheel
test-wheel: $(VENV_PYTHON) wheel
	@echo $(CS)Testing built distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.whl
	@echo
	$(VENV_BIN)/$(PKG_NAME) --version
	@echo

.PHONY: publish
publish: test-all

.PHONY: help
help:
	@echo $(PKG_NAME)
	@echo
	@echo 'Run "make init" first to install and update all dev dependencies.'
	@echo 'See "default.mk" for variables you might want to set.'
	@echo
	@echo 'Available targets:'
	@echo
	@echo '  help:         Show this help and exit'
	@echo '  init:         Set up virtualenv (has to be launched first)'
	@echo '  install:      Install project and all its dependencies'
	@echo '  uninstall:    Uninstall local version of the project'
	@echo '  build:        Build $(PKG_NAME) distribution (sdist and wheel)'
	@echo '  sdist:        Creating source distribution'
	@echo '  wheel:        Creating wheel distribution'
	@echo '  publish:      Publish $(PKG_NAME) distribution to the repository'
	@echo '  check-dist:   Check integrity of the distribution files and validate package'
	@echo '  manifest:     Check MANIFEST.in in a source package'
	@echo '  lint:         Lint the code'
	@echo '  typecheck:    Type check with mypy'
	@echo '  test:         Run unit tests with coverage'
	@echo '  test-dist:    Testing package distribution and installation'
	@echo '  test-sdist:   Testing source distribution and installation'
	@echo '  test-wheel:   Testing built distribution and installation'
	@echo '  test-all:     Test everything'
	@echo '  ccov:         Combine coverage reports'
	@echo '  clean:        Remove build and tests artefacts and directories'
	@echo '  maintainer-clean:'
	@echo '                Delete almost everything that can be reconstructed'
	@echo '                with this Makefile'
	@echo
	@echo 'Virtualenv:'
	@echo
	@echo '  Python:       $(VENV_PYTHON)'
	@echo '  pip:          $(VENV_PIP)'
	@echo
	@echo 'Flags:'
	@echo
	@echo '  FLAKE8_FLAGS: $(FLAKE8_FLAGS)'
	@echo '  PYTEST_FLAGS: $(PYTEST_FLAGS)'
	@echo '  PYLINT_FLAGS: $(PYLINT_FLAGS)'
	@echo '  MYPY_FLAGS:   $(MYPY_FLAGS)'
	@echo
	@echo 'Environment variables:'
	@echo
	@echo '  PYTHON:       $(PYTHON)'
	@echo '  WORKON_HOME:  ${WORKON_HOME}'
	@echo '  VIRTUAL_ENV:  ${VIRTUAL_ENV}'
	@echo '  SHELL:        $(shell echo $$SHELL)'
	@echo '  TERM:         $(shell echo $$TERM)'
	@echo
