import sqlite3
import hashlib
from getpass import getpass
import os
import random
# for stdiomask type this pip install below into the terminal
# pip install stdiomask
import stdiomask
import secrets
import customtkinter as ctk
class Role:
    MANAGER = "Manager"
    ADMIN = "Admin"
# User Guide, install Sqlite Viewer from extentions to view the database in VS Code

# Random South African greeting 
greeting = ["Hello", "Hallo", "Sawubona", "Molo", "Thobela", "Lufuno", "Dumela", "Mhoro", "Xewani"]

# Hashing with salting, providing more security of data
def hash_password(password: str, salt: str = None) -> tuple:
    if not salt:
        # generate random salt
        salt = secrets.token_hex(16)  
    hashed = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode(), 
        salt.encode(), 
        100000  
    ).hex()
    return hashed, salt

# Employee data to be inserted into the DB
employees_data = {
    "MAN01": {"name": "Patrick", "password": hash_password("SuchIsLife"), "leave_available": 45, "role": "Manager"},
    "KGAS01": {"name": "Kaleb", "password": hash_password("4515449"), "leave_available": 27, "role": "Admin"},
    "MBAT02": {"name": "Mbasa", "password": hash_password("4540469"), "leave_available": 32, "role": "Frontend Dev"},
    "IKOL03": {"name": "Inga", "password": hash_password("4514785"), "leave_available": 14, "role": "Chief Consultant"},
    "TMOK04": {"name": "Tshwaraganang", "password": hash_password("4564064"), "leave_available": 30, "role": "System Analyst"},
    "AKRI05": {"name": "Ayron", "password": hash_password("4556168"), "leave_available": 23, "role": "Backend Dev"},
    "SMAT06": {"name": "Sekwele", "password": hash_password("4546163"), "leave_available": 10, "role": "Data Analyst"},
}

# Creating the table and inserting employees
def setup_database():
    # Creates the employee table and request table
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            leave_available INTEGER NOT NULL,
            role TEXT NOT NULL
        )
        """)
        
        # Request table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            leave_type TEXT NOT NULL,     -- family, vacation, personal
            description TEXT,
            days_requested INTEGER NOT NULL,
            paid_leave INTEGER NOT NULL,  -- 1 = Paid, 0 = Unpaid
            status TEXT DEFAULT 'Pending',-- Pending, Approved, Rejected
            FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
        )        
        """)
        
        # inserting all employees into the database
        for emp_id, details in employees_data.items():
            hashed, salt = details["password"]
            cursor.execute("INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?, ?, ?)",
                           (emp_id, details["name"], hashed, salt, 
                            details["leave_available"], details["role"]))
        conn.commit()

# verification of the employee
def verification(emp_id: str, password: str):
    # Retrieves the data per user on the DB
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, leave_available, role, password, salt FROM employees WHERE emp_id = ?", (emp_id,))
        result = cursor.fetchone()
        if result:
            name, leave, role, stored_hash, stored_salt = result
            hashed, _ = hash_password(password, stored_salt)
            if hashed == stored_hash:
                return name, leave, role
        return None

# Function to view all staff members without revealing personal info
def view_all_staff():
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, name, leave_available FROM employees")
        all_staff = cursor.fetchall()
        print("All Staff Members:\n")
        for emp_id, name, leave in all_staff:
            print(f"ID: {emp_id}, Name: {name}, Leave: {leave} days")
        print("\n")

# Adding New Employees
def add_employee():
    emp_id = input("New Employee ID: ").strip()
    name = input("Name: ").strip()
    password = stdiomask.getpass("Password: ").strip()
    leave = int(input("Leave Days: ").strip())
    role = input("Role: ").strip()
    
    hashed, salt = hash_password(password)
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)",
                       (emp_id, name, hashed, salt, leave, role))
        conn.commit()
    print(f"\n New employee {name} added succesfully!")

# Removing an Employee   
def remove_employee():
    emp_id = input("Enter Employee ID to remove: ").strip()
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
        conn.commit()
    print(f"\n Employee {emp_id} removed successfully.")
    
