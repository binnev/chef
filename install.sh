#!/bin/sh

name="chef"

# build
pyinstaller entrypoint.py --name $name --onefile --clean

# install
cp dist/$name ~/.local/bin

#clean up
rm -R build
rm -R dist
rm $name.spec