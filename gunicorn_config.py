import multiprocessing

# Server socket
bind = "0.0.0.0:8080"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'  # 'sync', 'gevent', 'eventlet', etc.

# Timeout
timeout = 120  # seconds

# Logging
accesslog = '-'  # '-' means log to stdout
errorlog = '-'
loglevel = 'info'

# Reduce logging noise from workers
if workers > 1:
    accesslog = None  # Disable access logging when running multiple workers 