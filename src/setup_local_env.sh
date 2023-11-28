
PYTHON3_PATH=/mnt/data/dataEng1CW/venv/bin/python3
HH_SUITE__BIN_PATH=/mnt/data/programs/hh-suite/bin
PDB70_PATH=/mnt/data/pdb70/pdb70
S4PRED_PATH=/mnt/data/programs/s4pred
S3_BUCKET_NAME=comp0235-ucabfri
SPARK_MASTER_URL=spark://ip-10-0-13-106.eu-west-2.compute.internal:7077

echo "PYTHON3_PATH=$PYTHON3_PATH" > .env
echo "HH_SUITE__BIN_PATH=$HH_SUITE__BIN_PATH" >> .env
echo "PDB70_PATH=$PDB70_PATH" >> .env
echo "S4PRED_PATH=$S4PRED_PATH" >> .env
echo "S3_BUCKET_NAME=$S3_BUCKET_NAME" >> .env
echo "SPARK_MASTER_URL=$SPARK_MASTER_URL" >> .env