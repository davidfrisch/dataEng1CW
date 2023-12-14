#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

SECRET_KEY_FILE=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -s|--secret-key-file) SECRET_KEY_FILE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done


if [[ -z "$SECRET_KEY_FILE" ]]; then
    echo "ERROR: secret key file not specified!"
    exit 1
fi

if [[ ! -f "$SECRET_KEY_FILE" ]]; then
    echo "ERROR: secret key file does not exist!"
    exit 1
fi



python3_version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')

if [[ $python3_version != 3.9* ]]; then
    echo "ERROR: this script requires Python3.9!"
    exit 1
fi

if ! which pip3 >& /dev/null; then
    echo "ERROR: pip3 is not installed."
    echo "       On Ubuntu, run:"
    echo "       curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.9"
    echo "       and try running this script again."
    exit 1
fi


echo "
ssh_private_key: $SECRET_KEY_FILE
spark_user: ec2-user
spark_group: ec2-user
" > $DIRECTORY/../ansible/custom_vars.yml


# Software installation
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
pip3 install ansible

echo "Finished installing host dependencies."