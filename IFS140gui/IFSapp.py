# import requests
# import random
# import customtkinter as ctk
# from tkinter import messagebox, simpledialog

# # After starting server run this in another terminal:
# # python IFS140gui/IFSapp.py

# API_BASE = "http://127.0.0.1:8000"

# greeting = ["Hello", "Hallo", "Sawubona", "Molo", "Thobela",
#             "Lufuno", "Dumela", "Mhoro", "Avuxeni"]

# class ClockedInApp:
#     # App setup
#     def __init__(self, root):
#         self.root = root
#         self.root.title("ClockedIn Outsourcing Suite")
#         self.root.geometry("600x450")
#         ctk.set_appearance_mode("system")
#         ctk.set_default_color_theme("green")
#         ctk.set_window_scaling(1.5)
#         ctk.set_widget_scaling(1.5)

#         self.logged_in = None  # Will be dict with emp_id, name, role, leave
#         self.show_login()

#     # - Start-up login page -
#     def show_login(self):
#         self.clear_window()
        
#         frame = ctk.CTkFrame(self.root, corner_radius=15)
#         frame.pack(pady=60, padx=40, fill="both", expand=True)
        
#         ctk.CTkLabel(frame, text=f"{random.choice(greeting)}", font=("Lucida Grande", 22, "bold"),
#                      text_color="#27823f").pack(pady=(15, 5))
#         ctk.CTkLabel(frame, text="Welcome to ClockedIn HR Suite", font=("Lucida Grande", 16),
#                      text_color="grey").pack(pady=(0, 20))

#         ctk.CTkLabel(frame, text="Employee ID:", text_color="#27823f").pack(anchor="w", padx=20)
#         self.emp_entry = ctk.CTkEntry(frame, placeholder_text="Enter ID eg. TEST01", text_color="#27823f")
#         self.emp_entry.pack(fill="x", padx=20, pady=5)

#         ctk.CTkLabel(frame, text="Password:", text_color="#27823f").pack(anchor="w", padx=20)
#         self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Enter Password", show="*", text_color="#27823f")
#         self.pass_entry.pack(fill="x", padx=20, pady=5)
#         self.show_password_switch = ctk.CTkSwitch(frame, text="Show Password", text_color="#27823f", cursor="hand2",
#                                                   font=("Lucida Grande", 11), command=self.toggle_password)
#         self.show_password_switch.pack(anchor="w", padx=20, pady=5)
        
#         btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
#         btn_frame.pack(pady=15)

#         ctk.CTkButton(btn_frame, text="Login", fg_color="#27823f", text_color="white",
#                       cursor="hand2", width=120, command=self.login_action).pack(side="left", padx=10)
#         ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray", text_color="white",
#                       cursor="hand2", width=120, command=self.root.destroy).pack(side="left", padx=10)

#     def toggle_password(self):
#             if self.show_password_switch.get() == 1:
#                 self.pass_entry.configure(show="")   
#             else:
#                 self.pass_entry.configure(show="*") 

#     def login_action(self):
#         emp_id = self.emp_entry.get().strip()
#         password = self.pass_entry.get().strip()
#         if not emp_id or not password:
#             messagebox.showerror("Login Failed", "Enter both ID and password.")
#             return
#         try:
#             r = requests.post(f"{API_BASE}/login", json={"emp_id": emp_id, "password": password})
#         except Exception as e:
#             messagebox.showerror("Network Error", f"Could not connect to API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Login Failed", r.json().get("detail", "Invalid credentials"))
#             return
#         self.logged_in = r.json()
#         role = self.logged_in.get("role", "")
#         name = self.logged_in.get("name", "")
#         leave = self.logged_in.get("leave", 0)
#         if role.lower() == "manager" or role == "Manager":
#             self.show_manager(self.logged_in["emp_id"], name, leave, role)
#         elif role.lower() == "admin" or role == "Admin":
#             self.show_admin(self.logged_in["emp_id"], name, leave, role)
#         else:
#             self.show_staff(self.logged_in["emp_id"], name, leave, role)

#     # - Staff UI Dashboard -
#     def show_staff(self, emp_id, name, leave, role):
#         self.clear_window()
#         frame = ctk.CTkFrame(self.root, corner_radius=12)
#         frame.pack(padx=30, pady=30, fill="both", expand=True)

#         ctk.CTkLabel(frame, text=f"Welcome {name} ({role})", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=(10,5))
#         ctk.CTkLabel(frame, text=f"Leave days available: {leave}", text_color="gray").pack(pady=(0,10))

#         btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
#         btn_frame.pack(pady=10)

