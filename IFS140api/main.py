# from fastapi import FastAPI, HTTPException, Header
# from pydantic import BaseModel
# from typing import List, Optional
# from IFS140backend.IFSdb import setup_database, get_conn
# from IFS140backend import IFSservices
# from IFS140backend.IFSroles import Role 

# # Setup configuration, the two commands in the terminal to run the live server
# # these two lines can be used to activate the API
# # uvicorn IFS140api.main:app --reload
# # python -m uvicorn IFS140api.main:app --reload --app-dir /home/kgas/code/python

# # then paste this into the terminal to run the APP
# # python IFS140gui/IFSapp.py

# #API_URL = "http://127.0.0.1:8000"

# # class Role:
# #     MANAGER = "Manager"
# #     ADMIN = "Admin"
# #     STAFF = "Staff"

# app = FastAPI(title="ClockedIn API")

# class Login_Request(BaseModel):
#     emp_id: str
#     password: str
    
# class EmployeeCreate(BaseModel):
#     emp_id: str
#     name: str
#     password: str
#     role: str
#     leave_available: Optional[int] = 0

# class EmployeeUpdate(BaseModel):
#     field: str   
#     value: str

# class Leave_Request(BaseModel):
#     emp_id: str
#     leave_type: str
#     days_requested: int
#     description: Optional[str] = ""
#     paid_leave: bool = True

# def get_role(emp_id: str) -> Optional[str]:
#     with get_conn() as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT role FROM employees WHERE emp_id = ?", (emp_id,))
#         r = cur.fetchone()
#         return r[0] if r else None

# def require_role(requester_emp_id: str, allowed_roles: List[str]):
#     if not requester_emp_id:
#         raise HTTPException(status_code=401, detail="Missing requester header (X-Requester-EmpId)")
#     role = get_role(requester_emp_id)
#     if not role or role not in allowed_roles:
#         raise HTTPException(status_code=403, detail="Insufficient permissions")
    
# @app.on_event("startup")
# def startup():
#     setup_database()

# # ------ routes ------
# @app.post("/login")
# def login(data: Login_Request):
#     u = IFSservices.verification(data.emp_id, data.password)
#     if not u:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return u

# @app.get("/employees")
# def all_employees():
#     return IFSservices.view_all_staff()

# @app.post("/employees")
# def add_employee(data: Employee_Create, x_requester_empid: Optional[str] = Header(None, alias="X-Requester-EmpId")):
#     # allow only Admin or Manager to add employees
#     require_role(x_requester_empid, ["Admin", "Manager"] if False else ["Admin", "Manager"])
#     return IFSservices.add_employee(data.emp_id, data.name, data.password, data.role, data.leave_available)

# @app.delete("/employees/{emp_id}")
# def delete_employee(emp_id: str, x_requester_empid: Optional[str] = Header(None, alias="X-Requester-EmpId")):
#     require_role(x_requester_empid, ["Admin", "Manager"])
#     return IFSservices.remove_employee(emp_id)

# @app.put("/employees/{emp_id}")
# def edit_employee(emp_id: str, data: Employee_Update, x_requester_empid: Optional[str] = Header(None, alias="X-Requester-EmpId")):
#     require_role(x_requester_empid, ["Admin", "Manager"])
#     return IFSservices.update_employee(emp_id, data.field, data.value)

# # Leave routes
# @app.post("/leave/request")
# def create_leave_request(data: Leave_Request):
#     return IFSservices.request_leave(data.emp_id, data.leave_type, data.description, data.days_requested, data.paid_leave)

# @app.get("/leave/{emp_id}")
# def get_your_requests(emp_id: str):
#     return IFSservices.view_your_requests(emp_id)

# @app.get("/leave")
# def all_leave_requests(x_requester_empid: Optional[str] = Header(None, alias="X-Requester-EmpId")):
#     require_role(x_requester_empid, ["Manager", "Admin"])
#     return IFSservices.manage_leave_requests()

# @app.put("/leave/{request_id}/approve")
# def approve(request_id: int, x_requester_empid: Optional[str] = Header(None, alias="X-Requester-EmpId")):
#     require_role(x_requester_empid, ["Manager", "Admin"])
#     return IFSservices.approve_request(request_id)

# @app.put("/leave/{request_id}/deny")
# def deny(request_id: int, x_requester_empid: Optional[str] = Header(None, alias="X-Requester-EmpId")):
#     require_role(x_requester_empid, ["Manager", "Admin"])
#     return IFSservices.deny_request(request_id)

