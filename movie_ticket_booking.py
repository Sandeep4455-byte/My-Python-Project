"""
PS No. 48 - Movie Ticket Booking System
Console app: book seats, cancel bookings, view seat map.
Bookings are saved in bookings.txt (one line per seat: SEAT,NAME).
"""

import os

ROWS = ["A", "B", "C"]
SEATS_PER_ROW = 5
PRICE = 200
FILE_NAME = "bookings.txt"
INVALID_MSG = "Invalid seat. Rows are A to C and seat numbers are 1 to 5."


def create_hall():
    """2D list: hall[row][seat] is None (free) or the customer's name."""
    return [[None] * SEATS_PER_ROW for _ in ROWS]


def parse_seat(code):
    """Convert 'A1' -> (0, 0). Return None if the code is invalid."""
    code = code.strip().upper()
    if len(code) != 2:
        return None
    row_letter, number = code[0], code[1]
    if row_letter not in ROWS or not number.isdigit():
        return None
    seat = int(number)
    if seat < 1 or seat > SEATS_PER_ROW:
        return None
    return ROWS.index(row_letter), seat - 1


def seat_name(row, col):
    return f"{ROWS[row]}{col + 1}"


def seats_left(hall):
    return sum(1 for r in hall for s in r if s is None)


def load_bookings(hall):
    """Load saved bookings from the file at program start."""
    if not os.path.exists(FILE_NAME):
        return
    with open(FILE_NAME, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "," not in line:
                continue
            code, name = line.split(",", 1)
            pos = parse_seat(code)
            if pos:
                hall[pos[0]][pos[1]] = name


def save_bookings(hall):
    """Save all bookings to the file (called after every change)."""
    with open(FILE_NAME, "w") as f:
        for r in range(len(ROWS)):
            for c in range(SEATS_PER_ROW):
                if hall[r][c] is not None:
                    f.write(f"{seat_name(r, c)},{hall[r][c]}\n")


def read_seats(text):
    """Split input like 'A2 A3' or 'A2,A3' into a list of unique codes."""
    codes = []
    for part in text.replace(",", " ").split():
        part = part.upper()
        if part not in codes:
            codes.append(part)
    return codes


def book_seats(hall):
    if seats_left(hall) == 0:
        print("Show is housefull. No seats available.")
        return

    codes = read_seats(input("Seat: "))
    if not codes:
        print(INVALID_MSG)
        return

    # Validate every seat before booking anything
    positions = []
    for code in codes:
        pos = parse_seat(code)
        if pos is None:
            print(INVALID_MSG)
            return
        positions.append((code, pos))
    for code, (r, c) in positions:
        if hall[r][c] is not None:
            print(f"Seat {code} is already booked.")
            return

    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    for code, (r, c) in positions:
        hall[r][c] = name
    save_bookings(hall)

    amount = len(positions) * PRICE
    label = "Seat" if len(positions) == 1 else "Seats"
    print(f"{label} {', '.join(c for c, _ in positions)} booked for {name}. Amount: {amount}")

    if seats_left(hall) == 0:
        print("Seats left: 0")
        print("Show is now housefull.")


def cancel_booking(hall):
    codes = read_seats(input("Seat to cancel: "))
    if not codes:
        print(INVALID_MSG)
        return

    positions = []
    for code in codes:
        pos = parse_seat(code)
        if pos is None:
            print(INVALID_MSG)
            return
        positions.append((code, pos))
    for code, (r, c) in positions:
        if hall[r][c] is None:
            print(f"Seat {code} is not booked.")
            return

    for code, (r, c) in positions:
        hall[r][c] = None
    save_bookings(hall)

    label = "Seat" if len(positions) == 1 else "Seats"
    print(f"{label} {', '.join(c for c, _ in positions)} cancelled. Refund: {len(positions) * PRICE}")


def show_seat_map(hall):
    for r, row_letter in enumerate(ROWS):
        cells = " ".join("X" if s is not None else "_" for s in hall[r])
        print(f"Row {row_letter}: {cells}")
    print(f"Seats left: {seats_left(hall)}")


def main():
    hall = create_hall()
    load_bookings(hall)

    while True:
        print("\n--- Movie Ticket Booking System ---")
        print("1. Book")
        print("2. Cancel")
        print("3. Seat map")
        print("4. Exit")
        try:
            choice = input("Menu option: ").strip()
        except EOFError:
            break

        if choice == "1":
            book_seats(hall)
        elif choice == "2":
            cancel_booking(hall)
        elif choice == "3":
            show_seat_map(hall)
        elif choice == "4":
            print("Thank you!")
            break
        else:
            print("Invalid option. Choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()