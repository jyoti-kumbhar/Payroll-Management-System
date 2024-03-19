import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class LoginWindow:
    def __init__(self, master, app):
        self.master = master
        self.master.title("Login")
        self.master.state('zoomed')

        # configure row and column
        self.master.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.master.grid_rowconfigure(5, weight=5)
        self.master.grid_columnconfigure((0,1,2), weight=10)

        # GUI of login window
        self.label_username = tk.Label(self.master, text="Username:", bg="lightblue", font=("Arial", 12))
        self.label_username.grid(row=0, column=1, sticky='s', columnspan=1, padx=10, pady=10, ipadx=10, ipady=10)
        self.entry_username = tk.Entry(self.master)
        self.entry_username.grid(row=1, column=1, sticky='n')

        self.label_password = tk.Label(self.master, text="Password:", bg="lightblue", font=("Arial", 12))
        self.label_password.grid(row=1, column=1, sticky='s', columnspan=1, padx=10, pady=10, ipadx=10, ipady=10)
        self.entry_password = tk.Entry(self.master, show='*')
        self.entry_password.grid(row=2, column=1, sticky='n')

        self.button_login = tk.Button(self.master, text="Login", command=self.login, bg="grey", fg="black", font=("Arial", 12, "bold"))
        self.button_login.grid(row=2, column=1, sticky='s', columnspan=1, padx=10, pady=10, ipadx=5, ipady=5)
        self.app = app

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Replace this with your authentication logic
        if username == "admin" and password == "password":
            self.master.destroy()  # Close the login window
            self.app.show_main_window()  # Show the main application window
        else:
            messagebox.showerror("Error", "Invalid username or password.")

