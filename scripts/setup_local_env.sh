DIRECTORY=$(dirname $0)

PYTHON3_PATH=/mnt/data/dataEng1CW/venv/bin/python3
HH_SUITE__BIN_PATH=/mnt/data/programs/hh-suite/bin
PDB70_PATH=/mnt/data/pdb70/pdb70
S4PRED_PATH=/mnt/data/programs/s4pred
S3_BUCKET_NAME=comp0235-ucabfri
SPARK_MASTER_URL=spark://ip-10-0-0-169.eu-west-2.compute.internal:7077
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/proteomics?schema=public"
SHARE_DIR="/mnt/data/dataEng1CW/data"
VITE_BACKEND_URL="http://localhost:3001"
FLASK_URL=http://127.0.0.1:5000

# For pipeline
echo "PYTHON3_PATH=$PYTHON3_PATH" > $DIRECTORY/../.env
echo "HH_SUITE__BIN_PATH=$HH_SUITE__BIN_PATH" >> $DIRECTORY/../.env
echo "PDB70_PATH=$PDB70_PATH" >> $DIRECTORY/../.env
echo "S4PRED_PATH=$S4PRED_PATH" >> $DIRECTORY/../.env
echo "S3_BUCKET_NAME=$S3_BUCKET_NAME" >> $DIRECTORY/../.env
echo "SPARK_MASTER_URL=$SPARK_MASTER_URL" >> $DIRECTORY/../.env
echo "SHARE_DIR=$SHARE_DIR" >> $DIRECTORY/../.env

# For backend
echo "DATABASE_URL=$DATABASE_URL" > $DIRECTORY/../backend/.env
echo "SHARE_DIR=$SHARE_DIR" >> $DIRECTORY/../backend/.env
echo "FLASK_URL=$FLASK_URL" >> $DIRECTORY/../backend/.env

# For frontend
echo "VITE_BACKEND_URL=$VITE_BACKEND_URL" > $DIRECTORY/../frontend/.env