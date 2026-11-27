import json
import os
from datetime import datetime

FILE_NAME = "attendance.txt"


def load_data():
    """Loads employee records from attendance.txt."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            content = file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []


def save_data(employees):
    """Saves employee records to attendance.txt."""
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)


def generate_employee_id(employees):
    """Generates sequential employee IDs starting from E101."""
    if not employees:
        return "E101"
    last_id = employees[-1]["id"]
    num = int(last_id[1:]) + 1
    return f"E{num}"


def find_employee(employees, emp_id):
    """Finds and returns an employee dictionary by ID, or None if not found."""
    for emp in employees:
        if emp["id"].upper() == emp_id.upper():
            return emp
    return None


def is_valid_date(date_str):
    """Validates if the date string matches YYYY-MM-DD."""
    if len(date_str) != 10:
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_employee(employees):
    """Adds a new employee and saves to file."""
    name = input("Name: ").strip()
    if not name:
        print("Employee name cannot be empty.")
        return

    emp_id = generate_employee_id(employees)
    new_employee = {
        "id": emp_id,
        "name": name,
        "records": {}
    }
    employees.append(new_employee)
    save_data(employees)
    print(f"Employee added: {emp_id} | {name}")


def mark_attendance(employees):
    """Marks daily attendance with validation and duplicate checking."""
    emp_id = input("Employee ID: ").strip().upper()
    emp = find_employee(employees, emp_id)
    if not emp:
        print(f"Employee {emp_id} not found.")
        return

    date_str = input("Date (YYYY-MM-DD): ").strip()
    if not is_valid_date(date_str):
        print("Invalid date. Use YYYY-MM-DD.")
        return

    status = input("Status (P/A/L): ").strip().upper()
    if status not in ("P", "A", "L"):
        print("Invalid status. Enter P, A or L.")
        return

    if date_str in emp["records"]:
        print(f"Attendance for {date_str} is already marked.")
        return

    emp["records"][date_str] = status
    save_data(employees)
    print(f"Attendance marked for {emp['name']} ({emp_id}) on {date_str}: {status}")


def show_report(employees):
    """Displays the attendance summary and percentage for a specific employee."""
    emp_id = input("Employee ID: ").strip().upper()
    emp = find_employee(employees, emp_id)
    if not emp:
        print(f"Employee {emp_id} not found.")
        return

    records = emp["records"]
    present_count = sum(1 for s in records.values() if s == "P")
    absent_count = sum(1 for s in records.values() if s == "A")
    leave_count = sum(1 for s in records.values() if s == "L")
    total_marked = len(records)

    print(f"{emp['name']}: Present {present_count} | Absent {absent_count} | Leave {leave_count}")

    if total_marked == 0:
        print("Attendance: 0.00% (no records)")
    else:
        percentage = (present_count / total_marked) * 100
        print(f"Attendance: {percentage:.2f}%")


def main():
    employees = load_data()

    while True:
        print("\n--- Employee Attendance System ---")
        print("1. Add Employee")
        print("2. Mark Attendance")
        print("3. View Attendance Report")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            mark_attendance(employees)
        elif choice == "3":
            show_report(employees)
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()