#         ctk.CTkButton(btn_frame, text="Request Leave", command=lambda: self.request_leave(emp_id)).pack(pady=5)
#         ctk.CTkButton(btn_frame, text="View My Requests", command=lambda: self.view_requests(emp_id)).pack(pady=5)
#         ctk.CTkButton(btn_frame, text="Clear My Requests", command=lambda: self.clear_requests(emp_id)).pack(pady=5)
#         ctk.CTkButton(btn_frame, text="Logout", fg_color="gray", command=self.logout).pack(pady=10)

#     def request_leave(self, emp_id):
#         leave_type = simpledialog.askstring("Leave Type", "Enter leave type (family/vacation/personal):", parent=self.root)
#         if leave_type is None:
#             return
#         leave_type = leave_type.lower().strip()
#         if leave_type not in ["family", "vacation", "personal"]:
#             messagebox.showerror("Error", "Invalid leave type.")
#             return
#         days = simpledialog.askinteger("Days", "Enter number of days:", parent=self.root, minvalue=1)
#         if days is None:
#             return
#         paid_choice = messagebox.askyesno("Paid Leave?", "Is this paid leave?", parent=self.root)
#         description = simpledialog.askstring("Description", "Enter description:", parent=self.root) or ""
#         payload = {
#             "emp_id": emp_id,
#             "leave_type": leave_type,
#             "description": description,
#             "days_requested": days,
#             "paid_leave": paid_choice
#         }
#         try:
#             r = requests.post(f"{API_BASE}/leave/request", json=payload)
#         except Exception as e:
#             messagebox.showerror("Network", f"Failed to contact API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Error", r.json().get("message", r.text))
#             return
#         messagebox.showinfo("Submitted", "Leave request submitted successfully.")

#     def view_requests(self, emp_id):
#         try:
#             r = requests.get(f"{API_BASE}/leave/{emp_id}")
#         except Exception as e:
#             messagebox.showerror("Network", f"Failed to contact API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Error", r.text)
#             return
#         rows = r.json()
#         if not rows:
#             messagebox.showinfo("My Requests", "No requests.")
#             return
#         text_lines = []
#         for row in rows:
#             rid, ltype, desc, days, paid, status = row[0], row[1], (row[2] or ""), row[3], row[4], row[5]
#             text_lines.append(f"#{rid} | {ltype} | {days} days | Paid: {'Yes' if paid else 'No'} | Status: {status}\nDesc: {desc}")
#         messagebox.showinfo("My Requests", "\n\n".join(text_lines))

#     def clear_requests(self, emp_id):
#         # get requests that are Approved or Rejected then allow user to select ones to delete
#         try:
#             r = requests.get(f"{API_BASE}/leave/{emp_id}")
#         except Exception as e:
#             messagebox.showerror("Network", f"Failed to contact API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Error", r.text)
#             return
#         rows = r.json()
#         filtered = [row for row in rows if row[5] in ("Approved", "Rejected")]
#         if not filtered:
#             messagebox.showinfo("Clear Requests", "No approved or denied requests to delete.")
#             return

#         popup = ctk.CTkToplevel(self.root)
#         popup.title("Clear Requests")
#         popup.geometry("500x400")
#         ctk.CTkLabel(popup, text="Select requests to delete:", font=("Arial", 13, "bold")).pack(pady=10)

#         check_vars = {}
#         for r in filtered:
#             rid, ltype, desc, days, paid, status = r[0], r[1], (r[2] or ""), r[3], r[4], r[5]
#             text = f"#{rid} | {ltype} | {days} | Paid: {'Yes' if paid else 'No'} | Status: {status}"
#             var = ctk.BooleanVar(value=False)
#             cb = ctk.CTkCheckBox(popup, text=text, variable=var)
#             cb.pack(anchor="w", padx=20, pady=2)
#             check_vars[rid] = var

#         def confirm_delete():
#             selected = [rid for rid, var in check_vars.items() if var.get()]
#             if not selected:
#                 messagebox.showwarning("No Selection", "Select at least one.")
#                 return
#             try:
#                 headers = {"X-Requester-EmpId": self.logged_in["emp_id"]}
#                 r2 = requests.post(f"{API_BASE}/leave/clear", json={"emp_id": emp_id, "request_ids": selected}, headers=headers)
#             except Exception as e:
#                 messagebox.showerror("Network", f"Failed to contact API: {e}")
#                 return
#             if r2.status_code != 200:
#                 messagebox.showerror("Error", r2.text)
#                 return
#             messagebox.showinfo("Deleted", f"Deleted {len(selected)} request(s).")
#             popup.destroy()

#         ctk.CTkButton(popup, text="Delete Selected", fg_color="#e04343", command=confirm_delete).pack(pady=10)
#         ctk.CTkButton(popup, text="Cancel", fg_color="gray", command=popup.destroy).pack()

