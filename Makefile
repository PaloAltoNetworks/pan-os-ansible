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
