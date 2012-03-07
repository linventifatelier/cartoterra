import os

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

workers = numCPUs() * 2 + 1
bind = "127.0.0.1:8001"
pidfile = "/tmp/gunicorn-earthbuilding-2.pid"
backlog = 2048
logfile = "/home/linventifatelier/earthbuilding/log/gunicorn-earthbuilding-2.log"
loglevel = "info"
timeout=90
