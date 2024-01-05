# Project Setup Guide

## Git Clone

Clone the repository to the Host VM:

```bash
git clone https://github.com/davidfrisch/dataEng1CW.git
cd dataEng1CW/
```

## SSH Configuration

Ensure that the public key is added to the 'authorized_keys' file on each VM, corresponding to the private key intended for ssh connection.


## Inventory Configuration

Create an inventory file (`./ansible/inventory.ini`) with your cluster information by editing the following template and running the command:

```bash
echo "\
[client]
<client_ip>

[clusters]
<cluster1_ip>
<cluster2_ip>
<cluster.._ip>
<clusterN_ip>
"\
>./ansible/inventory.ini
```

## Host Setup

Run the following commands to set up the hosts:

```bash
./scripts/host_setup_script.sh 
-s <my_private_key> \
-t <git_token> \
--db-user <db_user> \
--db-pass <db_pass>
```

If it fails because the ansible ping fails, fix the issue and run the script again.

This script creates the file `ansible/custom_vars.yml`, install ansible and test the connection to the VMs.

## Dependencies Installation

Install dependencies with:

```bash
sudo dnf install tmux
```

## Ansible Playbook Execution

Start a new `tmux` session:

```bash
tmux
```

Run the Ansible playbook:

```bash
ansible-playbook ansible/main_playbook.yml -i ansible/inventory.ini
```

### Note

⚠️ It will take approximately 2-3 hours for the initial setup because pdb70 is a large database.

💡 Monitor the progress of the Ansible script using:

```bash
tmux attach-session -t <session-id>
```

Now, your environment should be set up and ready for use.
