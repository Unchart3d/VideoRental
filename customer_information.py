import tkinter as tk
from tkinter import messagebox

class CustomerManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management")
        self.root.geometry("1000x600")

        # Customer Information Input Fields
        tk.Label(root, text="First Name").pack(pady=5)
        self.first_name_input = tk.Entry(root)
        self.first_name_input.pack(pady=5)

        tk.Label(root, text="Last Name").pack(pady=5)
        self.last_name_input = tk.Entry(root)
        self.last_name_input.pack(pady=5)

        tk.Label(root, text="Address").pack(pady=5)
        self.address_input = tk.Entry(root)
        self.address_input.pack(pady=5)

        tk.Label(root, text="Phone Number").pack(pady=5)
        self.phone_number_input = tk.Entry(root)
        self.phone_number_input.pack(pady=5)

        tk.Label(root, text="Email Address").pack(pady=5)
        self.email_input = tk.Entry(root)
        self.email_input.pack(pady=5)

        # Buttons for Actions
        self.add_customer_button = tk.Button(root, text="Add Customer", command=self.add_customer)
        self.add_customer_button.pack(pady=10)

        self.update_customer_button = tk.Button(root, text="Update Customer", command=self.update_customer)
        self.update_customer_button.pack(pady=10)

        self.delete_customer_button = tk.Button(root, text="Delete Customer", command=self.delete_customer)
        self.delete_customer_button.pack(pady=10)

        # Listbox to Display Customers
        self.customer_listbox = tk.Listbox(root)
        self.customer_listbox.pack(pady=20, fill=tk.BOTH, expand=True)

        self.customers = []

    def add_customer(self):
        first_name = self.first_name_input.get().strip()
        last_name = self.last_name_input.get().strip()
        address = self.address_input.get().strip()
        phone_number = self.phone_number_input.get().strip()
        email = self.email_input.get().strip()

        if not all([first_name, last_name, address, phone_number, email]):
            messagebox.showwarning("Input Error", "Please fill in all fields")
        else:
            customer = f"{first_name} {last_name} - {phone_number}"
            self.customers.append(customer)
            self.customer_listbox.insert(tk.END, customer)
            self.clear_fields()
            messagebox.showinfo("Success", "Customer added")

    def update_customer(self):
        selected_index = self.customer_listbox.curselection()
        if selected_index:
            first_name = self.first_name_input.get().strip()
            last_name = self.last_name_input.get().strip()
            address = self.address_input.get().strip()
            phone_number = self.phone_number_input.get().strip()
            email = self.email_input.get().strip()

            if not all([first_name, last_name, address, phone_number, email]):
                messagebox.showwarning("Input Error", "Please fill in all fields")
            else:
                customer = f"{first_name} {last_name} - {phone_number}"
                self.customers[selected_index[0]] = customer
                self.customer_listbox.delete(selected_index)
                self.customer_listbox.insert(selected_index, customer)
                self.clear_fields()
                messagebox.showinfo("Success", "Customer updated")
        else:
            messagebox.showwarning("Selection Error", "Please select a customer to update")

    def delete_customer(self):
        selected_index = self.customer_listbox.curselection()
        if selected_index:
            self.customers.pop(selected_index[0])
            self.customer_listbox.delete(selected_index)
            messagebox.showinfo("Success", "Customer deleted")
        else:
            messagebox.showwarning("Selection Error", "Please select a customer to delete")

    def clear_fields(self):
        self.first_name_input.delete(0, tk.END)
        self.last_name_input.delete(0, tk.END)
        self.address_input.delete(0, tk.END)
        self.phone_number_input.delete(0, tk.END)
        self.email_input.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManagementApp(root)
    root.mainloop()
