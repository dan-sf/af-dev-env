#!/usr/bin/env bash

executor=$1
docker-compose -f docker-compose-${executor}.yml down
