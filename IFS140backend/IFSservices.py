# from typing import Optional, List, Tuple, Any
# from .IFSdb import get_conn, ensure_parent, setup_database, employees_data
# from .IFSroles import Role
# from .IFSsecurity import hash_password

# # - Authentication -

# employees_data

# setup_database()

# def verification(emp_id: str, password: str) -> Optional[dict]:
#     if not emp_id or not password:
#         return None
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT name, password, salt, leave_available, role FROM employees WHERE emp_id = ?", (emp_id,))
#         row = cur.fetchone()
#         if not row:
#             return None
#         name, stored_hash, salt, leave_available, role = row
#         try:
#             hashed, _ = hash_password(password, salt)
#         except Exception:
#             return None
#         if hashed == stored_hash:
#             return {"emp_id": emp_id, "name": name, "leave": leave_available, "role": role}
#     return None



# def login(emp_id: str, password: str):
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT name, password, salt, leave_available, role FROM employees WHERE emp_id = ?", (emp_id,))
#         row = cur.fetchone()
#         if not row:
#             return None
#         name, stored_hash, salt, leave, role = row
#         hashed, _ = hash_password(password, salt)
#         if hashed != stored_hash:
#             return None
#         return {"emp_id": emp_id, "name": name, "leave": leave, "role": role}

# # - Employee Management -
# def add_employee(emp_id: str, name: str, password: str, role: str, leave_available: int = 0) -> dict:
#     hashed, salt = hash_password(password)
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("""
#             INSERT INTO employees (emp_id, name, password, salt, leave_available, role)
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (emp_id, name, hashed, salt, int(leave_available), role))
#         conn.commit()
#     return {"status": "Employee added", "emp_id": emp_id}

# def remove_employee(emp_id: str) -> dict:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
#         conn.commit()
#     return {"status": "Employee removed", "emp_id": emp_id}

# def update_employee(emp_id: str, field: str, value: Any) -> dict:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         if field == "password":
#             hashed, salt = hash_password(str(value))
#             cur.execute("UPDATE employees SET password = ?, salt = ? WHERE emp_id = ?", (hashed, salt, emp_id))
#         elif field == "name":
#             cur.execute("UPDATE employees SET name = ? WHERE emp_id = ?", (str(value), emp_id))
#         elif field == "role":
#             cur.execute("UPDATE employees SET role = ? WHERE emp_id = ?", (str(value), emp_id))
#         elif field == "leave":
#             cur.execute("UPDATE employees SET leave_available = ? WHERE emp_id = ?", (int(value), emp_id))
#         else:
#             return {"status": "error", "message": "Unknown field"}
#         conn.commit()
#     return {"status": "Employee Updated"} 

# # ---------- Leave Management ----------
# def request_leave(emp_id: str, leave_type: str, description: str, days_requested: int, paid_leave: bool) -> dict:
#     days_requested = int(days_requested)
#     with get_conn() as conn:
#         cur = conn.cursor()
#         # makes sure the emploee is on the system 
#         cur.execute("SELECT leave_available FROM employees WHERE emp_id = ?", (emp_id,))
#         r = cur.fetchone()
#         if not r:
#             return {"status": "error", "message": "Employee not found"}
#         leave_available = r[0] or 0
#         if paid_leave and leave_available < days_requested:
#             return {"status": "error", "message": "Insufficient leave balance", "available": leave_available}
#         cur.execute("""
#             INSERT INTO leave_requests (emp_id, leave_type, description, days_requested, paid_leave, status)
#             VALUES (?, ?, ?, ?, ?, 'Pending')
#         """, (emp_id, leave_type, description, days_requested, 1 if paid_leave else 0))
#         # deduct immediately if paid (the UI/manager could later adjust on partial approval as needed)
#         if paid_leave:
#             cur.execute("UPDATE employees SET leave_available = leave_available - ? WHERE emp_id = ?", (days_requested, emp_id))
#         conn.commit()
#     return {"status": "requested"}

# def view_your_requests(emp_id: str) -> List[Tuple]:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT request_id, leave_type, days_requested, description, paid_leave, status FROM leave_requests WHERE emp_id = ?", (emp_id,))
#         return cur.fetchall()

# def view_all_staff() -> List[Tuple]:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT emp_id, name, role, leave_available FROM employees")
#         return cur.fetchall()

# def clear_requests(emp_id: str, request_ids: List[int]) -> dict:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.executemany("DELETE FROM leave_requests WHERE request_id = ? AND emp_id = ?", [(rid, emp_id) for rid in request_ids])
#         deleted = cur.rowcount
#         conn.commit()
#     return {"status": "ok", "deleted": deleted}

# def manage_leave_requests() -> List[Tuple]:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT request_id, emp_id, leave_type, days_requested, description, paid_leave, status FROM leave_requests")
#         return cur.fetchall()

# def approve_leave_request(request_id: int) -> dict:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("UPDATE leave_requests SET status = 'Approved' WHERE request_id = ?", (request_id,))
#         conn.commit()
#     return {"status": "Leave approved", "request_id": request_id}

# def deny_leave_request(request_id: int) -> dict:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("UPDATE leave_requests SET status = 'Denied' WHERE request_id = ?", (request_id,))
#         conn.commit()
#     return {"status": "Leave denied", "request_id": request_id}

import sqlite3
from typing import List, Tuple, Optional, Any, Dict
from .IFSdb import get_conn
from .IFSsecurity import verify_password, hash_password
from tkinter import messagebox, simpledialog

def authenticate_user(emp_id: str, password: str) -> Optional[Tuple[str, str]]:
    """Authenticate user credentials. Returns (name, role) if valid, else None."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, password, salt, role FROM employees WHERE emp_id = ?", (emp_id,))
        row = cur.fetchone()

        if not row:
            return None

        name, stored_hash, salt, role = row
        if verify_password(password, stored_hash, salt):
            return (name, role)
    return None


def get_leave_balance(emp_id: str) -> Optional[int]:
    """Get remaining leave balance for an employee."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT leave_available FROM employees WHERE emp_id = ?", (emp_id,))
        row = cur.fetchone()
        return row[0] if row else None


