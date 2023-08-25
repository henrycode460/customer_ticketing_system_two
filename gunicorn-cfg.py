
import multiprocessing

bind = "0.0.0.0:8000"  # Gunicorn will bind to all available network interfaces
workers = multiprocessing.cpu_count() * 2 + 1  # Adjust the number of workers as needed
accesslog = "-"  # You can customize the log paths
errorlog = "-"

