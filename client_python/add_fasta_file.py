from dotenv import load_dotenv
import os
import requests
import sys
load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL')
PROTEIN_STATUS_UPLOAD = {
    0: 'SUCCESS',
    1: 'PROTEIN_ALREADY_EXIST',
    2: 'ERROR'
}

def send_fasta_file(file_path):
  if not file_path.endswith('.fasta'):
    print('File is not a fasta file.')
    sys.exit(1)

  if not os.path.isfile(file_path):
    print('File does not exist.')
    sys.exit(1)


  with open(file_path, 'rb') as file:
    response = requests.post(BACKEND_URL + '/upload', files={'file': file}, data={'name': 'my_file.fasta'})
    if response.status_code == 200:
      data = response.json()
      protein_status = data['protein_status']
      print('Fasta file uploaded successfully.')
      for protein in protein_status:
        print(f"{protein['id']}, {PROTEIN_STATUS_UPLOAD[protein['status']]}")
    else:
      print('Failed to upload fasta file.')
      print(response.text)


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: python add_fasta_file.py <file_path>')
    sys.exit(1)

  file_path = sys.argv[1]
  send_fasta_file(file_path)