def submit_leave_request(emp_id: str, leave_type: str, description: str, days: int, paid_leave: int) -> bool:
    """Insert a new leave request into the database."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO leave_requests (emp_id, leave_type, description, days_requested, paid_leave, status)
            VALUES (?, ?, ?, ?, ?, 'Pending')
            """,
            (emp_id, leave_type, description, days, paid_leave),
        )
        conn.commit()
        return cur.rowcount > 0


def view_leave_requests(emp_id: str) -> List[Tuple]:
    """View all leave requests for a specific employee."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT request_id, leave_type, description, days_requested, paid_leave, status
            FROM leave_requests WHERE emp_id = ?
            """,
            (emp_id,),
        )
        return cur.fetchall()


def view_all_leave_requests() -> List[Tuple]:
    """View all leave requests (admin/manager view)."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT request_id, emp_id, leave_type, description, days_requested, paid_leave, status
            FROM leave_requests
            ORDER BY request_id DESC
            """
        )
        return cur.fetchall()


def approve_leave_request(request_id: int) -> bool:
    """Approve a leave request and deduct days from the employee's leave balance."""
    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT emp_id, days_requested, status FROM leave_requests WHERE request_id = ?",
            (request_id,),
        )
        row = cur.fetchone()
        if not row or row[2] == "Approved":
            return False

        emp_id, days_requested, _ = row
        cur.execute("SELECT leave_available FROM employees WHERE emp_id = ?", (emp_id,))
        emp_row = cur.fetchone()

        if not emp_row or emp_row[0] < days_requested:
            return False  # insufficient balance

        new_balance = emp_row[0] - days_requested
        cur.execute("UPDATE employees SET leave_available = ? WHERE emp_id = ?", (new_balance, emp_id))
        cur.execute("UPDATE leave_requests SET status = 'Approved' WHERE request_id = ?", (request_id,))
        conn.commit()
        return True


def deny_leave_request(request_id: int) -> bool:
    """Deny a leave request."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE leave_requests SET status = 'Denied' WHERE request_id = ?", (request_id,))
        conn.commit()
        return cur.rowcount > 0


def view_all_staff() -> List[Tuple]:
    """List all employees and their current leave balances."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT emp_id, name, leave_available, role FROM employees")
        return cur.fetchall()

def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {k: row[k] for k in row.keys()}

def add_employee(name: str, password: str, leave_available: int, role: str) -> Dict[str, Any]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO employees (name, password, leave_available, role) VALUES (?, ?, ?, ?)",
            (name, password, leave_available, role)
        )
        emp_id = cur.lastrowid
        conn.commit()
        cur.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        row = cur.fetchone()
    return row_to_dict(row) if row else {}

