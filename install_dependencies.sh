#!/bin/bash

# create venv
python3 -m venv simulation

# Activate virtual environment
source simulation/bin/activate

# install required python packages
pip install -r requirements.txt
