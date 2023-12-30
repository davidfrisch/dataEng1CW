from client_api import client
import sys
import os
import json

def start_run(ids, name):
    obj = {
        'ids': ids,
        'process_name': name    
    }

    response = client.start_run(json.dumps(obj))
    if response.status_code == 200:
        # Print the content of the response
        print(response.content)
    else:
        # Print an error message
        print(f"Error: {response.status_code}, {response.text}")

def check_id(protein_id):
    response = client.get_protein(protein_id)
    if response.status_code != 200:
        return False
    
    return True



if __name__ == '__main__':

    ids = []
    # filepath in the arguments
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f:
                    if line.strip() != '':
                        ids.append(line.strip())
        else:
            print('Invalid argument')
            exit(1)
    else:
        print('No arguments provided')
        exit(1)

    if len(ids) == 0:
        print('No ids provided')
        exit(1)
    

    has_invalid_id = False
    for i in range(len(ids)):
        if not check_id(ids[i]):
            print(f'Invalid id: {ids[i]}')
            has_invalid_id = True

    if has_invalid_id:
        print("Add the invalid ids in the database")
        exit(1)

    name = ''
    is_valid = False

    while not is_valid:
        name = input('Enter the name of the process: ')
        if ' ' not in name.strip() and len(name) > 0:
            is_valid = True
        else:
            print('Invalid name, no spaces allowed')

    start_run(ids, name.strip())