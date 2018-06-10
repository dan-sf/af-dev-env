#!/usr/bin/env python

import os
import sys
import argparse
import subprocess


def cmd_line_parser():
    """
    Parse cmd line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--local', action='store_true', default=False, # @Todo: Implement this process for the local executor
                        help='Use the local container, defaults to use the Celery container')
    parser.add_argument('-v', '--version', action='store', type=str, default='master',
                        choices=['master', '1.8.2', '1.9.0'],
                        help='Which version to use, defaults to master')
    parser.add_argument('-d', '--down', action='store_true', default=False,
                        help='Take the container down')
    return parser.parse_args()

def create_compose_file(args):
    compose_file = 'docker-compose.yml'
    current_dir = os.path.dirname(os.path.realpath(__file__))
    if args.local:
        pass
    else:
        with open(os.path.join(current_dir, 'docker-compose-celery.template.yml')) as template:
            data_dir = 'data_' + args.version.replace('.', '') if args.version != 'master' else 'data'
            af_path = '../airflow_versions/{}/incubator-airflow'.format(args.version) if args.version != 'master' else '../incubator-airflow'
            read_template = template.readlines()
            format_template = ''.join(read_template).format(pgsql_data_location=data_dir, airflow_source_path=af_path, version=args.version)
            with open(os.path.join(current_dir, compose_file), 'w') as out:
                out.write(format_template)
    return compose_file


if __name__ == "__main__":
    args = cmd_line_parser()
    compose_file = create_compose_file(args)
    if args.down:
        subprocess.run(["docker-compose", "down"])
    else:
        subprocess.run(["docker-compose", "up", "-d"])
    os.remove(compose_file)

