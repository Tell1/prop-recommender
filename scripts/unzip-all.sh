#!/bin/bash

# Example:
# ./script.sh ./data/raw_00/valuergeneral/2022

# This script unzips all .zip files in a directory, and extracts them to a
# subdirectory with the same name.

DIR=$1

for zip in $DIR/*.zip; do
	dirname=$(basename "$zip" .zip)
	echo "Unzipping $zip to $dirname"
	mkdir -p "$dirname"
	unzip "$zip" -d "$dirname"
done
