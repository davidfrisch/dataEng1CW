#!/bin/bash
set -e

DIRECTORY=$(dirname $0)

# Path in VMs
PYTHON3_PATH=/mnt/data/dataEng1CW/venv/bin/python3
HH_SUITE__BIN_PATH=/mnt/data/programs/hh-suite/bin
PDB70_PATH=/mnt/data/pdb70/pdb70
S4PRED_PATH=/mnt/data/programs/s4pred
SHARE_DIR="/mnt/data/dataEng1CW/data"
DOCKER_SHARE_DIR="/data"

# For local
SPARK_LOCAL_UI_URL="http://localhost:8080"
VITE_BACKEND_URL="http://localhost:3001"
FLASK_URL=http://127.0.0.1:5000

# USER SPECIFIC VARIABLES
HOSTNAME=""
DATABASE_NAME=proteomics
DATABASE_USER=postgres
DATABASE_PASS=postgres

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--hostname) HOSTNAME="$2"; shift ;;
        -db|--db-name) DATABASE_NAME="$2"; shift ;;
        -du|--db-user) DATABASE_USER="$2"; shift ;;
        -dp|--db-pass) DATABASE_PASS="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [[ -z "$HOSTNAME" ]]; then
    echo "ERROR: hostname not specified!, use -h or --hostname"
    exit 1
fi

echo "CLIENT HOSTNAME=$HOSTNAME"
IP_ADDRESS=$(nslookup "$HOSTNAME" | awk '/^Address: / { print $2 }')

if [[ -z "$IP_ADDRESS" ]]; then
    echo "ERROR: IP address not found in DNS!"
    exit 1
fi

SPARK_UI_URL="http://$HOSTNAME/spark-master"
DOCKER_VITE_BACKEND_URL="http://$HOSTNAME/api"
DOCKER_DATABASE_URL="postgresql://$DATABASE_USER:$DATABASE_PASS@postgres:5432/$DATABASE_NAME"
DOCKER_FLASK_URL=http://$IP_ADDRESS:5000
SPARK_MASTER_URL=spark://$IP_ADDRESS:7077
DATABASE_URL="postgresql://$DATABASE_USER:$DATABASE_PASS@$IP_ADDRESS:5432/$DATABASE_NAME"


# For pipeline
echo "PYTHON3_PATH=$PYTHON3_PATH" > $DIRECTORY/../.env
echo "HH_SUITE__BIN_PATH=$HH_SUITE__BIN_PATH" >> $DIRECTORY/../.env
echo "PDB70_PATH=$PDB70_PATH" >> $DIRECTORY/../.env
echo "S4PRED_PATH=$S4PRED_PATH" >> $DIRECTORY/../.env
echo "SHARE_DIR=$SHARE_DIR" >> $DIRECTORY/../.env
echo "DATABASE_URL=$DATABASE_URL" >> $DIRECTORY/../.env
echo "SPARK_MASTER_URL=$SPARK_MASTER_URL" >> $DIRECTORY/../.env
echo "SPARK_LOCAL_UI_URL=$SPARK_LOCAL_UI_URL" >> $DIRECTORY/../.env

# For backend
echo "DATABASE_URL=$DATABASE_URL" > $DIRECTORY/../backend/.env
echo "SHARE_DIR=$SHARE_DIR" >> $DIRECTORY/../backend/.env
echo "FLASK_URL=$FLASK_URL" >> $DIRECTORY/../backend/.env

# For frontend
echo "VITE_BACKEND_URL=$VITE_BACKEND_URL" > $DIRECTORY/../frontend/.env
echo "VITE_SPARK_UI_URL=$SPARK_UI_URL" >> $DIRECTORY/../frontend/.env


### Docker with .env.staging
# For pipeline
echo "PYTHON3_PATH=$PYTHON3_PATH" > $DIRECTORY/../.env.staging
echo "HH_SUITE__BIN_PATH=$HH_SUITE__BIN_PATH" >> $DIRECTORY/../.env.staging
echo "PDB70_PATH=$PDB70_PATH" >> $DIRECTORY/../.env.staging
echo "S4PRED_PATH=$S4PRED_PATH" >> $DIRECTORY/../.env.staging
echo "SPARK_MASTER_URL=$SPARK_MASTER_URL" >> $DIRECTORY/../.env.staging
echo "SHARE_DIR=$DOCKER_SHARE_DIR" >> $DIRECTORY/../.env.staging

# For database
echo "POSTGRES_USER=$DATABASE_USER" > $DIRECTORY/../.env-database
echo "POSTGRES_PASSWORD=$DATABASE_PASS" >> $DIRECTORY/../.env-database
echo "POSTGRES_DB=$DATABASE_NAME" >> $DIRECTORY/../.env-database

# For backend
echo "DATABASE_URL=$DOCKER_DATABASE_URL" > $DIRECTORY/../backend/.env.staging
echo "SHARE_DIR=$DOCKER_SHARE_DIR" >> $DIRECTORY/../backend/.env.staging
echo "FLASK_URL=$DOCKER_FLASK_URL" >> $DIRECTORY/../backend/.env.staging

# For frontend
echo "VITE_BACKEND_URL=$DOCKER_VITE_BACKEND_URL" > $DIRECTORY/../frontend/.env.staging
echo "VITE_SPARK_UI_URL=$SPARK_UI_URL" >> $DIRECTORY/../frontend/.env.staging



echo "Finished setting up local environment variables."