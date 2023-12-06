from flask import Flask, request
from flask_cors import CORS
from subprocess import Popen, PIPE
import sys
import os
from time import time
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import SPARK_MASTER_URL
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

@app.route('/launch_pipeline', methods=['POST'])
def launch_pipeline():
    data = request.get_json()
    filepath = data['file_path'] if 'file_path' in data else None
    filename = filepath.split('/')[-1] if filepath else None
    local_path = f'/mnt/data/dataEng1CW/data/{filename}'
    name = data['name'] if 'name' in data else None
    run_id = name + '_' + str(int(time()))

    if filepath is None:
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
    app.run(debug=False, host='0.0.0.0', port=5000)
