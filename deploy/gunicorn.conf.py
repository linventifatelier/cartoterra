import os

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

workers = numCPUs() * 2 + 1
bind = "127.0.0.1:8000"
pidfile = "/home/www-cartoterra/gunicorn-cartoterra.pid"
backlog = 2048
logfile = "/home/www-cartoterra/gunicorn-cartoterra.log"
loglevel = "info"
timeout=90
