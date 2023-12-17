#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

ansible-playbook $DIRECTORY/../ansible/start_all.yml -i $DIRECTORY/../ansible/inventory.ini 