import os

log_dir = 'logs'

def create_logs_dir(log_dir):
    os.makedirs(log_dir, exist_ok=True)

