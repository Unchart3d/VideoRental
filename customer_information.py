import tkinter as tk
from tkinter import messagebox, ttk
import os

class Customer:
    def __init__(self, firstName, lastName, address, phone, email):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.phone = phone
        self.email = email
        
    def __str__(self):
        return f"{self.firstName} | {self.lastName} | {self.address} | {self.phone} | {self.email}"
        
class CustomerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management")
        self.root.geometry("1000x500")

        # Customer Information 
        tk.Label(root, text="First Name").grid(row=0, column=0, padx=10, pady=10)
        self.first_name_input = tk.Entry(root)
        self.first_name_input.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Last Name").grid(row=0, column=2, padx=10, pady=10)
        self.last_name_input = tk.Entry(root)
        self.last_name_input.grid(row=0, column=3, padx=10, pady=10)

        tk.Label(root, text="Address").grid(row=1, column=0, padx=10, pady=10)
        self.address_input = tk.Entry(root)
        self.address_input.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Phone Number").grid(row=1, column=2, padx=10, pady=10)
        self.phone_number_input = tk.Entry(root)
        self.phone_number_input.grid(row=1, column=3, padx=10, pady=10)

        tk.Label(root, text="Email Address").grid(row=2, column=0, padx=10, pady=10)
        self.email_input = tk.Entry(root)
        self.email_input.grid(row=2, column=1, padx=10, pady=10)

        # Buttons for Actions
        self.add_customer_button = tk.Button(root, text="Add Customer", command=self.add_customer)
        self.add_customer_button.grid(row=3, column=0, padx=10, pady=10)

        self.update_customer_button = tk.Button(root, text="Update Customer", command=self.update_customer)
        self.update_customer_button.grid(row=3, column=1, padx=10, pady=10)

        self.delete_customer_button = tk.Button(root, text="Delete Customer", command=self.delete_customer)
        self.delete_customer_button.grid(row=3, column=2, padx=10, pady=10)

        self.save_to_file_button = tk.Button(root, text="Save to File", command=self.save_to_file)
        self.save_to_file_button.grid(row=3, column=3, padx=10, pady=10)

        #  list Customers as a Table
        self.customer_tree = ttk.Treeview(root, columns=("First Name", "Last Name", "Email", "Address", "Phone Number"), show="headings")
        self.customer_tree.heading("First Name", text="First Name")
        self.customer_tree.heading("Last Name", text="Last Name")
        self.customer_tree.heading("Email", text="Email")
        self.customer_tree.heading("Address", text="Address")
        self.customer_tree.heading("Phone Number", text="Phone Number")
        self.customer_tree.grid(row=4, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

        self.customers = []

        self.open_file()

    def add_customer(self):
        first_name = self.first_name_input.get().strip()
        last_name = self.last_name_input.get().strip()
        address = self.address_input.get().strip()
        phone_number = self.phone_number_input.get().strip()
        email = self.email_input.get().strip()

        if not all([first_name, last_name, address, phone_number, email]):
            messagebox.showwarning("Input Error", "Please fill in all fields")
        else:
            customer = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "address": address,
                "phone_number": phone_number
            }
            self.customers.append(customer)
            self.customer_tree.insert("", tk.END, values=(first_name, last_name, email, address, phone_number))
            self.clear_fields()
            messagebox.showinfo("Success", "Customer added")

    def update_customer(self):
        selected_item = self.customer_tree.selection()
        if selected_item:
            first_name = self.first_name_input.get().strip()
            last_name = self.last_name_input.get().strip()
            address = self.address_input.get().strip()
            phone_number = self.phone_number_input.get().strip()
            email = self.email_input.get().strip()

            if not all([first_name, last_name, address, phone_number, email]):
                messagebox.showwarning("Input Error", "Please fill in all fields")
            else:
                customer = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "address": address,
                    "phone_number": phone_number
                }
                index = self.customer_tree.index(selected_item)
                self.customers[index] = customer
                self.customer_tree.item(selected_item, values=(first_name, last_name, email, address, phone_number))
                self.clear_fields()
                messagebox.showinfo("Success", "Customer updated")
        else:
            messagebox.showwarning("Selection Error", "Please select a customer to update")

    def delete_customer(self):
        selected_item = self.customer_tree.selection()
        if selected_item:
            index = self.customer_tree.index(selected_item)
            self.customers.pop(index)
            self.customer_tree.delete(selected_item)
            messagebox.showinfo("Success", "Customer deleted")
        else:
            messagebox.showwarning("Selection Error", "Please select a customer to delete")

    def clear_fields(self):
        self.first_name_input.delete(0, tk.END)
        self.last_name_input.delete(0, tk.END)
        self.address_input.delete(0, tk.END)
        self.phone_number_input.delete(0, tk.END)
        self.email_input.delete(0, tk.END)

    def save_to_file(self):
        with open("customers.txt", "w") as file:
            for customer in self.customers:
                file.write(f"{customer['first_name']} - {customer['last_name']} - {customer['email']} - {customer['address']} - {customer['phone_number']}\n")
        messagebox.showinfo("Success", "Customer data saved to customers.txt")
        
    def open_file(self):
        if os.path.exists("customers.txt"):
            self.customer_tree.delete(*self.customer_tree.get_children())
            self.customers = []

            with open("customers.txt", 'r') as file:
                for line in file:
                    customer_info = line.strip().split(" - ")
                    if len(customer_info) == 5:
                        customer = {
                            "first_name": customer_info[0],
                            "last_name": customer_info[1],
                            "email": customer_info[2],
                            "address": customer_info[3],
                            "phone_number": customer_info[4]
                        }
                        self.customers.append(customer)
                        self.customer_tree.insert('', tk.END, values=(customer["first_name"], customer["last_name"], customer["email"], customer["address"], customer["phone_number"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManagementApp(root)
    root.mainloop()
