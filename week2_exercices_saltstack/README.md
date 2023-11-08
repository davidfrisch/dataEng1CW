# Instructions

At the end of the lesson we had installed and started apache/httpd using Saltstack. 

Now write the appropriate .sls files to use saltstack to start httpd listening on port 4444 rather than the standard port of port 80. Confirm that you can reach the apache default page.

Once your Salt sls files are working start a post in this forum. Cut and paste your code and explain how it works. Reply to another post and comment on something that is good about your classmate's solution and one thing that might be improved.

=> Write .sls file to use slatstack to start httpd listening on port 4444 rather than port 80
=> Confirm that you can reach the apache default page


# About the exercise

## Create a Salt State file:
 - The httpd_config.sls is in `/srv/salt/httpd_config.sls` in the master salt directory.

  -  `salt://` source refers to the `/srv/salt` of the master machine

## Apply file
```bash
sudo salt 'id_minion' state.sls 'filename_without_extensions'
```

## Restart httpd in the client
```bash
ssh DataEngClient
sudo systemctl restart httpd
```

## Check if it works
 
Open your brwoser and visit my_ip_address:4444