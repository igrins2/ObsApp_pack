#!/bin/bash

if [[ ! -e $HOME/ObsApp ]]; then
    mkdir $HOME/ObsApp
    echo "mkdir"
elif [[ ! -d $HOME/ObsApp ]]; then
    echo $HOME + "/ObsApp already exists but is not a directory" 1>&2
fi


# configuration file
cp $HOME/ObsApp_pack/installation/ObsApp $HOME


# install python library
cd $HOME/ObsApp_pack/installation
bash Miniconda3-latest-Linux-x86_64.sh
export PATH=$HOME/miniconda3/bin:$PATH
source ~/.bash_profile

conda update conda
conda create -n ObsApp python=3.9
conda activate ObsApp

pip install numpy
pip install astropy
pip install matplotlib
pip install pyside6
pip install PyQt5
pip install pika
pip install scipy

