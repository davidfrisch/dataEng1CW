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
    # 'progress': {'total': 5, 'PENDING': 0, 'RUNNING': 0, 'SUCCESS': 5, 'FAILED': 0}}
    print(f"Progress: {progress['total']} total, {progress['PENDING']} pending, {progress['RUNNING']} running, "
          f"{progress['SUCCESS']} success, {progress['FAILED']} failed")
    print(f"{progress['SUCCESS']}/{progress['total']} proteins completed")


if __name__ == '__main__':
    run_id = ''
    if len(sys.argv) > 1:
        run_id = sys.argv[1]
    else:
        run_id = input('Enter run id: ')
    run_id = get_run_status(run_id)

