import sqlite3
import hashlib
import secrets
import random
# pip install customtkinter
import customtkinter as ctk
from tkinter import messagebox, simpledialog

# -------- USER/TESTER BASIC GUIDE ----------
# Input one of the USER IDS in the intial template (eg. KGAS01)
# Enter the corresponding password (eg. 4515449)

# ---------- CONFIG ----------
class Role:
    MANAGER = "Manager"
    ADMIN = "Admin"
    STAFF = "Staff"

greeting = ["Hello", "Hallo", "Sawubona", "Molo", "Thobela",
            "Lufuno", "Dumela", "Mhoro", "Avuxeni"]

# ---------- SECURITY ----------
def hash_password(password: str, salt: str = None) -> tuple:
    """
    Returns (hashed_hex, salt_hex). If salt is provided it is used (must be hex string).
    """
    if password is None:
        raise ValueError("Please Enter your Password")
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(),100000).hex()
    return hashed, salt

# ---------- DATABASE (initial template testing data) ----------
# Use these User IDs and passwords for testing
employees_data = {
    "MAN01": {"name": "Patrick", "password": hash_password("SuchIsLife"), "leave_available": 45, "role": Role.MANAGER},
    "KGAS01": {"name": "Kaleb", "password": hash_password("4515449"), "leave_available": 27, "role": Role.ADMIN},
    "MBAT02": {"name": "Mbasa", "password": hash_password("4540469"), "leave_available": 32, "role": "Frontend Dev"},
    "IKOL03": {"name": "Inga", "password": hash_password("4514785"), "leave_available": 14, "role": "Chief Consultant"},
    "TMOK04": {"name": "Tshwaraganang", "password": hash_password("4564064"), "leave_available": 30, "role": "System Analyst"},
    "AKRI05": {"name": "Ayron", "password": hash_password("4556168"), "leave_available": 23, "role": "Backend Dev"},
    "SMAT06": {"name": "Sekwele", "password": hash_password("4546163"), "leave_available": 10, "role": "Data Analyst"},
}

DB_FILE = "test1.db"

def setup_database():
    with sqlite3.connect(DB_FILE) as conn:
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
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            leave_type TEXT NOT NULL,
            description TEXT,
            days_requested INTEGER NOT NULL,
            paid_leave INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
        )
        """)
        # seed the data into the database
        for emp_id, details in employees_data.items():
            try:
                hashed, salt = details["password"]
            except Exception:
                # if something unexpected occurs, a re-hash takes place
                hashed, salt = hash_password(str(details.get("password", "")))
            cursor.execute("""
                INSERT OR REPLACE INTO employees (emp_id, name, password, salt, leave_available, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (emp_id, details["name"], hashed, salt, details["leave_available"], details["role"]))
        conn.commit()

def verification(emp_id: str, password: str):
    """
    Returns tuple (emp_id, name, leave_available, role) on success, else None.
    Fixed column ordering and validation.
    """
    if not emp_id or not password:
        return None
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # select columns in known order: name, password, salt, leave_available, role
        cursor.execute("SELECT name, password, salt, leave_available, role FROM employees WHERE emp_id = ?", (emp_id,))
        result = cursor.fetchone()
        if result:
            name, stored_hash, stored_salt, leave_available, role = result
            try:
                hashed, _ = hash_password(password, stored_salt)
            except Exception:
                return None
            if hashed == stored_hash:
                return emp_id, name, leave_available, role
    return None