#     def logout(self):
#         self.logged_in = None
#         self.show_login()

#     # - Manager Dashboard -
#     def show_manager(self, emp_id, name, leave, role):
#         self.clear_window()
#         frame = ctk.CTkFrame(self.root, corner_radius=12)
#         frame.pack(padx=30, pady=30, fill="both", expand=True)
#         ctk.CTkLabel(frame, text=f"Manager Dashboard - {name} ({role})", font=("Arial", 16, "bold"), text_color="#27823f").pack(pady=10)
#         ctk.CTkLabel(frame, text=f"Leave days available: {leave}", text_color="gray").pack()

#         btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
#         btn_frame.pack(pady=15)
#         ctk.CTkButton(btn_frame, text="View Staff", command=self.view_all_staff).pack(pady=5)
#         ctk.CTkButton(btn_frame, text="Manage Leave Requests", command=self.manage_leave_requests).pack(pady=5)
#         ctk.CTkButton(btn_frame, text="Logout", fg_color="gray", command=self.logout).pack(pady=10)

#     def view_all_staff(self):
#         try:
#             r = requests.get(f"{API_BASE}/employees")
#         except Exception as e:
#             messagebox.showerror("Network", f"Failed to contact API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Error", r.text)
#             return
#         rows = r.json()
#         if not rows:
#             messagebox.showinfo("All Staff", "No staff records.")
#             return
#         text = "\n".join([f"{s[0]} | {s[1]} | {s[2]} | Role: {s[3]}" for s in rows])
#         messagebox.showinfo("All Staff", text)

#     def manage_leave_requests(self):
#         # get all requests (requires manager/admin)
#         headers = {"X-Requester-EmpId": self.logged_in["emp_id"]}
#         try:
#             r = requests.get(f"{API_BASE}/leave", headers=headers)
#         except Exception as e:
#             messagebox.showerror("Network", f"Failed to contact API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Error", r.text)
#             return
#         rows = r.json()
#         if not rows:
#             messagebox.showinfo("Requests", "No leave requests.")
#             return

#         # present a simple interactive sequential manager flow (dialog per request) we are looking to innovate this
#         for req in rows:
#             req_id, emp_id, ltype, desc, days, paid, status = req[0], req[1], req[2], (req[3] or ""), req[4], req[5], req[6] if len(req) > 6 else (req[5])
#             # show prompt only for pending, else show and allow to re-decide
#             prompt = f"#{req_id} {emp_id} | {ltype} | {days} days | {desc} | Paid: {'Yes' if paid else 'No'} | Status: {status}\n\nApprove?"
#             choice = messagebox.askquestion("Manage Request", prompt, parent=self.root)
#             if choice == "yes":
#                 # approve
#                 try:
#                     r2 = requests.put(f"{API_BASE}/leave/{req_id}/approve", headers=headers)
#                     if r2.status_code != 200:
#                         messagebox.showerror("Error", r2.text)
#                 except Exception as e:
#                     messagebox.showerror("Network", f"Failed to contact API: {e}")
#             else:
#                 try:
#                     r2 = requests.put(f"{API_BASE}/leave/{req_id}/deny", headers=headers)
#                     if r2.status_code != 200:
#                         messagebox.showerror("Error", r2.text)
#                 except Exception as e:
#                     messagebox.showerror("Network", f"Failed to contact API: {e}")
#         messagebox.showinfo("Done", "All requests processed (you were prompted for each).")

#     # - Admin Dashboard -
#     def show_admin(self, emp_id, name, leave, role):
#         self.clear_window()
#         frame = ctk.CTkFrame(self.root, corner_radius=12)
#         frame.pack(padx=30, pady=30, fill="both", expand=True)
#         ctk.CTkLabel(frame, text=f"Admin Dashboard - {name} ({role})", font=("Arial", 16, "bold"), text_color="#27823f").pack(pady=10)
#         ctk.CTkLabel(frame, text=f"Leave days available: {leave}", text_color="gray").pack()

#         ctk.CTkButton(frame, text="Add Employee", command=self.add_employee).pack(pady=5)
#         ctk.CTkButton(frame, text="Remove Employee", command=self.remove_employee).pack(pady=5)
#         ctk.CTkButton(frame, text="Update Employee", command=self.update_employee).pack(pady=5)
#         ctk.CTkButton(frame, text="Manage Leave Requests", command=self.manage_leave_requests).pack(pady=5)
#         ctk.CTkButton(frame, text="Logout", fg_color="gray", command=self.logout).pack(pady=10)

