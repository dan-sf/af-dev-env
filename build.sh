#!/usr/bin/env bash

set -e

# Path to airflow source
AF_SRC='../incubator-airflow'

[[ -d incubator-airflow ]] && rm -rf incubator-airflow

# Create the python egg file in the airflow src dir
pushd $AF_SRC
[[ -d apache_airflow.egg-info ]] && rm -rf apache_airflow.egg-info
python setup.py develop --editable --build-directory . --no-deps --dry-run
popd

cp -R ../../git/incubator-airflow .
docker build -t af-dev .
rm -rf incubator-airflow

