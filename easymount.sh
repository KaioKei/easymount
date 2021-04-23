#!/usr/bin/env bash

# === CONSTANTS ===
TIME=$(date +%s)
EASYMOUNT_SHELL_SCRIPT="$(realpath "$0")"
EASYMOUNT_ROOT_DIR="$(dirname "${EASYMOUNT_SHELL_SCRIPT}")"

mode=""
conf_file=""
output_path=""
verbose="False"

# === FUNCTIONS ===

function usage(){
    printf "Usage:

    [command]
    easymount [mode] [options]

    [mode]
    mount\tMount the VMs from the given configuration file
    configure\tOnly Generate the vagrant file from the given configuration file, for debug purposes

    [other modes]
    start\tStart the VMs from the last generated vagrant file, and reload the vms if needed
    stop\tStop the VMs mounted from the last generated vagrant file using 'vagrant halt'
    status\tPrint the status of the VMs mounted from the last generated vagrant file using 'vagrant status'
    delete\tDelete the VMs mounted from the last generated vagrant file using 'vagrant destroy -f'
    reload\tStart and reload provisions of the VMs mounted from the last generated vagrant file using 'vagrant reload'
    reset\tDelete and mount again the VMs from the last generated vagrant file

    [options]
    -c | --conf [file]\tConfiguration file for the VMs to mount
    -o | --output [path]\tExport the current generated vagrant file into the given path

    [examples]
    # Create Vagrant file and start VMs :
    easymount mount -c simple_conf_example.yaml

    # Create Vagrant file and export output :
    easymount configure -c simple_conf_example.yaml -o /tmp
    "
}

# check if configuration is provided
function check_conf_option() {
    if [ "${conf_file}" == "" ]; then
        echo "! FATAL: Missing -c|--conf option"
        usage
        exit 1
    fi
}

function configure_vagrant() {
    echo "Configure vagrant"
    python_cmd="python ${EASYMOUNT_PYTHON_SCRIPT} -c ${conf_file}"
    # output template
    if [ -n "${output_path}" ]; then
        python_cmd+=" -o ${output_path}"
    fi
    # verbosity
    if [ "${verbose}" == "True" ]; then
        python_cmd+=" -v"
    fi

    # execute vagrant configuration for template
    eval "${python_cmd}"
}

function start_vagrant() {
    echo "Mount the virtual machines"
    cd "${EASYMOUNT_VAGRANT_DIR}" || exit
    vagrant up
}

function stop_vagrant() {
    echo "Stop the virtual machines"
    cd "${EASYMOUNT_VAGRANT_DIR}" || exit
    vagrant halt
}

function status_vagrant() {
    cd "${EASYMOUNT_VAGRANT_DIR}" || exit
    vagrant status
}

function destroy_vagrant() {
    echo "Delete the virtual machines"
    cd "${EASYMOUNT_VAGRANT_DIR}" || exit
    vagrant destroy -f
}

function reload_vagrant() {
    echo "Reload the virtual machines"
    cd "${EASYMOUNT_VAGRANT_DIR}" || exit
    vagrant reload
}

# === PARSING ===

POSITIONAL=()
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
    -h|--help|help)
        usage
        exit 0
        ;;
    mount)
        mode="mount"
        shift
        ;;
    configure)
        mode="configure"
        shift
        ;;

    start)
        mode="start"
        shift
        ;;
    stop)
        mode="stop"
        shift
        ;;
    status)
        mode="status"
        shift
        ;;
    delete)
        mode="destroy"
        shift
        ;;
    reload)
        mode="reload"
        shift
        ;;
    reset)
        mode="reset"
        shift
        ;;

    up)
        echo "! ERROR: Did you mean 'easymount start' ?"
        exit 0
        ;;
    destroy)
        echo "! ERROR: Did you mean 'easymount delete' ?"
        exit 0
        ;;
    halt)
        echo "! ERROR: Did you mean 'easymount stop' ?"
        exit 0
        ;;

    -c|--conf)
        conf_file="$2"
        shift 2
        ;;
    -o|--output)
        output_path="$2"
        shift 2
        ;;
    -v|--verbose)
        verbose="True"
        shift
        ;;
    *) # unknown option
        POSITIONAL+=("$1") # save it in an array for later
        usage
        exit 1
        shift              # past argument
        ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

# === MAIN ===

# environment
if [ ! -f "${EASYMOUNT_ROOT_DIR}/.env" ];then
    echo "! FATAL: execute ./install.sh"
    exit 1
fi
# shellcheck source=src/util.sh
source "${EASYMOUNT_ROOT_DIR}/.env"

# modes
if [ "${mode}" == "mount" ]; then
    check_conf_option
    configure_vagrant
    start_vagrant
    echo ""
    echo "Copy in your /etc/hosts:"
    cat "${EASYMOUNT_ROOT_DIR}/.hosts"
elif [ "${mode}" == "configure" ]; then
    check_conf_option
    configure_vagrant
elif [ "${mode}" == "start" ]; then
    start_vagrant
elif [ "${mode}" == "stop" ]; then
    stop_vagrant
elif [ "${mode}" == "status" ]; then
    status_vagrant
elif [ "${mode}" == "destroy" ]; then
    destroy_vagrant
elif [ "${mode}" == "reload" ]; then
    reload_vagrant
elif [ "${mode}" == "reset" ]; then
    destroy_vagrant
    start_vagrant
fi

if [ $? == 0 ];then
  echo "OK"
fi
exit $?