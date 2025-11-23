from datetime import datetime, timedelta
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass

def get_last_visitor():
    if not os.path.exists(FILENAME):
        return None, None

    with open(FILENAME, "r") as f:
        lines = f.readlines()

    if not lines:
        return None, None

    last_line = lines[-1].strip()
    try:
        name, timestamp = last_line.split(" | ")
        dt = datetime.fromisoformat(timestamp)
        return name, dt
    except:
        return None, None

def add_visitor(visitor_name):
    ensure_file()

    last_name, last_time = get_last_visitor()

    if visitor_name == last_name:
        raise DuplicateVisitorError("Duplicate consecutive visitor not allowed.")

    if last_time is not None:
        now = datetime.now()
        if now - last_time < timedelta(minutes=5):
            raise EarlyEntryError("Must wait 5 minutes before logging a new visitor.")

    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {datetime.now().isoformat()}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main(
