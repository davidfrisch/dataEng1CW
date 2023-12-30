# Micro-Services Startup Guide

## Start Micro-Services

Run the following command to start all micro-services:

```bash
./scripts/start_all.sh
```

## Stop Micro-Services

To stop the running micro-services, execute the following command:

```bash
./scripts/stop_all.sh
```

Now, your micro-services should be up and running. Adjust configurations as needed and enjoy using the system!


## Use the Web Application

Guide tour of the web application is available in the pdf report of the coursework.
Visit on your browser the url of the client VM to access the web application.

## Use the python client

The python client is available in the client_python folder. 
Install its dependencies with the following command:

```bash
cd client_python
pip3 install python-dotenv requests
```

### Add a fasta file

To add a fast file to the platform, run the following command:

```bash
python3 add_fasta_file.py <path_to_fasta_file>
```

### Search for a sequence ID

To search for a sequence ID, run the following command:
Make sure to use apostrophes around the sequence ID.

```bash
python3 search_protein_id.py '<sequence_id>'
```
e.g.:
```bash
python3 search_protein_id.py 'sp|A0A0B4J2F'
```

### Start a run from a list of sequence ids

To start a run from a list of sequence ids, run the following command:
Make sure to use apostrophes around the sequence IDs.

```bash
python3 start_run.py <file_path_with_sequence_ids>
```

### View progress of a run

To view the progress of a run, run the following command:

```bash
python3 get_run_status.py <run_id>
```

### Download the results of a run

To download the results of a run, run the following command:

```bash
python3 download_run_results.py <run_id>
```
