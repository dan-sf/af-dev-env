#!/usr/bin/env bash

# @Note: I may need to generate an egg file here so that airflow has proper
# links when docker looks into the airflow repo @InvestigateThis

[[ -d incubator-airflow ]] && rm -rf incubator-airflow
cp -r ../../git/incubator-airflow .
docker build -t af-dev .
rm -rf incubator-airflow

