#!/bin/bash
# Install only works on debian based systems
apt install python3.10-venv

# Create a vitrual environment
python3.10 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install package requirements
pip install -r requirements.txt

# Exit virtual environment
deactivate