def get_employee(emp_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        row = cur.fetchone()
    return row_to_dict(row) if row else None

def list_employees() -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees ORDER BY emp_id")
        rows = cur.fetchall()
    return [row_to_dict(r) for r in rows]

def update_employee(emp_id: int,
                    name: Optional[str] = None,
                    password: Optional[str] = None,
                    leave_available: Optional[int] = None,
                    role: Optional[str] = None) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        existing = cur.fetchone()
        if not existing:
            return None
        new_name = name if name is not None else existing["name"]
        new_password = password if password is not None else existing["password"]
        new_leave = leave_available if leave_available is not None else existing["leave_available"]
        new_role = role if role is not None else existing["role"]

        cur.execute("""
            UPDATE employees
            SET name = ?, password = ?, leave_available = ?, role = ?
            WHERE emp_id = ?
        """, (new_name, new_password, new_leave, new_role, emp_id))
        conn.commit()
        cur.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        row = cur.fetchone()
    return row_to_dict(row) if row else None

def remove_employee(emp_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
        affected = cur.rowcount
        conn.commit()
    return affected > 0

# def add_employee(emp_id: str, name: str, password: str, role: str, leave: int) -> bool:
#         try:
#             hashed, salt = hash_password(password)
#             with get_conn() as conn:
#                 cursor = conn.cursor()
#                 # prevent accidental overwrite: check existence
#                 cursor.execute("SELECT 1 FROM employees WHERE emp_id = ?", (emp_id,))
#                 if cursor.fetchone():
#                     overwrite = messagebox.askyesno("Exists", f"Employee {emp_id} exists. Overwrite?", (emp_id))
#                     if not overwrite:
#                         return
#                 cursor.execute("""
#                     INSERT OR REPLACE INTO employees (emp_id, name, password, salt, leave_available, role)
#                     VALUES (?, ?, ?, ?, ?, ?)
#                 """, (emp_id, name, hashed, salt, int(leave), role))
#                 conn.commit()
#             messagebox.showinfo("Added", f"Employee {name} ({emp_id}) added/updated.")
#         except Exception as e:
#             messagebox.showerror("Error", f"Could not add employee: {e}")

# def remove_employee(self):
#     emp_id = simpledialog.askstring("Remove", "Enter employee ID to remove:", parent=self.root)
#     if not emp_id:
#         return
#     confirm = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove {emp_id}?", parent=self.root)
#     if not confirm:
#         return
#     try:
#         with get_conn() as conn:
#             cursor = conn.cursor()
#             cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
#             deleted = cursor.rowcount
#             conn.commit()
#         if deleted:
#             messagebox.showinfo("Removed", f"Employee {emp_id} removed.")
#         else:
#             messagebox.showinfo("Not Found", f"No employee with ID {emp_id} found.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Could not remove employee: {e}")

# def update_employee(emp_id: str,
#                     name: Optional[str] = None,
#                     password: Optional[str] = None,
#                     role: Optional[str] = None,
#                     leave_available: Optional[int] = None) -> bool: 
#     try:
#         with get_conn() as conn:
#             cursor = conn.cursor()
#             updates = []
#             params = []

#             if name is not None:
#                 updates.append("name = ?")
#                 params.append(name)
#             if password is not None:
#                 hashed, salt = hash_password(password)
#                 updates.append("password = ?")
#                 updates.append("salt = ?")
#                 params.append(hashed)
#                 params.append(salt)
#             if role is not None:
#                 updates.append("role = ?")
#                 params.append(role)
#             if leave_available is not None:
#                 updates.append("leave_available = ?")
#                 params.append(leave_available)

#             if not updates:
#                 return False  # Nothing to update

#             params.append(emp_id)
#             sql = f"UPDATE employees SET {', '.join(updates)} WHERE emp_id = ?"
#             cursor.execute(sql, tuple(params))
#             conn.commit()
#         return cursor.rowcount > 0
#     except Exception as e:
#         messagebox.showerror("Error", f"Could not update employee: {e}")
#         return False
    

#     # try:
#     #     with get_conn() as conn:
#     #         cursor = conn.cursor()
#     #         if field == "password":
#     #             hashed, salt = hash_password(new_value)
#     #             cursor.execute("UPDATE employees SET password = ?, salt = ? WHERE emp_id = ?",
#     #                             (hashed, salt, emp_id))
#     #         elif field in ["name", "role"]:
#     #             cursor.execute(f"UPDATE employees SET {field} = ? WHERE emp_id = ?", (new_value, emp_id))
#     #         elif field == "leave":
#     #             try:
#     #                 leave_int = int(new_value)
#     #                 if leave_int < 0:
#     #                     raise ValueError("Leave must be >= 0")
#     #             except Exception:
#     #                 messagebox.showerror("Error", "Leave must be a non-negative integer.")
#     #                 return
#     #             cursor.execute("UPDATE employees SET leave_available = ? WHERE emp_id = ?", (leave_int, emp_id))
#     #         conn.commit()
#     #     messagebox.showinfo("Updated", f"Employee {emp_id} updated.")
#     # except Exception as e:
#     #     messagebox.showerror("Error", f"Could not update employee: {e}")
