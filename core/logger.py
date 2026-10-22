# NIGHT HUNTER - Logger

from datetime import datetime


def log_info(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time}] [INFO] {message}")


def log_warning(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time}] [WARNING] {message}")


def log_error(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time}] [ERROR] {message}")