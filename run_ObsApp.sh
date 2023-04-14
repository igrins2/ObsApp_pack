#!/bin/bash

PYTHONBIN=$HOME/miniconda3/envs/ObsApp/bin/python

source ~/.bash_profile
conda activate ObsApp

cd code/ObsApp

case "$1" in

        obs)
	    ($PYTHONBIN ObsApp_gui.py False)
            ;;
         
        simul)
	    ($PYTHONBIN ObsApp_gui.py True)
            ;;

        *)
            echo $"Usage: $0 {obs|simul}"
            exit 1
esac