class PayrollManagementSystem:
    def __init__(self, master):
        self.master = master

        # main window
        self.master.title("Payroll Management System")
        self.master.state('zoomed')
        self.master.withdraw()

        # login window
        self.login_window = tk.Toplevel(self.master)
        self.login = LoginWindow(self.login_window, self)

        # Database connection
        self.conn = sqlite3.connect('payroll.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS employees
                            (id INTEGER PRIMARY KEY, name TEXT, salary REAL)''')
        self.conn.commit()

    def show_main_window(self):
        self.master.deiconify()  # Show the main window

        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0, sticky='nsew')

        self.label_employee_id = tk.Label(self.frame, text="Employee ID:", bg="lightblue", font=("Arial", 12))
        self.label_employee_id.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_employee_id = tk.Entry(self.frame)
        self.entry_employee_id.grid(row=1, column=1, padx=10, pady=10)

        self.label_name = tk.Label(self.frame, text="Name:", bg="lightblue", font=("Arial", 12))
        self.label_name.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.grid(row=2, column=1, padx=10, pady=10)

        self.label_salary = tk.Label(self.frame, text="Salary:", bg="lightblue", font=("Arial", 12))
        self.label_salary.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_salary = tk.Entry(self.frame)
        self.entry_salary.grid(row=3, column=1, padx=10, pady=10)

        self.button_add_employee = tk.Button(self.frame, text="Add", command=self.add_employee, bg="light grey", fg='black', font=("Arial", 12))
        self.button_add_employee.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.button_display_employee = tk.Button(self.frame, text="View", command=self.display_existing_employees, bg="light grey", fg='black', font=("Arial", 12))
        self.button_display_employee.grid(row=4, column=1, columnspan=2, padx=10, pady=10,sticky='w')

        self.button_delete_employee = tk.Button(self.frame, text="Delete", command=self.delete_employee, bg="light grey", fg='black', font=("Arial", 12))
        self.button_delete_employee.grid(row=4, column=2, columnspan=2, padx=10, pady=10,sticky='w')

        self.button_calculate_payroll = tk.Button(self.frame, text="Calculate Payroll", command=self.calculate_payroll_window, bg="light grey", fg='black', font=("Arial", 12))
        self.button_calculate_payroll.grid(row=4, column=3, columnspan=2, padx=10, pady=10, sticky='e')

        self.label_search = tk.Label(self.frame, text="Search Employee:", bg="lightblue", font=("Arial", 12))
        self.label_search.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.entry_search = tk.Entry(self.frame)
        self.entry_search.grid(row=5, column=1, padx=10, pady=10)
        self.button_search = tk.Button(self.frame, text="Search", command=self.search_employee, bg="light grey", fg='black', font=("Arial", 12))
        self.button_search.grid(row=5, column=2, padx=10, pady=10)

        self.display_frame = tk.Frame(self.master)
        self.display_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)

        self.label_existing_employees = tk.Label(self.display_frame, text="Existing Employees", font=('Helvetica', 12, 'bold'), bg="lightblue")

        self.tree = ttk.Treeview(self.display_frame, columns=('ID', 'Name', 'Salary'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Salary', text='Salary')
        self.tree.grid(row=1, column=0, columnspan=3)

        # Initialize display of existing employees
        self.display_existing_employees()
       
    def calculate_payroll_window(self):
        self.payroll_window = tk.Toplevel(self.master)
        self.payroll_window.state('zoomed')
        self.payroll_window.title("Calculate Payroll")

        # Define labels and entry fields for payroll calculation
        tk.Label(self.payroll_window, text="Employee ID:", bg="lightblue", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.employee_id_entry = tk.Entry(self.payroll_window)
        self.employee_id_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.payroll_window, text="Extra Hours Worked:", bg="lightblue", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.hours_worked_entry = tk.Entry(self.payroll_window)
        self.hours_worked_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.payroll_window, text="Calculate", command=self.calculate_payroll, bg="light grey", fg='black', font=("Arial", 12)).grid(row=3, columnspan=2, padx=10, pady=10)

        back_to_main_button = tk.Button(self.payroll_window, text="Back", command=self.show_main_window_from_payroll, bg="light grey", fg='black', font=("Arial", 12))
        back_to_main_button.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

    def show_main_window_from_payroll(self):
        self.payroll_window.withdraw()
        self.show_main_window()

    def calculate_payroll(self):
        employee_id = self.employee_id_entry.get()
        hours_worked = float(self.hours_worked_entry.get())

        # Fetch employee ID and salary from the database using the entered employee ID
        self.cur.execute("SELECT id, name, salary FROM employees WHERE id=?", (employee_id,))
        row = self.cur.fetchone()

        try:
            if row:
                emp_id, name, salary = row
                allowance = 2000  # Example allowance, you can adjust this value as needed
                hours = hours_worked * 100
                pay = salary + hours
                total_pay = pay + allowance

                # Create a new small window to display the payroll
                payroll_result_window = tk.Toplevel(self.master)
                payroll_result_window.title("Payroll Result")

                result_label = tk.Label(payroll_result_window, text=f"Employee Name: {name}\n Employee ID: {emp_id}\n Allowance: {2000}\n Total Pay: Rs.{total_pay}",font=("Arial", 12))
                result_label.pack(padx=20, pady=10)

                # Adjust window size
                payroll_result_window.geometry("300x200")

        except:
            messagebox.showerror("Error", "Employee not found.")

    def search_employee(self):
        search_query = self.entry_search.get().strip()

        if not search_query:
            messagebox.showerror("Error", "Please enter a search query.")
            return

        # Clear existing entries in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Retrieve employees matching the search query from the database
        self.cur.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + search_query + '%',))
        rows = self.cur.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)

        if not rows:
            messagebox.showinfo("Info", "No employees found matching the search query.")

    def add_employee(self):
        employee_id = self.entry_employee_id.get()
        name = self.entry_name.get()
        salary = self.entry_salary.get()

        if employee_id == '' or name == '' or salary == '':
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Error", "Invalid salary format.","Enter integer value")
            return


        self.cur.execute("INSERT INTO employees (id, name, salary) VALUES (?, ?, ?)",
                         (employee_id, name, salary))
        self.conn.commit()
        messagebox.showinfo("Success", "Employee added successfully.")

        self.entry_employee_id.delete(0, 'end')
        self.entry_name.delete(0, 'end')
        self.entry_salary.delete(0, 'end')

        # Refresh the displayed employees
        self.display_existing_employees()

    def delete_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an employee to delete.")
            return

        for item in selected_item:
            employee_id = self.tree.item(item, 'values')[0]
            self.cur.execute("DELETE FROM employees WHERE id=?", (employee_id,))
            self.conn.commit()

        messagebox.showinfo("Success", "Selected employee(s) deleted successfully.")
        self.display_existing_employees()

    def display_existing_employees(self):
        # Clear existing entries in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Retrieve existing employees from the database
        self.cur.execute("SELECT * FROM employees")
        rows = self.cur.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)
    
    def show_settings_window(self):
        self.settings_window.deiconify()

def main():
    root = tk.Tk()
    root.state('zoomed')
    LoginWindow.app = PayrollManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
