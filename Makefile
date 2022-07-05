# Taken from: https://github.com/sensu/sensu-go-ansible/blob/master/Makefile

# Make sure we have ansible_collections/paloaltonetworks/panos_enhanced
# as a prefix. This is ugly as heck, but it works. I suggest all future
# developer to treat next few lines as an opportunity to learn a thing or two
# about GNU make ;)
collection := $(notdir $(realpath $(CURDIR)      ))
namespace  := $(notdir $(realpath $(CURDIR)/..   ))
toplevel   := $(notdir $(realpath $(CURDIR)/../..))

err_msg := Place collection at <WHATEVER>/ansible_collections/paloaltonetworks/panos
ifneq (panos,$(collection))
  $(error $(err_msg))
else ifneq (paloaltonetworks,$(namespace))
  $(error $(err_msg))
else ifneq (ansible_collections,$(toplevel))
  $(error $(err_msg))
endif

python_version := $(shell \
  python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))' \
)


.PHONY: help
help:
	@echo Available targets:
	@fgrep "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort

.PHONY: tests
tests:	check-format sanity

.PHONY: sanity
sanity:		## Run sanity tests
	# import is broken on macOS.
	ansible-test sanity --python $(python_version) --skip-test import

.PHONY: units
units:		## Run unit tests
	./fix-pytest-ini.py
	-ansible-test coverage erase # On first run, there is nothing to erase.
	ansible-test units --python $(python_version) --coverage
	ansible-test coverage html

.PHONY: integration
integration:	## Run integration tests
	$(MAKE) -C tests/integration $(CI)

.PHONY: docs
docs:		## Build collection documentation
	mkdir -p docs/source/modules
	cd docs && ansible-doc-extractor --template templates/module.rst.j2 source/modules ~/.ansible/collections/ansible_collections/paloaltonetworks/panos/plugins/modules/panos*.py
	cd docs && sphinx-build source html

.PHONY: clean
clean:		## Remove all auto-generated files
	rm -rf tests/output
	rm -rf *.tar.gz

build:		## Build collection
	ansible-galaxy collection build

format:		## Format with black, isort
	black .
	isort .

check-format:	## Check with black, isort
	black --check .
	isort --diff .
	isort --check .

sync-deps:	## Sync Pipfile.lock to requirements.txt
	pipenv lock --requirements > requirements.txt

test-release:	## Semantic release dry run
	semantic-release --dry-run --no-ci --branches=develop

old-sanity:		## Sanity tests for Ansible v2.9 and Ansible v2.10
	ansible-test sanity -v --skip-test pylint --skip-test rstcheck --python $(python_version)

new-sanity:		## Sanity tests for Ansible v2.11 and above
	ansible-test sanity -v --skip-test pylint --python $(python_version)
