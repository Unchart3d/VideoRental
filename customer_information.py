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
        
        self.is_editing = False
        self.current_edit_index = None
        self.customers = []  # Moved to the correct place

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

        self.update_customer_button = tk.Button(root, text="Update Customer", command=self.edit_or_apply)
        self.update_customer_button.grid(row=3, column=1, padx=10, pady=10)

        self.delete_customer_button = tk.Button(root, text="Delete Customer", command=self.delete_customer)
        self.delete_customer_button.grid(row=3, column=2, padx=10, pady=10)

        self.save_to_file_button = tk.Button(root, text="Save to File", command=self.save_to_file)
        self.save_to_file_button.grid(row=3, column=3, padx=10, pady=10)

        # List Customers as a Table
        self.customer_tree = ttk.Treeview(root, columns=("First Name", "Last Name", "Email", "Address", "Phone Number"), show="headings")
        self.customer_tree.heading("First Name", text="First Name")
        self.customer_tree.heading("Last Name", text="Last Name")
        self.customer_tree.heading("Email", text="Email")
        self.customer_tree.heading("Address", text="Address")
        self.customer_tree.heading("Phone Number", text="Phone Number")
        self.customer_tree.grid(row=4, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

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
            # Create Customer object
            customer = Customer(first_name, last_name, address, phone_number, email)
            self.customers.append(customer)
            self.customer_tree.insert("", tk.END, values=(first_name, last_name, email, address, phone_number))
            self.clear_fields()
            messagebox.showinfo("Success", "Customer added")

    def edit_or_apply(self):
        if not self.is_editing:
            self.update_customer()
        else:
            self.apply_edits()

    def update_customer(self):
        self.add_customer_button.config(state="disabled")
        self.delete_customer_button.config(state="disabled")
        self.save_to_file_button.config(state="disabled")
        
        selected_item = self.customer_tree.selection()
        if selected_item:
            item = self.customer_tree.item(selected_item)
            customer = item['values']

            self.first_name_input.delete(0, tk.END)
            self.first_name_input.insert(0, customer[0])

            self.last_name_input.delete(0, tk.END)
            self.last_name_input.insert(0, customer[1])

            self.address_input.delete(0, tk.END)
            self.address_input.insert(0, customer[3])

            self.phone_number_input.delete(0, tk.END)
            self.phone_number_input.insert(0, customer[4])

            self.email_input.delete(0, tk.END)
            self.email_input.insert(0, customer[2])

            self.is_editing = True
            self.current_edit_index = self.customer_tree.index(selected_item)  # Correctly get the index
            self.update_customer_button.config(text="Apply Changes")
        else:
            messagebox.showwarning("Selection Error", "Please select a customer to update")

    def apply_edits(self):
        first_name = self.first_name_input.get().strip()
        last_name = self.last_name_input.get().strip()
        address = self.address_input.get().strip()
        phone_number = self.phone_number_input.get().strip()
        email = self.email_input.get().strip()

        if not all([first_name, last_name, address, phone_number, email]):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        selected_item = self.customer_tree.selection()
        if selected_item:
            # Get the index of the selected item
            index = self.customer_tree.index(selected_item[0])
            customer = self.customers[index]

            # Update customer attributes
            customer.firstName = first_name
            customer.lastName = last_name
            customer.address = address
            customer.phone = phone_number
            customer.email = email

            # Update the tree view item
            self.customer_tree.item(selected_item[0], values=(first_name, last_name, email, address, phone_number))
            
            self.add_customer_button.config(state="normal")
            self.delete_customer_button.config(state="normal")
            self.save_to_file_button.config(state="normal")

            self.clear_fields()
            self.is_editing = False
            self.current_edit_index = None
            self.update_customer_button.config(text="Update Customer")
            messagebox.showinfo("Success", "Customer updated successfully.")
        else:
            messagebox.showwarning("Edit Error", "No customer selected for editing.")

    def delete_customer(self):
        selected_item = self.customer_tree.selection()
        if selected_item:
            index = self.customer_tree.index(selected_item[0])  # Get the index of the selected item
            self.customers.pop(index)  # Remove the customer from the list
            self.customer_tree.delete(selected_item)  # Delete the item from the treeview
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
                file.write(f"{customer.firstName} - {customer.lastName} - {customer.email} - {customer.address} - {customer.phone}\n")
        messagebox.showinfo("Success", "Customer data saved to customers.txt")

    def open_file(self):
        if os.path.exists("customers.txt"):
            self.customer_tree.delete(*self.customer_tree.get_children())
            self.customers = []

            with open("customers.txt", 'r') as file:
                for line in file:
                    first_name, last_name, email, address, phone = line.strip().split(" - ")
                    customer = Customer(first_name, last_name, address, phone, email)
                    self.customers.append(customer)
                    self.customer_tree.insert("", tk.END, values=(first_name, last_name, email, address, phone))
                    
def get_customer_info_by_email(email, file_path="customers.txt"):
        with open(file_path, "r") as file:
            for line in file:
                customer_info = line.strip().split(" - ")
                if len(customer_info) == 5:
                    first_name, last_name, customer_email, address, phone_number = customer_info
                    if customer_email == email:
                        return {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": customer_email,
                            "address": address,
                            "phone": phone_number
                            }
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManagementApp(root)
    root.mainloop()
