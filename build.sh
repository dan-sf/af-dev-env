#!/usr/bin/env bash

# This script can be used to build the local docker image

# Usage:
# ./build.sh [tag]

# tag defaults to 'latest'

set -e

tag=$1

# Airflow needs this...
export SLUGIFY_USES_TEXT_UNIDECODE=yes

# Path to airflow source
curr_path=`dirname $0`
af_src="${curr_path}/../airflow"

[[ -d airflow ]] && rm -rf airflow
[[ $tag == "" ]] && tag="latest"

# Create the python egg file in the airflow src dir
pushd $af_src
[[ -d apache_airflow.egg-info ]] && rm -rf apache_airflow.egg-info
python setup.py develop --editable --build-directory . --no-deps --dry-run
popd

cp -R $af_src .
docker build -t af-dev:$tag .
rm -rf airflow

