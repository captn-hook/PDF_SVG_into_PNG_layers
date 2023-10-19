#!/bin/bash

# recursively scours all svgs in a directory and subdirs and saves them as [name]-scoured.svg, using scour -i in.svg -o out.svg
echo "scouring svgs in $1"

# for all files in directory
for f in "$1"/*
do
    # if it is a directory, and not the current directory, scour it
    if [ -d "$f" ] && [ "$f" != "$1/." ]
    then
        echo "scouring $f"
        "$0" "$f" "$0"
    fi
    # if it is a .svg, scour it
    if [ "${f: -4}" == ".svg" ]
    then
        echo "scouring $f"
        scour -i "$f" -o "${f%.*}-scoured.svg"
    fi
done