# Updating current Employee details
def update_employee():
    emp_id = input("Enter Employee ID to update: ").strip()
    field = input("Which field to update? (name/leave/role/password): ").strip().lower()
    valid_fields = {"name", "role", "leave", "password"}
    if field not in valid_fields:
        print("Invalid field.")
        return
    new_value = input("Enter new value: ").strip()

    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        if field == "password":
            hashed, salt = hash_password(new_value)
            cursor.execute("UPDATE employees SET password = ?, salt = ? WHERE emp_id = ?", 
                           (hashed, salt, emp_id))
        elif field in ["name", "role"]:
            cursor.execute(f"UPDATE employees SET {field} = ? WHERE emp_id = ?", (new_value, emp_id))
        elif field == "leave":
            cursor.execute("UPDATE employees SET leave_available = ? WHERE emp_id = ?", (int(new_value), emp_id))
        conn.commit()
    print(f"\n Employee {emp_id} updated successfully.")

# Request leave function for Employees
def request_leave(emp_id):
    print("\n_____Request Leave_____\n")
    leave_type = input("Leave Type (family/vacation/personal): ").strip().lower()
    if leave_type not in ["family", "vacation", "personal"]:
        print("Invalid leave type.")
        return
    
    days = int(input("Number of days: ").strip())
    paid_choice = input("Is this paid leave? (yes/no): ").strip().lower()
    paid_leave = 1 if paid_choice == "yes" else 0
    description = input("Description: ").strip()
    
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leave_requests (emp_id, leave_type, description, days_requested, paid_leave)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_id, leave_type, description, days, paid_leave))
        conn.commit()
    print("\n Leave request submitted and pending approval.")

# Managing Leave Requests
def manage_leave_requests():
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT request_id, emp_id, leave_type, description, days_requested, paid_leave, status 
            FROM leave_requests
        """)
        requests = cursor.fetchall()
        
        if not requests:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("No leave requests found.")
            return
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n_____Leave Requests_____\n")
        for req in requests:
            req_id, emp_id, ltype, desc, days, paid, status = req
            print(f" Request Number {req_id}: {emp_id} | {ltype} | {days} days | Paid: {'Yes' if paid else 'No'} | Status: {status}")
            print(f"\n Description: {desc}\n")
        
        # Manager action
        req_id = int(input("Enter request ID number to manage (0 to cancel): ").strip())
        if req_id == 0:
            return
        action = input("\n Approve (a) / Reject (r): ").strip().lower()
        
        if action == "a":
            # Get request details
            cursor.execute("SELECT emp_id, days_requested, paid_leave FROM leave_requests WHERE request_id = ?", (req_id,))
            emp_id, days, paid_leave = cursor.fetchone()
            
            if paid_leave == 1:  # deduct leave days
                cursor.execute("UPDATE employees SET leave_available = leave_available - ? WHERE emp_id = ?", (days, emp_id))
            
            cursor.execute("UPDATE leave_requests SET status = 'Approved' WHERE request_id = ?", (req_id,))
            conn.commit()
            print("\n Leave approved.")
        
        elif action == "r":
            cursor.execute("UPDATE leave_requests SET status = 'Rejected' WHERE request_id = ?", (req_id,))
            conn.commit()
            print("\n Leave rejected.")

# Function called for the GUI        
def approve_leave_request(request_id: int):
    """Approve a leave request by ID. Deduct leave days if paid."""
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        # fetch request details
        cursor.execute("SELECT emp_id, days_requested, paid_leave, status FROM leave_requests WHERE request_id = ?", (request_id,))
        row = cursor.fetchone()
        if not row:
            return False, "Request not found."
        
        emp_id, days, paid_leave, status = row
        if status != "Pending":
            return False, f"Request already {status}."

        # deduct leave if paid
        if paid_leave == 1:
            cursor.execute("SELECT leave_available FROM employees WHERE emp_id = ?", (emp_id,))
            leave_row = cursor.fetchone()
            if not leave_row:
                return False, "Employee not found."
            leave_available = leave_row[0]
            if leave_available < days:
                return False, f"Insufficient leave balance ({leave_available} days left)."
            cursor.execute("UPDATE employees SET leave_available = leave_available - ? WHERE emp_id = ?", (days, emp_id))

        # update request status
        cursor.execute("UPDATE leave_requests SET status = 'Approved' WHERE request_id = ?", (request_id,))
        conn.commit()
        return True, "Leave approved."

# Function called for the GUI
def deny_leave_request(request_id: int):
    """Reject a leave request by ID."""
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM leave_requests WHERE request_id = ?", (request_id,))
        row = cursor.fetchone()
        if not row:
            return False, "Request not found."
        
        status = row[0]
        if status != "Pending":
            return False, f"Request already {status}."

        cursor.execute("UPDATE leave_requests SET status = 'Rejected' WHERE request_id = ?", (request_id,))
        conn.commit()
        return True, "Leave rejected."


def view_your_requests(emp_id):
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT request_id, leave_type, description, days_requested, paid_leave, status
            FROM leave_requests
            WHERE emp_id = ?
        """, (emp_id,))
        requests = cursor.fetchall()
        
        if not requests:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nYou have no leave requests.")
            return
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n_____My Leave Requests_____\n")
        for req in requests:
            req_id, ltype, desc, days, paid, status = req
            print(f"Request {req_id}: {ltype} | {days} days | Paid: {'Yes' if paid else 'No'} | Status: {status}")
            print(f"Description: {desc}\n")

