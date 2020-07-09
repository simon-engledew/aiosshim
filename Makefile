MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:

tox:
	tox

requirements.txt: requirements.in
	pip-compile --generate-hashes --output-file=$@ $<

ssh_host_key:
	ssh-keygen -m PEM -q -t ed25519 -N '' -f $@
