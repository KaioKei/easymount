#!/usr/bin/env python3

import argparse
import logging
import yaml
from jinja2 import Environment, FileSystemLoader
import pathlib

TEMPLATES_DIR = f"{pathlib.Path().absolute()}/easymount/templates"
RENDERS_DIR = f"{pathlib.Path().absolute()}/easymount/.renders"
VAGRANT_TEMPLATE = 'Vagrantfile.j2'
# VAGRANT_TEMPLATE = 'test.j2'
VAGRANT_FILE = f"{RENDERS_DIR}/Vagrantfile"


def load_configuration(configuration: str):
    with open(configuration, 'r') as f:
        logging.debug(f"msg: load configuration file, file: {configuration}")
        return yaml.safe_load(f)


def render_template(yaml_conf):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(VAGRANT_TEMPLATE)
    logging.debug(f"msg: render vagrant file template, file:{TEMPLATES_DIR}/{VAGRANT_TEMPLATE}")
    return template.render(yaml_conf)


def write_vagrant_file(template_rendering):
    pathlib.Path(RENDERS_DIR).mkdir(parents=True, exist_ok=True)
    logging.debug(f"msg: write vagrant file, file:{RENDERS_DIR}/{VAGRANT_FILE}")
    with open(VAGRANT_FILE, 'w') as f:
        f.write(template_rendering)


if __name__ == "__main__":
    description: str = "easymount"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--conf', dest='configuration', action='store', required=True,
                        help='Platform configuration file. Check "conf_example.yaml"')
    args = parser.parse_args()

    yaml_configuration = load_configuration(args.configuration)
    vagrant_file_render = render_template(yaml_configuration)
    write_vagrant_file(vagrant_file_render)

