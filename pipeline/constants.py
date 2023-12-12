import os
import sys
from dotenv import load_dotenv
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))+ "/.."
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(f"/mnt/data/dataEng1CW/.env")
load_dotenv(f"{ROOT_DIR}/.env")

NUM_WORKERS_DEFAULT = 5
PYTHON3_PATH = os.getenv('PYTHON3_PATH')
HH_SUITE__BIN_PATH = os.getenv('HH_SUITE__BIN_PATH')
PDB70_PATH = os.getenv('PDB70_PATH')
S4PRED_PATH = os.getenv('S4PRED_PATH')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
SPARK_MASTER_URL = os.getenv('SPARK_MASTER_URL')
DATABASE_URL = os.getenv('DATABASE_URL')

if not SPARK_MASTER_URL:
    print("Please set the SPARK_MASTER_URL in the .env file")
    sys.exit(1)

if not HH_SUITE__BIN_PATH:
    print("Please set the HH_SUITE__BIN_PATH in the .env file")
    sys.exit(1)

if not PDB70_PATH:
    print("Please set the PDB70_PATH in the .env file")
    sys.exit(1)

if not S4PRED_PATH:
    print("Please set the S4PRED_PATH in the .env file")
    sys.exit(1)

if not PYTHON3_PATH:
    print("Please set the PYTHON3_PATH in the .env file")
    sys.exit(1)

if not BUCKET_NAME:
    print("Please set the BUCKET_NAME in the .env file")
    sys.exit(1)

if not DATABASE_URL:
    print("Please set the DATABASE_URL in the .env file")
    sys.exit(1)

os.environ['PYSPARK_DRIVER_PYTHON'] = PYTHON3_PATH
os.environ['PYSPARK_PYTHON'] = PYTHON3_PATH
