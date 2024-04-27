#!/bin/sh
# install locally in venv for testing purposes

# build
pip install .

#clean up
rm -R build
rm -R yes_chef.egg-info