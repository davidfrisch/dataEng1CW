from client_api import client
import sys

def download_protein(protein):
  id = protein['id']
  seq = protein['sequence']
  with open(f'{id}.fasta', 'w') as f:
    f.write(f'>{id}\n')
    f.write(f'{seq}\n')


# Find proteins by name
def search_protein_id(protein_name: str):
  
  """
  Search for a protein by name
  :param protein_name: The protein name
  :return: The protein id
  """
  res = client.get_protein(protein_name)
  if res.status_code != 200:
    print(f'Error: {res.status_code}, {res.text}')
    return
  
  protein = res.json()
  status = protein['status']
  if status == 'NOT_FOUND':
    print(f'No protein found with name {protein_name}')
    return
  
  if status == 'MULTIPLE_FOUND':
    print(f'Multiple proteins found with name {protein_name}')
    print('Please choose one of the following ids (showing first 10):')
    for protein_id in protein['proteins'][:10]:
      print(protein_id)
  
  if status == 'success':
    print(f'Found protein id: {protein["id"]} in DB')
    runs_found = protein['runs']
    print(f'There are {len(runs_found)} runs for this protein')
    if len(sys.argv) > 2 and sys.argv[2] == '--download':
      download_protein(protein)
    else:
      print('Use --download to download the protein')
    

    


if __name__ == '__main__':
    protein_name = ''
    if len(sys.argv) > 1:
        protein_name = sys.argv[1]
    else:
        protein_name = input('Enter protein name: ')


    protein_id = search_protein_id(protein_name)
