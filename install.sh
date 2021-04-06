#!/usr/bin/env bash

CURRENT_PATH="$(realpath "$0")"
CURRENT_DIR="$(dirname "${CURRENT_PATH}")"
ENV_FILE="${CURRENT_DIR}/.env"

# install env
echo ". Create user environment"
cp "${ENV_FILE}.bak" "${ENV_FILE}"
sed -i -e "s+{{EASYMOUNT_ROOT_DIR}}+${CURRENT_DIR}+g" "${ENV_FILE}"

# install easymount
easymount_cmd="/usr/local/bin/easymount"
if [ ! -f "${easymount_cmd}" ]; then
  echo ". Install easymount"
  sudo ln -s "${CURRENT_DIR}/easymount.sh" "${easymount_cmd}"
fi

echo ". Done"
exit 0