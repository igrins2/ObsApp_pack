#!/bin/bash
docker run -it --rm -e DISPLAY=:0 registry.gitlab.com/nsf-noirlab/gemini/rtsw/iocs/obsapp/obsapp-deploy bash -c "cd /ObsApp_pack/ && ./run_ObsApp.sh simul"
