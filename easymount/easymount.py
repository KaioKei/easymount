#!/usr/bin/env python3

import os
import sys
import argparse
import logging
from logging import Logger
import shutil

import yaml
from jinja2 import Environment, FileSystemLoader
import pathlib

# filenames
VAGRANT_TEMPLATE_NAME = "Vagrantfile.j2"
VAGRANT_FILE_NAME = "Vagrantfile"

# env keys
ENV_TEMPLATES_DIR_KEY = "EASYMOUNT_TEMPLATES_DIR"
ENV_VAGRANT_DIR_KEY = "EASYMOUNT_VAGRANT_DIR"

# global env variables
g_templates_dir: str
g_vagrant_template: str
g_vagrant_dir: str
g_vagrant_file= str

# logger
g_logger: Logger


def init_logger(debug: bool):
    global g_logger
    g_logger = logging.getLogger()

    # verbosity
    level = logging.DEBUG if debug else logging.INFO
    g_logger.setLevel(level)

    output_file_handler = logging.FileHandler("/tmp/easymount/output.log")
    stdout_handler = logging.StreamHandler(sys.stdout)
    g_logger.addHandler(output_file_handler)
    g_logger.addHandler(stdout_handler)


def load_environment():
    logging.debug(f"msg=load the user's environment")
    global g_templates_dir
    global g_vagrant_dir
    g_templates_dir = os.getenv(ENV_TEMPLATES_DIR_KEY)
    g_vagrant_dir = os.getenv(ENV_VAGRANT_DIR_KEY)

    # check environment
    if g_templates_dir is None or g_vagrant_dir is None:
        logging.error("msg=missing environment, execute 'install.sh'")
        sys.exit(1)
    else:
        global g_vagrant_template
        global g_vagrant_file
        g_vagrant_template = f"{g_templates_dir}/{VAGRANT_TEMPLATE_NAME}"
        g_vagrant_file = f"{g_vagrant_dir}/{VAGRANT_FILE_NAME}"


def load_configuration(configuration: str):
    with open(configuration, 'r') as f:
        logging.debug(f"msg=load configuration file;file={configuration}")
        return yaml.safe_load(f)


def render_template(yaml_conf):
    logging.debug(f"msg=render vagrant file template;file={g_vagrant_file}")
    env = Environment(loader=FileSystemLoader(g_templates_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(VAGRANT_TEMPLATE_NAME)
    return template.render(yaml_conf)


def write_vagrant_file(template_rendering):
    pathlib.Path(g_vagrant_dir).mkdir(parents=True, exist_ok=True)
    logging.debug(f"msg=write vagrant file;file={g_vagrant_file}")
    with open(g_vagrant_file, "w") as f:
        f.write(template_rendering)


def copy_vagrant_file(output_path: str):
    shutil.copy(g_vagrant_file, output_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', dest='configuration', action='store', required=True,
                        help='Platform configuration file. Check "conf_example.yaml"')
    parser.add_argument('-o', '--output', dest='output', action='store',
                        help='Path to copy the rendered vagrant file')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Path to copy the rendered vagrant file')
    args = parser.parse_args()

    init_logger(args.verbose)
    load_environment()

    yaml_configuration = load_configuration(args.configuration)
    vagrant_file_render = render_template(yaml_configuration)
    write_vagrant_file(vagrant_file_render)

    if args.output is not None:
        copy_vagrant_file(str(args.output))


