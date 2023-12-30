from client_api import client
import sys

def download_run(run_id: str):
    """
    Download the results of a run
    :param run_id: The run id
    :return: save a zip file with the results
    """
    run_exists = client.get_run_status(run_id)
    if not run_exists:
        print(f'No run found for with id {run_id}')
        return
    
    if run_exists['progress']['PENDING'] != 0:
        print(f'Run {run_id} is not complete yet')
        should_download = input('Do you want to download the results anyway? (y/n)')
        if should_download != 'y':
            return
        

    res = client.download_run(run_id)
    with open(f'{run_id}.zip', 'wb') as f:
        f.write(res.content)


if __name__ == '__main__':
    run_id = ''
    if len(sys.argv) > 1:
        run_id = sys.argv[1]
    else:
        run_id = input('Enter run id: ')
    download_run(run_id)