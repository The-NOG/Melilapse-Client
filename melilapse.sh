#!/bin/bash

dir="/var/python/Melilapse-Client/"
cd $dir
venv="${dir}venv/bin/activate"
python melilapse-client.py
deactivate