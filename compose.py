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
    # @Todo: Implement this process for the local executor
    parser.add_argument('-e', '--env', action='store', type=str, default='celery', choices=['celery', 'local', 'cli'],
                        help='Set which type of container to use (local, celery, or cli), defaults to use the Celery container')
    parser.add_argument('-v', '--version', action='store', type=str, default='master',
                        choices=['master', '1.8.2', '1.9.0', '1.10.1'],
                        help='Which version to use, defaults to master')
    parser.add_argument('-t', '--tag', action='store', type=str, default='latest',
                        help="Docker tag for which image to use, defaults to 'latest'")
    parser.add_argument('-s', '--source', action='store', type=str, required=True,
                        help='Path to airflow source code')
    parser.add_argument('-d', '--down', action='store_true', default=False,
                        help='Take the containers down')
    return parser.parse_args()

def create_compose_file(args):
    compose_file = 'docker-compose.yml'
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = 'pgsql_data_' + args.tag
    if args.env == 'local':
        pass # @NotDone
    else:
        with open(os.path.join(current_dir, 'docker-compose-{}.template.yml'.format(args.env))) as template:
            read_template = template.readlines()
            format_template = ''.join(read_template).format(pgsql_data_location=data_dir, airflow_source_path=args.source, tag=args.tag)
            with open(os.path.join(current_dir, compose_file), 'w') as out:
                out.write(format_template)
    return compose_file


if __name__ == "__main__":
    args = cmd_line_parser()
    compose_file = create_compose_file(args)
    if args.down:
        subprocess.run(["docker-compose", "down"])
    else:
        if args.env == 'cli':
            subprocess.run(["docker-compose", "run", "--rm", "cli"])
        else:
            subprocess.run(["docker-compose", "up", "-d"])
    os.remove(compose_file)

