
install_httpd:
  pkg.installed:
    - name: httpd

change_httpd_port:
  file.replace:
    - name: /etc/httpd/conf/httpd.conf  # Specify the path to your Apache configuration file
    - pattern: 'Listen 80'  # The pattern to search for in the file
    - repl: 'Listen 4444'   # The replacement value with the new port

semanage_port_4444:
  cmd.run:
    - name: sudo semanage port -m -t http_port_t -p tcp 4444

open_firewall_port:
  cmd.run:
    - name: firewall-cmd --add-port=4444/tcp --permanent
    - require:
      - pkg: httpd
    - onchanges:
      - file: /etc/httpd/conf/httpd.conf

reload_firewall:
  cmd.run:
    - name: firewall-cmd --reload
    - require:
      - cmd: open_firewall_port

stop_httpd:
  service.dead:
    - name: httpd

start_httpd:
  service.running:
    - name: httpd
    - enable: True

# Check that the port is open
curl_example:
  cmd.run:
    - name: curl http://ec2-35-178-4-221.eu-west-2.compute.amazonaws.com:4444
