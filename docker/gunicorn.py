# The Access log file to write to. [None]

# The Access log format . [%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"]
# access_log_format='"%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Logging config file.
# logconfig="/opt/example/log.conf"

# The Error log file to write to. [-]
errorlog = "/app/logs/gunicorn-error.log"
accesslog = "-"

# The granularity of Error log outputs. [info]
loglevel = "error"

# The logger you want to use to log events in gunicorn. [simple]
# logger_class='simple'

# A base to use with setproctitle for process naming. [None]
proc_name = "core"

# Load application code before the worker processes are forked. [False]
preload_app = False

# forked. [False]
daemon = False
# daemon=True

# A filename to use for the PID file. [None]
# pidfile='/var/run/example.pid'
pidfile = "/tmp/gunicorn.pid"

# Switch worker processes to run as this user. [0]
# user="example"

# Switch worker process to run as this group. [0]
# group="example"

# A bit mask for the file mode on files written by Gunicorn. [0]
# umask=0002

# The socket to bind. [127.0.0.1:8000]
# bind = "0.0.0.0:8000"

# The maximum number of pending connections.     [2048]
#  - Amazon Linux default=1024 ($ sysctl net.ipv4.tcp_max_syn_backlog)
backlog = 512

# The number of worker process for handling requests. [1]
workers = 1

# The type of workers to use. [sync]
# https://hackernoon.com/why-you-should-almost-always-choose-sync-gunicorn-over-workers-ze9c32wj
# worker_class='gevent'

# The maximum number of simultaneous clients. [1000]
worker_connections = 4096

# The maximum number of requests a worker will process before restarting. [0]
max_requests = 4096

# Workers silent for more than this many seconds are killed and restarted. [30]
timeout = 120

# The number of seconds to wait for requests on a Keep-Alive connection. [2]
# keepalive=65

# The jitter causes the restart per worker to be randomized by randint(0, max_requests_jitter). This is intended to stagger worker restarts to avoid all workers restarting at the same time. [0]
max_requests_jitter = 1000

# After receiving a restart signal, workers have this much time to finish serving requests.
# Workers still alive after the timeout (starting from the receipt of the restart signal) are force killed. [30]
graceful_timeout = 120
