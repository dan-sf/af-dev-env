#!/usr/bin/env bash

set -e

version=$1

# Path to airflow source
AF_SRC_MASTER='../incubator-airflow'
AF_SRC_190='../airflow_versions/1.9.0/incubator-airflow'
AF_SRC_182='../airflow_versions/1.8.2/incubator-airflow'

[[ -d incubator-airflow ]] && rm -rf incubator-airflow

if [[ $version == '1.9.0' ]]
then
    AF_SRC=$AF_SRC_190
    TAG=${version}
elif [[ $version == '1.8.2' ]]
then
    AF_SRC=$AF_SRC_182
    TAG=${version}
else
    AF_SRC=$AF_SRC_MASTER
    TAG='master'
fi

# Create the python egg file in the airflow src dir
pushd $AF_SRC
[[ -d apache_airflow.egg-info ]] && rm -rf apache_airflow.egg-info
python setup.py develop --editable --build-directory . --no-deps --dry-run
popd

cp -R $AF_SRC .
docker build -t af-dev:$TAG .
rm -rf incubator-airflow

