from datetime import datetime, timedelta
import os

VISITORS_FILE = "visitors.txt"  # File to store visitor data
WAIT_MINUTES = 5  # Minimum waiting time between visitors

def ensure_file_exists():
    # Make sure the file exists; create it if not
    if not os.path.exists(VISITORS_FILE):
        with open(VISITORS_FILE, "w", encoding="utf-8") as f:
            pass

def _read_last_entry():
    # Read the last entry from the file
    if not os.path.exists(VISITORS_FILE):
        return None, None

    with open(VISITORS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return None, None

    last = lines[-1]
    if "|" not in last:
        return last, None

    name, ts = last.rsplit("|", 1)  # Split only on last '|'
    try:
        dt = datetime.fromisoformat(ts)
    except Exception:
        dt = None

    return name, dt

def _append_entry(name, when):
    # Append a new visitor entry with timestamp
    with open(VISITORS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name}|{when.isoformat()}\n")

def log_visitor(name):
    # Validate name input
    if not isinstance(name, str) or not name.strip():
        return False, "Invalid name provided"

    name_clean = name.strip()
    ensure_file_exists()
    last_name, last_ts = _read_last_entry()

    # Prevent consecutive duplicate names
    if last_name is not None and last_name.strip().lower() == name_clean.lower():
        return False, "Duplicate consecutive visitor not allowed"

    now = datetime.now()

    # Enforce waiting time
    if last_ts is not None and isinstance(last_ts, datetime):
        delta = now - last_ts
        if delta < timedelta(minutes=WAIT_MINUTES):
            remaining = timedelta(minutes=WAIT_MINUTES) - delta
            remaining_seconds = int(remaining.total_seconds())
            mins, secs = divmod(remaining_seconds, 60)
            return False, f"Please wait {mins} minute(s) {secs} second(s) before next visitor"

    _append_entry(name_clean, now)
    return True, "Visitor successfully logged"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Usage: python main.py "Visitor Name"')
        sys.exit(1)

    # Combine all command-line arguments to support multi-word names
    name = " ".join(sys.argv[1:])
    success, message = log_visitor(name)
    print(message)
    sys.exit(0 if success else 2)
