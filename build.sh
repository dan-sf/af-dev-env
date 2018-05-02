#!/usr/bin/env bash

set -e

# @Note: I may need to generate an egg file here so that airflow has proper
# links when docker looks into the airflow repo @InvestigateThis

[[ -d incubator-airflow ]] && rm -rf incubator-airflow

# # Is this needed? Is there a better way to do this??
# pushd ../../git/incubator-airflow
# python setup.py bdist_egg # This creates the egg file that links the source paths (research this more)
# popd

cp -r ../../git/incubator-airflow .
docker build -t af-dev .
rm -rf incubator-airflow

