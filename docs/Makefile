# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
#SPHINXBUILD   ?= sphinx-build
PYTHON_VERSION=$(shell python -c "import sys;v=str(sys.version_info[0]);sys.stdout.write(v)")
SPHINXBUILD ?= $(if $(ifeq $(PYTHON_VERSION), 3),sphinx-build,python3 -msphinx)
SOURCEDIR     = .
BUILDDIR      = _build


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@echo Python version is \"$(PYTHON_VERSION)\"
	@echo Sphinx build command is \"$(SPHINXBUILD)\"
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

jahtml:
	make -e SPHINXOPTS="-D language='ja'" html

jalatex:
	make -e SPHINXOPTS="-D language='ja'" latexpdf

translation:
	make gettext
	sphinx-intl update -d locale -l ja
