#!/usr/bin/env python3

import argparse
import logging
import yaml
from jinja2 import Environment, FileSystemLoader
import pathlib

TEMPLATES_DIR = f"{pathlib.Path().absolute()}/easymount/templates"
VAGRANT_TEMPLATE = 'Vagrantfile.j2'
# VAGRANT_TEMPLATE = 'test.j2'


def load_configuration(configuration: str):
    with open(configuration, 'r') as f:
        logging.debug(f"msg: load configuration file, file: {configuration}")
        return yaml.safe_load(f)


def render_template(yaml_conf):
    print(TEMPLATES_DIR)
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(VAGRANT_TEMPLATE)
    logging.debug(f"msg: render vagrant file template, file:{TEMPLATES_DIR}/{VAGRANT_TEMPLATE}")
    print(template.render(yaml_conf))


if __name__ == "__main__":
    description: str = "easymount"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--conf', dest='configuration', action='store', required=True,
                        help='Platform configuration file. Check "conf_example.yaml"')
    args = parser.parse_args()

    yaml_configuration = load_configuration(args.configuration)
    render_template(yaml_configuration)

