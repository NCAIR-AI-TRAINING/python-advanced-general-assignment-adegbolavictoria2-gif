from datetime import datetime, timedelta

# Custom Exception
\
class DuplicateVisitorError(Exception):
    def __init__(self, name, minutes_left=None):
        if minutes_left is None:
            message = (
                f"Visitor '{name}' already signed in last! "
                f"Duplicate entry is not allowed."
            )
        else:
            message = (
                f"Visitor '{name}' must wait {minutes_left:.1f} more minutes "
                f"before signing in again."
            )
        super().__init__(message)


# Main Program

def main():
    filename = "visitors.txt"

    #  Ensure file exists
    
    try:
        with open(filename, "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        print("visitors.txt not found. Creating a new one...")
        with open(filename, "w", encoding="utf-8"):
            pass

    
    # User Input
    
    visitor = input("Enter visitor's name: ").strip()

    try:
       
        # Read last entry in file
        
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        last_visitor = None
        last_time = None

        if lines:
            last_line = lines[-1].strip().split(" | ")
            last_visitor = last_line[0]

            # Convert saved timestamp to datetime object
            last_time = datetime.strptime(
                last_line[1].strip(),
                "%Y-%m-%d %H:%M:%S.%f"
            )

       
        # Duplicate + 5-minute rule
        if visitor == last_visitor:
            now = datetime.now()
            elapsed_time = now - last_time

            minimum_wait = timedelta(minutes=5)

            if elapsed_time < minimum_wait:
                minutes_left = (minimum_wait - elapsed_time).total_seconds() / 60
                raise DuplicateVisitorError(visitor, minutes_left)
            else:
                raise DuplicateVisitorError(visitor)

        #  Log visitor with timestamp

        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now()}\n")

        print("Visitor added successfully!")

   
    #  Error Handling
    except DuplicateVisitorError as e:
        print("Error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


# Run the program
main()
