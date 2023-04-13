import datetime

def log(message):
    with open("log.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        f.write(f"[{timestamp}]: {message}")
