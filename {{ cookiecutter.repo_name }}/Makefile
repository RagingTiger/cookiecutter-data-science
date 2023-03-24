.PHONY: all convert execute resetnb delout clean jupyter

# Usage:
# make         # execute and convert all Jupyter notebooks
# make convert # only convert Jupyter notebooks
# make execute # only execute Jupyter notebooks
# make resetnb # only clear Jupyter notebook outputs
# make delout  # only remove converted files
# make clean   # combine resetnb and remove converted files
# make jupyter # startup docker container running Jupyter server

################################################################################
# GLOBALS                                                                      #
################################################################################

# make cli args
OFRMT := html
THEME := dark
TMPLT := lab
OUTDR := converted
INTDR := notebooks
DCTNR := $(notdir $(PWD))

# extensions available
OEXT_html     = html
OEXT_latex    = tex
OEXT_pdf      = pdf
OEXT_webpdf   = pdf
OEXT_markdown = md
OEXT_rst      = rst
OEXT_script   = py
OEXT_notebook = ipynb
OEXT = ${OEXT_${OFRMT}}

# individual conversion flag variables
OUTFL = --to ${OFRMT}
THMFL = --theme ${THEME}
TMPFL = --template ${TMPLT}
ODRFL = --output-dir ${OUTDR}
RMTGS = --TagRemovePreprocessor.enabled=True
RMCEL = --TagRemovePreprocessor.remove_cell_tags remove_cell
RMNPT = --TagRemovePreprocessor.remove_input_tags remove_input
RMIPT = --TemplateExporter.exclude_input_prompt=True
RMOPT = --TemplateExporter.exclude_output_prompt=True
RMWSP = --RegexRemovePreprocessor.patterns '\s*\Z'

# check for conditional vars
ifdef NOTMPLT
  undefine TMPFL
endif
ifdef NOTHEME
  undefine THMFL
endif

# combined conversion flag variables
TMPFLGS = ${OUTFL} ${THMFL} ${TMPFL} ${ODRFL}
RMVFLGS = ${RMTGS} ${RMCEL} ${RMNPT} ${RMIPT} ${RMOPT} ${RMWSP}

# final conversion flag variable
CNVRSNFLGS = ${TMPFLGS} ${RMVFLGS}

# notebook-related variables
CURRENTDIR := $(PWD)
NOTEBOOKS  := $(wildcard **/*.ipynb)
CONVERTNB  := $(addprefix ${OUTDR}/, $(notdir $(NOTEBOOKS:%.ipynb=%.${OEXT})))

# docker-related variables
DCKRIMG = ghcr.io/ragingtiger/omega-notebook:master
DCKRRUN = docker run --rm -v ${CURRENTDIR}:/home/jovyan -it ${DCKRIMG}

# check for conditional vars to turn off docker
ifdef NODOCKER
  undefine DCKRRUN
endif

# jupyter nbconvert vars
NBEXEC = jupyter nbconvert --to notebook --execute --inplace
NBCNVR = jupyter nbconvert ${CNVRSNFLGS}
NBCLER = jupyter nbconvert --clear-output --inplace

################################################################################
# COMMANDS                                                                     #
################################################################################

# default
all: ${CONVERTNB}

# rule for executing single notebooks before converting
%.ipynb:
	@ echo "Executing ${INTDR}/$@ in place."
	@ ${DCKRRUN} ${NBEXEC} ${INTDR}/$@

# rule for converting single notebooks to HTML
${OUTDR}/%.${OEXT}: %.ipynb
	@ echo "Converting ${INTDR}/$< to ${OFRMT}"
	@ ${DCKRRUN} ${NBCNVR} ${INTDR}/$<

# convert all notebooks to HTML
convert:
	@ ${DCKRRUN} ${NBCNVR} ${NOTEBOOKS}

# execute all notebooks and store output inplace
execute:
	@ ${DCKRRUN} ${NBEXEC} ${NOTEBOOKS}

# remove output from executed notebooks
resetnb:
	@ ${DCKRRUN} ${NBCLER} ${NOTEBOOKS}

# delete all converted files
delout:
	@ if [ -d "${CURRENTDIR}/${OUTDR}" ]; then \
	  rm -rf "${CURRENTDIR}/${OUTDR}"; \
	fi

# cleanup everything
clean: delout resetnb

# launch jupyter notebook development Docker image
jupyter:
	docker run -d \
	           --rm \
	           --name ${DCTNR} \
	           -e JUPYTER_ENABLE_LAB=yes \
	           -p 8888 \
	           -v ${CURRENTDIR}:/home/jovyan \
	           ${DCKRIMG} && \
	sleep 5 && \
	  docker logs ${DCTNR} 2>&1 | \
	    grep "http://127.0.0.1" | tail -n 1 | \
	    sed "s/:8888/:$$(docker port ${DCTNR} | \
	    grep '0.0.0.0:' | awk '{print $$3'} | sed 's/0.0.0.0://g')/g"
