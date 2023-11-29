import os
import sys
from dotenv import load_dotenv
load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))+ "/../"
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

PYTHON3_PATH = os.getenv('PYTHON3_PATH')
HH_SUITE__BIN_PATH = os.getenv('HH_SUITE__BIN_PATH')
PDB70_PATH = os.getenv('PDB70_PATH')
S4PRED_PATH = os.getenv('S4PRED_PATH')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
SPARK_MASTER_URL = os.getenv('SPARK_MASTER_URL')

if not (HH_SUITE__BIN_PATH and PDB70_PATH and S4PRED_PATH and PYTHON3_PATH and BUCKET_NAME):
    print("Please set the paths for S3_BUCKET_NAME, PYTHON3_PATH, HH_SUITE__BIN_PATH, PDB70_PATH and S4PRED_PATH in the .env file")
    sys.exit(1)

os.environ['PYSPARK_DRIVER_PYTHON'] = PYTHON3_PATH
os.environ['PYSPARK_PYTHON'] = PYTHON3_PATH
