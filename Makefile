MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:

tox:
	tox

requirements.txt: requirements.in
	CUSTOM_COMPILE_COMMAND="make requirements.txt" pip-compile --generate-hashes --output-file=- $< | sed '\%^file://$(abspath .)  # via -r requirements.in$$%d' > $@

ssh_host_key:
	ssh-keygen -m PEM -q -t ed25519 -N '' -f $@