# @app.post("/leave/clear")
# def clear_requests(emp_id: str, request_ids: List[int], x_requester_empid: Optional[str] = Header(None, alias="X-Requester-EmpId")):
#     # allow the employee themselves or admin/manager to clear their completed requests
#     if x_requester_empid != emp_id:
#         require_role(x_requester_empid, ["Manager", "Admin"])
#     return IFSservices.clear_requests(emp_id, request_ids)

# IFS140api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from IFS140backend.IFSdb import setup_database
from IFS140backend import IFSservices as services

app = FastAPI(title="IFS140 Leave Management API")


# ------------------ Models ------------------ #
class LoginRequest(BaseModel):
    emp_id: str
    password: str


class LeaveRequest(BaseModel):
    emp_id: str
    leave_type: str
    description: str
    days: int
    paid_leave: int

# class EmployeeCreate(BaseModel):
#     emp_id: str
#     name: str
#     password: str
#     role: str
#     leave_available: Optional[int]

# class EmployeeUpdate(BaseModel):
#     emp_id: str
#     name: Optional[str] = None
#     password: Optional[str] = None
#     role: Optional[str] = None
#     leave_available: Optional[int] = None
    
# class EmployeeDelete(BaseModel):
#     emp_id: str

class EmployeeBase(BaseModel):
    name: str = Field(..., example="Kaleb")
    password: str = Field(..., example="SecurePass123")
    leave_available: int = Field(..., example=20)
    role: str = Field(..., example="Staff")

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    leave_available: Optional[int] = None
    role: Optional[str] = None

class EmployeeOut(EmployeeBase):
    emp_id: int

# ------------------ Startup ------------------ #
@app.on_event("startup")
def startup_event():
    setup_database()


# ------------------ Auth ------------------ #
@app.post("/login")
def login(data: LoginRequest):
    user = services.authenticate_user(data.emp_id, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    name, role = user
    return {"status": "success", "emp_id": data.emp_id, "name": name, "role": role, "leave_available": services.get_leave_balance(data.emp_id)}


# ------------------ Leave Requests ------------------ #
@app.post("/leave/submit")
def submit_leave(data: LeaveRequest):
    ok = services.submit_leave_request(data.emp_id, data.leave_type, data.description, data.days, data.paid_leave)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to submit leave request")
    return {"status": "success", "message": "Leave request submitted"}


@app.get("/leave/view/{emp_id}")
def view_my_requests(emp_id: str):
    requests = services.view_leave_requests(emp_id)
    return {"status": "success", "requests": requests}


@app.get("/leave/view_all")
def view_all():
    return {"status": "success", "requests": services.view_all_leave_requests()}


@app.post("/leave/approve/{request_id}")
def approve(request_id: int):
    ok = services.approve_leave_request(request_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Unable to approve request")
    return {"status": "success", "message": "Request approved"}


@app.post("/leave/deny/{request_id}")
def deny(request_id: int):
    ok = services.deny_leave_request(request_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Unable to deny request")
    return {"status": "success", "message": "Request denied"}


@app.get("/staff/all")
def view_staff():
    return {"status": "success", "employees": services.view_all_staff()}

@app.get("/staff", response_model=List[EmployeeOut])
def api_list_employees():
    return services.list_employees()

@app.get("/staff/{emp_id}", response_model=EmployeeOut)
def api_get_employee(emp_id: int):
    emp = services.get_employee(emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.post("/staff", response_model=EmployeeOut, status_code=201)
def api_create_employee(payload: EmployeeCreate):
    created = services.add_employee(payload.name, payload.password, payload.leave_available, payload.role)
    return created

@app.put("/staff/{emp_id}", response_model=EmployeeOut)
def api_update_employee(emp_id: int, payload: EmployeeUpdate):
    updated = services.update_employee(emp_id, payload.name, payload.password, payload.leave_available, payload.role)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@app.delete("/staff/{emp_id}", status_code=204)
def api_delete_employee(emp_id: int):
    ok = services.remove_employee(emp_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None

@app.post("/employees/add", response_model=EmployeeOut, status_code=201)
def legacy_add_employee(payload: EmployeeCreate):
    return api_create_employee(payload)

@app.put("/employees/update/{emp_id}", response_model=EmployeeOut)
def legacy_update_employee(emp_id: int, payload: EmployeeUpdate):
    return api_update_employee(emp_id, payload)