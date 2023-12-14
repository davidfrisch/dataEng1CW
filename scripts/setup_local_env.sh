DIRECTORY=$(dirname $0)

PYTHON3_PATH=/mnt/data/dataEng1CW/venv/bin/python3
HH_SUITE__BIN_PATH=/mnt/data/programs/hh-suite/bin
PDB70_PATH=/mnt/data/pdb70/pdb70
S4PRED_PATH=/mnt/data/programs/s4pred
SPARK_MASTER_URL=spark://ip-10-0-0-169.eu-west-2.compute.internal:7077
SPARK_UI_URL="http://ec2-18-130-66-138.eu-west-2.compute.amazonaws.com/spark-master"
SPARK_LOCAL_UI_URL="http://localhost:8080"
# DOCKER_SPARK_MASTER_URL=spark://spark-master:7077
DATABASE_URL="postgresql://postgres:postgres@ip-10-0-0-169.eu-west-2.compute.internal:5432/proteomics"
DOCKER_DATABASE_URL="postgresql://postgres:postgres@postgres:5432/proteomics"
SHARE_DIR="/mnt/data/dataEng1CW/data"
DOCKER_SHARE_DIR="/data"
VITE_BACKEND_URL="http://localhost:3001"
DOCKER_VITE_BACKEND_URL="http://ec2-18-130-66-138.eu-west-2.compute.amazonaws.com/api"
FLASK_URL=http://127.0.0.1:5000
DOCKER_FLASK_URL=http://10.0.0.169:5000

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

# For backend
echo "DATABASE_URL=$DOCKER_DATABASE_URL" > $DIRECTORY/../backend/.env.staging
echo "SHARE_DIR=$DOCKER_SHARE_DIR" >> $DIRECTORY/../backend/.env.staging
echo "FLASK_URL=$DOCKER_FLASK_URL" >> $DIRECTORY/../backend/.env.staging

# For frontend
echo "VITE_BACKEND_URL=$DOCKER_VITE_BACKEND_URL" > $DIRECTORY/../frontend/.env.staging
echo "VITE_SPARK_UI_URL=$SPARK_UI_URL" >> $DIRECTORY/../frontend/.env.staging
