#!/bin/bash

# remove binary and create dummy file
echo -----------------------------------------------------------
files_to_exclude="
tdmelodic/nn/resource/net_it_2500000
"

for f in $files_to_exclude;
do
    echo replace $f with an empty file
    if [ -e $f ]; then
	mv $f ${f}_bak
    fi
    touch $f
done

# remove old files
echo -----------------------------------------------------------
echo removing obosolete files
rm -rf dist/*
rm -rf tdmelodic.egg-info*

# sdist
echo -----------------------------------------------------------
python3 setup.py sdist bdist_wheel

# back
echo -----------------------------------------------------------
for f in $files_to_exclude;
do
    echo moving ${f}_bak back to $f
    mv ${f}_bak ${f}
done

# done
echo -----------------------------------------------------------
echo Done.