# ---------- GUI APP ----------
class ClockedInApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ClockedIn Outsourcing Suite")
        self.root.geometry("600x450")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        ctk.set_window_scaling(1.5)
        ctk.set_widget_scaling(1.5)


        self.show_login()

    # ---------- LOGIN ----------
    def show_login(self):
        self.clear_window()

        frame = ctk.CTkFrame(self.root, corner_radius=15)
        frame.pack(pady=60, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text=f"{random.choice(greeting)}", font=("Lucida Grande", 22, "bold"),
                     text_color="#27823f").pack(pady=(15, 5))
        ctk.CTkLabel(frame, text="Welcome to ClockedIn HR Suite", font=("Lucida Grande", 16),
                     text_color="grey").pack(pady=(0, 20))

        ctk.CTkLabel(frame, text="Employee ID:", text_color="#27823f").pack(anchor="w", padx=20)
        self.emp_entry = ctk.CTkEntry(frame, placeholder_text="Enter ID eg. TEST01", text_color="#27823f")
        self.emp_entry.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame, text="Password:", text_color="#27823f").pack(anchor="w", padx=20)
        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Enter Password", show="*", text_color="#27823f")
        self.pass_entry.pack(fill="x", padx=20, pady=5)
        self.show_password_switch = ctk.CTkSwitch(frame, text="Show Password", text_color="#27823f", cursor="hand2",
                                                  font=("Lucida Grande", 11), command=self.toggle_password)
        self.show_password_switch.pack(anchor="w", padx=20, pady=5)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Login", fg_color="#27823f", text_color="white",
                      cursor="hand2", width=120, command=self.login_action).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray", text_color="white",
                      cursor="hand2", width=120, command=self.root.destroy).pack(side="left", padx=10)

    def toggle_password(self):
            if self.show_password_switch.get() == 1:
                self.pass_entry.configure(show="")   
            else:
                self.pass_entry.configure(show="*") 

    def login_action(self):
        emp_id = self.emp_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not emp_id or not password:
            messagebox.showerror("Login Failed", "Please Enter your Employee ID and Password.")
            return
        user_info = verification(emp_id, password)
        if user_info:
            emp_id, name, leave, role = user_info
            if role == Role.MANAGER:
                self.show_manager(emp_id, name, leave, role)
            elif role == Role.ADMIN:
                self.show_admin(emp_id, name, leave, role)
            else:
                self.show_staff(emp_id, name, leave, role)
        else:
            messagebox.showerror("Login Failed", "Invalid Employee ID or Password.")

    # ---------- STAFF ----------
    def show_staff(self, emp_id, name, leave, role):
        self.clear_window()
        
        frame = ctk.CTkFrame(self.root, corner_radius=15)
        frame.pack(pady=60, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text=f"Welcome {name} ({role})", font=("Lucida Grande", 18, "bold"), 
                     text_color="#27823f").pack(pady=(15, 5))
        ctk.CTkLabel(frame, text=f"Leave days available: {leave}", font=("Lucida Grande", 16), 
                     text_color="gray").pack(pady=(0, 20))
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Request Leave", fg_color="#43e06d", 
                      command=lambda: self.request_leave(emp_id)).pack(pady=5)
        ctk.CTkButton(btn_frame, text="View My Requests", fg_color="#43e06d",
                      command=lambda: self.view_requests(emp_id)).pack(pady=5)
        ctk.CTkButton(btn_frame, text="Clear My Requests", fg_color="#e04343",
                      command=lambda: self.clear_requests(emp_id)).pack(pady=5)
        ctk.CTkButton(btn_frame, text="Logout", fg_color="gray", 
                      command=self.show_login).pack(pady=10)

    def clear_requests(self, emp_id):
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT request_id, leave_type, description, days_requested, paid_leave, status
                    FROM leave_requests 
                    WHERE emp_id = ? AND status IN ('Approved','Rejected')
                """, (emp_id,))
                requests = cursor.fetchall()

            if not requests:
                messagebox.showinfo("Clear Requests", "No approved or denied requests to delete.")
                return

            # Create a new popup window
            popup = ctk.CTkToplevel(self.root)
            popup.title("Clear Requests")
            popup.geometry("500x400")

            ctk.CTkLabel(popup, text="Select requests to delete:", font=("Lucida Grande", 14, "bold")).pack(pady=10)

            # Store checkboxes
            check_vars = {}
            for r in requests:
                rid, ltype, desc, days, paid, status = r
                text = f"#{rid} | {ltype} | {days} days | Paid: {'Yes' if paid else 'No'} | Status: {status}"
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(popup, text=text, variable=var)
                cb.pack(anchor="w", padx=20, pady=2)
                check_vars[rid] = var

            def confirm_delete():
                selected_ids = [rid for rid, var in check_vars.items() if var.get()]
                if not selected_ids:
                    messagebox.showwarning("No Selection", "Please select at least one request to delete.")
                    return

                confirm = messagebox.askyesno("Confirm Delete", f"Delete {len(selected_ids)} request(s)?")
                if not confirm:
                    return

                try:
                    with sqlite3.connect(DB_FILE) as conn:
                        cursor = conn.cursor()
                        cursor.executemany("DELETE FROM leave_requests WHERE request_id = ? AND emp_id = ?",
                                        [(rid, emp_id) for rid in selected_ids])
                        conn.commit()
                    messagebox.showinfo("Deleted", f"Deleted {len(selected_ids)} request(s).")
                    popup.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete requests: {e}")

            # Buttons
            ctk.CTkButton(popup, text="Delete Selected", fg_color="#e04343", command=confirm_delete).pack(pady=10)
            ctk.CTkButton(popup, text="Cancel", fg_color="gray", command=popup.destroy).pack()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load requests: {e}")


    def request_leave(self, emp_id):
        leave_type = simpledialog.askstring("Leave Type", "Enter leave type (family/vacation/personal):", parent=self.root)
        if leave_type is None:
            return  # user cancelled application
        leave_type = leave_type.lower().strip()
        if leave_type not in ["family", "vacation", "personal"]:
            messagebox.showerror("Error", "Invalid leave type. Use family, vacation or personal.")
            return

        days = simpledialog.askinteger("Days", "Enter number of days:", parent=self.root, minvalue=1)
        if days is None:
            return

        paid_choice = messagebox.askyesno("Paid Leave?", "Is this paid leave?", parent=self.root)
        description = simpledialog.askstring("Description", "Enter description:", parent=self.root) or ""

        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO leave_requests (emp_id, leave_type, description, days_requested, paid_leave)
                    VALUES (?, ?, ?, ?, ?)
                """, (emp_id, leave_type, description, int(days), 1 if paid_choice else 0))
                conn.commit()
            messagebox.showinfo("Submitted", "Leave request submitted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not submit leave request: {e}")

    def view_requests(self, emp_id):
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT request_id, leave_type, description, days_requested, paid_leave, status
                    FROM leave_requests WHERE emp_id = ?
                """, (emp_id,))
                requests = cursor.fetchall()
            if not requests:
                messagebox.showinfo("My Requests", "No requests.")
                return
            text_lines = []
            for r in requests:
                rid, ltype, desc, days, paid, status = r[0], r[1], r[2] or "", r[3], r[4], r[5]
                text_lines.append(f"#{rid} | {ltype} | {days} days | Paid: {'Yes' if paid else 'No'} | Status: {status}\nDesc: {desc}")
            messagebox.showinfo("My Requests", "\n\n".join(text_lines))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load requests: {e}")

    # MANAGER
    def show_manager(self, emp_id, name, leave, role):
        self.clear_window()
        
        frame = ctk.CTkFrame(self.root, corner_radius=15)
        frame.pack(pady=60, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text=f"Manager Dashboard - {name} ({role})", font=("Arial", 16, "bold"), text_color="#27823f").pack(pady=10)
        ctk.CTkLabel(frame, text=f"Leave days available: {leave}", text_color="gray").pack()

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="View Staff", fg_color="#43e06d", command=self.view_all_staff).pack(pady=5)
        ctk.CTkButton(btn_frame, text="Manage Leave Requests", fg_color="#43e06d", command=self.manage_requests).pack(pady=5)
        ctk.CTkButton(btn_frame, text="Logout", fg_color="gray", command=self.show_login).pack(pady=10)

    def view_all_staff(self):
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT emp_id, name, leave_available, role FROM employees")
                staff = cursor.fetchall()
            if not staff:
                messagebox.showinfo("All Staff", "No staff records.")
                return
            text = "\n".join([f"{s[0]} | {s[1]} | {s[2]} days | Role: {s[3]}" for s in staff])
            messagebox.showinfo("All Staff", text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load staff: {e}")

    def manage_requests(self):
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT request_id, emp_id, leave_type, days_requested, paid_leave, status FROM leave_requests")
                requests = cursor.fetchall()
            if not requests:
                messagebox.showinfo("Requests", "No leave requests.")
                return

            for req in requests:
                req_id, emp_id, ltype, days, paid, status = req
                # Show current status and ask only if pending, otherwise show info
                prompt = f"#{req_id} {emp_id} | {ltype} | {days} days | Paid: {'Yes' if paid else 'No'} | Status: {status}\n\nApprove?"
                if status and status.lower() != "pending":
                    # allow manager to re-decide if desired - show current and ask
                    pass

                choice = messagebox.askquestion("Manage Request", prompt, parent=self.root)
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    if choice == "yes":
                        if paid:
                            # check leave balance first
                            cursor.execute("SELECT leave_available FROM employees WHERE emp_id = ?", (emp_id,))
                            row = cursor.fetchone()
                            if not row:
                                messagebox.showerror("Error", f"Employee {emp_id} not found. Skipping request #{req_id}.")
                                continue
                            current_leave = row[0] or 0
                            if current_leave < days:
                                # can't approve fully — ask whether to partially approve or reject
                                msg = (f"Employee {emp_id} has only {current_leave} days available but request asks for {days} days.\n"
                                       "Approve partial (use available days)?")
                                partial = messagebox.askyesno("Insufficient Leave", msg, parent=self.root)
                                if partial and current_leave > 0:
                                    # deduct what's available and mark approved (and adjust days_requested to amount approved)
                                    cursor.execute("UPDATE employees SET leave_available = 0 WHERE emp_id = ?", (emp_id,))
                                    cursor.execute("UPDATE leave_requests SET status = 'Approved', days_requested = ? WHERE request_id = ?",
                                                   (current_leave, req_id))
                                else:
                                    cursor.execute("UPDATE leave_requests SET status = 'Rejected' WHERE request_id = ?", (req_id,))
                            else:
                                cursor.execute("UPDATE employees SET leave_available = leave_available - ? WHERE emp_id = ?",
                                               (days, emp_id))
                                cursor.execute("UPDATE leave_requests SET status = 'Approved' WHERE request_id = ?", (req_id,))
                        else:
                            # unpaid leave — just approve
                            cursor.execute("UPDATE leave_requests SET status = 'Approved' WHERE request_id = ?", (req_id,))
                    else:
                        cursor.execute("UPDATE leave_requests SET status = 'Rejected' WHERE request_id = ?", (req_id,))
                    conn.commit()
            messagebox.showinfo("Done", "All requests on the system processed.")
        except Exception as e:
            messagebox.showerror("Error", f"Error managing requests: {e}")

    # ---------- ADMIN ----------
    def show_admin(self, emp_id, name, leave, role):
        self.clear_window()
        
        frame = ctk.CTkFrame(self.root, corner_radius=15)
        frame.pack(pady=60, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text=f"Admin Dashboard - {name} ({role})", font=("Arial", 16, "bold"), text_color="#27823f").pack(pady=10)
        ctk.CTkLabel(frame, text=f"Leave days available: {leave}", text_color="gray").pack()

        ctk.CTkButton(frame, text="Add Employee", cursor="hand2", fg_color="#43e06d", command=self.add_employee).pack(pady=5)
        ctk.CTkButton(frame, text="Remove Employee", cursor="hand2", fg_color="#43e06d", command=self.remove_employee).pack(pady=5)
        ctk.CTkButton(frame, text="Update Employee", cursor="hand2", fg_color="#43e06d", command=self.update_employee).pack(pady=5)
        ctk.CTkButton(frame, text="Manage Leave Requests", cursor="hand2", fg_color="#43e06d", command=self.manage_requests).pack(pady=5)
        ctk.CTkButton(frame, text="Logout", cursor="hand2", fg_color="gray", command=self.show_login).pack(pady=10)

    def add_employee(self):
        emp_id = simpledialog.askstring("Employee ID", "Enter new employee ID:", parent=self.root)
        if not emp_id:
            return
        name = simpledialog.askstring("Name", "Enter name:", parent=self.root)
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return
        password = simpledialog.askstring("Password", "Enter password:", show="*", parent=self.root)
        if not password:
            messagebox.showerror("Error", "Password is required.")
            return
        leave = simpledialog.askinteger("Leave", "Enter leave days:", parent=self.root, minvalue=0)
        if leave is None:
            leave = 0
        role = simpledialog.askstring("Role", "Enter role:", parent=self.root) or Role.STAFF

        try:
            hashed, salt = hash_password(password)
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                # prevent accidental overwrite: check existence
                cursor.execute("SELECT 1 FROM employees WHERE emp_id = ?", (emp_id,))
                if cursor.fetchone():
                    overwrite = messagebox.askyesno("Exists", f"Employee {emp_id} exists. Overwrite?", parent=self.root)
                    if not overwrite:
                        return
                cursor.execute("""
                    INSERT OR REPLACE INTO employees (emp_id, name, password, salt, leave_available, role)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (emp_id, name, hashed, salt, int(leave), role))
                conn.commit()
            messagebox.showinfo("Added", f"Employee {name} ({emp_id}) added/updated.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add employee: {e}")

    def remove_employee(self):
        emp_id = simpledialog.askstring("Remove", "Enter employee ID to remove:", parent=self.root)
        if not emp_id:
            return
        confirm = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove {emp_id}?", parent=self.root)
        if not confirm:
            return
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
                deleted = cursor.rowcount
                conn.commit()
            if deleted:
                messagebox.showinfo("Removed", f"Employee {emp_id} removed.")
            else:
                messagebox.showinfo("Not Found", f"No employee with ID {emp_id} found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not remove employee: {e}")

    def update_employee(self):
        emp_id = simpledialog.askstring("Update", "Enter employee ID to update:", parent=self.root)
        if not emp_id:
            return
        field = simpledialog.askstring("Field", "Which field? (name/leave/role/password):", parent=self.root)
        if not field:
            return
        field = field.lower().strip()
        if field not in ("name", "leave", "role", "password"):
            messagebox.showerror("Error", "Field must be one of: name, leave, role, password.")
            return

        if field == "password":
            new_value = simpledialog.askstring("New Value", "Enter new password:", show="*", parent=self.root)
        else:
            new_value = simpledialog.askstring("New Value", "Enter new value:", parent=self.root)

        if new_value is None:
            return

        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                if field == "password":
                    hashed, salt = hash_password(new_value)
                    cursor.execute("UPDATE employees SET password = ?, salt = ? WHERE emp_id = ?",
                                   (hashed, salt, emp_id))
                elif field in ["name", "role"]:
                    cursor.execute(f"UPDATE employees SET {field} = ? WHERE emp_id = ?", (new_value, emp_id))
                elif field == "leave":
                    try:
                        leave_int = int(new_value)
                        if leave_int < 0:
                            raise ValueError("Leave must be >= 0")
                    except Exception:
                        messagebox.showerror("Error", "Leave must be a non-negative integer.")
                        return
                    cursor.execute("UPDATE employees SET leave_available = ? WHERE emp_id = ?", (leave_int, emp_id))
                conn.commit()
            messagebox.showinfo("Updated", f"Employee {emp_id} updated.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update employee: {e}")

    # closes other sub windows opened during program run time 
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# sets up the database and app
if __name__ == "__main__":
    setup_database()
    root = ctk.CTk()
    app = ClockedInApp(root)
    root.mainloop()
