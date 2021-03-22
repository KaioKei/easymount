#!/usr/bin/env bash

CURRENT_PATH="$(realpath "$0")"
CURRENT_DIR="$(dirname "${CURRENT_PATH}")"
ln -s "${CURRENT_DIR}/easymount/easymount.py" /usr/local/bin/easymount