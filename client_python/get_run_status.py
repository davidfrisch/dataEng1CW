from client_api import client
import sys

def get_run_status(run_id: str):
    """
    Get the status of a run
    :param run_id: The run id
    :return: The status of the run
    """
    res = client.get_run_status(run_id)
    proteins = res['proteins']
    run_summary = res['run_summary']
    progress = res['progress']

    if not proteins:
        print(f'No run found for with id {run_id}')
        return

    print(f'Run summary: {run_summary["run_id"]}')
    print(f"Progress: {progress['total']} total, {progress['PENDING']} pending, {progress['RUNNING']} running, "
          f"{progress['SUCCESS']} success, {progress['FAILED']} failed")
    print(f"{progress['SUCCESS']}/{progress['total']} proteins completed")
    
    if progress['PENDING'] == 0:
        print('You can download the results by running:')
        print(f'python3 download_run_results.py {run_id}')
    else:
        SPARK_URL = client.base_url.replace('api', 'spark-master/')
        print(f"Spark master url: {SPARK_URL}")


if __name__ == '__main__':
    run_id = ''
    if len(sys.argv) > 1:
        run_id = sys.argv[1]
    else:
        run_id = input('Enter run id: ')
    run_id = get_run_status(run_id)

