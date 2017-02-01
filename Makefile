VE ?= venv

.PHONY: check
check: lint test

.PHONY: test-all
	check-all:
	tox

.PHONY: lint
lint: $(VE)
	$(VE)/bin/python setup.py flake8

.PHONY: test
test: $(VE)
	$(VE)/bin/python setup.py nosetests

.PHONY: docs
docs: sphinx-clean sphinx-apidoc sphinx-html

.PHONY: clean
clean:
	rm -rf $(VE) .tox
	find ffmddb -name *.py[co] -exec rm -f {} \;

$(VE):
	virtualenv $(VE)

######
# Sphinx stuff:

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = ffmddb
SOURCEDIR     = docs
BUILDDIR      = docs/_build
APIDIR        = docs/api

# Put it first so that "make" without argument is like "make help".
sphinx-help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

sphinx-apidoc:
	sphinx-apidoc -M -T -e -a -o $(APIDIR) $(SPHINXPROJ) "*_test.py"

sphinx-clean:
	- rm $(APIDIR)/$(SPHINXPROJ).*
	- rm -rf $(BUILDDIR)

.PHONY: sphinx-help sphinx-autodoc Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
sphinx-%: Makefile
	@ PYTHONPATH=. $(SPHINXBUILD) -M `echo $@ | sed -e 's/^sphinx-//'` "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
