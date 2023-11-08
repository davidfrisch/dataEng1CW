copy_my_files:
  file.managed:
    - name: /etc/config_fake.yml
    - source: salt://config_fake.yml
    - makedirs: True
