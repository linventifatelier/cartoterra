import multiprocessing

bind = "127.0.0.1:8001"
workers = multiprocessing.cpu_count() * 2 + 1

pidfile = "/home/www-cartoterra/gunicorn-cartoterra.pid"
backlog = 2048
accesslog = "/home/www-cartoterra/log/gunicorn-access.log"
errorlog = "/home/www-cartoterra/log/gunicorn-error.log"
loglevel = "debug"
timeout=90
