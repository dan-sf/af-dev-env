#!/usr/bin/env bash

curr_path=`dirname $0`
${curr_path}/compose.py -d -s ${curr_path}/../airflow
