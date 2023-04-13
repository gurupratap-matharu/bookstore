# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
# https://docs.gunicorn.org/en/stable/settings.html

import multiprocessing  # noqa

# restart workers after so many requests with some variability
max_requests = 1000
max_requests_jitter = 50


# Bind to a unix socket (created by systemd)
bind = "unix:/run/bookstore-gunicorn.sock"


# Define the number of workers
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1  # <-- Change this later but for testing 1 is enough

# Access log - records incoming HTTP requests
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s "%(r)s" %(s)s'

# Error log - records Gunicorn server errors
errorlog = "-"
error_log_format = '%(h)s %(l)s %(u)s "%(r)s" %(s)s'

log_file = "-"


# Whether to send Django output to the error log
capture_output = True


# How verbose the Gunicorn error logs should be
loglevel = "info"

enable_stdio_inheritance = True
