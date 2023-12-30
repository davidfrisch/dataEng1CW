from dotenv import load_dotenv
import os
import requests

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL')

if not BACKEND_URL:
    raise Exception('BACKEND_URL not defined in .env file')

client = requests.Session()
client.headers.update({'Content-Type': 'application/json'})
client.base_url = BACKEND_URL





# Runs
client.start_run = lambda run: client.post(f'{client.base_url}/runs/launch_pipeline', headers={'Content-type': 'application/json'}, data=run)
client.get_run_status = lambda run_id: client.get(f'{client.base_url}/runs/{run_id}').json()
client.download_run = lambda run_id: client.get(f'{client.base_url}/runs/{run_id}/download')


# Proteins
client.get_protein = lambda protein_id: client.get(f'{client.base_url}/proteins/{protein_id}')