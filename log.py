import datetime


def log(message):
    with open("log.txt", "a", encoding='utf-8', errors='ignore') as f:
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")
