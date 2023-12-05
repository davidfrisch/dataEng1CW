from flask import Flask, request
from subprocess import Popen, PIPE
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import SPARK_MASTER_URL
app = Flask(__name__)

@app.route('/')
def hello_world():
    # give a nice welcome message
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
    filepath = request.form['file_path']
    cmd = f'python3 pipeline_script.py -f {filepath} --master {SPARK_MASTER_URL}'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    # run in the background
    return 'Pipeline launched'
    
    

if __name__ == '__main__':
    app.run(debug=True)
