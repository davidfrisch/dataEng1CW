import sys
import os
from time import time
from flask import Flask, request
from flask_cors import CORS
from subprocess import Popen, PIPE
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import SPARK_MASTER_URL, ROOT_DIR, SPARK_LOCAL_UI_URL
from pipeline.save_fasta_from_db import create_fasta_file

app = Flask(__name__)
CORS(app, origins=['*'])

@app.route('/')
def hello_world():
  return """
    <html>
        <head>
            <title>Spark Pipeline</title>
        </head>
        <body>
            <h1>Spark Pipeline</h1>
            <div>
              POST to /launch_pipeline with file_path as path of the file to process
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    try:
        spark_info = requests.get(f'{SPARK_LOCAL_UI_URL}/json/')
        return {'flask': {'status': "ALIVE"}, 'spark': spark_info.json()}
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'spark_master_url': SPARK_MASTER_URL, 'spark': 'error'}



@app.route('/launch_pipeline', methods=['POST'])
def launch_pipeline():
    data = request.get_json()
    filepath = data['file_path'] if 'file_path' in data else None
    filename = filepath.split('/')[-1] if filepath else None
    ids = data['ids'] if 'ids' in data else None
    name = data['name'] if 'name' in data else None
    local_path = f'{ROOT_DIR}/data/{filename}'
    run_id = name + '_' + str(int(time()))

    if ids and not filename:
        local_path = f'{ROOT_DIR}/data/{run_id}.fasta'
        create_fasta_file(ids, local_path)

    if filepath is None and ids is None:
        return {'error': 'No file path provided'}, 400

    if not os.path.exists(local_path):
        return {'error': 'File not found'}, 404

    if not name:
        return {'error': 'No process name provided'}, 400

    if not local_path.endswith('.fasta'):
        return {'error': 'File is not a fasta file'}

    cmd = f'python3 pipeline_script.py -f {local_path} --master {SPARK_MASTER_URL} --run_id {run_id}'
    print(cmd)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    # run in the background
    return {'run_id': run_id, 'spark_master_url': SPARK_MASTER_URL, 'file_path': local_path}
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
