import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1
wsg_app = 'app:app'
bind = '0.0.0.0:80'
accesslog = 'logs/gunicorn.log'
errorlog = 'logs/gunicorn.error.log'
capture_output = True
timeout = 10