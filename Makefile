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
  python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))' \
)


.PHONY: help
help:
	@echo Available targets:
	@fgrep "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort

.PHONY: sanity
sanity:  ## Run sanity tests
	ansible-test sanity --python $(python_version)

.PHONY: units
units:  ## Run unit tests
	./fix-pytest-ini.py
	-ansible-test coverage erase # On first run, there is nothing to erase.
	ansible-test units --python $(python_version) --coverage
	ansible-test coverage html

.PHONY: integration
integration:  ## Run integration tests
	$(MAKE) -C tests/integration $(CI)

.PHONY: docs
docs:  ## Build collection documentation
	$(MAKE) -C docs -f Makefile.custom docs

.PHONY: clean
clean:  ## Remove all auto-generated files
	$(MAKE) -C docs -f Makefile.custom clean
	rm -rf tests/output

format:
	black .
	isort .

check-format:
	black --check .
	isort --check .

sync-deps:
	pipenv lock -r > requirements.txt

default: install

install:
	rm -f paloaltonetworks*
	ansible-galaxy collection build . --force
	ansible-galaxy collection install paloaltonetworks* --force
	rm -f paloaltonetworks*

doctest:
	for i in $$(ls -1 plugins/modules | grep -v init); do \
		echo "Checking $$i..." ; \
		ansible-doc -M plugins/modules $$i > /dev/null ; \
	done

.PHONY: install doctest
