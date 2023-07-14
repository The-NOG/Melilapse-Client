#!/bin/bash

dir="/var/python/Melilapse-Client/"
cd $dir
venv="${dir}venv/bin/activate"
source $venv
python melilapse-client.py