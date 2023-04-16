.PHONY: all jupyter pause address containers stop-containers restart-containers

# Usage:
# make                    # just alias to containers command
# make jupyter            # startup Docker container running Jupyter server
# make pause              # pause PSECS (to pause between commands)
# make address            # get Docker container address/port
# make containers         # launch all Docker containers
# make stop-containers    # simply stops all running Docker containers
# make restart-containers # restart all containers

################################################################################
# GLOBALS                                                                      #
################################################################################

# make cli args
DCTNR := $(notdir $(PWD))
PSECS := 5

# notebook-related variables
CURRENTDIR := $(PWD)

# docker-related variables
JPTCTNR = jupyter.${DCTNR}
DCKRIMG = ghcr.io/ragingtiger/omega-notebook:master
DCKRRUN = docker run --rm -v ${CURRENTDIR}:/home/jovyan -it ${DCKRIMG}

################################################################################
# COMMANDS                                                                     #
################################################################################

# launch jupyter
all: containers

# launch jupyter notebook development Docker image
jupyter:
	@ echo "Launching Jupyter in Docker container -> ${JPTCTNR} ..."
	@ docker run -d \
	           --rm \
	           --name ${JPTCTNR} \
	           -e PYTHONPATH=/home/jovyan/src \
	           -e JUPYTER_ENABLE_LAB=yes \
	           -p 8888 \
	           -v "${CURRENTDIR}":/home/jovyan \
	           ${DCKRIMG} && \
	echo "${JPTCTNR}" >> .running_containers

# simply wait for a certain amount of time
pause:
	@ echo "Sleeping ${PSECS} seconds ..."
	@ sleep ${PSECS}

# get containerized server address
address:
	@ if [ -f "${CURRENTDIR}/.running_containers" ]; then \
	while read container; do \
	  if echo "$${container}" | grep -q "${JPTCTNR}" ; then \
	    echo "Server address: $$(docker logs $${container} 2>&1 | \
	          grep http://127.0.0.1 | tail -n 1 | \
	          sed s/:8888/:$$(docker port $${container} | \
	          grep '0.0.0.0:' | awk '{print $$3}' | sed 's/0.0.0.0://g')/g | \
	          tr -d '[:blank:]')"; \
	  else \
	    echo "Could not find running container: $${container}." \
	         "Try running: make address" \
	         "DCTNR=$$(echo $${container} | sed 's/jupyter\.//g')"; \
	  fi \
	done < "${CURRENTDIR}/.running_containers"; \
	else \
	  echo ".running_containers file not found. Is a Docker container running?"; \
	fi

# launch all docker containers
containers: jupyter pause address

# stop all containers
stop-containers:
	@ if [ -f "${CURRENTDIR}/.running_containers" ]; then \
	  echo "Stopping Docker containers ..."; \
	  while read container; do \
	    echo "Container $$(docker stop $$container) stopped."; \
	  done < "${CURRENTDIR}/.running_containers"; \
	  rm -f "${CURRENTDIR}/.running_containers"; \
	else \
	  echo "${CURRENTDIR}/.running_containers file not found."; \
	fi

# restart all containers
restart-containers: stop-containers containers