#     def add_employee(self):
#         emp_id = simpledialog.askstring("Employee ID", "Enter new employee ID:", parent=self.root)
#         if not emp_id:
#             return
#         name = simpledialog.askstring("Name", "Enter name:", parent=self.root)
#         if not name:
#             messagebox.showerror("Error", "Name is required.")
#             return
#         password = simpledialog.askstring("Password", "Enter password:", show="*", parent=self.root)
#         if not password:
#             messagebox.showerror("Error", "Password is required.")
#             return
#         leave = simpledialog.askinteger("Leave", "Enter leave days:", parent=self.root, minvalue=0)
#         if leave is None:
#             leave = 0
#         role = simpledialog.askstring("Role", "Enter role:", parent=self.root) or "Staff"

#         payload = {"emp_id": emp_id, "name": name, "password": password, "role": role, "leave_available": leave}
#         headers = {"X-Requester-EmpId": self.logged_in["emp_id"]}
#         try:
#             r = requests.post(f"{API_BASE}/employees", json=payload, headers=headers)
#         except Exception as e:
#             messagebox.showerror("Network", f"Failed to contact API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Error", r.text)
#             return
#         messagebox.showinfo("Added", f"Employee {name} ({emp_id}) added.")

#     def remove_employee(self):
#         emp_id = simpledialog.askstring("Remove", "Enter employee ID to remove:", parent=self.root)
#         if not emp_id:
#             return
#         confirm = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove {emp_id}?", parent=self.root)
#         if not confirm:
#             return
#         headers = {"X-Requester-EmpId": self.logged_in["emp_id"]}
#         try:
#             r = requests.delete(f"{API_BASE}/employees/{emp_id}", headers=headers)
#         except Exception as e:
#             messagebox.showerror("Network", f"Failed to contact API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Error", r.text)
#             return
#         messagebox.showinfo("Removed", f"Employee {emp_id} removed.")

#     def update_employee(self):
#         emp_id = simpledialog.askstring("Update", "Enter employee ID to update:", parent=self.root)
#         if not emp_id:
#             return
#         field = simpledialog.askstring("Field", "Which field? (name/leave/role/password):", parent=self.root)
#         if not field:
#             return
#         field = field.lower().strip()
#         if field not in ("name", "leave", "role", "password"):
#             messagebox.showerror("Error", "Field must be one of: name, leave, role, password.")
#             return
#         if field == "password":
#             new_value = simpledialog.askstring("New Value", "Enter new password:", show="*", parent=self.root)
#         else:
#             new_value = simpledialog.askstring("New Value", "Enter new value:", parent=self.root)
#         if new_value is None:
#             return
#         headers = {"X-Requester-EmpId": self.logged_in["emp_id"]}
#         payload = {"field": field, "value": new_value}
#         try:
#             r = requests.put(f"{API_BASE}/employees/{emp_id}", json=payload, headers=headers)
#         except Exception as e:
#             messagebox.showerror("Network", f"Failed to contact API: {e}")
#             return
#         if r.status_code != 200:
#             messagebox.showerror("Error", r.text)
#             return
#         messagebox.showinfo("Updated", f"Employee {emp_id} updated.")

#     def clear_window(self):
#         for w in self.root.winfo_children():
#             w.destroy()

# if __name__ == "__main__":
#     root = ctk.CTk()
#     app = ClockedInApp(root)
#     root.mainloop()

# IFS140gui/IFSapp.py
import customtkinter as ctk
from tkinter import messagebox, Listbox, END, SINGLE, Scrollbar, RIGHT, Y
import requests
import random

API_URL = "http://127.0.0.1:8000"

greetings = ["Hello", "Sawubona", "Molo", "Dumela", "Hallo", "Thobela", "Lufuno", "Mhoro", "Avuxeni"]

