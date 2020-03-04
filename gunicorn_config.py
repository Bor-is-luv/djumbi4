command = '/home/bor/dvenv/bin/gunicorn'
pythonpath = '/home/bor/test/djumbi4'
bind = '127.0.0.1:8001'
workers = 5
user = 'bor'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO-SETTINGS_MODULE=djumbi4.settings'

