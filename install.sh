#!/bin/sh

name="sous-chef"

# build
pyinstaller entrypoint.py --name $name --onefile --clean

# install
sudo cp dist/$name /usr/local/bin

#clean up
rm -R build
rm -R dist
rm $name.spec