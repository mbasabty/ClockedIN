import os
import hashlib
from getpass import getpass
import stdiomask
# import sqlite3

# Code test guide.
# 1. Choose yes or no , for if you're the manager.
# 2. For Manager login: enter Id(eg. MAN01), for Staff Login: enter Id(eg. KGAS01).
# 3. Enter respective password for login Id chosen, Password will be invisible while entering.
# 4. Displays client name and leave days, manager client is the same but also views the entire staff dictionary.

# This system uses a mini pseudo-database to emulate how our leave system will run in demo

# The library function we are using to encrypt our passwords 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# staff and manager mini databases, hash_password() function is used to convert passwords to string of encoded digits. 
manager_info = {
    "MAN01": {"password": hash_password("SuchIsLife"), "name": "Patrick", "Leave Available": 45}
}
staff_info = {
    "KGAS01": {"password": hash_password("4515449"), "name": "Kaleb", "Leave Available": 27},
    "MBAT02": {"password": hash_password("4540469"), "name": "Mbasa", "Leave Available": 32},
    "IKOL03": {"password": hash_password("4514785"), "name": "Inga", "Leave Available": 14},
    "TMOK04": {"password": hash_password("4564064"), "name": "Tshwaraganang", "Leave Available": 30},
    "AKRI05": {"password": hash_password("4556168"), "name": "Ayron", "Leave Available": 23},
    "SMAT06": {"password": hash_password("4546163"), "name": "Sekwele", "Leave Available": 10}
}

def manager_login():
    manager_running = True
    while manager_running:
        # os.system("clear")
        # Checks if Manager username is on the database and that the password matches, then moves to next display
        print("\nManager Login")
        man_id = input("\nEnter Manager Id: ")
        if man_id in manager_info:
            man_pass = stdiomask.getpass("Enter your Password: ").strip()
            if hash_password(man_pass) == manager_info[man_id]["password"]:
                os.system("clear")
                # displays manager name and their leave hours with the staff database
                print("\nWelcome!",manager_info[man_id]["name"],"you have",manager_info[man_id]["Leave Available"],"days of leave")
                # Manager doesn't have access to staff passwords as they are encrypted, but views other staff info.
                print("\n",staff_info)
                # testing purpose to see hash key for manager.
                # print(manager_info[man_id]["Manager Password"])
                break
            else:
                os.system("clear")
                print("Incorrect Password")
        else:
            os.system("clear")
            print("User not Found")
                    
def staff_login():
    staff_running = True
    while staff_running:
        # os.system("clear")
        # checks if Staff username is on the database and that the password matches, then moves to next display 
        print("\nStaff Login")
        staff_id = input("\nEnter Staff Id: ")
        if staff_id in staff_info:
            staff_pass = stdiomask.getpass("Enter your Password: ").strip()
            if hash_password(staff_pass) == staff_info[staff_id]["password"]:
                os.system("clear")
                # displays staff name and their leave hours
                print("\nWelcome!",staff_info[staff_id]["name"],"you have",staff_info[staff_id]["Leave Available"],"days of leave")
                # testing to see if hash function works for staff login
                # print(staff_info[staff_id]["Staff Passwords"])
                break
            else:
                os.system("clear")
                print("Incorrect Password")
        else:
            os.system("clear")
            print("User not Found")

# os clears the terminal after each run
os.system("clear")
app_is_running = True
# Main while loop allows us to continuously run the app until certian criteria are met
while app_is_running:
    # these two print functions are just display for the user
    print("--- TagTeam Human Resources Leave System ---")
    print("\n-------- Are you the Manager? --------")

    # user inputs 'yes' or 'no', checks for all variations of the two
    choice = input("\nYes/No: ").strip().lower()
    # if the choice is one of the strings it will move to the next screen
    if choice in ("yes", "no", "y", "n"):
        if choice in ("yes", "y"):
            manager_login()
            break   
        elif choice in ("no", "n"):
            staff_login()
            break
    else:
        os.system("clear")
        print("\ntry yes or no.")   
else:
    # basically gets rid of any inputs other than yes or no
    os.system("clear")
    print("\ntry yes or no.")