# ------------------ GUI CLASS ------------------ #
class IFSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ClockedIn HR Suite")
        self.root.geometry("600x450")
        ctk.set_window_scaling(1.5)
        ctk.set_widget_scaling(1.5)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        self.user_data = {}
        self.show_login()

    # WINDOW HELPERS 
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def api_post(self, endpoint, data=None):
        try:
            res = requests.post(f"{API_URL}{endpoint}", json=data)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not reach server:\n{e}")
            return None

    def api_get(self, endpoint):
        try:
            res = requests.get(f"{API_URL}{endpoint}")
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not reach server:\n{e}")
            return None

    def api_delete(self, endpoint, data=None):
        try:
            res = requests.delete(f"{API_URL}{endpoint}", json=data)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not reach server:\n{e}")
            return None
        
    # LOGIN SCREEN
    def show_login(self):
        self.clear_window()
        
        frame = ctk.CTkFrame(self.root, corner_radius=15)
        frame.pack(pady=60, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text=f"{random.choice(greetings)}", font=("Lucida Grande", 22, "bold"),
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
                      cursor="hand2", width=120, command=self.login_user).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray", text_color="white",
                      cursor="hand2", width=120, command=self.root.destroy).pack(side="left", padx=10)

    def toggle_password(self):
            if self.show_password_switch.get() == 1:
                self.pass_entry.configure(show="")   
            else:
                self.pass_entry.configure(show="*")
    
    def login_user(self):
        emp_id = self.emp_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not emp_id or not password:
            messagebox.showwarning("Missing Info", "Please enter both ID and password.")
            return

        res = self.api_post("/login", {"emp_id": emp_id, "password": password})
        if not res or res.get("status") != "success":
            messagebox.showerror("Login Failed", "Invalid ID or password.")
            return

        self.user_data = res
        role = res.get("role")
        if role in ("Admin", "Manager"):
            self.show_admin_dashboard()
        else:
            self.show_staff_dashboard()

    # ---------- STAFF DASHBOARD ---------- #
    def show_staff_dashboard(self):
        self.clear_window()
        name = self.user_data.get("name", "User")
        emp_id = self.user_data.get("emp_id")
        days = self.user_data.get("leave_available", 0)

        ctk.CTkLabel(
            self.root,
            text=f"Welcome {name}! ({emp_id})",
            font=("Lucida Grande", 18, "bold"),
            text_color="#27823f",
        ).pack(pady=15)

        ctk.CTkLabel(
            self.root,
            text=f"Leave Days Available: {days}",
            font=("Lucida Grande", 14), 
            text_color="#27823f"
        ).pack(pady=5)
        
        btn_frame = ctk.CTkFrame(self.root, corner_radius=10)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Request Leave", command=self.show_leave_form).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="View My Requests", command=self.show_my_requests).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Logout", command=self.show_login).grid(row=1, column=0, columnspan=2, pady=15)

    def show_leave_form(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Submit Leave Request", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=20)

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10, padx=20, fill="both")

        self.leave_type = ctk.CTkEntry(frame, placeholder_text="Leave Type")
        self.leave_desc = ctk.CTkEntry(frame, placeholder_text="Description (optional)")
        self.leave_days = ctk.CTkEntry(frame, placeholder_text="Days Requested")
        self.leave_paid = ctk.CTkSwitch(frame, text="Paid Leave")

        for w in (self.leave_type, self.leave_desc, self.leave_days, self.leave_paid):
            w.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(frame, text="Submit", command=self.submit_leave).pack(pady=20)
        ctk.CTkButton(frame, text="Back", command=self.show_staff_dashboard).pack()

    def submit_leave(self):
        emp_id = self.user_data.get("emp_id")
        data = {
            "emp_id": emp_id,
            "leave_type": self.leave_type.get().strip(),
            "description": self.leave_desc.get().strip(),
            "days": int(self.leave_days.get() or 0),
            "paid_leave": 1 if self.leave_paid.get() else 0,
        }
        res = self.api_post("/leave/submit", data)
        if res and res.get("status") == "success":
            messagebox.showinfo("Success", "Leave request submitted.")
            self.show_staff_dashboard()

    def show_my_requests(self):
        emp_id = self.user_data.get("emp_id")
        res = self.api_get(f"/leave/view/{emp_id}")
        self.clear_window()
        ctk.CTkLabel(self.root, text="My Leave Requests", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=20)

        frame = ctk.CTkScrollableFrame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        for r in res.get("requests", []):
            req_id, ltype, desc, days, paid, status = r
            ctk.CTkLabel(
                frame,
                text=f"#{req_id} | {ltype} | {days} days | {'Paid' if paid else 'Unpaid'} | {status}\n{desc or ''}",
                anchor="w",
                justify="left",
            ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.root, text="Back", command=self.show_staff_dashboard).pack(pady=10)

    # ADMIN/MANAGER DASHBOARD
    def show_admin_dashboard(self):
        self.clear_window()
        name = self.user_data.get("name", "Admin")
        days = self.user_data.get("leave_available", 0)
        frame = ctk.CTkFrame(self.root, corner_radius=15)
        frame.pack(pady=60, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text=f"Welcome {name}", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=15)
        ctk.CTkLabel(frame, text=f"Leave days available: {days}", text_color="gray").pack()
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="View All Requests", command=self.manage_leave_requests).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="View All Staff", command=self.show_all_staff).grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Add Employee", command=self.show_add_employee_form).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Remove Employee", command=self.show_remove_employee_form).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Update Employee", command=self.show_update_employee_form).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Logout", fg_color="#27823f", command=self.show_login).grid(row=2, column=0, columnspan=3, pady=10)

        # # Variables
        # self.emp_id_var = ctk.StringVar()
        # self.name_var = ctk.StringVar()
        # self.pass_var = ctk.StringVar()
        # self.leave_var = ctk.StringVar()
        # self.role_var = ctk.StringVar()

        # # Left: list area (tk.Listbox for selection events)
        # left_frame = ctk.CTkFrame(self.root, width=290)
        # left_frame.pack(side="left", fill="y", padx=12, pady=12)

        # ctk.CTkLabel(left_frame, text="Employees").pack(anchor="w", padx=6, pady=(4,0))

        # # Use tk.Listbox for easy selection binding
        # self.lb = Listbox(left_frame, width=46, height=25, selectmode=SINGLE)
        # self.lb.pack(side="left", fill="y", padx=(6,0), pady=6)
        # self.lb.bind("<<ListboxSelect>>", self.on_list_select)

        # scrollbar = Scrollbar(left_frame, orient="vertical", command=self.lb.yview)
        # scrollbar.pack(side=RIGHT, fill=Y)
        # self.lb.configure(yscrollcommand=scrollbar.set)

        # ctk.CTkButton(left_frame, text="Reload", command=self.load_employees).pack(pady=(6,4), padx=6, anchor="w")

        # # Right: form
        # right = ctk.CTkFrame(self.root)
        # right.pack(side="left", fill="both", expand=True, padx=12, pady=12)
        # right.grid_columnconfigure(0, weight=1)

        # ctk.CTkLabel(right, text="emp_id (for update/delete)").grid(row=0, column=0, sticky="w", padx=6, pady=(6,0))
        # ctk.CTkEntry(right, textvariable=self.emp_id_var).grid(row=1, column=0, sticky="ew", padx=6)

        # ctk.CTkLabel(right, text="Name").grid(row=2, column=0, sticky="w", padx=6, pady=(8,0))
        # ctk.CTkEntry(right, textvariable=self.name_var).grid(row=3, column=0, sticky="ew", padx=6)

        # ctk.CTkLabel(right, text="Password").grid(row=4, column=0, sticky="w", padx=6, pady=(8,0))
        # ctk.CTkEntry(right, textvariable=self.pass_var, show="*").grid(row=5, column=0, sticky="ew", padx=6)

        # ctk.CTkLabel(right, text="Leave available").grid(row=6, column=0, sticky="w", padx=6, pady=(8,0))
        # ctk.CTkEntry(right, textvariable=self.leave_var).grid(row=7, column=0, sticky="ew", padx=6)

        # ctk.CTkLabel(right, text="Role").grid(row=8, column=0, sticky="w", padx=6, pady=(8,0))
        # ctk.CTkEntry(right, textvariable=self.role_var).grid(row=9, column=0, sticky="ew", padx=6)

        # # Buttons
        # btn_row = ctk.CTkFrame(right)
        # btn_row.grid(row=10, column=0, pady=12, sticky="ew", padx=6)
        # ctk.CTkButton(btn_row, text="Add", command=self.add_employee).pack(side="left", padx=6)
        # ctk.CTkButton(btn_row, text="Update", command=self.update_employee).pack(side="left", padx=6)
        # ctk.CTkButton(btn_row, text="Remove", command=self.remove_employee).pack(side="left", padx=6)
        # ctk.CTkButton(btn_row, text="Clear", command=self.clear_form).pack(side="left", padx=6)

        # # Load initial employees
        # self.load_employees()
        
    def manage_leave_requests(self):
        res = self.api_get("/leave/view_all")
        self.clear_window()
        ctk.CTkLabel(self.root, text="Manage Leave Requests", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=20)

        frame = ctk.CTkScrollableFrame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        for r in res.get("requests", []):
            req_id, emp_id, ltype, desc, days, paid, status = r
            text = f"#{req_id} | {emp_id} | {ltype} | {days} days | {'Paid' if paid else 'Unpaid'} | {status}\n{desc or ''}"

            item_frame = ctk.CTkFrame(frame)
            item_frame.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(item_frame, text=text, anchor="w", justify="left").pack(side="left", padx=5)
            if status == "Pending":
                ctk.CTkButton(item_frame, text="Approve", width=70, command=lambda r=req_id: self.approve_request(r)).pack(side="right", padx=2)
                ctk.CTkButton(item_frame, text="Deny", width=70, command=lambda r=req_id: self.deny_request(r)).pack(side="right", padx=2)

        ctk.CTkButton(self.root, text="Back", command=self.show_admin_dashboard).pack(pady=10)

    def approve_request(self, request_id):
        res = self.api_post(f"/leave/approve/{request_id}")
        if res and res.get("status") == "success":
            messagebox.showinfo("Success", "Request approved.")
            self.manage_leave_requests()

    def deny_request(self, request_id):
        res = self.api_post(f"/leave/deny/{request_id}")
        if res and res.get("status") == "success":
            messagebox.showinfo("Success", "Request denied.")
            self.manage_leave_requests()

    def show_all_staff(self):
        res = self.api_get("/staff/all")
        self.clear_window()
        ctk.CTkLabel(self.root, text="All Staff Members", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=20)

        frame = ctk.CTkScrollableFrame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        for e in res.get("employees", []):
            emp_id, name, leave_avail, role = e
            ctk.CTkLabel(
                frame,
                text=f"{emp_id} | {name} | {leave_avail} days left | {role}",
                anchor="w",
                justify="left",
            ).pack(fill="x", padx=10, pady=3)

        ctk.CTkButton(self.root, text="Back", command=self.show_admin_dashboard).pack(pady=10)
    
    def show_add_employee_form(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Add New Employee", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=20)

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10, padx=20, fill="both")

        self.new_emp_id = ctk.CTkEntry(frame, placeholder_text="Employee ID")
        self.new_emp_name = ctk.CTkEntry(frame, placeholder_text="Name")
        self.new_emp_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.new_emp_role = ctk.CTkEntry(frame, placeholder_text="Role")
        self.new_emp_leave = ctk.CTkEntry(frame, placeholder_text="Leave Available")

        for w in (self.new_emp_id, self.new_emp_name, self.new_emp_password, self.new_emp_role, self.new_emp_leave):
            w.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(frame, text="Submit", command=self.submit_add_employee).pack(pady=20)
        ctk.CTkButton(frame, text="Back", command=self.show_admin_dashboard).pack()
    
    def submit_add_employee(self):
        data = {
            "emp_id": self.new_emp_id.get().strip(),
            "name": self.new_emp_name.get().strip(),
            "password": self.new_emp_password.get().strip(),
            "role": self.new_emp_role.get().strip(),
            "leave_available": int(self.new_emp_leave.get().strip() or 0),
        }
        res = self.api_post("/employees/add", data)
        if res and res.get("status") == "success":
            messagebox.showinfo("Success", "New employee added.")
            self.show_staff_dashboard()
        
    def show_update_employee_form(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Update Employee", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=20)

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10, padx=20, fill="both")

        self.update_emp_id = ctk.CTkEntry(frame, placeholder_text="Employee ID")
        self.update_emp_name = ctk.CTkEntry(frame, placeholder_text="New Name (leave blank to skip)")
        self.update_emp_password = ctk.CTkEntry(frame, placeholder_text="New Password (leave blank to skip)", show="*")
        self.update_emp_role = ctk.CTkEntry(frame, placeholder_text="New Role (leave blank to skip)")
        self.update_emp_leave = ctk.CTkEntry(frame, placeholder_text="New Leave Available (leave blank to skip)")

        for w in (self.update_emp_id, self.update_emp_name, self.update_emp_password, self.update_emp_role, self.update_emp_leave):
            w.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(frame, text="Submit", command=self.submit_update_employee).pack(pady=20)
        ctk.CTkButton(frame, text="Back", command=self.show_admin_dashboard).pack()
    
    def submit_update_employee(self):
        data = {
            "emp_id": self.update_emp_id.get().strip(),
            "name": self.update_emp_name.get().strip(),
            "password": self.update_emp_password.get().strip(),
            "role": self.update_emp_role.get().strip(),
            "leave_available": self.update_emp_leave.get().strip(),
            }
        res = self.api_post("/employees/update", data)
        if res and res.get("status") == "success":
            messagebox.showinfo("Success", "Employee updated.")
            self.show_staff_dashboard()
    
    def show_remove_employee_form(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Remove Employee", font=("Lucida Grande", 18, "bold"), text_color="#27823f").pack(pady=20)

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10, padx=20, fill="both")

        self.remove_emp_id = ctk.CTkEntry(frame, placeholder_text="Employee ID to Remove")
        self.remove_emp_id.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(frame, text="Submit", command=self.submit_remove_employee).pack(pady=20)
        ctk.CTkButton(frame, text="Back", command=self.show_admin_dashboard).pack()
    
    def submit_remove_employee(self):
        data = {
            "employee_id": self.remove_emp_id.get().strip(),
        }
        res = self.api_delete("/employees/remove", data)
        if res and res.get("status") == "success":
            messagebox.showinfo("Success", "New employee added.")
            self.show_staff_dashboard()

    def load_employees(self):
        try:
            r = requests.get("/employees")
            r.raise_for_status()
            employees = r.json()
            self.lb.delete(0, END)
            for e in employees:
                
                line = f"{e['emp_id']:>4} | {e['name']} | leave:{e['leave_available']} | role:{e['role']}"
                self.lb.insert(END, line)
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to load employees:\n{ex}")

    def on_list_select(self, event):
        # Called when user selects an employee line in the listbox.
        try:
            sel = self.lb.curselection()
            if not sel:
                return
            index = sel[0]
            line = self.lb.get(index)
            # Expecting format " 123 | Name | leave:10 | role:Role"
            emp_id_str = line.split("|", 1)[0].strip()
            try:
                emp_id = int(emp_id_str)
            except ValueError:
                return
            # Fetch single employee from API (ensures latest and gets all fields)
            r = requests.get(f"/employees/{emp_id}")
            if r.status_code == 200:
                e = r.json()
                self.fill_form_from_employee(e)
            else:
                # if not found, remove from list and inform
                messagebox.showwarning("Warning", f"Employee {emp_id} not found (refreshing list).")
                self.load_employees()
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to load selected employee:\n{ex}")

    def fill_form_from_employee(self, e: dict):
        """Populate form fields from an employee dict."""
        self.emp_id_var.set(str(e.get("emp_id", "")))
        self.name_var.set(e.get("name", ""))
        # For security, we won't display password; leave password blank for update (only set if user wants to change)
        self.pass_var.set("")  
        self.leave_var.set(str(e.get("leave_available", "")))
        self.role_var.set(e.get("role", ""))

    def add_employee(self):
        payload = {
            "name": self.name_var.get().strip(),
            "password": self.pass_var.get().strip(),
            "leave_available": int(self.leave_var.get() or 0),
            "role": self.role_var.get().strip()
        }
        if not payload["name"] or not payload["password"] or not payload["role"]:
            messagebox.showerror("Validation", "Name, Password and Role are required to add")
            return
        try:
            r = requests.post(f"/employees", json=payload)
            r.raise_for_status()
            messagebox.showinfo("Success", "Employee added")
            self.clear_form()
            self.load_employees()
        except requests.exceptions.HTTPError:
            try:
                details = r.json().get("detail", r.text)
            except:
                details = str(r.text)
            messagebox.showerror("API Error", details)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def update_employee(self):
        emp_id_text = self.emp_id_var.get().strip()
        if not emp_id_text:
            messagebox.showerror("Validation", "emp_id is required for update (select an employee or enter id)")
            return
        try:
            emp_id = int(emp_id_text)
        except ValueError:
            messagebox.showerror("Validation", "emp_id must be an integer")
            return

        payload = {}
        if self.name_var.get().strip(): payload["name"] = self.name_var.get().strip()
        if self.pass_var.get().strip(): payload["password"] = self.pass_var.get().strip()
        if self.leave_var.get().strip():
            try:
                payload["leave_available"] = int(self.leave_var.get().strip())
            except:
                messagebox.showerror("Validation", "leave_available must be an integer")
                return
        if self.role_var.get().strip(): payload["role"] = self.role_var.get().strip()

        if not payload:
            messagebox.showerror("Validation", "Provide at least one field to update")
            return

        try:
            r = requests.put(f"/employees/{emp_id}", json=payload)
            r.raise_for_status()
            messagebox.showinfo("Success", "Employee updated")
            self.clear_form()
            self.load_employees()
        except requests.exceptions.HTTPError:
            try:
                details = r.json().get("detail", r.text)
            except:
                details = str(r.text)
            messagebox.showerror("API Error", details)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def remove_employee(self):
        emp_id_text = self.emp_id_var.get().strip()
        if not emp_id_text:
            messagebox.showerror("Validation", "emp_id required for delete (select an employee or enter id)")
            return
        try:
            emp_id = int(emp_id_text)
        except ValueError:
            messagebox.showerror("Validation", "emp_id must be an integer")
            return

        if not messagebox.askyesno("Confirm", f"Delete employee {emp_id}?"):
            return
        try:
            r = requests.delete(f"/employees/{emp_id}")
            if r.status_code in (200, 204):
                messagebox.showinfo("Deleted", "Employee removed")
                self.clear_form()
                self.load_employees()
            else:
                # If API returns error, show its message
                try:
                    details = r.json().get("detail", r.text)
                except:
                    details = r.text
                messagebox.showerror("API Error", details)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def clear_form(self):
        self.emp_id_var.set("")
        self.name_var.set("")
        self.pass_var.set("")
        self.leave_var.set("")
        self.role_var.set("")

# ------------------ RUN ------------------ #
if __name__ == "__main__":
    root = ctk.CTk()
    app = IFSApp(root)
    root.mainloop()
