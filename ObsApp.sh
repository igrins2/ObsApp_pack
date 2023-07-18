#!/bin/bash
docker run -it --rm -e DISPLAY=host.docker.internal:0 f78ea60535a9 bash -c "cd /ObsApp_pack/ && ./run_ObsApp.sh simul"
