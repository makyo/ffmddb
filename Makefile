VE ?= venv

.PHONY: test
test: $(VE)
	$(VE)/bin/python setup.py flake8
	$(VE)/bin/python setup.py nosetests

.PHONY: test-all
test-all:
	tox

.PHONY: clean
clean:
	rm -rf $(VE)
	find ffmddb -name *.py[co] -exec rm -f {} \;

$(VE):
	virtualenv $(VE)
