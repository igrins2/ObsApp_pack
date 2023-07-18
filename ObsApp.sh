#!/bin/bash
docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=:0 registry.gitlab.com/nsf-noirlab/gemini/rtsw/iocs/obsapp/obsapp-deploy bash -c "cd /ObsApp_pack/ && ./run_ObsApp.sh simul"