app_running = True

# Staff Login page
def staff_page(emp_id, name, leave, role):
    while app_running:
        print("_____Staff Page_____\n")
        print(f"Hey there {name}, you are logged in as {role}.")
        print(f"Leave days available: {leave} days\n")
        print("1. Request Leave ")
        print("2. View Your Leave Requests ")
        print("3. Logout\n")
        try:
            choice = int(input(" Choose an option: ").strip())
            
            if choice == 1:
                request_leave(emp_id)
            elif choice == 2:
                view_your_requests(emp_id)
            elif choice == 3:
                break
        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(" Invalid Choice...try again.")

# Unique Manager Login page       
def manager_page(name, leave, role):
    while app_running:
        print("_____Manager Page_____\n")
        print(f"Hey there {name}, you are logged in as {role}.")
        print(f"Leave days available: {leave} days\n")
        print("1. View All Staff Members")
        print("2. Manage Leave Requests")
        print("3. Logout\n")
        try:
            choice = int(input("Choose an option: ").strip())
        
            if choice == 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                view_all_staff()
            elif choice == 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                manage_leave_requests()
            elif choice == 3:
                break
        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid Choice...try again.")
            
# Unique Admin Login page
def admin_page(name, leave, role):
    while app_running:
        print("_____Admin Page_____\n")
        print(f"Hey there {name}, you are logged in as {role}.")
        print(f"Leave days available: {leave} days\n")
        print("1. Add new employee")
        print("2. Remove employee")
        print("3. Update employee details")
        print("4. Manage Leave Requests")
        print("5. Logout\n")
        try:
            choice = int(input("Choose an option: ").strip())

            if choice == 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                add_employee()
            elif choice == 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                remove_employee()
            elif choice == 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                update_employee()
            elif choice == 4:
                os.system('cls' if os.name == 'nt' else 'clear')
                manage_leave_requests()
            elif choice == 5:
                break
        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid Choice...try again.")

# The User Interface Logic function
def ui_interface(max_attempts = 3):
    # While loop used to allow seemless function between frames and allow the app to continuosly run
    attempts = 0
    while attempts < max_attempts:
        print("______ClockedIn Outsourcing Suite______")
        print(f"\n     -----{random.choice(greeting)}!-----     ")
        emp_id = input("\n Enter Employee ID: ").strip()
        password = stdiomask.getpass(" Enter Password: ").strip()
        
        user_info = verification(emp_id, password)   
        if user_info:
            os.system('cls' if os.name == 'nt' else 'clear')
            name, leave, role = user_info
            # print(f"\nWelcome! {name} ({role}) ({leave} days)")
            
            if role == Role.MANAGER:
                manager_page(name, leave, role)
            elif role == Role.ADMIN:
                admin_page(name, leave, role)
            else:
                staff_page(emp_id, name, leave, role)
            return
        else:
            attempts += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n Invalid Password or User ID, you have {max_attempts - attempts} attempts remaining.")
            if attempts == max_attempts:
                print("\n Maximum Login Attempts reached!")

# User interface
if __name__ == "__main__":
    setup_database()
    os.system('cls' if os.name == 'nt' else 'clear')
    ui_interface()